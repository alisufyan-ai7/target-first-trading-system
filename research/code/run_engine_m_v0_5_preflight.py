#!/usr/bin/env python3
"""EXP-031 Engine M v0.5 zero-outcome recent-H1-range preflight."""

from __future__ import annotations

import json
import statistics
from collections import Counter
from pathlib import Path

import pandas as pd

from engine_k_v0_1 import EXECUTION_MARKETS, download_pinned
from engine_m_v0_1 import build_mtf_bars, find_limit_fill, self_tests_engine_m
from engine_m_v0_2 import safe_deployability_overlay, self_tests_engine_m_v02
from engine_m_v0_5 import recent_h1_range_setup_at, self_tests_engine_m_v05
from run_engine_k_v0_2_training_calibration import load_scoped_csv
from run_engine_m_v0_1_preflight import synthetic_fill_tests

ROOT=Path(__file__).resolve().parents[2]
CACHE=Path("/tmp/engine-m-v05-preflight")
OUT=ROOT/"research/results"
OUT.mkdir(parents=True,exist_ok=True)

START=pd.Timestamp("2026-03-23",tz="UTC")
SEALED_START=pd.Timestamp("2026-07-01",tz="UTC")


def _base_fixture():
    h4=pd.DataFrame({
        "datetime":pd.to_datetime(["2026-04-06T00:00Z","2026-04-06T04:00Z"]),
        "available_ts":pd.to_datetime(["2026-04-06T04:00Z","2026-04-06T08:00Z"]),
        "open":[1.10,1.10],"high":[1.20,1.35],"low":[1.00,1.05],"close":[1.12,1.24],
    })
    h1=pd.DataFrame({
        "datetime":pd.to_datetime(["2026-04-06T06:00Z","2026-04-06T07:00Z"]),
        "available_ts":pd.to_datetime(["2026-04-06T07:00Z","2026-04-06T08:00Z"]),
        "open":[1.12,1.16],"high":[1.28,1.30],"low":[1.07,1.10],"close":[1.15,1.24],
    })
    m15=pd.DataFrame({
        "datetime":pd.to_datetime(["2026-04-06T08:00Z"]),
        "available_ts":pd.to_datetime(["2026-04-06T08:15Z"]),
        "open":[1.15],"high":[1.23],"low":[1.06],"close":[1.20],
    })
    m5=pd.DataFrame({
        "datetime":pd.to_datetime(["2026-04-06T08:05Z","2026-04-06T08:10Z"]),
        "available_ts":pd.to_datetime(["2026-04-06T08:10Z","2026-04-06T08:15Z"]),
        "open":[1.16,1.17],"high":[1.19,1.22],"low":[1.14,1.16],"close":[1.17,1.21],
    })
    return {"h4":h4,"h1":h1,"m15":m15,"m5":m5}


def synthetic_recent_h1_tests()->list[str]:
    tests=[]

    # Both H1_0 and H1_1 qualify; deterministic recency must select H1_0.
    bars=_base_fixture()
    x=recent_h1_range_setup_at(bars,0,"EURUSD")
    assert x["status"]=="armed"
    assert x["selected_h1"]=="H1_0" and x["selected_h1_rank"]==0
    assert x["s15_low"]<x["h1_low"] and x["s15_close"]>x["h1_low"]
    assert x["target_price"]<=x["h1_high"]
    tests.append("h1_0_preferred_when_both_qualify")

    # Make H1_0 fail sweep while H1_1 still qualifies.
    bars2=_base_fixture()
    bars2["h1"].loc[1,"low"]=1.05
    bars2["h1"].loc[0,"low"]=1.07
    bars2["m15"].loc[0,"low"]=1.06
    y=recent_h1_range_setup_at(bars2,0,"EURUSD")
    assert y["status"]=="armed"
    assert y["selected_h1"]=="H1_1" and y["selected_h1_rank"]==1
    tests.append("h1_1_fallback_only_after_h1_0_fail")

    # Equality at both candidate lows is not a sweep -> no arm.
    bars3=_base_fixture()
    bars3["h1"].loc[0,"low"]=1.06
    bars3["h1"].loc[1,"low"]=1.06
    bars3["m15"].loc[0,"low"]=1.06
    z=recent_h1_range_setup_at(bars3,0,"EURUSD")
    assert z["status"]=="no_recent_h1_range_qualified"
    assert len(z["candidate_failures"])==2
    tests.append("strict_equal_boundary_no_arm")

    # Short mirror: H1_0 fails on sweep, H1_1 qualifies.
    bars4=_base_fixture()
    bars4["h4"].loc[1,"close"]=1.02
    bars4["h1"].loc[0,["open","high","low","close"]]=[1.20,1.35,0.80,1.18]
    bars4["h1"].loc[1,["open","high","low","close"]]=[1.16,1.20,0.85,1.02]
    bars4["m15"].loc[0,["open","high","low","close"]]=[1.15,1.25,1.00,1.05]
    bars4["m5"].loc[0,["open","high","low","close"]]=[1.10,1.12,1.04,1.08]
    bars4["m5"].loc[1,["open","high","low","close"]]=[1.08,1.12,0.94,0.96]
    q=recent_h1_range_setup_at(bars4,0,"EURUSD")
    assert q["status"]=="armed"
    assert q["direction"]=="short"
    assert q["selected_h1"]=="H1_1"
    assert q["target_price"]>=q["h1_low"]
    tests.append("short_h1_1_fallback")

    return tests


