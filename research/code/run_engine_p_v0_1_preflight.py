#!/usr/bin/env python3
"""EXP-036 Engine P v0.1 zero-outcome cross-market relative-strength preflight."""

from __future__ import annotations

import json
import statistics
from collections import Counter
from pathlib import Path

import pandas as pd

from engine_k_v0_1 import EXECUTION_MARKETS, download_pinned
from engine_m_v0_1 import build_mtf_bars
from engine_m_v0_2 import safe_deployability_overlay, self_tests_engine_m_v02
from engine_p_v0_1 import (
    metric_at_time,
    usd_score,
    factor_direction,
    setup_from_snapshot,
    find_limit_fill,
    self_tests_engine_p_v01,
)
from run_engine_k_v0_2_training_calibration import load_scoped_csv

ROOT=Path(__file__).resolve().parents[2]
CACHE=Path("/tmp/engine-p-v01-preflight")
OUT=ROOT/"research/results"
OUT.mkdir(parents=True,exist_ok=True)

START=pd.Timestamp("2026-03-23",tz="UTC")
SEALED_START=pd.Timestamp("2026-07-01",tz="UTC")


def synthetic_factor_tests()->list[str]:
    tests=[]
    dt=pd.Timestamp("2026-04-06T10:05:00Z")

    def m(mom,o,h,l,c):
        return {
            "status":"ok","decision_ts":dt,"trigger_start":dt-pd.Timedelta(minutes=5),
            "mom":mom,"open":o,"high":h,"low":l,"close":c,
        }

    weak_usd={
        "EURUSD":m(2.0,1.1000,1.1030,1.0990,1.1025),
        "GBPUSD":m(1.0,1.2000,1.2030,1.1990,1.2025),
        "AUDUSD":m(1.0,0.7000,0.7030,0.6990,0.7025),
        "USDJPY":m(-1.0,150.0,150.2,149.6,149.7),
        "USDCAD":m(-1.0,1.3000,1.3010,1.2960,1.2970),
        "USDCHF":m(-1.0,0.9000,0.9010,0.8960,0.8970),
        "XAUUSD":m(2.0,4400.0,4412.0,4398.0,4409.0),
        "EURJPY":m(2.0,164.0,164.6,163.9,164.5),
    }

    x=setup_from_snapshot("EURUSD",weak_usd)
    assert x["status"]=="armed" and x["direction"]=="long"
    assert x["usd_score"]<=-0.5
    tests.append("base_usd_long_factor_confirmation")

    g=setup_from_snapshot("XAUUSD",weak_usd)
    assert g["status"]=="armed" and g["direction"]=="long"
    tests.append("gold_uses_fx_usd_factor")

    ej=setup_from_snapshot("EURJPY",weak_usd)
    # USDJPY leg is negative here, so the cross must reject despite positive own/EUR momentum.
    assert ej["status"]=="cross_factor_failed"
    tests.append("eurjpy_two_leg_identity_rejects_disagreement")

    strong_usd={
        "EURUSD":m(-1.0,1.1025,1.1030,1.0990,1.0995),
        "GBPUSD":m(-1.0,1.2025,1.2030,1.1990,1.1995),
        "AUDUSD":m(-1.0,0.7025,0.7030,0.6990,0.6995),
        "USDJPY":m(2.0,149.7,150.4,149.6,150.3),
        "USDCAD":m(1.0,1.2970,1.3020,1.2960,1.3010),
        "USDCHF":m(1.0,0.8970,0.9020,0.8960,0.9010),
        "XAUUSD":m(-2.0,4409.0,4412.0,4398.0,4401.0),
        "EURJPY":m(-2.0,164.5,164.6,163.9,164.0),
    }
    uj=setup_from_snapshot("USDJPY",strong_usd)
    assert uj["status"]=="armed" and uj["direction"]=="long"
    assert uj["usd_score"]>=0.5
    tests.append("usd_quote_long_factor_confirmation")

    eurjpy_long=dict(weak_usd)
    eurjpy_long["USDJPY"]=m(1.0,149.7,150.2,149.6,150.1)
    ej2=setup_from_snapshot("EURJPY",eurjpy_long)
    assert ej2["status"]=="armed" and ej2["direction"]=="long"
    tests.append("eurjpy_two_leg_identity_accepts_alignment")

    return tests


