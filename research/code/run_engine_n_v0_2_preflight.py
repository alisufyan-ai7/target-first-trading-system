#!/usr/bin/env python3
"""EXP-033 Engine N v0.2 zero-outcome rolling intraday preflight."""

from __future__ import annotations

import json
import statistics
from collections import Counter
from pathlib import Path

import pandas as pd

from engine_k_v0_1 import EXECUTION_MARKETS, download_pinned
from engine_m_v0_1 import build_mtf_bars
from engine_m_v0_2 import safe_deployability_overlay, self_tests_engine_m_v02
from engine_n_v0_1 import session_anchor, session_setup, find_session_pullback_fill
from engine_n_v0_2 import ROLLING_ANCHORS, self_tests_engine_n_v02
from run_engine_k_v0_2_training_calibration import load_scoped_csv
from run_engine_n_v0_1_preflight import synthetic_engine_n_tests

ROOT=Path(__file__).resolve().parents[2]
CACHE=Path("/tmp/engine-n-v02-preflight")
OUT=ROOT/"research/results"
OUT.mkdir(parents=True,exist_ok=True)

START=pd.Timestamp("2026-03-23",tz="UTC")
SEALED_START=pd.Timestamp("2026-07-01",tz="UTC")


def rolling_anchor_tests()->list[str]:
    tests=[]
    assert len(ROLLING_ANCHORS)==12
    times=[h*60+m for h,m,_ in ROLLING_ANCHORS]
    assert all(b-a==60 for a,b in zip(times,times[1:]))
    tests.append("hourly_anchor_spacing_exact")

    d=pd.Timestamp("2026-04-06",tz="UTC")
    anchors=[session_anchor(d,h,m) for h,m,_ in ROLLING_ANCHORS]
    decisions=[a+pd.Timedelta(minutes=30) for a in anchors]
    horizons=[a+pd.Timedelta(minutes=90) for a in anchors]
    assert all(horizons[i]==decisions[i+1] for i in range(len(decisions)-1))
    tests.append("prior_horizon_equals_next_decision")
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
    m15=bars["m15"]
    usd_jpy_series=None
    if usd_jpy_df is not None:
        usd_jpy_series=usd_jpy_df.set_index("datetime")["close"].sort_index()

    setup_status=Counter()
    anchor_armed=Counter()
    fill_status=Counter()
    filled_by_direction={"long":0,"short":0}
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

    for day in pd.date_range(
        START.normalize(),
        SEALED_START-pd.Timedelta(days=1),
        freq="D",
        tz="UTC",
    ):
        if day.weekday()>=5:
            continue

        for hour,minute,name in ROLLING_ANCHORS:
            anchor=session_anchor(day,hour,minute)
            setup=session_setup(df1,m15,anchor,name,symbol)
            setup_status[setup["status"]]+=1
            if setup["status"]!="armed":
                continue

            anchor_armed[name]+=1
            fill=find_session_pullback_fill(df1,setup)
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
            improvements.append(float(fill["entry_improvement_drive_range"]))

            if overlay["deployable"]:
                deployable+=1
                safe_lots.append(float(overlay["safe_lot"]))
                safe_gross.append(float(overlay["gross_target_usd"]))
                safe_risks.append(float(overlay["stop_risk_usd"]))
                safe_notionals.append(float(overlay["notional_usd"]))
                safe_margins.append(float(overlay["margin_usd"]))

            if len(examples)<8:
                examples.append({
                    "anchor_name":name,
                    "anchor":str(anchor),
                    "direction":setup["direction"],
                    "baseline_median":setup["baseline_median"],
                    "drive_range":setup["drive_range"],
                    "drive_range_over_baseline_median":setup["drive_range_over_baseline_median"],
                    "drive_body_fraction":setup["drive_body_fraction"],
                    "entry_ts":str(fill["entry_ts"]),
                    "entry":entry,
                    "stop":stop,
                    "wait_active_m1_bars":int(fill["wait_active_m1_bars"]),
                    "entry_improvement_drive_range":float(fill["entry_improvement_drive_range"]),
                    "safe_overlay":overlay,
                })

    return {
        "setup_status_counts":dict(sorted(setup_status.items())),
        "armed_by_anchor":dict(sorted(anchor_armed.items())),
        "fill_status_counts":dict(sorted(fill_status.items())),
        "filled_signal_paths":signals,
        "filled_by_direction":filled_by_direction,
        "deployable_paths_safe_lot_ge_0_01":deployable,
        "utility_band_counts":dict(sorted(utility.items())),
        "median_wait_active_m1_bars":statistics.median(waits) if waits else None,
        "median_entry_improvement_drive_range":statistics.median(improvements) if improvements else None,
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
        "engine_n_v02":self_tests_engine_n_v02(),
        "engine_m_v02_safe_overlay":self_tests_engine_m_v02(),
        "synthetic_engine_n":synthetic_engine_n_tests(),
        "rolling_anchor":rolling_anchor_tests(),
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
        "experiment":"EXP-033",
        "engine":"Engine N v0.2",
        "stage":"zero_outcome_rolling_intraday_drive_preflight",
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

    out=OUT/"EXP-033-rolling-drive-preflight-v0.2.json"
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
