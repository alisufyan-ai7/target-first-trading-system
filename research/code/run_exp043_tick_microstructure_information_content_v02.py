#!/usr/bin/env python3
"""EXP-043 v0.2 availability-defined quote/tick microstructure information-content study."""

from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from engine_k_v0_1 import EXECUTION_MARKETS
from mtf_information_v0_1 import FEATURE_SETS, build_candidate_rows
from run_engine_k_v0_2_training_calibration import clipped_logit

ROOT=Path(__file__).resolve().parents[2]
TARGET_DIR=Path(os.environ.get("EXP041_DUKA_DIR","/tmp/exp041-dukas-v2"))
MICRO_DIR=Path(os.environ.get("EXP043_MICRO_DIR","/tmp/exp043-microstructure"))
OUT=ROOT/"research/results"
OUT.mkdir(parents=True,exist_ok=True)

TARGET_AUDIT=ROOT/"research/results/EXP-041-dukas-repeatability-snapshot-recovery-v0.1.json"
MICRO_AUDIT=ROOT/"research/results/EXP-043-development-microstructure-snapshot-v0.1.json"\nSOURCE_DIAG=ROOT/"research/results/EXP-043-microstructure-availability-coverage-diagnostic-v0.1.json"

EXPECTED_TARGET_ARCHIVE="90bc7301e459062e8e35cd89a1a9aac23332ca3472014dd2cc5045ba34794272"
EXPECTED_MICRO_ARCHIVE="f95edf1f7762271941a1d24b3204c4640485d9e7b9b01440fbef86f521f52ca5"
EXPECTED_MICRO_AUDIT_BLOB="f1bc941e88ee809bf9810fe34d780e41e4530fe7"\nEXPECTED_SOURCE_DIAG_BLOB="c0f5a33d5a73495922280b241b037e0f81641f33"\nACTIVE_MARKETS=("XAUUSD","EURUSD","GBPUSD","USDJPY","EURJPY","USDCAD")\nEXCLUDED_SOURCE_MARKETS=("AUDUSD","USDCHF")

DEV_START=pd.Timestamp("2026-03-23T00:00:00Z")
DATA_END=pd.Timestamp("2026-06-30T00:00:00Z")
PURGE=pd.Timedelta(minutes=120)
PRIMARY_RUNGS=("T40eq","T50eq")
EPS=1e-9

FOLDS=(
    {"id":"WF1","cal_start":"2026-04-06","eval_start":"2026-04-13","eval_end":"2026-04-27"},
    {"id":"WF2","cal_start":"2026-04-20","eval_start":"2026-04-27","eval_end":"2026-05-11"},
    {"id":"WF3","cal_start":"2026-05-04","eval_start":"2026-05-11","eval_end":"2026-05-25"},
    {"id":"WF4","cal_start":"2026-05-18","eval_start":"2026-05-25","eval_end":"2026-06-08"},
    {"id":"WF5","cal_start":"2026-06-01","eval_start":"2026-06-08","eval_end":"2026-06-22"},
    {"id":"WF6","cal_start":"2026-06-15","eval_start":"2026-06-22","eval_end":"2026-07-01"},
)

BASE_COLS=tuple(FEATURE_SETS["LOCAL_M5"])
EXECUTION_COLS=(
    "spread_bps_recent",
    "spread_bps_p90_recent",
    "log_spread_ratio_5_to_60",
    "quote_age_recent_fraction",
)
PARTICIPATION_COLS=(
    "log_tick_activity_ratio_5_to_60",
    "log_interarrival_ratio_5_to_60",
    "price_update_fraction_recent",
    "log_quote_size_ratio_5_to_60",
    "distinct_timestamp_fraction_recent",
)
IMBALANCE_COLS=(
    "directional_imbalance_recent",
    "directional_imbalance_medium",
    "directional_heavy_balance_recent",
    "directional_imbalance_change_5_vs_30",
)
FEATURE_SETS_043={
    "LOCAL_M5":BASE_COLS,
    "PLUS_EXECUTION_COST_STATE":BASE_COLS+EXECUTION_COLS,
    "PLUS_PARTICIPATION_STATE":BASE_COLS+EXECUTION_COLS+PARTICIPATION_COLS,
    "PLUS_QUOTE_IMBALANCE_STATE":BASE_COLS+EXECUTION_COLS+PARTICIPATION_COLS+IMBALANCE_COLS,
}
FEATURE_ORDER=tuple(FEATURE_SETS_043)

