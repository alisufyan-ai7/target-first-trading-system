#!/usr/bin/env python3
"""EXP-034 Engine O v0.1 zero-outcome statistical-reversion preflight."""

from __future__ import annotations

import json
import statistics
from collections import Counter
from pathlib import Path

import pandas as pd

from engine_k_v0_1 import EXECUTION_MARKETS, download_pinned
from engine_m_v0_1 import build_mtf_bars
from engine_m_v0_2 import safe_deployability_overlay, self_tests_engine_m_v02
from engine_o_v0_1 import setup_at, find_limit_fill, self_tests_engine_o_v01
from run_engine_k_v0_2_training_calibration import load_scoped_csv

ROOT=Path(__file__).resolve().parents[2]
CACHE=Path("/tmp/engine-o-v01-preflight")
OUT=ROOT/"research/results"
OUT.mkdir(parents=True,exist_ok=True)

START=pd.Timestamp("2026-03-23",tz="UTC")
SEALED_START=pd.Timestamp("2026-07-01",tz="UTC")


def synthetic_engine_o_tests()->list[str]:
    tests=[]

    # Build 24 baseline M5 bars with median close 100 and MAD 1.
    starts=pd.date_range("2026-04-06T04:10:00Z",periods=25,freq="5min")
    closes=[99.0]*12+[101.0]*12
    rows=[]
    for i,t in enumerate(starts[:24]):
        c=closes[i]
        rows.append((t,c,c+0.4,c-0.4,c))
    # Long rejection trigger ending 06:15: close 97.4, bullish, stretched and large.
    rows.append((starts[24],96.2,98.0,96.0,97.4))
    bars5=pd.DataFrame(rows,columns=["datetime","open","high","low","close"])
    bars5["available_ts"]=bars5["datetime"]+pd.Timedelta(minutes=5)

    x=setup_at(bars5,24,"EURUSD")
    assert x["status"]=="armed" and x["direction"]=="long"
    assert x["stretch_mad_multiple"]>=2.5
    assert x["target_price"]<=x["center"]
    assert x["limit"]<x["trigger_close"]
    tests.append("synthetic_long_statistical_reversion")

    # Short mirror.
    rows2=[]
    for i,t in enumerate(starts[:24]):
        c=closes[i]
        rows2.append((t,c,c+0.4,c-0.4,c))
    rows2.append((starts[24],103.8,104.0,102.0,102.6))
    b2=pd.DataFrame(rows2,columns=["datetime","open","high","low","close"])
    b2["available_ts"]=b2["datetime"]+pd.Timedelta(minutes=5)
    y=setup_at(b2,24,"EURUSD")
    assert y["status"]=="armed" and y["direction"]=="short"
    assert y["target_price"]>=y["center"]
    assert y["limit"]>y["trigger_close"]
    tests.append("synthetic_short_statistical_reversion")

    # Candidate excluded from baseline: mutating trigger close cannot alter center.
    center_before=x["center"]
    b3=bars5.copy()
    b3.loc[24,"close"]=97.3
    z=setup_at(b3,24,"EURUSD")
    assert z["center"]==center_before
    tests.append("trigger_excluded_from_baseline")

    return tests


def entry_usd_jpy_at(series:pd.Series|None,entry_ts:pd.Timestamp):
    if series is None:
        return None
    k=int(series.index.searchsorted(entry_ts,side="right"))-1
    if k<0:
        return None
    return float(series.iloc[k])


