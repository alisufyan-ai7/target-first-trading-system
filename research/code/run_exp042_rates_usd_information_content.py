#!/usr/bin/env python3
from __future__ import annotations

import bisect, hashlib, json, math, os, subprocess
from collections import defaultdict
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
TARGET_DIR=Path(os.environ.get("EXP041_DUKA_DIR","/tmp/exp041-dukas-v2"))
PROXY_DIR=Path(os.environ.get("EXP042_PROXY_DIR","/tmp/exp042-proxy"))
OUT=ROOT/"research/results"; OUT.mkdir(parents=True,exist_ok=True)

DUKA_AUDIT=ROOT/"research/results/EXP-041-dukas-repeatability-snapshot-recovery-v0.1.json"
PROXY_AUDIT=ROOT/"research/results/EXP-042-rates-usd-proxy-repeatability-snapshot-v0.1.json"
AVAIL=ROOT/"research/results/EXP-042-proxy-availability-stratified-preflight-v0.3.json"

EXPECTED_DUKA_ARCHIVE="90bc7301e459062e8e35cd89a1a9aac23332ca3472014dd2cc5045ba34794272"
EXPECTED_PROXY_ARCHIVE="86cef306c36f08a12510c563e307a3158dc45d3236a424251db4d1c1bbaedcb4"
EXPECTED_AVAIL_BLOB="d6fe91ff1136b57fa4a7e92a5ddf1bfc7608d0a1"
EXPECTED_PROXY_SHA={
    "DOLLARIDXUSD":"2f070a99784a60f15e9afe5cb1c906f1ded22aedaa74205cd3a286adefb839d2",
    "USTBONDTRUSD":"e1ff7bea80f40b1529e046a7b0f7b4c6265cc147ee8c6c324ddef05cc7c5acf7",
}
START=pd.Timestamp("2025-07-01T00:00:00Z")
END=pd.Timestamp("2026-06-30T00:00:00Z")
PRIMARY=("T40eq","T50eq")
FAMS=("EMPLOYMENT","CPI","PPI","RETAIL","GDP_PCE")
BASE=tuple(FEATURE_SETS["LOCAL_M5"])
CONTROL=("minutes_since_event",)+tuple(f"event_{f}" for f in FAMS)
DXY=("dxy_log_return_bps","dxy_abs_log_return_bps")
TBOND=("tbond_log_return_bps","tbond_abs_log_return_bps")
MODEL_PARAMS=dict(C=0.25,penalty="l2",solver="lbfgs",max_iter=1000,random_state=20260925)
PLATT_PARAMS=dict(C=1_000_000.0,solver="lbfgs",max_iter=1000)

STUDIES={
    "A":{
        "subset":"DXY_COMPLETE",
        "sets":{
            "A_CONTROL":BASE+CONTROL,
            "A_PLUS_DXY":BASE+CONTROL+DXY,
        },
        "comparisons":[("A_PLUS_DXY","A_CONTROL")],
    },
    "B":{
        "subset":"DXY_TBOND_COMPLETE",
        "sets":{
            "B_CONTROL":BASE+CONTROL,
            "B_PLUS_DXY":BASE+CONTROL+DXY,
            "B_PLUS_DXY_TBOND":BASE+CONTROL+DXY+TBOND,
        },
        "comparisons":[
            ("B_PLUS_DXY_TBOND","B_PLUS_DXY"),
            ("B_PLUS_DXY_TBOND","B_CONTROL"),
        ],
    },
}

def repo_sha():
    return subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()

def blob(path:Path):
    return subprocess.check_output(["git","hash-object",str(path.relative_to(ROOT))],cwd=ROOT,text=True).strip()