BASE_MODEL_PARAMS=dict(
    C=0.25,
    penalty="l2",
    solver="lbfgs",
    max_iter=1000,
    random_state=20260925,
)
PLATT_PARAMS=dict(C=1_000_000.0,solver="lbfgs",max_iter=1000)


def ts(x:str)->pd.Timestamp:
    return pd.Timestamp(x,tz="UTC")


def repo_sha()->str:
    return subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()


def git_blob(path:Path)->str:
    return subprocess.check_output(
        ["git","hash-object",str(path.relative_to(ROOT))],
        cwd=ROOT,text=True,
    ).strip()


def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""):
            h.update(c)
    return h.hexdigest()


def load_target(symbol:str,expected_sha:str)->pd.DataFrame:
    p=TARGET_DIR/f"{symbol}.csv"
    if not p.exists():
        raise RuntimeError(f"{symbol}: target CSV missing")
    if sha256_file(p)!=expected_sha:
        raise RuntimeError(f"{symbol}: target SHA mismatch")
    x=pd.read_csv(p)
    if list(x.columns)!=["datetime","open","high","low","close","volume"]:
        raise RuntimeError(f"{symbol}: target schema mismatch")
    x["datetime"]=pd.to_datetime(x["datetime"],utc=True)
    for c in ["open","high","low","close","volume"]:
        x[c]=pd.to_numeric(x[c],errors="raise")
    x=x[(x["datetime"]>=DEV_START)&(x["datetime"]<DATA_END)].copy()
    x=x.sort_values("datetime").drop_duplicates("datetime",keep="last").reset_index(drop=True)
    if x.empty or x["datetime"].max()>=DATA_END:
        raise RuntimeError(f"{symbol}: invalid target scope")
    return x


def load_micro(symbol:str,expected_sha:str)->pd.DataFrame:
    p=MICRO_DIR/f"{symbol}.csv"
    if not p.exists():
        raise RuntimeError(f"{symbol}: micro CSV missing")
    if sha256_file(p)!=expected_sha:
        raise RuntimeError(f"{symbol}: micro SHA mismatch")
    x=pd.read_csv(p)
    required=[
        "minute_start_utc","tick_count","distinct_timestamp_count",
        "median_interarrival_ms","p90_interarrival_ms",
        "spread_bps_median","spread_bps_p90","spread_bps_last","last_quote_age_ms",
        "bid_update_count","ask_update_count","both_price_update_count",
        "bid_volume_median","ask_volume_median",
        "signed_quote_imbalance_mean","signed_quote_imbalance_median",
        "bid_heavy_fraction","ask_heavy_fraction",
    ]
    if list(x.columns)!=required:
        raise RuntimeError(f"{symbol}: micro schema mismatch")
    x["minute_start_utc"]=pd.to_datetime(x["minute_start_utc"],utc=True)
    for c in required[1:]:
        x[c]=pd.to_numeric(x[c],errors="coerce")
    x=x[(x["minute_start_utc"]>=DEV_START)&(x["minute_start_utc"]<DATA_END)].copy()
    x=x.sort_values("minute_start_utc").drop_duplicates("minute_start_utc",keep="last")
    return x.reset_index(drop=True)


def rolling_median(s:pd.Series,w:int)->pd.Series:
    return s.rolling(w,min_periods=1).median()


def rolling_sum(s:pd.Series,w:int)->pd.Series:
    return s.rolling(w,min_periods=1).sum()