def market_preflight(symbol:str,df1:pd.DataFrame,usd_jpy_df:pd.DataFrame|None=None)->dict:
    bars=build_mtf_bars(df1)
    usd_jpy_series=None
    if usd_jpy_df is not None:
        usd_jpy_series=usd_jpy_df.set_index("datetime")["close"].sort_index()

    setup_status=Counter()
    selected_h1=Counter()
    fill_status=Counter()
    filled_by_direction={"long":0,"short":0}
    pending_until=pd.Timestamp.min.tz_localize("UTC")
    blocked_pending=0

    signals=0
    deployable=0
    utility=Counter()
    waits=[]
    improvements=[]
    safe_lots=[]
    safe_gross=[]
    safe_risks=[]
    safe_notionals=[]
    safe_margins=[]
    examples=[]

    for i in range(len(bars["m15"])):
        decision_ts=bars["m15"].iloc[i]["available_ts"]
        if decision_ts<START or decision_ts>=SEALED_START:
            continue
        if decision_ts.weekday()>=5 or decision_ts.hour>=18:
            continue

        setup=recent_h1_range_setup_at(bars,i,symbol)
        setup_status[setup["status"]]+=1
        if setup["status"]!="armed":
            continue

        selected_h1[setup["selected_h1"]]+=1

        if decision_ts<pending_until:
            blocked_pending+=1
            continue

        fill=find_limit_fill(df1,setup,symbol,usd_jpy_series)
        pending_until=fill["resolved_ts"]
        fill_status[fill["status"]]+=1
        if not fill.get("filled"):
            continue

        direction=setup["direction"]
        entry=float(fill["entry"])
        stop=float(fill["stop"])
        entry_usd_jpy=None
        if symbol=="EURJPY" and usd_jpy_series is not None:
            k=int(usd_jpy_series.index.searchsorted(fill["entry_ts"],side="right"))-1
            if k>=0:
                entry_usd_jpy=float(usd_jpy_series.iloc[k])

        overlay=safe_deployability_overlay(symbol,entry,stop,entry_usd_jpy)
        if overlay.get("reason") in (
            "invalid_geometry","value_or_notional_unavailable",
            "target_geometry_unavailable","invalid_stop_loss_per_lot"
        ):
            continue

        signals+=1
        filled_by_direction[direction]+=1
        waits.append(int(fill["wait_active_m1_bars"]))
        improvements.append(float(fill["entry_improvement_a5_range"]))
        utility[overlay["utility_band"]]+=1

        if overlay["deployable"]:
            deployable+=1
            safe_lots.append(float(overlay["safe_lot"]))
            safe_gross.append(float(overlay["gross_target_usd"]))
            safe_risks.append(float(overlay["stop_risk_usd"]))
            safe_notionals.append(float(overlay["notional_usd"]))
            safe_margins.append(float(overlay["margin_usd"]))

        if len(examples)<5:
            examples.append({
                "decision_ts":str(decision_ts),
                "direction":direction,
                "selected_h1":setup["selected_h1"],
                "selected_h1_start":str(setup["selected_h1_start"]),
                "h1_low":setup["h1_low"],
                "h1_high":setup["h1_high"],
                "target_price":setup["target_price"],
                "entry_ts":str(fill["entry_ts"]),
                "entry":entry,
                "stop":stop,
                "wait_active_m1_bars":int(fill["wait_active_m1_bars"]),
                "entry_improvement_a5_range":float(fill["entry_improvement_a5_range"]),
                "safe_overlay":overlay,
            })

    return {
        "bar_counts":{k:len(v) for k,v in bars.items()},
        "setup_status_counts":dict(sorted(setup_status.items())),
        "selected_h1_counts":dict(sorted(selected_h1.items())),
        "blocked_setups_due_pending_order":blocked_pending,
        "fill_status_counts":dict(sorted(fill_status.items())),
        "filled_signal_paths":signals,
        "filled_by_direction":filled_by_direction,
        "deployable_paths_safe_lot_ge_0_01":deployable,
        "utility_band_counts":dict(sorted(utility.items())),
        "median_wait_active_m1_bars":statistics.median(waits) if waits else None,
        "median_entry_improvement_a5_range":statistics.median(improvements) if improvements else None,
        "safe_overlay_diagnostics":{
            "median_safe_lot":statistics.median(safe_lots) if safe_lots else None,
            "median_gross_target_usd":statistics.median(safe_gross) if safe_gross else None,
            "median_stop_risk_usd":statistics.median(safe_risks) if safe_risks else None,
            "median_notional_usd":statistics.median(safe_notionals) if safe_notionals else None,
            "median_margin_usd":statistics.median(safe_margins) if safe_margins else None,
            "max_stop_risk_usd":max(safe_risks) if safe_risks else None,
            "max_notional_usd":max(safe_notionals) if safe_notionals else None,
            "max_margin_usd":max(safe_margins) if safe_margins else None,
        },
        "examples":examples,
    }