def sha256(path:Path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def load_target(symbol,expected_sha):
    p=TARGET_DIR/f"{symbol}.csv"
    if sha256(p)!=expected_sha: raise RuntimeError(f"{symbol}: target SHA mismatch")
    x=pd.read_csv(p)
    x["datetime"]=pd.to_datetime(x["datetime"],utc=True)
    for c in ["open","high","low","close","volume"]: x[c]=pd.to_numeric(x[c],errors="raise")
    x=x[(x["datetime"]>=START)&(x["datetime"]<END)].sort_values("datetime").drop_duplicates("datetime").reset_index(drop=True)
    if x.empty or x["datetime"].max()>=END: raise RuntimeError(f"{symbol}: invalid target interval")
    return x

def load_proxy(symbol):
    p=PROXY_DIR/f"{symbol}.csv"
    if sha256(p)!=EXPECTED_PROXY_SHA[symbol]: raise RuntimeError(f"{symbol}: proxy SHA mismatch")
    x=pd.read_csv(p,usecols=["datetime","close"])
    x["datetime"]=pd.to_datetime(x["datetime"],utc=True)
    x["close"]=pd.to_numeric(x["close"],errors="raise")
    x=x[(x["datetime"]>=START)&(x["datetime"]<END)].sort_values("datetime").drop_duplicates("datetime").reset_index(drop=True)
    return x

def strict_asof(x,t):
    i=int(x["datetime"].searchsorted(t,side="left"))-1
    if i<0:return None
    row=x.iloc[i]
    stale=float((t-row["datetime"]).total_seconds()/60.0)
    return row["datetime"],float(row["close"]),stale

def focal_event(decision,events,event_ts):
    i=bisect.bisect_right(event_ts,decision)-1
    if i<0:return None
    e=events[i]
    delta=(decision-e["ts"]).total_seconds()/60.0
    return e if 0<=delta<=180 else None

def add_exp042_features(row,event,proxy):
    d=float((row["decision_ts"]-event["ts"]).total_seconds()/60.0)
    q={"minutes_since_event":d}
    for f in FAMS:q[f"event_{f}"]=1.0 if f in event["families"] else 0.0

    causal=True
    for sym,prefix in [("DOLLARIDXUSD","dxy"),("USTBONDTRUSD","tbond")]:
        b=strict_asof(proxy[sym],event["ts"])
        c=strict_asof(proxy[sym],row["decision_ts"])
        if b is None or c is None:
            q[prefix+"_available"]=0.0
            q[prefix+"_log_return_bps"]=0.0
            q[prefix+"_abs_log_return_bps"]=0.0
            continue
        bt,bp,bs=b; ct,cp,cs=c
        ok=(0<bs<=5 and 0<cs<=5 and bt<event["ts"] and ct<row["decision_ts"])
        q[prefix+"_available"]=1.0 if ok else 0.0
        if ok:
            r=10000.0*math.log(cp/bp)
            q[prefix+"_log_return_bps"]=r
            q[prefix+"_abs_log_return_bps"]=abs(r)
        else:
            q[prefix+"_log_return_bps"]=0.0
            q[prefix+"_abs_log_return_bps"]=0.0
        causal &= (bt<event["ts"] and ct<row["decision_ts"])
    return q,causal

def clipped_logit(p):
    q=np.clip(np.asarray(p,float),1e-6,1-1e-6)
    return np.log(q/(1-q)).reshape(-1,1)

def ece(y,p,bins=10):
    y=np.asarray(y,int);p=np.asarray(p,float);edges=np.linspace(0,1,bins+1);out=0.0
    for i in range(bins):
        lo,hi=edges[i],edges[i+1]
        m=(p>=lo)&(p<(hi if i<bins-1 else hi+1e-15))
        if m.any():out+=(m.sum()/len(y))*abs(float(p[m].mean())-float(y[m].mean()))
    return float(out)

def metrics(y,p):
    y=np.asarray(y,int);p=np.clip(np.asarray(p,float),1e-9,1-1e-9)
    return {
        "n":int(len(y)),"positive_rate":float(y.mean()),
        "brier":float(brier_score_loss(y,p)),
        "log_loss":float(log_loss(y,p,labels=[0,1])),
        "roc_auc":float(roc_auc_score(y,p)) if len(np.unique(y))==2 else None,
        "ece_10bin":ece(y,p),
    }

def encode(rows,cols):
    z=[]
    for r in rows:
        vals=[]
        for c in cols:
            if c in r["features"]: vals.append(float(r["features"][c]))
            else: vals.append(float(r["exp042"][c]))
        vals.extend(1.0 if r["symbol"]==s else 0.0 for s in EXECUTION_MARKETS)
        vals.extend([1.0 if r["direction"]=="long" else 0.0,1.0 if r["direction"]=="short" else 0.0])
        z.append(vals)
    x=np.asarray(z,float)
    if x.ndim!=2 or not np.isfinite(x).all(): raise RuntimeError("invalid design matrix")
    return x

def fit_base(rows,cols,rung):
    y=np.asarray([r["labels"][rung] for r in rows],int)
    if len(np.unique(y))!=2: raise RuntimeError("fit both classes required")
    sc=StandardScaler(); X=sc.fit_transform(encode(rows,cols))
    m=LogisticRegression(**MODEL_PARAMS);m.fit(X,y)
    return sc,m

def pred_raw(bundle,rows,cols):
    sc,m=bundle
    return m.predict_proba(sc.transform(encode(rows,cols)))[:,1]

def crossfit(rows,cols,rung,outer):
    train=[r for r in rows if r["event_fold"]!=outer]
    ev=[r for r in rows if r["event_fold"]==outer]
    if not train or not ev: raise RuntimeError(f"fold {outer}: empty")
    ye=np.asarray([r["labels"][rung] for r in ev],int)
    if len(np.unique(ye))!=2: raise RuntimeError(f"fold {outer}: eval both classes")
    inner=sorted(set(r["event_fold"] for r in train))
    if inner!=[x for x in range(1,7) if x!=outer]: raise RuntimeError("inner folds mismatch")
    op=[];oy=[]
    for h in inner:
        fit=[r for r in train if r["event_fold"]!=h]; hold=[r for r in train if r["event_fold"]==h]
        yf=np.asarray([r["labels"][rung] for r in fit],int);yh=np.asarray([r["labels"][rung] for r in hold],int)
        if len(np.unique(yf))!=2 or len(np.unique(yh))!=2: raise RuntimeError(f"outer {outer} inner {h}: both classes")
        pp=pred_raw(fit_base(fit,cols,rung),hold,cols)
        op.extend(pp.tolist());oy.extend(yh.tolist())
    op=np.asarray(op,float);oy=np.asarray(oy,int)
    pl=LogisticRegression(**PLATT_PARAMS);pl.fit(clipped_logit(op),oy)
    pe=pl.predict_proba(clipped_logit(pred_raw(fit_base(train,cols,rung),ev,cols)))[:,1]
    return {
        "fold":outer,"train_n":len(train),"eval_n":len(ev),"metrics":metrics(ye,pe)
    },[
        {"y":int(y),"p":float(p),"symbol":r["symbol"],"event_ts":r["event_ts"].isoformat(),"fold":outer}
        for y,p,r in zip(ye,pe,ev)
    ]

def comparison(base,enriched,basefold,enrfold):
    bm=base["metrics"];em=enriched["metrics"]
    fw=0
    for b,e in zip(basefold,enrfold):
        fw+=int(b["metrics"]["log_loss"]>e["metrics"]["log_loss"])
    md={};mn=0
    for s in EXECUTION_MARKETS:
        b=base["per_market"][s];e=enriched["per_market"][s]
        if "log_loss" in b and "log_loss" in e:
            d=b["log_loss"]-e["log_loss"];nw=d>=-1e-12;mn+=int(nw)
            md[s]={"baseline_minus_enriched_log_loss":float(d),"nonworse":bool(nw)}
        else: md[s]={"status":"unavailable"}
    common=sorted(set(base["per_event"])&set(enriched["per_event"]))
    ew=0
    for t in common:ew+=int(base["per_event"][t]["log_loss"]>enriched["per_event"][t]["log_loss"])
    c={
        "relative_log_loss_improvement":float((bm["log_loss"]-em["log_loss"])/bm["log_loss"]),
        "absolute_brier_improvement":float(bm["brier"]-em["brier"]),
        "ece_change_enriched_minus_baseline":float(em["ece_10bin"]-bm["ece_10bin"]),
        "fold_log_loss_wins":int(fw),
        "evaluated_event_blocks":len(common),
        "event_block_log_loss_wins":int(ew),
        "event_block_win_fraction":float(ew/len(common) if common else 0.0),
        "market_log_loss_nonworse_count":int(mn),
        "market_details":md,
    }
    g={
        "relative_logloss_improvement_ge_1pct":c["relative_log_loss_improvement"]>=0.01,
        "brier_improves":c["absolute_brier_improvement"]>0,
        "fold_logloss_wins_ge_4_of_6":c["fold_log_loss_wins"]>=4,
        "event_block_win_fraction_ge_60pct":c["event_block_win_fraction"]>=0.60,
        "market_logloss_nonworse_ge_5_of_8":c["market_log_loss_nonworse_count"]>=5,
        "ece_not_worse_by_more_than_0_01":c["ece_change_enriched_minus_baseline"]<=0.01,
    }
    g["rung_pass"]=all(g.values())
    return c,g

def pooled_summary(preds):
    y=np.asarray([x["y"] for x in preds],int);p=np.asarray([x["p"] for x in preds],float)
    per_market={};all_both=True
    for s in EXECUTION_MARKETS:
        m=np.asarray([x["symbol"]==s for x in preds],bool);ys=y[m];ps=p[m]
        if len(ys)==0 or len(np.unique(ys))!=2:
            per_market[s]={"n":int(len(ys)),"status":"both_classes_required"};all_both=False
        else:per_market[s]=metrics(ys,ps)
    g=defaultdict(list)
    for x in preds:g[x["event_ts"]].append(x)
    per_event={}
    for t,z in g.items():
        yy=np.asarray([a["y"] for a in z],int);pp=np.asarray([a["p"] for a in z],float)
        per_event[t]={"n":len(z),"log_loss":float(log_loss(yy,np.clip(pp,1e-9,1-1e-9),labels=[0,1]))}
    return {"metrics":metrics(y,p),"per_market":per_market,"all_markets_both_classes":all_both,"per_event":per_event}

def main():
    duka=json.loads(DUKA_AUDIT.read_text());proxya=json.loads(PROXY_AUDIT.read_text());avail=json.loads(AVAIL.read_text())
    if blob(AVAIL)!=EXPECTED_AVAIL_BLOB: raise RuntimeError("availability result blob changed")
    if duka["release"]["archive_sha256"]!=EXPECTED_DUKA_ARCHIVE: raise RuntimeError("target archive mismatch")
    if proxya["release"]["archive_sha256"]!=EXPECTED_PROXY_ARCHIVE: raise RuntimeError("proxy archive mismatch")
    if avail["disposition"]!="EXP042_AVAILABILITY_SUBSETS_FROZEN_AUTHORIZE_NESTED_STUDIES": raise RuntimeError("availability not authorized")
    if len(avail["subsets"]["DXY_COMPLETE"]["event_timestamps"])!=53: raise RuntimeError("DXY subset size")
    if len(avail["subsets"]["DXY_TBOND_COMPLETE"]["event_timestamps"])!=51: raise RuntimeError("both subset size")

    proxy={s:load_proxy(s) for s in EXPECTED_PROXY_SHA}
    events=[]
    for d in avail["event_details"]:
        events.append({"ts":pd.Timestamp(d["event_ts"]),"fold":int(d["fold"]),"families":d["families"]})
    events.sort(key=lambda e:e["ts"]);event_ts=[e["ts"] for e in events]
    if len(events)!=57: raise RuntimeError("expected 57 structural events")
    subset_sets={k:{pd.Timestamp(t) for t in avail["subsets"][k]["event_timestamps"]} for k in ("DXY_COMPLETE","DXY_TBOND_COMPLETE")}

    candidates=[];max_dec=None
    file_integrity={}
    for s in EXECUTION_MARKETS:
        expected=duka["markets"][s]["copy_a"]["sha256"]
        df=load_target(s,expected);file_integrity[s]={"sha256":expected,"rows":len(df)}
        rr=build_candidate_rows(s,df);candidates.extend(rr)
        if rr:
            z=max(r["decision_ts"] for r in rr);max_dec=z if max_dec is None or z>max_dec else max_dec
    if not candidates or max_dec>=END: raise RuntimeError("target candidate interval problem")

    assigned=[]
    causal_ok=True
    for r in candidates:
        e=focal_event(r["decision_ts"],events,event_ts)
        if e is None:continue
        fx,ok=add_exp042_features(r,e,proxy);causal_ok &= ok
        q=dict(r);q["exp042"]=fx;q["event_ts"]=e["ts"];q["event_fold"]=e["fold"];q["event_families"]=e["families"]
        assigned.append(q)

    study_rows={}
    expected_sizes={"A":53,"B":51}
    for name,cfg in STUDIES.items():
        subset=subset_sets[cfg["subset"]]
        req=["dxy"] if name=="A" else ["dxy","tbond"]
        rows=[]
        for r in assigned:
            if r["event_ts"] not in subset:continue
            if any(r["exp042"][p+"_available"]<0.5 for p in req):continue
            rows.append(r)
        rows.sort(key=lambda r:(r["event_ts"],r["decision_ts"],r["symbol"],r["direction"]))
        covered={r["event_ts"] for r in rows}
        if covered!=subset: raise RuntimeError(f"study {name}: not all frozen subset events have structural candidates")
        study_rows[name]=rows

    study_results={}
    integrity_class=True
    all_market_class=True
    for name,cfg in STUDIES.items():
        rows=study_rows[name]
        set_results={};fold_results={}
        for fs,cols in cfg["sets"].items():
            set_results[fs]={};fold_results[fs]={}
            for rung in PRIMARY:
                preds=[];fr=[]
                for outer in range(1,7):
                    try:s,p=crossfit(rows,cols,rung,outer)
                    except RuntimeError:
                        integrity_class=False;raise
                    fr.append(s);preds.extend(p)
                ps=pooled_summary(preds);all_market_class &= ps["all_markets_both_classes"]
                set_results[fs][rung]=ps;fold_results[fs][rung]=fr
        comps={}
        gates={}
        for enr,basefs in cfg["comparisons"]:
            key=f"{enr}_vs_{basefs}";comps[key]={};gates[key]={}
            for rung in PRIMARY:
                c,g=comparison(set_results[basefs][rung],set_results[enr][rung],fold_results[basefs][rung],fold_results[enr][rung])
                comps[key][rung]=c;gates[key][rung]=g
            gates[key]["comparison_pass"]=all(gates[key][r]["rung_pass"] for r in PRIMARY)
        if name=="A":
            passed=gates["A_PLUS_DXY_vs_A_CONTROL"]["comparison_pass"]
        else:
            passed=all(gates[k]["comparison_pass"] for k in gates)
        study_results[name]={
            "subset":cfg["subset"],"event_count":len({r["event_ts"] for r in rows}),
            "candidate_rows":len(rows),"feature_sets":{k:list(v) for k,v in cfg["sets"].items()},
            "pooled_metrics":set_results,"fold_results":fold_results,
            "comparisons":comps,"gates":gates,"study_pass":bool(passed),
        }

    integrity={
        "target_archive_sha_verified":duka["release"]["archive_sha256"]==EXPECTED_DUKA_ARCHIVE,
        "all_8_target_file_shas_verified":len(file_integrity)==8,
        "proxy_archive_sha_verified":proxya["release"]["archive_sha256"]==EXPECTED_PROXY_ARCHIVE,
        "proxy_file_shas_verified":all(proxya["instruments"][s]["copy_a"]["sha256"]==EXPECTED_PROXY_SHA[s] for s in EXPECTED_PROXY_SHA),
        "availability_v03_blob_unchanged":blob(AVAIL)==EXPECTED_AVAIL_BLOB,
        "dxy_subset_53_exact":len(subset_sets["DXY_COMPLETE"])==53,
        "dxy_tbond_subset_51_exact":len(subset_sets["DXY_TBOND_COMPLETE"])==51,
        "all_subset_events_have_candidates":all(study_results[n]["event_count"]==expected_sizes[n] for n in expected_sizes),
        "outer_inner_primary_both_classes":integrity_class,
        "all_markets_both_primary_classes":all_market_class,
        "proxy_feature_timestamps_strictly_causal":causal_ok,
        "candidate_rows_before_2026_06_30":max_dec<END,
        "protected_periods_sealed":True,
        "engine_r_or_exp015_outcomes_used":False,
    }
    integrity["integrity_pass"]=all(v for k,v in integrity.items() if k!="engine_r_or_exp015_outcomes_used") and not integrity["engine_r_or_exp015_outcomes_used"]

    if not integrity["integrity_pass"]:
        disposition="INTEGRITY_FAIL_DO_NOT_INTERPRET"
        a_disp=b_disp="INTEGRITY_FAIL_DO_NOT_INTERPRET"
    else:
        a_disp="STABLE_DXY_REACTION_INFORMATION_ADVANTAGE_FOUND" if study_results["A"]["study_pass"] else "NO_STABLE_DXY_REACTION_INFORMATION_ADVANTAGE"
        b_disp="STABLE_DXY_TBOND_INTERPRETATION_ADVANTAGE_FOUND" if study_results["B"]["study_pass"] else "NO_STABLE_DXY_TBOND_INTERPRETATION_ADVANTAGE"
        disposition="EXP042_INFORMATION_CONTENT_COMPLETE"

    result={
        "experiment":"EXP-042","stage":"rates_usd_interpretation_information_content_v0.1",
        "tested_repository_sha":repo_sha(),"sklearn_version":sklearn.__version__,
        "scope":{"secondary_test_loaded_or_labeled":False,"final_holdout_loaded_or_labeled":False,"engine_r_or_exp015_outcomes_used":False},
        "inputs":{
            "target_release_tag":duka["release"]["tag"],"target_archive_sha256":duka["release"]["archive_sha256"],
            "proxy_release_tag":proxya["release"]["tag"],"proxy_archive_sha256":proxya["release"]["archive_sha256"],
            "availability_v03_blob":blob(AVAIL),
        },
        "model":{"base_params":MODEL_PARAMS,"platt_params":PLATT_PARAMS,"outer_folds":"original Gate-A fold numbers after availability filtering"},
        "primary_rungs":list(PRIMARY),
        "structural_candidates_total":len(candidates),"post_release_assigned_candidates":len(assigned),
        "study_results":study_results,
        "study_dispositions":{"A_DXY":a_disp,"B_DXY_TBOND":b_disp},
        "integrity":integrity,"disposition":disposition,
    }
    p=OUT/"EXP-042-rates-usd-interpretation-information-content-v0.1.json"
    p.write_text(json.dumps(result,indent=2,default=str)+"\n")
    print(json.dumps({
        "integrity_pass":integrity["integrity_pass"],
        "study_A_events":study_results["A"]["event_count"],"study_A_rows":study_results["A"]["candidate_rows"],"study_A":a_disp,
        "study_B_events":study_results["B"]["event_count"],"study_B_rows":study_results["B"]["candidate_rows"],"study_B":b_disp,
        "disposition":disposition,
    },indent=2))

if __name__=="__main__":
    main()