def build_micro_decision_features(x:pd.DataFrame)->pd.DataFrame:
    raw=x.set_index("minute_start_utc")
    rows=[]

    start_day=DEV_START.normalize()
    end_day=(DATA_END-pd.Timedelta(days=1)).normalize()
    days=pd.date_range(start_day,end_day,freq="D",tz="UTC")

    for day in days:
        if day.weekday()>=5:
            continue
        idx=pd.date_range(day+pd.Timedelta(hours=5),day+pd.Timedelta(hours=17,minutes=59),freq="1min",tz="UTC")
        d=raw.reindex(idx)
        obs=d["tick_count"].notna().astype(float)

        cov5=rolling_sum(obs,5)
        cov30=rolling_sum(obs,30)
        cov60=rolling_sum(obs,60)

        spread5=rolling_median(d["spread_bps_median"],5)
        spread60=rolling_median(d["spread_bps_median"],60)
        spread_p90_5=rolling_median(d["spread_bps_p90"],5)
        quote_age5=rolling_median(d["last_quote_age_ms"],5)/60000.0

        tick0=d["tick_count"].fillna(0.0)
        tick5=rolling_sum(tick0,5)
        tick60=rolling_sum(tick0,60)
        tick_mean5=tick5/cov5.replace(0,np.nan)
        tick_mean60=tick60/cov60.replace(0,np.nan)

        inter5=rolling_median(d["median_interarrival_ms"],5)
        inter60=rolling_median(d["median_interarrival_ms"],60)

        any_update=(
            d["bid_update_count"].fillna(0.0)
            +d["ask_update_count"].fillna(0.0)
            -d["both_price_update_count"].fillna(0.0)
        )
        update5=rolling_sum(any_update,5)
        transition0=(d["tick_count"].fillna(0.0)-1.0).clip(lower=0.0)
        transitions5=rolling_sum(transition0,5)
        update_frac5=update5/transitions5.clip(lower=1.0)

        quote_size=d["bid_volume_median"]+d["ask_volume_median"]
        quote_size5=rolling_median(quote_size,5)
        quote_size60=rolling_median(quote_size,60)

        distinct5=rolling_sum(d["distinct_timestamp_count"].fillna(0.0),5)
        distinct_frac5=distinct5/tick5.replace(0,np.nan)

        imb=d["signed_quote_imbalance_mean"]
        imb_weight=d["tick_count"].where(imb.notna(),0.0).fillna(0.0)
        imb_num=(imb.fillna(0.0)*imb_weight)
        imb5=rolling_sum(imb_num,5)/rolling_sum(imb_weight,5).replace(0,np.nan)
        imb30=rolling_sum(imb_num,30)/rolling_sum(imb_weight,30).replace(0,np.nan)

        heavy=d["bid_heavy_fraction"]-d["ask_heavy_fraction"]
        heavy_weight=d["tick_count"].where(heavy.notna(),0.0).fillna(0.0)
        heavy_num=heavy.fillna(0.0)*heavy_weight
        heavy5=rolling_sum(heavy_num,5)/rolling_sum(heavy_weight,5).replace(0,np.nan)

        feat=pd.DataFrame(index=idx)
        feat["micro_cov5"]=cov5
        feat["micro_cov30"]=cov30
        feat["micro_cov60"]=cov60
        feat["spread_bps_recent"]=spread5
        feat["spread_bps_p90_recent"]=spread_p90_5
        feat["log_spread_ratio_5_to_60"]=np.log((spread5+EPS)/(spread60+EPS))
        feat["quote_age_recent_fraction"]=quote_age5
        feat["log_tick_activity_ratio_5_to_60"]=np.log((tick_mean5+EPS)/(tick_mean60+EPS))
        feat["log_interarrival_ratio_5_to_60"]=np.log((inter5+EPS)/(inter60+EPS))
        feat["price_update_fraction_recent"]=update_frac5
        feat["log_quote_size_ratio_5_to_60"]=np.log((quote_size5+EPS)/(quote_size60+EPS))
        feat["distinct_timestamp_fraction_recent"]=distinct_frac5
        feat["imbalance_recent_raw"]=imb5
        feat["imbalance_medium_raw"]=imb30
        feat["heavy_balance_recent_raw"]=heavy5

        decision_minutes=pd.date_range(
            day+pd.Timedelta(hours=6,minutes=4),
            day+pd.Timedelta(hours=17,minutes=54),
            freq="5min",tz="UTC"
        )
        rows.append(feat.loc[decision_minutes])

    out=pd.concat(rows).sort_index()
    if out.index.has_duplicates:
        raise RuntimeError("micro decision feature index duplicated")
    return out


