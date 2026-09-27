#!/usr/bin/env python3
"""EXP-041 Gate-B macro/catalyst information-content study v0.1.

Uses immutable Dukascopy v2, frozen Gate-A macro layer/folds, and EXP-040
structural candidate/target mechanics. Development only.
"""

from __future__ import annotations

import bisect
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
from sklearn.preprocessing import StandardScaler

from engine_k_v0_1 import EXECUTION_MARKETS
from mtf_information_v0_1 import FEATURE_SETS, build_candidate_rows

ROOT=Path(__file__).resolve().parents[2]
DATA_DIR=Path(os.environ.get("EXP041_DUKA_DIR","/tmp/exp041-dukas-v2"))
OUT=ROOT/"research/results"
OUT.mkdir(parents=True,exist_ok=True)

DUKA_AUDIT=ROOT/"research/results/EXP-041-dukas-repeatability-snapshot-recovery-v0.1.json"
MACRO=ROOT/"research/data/EXP-041-official-macro-surprise-layer-v0.1.json"
MACRO_AUDIT=ROOT/"research/results/EXP-041-official-actual-reconciliation-v0.1.json"
GATE_A=ROOT/"research/results/EXP-041-final-gate-a-audit-v0.1.json"

EXPECTED_ARCHIVE_SHA="90bc7301e459062e8e35cd89a1a9aac23332ca3472014dd2cc5045ba34794272"
EXPECTED_MACRO_SHA="ec267643940733db4647d5d1dc5537099e3fc149ee7e0e9257b1b8786017c362"
START=pd.Timestamp("2025-07-01T00:00:00Z")
END=pd.Timestamp("2026-06-30T00:00:00Z")

PRIMARY_RUNGS=("T40eq","T50eq")
FEATURE_ORDER=("LOCAL_M5","PLUS_CATALYST_TIMING","PLUS_SURPRISE_MAGNITUDE")

BASE_COLS=tuple(FEATURE_SETS["LOCAL_M5"])
TIMING_COLS=(
    "minutes_to_next_event_clip60",
    "minutes_since_last_event_clip180",
    "pre_0_60",
    "post_0_15",
    "post_15_60",
    "post_60_180",
    "surprise_known",
    "event_EMPLOYMENT",
    "event_CPI",
    "event_PPI",
    "event_RETAIL",
    "event_GDP_PCE",
    "event_FOMC",
)
SURPRISE_COLS=(
    "mean_abs_scaled_surprise",
    "max_abs_scaled_surprise",
    "available_surprise_component_count",
    "conflict_flag",
)
MODEL_PARAMS=dict(C=0.25,penalty="l2",solver="lbfgs",max_iter=1000,random_state=20260925)
PLATT_PARAMS=dict(C=1_000_000.0,solver="lbfgs",max_iter=1000)
FAMILIES=("EMPLOYMENT","CPI","PPI","RETAIL","GDP_PCE","FOMC")


def repo_sha()->str:
    return subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()


def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda:fh.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def load_market(symbol:str,expected_sha:str)->pd.DataFrame:
    p=DATA_DIR/f"{symbol}.csv"
    if not p.exists():
        raise RuntimeError(f"{symbol}: snapshot CSV missing")
    observed=sha256_file(p)
    if observed!=expected_sha:
        raise RuntimeError(f"{symbol}: snapshot SHA mismatch")
    x=pd.read_csv(p)
    if list(x.columns)!=["datetime","open","high","low","close","volume"]:
        raise RuntimeError(f"{symbol}: unexpected schema")
    x["datetime"]=pd.to_datetime(x["datetime"],utc=True)
    for c in ["open","high","low","close","volume"]:
        x[c]=pd.to_numeric(x[c],errors="raise")
    x=x[(x["datetime"]>=START)&(x["datetime"]<END)].copy()
    x=x.sort_values("datetime").drop_duplicates("datetime",keep="last").reset_index(drop=True)
    if x.empty or x["datetime"].min()>START+pd.Timedelta(days=1) or x["datetime"].max()>=END:
        raise RuntimeError(f"{symbol}: invalid scoped interval")
    return x