def entry_usd_jpy_at(series:pd.Series|None,entry_ts:pd.Timestamp):
    if series is None:
        return None
    k=int(series.index.searchsorted(entry_ts,side="right"))-1
    if k<0:
        return None
    return float(series.iloc[k])


def main():
    tests={
        "engine_p_v01":self_tests_engine_p_v01(),
        "engine_m_v02_safe_overlay":self_tests_engine_m_v02(),
        "synthetic_factor":synthetic_factor_tests(),
    }

    data={}
    bars5={}
    for symbol in EXECUTION_MARKETS:
        path=download_pinned(symbol,CACHE)
        df=load_scoped_csv(path,symbol,SEALED_START)
        if df.empty or df["datetime"].max()>=SEALED_START:
            raise RuntimeError(f"{symbol}: protected-period leak")
        data[symbol]=df
        bars5[symbol]=build_mtf_bars(df)["m5"]

    usd_jpy_series=data["USDJPY"].set_index("datetime")["close"].sort_index()

    status={s:Counter() for s in EXECUTION_MARKETS}
    fill_status={s:Counter() for s in EXECUTION_MARKETS}
    blocked={s:0 for s in EXECUTION_MARKETS}
    pending_until={s:pd.Timestamp.min.tz_localize("UTC") for s in EXECUTION_MARKETS}
    signals={s:0 for s in EXECUTION_MARKETS}
    deployable={s:0 for s in EXECUTION_MARKETS}
    by_dir={s:{"long":0,"short":0} for s in EXECUTION_MARKETS}
    utility={s:Counter() for s in EXECUTION_MARKETS}
    safe_max={s:{"risk":None,"notional":None,"margin":None} for s in EXECUTION_MARKETS}
    examples={s:[] for s in EXECUTION_MARKETS}

    days=pd.date_range(START.normalize(),SEALED_START-pd.Timedelta(days=1),freq="D",tz="UTC")
    for day in days:
        if day.weekday()>=5:
            continue
        for mins in range(6*60+5,17*60+55+1,5):
            decision_ts=day+pd.Timedelta(minutes=mins)
            snapshot={s:metric_at_time(bars5[s],decision_ts) for s in EXECUTION_MARKETS}

            for symbol in EXECUTION_MARKETS:
                setup=setup_from_snapshot(symbol,snapshot)
                status[symbol][setup["status"]]+=1
                if setup["status"]!="armed":
                    continue

                if decision_ts<pending_until[symbol]:
                    blocked[symbol]+=1
                    continue

                fill=find_limit_fill(data[symbol],setup)
                pending_until[symbol]=fill["resolved_ts"]
                fill_status[symbol][fill["status"]]+=1
                if not fill.get("filled"):
                    continue

                entry=float(fill["entry"])
                stop=float(fill["stop"])
                uj=entry_usd_jpy_at(usd_jpy_series,fill["entry_ts"]) if symbol=="EURJPY" else None
                overlay=safe_deployability_overlay(symbol,entry,stop,uj)
                if overlay.get("reason") in (
                    "invalid_geometry","value_or_notional_unavailable",
                    "target_geometry_unavailable","invalid_stop_loss_per_lot"
                ):
                    continue

                signals[symbol]+=1
                by_dir[symbol][setup["direction"]]+=1
                utility[symbol][overlay["utility_band"]]+=1

                if overlay["deployable"]:
                    deployable[symbol]+=1
                    for key,field in (
                        ("risk","stop_risk_usd"),
                        ("notional","notional_usd"),
                        ("margin","margin_usd"),
                    ):
                        val=float(overlay[field])
                        prev=safe_max[symbol][key]
                        safe_max[symbol][key]=val if prev is None else max(prev,val)

                if len(examples[symbol])<5:
                    examples[symbol].append({
                        "decision_ts":str(decision_ts),
                        "direction":setup["direction"],
                        "own_mom":setup["own_mom"],
                        "usd_score":setup.get("usd_score"),
                        "eurusd_mom":setup.get("eurusd_mom"),
                        "usdjpy_mom":setup.get("usdjpy_mom"),
                        "entry_ts":str(fill["entry_ts"]),
                        "entry":entry,
                        "stop":stop,
                        "safe_overlay":overlay,
                    })

    markets={}
    per_market_gate={}
    total=0
    total_deployable=0
    total_utility=Counter()
    safety_ok=True

    for s in EXECUTION_MARKETS:
        markets[s]={
            "setup_status_counts":dict(sorted(status[s].items())),
            "blocked_due_pending_order":blocked[s],
            "fill_status_counts":dict(sorted(fill_status[s].items())),
            "filled_signal_paths":signals[s],
            "filled_by_direction":by_dir[s],
            "deployable_paths_safe_lot_ge_0_01":deployable[s],
            "utility_band_counts":dict(sorted(utility[s].items())),
            "safe_overlay_maxima":safe_max[s],
            "examples":examples[s],
        }
        per_market_gate[s]=signals[s]>=25 and by_dir[s]["long"]>0 and by_dir[s]["short"]>0
        total+=signals[s]
        total_deployable+=deployable[s]
        total_utility.update(utility[s])

        mx=safe_max[s]
        if mx["risk"] is not None and mx["risk"]>20.0+1e-9:
            safety_ok=False
        if mx["notional"] is not None and mx["notional"]>50000.0+1e-9:
            safety_ok=False
        if mx["margin"] is not None and mx["margin"]>100.0+1e-9:
            safety_ok=False

    gate={
        "each_market_ge_25_and_both_directions":all(per_market_gate.values()),
        "total_signal_paths_ge_300":total>=300,
        "safe_overlay_never_violates_caps":safety_ok,
        "protected_periods_sealed":True,
        "target_outcomes_calculated":False,
        "pnl_outcomes_calculated":False,
    }
    passed=bool(
        gate["each_market_ge_25_and_both_directions"]
        and gate["total_signal_paths_ge_300"]
        and gate["safe_overlay_never_violates_caps"]
        and gate["protected_periods_sealed"]
    )

    result={
        "experiment":"EXP-036",
        "engine":"Engine P v0.1",
        "stage":"zero_outcome_cross_market_relative_strength_preflight",
        "target_outcomes_calculated":False,
        "pnl_outcomes_calculated":False,
        "secondary_test_loaded_or_inspected":False,
        "final_holdout_loaded_or_inspected":False,
        "parsed_market_data_max_timestamp":str(max(df["datetime"].max() for df in data.values())),
        "tests":tests,
        "markets":markets,
        "per_market_gate":per_market_gate,
        "gate":gate,
        "totals":{
            "filled_signal_paths":total,
            "deployable_paths_safe_lot_ge_0_01":total_deployable,
            "utility_band_counts":dict(sorted(total_utility.items())),
        },
        "preflight_pass":passed,
    }

    out=OUT/"EXP-036-cross-market-relative-strength-preflight-v0.1.json"
    out.write_text(json.dumps(result,indent=2,default=str)+"\n")
    print(json.dumps({
        "preflight_pass":passed,
        "per_market_gate":per_market_gate,
        "totals":result["totals"],
        "target_outcomes_calculated":False,
        "pnl_outcomes_calculated":False,
        "secondary_test_loaded_or_inspected":False,
        "final_holdout_loaded_or_inspected":False,
    },indent=2))


if __name__=="__main__":
    main()