def attach_micro_features(rows:list[dict],micro_by_market:dict[str,pd.DataFrame]):
    out=[]
    broad=Counter()
    eligible=Counter()

    all_cols=list(EXECUTION_COLS+PARTICIPATION_COLS)
    raw_cols=["imbalance_recent_raw","imbalance_medium_raw","heavy_balance_recent_raw"]

    for r in rows:
        s=r["symbol"]
        broad[s]+=1
        key=r["decision_ts"]-pd.Timedelta(minutes=1)
        tab=micro_by_market[s]
        if key not in tab.index:
            continue
        z=tab.loc[key]
        if not (z["micro_cov5"]>=4 and z["micro_cov30"]>=24 and z["micro_cov60"]>=48):
            continue
        vals=[float(z[c]) for c in all_cols+raw_cols]
        if not np.isfinite(vals).all():
            continue

        sign=1.0 if r["direction"]=="long" else -1.0
        f={c:float(z[c]) for c in all_cols}
        f["directional_imbalance_recent"]=sign*float(z["imbalance_recent_raw"])
        f["directional_imbalance_medium"]=sign*float(z["imbalance_medium_raw"])
        f["directional_heavy_balance_recent"]=sign*float(z["heavy_balance_recent_raw"])
        f["directional_imbalance_change_5_vs_30"]=(
            f["directional_imbalance_recent"]-f["directional_imbalance_medium"]
        )

        q=dict(r)
        q["micro_features"]=f
        q["micro_last_minute_start"]=key
        out.append(q)
        eligible[s]+=1

    coverage={s:eligible[s]/broad[s] if broad[s] else 0.0 for s in ACTIVE_MARKETS}
    return out,dict(broad),dict(eligible),coverage


def encode(rows:list[dict],feature_set:str)->np.ndarray:
    cols=FEATURE_SETS_043[feature_set]
    vals=[]
    for r in rows:
        z=[]
        for c in cols:
            if c in r["features"]:
                z.append(float(r["features"][c]))
            else:
                z.append(float(r["micro_features"][c]))
        z.extend(1.0 if r["symbol"]==s else 0.0 for s in EXECUTION_MARKETS)
        z.extend([
            1.0 if r["direction"]=="long" else 0.0,
            1.0 if r["direction"]=="short" else 0.0,
        ])
        vals.append(z)
    x=np.asarray(vals,dtype=float)
    if x.ndim!=2 or not np.isfinite(x).all():
        raise RuntimeError(f"{feature_set}: invalid design matrix")
    return x


def ece(y,p,bins=10):
    y=np.asarray(y,dtype=int);p=np.asarray(p,dtype=float)
    edges=np.linspace(0,1,bins+1);out=0.0
    for i in range(bins):
        lo,hi=edges[i],edges[i+1]
        m=(p>=lo)&(p<(hi if i<bins-1 else hi+1e-15))
        if m.any():
            out+=(m.sum()/len(y))*abs(float(p[m].mean())-float(y[m].mean()))
    return float(out)


def metrics(y,p):
    y=np.asarray(y,dtype=int)
    p=np.clip(np.asarray(p,dtype=float),1e-9,1-1e-9)
    return {
        "n":int(len(y)),
        "positive_rate":float(y.mean()),
        "brier":float(brier_score_loss(y,p)),
        "log_loss":float(log_loss(y,p,labels=[0,1])),
        "roc_auc":float(roc_auc_score(y,p)) if len(np.unique(y))==2 else None,
        "ece_10bin":ece(y,p),
    }


def fit_predict(fit_rows,cal_rows,eval_rows,feature_set,rung):
    yfit=np.asarray([r["labels"][rung] for r in fit_rows],dtype=int)
    ycal=np.asarray([r["labels"][rung] for r in cal_rows],dtype=int)
    yeval=np.asarray([r["labels"][rung] for r in eval_rows],dtype=int)
    if len(np.unique(yfit))!=2 or len(np.unique(ycal))!=2 or len(np.unique(yeval))!=2:
        return {"status":"both_classes_required"},None

    model=Pipeline([
        ("scale",StandardScaler()),
        ("logit",LogisticRegression(**BASE_MODEL_PARAMS)),
    ])
    model.fit(encode(fit_rows,feature_set),yfit)
    pcal_raw=model.predict_proba(encode(cal_rows,feature_set))[:,1]
    peval_raw=model.predict_proba(encode(eval_rows,feature_set))[:,1]

    platt=LogisticRegression(**PLATT_PARAMS)
    platt.fit(clipped_logit(pcal_raw),ycal)
    peval=platt.predict_proba(clipped_logit(peval_raw))[:,1]

    summary={
        "status":"ok",
        "fit_n":len(fit_rows),
        "calibration_n":len(cal_rows),
        "evaluation_n":len(eval_rows),
        "evaluation_metrics":metrics(yeval,peval),
    }
    preds=[
        {
            "y":int(y),"p":float(p),
            "symbol":r["symbol"],"direction":r["direction"],
            "decision_ts":r["decision_ts"],
            "date":r["decision_ts"].date().isoformat(),
        }
        for y,p,r in zip(yeval,peval,eval_rows)
    ]
    return summary,preds