def main():
    tests={
        "engine_m_v01":self_tests_engine_m(),
        "engine_m_v02":self_tests_engine_m_v02(),
        "engine_m_v05":self_tests_engine_m_v05(),
        "synthetic_recent_h1":synthetic_recent_h1_tests(),
        "synthetic_fill":synthetic_fill_tests(),
    }

    data={}
    for symbol in EXECUTION_MARKETS:
        path=download_pinned(symbol,CACHE)
        df=load_scoped_csv(path,symbol,SEALED_START)
        if df.empty or df["datetime"].max()>=SEALED_START:
            raise RuntimeError(f"{symbol}: protected-period leak")
        data[symbol]=df

    markets={}
    for symbol in EXECUTION_MARKETS:
        uj=data["USDJPY"] if symbol=="EURJPY" else None
        markets[symbol]=market_preflight(symbol,data[symbol],uj)

    per_market_gate={
        s:(
            markets[s]["filled_signal_paths"]>=25
            and markets[s]["filled_by_direction"]["long"]>0
            and markets[s]["filled_by_direction"]["short"]>0
        )
        for s in EXECUTION_MARKETS
    }
    total_signals=sum(x["filled_signal_paths"] for x in markets.values())
    total_deployable=sum(x["deployable_paths_safe_lot_ge_0_01"] for x in markets.values())
    utility_total=Counter()
    selected_total=Counter()
    for x in markets.values():
        utility_total.update(x["utility_band_counts"])
        selected_total.update(x["selected_h1_counts"])

    safety_ok=True
    for x in markets.values():
        d=x["safe_overlay_diagnostics"]
        if d["max_stop_risk_usd"] is not None and d["max_stop_risk_usd"]>20.0+1e-9:
            safety_ok=False
        if d["max_notional_usd"] is not None and d["max_notional_usd"]>50000.0+1e-9:
            safety_ok=False
        if d["max_margin_usd"] is not None and d["max_margin_usd"]>100.0+1e-9:
            safety_ok=False

    gate={
        "each_market_ge_25_and_both_directions":all(per_market_gate.values()),
        "total_signal_paths_ge_300":total_signals>=300,
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
        "experiment":"EXP-031",
        "engine":"Engine M v0.5",
        "stage":"zero_outcome_recent_h1_range_preflight",
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
            "filled_signal_paths":total_signals,
            "deployable_paths_safe_lot_ge_0_01":total_deployable,
            "selected_h1_counts":dict(sorted(selected_total.items())),
            "utility_band_counts":dict(sorted(utility_total.items())),
        },
        "preflight_pass":passed,
    }

    out=OUT/"EXP-031-recent-h1-preflight-v0.5.json"
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