def clipped_logit(p:np.ndarray)->np.ndarray:
    q=np.clip(np.asarray(p,dtype=float),1e-6,1-1e-6)
    return np.log(q/(1-q)).reshape(-1,1)


def ece(y,p,bins:int=10)->float:
    y=np.asarray(y,dtype=int); p=np.asarray(p,dtype=float)
    edges=np.linspace(0,1,bins+1)
    out=0.0
    for i in range(bins):
        lo,hi=edges[i],edges[i+1]
        mask=(p>=lo)&(p<(hi if i<bins-1 else hi+1e-15))
        if mask.any():
            out+=(mask.sum()/len(y))*abs(float(p[mask].mean())-float(y[mask].mean()))
    return float(out)


def metrics(y,p)->dict:
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


def macro_scale(component:str)->float:
    if component=="Non-Farm Employment Change":
        return 50_000.0
    if component in {
        "Unemployment Rate","Average Hourly Earnings m/m",
        "CPI m/m","Core CPI m/m","CPI y/y","Core CPI y/y",
        "PPI m/m","Core PPI m/m",
        "Core PCE Price Index m/m","Personal Income m/m","Personal Spending m/m",
    }:
        return 0.1
    if component in {"Retail Sales m/m","Core Retail Sales m/m"}:
        return 0.5
    if component in {"Advance GDP q/q","Prelim GDP q/q","Final GDP q/q"}:
        return 0.5
    raise RuntimeError(f"no frozen surprise scale for {component}")


def build_events(macro:dict,gate_a:dict):
    by_ts=defaultdict(list)
    for r in macro["records"]:
        by_ts[pd.Timestamp(r["official_release_timestamp_utc"])].append(r)

    fold_by_ts={}
    frozen_ts=[]
    for f in gate_a["chronological_folds"]:
        for s in f["block_timestamps"]:
            t=pd.Timestamp(s)
            if t in fold_by_ts:
                raise RuntimeError("duplicate frozen event timestamp")
            fold_by_ts[t]=int(f["fold"])
            frozen_ts.append(t)

    frozen_ts=sorted(frozen_ts)
    if len(frozen_ts)!=65 or set(frozen_ts)!=set(by_ts):
        raise RuntimeError("macro timestamp set differs from frozen Gate-A set")

    events=[]
    for t in frozen_ts:
        rs=by_ts[t]
        families=sorted(set(r["family"] for r in rs))
        scaled=[]
        for r in rs:
            if r.get("timing_only"):
                continue
            scale=macro_scale(r["selected_component"])
            scaled.append(float(r["surprise_native"])/scale)
        events.append({
            "ts":t,
            "fold":fold_by_ts[t],
            "families":families,
            "scaled_surprises":scaled,
        })
    return events