def market_preflight(symbol:str,df1:pd.DataFrame,usd_jpy_df:pd.DataFrame|None=None)->dict:
    bars=build_mtf_bars(df1)
    b5=bars["m5"]
    usd_jpy_series=None
    if usd_jpy_df is not None:
        usd_jpy_series=usd_jpy_df.set_index("datetime")["close"].sort_index()

    setup_status=Counter()
    fill_status=Counter()
    filled_by_direction={"long":0,"short":0}
    decision_counts=Counter()
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

    for i in range(len(b5)):
        decision_ts=b5.iloc[i]["available_ts"]
        if decision_ts<START or decision_ts>=SEALED_START:
            continue
        setup=setup_at(b5,i,symbol)
        setup_status[setup["status"]]+=1
        if setup["status"]!="armed":
            continue

        hhmm=decision_ts.strftime("%H:%M")
        decision_counts[hhmm]+=1

        if decision_ts<pending_until:
            blocked_pending+=1
            continue

        fill=find_limit_fill(df1,setup)
        pending_until=fill["resolved_ts"]
        fill_status[fill["status"]]+=1
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

        signals+=1
        filled_by_direction[setup["direction"]]+=1
        utility[overlay["utility_band"]]+=1
        waits.append(int(fill["wait_active_m1_bars"]))
        improvements.append(float(fill["entry_improvement_trigger_range"]))

        if overlay["deployable"]:
            deployable+=1
            safe_lots.append(float(overlay["safe_lot"]))
            safe_gross.append(float(overlay["gross_target_usd"]))
            safe_risks.append(float(overlay["stop_risk_usd"]))
            safe_notionals.append(float(overlay["notional_usd"]))
            safe_margins.append(float(overlay["margin_usd"]))

        if len(examples)<8:
            examples.append({
                "decision_ts":str(decision_ts),
                "direction":setup["direction"],
                "center":setup["center"],
                "mad":setup["mad"],
                "stretch_mad_multiple":setup["stretch_mad_multiple"],
                "trigger_range":setup["trigger_range"],
                "trigger_body_fraction":setup["trigger_body_fraction"],
                "entry_ts":str(fill["entry_ts"]),
                "entry":entry,
                "stop":stop,
                "target_price":setup["target_price"],
                "wait_active_m1_bars":int(fill["wait_active_m1_bars"]),
                "entry_improvement_trigger_range":float(fill["entry_improvement_trigger_range"]),
                "safe_overlay":overlay,
            })

    return {
        "setup_status_counts":dict(sorted(setup_status.items())),
        "armed_by_decision_time":dict(sorted(decision_counts.items())),
        "blocked_setups_due_pending_order":blocked_pending,
        "fill_status_counts":dict(sorted(fill_status.items())),
        "filled_signal_paths":signals,
        "filled_by_direction":filled_by_direction,
        "deployable_paths_safe_lot_ge_0_01":deployable,
        "utility_band_counts":dict(sorted(utility.items())),
        "median_wait_active_m1_bars":statistics.median(waits) if waits else None,
        "median_entry_improvement_trigger_range":statistics.median(improvements) if improvements else None,
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
        "engine_o_v01":self_tests_engine_o_v01(),
        "engine_m_v02_safe_overlay":self_tests_engine_m_v02(),
        "synthetic_engine_o":synthetic_engine_o_tests(),
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
    for x in markets.values():
        utility_total.update(x["utility_band_counts"])

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

    max_ts=max(df["datetime"].max() for df in data.values())

    result={
        "experiment":"EXP-034",
        "engine":"Engine O v0.1",
        "stage":"zero_outcome_statistical_reversion_preflight",
        "target_outcomes_calculated":False,
        "pnl_outcomes_calculated":False,
        "secondary_test_loaded_or_inspected":False,
        "final_holdout_loaded_or_inspected":False,
        "parsed_market_data_max_timestamp":str(max_ts),
        "tests":tests,
        "markets":markets,
        "per_market_gate":per_market_gate,
        "gate":gate,
        "totals":{
            "filled_signal_paths":total_signals,
            "deployable_paths_safe_lot_ge_0_01":total_deployable,
            "utility_band_counts":dict(sorted(utility_total.items())),
        },
        "preflight_pass":passed,
    }

    out=OUT/"EXP-034-statistical-reversion-preflight-v0.1.json"
    out.write_text(json.dumps(result,indent=2,default=str)+"\n")
    print(json.dumps({
        "preflight_pass":passed,
        "per_market_gate":per_market_gate,
        "totals":result["totals"],
        "parsed_market_data_max_timestamp":str(max_ts),
        "target_outcomes_calculated":False,
        "pnl_outcomes_calculated":False,
        "secondary_test_loaded_or_inspected":False,
        "final_holdout_loaded_or_inspected":False,
    },indent=2))


if __name__=="__main__":
    main()
