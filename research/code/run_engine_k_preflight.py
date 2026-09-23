#!/usr/bin/env python3
import json
from pathlib import Path

from engine_k_v0_1 import (
    SOURCES,
    EXECUTION_MARKETS,
    FORECAST_ONLY_MARKETS,
    REFERENCE_EQUITY_USD,
    PRIMARY_STOP_RISK_USD,
    PRIMARY_PROBABILITY_FLOOR,
    BREAKEVEN_PROBABILITY_BUFFER,
    PRIMARY_COST_FRACTION_OF_GROSS_TARGET,
    STRESS_COST_FRACTION_OF_GROSS_TARGET,
    RESEARCH_LEVERAGE_REFERENCE,
    MAX_MARGIN_FRACTION_OF_EQUITY,
    MAX_NOTIONAL_TO_EQUITY,
    MAX_NEXT_ENTRY_GAP_MINUTES,
    download_pinned,
    load_csv,
    preflight_states,
    self_tests,
)

ROOT=Path(__file__).resolve().parents[2]
CACHE=Path("/tmp/engine-k-data")
OUT=ROOT/"research/results"
OUT.mkdir(parents=True, exist_ok=True)

TRAIN_START="2026-03-23"
TRAIN_END="2026-05-31"
CALIBRATION_START="2026-06-01"
CALIBRATION_END="2026-06-30"
SECONDARY_START="2026-07-01"
SECONDARY_END="2026-08-31"
FINAL_HOLDOUT_START="2026-09-01"
FINAL_HOLDOUT_END="2026-09-22"


def gap_diagnostics(df):
    delta=df["datetime"].diff().dropna()
    if delta.empty:
        return {"gap_count_gt_1m":0,"max_gap_minutes":0.0}
    gt=delta[delta > delta.iloc[0]*1.5]
    return {
        "gap_count_gt_1m":int((delta > __import__("pandas").Timedelta(minutes=1)).sum()),
        "max_gap_minutes":float(delta.max().total_seconds()/60.0),
    }


def main():
    tests=self_tests()
    result={
        "experiment":"EXP-022",
        "engine":"Engine K v0.1",
        "checkpoint":"pre_outcome_cleanup_preflight",
        "target_outcomes_calculated":False,
        "model_outcomes_calculated":False,
        "training_run":False,
        "calibration_run":False,
        "secondary_test_run":False,
        "final_holdout_loaded_for_outcomes":False,
        "secondary_or_final_state_distributions_inspected_by_final_preflight":False,
        "execution_markets":list(EXECUTION_MARKETS),
        "forecast_only_markets":list(FORECAST_ONLY_MARKETS),
        "split":{
            "training":[TRAIN_START,TRAIN_END],
            "calibration":[CALIBRATION_START,CALIBRATION_END],
            "secondary_test":[SECONDARY_START,SECONDARY_END],
            "final_holdout":[FINAL_HOLDOUT_START,FINAL_HOLDOUT_END],
            "excluded_incomplete_day":"2026-09-23",
        },
        "research_economics":{
            "reference_equity_usd":REFERENCE_EQUITY_USD,
            "primary_stop_risk_usd":PRIMARY_STOP_RISK_USD,
            "primary_probability_floor":PRIMARY_PROBABILITY_FLOOR,
            "breakeven_probability_buffer":BREAKEVEN_PROBABILITY_BUFFER,
            "primary_cost_fraction_of_gross_target":PRIMARY_COST_FRACTION_OF_GROSS_TARGET,
            "stress_cost_fraction_of_gross_target":STRESS_COST_FRACTION_OF_GROSS_TARGET,
            "research_leverage_reference":RESEARCH_LEVERAGE_REFERENCE,
            "max_margin_fraction_of_equity":MAX_MARGIN_FRACTION_OF_EQUITY,
            "max_notional_to_equity":MAX_NOTIONAL_TO_EQUITY,
            "max_next_entry_gap_minutes":MAX_NEXT_ENTRY_GAP_MINUTES,
            "broker_specific_economics_required_before_live":True,
        },
        "self_tests":tests,
        "markets":{},
    }

    assert set(EXECUTION_MARKETS).isdisjoint(set(FORECAST_ONLY_MARKETS))
    assert set(EXECUTION_MARKETS) | set(FORECAST_ONLY_MARKETS) == set(SOURCES)

    data={}
    for symbol in SOURCES:
        path=download_pinned(symbol,CACHE)
        df=load_csv(path,symbol)
        data[symbol]=df
        result["markets"][symbol]={
            "universe_class":"execution" if symbol in EXECUTION_MARKETS else "forecast_only",
            "downloaded":True,
            "raw_rows_expected":SOURCES[symbol]["rows"],
            "rows_after_sep23_cut":len(df),
            "first_ts":str(df["datetime"].iloc[0]),
            "last_ts":str(df["datetime"].iloc[-1]),
            "gap_diagnostics":gap_diagnostics(df),
        }

    # Preserve later-period state/feature distributions: full pinned files are
    # verified for raw integrity, but candidate/feature preflight uses only
    # training + calibration data through 2026-06-30.
    preflight_cutoff=__import__("pandas").Timestamp("2026-07-01", tz="UTC")
    for symbol,df in data.items():
        scoped=df[df["datetime"] < preflight_cutoff].reset_index(drop=True)
        uj=None
        if symbol=="EURJPY":
            uj=data["USDJPY"][data["USDJPY"]["datetime"] < preflight_cutoff].reset_index(drop=True)
        result["markets"][symbol]["state_preflight_scope"]="2026-03-23 through 2026-06-30 only"
        result["markets"][symbol]["state_preflight"]=preflight_states(symbol,scoped,uj)

    result["totals"]={
        "execution_structural_states":sum(
            result["markets"][s]["state_preflight"]["structural_states"]
            for s in EXECUTION_MARKETS
        ),
        "execution_admissible_target_rungs_pre_probability":sum(
            result["markets"][s]["state_preflight"]["admissible_target_rungs"]
            for s in EXECUTION_MARKETS
        ),
        "forecast_only_structural_states":sum(
            result["markets"][s]["state_preflight"]["structural_states"]
            for s in FORECAST_ONLY_MARKETS
        ),
    }

    # Forecast-only markets must have no executable dollar-economics rungs.
    for s in FORECAST_ONLY_MARKETS:
        assert result["markets"][s]["state_preflight"]["admissible_target_rungs"] == 0

    out=OUT/"EXP-022-preflight-cleanup-v0.1.json"
    out.write_text(json.dumps(result,indent=2,default=str)+"\n")
    print(json.dumps({
        "checkpoint":result["checkpoint"],
        "self_tests":len(tests),
        "execution_markets":len(EXECUTION_MARKETS),
        "forecast_only_markets":len(FORECAST_ONLY_MARKETS),
        "execution_structural_states":result["totals"]["execution_structural_states"],
        "execution_admissible_target_rungs_pre_probability":result["totals"]["execution_admissible_target_rungs_pre_probability"],
        "target_outcomes_calculated":False,
        "model_outcomes_calculated":False,
    },indent=2))
    print(f"WROTE {out}")
    print("ENGINE_K_TARGET_OUTCOMES_CALCULATED=NO")
    print("ENGINE_K_MODEL_OUTCOMES_CALCULATED=NO")


if __name__=="__main__":
    main()