def macro_context(t:pd.Timestamp,events:list[dict],event_ts:list[pd.Timestamp]):
    # last <= t; next >= t
    li=bisect.bisect_right(event_ts,t)-1
    ni=bisect.bisect_left(event_ts,t)

    last=events[li] if li>=0 else None
    nxt=events[ni] if ni<len(events) else None

    candidates=[]
    if last is not None:
        d=(t-last["ts"]).total_seconds()/60.0
        if 0<=d<=180:
            candidates.append((abs(d),0,last,d))
    if nxt is not None:
        d=(t-nxt["ts"]).total_seconds()/60.0
        if -60<=d<=0:
            candidates.append((abs(d),0 if d>=0 else 1,nxt,d))

    # Deduplicate exact-timestamp last/next representation.
    uniq={}
    for item in candidates:
        key=item[2]["ts"]
        old=uniq.get(key)
        if old is None or (item[0],item[1],item[2]["ts"])<(old[0],old[1],old[2]["ts"]):
            uniq[key]=item
    candidates=list(uniq.values())

    if not candidates:
        return None

    candidates.sort(key=lambda z:(z[0],z[1],z[2]["ts"]))
    _,_,focal,delta=candidates[0]

    # Timing features use the global previous/next event, including an exact event.
    next_idx=bisect.bisect_left(event_ts,t)
    next_ev=events[next_idx] if next_idx<len(events) else None
    last_idx=bisect.bisect_right(event_ts,t)-1
    last_ev=events[last_idx] if last_idx>=0 else None

    mins_next=60.0 if next_ev is None else min(60.0,max(0.0,(next_ev["ts"]-t).total_seconds()/60.0))
    mins_last=180.0 if last_ev is None else min(180.0,max(0.0,(t-last_ev["ts"]).total_seconds()/60.0))

    known=bool(delta>=0 and focal["scaled_surprises"])
    vals=focal["scaled_surprises"] if known else []
    absvals=[abs(x) for x in vals]
    pos=any(x>0 for x in vals); neg=any(x<0 for x in vals)

    f={
        "minutes_to_next_event_clip60":float(mins_next),
        "minutes_since_last_event_clip180":float(mins_last),
        "pre_0_60":1.0 if -60<=delta<0 else 0.0,
        "post_0_15":1.0 if 0<=delta<15 else 0.0,
        "post_15_60":1.0 if 15<=delta<60 else 0.0,
        "post_60_180":1.0 if 60<=delta<=180 else 0.0,
        "surprise_known":1.0 if known else 0.0,
        "mean_abs_scaled_surprise":float(np.mean(absvals)) if absvals else 0.0,
        "max_abs_scaled_surprise":float(max(absvals)) if absvals else 0.0,
        "available_surprise_component_count":float(len(vals)),
        "conflict_flag":1.0 if pos and neg else 0.0,
    }
    for fam in FAMILIES:
        f[f"event_{fam}"]=1.0 if fam in focal["families"] else 0.0

    return {"focal":focal,"delta_minutes":float(delta),"features":f}


def attach_macro(rows:list[dict],events:list[dict])->list[dict]:
    ts=[e["ts"] for e in events]
    out=[]
    for r in rows:
        ctx=macro_context(r["decision_ts"],events,ts)
        if ctx is None:
            continue
        q=dict(r)
        q["macro_features"]=ctx["features"]
        q["event_ts"]=ctx["focal"]["ts"]
        q["event_fold"]=ctx["focal"]["fold"]
        q["event_families"]=ctx["focal"]["families"]
        q["event_delta_minutes"]=ctx["delta_minutes"]
        out.append(q)
    return out


def feature_cols(fs:str):
    if fs=="LOCAL_M5":
        return BASE_COLS
    if fs=="PLUS_CATALYST_TIMING":
        return BASE_COLS+TIMING_COLS
    if fs=="PLUS_SURPRISE_MAGNITUDE":
        return BASE_COLS+TIMING_COLS+SURPRISE_COLS
    raise KeyError(fs)


def encode(rows:list[dict],fs:str)->np.ndarray:
    cols=feature_cols(fs)
    data=[]
    for r in rows:
        vals=[]
        for c in cols:
            if c in r["features"]:
                vals.append(float(r["features"][c]))
            else:
                vals.append(float(r["macro_features"][c]))
        vals.extend(1.0 if r["symbol"]==s else 0.0 for s in EXECUTION_MARKETS)
        vals.extend([1.0 if r["direction"]=="long" else 0.0,1.0 if r["direction"]=="short" else 0.0])
        data.append(vals)
    x=np.asarray(data,dtype=float)
    if x.ndim!=2 or not np.isfinite(x).all():
        raise RuntimeError(f"{fs}: invalid design matrix")
    return x


def fit_base(rows:list[dict],fs:str,rung:str):
    y=np.asarray([r["labels"][rung] for r in rows],dtype=int)
    if len(np.unique(y))!=2:
        raise RuntimeError("base fit requires both classes")
    scaler=StandardScaler()
    x=scaler.fit_transform(encode(rows,fs))
    model=LogisticRegression(**MODEL_PARAMS)
    model.fit(x,y)
    return scaler,model


def predict_raw(bundle,rows:list[dict],fs:str)->np.ndarray:
    scaler,model=bundle
    return model.predict_proba(scaler.transform(encode(rows,fs)))[:,1]


