#!/usr/bin/env python3
"""EXP-040 development-only multi-timeframe information-content study."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from collections import Counter,defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss,log_loss,roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from engine_k_v0_1 import EXECUTION_MARKETS,download_pinned
from run_engine_k_v0_2_training_calibration import load_scoped_csv,clipped_logit
from mtf_information_v0_1 import (
    TARGET_R_MULTIPLES,
    FEATURE_SETS,
    build_candidate_rows,
    self_tests_mtf_information,
)

ROOT=Path(__file__).resolve().parents[2]
CACHE=Path("/tmp/exp040-mtf-context")
OUT=ROOT/"research/results"
OUT.mkdir(parents=True,exist_ok=True)

DEV_START=pd.Timestamp("2026-03-23",tz="UTC")
SEALED_START=pd.Timestamp("2026-07-01",tz="UTC")
PURGE=pd.Timedelta(minutes=120)
PRIMARY_RUNGS=("T40eq","T50eq")
FEATURE_ORDER=("LOCAL_M5","PLUS_M15","PLUS_H1","PLUS_H4_D1","PLUS_SESSION")

FOLDS=(
    {"id":"WF1","cal_start":"2026-04-06","eval_start":"2026-04-13","eval_end":"2026-04-27"},
    {"id":"WF2","cal_start":"2026-04-20","eval_start":"2026-04-27","eval_end":"2026-05-11"},
    {"id":"WF3","cal_start":"2026-05-04","eval_start":"2026-05-11","eval_end":"2026-05-25"},
    {"id":"WF4","cal_start":"2026-05-18","eval_start":"2026-05-25","eval_end":"2026-06-08"},
    {"id":"WF5","cal_start":"2026-06-01","eval_start":"2026-06-08","eval_end":"2026-06-22"},
    {"id":"WF6","cal_start":"2026-06-15","eval_start":"2026-06-22","eval_end":"2026-07-01"},
)

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


def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda:fh.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def encode(rows:list[dict],feature_set:str)->np.ndarray:
    cols=FEATURE_SETS[feature_set]
    data=[]
    for r in rows:
        f=r["features"]
        vals=[float(f[c]) for c in cols]
        vals.extend(1.0 if r["symbol"]==s else 0.0 for s in EXECUTION_MARKETS)
        vals.extend([
            1.0 if r["direction"]=="long" else 0.0,
            1.0 if r["direction"]=="short" else 0.0,
        ])
        data.append(vals)
    x=np.asarray(data,dtype=float)
    if x.ndim!=2 or not np.isfinite(x).all():
        raise RuntimeError(f"{feature_set}: invalid design matrix")
    return x


def ece(y:np.ndarray,p:np.ndarray,bins:int=10)->float:
    y=np.asarray(y,dtype=int); p=np.asarray(p,dtype=float)
    edges=np.linspace(0.0,1.0,bins+1)
    total=len(y)
    out=0.0
    for i in range(bins):
        lo,hi=edges[i],edges[i+1]
        mask=(p>=lo)&(p<(hi if i<bins-1 else hi+1e-15))
        n=int(mask.sum())
        if not n:
            continue
        out+=(n/total)*abs(float(p[mask].mean())-float(y[mask].mean()))
    return float(out)


def safe_auc(y,p):
    return float(roc_auc_score(y,p)) if len(np.unique(y))==2 else None


def metrics(y,p)->dict:
    y=np.asarray(y,dtype=int)
    p=np.clip(np.asarray(p,dtype=float),1e-9,1-1e-9)
    bins=[]
    edges=np.linspace(0,1,11)
    for i in range(10):
        lo,hi=edges[i],edges[i+1]
        mask=(p>=lo)&(p<(hi if i<9 else hi+1e-15))
        if mask.any():
            bins.append({
                "lo":float(lo),"hi":float(hi),"n":int(mask.sum()),
                "mean_pred":float(p[mask].mean()),
                "observed_rate":float(y[mask].mean()),
            })
    return {
        "n":int(len(y)),
        "positive_rate":float(y.mean()) if len(y) else None,
        "brier":float(brier_score_loss(y,p)),
        "log_loss":float(log_loss(y,p,labels=[0,1])),
        "roc_auc":safe_auc(y,p),
        "ece_10bin":ece(y,p),
        "calibration_bins":bins,
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
    pcal=platt.predict_proba(clipped_logit(pcal_raw))[:,1]
    peval=platt.predict_proba(clipped_logit(peval_raw))[:,1]

    return {
        "status":"ok",
        "fit_n":len(fit_rows),
        "calibration_n":len(cal_rows),
        "evaluation_n":len(eval_rows),
        "calibration_metrics":metrics(ycal,pcal),
        "evaluation_metrics":metrics(yeval,peval),
        "platt_coef":float(platt.coef_[0][0]),
        "platt_intercept":float(platt.intercept_[0]),
    },{
        "y":yeval,
        "p":peval,
        "rows":eval_rows,
    }


def qstats(values:list[float])->dict:
    if not values:
        return {"n":0}
    a=np.asarray(values,dtype=float)
    return {
        "n":len(values),
        "mean":float(a.mean()),
        "median":float(np.median(a)),
        "p10":float(np.quantile(a,0.10)),
        "p25":float(np.quantile(a,0.25)),
        "p75":float(np.quantile(a,0.75)),
        "p90":float(np.quantile(a,0.90)),
    }


def self_tests_runner()->list[str]:
    tests=[]
    assert len(FOLDS)==6
    for f in FOLDS:
        cs,es,ee=ts(f["cal_start"]),ts(f["eval_start"]),ts(f["eval_end"])
        assert DEV_START<cs<es<ee<=SEALED_START
        assert es-cs==pd.Timedelta(days=7)
        assert es-PURGE>cs
    tests.append("six_purged_chronological_folds")
    assert PRIMARY_RUNGS==("T40eq","T50eq")
    tests.append("primary_rungs_frozen")
    assert FEATURE_ORDER==tuple(FEATURE_SETS)
    tests.append("feature_order_frozen")
    return tests


def main():
    tests={
        "feature_label_module":self_tests_mtf_information(),
        "runner":self_tests_runner(),
    }

    data={}
    rows=[]
    for s in EXECUTION_MARKETS:
        path=download_pinned(s,CACHE)
        df=load_scoped_csv(path,s,SEALED_START)
        if df.empty or df["datetime"].max()>=SEALED_START:
            raise RuntimeError(f"{s}: protected-period leak")
        data[s]=df
        rows.extend(build_candidate_rows(s,df))

    if not rows:
        raise RuntimeError("no EXP-040 candidate rows")
    if max(r["decision_ts"] for r in rows)>=SEALED_START:
        raise RuntimeError("protected-period candidate leak")

    rows.sort(key=lambda r:(r["decision_ts"],r["symbol"],r["direction"]))

    md_counts=Counter((r["symbol"],r["direction"]) for r in rows)
    sample_gate={
        f"{s}_{d}":int(md_counts[(s,d)])
        for s in EXECUTION_MARKETS for d in ("long","short")
    }
    each_md_ge_500=all(v>=500 for v in sample_gate.values())

    fold_outputs=[]
    pooled_store={
        fs:{rung:[] for rung in TARGET_R_MULTIPLES}
        for fs in FEATURE_ORDER
    }
    class_integrity=True

    for fold in FOLDS:
        cs,es,ee=ts(fold["cal_start"]),ts(fold["eval_start"]),ts(fold["eval_end"])
        fit_end=cs-PURGE
        cal_end=es-PURGE
        fit_rows=[r for r in rows if DEV_START<=r["decision_ts"]<fit_end]
        cal_rows=[r for r in rows if cs<=r["decision_ts"]<cal_end]
        eval_rows=[r for r in rows if es<=r["decision_ts"]<ee]
        if not fit_rows or not cal_rows or not eval_rows:
            raise RuntimeError(f"{fold['id']}: empty split")

        fresult={
            "fold":fold["id"],
            "fit":[str(DEV_START),str(fit_end)],
            "calibration":[str(cs),str(cal_end)],
            "evaluation":[str(es),str(ee)],
            "fit_rows":len(fit_rows),
            "calibration_rows":len(cal_rows),
            "evaluation_rows":len(eval_rows),
            "feature_sets":{},
        }

        for fs in FEATURE_ORDER:
            fresult["feature_sets"][fs]={}
            for rung in TARGET_R_MULTIPLES:
                summary,pred=fit_predict(fit_rows,cal_rows,eval_rows,fs,rung)
                fresult["feature_sets"][fs][rung]=summary
                if summary["status"]!="ok":
                    if rung in PRIMARY_RUNGS:
                        class_integrity=False
                    continue
                for y,p,row in zip(pred["y"],pred["p"],pred["rows"]):
                    pooled_store[fs][rung].append({
                        "y":int(y),"p":float(p),
                        "symbol":row["symbol"],
                        "direction":row["direction"],
                        "fold":fold["id"],
                        "decision_ts":str(row["decision_ts"]),
                    })
        fold_outputs.append(fresult)

    pooled={}
    for fs in FEATURE_ORDER:
        pooled[fs]={}
        for rung in TARGET_R_MULTIPLES:
            xs=pooled_store[fs][rung]
            if not xs:
                pooled[fs][rung]={"status":"unavailable"}
                continue
            y=np.asarray([x["y"] for x in xs],dtype=int)
            p=np.asarray([x["p"] for x in xs],dtype=float)
            per_market={}
            for s in EXECUTION_MARKETS:
                mask=np.asarray([x["symbol"]==s for x in xs],dtype=bool)
                ys=y[mask]; ps=p[mask]
                per_market[s]=metrics(ys,ps) if len(ys) and len(np.unique(ys))==2 else {
                    "n":int(len(ys)),"status":"both_classes_required"
                }
            pooled[fs][rung]={
                "status":"ok",
                "metrics":metrics(y,p),
                "per_market":per_market,
            }

    comparisons={}
    baseline="LOCAL_M5"
    for fs in FEATURE_ORDER[1:]:
        comparisons[fs]={}
        for rung in TARGET_R_MULTIPLES:
            b=pooled[baseline][rung]
            e=pooled[fs][rung]
            if b.get("status")!="ok" or e.get("status")!="ok":
                comparisons[fs][rung]={"status":"unavailable"}
                continue
            bm=b["metrics"]; em=e["metrics"]
            fold_wins=0
            fold_deltas=[]
            for fr in fold_outputs:
                x=fr["feature_sets"][baseline][rung]
                z=fr["feature_sets"][fs][rung]
                if x.get("status")=="ok" and z.get("status")=="ok":
                    delta=float(x["evaluation_metrics"]["log_loss"]-z["evaluation_metrics"]["log_loss"])
                    fold_deltas.append({"fold":fr["fold"],"baseline_minus_enriched":delta})
                    if delta>0:
                        fold_wins+=1
            market_nonworse=0
            market_details={}
            for s in EXECUTION_MARKETS:
                xb=b["per_market"][s]; ze=e["per_market"][s]
                if "log_loss" in xb and "log_loss" in ze:
                    delta=float(xb["log_loss"]-ze["log_loss"])
                    nonworse=delta>=-1e-12
                    market_nonworse+=int(nonworse)
                    market_details[s]={
                        "baseline_minus_enriched_log_loss":delta,
                        "nonworse":nonworse,
                    }
                else:
                    market_details[s]={"status":"unavailable"}
            comparisons[fs][rung]={
                "status":"ok",
                "relative_log_loss_improvement":float(
                    (bm["log_loss"]-em["log_loss"])/bm["log_loss"]
                ),
                "absolute_brier_improvement":float(bm["brier"]-em["brier"]),
                "ece_change_enriched_minus_baseline":float(em["ece_10bin"]-bm["ece_10bin"]),
                "fold_log_loss_wins":int(fold_wins),
                "fold_log_loss_differences":fold_deltas,
                "market_log_loss_nonworse_count":int(market_nonworse),
                "market_details":market_details,
            }

    set_gates={}
    passers=[]
    for fs in FEATURE_ORDER[1:]:
        rung_gates={}
        for rung in PRIMARY_RUNGS:
            c=comparisons[fs][rung]
            ok=c.get("status")=="ok"
            rg={
                "relative_logloss_improvement_ge_1pct":bool(ok and c["relative_log_loss_improvement"]>=0.01),
                "brier_improves":bool(ok and c["absolute_brier_improvement"]>0),
                "fold_logloss_wins_ge_4_of_6":bool(ok and c["fold_log_loss_wins"]>=4),
                "ece_not_worse_by_more_than_0_01":bool(ok and c["ece_change_enriched_minus_baseline"]<=0.01),
                "market_logloss_nonworse_ge_5_of_8":bool(ok and c["market_log_loss_nonworse_count"]>=5),
            }
            rg["rung_pass"]=bool(all(rg.values()))
            rung_gates[rung]=rg
        set_pass=all(rung_gates[r]["rung_pass"] for r in PRIMARY_RUNGS)
        set_gates[fs]={"rungs":rung_gates,"feature_set_pass":bool(set_pass)}
        if set_pass:
            passers.append(fs)

    selected=passers[0] if passers else None
    disposition=(
        "STABLE_MTF_INFORMATION_ADVANTAGE_FOUND"
        if selected is not None
        else "NO_STABLE_MTF_INFORMATION_ADVANTAGE"
    )

    path_stats={
        "mfe_r":qstats([r["mfe_r"] for r in rows]),
        "mae_r":qstats([r["mae_r"] for r in rows]),
        "path_end_counts":dict(sorted(Counter(r["path_end"] for r in rows).items())),
        "target_positive_rates":{
            rung:float(np.mean([r["labels"][rung] for r in rows]))
            for rung in TARGET_R_MULTIPLES
        },
    }

    integrity={
        "each_market_direction_ge_500":each_md_ge_500,
        "primary_rungs_both_classes_all_folds":class_integrity,
        "protected_periods_sealed":True,
        "feature_sets_exactly_nested":True,
        "engine_r_outcomes_used":False,
    }
    integrity["integrity_pass"]=bool(all(integrity.values()))

    if not integrity["integrity_pass"]:
        disposition="INTEGRITY_FAIL_DO_NOT_INTERPRET"

    result={
        "experiment":"EXP-040",
        "stage":"development_only_mtf_structural_context_information_content",
        "tested_repository_sha":repo_sha(),
        "runner_sha256":sha256_file(Path(__file__)),
        "feature_module_sha256":sha256_file(ROOT/"research/code/mtf_information_v0_1.py"),
        "sklearn_version":sklearn.__version__,
        "scope":{
            "development_source":["2026-03-23","2026-06-30"],
            "parsed_market_data_max_timestamp":max(str(df["datetime"].max()) for df in data.values()),
            "secondary_test_loaded_or_labeled":False,
            "final_holdout_loaded_or_labeled":False,
            "engine_r_target_pnl_development_used":False,
        },
        "target_r_multiples":TARGET_R_MULTIPLES,
        "primary_rungs":PRIMARY_RUNGS,
        "feature_sets":{k:list(v) for k,v in FEATURE_SETS.items()},
        "model":{
            "type":"StandardScaler + LogisticRegression + Platt calibration",
            "base_params":BASE_MODEL_PARAMS,
            "platt_params":PLATT_PARAMS,
        },
        "folds":FOLDS,
        "purge_minutes":int(PURGE.total_seconds()/60),
        "self_tests":tests,
        "candidate_rows":len(rows),
        "market_direction_counts":sample_gate,
        "path_diagnostics":path_stats,
        "fold_results":fold_outputs,
        "pooled_metrics":pooled,
        "comparisons_vs_local_m5":comparisons,
        "information_advantage_gates":set_gates,
        "passing_feature_sets":passers,
        "selected_smallest_passing_feature_set":selected,
        "integrity":integrity,
        "disposition":disposition,
    }

    out=OUT/"EXP-040-mtf-structural-context-information-content-v0.1.json"
    out.write_text(json.dumps(result,indent=2,default=str)+"\n")

    print(json.dumps({
        "candidate_rows":len(rows),
        "passing_feature_sets":passers,
        "selected_smallest_passing_feature_set":selected,
        "integrity":integrity,
        "disposition":disposition,
        "secondary_test_loaded_or_labeled":False,
        "final_holdout_loaded_or_labeled":False,
    },indent=2))


if __name__=="__main__":
    main()