def pooled_summary(preds:list[dict]):
    y=np.asarray([x["y"] for x in preds],dtype=int)
    p=np.asarray([x["p"] for x in preds],dtype=float)
    per_market={}
    all_market_classes=True
    for s in EXECUTION_MARKETS:
        mask=np.asarray([x["symbol"]==s for x in preds],dtype=bool)
        ys=y[mask];ps=p[mask]
        if len(ys)==0 or len(np.unique(ys))!=2:
            per_market[s]={"n":int(len(ys)),"status":"both_classes_required"}
            all_market_classes=False
        else:
            per_market[s]=metrics(ys,ps)

    day_groups=defaultdict(list)
    for x in preds:
        day_groups[x["date"]].append(x)
    per_day={}
    for d,z in sorted(day_groups.items()):
        yy=np.asarray([a["y"] for a in z],dtype=int)
        pp=np.asarray([a["p"] for a in z],dtype=float)
        per_day[d]={
            "n":len(z),
            "log_loss":float(log_loss(yy,np.clip(pp,1e-9,1-1e-9),labels=[0,1])),
        }

    return {
        "metrics":metrics(y,p),
        "per_market":per_market,
        "all_markets_both_classes":all_market_classes,
        "per_day":per_day,
    }


def compare(base,enriched,base_folds,enr_folds):
    bm=base["metrics"];em=enriched["metrics"]
    fold_wins=0;fold_diffs=[]
    for b,e in zip(base_folds,enr_folds):
        delta=b["evaluation_metrics"]["log_loss"]-e["evaluation_metrics"]["log_loss"]
        fold_diffs.append({"fold":b["fold"],"baseline_minus_enriched":float(delta)})
        fold_wins+=int(delta>0)

    market_nonworse=0;market_details={}
    for s in EXECUTION_MARKETS:
        b=base["per_market"][s];e=enriched["per_market"][s]
        if "log_loss" in b and "log_loss" in e:
            delta=b["log_loss"]-e["log_loss"]
            nw=delta>=-1e-12
            market_nonworse+=int(nw)
            market_details[s]={"baseline_minus_enriched_log_loss":float(delta),"nonworse":bool(nw)}
        else:
            market_details[s]={"status":"unavailable"}

    common_days=sorted(set(base["per_day"])&set(enriched["per_day"]))
    day_wins=0;day_diffs=[]
    for d in common_days:
        delta=base["per_day"][d]["log_loss"]-enriched["per_day"][d]["log_loss"]
        day_diffs.append({"date":d,"baseline_minus_enriched":float(delta)})
        day_wins+=int(delta>0)
    day_win_fraction=day_wins/len(common_days) if common_days else 0.0

    return {
        "relative_log_loss_improvement":float((bm["log_loss"]-em["log_loss"])/bm["log_loss"]),
        "absolute_brier_improvement":float(bm["brier"]-em["brier"]),
        "ece_change_enriched_minus_baseline":float(em["ece_10bin"]-bm["ece_10bin"]),
        "fold_log_loss_wins":int(fold_wins),
        "fold_log_loss_differences":fold_diffs,
        "market_log_loss_nonworse_count":int(market_nonworse),
        "market_details":market_details,
        "paired_evaluation_days":len(common_days),
        "day_log_loss_wins":int(day_wins),
        "day_log_loss_win_fraction":float(day_win_fraction),
        "day_log_loss_differences":day_diffs,
    }


def self_tests():
    assert FEATURE_ORDER==(
        "LOCAL_M5","PLUS_EXECUTION_COST_STATE",
        "PLUS_PARTICIPATION_STATE","PLUS_QUOTE_IMBALANCE_STATE"
    )
    assert FEATURE_SETS_043["PLUS_EXECUTION_COST_STATE"][:len(BASE_COLS)]==BASE_COLS
    assert FEATURE_SETS_043["PLUS_PARTICIPATION_STATE"][:len(FEATURE_SETS_043["PLUS_EXECUTION_COST_STATE"])]==FEATURE_SETS_043["PLUS_EXECUTION_COST_STATE"]
    assert FEATURE_SETS_043["PLUS_QUOTE_IMBALANCE_STATE"][:len(FEATURE_SETS_043["PLUS_PARTICIPATION_STATE"])]==FEATURE_SETS_043["PLUS_PARTICIPATION_STATE"]
    assert len(FOLDS)==6
    return ["nested_feature_sets_exact","six_original_exp040_folds","primary_rungs_t40_t50"]