def crossfit_outer(rows:list[dict],outer_fold:int,fs:str,rung:str):
    train=[r for r in rows if r["event_fold"]!=outer_fold]
    ev=[r for r in rows if r["event_fold"]==outer_fold]
    if not train or not ev:
        raise RuntimeError(f"outer fold {outer_fold}: empty split")

    ye=np.asarray([r["labels"][rung] for r in ev],dtype=int)
    if len(np.unique(ye))!=2:
        raise RuntimeError(f"outer fold {outer_fold}: eval both classes required")

    inner_folds=sorted(set(r["event_fold"] for r in train))
    if len(inner_folds)!=5:
        raise RuntimeError("expected five inner training folds")

    oof_p=[]; oof_y=[]
    for inner in inner_folds:
        inner_fit=[r for r in train if r["event_fold"]!=inner]
        inner_hold=[r for r in train if r["event_fold"]==inner]
        yf=np.asarray([r["labels"][rung] for r in inner_fit],dtype=int)
        yh=np.asarray([r["labels"][rung] for r in inner_hold],dtype=int)
        if len(np.unique(yf))!=2 or len(np.unique(yh))!=2:
            raise RuntimeError(f"outer {outer_fold} inner {inner}: both classes required")
        bundle=fit_base(inner_fit,fs,rung)
        pp=predict_raw(bundle,inner_hold,fs)
        oof_p.extend(pp.tolist()); oof_y.extend(yh.tolist())

    oof_p=np.asarray(oof_p,dtype=float); oof_y=np.asarray(oof_y,dtype=int)
    platt=LogisticRegression(**PLATT_PARAMS)
    platt.fit(clipped_logit(oof_p),oof_y)

    final_bundle=fit_base(train,fs,rung)
    raw_eval=predict_raw(final_bundle,ev,fs)
    p_eval=platt.predict_proba(clipped_logit(raw_eval))[:,1]

    return {
        "fold":outer_fold,
        "train_n":len(train),
        "eval_n":len(ev),
        "inner_calibration_n":len(oof_y),
        "metrics":metrics(ye,p_eval),
    },[
        {
            "y":int(y),"p":float(p),"symbol":r["symbol"],"direction":r["direction"],
            "event_ts":r["event_ts"].isoformat(),"fold":outer_fold,
            "decision_ts":r["decision_ts"].isoformat(),
        }
        for y,p,r in zip(ye,p_eval,ev)
    ]


def self_tests(events:list[dict],gate_a:dict):
    assert len(events)==65
    assert sorted(set(e["fold"] for e in events))==[1,2,3,4,5,6]
    assert PRIMARY_RUNGS==("T40eq","T50eq")
    assert FEATURE_ORDER==("LOCAL_M5","PLUS_CATALYST_TIMING","PLUS_SURPRISE_MAGNITUDE")
    assert feature_cols("PLUS_CATALYST_TIMING")==BASE_COLS+TIMING_COLS
    assert feature_cols("PLUS_SURPRISE_MAGNITUDE")==BASE_COLS+TIMING_COLS+SURPRISE_COLS
    # Exact fold timestamps must match Gate A.
    ga={pd.Timestamp(s) for f in gate_a["chronological_folds"] for s in f["block_timestamps"]}
    assert ga=={e["ts"] for e in events}
    return ["65_gate_a_events_exact","six_folds_exact","nested_macro_feature_sets","primary_rungs_exact"]


def main():
    duka=json.loads(DUKA_AUDIT.read_text())
    macro=json.loads(MACRO.read_text())
    macro_audit=json.loads(MACRO_AUDIT.read_text())
    gate_a=json.loads(GATE_A.read_text())

    if not gate_a.get("gate_a_pass"):
        raise RuntimeError("final Gate A did not pass")
    if gate_a.get("disposition")!="EXP041_GATE_A_PASS_AUTHORIZE_GATE_B_INFORMATION_CONTENT":
        raise RuntimeError("Gate A did not authorize Gate B")
    if sha256_file(MACRO)!=EXPECTED_MACRO_SHA or macro_audit["output"]["sha256"]!=EXPECTED_MACRO_SHA:
        raise RuntimeError("macro surprise-layer SHA mismatch")
    if duka["release"]["archive_sha256"]!=EXPECTED_ARCHIVE_SHA or not duka["release"]["created_or_verified_existing"]:
        raise RuntimeError("canonical Dukascopy release mismatch")

    events=build_events(macro,gate_a)
    tests=self_tests(events,gate_a)

    all_rows=[]
    market_data={}
    market_file_integrity={}
    for s in EXECUTION_MARKETS:
        expected=duka["markets"][s]["copy_a"]["sha256"]
        df=load_market(s,expected)
        market_data[s]=df
        market_file_integrity[s]={
            "sha256":expected,
            "rows_scoped":int(len(df)),
            "min_ts":df["datetime"].min().isoformat(),
            "max_ts":df["datetime"].max().isoformat(),
        }
        all_rows.extend(build_candidate_rows(s,df))

    if not all_rows:
        raise RuntimeError("no structural candidates")
    if max(r["decision_ts"] for r in all_rows)>=END:
        raise RuntimeError("candidate protected-period leak")

    eval_rows=attach_macro(all_rows,events)
    if not eval_rows:
        raise RuntimeError("no event-window candidates")
    eval_rows.sort(key=lambda r:(r["event_ts"],r["decision_ts"],r["symbol"],r["direction"]))

    event_counts=Counter(r["event_ts"].isoformat() for r in eval_rows)
    frozen_event_set={e["ts"].isoformat() for e in events}
    covered_event_set=set(event_counts)
    event_coverage_exact=covered_event_set==frozen_event_set

    fold_event_counts={}
    fold_row_counts={}
    for k in range(1,7):
        fold_event_counts[str(k)]=len({r["event_ts"] for r in eval_rows if r["event_fold"]==k})
        fold_row_counts[str(k)]=sum(r["event_fold"]==k for r in eval_rows)

    pooled_store={fs:{r:[] for r in PRIMARY_RUNGS} for fs in FEATURE_ORDER}
    fold_results={fs:{r:[] for r in PRIMARY_RUNGS} for fs in FEATURE_ORDER}
    class_integrity=True

    for fs in FEATURE_ORDER:
        for rung in PRIMARY_RUNGS:
            for outer in range(1,7):
                try:
                    summary,preds=crossfit_outer(eval_rows,outer,fs,rung)
                except RuntimeError:
                    class_integrity=False
                    raise
                fold_results[fs][rung].append(summary)
                pooled_store[fs][rung].extend(preds)

    pooled={}
    per_event={}
    for fs in FEATURE_ORDER:
        pooled[fs]={}
        per_event[fs]={}
        for rung in PRIMARY_RUNGS:
            xs=pooled_store[fs][rung]
            y=np.asarray([x["y"] for x in xs],dtype=int)
            p=np.asarray([x["p"] for x in xs],dtype=float)
            per_market={}
            market_both=True
            for s in EXECUTION_MARKETS:
                mask=np.asarray([x["symbol"]==s for x in xs],dtype=bool)
                ys=y[mask]; ps=p[mask]
                if len(ys)==0 or len(np.unique(ys))!=2:
                    market_both=False
                    per_market[s]={"n":int(len(ys)),"status":"both_classes_required"}
                else:
                    per_market[s]=metrics(ys,ps)
            pooled[fs][rung]={
                "metrics":metrics(y,p),
                "per_market":per_market,
                "all_markets_both_classes":market_both,
            }

            g=defaultdict(list)
            for x in xs: g[x["event_ts"]].append(x)
            per_event[fs][rung]={}
            for ets,z in sorted(g.items()):
                yy=np.asarray([a["y"] for a in z],dtype=int)
                pp=np.asarray([a["p"] for a in z],dtype=float)
                per_event[fs][rung][ets]={
                    "n":len(z),
                    "log_loss":float(log_loss(yy,np.clip(pp,1e-9,1-1e-9),labels=[0,1])),
                }

    comparisons={}
    gates={}
    passers=[]
    for fs in FEATURE_ORDER[1:]:
        comparisons[fs]={}
        gates[fs]={"rungs":{}}
        for rung in PRIMARY_RUNGS:
            bm=pooled["LOCAL_M5"][rung]["metrics"]
            em=pooled[fs][rung]["metrics"]

            fold_wins=0
            fold_deltas=[]
            for b,e in zip(fold_results["LOCAL_M5"][rung],fold_results[fs][rung]):
                d=b["metrics"]["log_loss"]-e["metrics"]["log_loss"]
                fold_deltas.append({"fold":b["fold"],"baseline_minus_enriched":float(d)})
                fold_wins+=int(d>0)

            event_deltas=[]
            event_wins=0
            common=sorted(set(per_event["LOCAL_M5"][rung])&set(per_event[fs][rung]))
            for ets in common:
                d=per_event["LOCAL_M5"][rung][ets]["log_loss"]-per_event[fs][rung][ets]["log_loss"]
                event_deltas.append({"event_ts":ets,"baseline_minus_enriched":float(d)})
                event_wins+=int(d>0)
            event_win_fraction=event_wins/len(common) if common else 0.0

            market_nonworse=0
            market_details={}
            for s in EXECUTION_MARKETS:
                b=pooled["LOCAL_M5"][rung]["per_market"][s]
                e=pooled[fs][rung]["per_market"][s]
                if "log_loss" in b and "log_loss" in e:
                    d=b["log_loss"]-e["log_loss"]
                    nw=d>=-1e-12
                    market_nonworse+=int(nw)
                    market_details[s]={"baseline_minus_enriched_log_loss":float(d),"nonworse":bool(nw)}
                else:
                    market_details[s]={"status":"unavailable"}

            c={
                "relative_log_loss_improvement":float((bm["log_loss"]-em["log_loss"])/bm["log_loss"]),
                "absolute_brier_improvement":float(bm["brier"]-em["brier"]),
                "ece_change_enriched_minus_baseline":float(em["ece_10bin"]-bm["ece_10bin"]),
                "fold_log_loss_wins":int(fold_wins),
                "fold_log_loss_differences":fold_deltas,
                "evaluated_event_blocks":len(common),
                "event_block_log_loss_wins":int(event_wins),
                "event_block_win_fraction":float(event_win_fraction),
                "event_block_log_loss_differences":event_deltas,
                "market_log_loss_nonworse_count":int(market_nonworse),
                "market_details":market_details,
            }
            comparisons[fs][rung]=c

            rg={
                "relative_logloss_improvement_ge_1pct":c["relative_log_loss_improvement"]>=0.01,
                "brier_improves":c["absolute_brier_improvement"]>0,
                "fold_logloss_wins_ge_4_of_6":c["fold_log_loss_wins"]>=4,
                "event_block_win_fraction_ge_60pct":c["event_block_win_fraction"]>=0.60,
                "market_logloss_nonworse_ge_5_of_8":c["market_log_loss_nonworse_count"]>=5,
                "ece_not_worse_by_more_than_0_01":c["ece_change_enriched_minus_baseline"]<=0.01,
            }
            rg["rung_pass"]=bool(all(rg.values()))
            gates[fs]["rungs"][rung]=rg

        gates[fs]["feature_set_pass"]=all(gates[fs]["rungs"][r]["rung_pass"] for r in PRIMARY_RUNGS)
        if gates[fs]["feature_set_pass"]: passers.append(fs)

    selected=passers[0] if passers else None
    if selected=="PLUS_CATALYST_TIMING":
        disposition="STABLE_MACRO_TIMING_INFORMATION_ADVANTAGE_FOUND"
    elif selected=="PLUS_SURPRISE_MAGNITUDE":
        disposition="STABLE_MACRO_SURPRISE_INFORMATION_ADVANTAGE_FOUND"
    else:
        disposition="NO_STABLE_MACRO_INFORMATION_ADVANTAGE"

    market_both=all(
        pooled[fs][r]["all_markets_both_classes"]
        for fs in FEATURE_ORDER for r in PRIMARY_RUNGS
    )
    integrity={
        "dukas_archive_sha_verified":duka["release"]["archive_sha256"]==EXPECTED_ARCHIVE_SHA,
        "all_8_market_files_verified":len(market_file_integrity)==8,
        "macro_surprise_layer_sha_verified":sha256_file(MACRO)==EXPECTED_MACRO_SHA,
        "final_gate_a_pass":bool(gate_a["gate_a_pass"]),
        "frozen_65_events_exact":len(events)==65,
        "frozen_six_fold_assignments_exact":True,
        "all_65_events_have_candidates":event_coverage_exact,
        "primary_outer_and_inner_both_classes":class_integrity,
        "all_markets_both_primary_classes":market_both,
        "candidate_rows_before_2026_06_30":max(r["decision_ts"] for r in all_rows)<END,
        "protected_periods_sealed":True,
        "engine_r_or_exp015_outcomes_used":False,
    }
    integrity["integrity_pass"]=all(v for k,v in integrity.items() if k!="engine_r_or_exp015_outcomes_used") and not integrity["engine_r_or_exp015_outcomes_used"]

    if not integrity["integrity_pass"]:
        disposition="INTEGRITY_FAIL_DO_NOT_INTERPRET"

    result={
        "experiment":"EXP-041",
        "stage":"gate_b_macro_catalyst_information_content_v0.1",
        "tested_repository_sha":repo_sha(),
        "sklearn_version":sklearn.__version__,
        "scope":{
            "market_data_interval":["2025-07-01T00:00:00Z","2026-06-30T00:00:00Z"],
            "secondary_test_loaded_or_labeled":False,
            "final_holdout_loaded_or_labeled":False,
            "engine_r_or_exp015_outcomes_used":False,
        },
        "inputs":{
            "dukas_release_tag":duka["release"]["tag"],
            "dukas_archive_sha256":duka["release"]["archive_sha256"],
            "macro_surprise_layer_sha256":sha256_file(MACRO),
            "gate_a_result_sha256":sha256_file(GATE_A),
        },
        "self_tests":tests,
        "primary_rungs":list(PRIMARY_RUNGS),
        "feature_sets":{
            "LOCAL_M5":list(BASE_COLS),
            "PLUS_CATALYST_TIMING":list(BASE_COLS+TIMING_COLS),
            "PLUS_SURPRISE_MAGNITUDE":list(BASE_COLS+TIMING_COLS+SURPRISE_COLS),
        },
        "model":{
            "type":"StandardScaler + LogisticRegression + nested fold OOF Platt calibration",
            "base_params":MODEL_PARAMS,
            "platt_params":PLATT_PARAMS,
            "outer_evaluation":"six frozen Gate-A event folds",
        },
        "structural_candidates_total":len(all_rows),
        "event_window_candidates":len(eval_rows),
        "event_candidate_counts":dict(sorted(event_counts.items())),
        "fold_event_counts":fold_event_counts,
        "fold_candidate_rows":fold_row_counts,
        "market_file_integrity":market_file_integrity,
        "fold_results":fold_results,
        "pooled_metrics":pooled,
        "comparisons_vs_local_m5":comparisons,
        "information_advantage_gates":gates,
        "passing_feature_sets":passers,
        "selected_smallest_passing_feature_set":selected,
        "integrity":integrity,
        "disposition":disposition,
    }

    p=OUT/"EXP-041-macro-catalyst-information-content-v0.1.json"
    p.write_text(json.dumps(result,indent=2,default=str)+"\n")

    print(json.dumps({
        "structural_candidates_total":len(all_rows),
        "event_window_candidates":len(eval_rows),
        "event_blocks_covered":len(covered_event_set),
        "passing_feature_sets":passers,
        "selected":selected,
        "integrity_pass":integrity["integrity_pass"],
        "disposition":disposition,
        "secondary_test_loaded_or_labeled":False,
        "final_holdout_loaded_or_labeled":False,
    },indent=2))


if __name__=="__main__":
    main()