def main():
    target_audit=json.loads(TARGET_AUDIT.read_text())
    micro_audit=json.loads(MICRO_AUDIT.read_text())

    if target_audit["release"]["archive_sha256"]!=EXPECTED_TARGET_ARCHIVE:
        raise RuntimeError("target archive SHA mismatch")
    if micro_audit["release"]["archive_sha256"]!=EXPECTED_MICRO_ARCHIVE:
        raise RuntimeError("micro archive SHA mismatch")
    if not micro_audit["snapshot_integrity_pass"] or not micro_audit["release"]["created_or_verified_existing"]:
        raise RuntimeError("micro snapshot not frozen")
    if git_blob(MICRO_AUDIT)!=EXPECTED_MICRO_AUDIT_BLOB:
        raise RuntimeError("micro snapshot result blob changed")

    broad_rows=[]
    micro_by_market={}
    target_file_integrity={}
    micro_file_integrity={}

    for s in EXECUTION_MARKETS:
        target_sha=target_audit["markets"][s]["copy_a"]["sha256"]
        df=load_target(s,target_sha)
        target_file_integrity[s]={"sha256":target_sha,"rows":int(len(df))}
        broad_rows.extend(build_candidate_rows(s,df))

        micro_sha=micro_audit["markets"][s]["aggregate"]["sha256"]
        mx=load_micro(s,micro_sha)
        micro_file_integrity[s]={"sha256":micro_sha,"rows":int(len(mx))}
        micro_by_market[s]=build_micro_decision_features(mx)

    if not broad_rows:
        raise RuntimeError("no broad candidates")
    if max(r["decision_ts"] for r in broad_rows)>=DATA_END:
        raise RuntimeError("candidate protected-period leak")

    rows,broad_counts,eligible_counts,coverage=attach_micro_features(broad_rows,micro_by_market)
    rows.sort(key=lambda r:(r["decision_ts"],r["symbol"],r["direction"]))
    if not rows:
        raise RuntimeError("no microstructure-eligible candidates")

    md=Counter((r["symbol"],r["direction"]) for r in rows)
    md_counts={f"{s}_{d}":int(md[(s,d)]) for s in ACTIVE_MARKETS for d in ("long","short")}

    fold_results={fs:{rung:[] for rung in PRIMARY_RUNGS} for fs in FEATURE_ORDER}
    pooled_preds={fs:{rung:[] for rung in PRIMARY_RUNGS} for fs in FEATURE_ORDER}
    class_integrity=True

    for fold in FOLDS:
        cs,es,ee=ts(fold["cal_start"]),ts(fold["eval_start"]),ts(fold["eval_end"])
        fit_end=cs-PURGE
        cal_end=es-PURGE
        actual_eval_end=min(ee,DATA_END)
        fit_rows=[r for r in rows if DEV_START<=r["decision_ts"]<fit_end]
        cal_rows=[r for r in rows if cs<=r["decision_ts"]<cal_end]
        eval_rows=[r for r in rows if es<=r["decision_ts"]<actual_eval_end]
        if not fit_rows or not cal_rows or not eval_rows:
            raise RuntimeError(f"{fold['id']}: empty split")

        for fs in FEATURE_ORDER:
            for rung in PRIMARY_RUNGS:
                summary,preds=fit_predict(fit_rows,cal_rows,eval_rows,fs,rung)
                summary["fold"]=fold["id"]
                summary["fit_interval"]=[str(DEV_START),str(fit_end)]
                summary["calibration_interval"]=[str(cs),str(cal_end)]
                summary["evaluation_interval"]=[str(es),str(actual_eval_end)]
                fold_results[fs][rung].append(summary)
                if summary["status"]!="ok":
                    class_integrity=False
                    continue
                for p in preds:
                    p["fold"]=fold["id"]
                    pooled_preds[fs][rung].append(p)

    pooled={fs:{} for fs in FEATURE_ORDER}
    all_market_classes=True
    for fs in FEATURE_ORDER:
        for rung in PRIMARY_RUNGS:
            preds=pooled_preds[fs][rung]
            if not preds:
                pooled[fs][rung]={"status":"unavailable"}
                all_market_classes=False
            else:
                pooled[fs][rung]=pooled_summary(preds)
                all_market_classes &= pooled[fs][rung]["all_markets_both_classes"]

    comparisons={}
    gates={}
    passers=[]
    baseline="LOCAL_M5"
    for fs in FEATURE_ORDER[1:]:
        comparisons[fs]={}
        gates[fs]={"rungs":{}}
        for rung in PRIMARY_RUNGS:
            c=compare(
                pooled[baseline][rung],
                pooled[fs][rung],
                fold_results[baseline][rung],
                fold_results[fs][rung],
            )
            comparisons[fs][rung]=c
            rg={
                "relative_logloss_improvement_ge_1pct":c["relative_log_loss_improvement"]>=0.01,
                "brier_improves":c["absolute_brier_improvement"]>0,
                "fold_logloss_wins_ge_4_of_6":c["fold_log_loss_wins"]>=4,
                "ece_not_worse_by_more_than_0_01":c["ece_change_enriched_minus_baseline"]<=0.01,
                "market_logloss_nonworse_ge_5_markets":c["market_log_loss_nonworse_count"]>=5,
                "day_logloss_win_fraction_ge_55pct":c["day_log_loss_win_fraction"]>=0.55,
            }
            rg["rung_pass"]=all(rg.values())
            gates[fs]["rungs"][rung]=rg
        gates[fs]["feature_set_pass"]=all(gates[fs]["rungs"][r]["rung_pass"] for r in PRIMARY_RUNGS)
        if gates[fs]["feature_set_pass"]:
            passers.append(fs)

    selected=passers[0] if passers else None
    if selected=="PLUS_EXECUTION_COST_STATE":
        disposition="STABLE_EXECUTION_COST_INFORMATION_ADVANTAGE_FOUND"
    elif selected=="PLUS_PARTICIPATION_STATE":
        disposition="STABLE_PARTICIPATION_INFORMATION_ADVANTAGE_FOUND"
    elif selected=="PLUS_QUOTE_IMBALANCE_STATE":
        disposition="STABLE_QUOTE_IMBALANCE_INFORMATION_ADVANTAGE_FOUND"
    else:
        disposition="NO_STABLE_TICK_MICROSTRUCTURE_INFORMATION_ADVANTAGE"

    eval_days=sorted({
        p["date"]
        for rung in PRIMARY_RUNGS
        for p in pooled_preds["LOCAL_M5"][rung]
    })

    same_rows_check=True
    for rung in PRIMARY_RUNGS:
        base_keys=[(p["fold"],p["decision_ts"],p["symbol"],p["direction"]) for p in pooled_preds["LOCAL_M5"][rung]]
        for fs in FEATURE_ORDER[1:]:
            keys=[(p["fold"],p["decision_ts"],p["symbol"],p["direction"]) for p in pooled_preds[fs][rung]]
            same_rows_check &= keys==base_keys

    causal_micro=True
    for r in rows:
        causal_micro &= (r["micro_last_minute_start"]+pd.Timedelta(minutes=1)<=r["decision_ts"])

    integrity={
        "target_archive_sha_verified":target_audit["release"]["archive_sha256"]==EXPECTED_TARGET_ARCHIVE,
        "all_6_active_target_file_shas_verified":len(target_file_integrity)==6,
        "micro_archive_sha_verified":micro_audit["release"]["archive_sha256"]==EXPECTED_MICRO_ARCHIVE,
        "micro_snapshot_result_blob_unchanged":git_blob(MICRO_AUDIT)==EXPECTED_MICRO_AUDIT_BLOB,
        "all_6_active_micro_file_shas_verified":len(micro_file_integrity)==6,
        "micro_minutes_strictly_causal":bool(causal_micro),
        "same_eligible_rows_all_feature_sets":bool(same_rows_check),
        "source_diagnostic_blob_unchanged":git_blob(SOURCE_DIAG)==EXPECTED_SOURCE_DIAG_BLOB,\n        "source_diagnostic_exact_excluded_markets":tuple(source_diag.get("markets_below_90pct",[]))==EXCLUDED_SOURCE_MARKETS,\n        "active_market_universe_exact":tuple(ACTIVE_MARKETS)==("XAUUSD","EURUSD","GBPUSD","USDJPY","EURJPY","USDCAD"),\n        "micro_eligible_coverage_ge_90pct_each_active_market":all(coverage[s]>=0.90 for s in ACTIVE_MARKETS),
        "each_market_direction_ge_500":all(v>=500 for v in md_counts.values()),
        "primary_rungs_both_classes_all_folds":bool(class_integrity),
        "all_markets_both_classes_pooled":bool(all_market_classes),
        "paired_evaluation_days_ge_45":len(eval_days)>=45,
        "candidate_rows_before_2026_06_30":max(r["decision_ts"] for r in rows)<DATA_END,
        "protected_periods_sealed":True,
        "engine_r_or_exp015_outcomes_used":False,
    }
    integrity["integrity_pass"]=(
        all(v for k,v in integrity.items() if k!="engine_r_or_exp015_outcomes_used")
        and not integrity["engine_r_or_exp015_outcomes_used"]
    )
    if not integrity["integrity_pass"]:
        disposition="INTEGRITY_FAIL_DO_NOT_INTERPRET"

    result={
        "experiment":"EXP-043",
        "stage":"development_tick_microstructure_information_content_v0.2",
        "tested_repository_sha":repo_sha(),
        "sklearn_version":sklearn.__version__,
        "scope":{
            "development_interval":["2026-03-23T00:00:00Z","2026-06-30T00:00:00Z"],
            "secondary_test_loaded_or_labeled":False,
            "final_holdout_loaded_or_labeled":False,
            "engine_r_or_exp015_outcomes_used":False,
        },
        "inputs":{
            "target_release_tag":target_audit["release"]["tag"],
            "target_archive_sha256":target_audit["release"]["archive_sha256"],
            "micro_release_tag":micro_audit["release"]["tag"],
            "micro_archive_sha256":micro_audit["release"]["archive_sha256"],
            "micro_snapshot_result_blob":git_blob(MICRO_AUDIT),\n            "source_availability_diagnostic_blob":git_blob(SOURCE_DIAG),
        },
        "self_tests":self_tests(),\n        "active_markets":list(ACTIVE_MARKETS),\n        "excluded_source_markets":list(EXCLUDED_SOURCE_MARKETS),\n        "v01_reinterpreted":False,
        "primary_rungs":list(PRIMARY_RUNGS),
        "feature_sets":{k:list(v) for k,v in FEATURE_SETS_043.items()},
        "micro_windows_minutes":{"recent":5,"medium":30,"baseline":60},
        "micro_window_min_observed_minutes":{"recent":4,"medium":24,"baseline":48},
        "model":{
            "type":"StandardScaler + LogisticRegression + Platt calibration",
            "base_params":BASE_MODEL_PARAMS,
            "platt_params":PLATT_PARAMS,
        },
        "folds":FOLDS,
        "purge_minutes":int(PURGE.total_seconds()/60),
        "broad_candidate_rows":len(broad_rows),
        "microstructure_eligible_candidate_rows":len(rows),
        "broad_candidates_by_market":broad_counts,
        "eligible_candidates_by_market":eligible_counts,
        "microstructure_coverage_by_market":coverage,
        "market_direction_eligible_counts":md_counts,
        "evaluation_days":eval_days,
        "fold_results":fold_results,
        "pooled_metrics":pooled,
        "comparisons_vs_local_m5":comparisons,
        "information_advantage_gates":gates,
        "passing_feature_sets":passers,
        "selected_smallest_passing_feature_set":selected,
        "integrity":integrity,
        "disposition":disposition,
    }

    p=OUT/"EXP-043-tick-microstructure-information-content-v0.2.json"
    p.write_text(json.dumps(result,indent=2,default=str)+"\n")
    print(json.dumps({
        "broad_candidate_rows":len(broad_rows),
        "microstructure_eligible_candidate_rows":len(rows),
        "coverage_by_market":coverage,
        "evaluation_days":len(eval_days),
        "passing_feature_sets":passers,
        "selected":selected,
        "integrity_pass":integrity["integrity_pass"],
        "disposition":disposition,
    },indent=2))


if __name__=="__main__":
    main()
