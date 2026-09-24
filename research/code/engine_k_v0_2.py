#!/usr/bin/env python3
"""Engine K v0.2 zero-outcome economics/reference utilities.

v0.2 preserves v0.1 causal state construction and replaces only:
- non-Gold native target function;
- equivalent-size economics derived after target definition;
- probability qualification rule.

No future target labels are calculated in this module.
"""

from __future__ import annotations

import math
from typing import Dict, Optional

from engine_k_v0_1 import (
    REFERENCE_EQUITY_USD,
    PRIMARY_STOP_RISK_USD,
    RESEARCH_LOT_STEP,
    EXECUTION_MARKETS,
    FORECAST_ONLY_MARKETS,
    PRIMARY_COST_FRACTION_OF_GROSS_TARGET,
    STRESS_COST_FRACTION_OF_GROSS_TARGET,
    RESEARCH_LEVERAGE_REFERENCE,
    MAX_MARGIN_FRACTION_OF_EQUITY,
    MAX_NOTIONAL_TO_EQUITY,
    SOURCES,
    usd_value_per_native_unit_1lot,
    notional_usd_1lot,
    floor_lot,
)

V02_PROBABILITY_FLOOR = 0.50
V02_BREAK_EVEN_BUFFER = 0.10

RUNG_ORDER = ("T30","T40","T50")
RUNG_NOMINAL_USD = {"T30":30.0,"T40":40.0,"T50":50.0}
NON_GOLD_R_MULTIPLE = {"T30":1.5,"T40":2.0,"T50":2.5}


def research_tick(symbol: str) -> float:
    if symbol in ("XAUUSD","USDJPY","EURJPY"):
        return 0.001
    return 0.00001


def round_up_to_tick(x: float, tick: float) -> float:
    if not math.isfinite(x) or not math.isfinite(tick) or x <= 0 or tick <= 0:
        raise ValueError("invalid round_up_to_tick input")
    return math.ceil((x / tick) - 1e-12) * tick


def research_costs_v02(actual_gross_target_usd: float) -> dict:
    return {
        "primary_cost_usd": actual_gross_target_usd * PRIMARY_COST_FRACTION_OF_GROSS_TARGET,
        "stress_cost_usd": actual_gross_target_usd * STRESS_COST_FRACTION_OF_GROSS_TARGET,
    }


def qualification_probability_floor_v02(
    actual_gross_target_usd: float,
    stop_risk_usd: float,
    primary_cost_usd: float,
) -> dict:
    denom = actual_gross_target_usd + stop_risk_usd
    if denom <= 0:
        return {"breakeven_probability": None, "required_probability": None}
    p_be = (stop_risk_usd + primary_cost_usd) / denom
    required = max(V02_PROBABILITY_FLOOR, p_be + V02_BREAK_EVEN_BUFFER)
    return {
        "breakeven_probability": p_be,
        "required_probability": required,
    }


def native_target_distances_v02(symbol: str, entry: float, stop: float) -> Dict[str,float]:
    if symbol == "XAUUSD":
        return {"T30":3.0,"T40":4.0,"T50":5.0}
    r = abs(entry-stop)
    if not math.isfinite(r) or r <= 0:
        return {}
    tick = research_tick(symbol)
    return {
        rung: round_up_to_tick(r * NON_GOLD_R_MULTIPLE[rung], tick)
        for rung in RUNG_ORDER
    }


def candidate_economics_v02(
    symbol: str,
    entry: float,
    stop: float,
    usd_jpy: Optional[float] = None,
) -> Dict[str,dict]:
    if symbol not in EXECUTION_MARKETS:
        return {}

    distances = native_target_distances_v02(symbol, entry, stop)
    if not distances:
        return {}

    v = usd_value_per_native_unit_1lot(symbol, entry, usd_jpy)
    n1 = notional_usd_1lot(symbol, entry, usd_jpy)
    if v is None or n1 is None or v <= 0 or n1 <= 0:
        return {}

    stop_dist = abs(entry-stop)
    out = {}

    for rung in RUNG_ORDER:
        target_nominal = RUNG_NOMINAL_USD[rung]
        d = distances[rung]

        if symbol == "XAUUSD":
            lot = 0.10
        else:
            lot = floor_lot(target_nominal / (d*v))

        actual_gross = d*v*lot
        stop_risk = stop_dist*v*lot
        notional = n1*lot
        margin = notional / RESEARCH_LEVERAGE_REFERENCE
        costs = research_costs_v02(actual_gross)
        probs = qualification_probability_floor_v02(
            actual_gross, stop_risk, costs["primary_cost_usd"]
        )

        lot_ok = lot >= RESEARCH_LOT_STEP
        risk_ok = lot_ok and stop_risk <= PRIMARY_STOP_RISK_USD + 1e-9
        notional_ok = notional <= REFERENCE_EQUITY_USD*MAX_NOTIONAL_TO_EQUITY + 1e-9
        margin_ok = margin <= REFERENCE_EQUITY_USD*MAX_MARGIN_FRACTION_OF_EQUITY + 1e-9

        out[rung] = {
            "target_usd_nominal": target_nominal,
            "target_r_multiple": None if symbol=="XAUUSD" else NON_GOLD_R_MULTIPLE[rung],
            "distance": d,
            "lot": lot,
            "gross_target_usd_actual": actual_gross,
            "stop_risk_usd": stop_risk,
            "notional_usd": notional,
            "notional_to_equity": notional/REFERENCE_EQUITY_USD,
            "research_margin_usd_at_1_500": margin,
            **costs,
            **probs,
            "admissible_lot": bool(lot_ok),
            "admissible_risk": bool(risk_ok),
            "admissible_notional": bool(notional_ok),
            "admissible_margin": bool(margin_ok),
            "execution_admissible_pre_probability": bool(lot_ok and risk_ok and notional_ok and margin_ok),
        }
    return out


def self_tests_v02() -> list[str]:
    passed=[]

    # Tick-up rounding never weakens target distance.
    x=round_up_to_tick(0.001234,0.00001)
    assert x >= 0.001234 and abs(x/0.00001-round(x/0.00001)) < 1e-9
    passed.append("target_tick_round_up")

    # Gold anchor remains unchanged.
    d=native_target_distances_v02("XAUUSD",4000.0,3998.0)
    assert d=={"T30":3.0,"T40":4.0,"T50":5.0}
    g=candidate_economics_v02("XAUUSD",4000.0,3999.0)
    assert abs(g["T30"]["lot"]-0.10)<1e-12
    assert abs(g["T30"]["gross_target_usd_actual"]-30.0)<1e-9
    assert abs(g["T50"]["gross_target_usd_actual"]-50.0)<1e-9
    passed.append("gold_anchor_unchanged")

    # FX target is defined from structural R before lot sizing.
    d=native_target_distances_v02("EURUSD",1.10000,1.09900)
    assert abs(d["T30"]-0.00150)<1e-12
    assert abs(d["T40"]-0.00200)<1e-12
    assert abs(d["T50"]-0.00250)<1e-12
    passed.append("non_gold_r_multiple_targets")

    # Downward lot rounding cannot exceed nominal gross target.
    e=candidate_economics_v02("EURUSD",1.10000,1.09900)
    assert e
    for rung,x in e.items():
        assert x["gross_target_usd_actual"] <= x["target_usd_nominal"] + 1e-9
        assert x["lot"] <= x["target_usd_nominal"]/(x["distance"]*100000.0) + 1e-12
    passed.append("lot_round_down_actual_reward")

    # Structural R-multiple construction naturally keeps risk around/below USD20 before other gates.
    assert e["T30"]["stop_risk_usd"] <= 20.0 + 1e-9
    assert e["T40"]["stop_risk_usd"] <= 20.0 + 1e-9
    assert e["T50"]["stop_risk_usd"] <= 20.0 + 1e-9
    passed.append("risk_normalized_target_ladder")

    # v0.2 qualification = max(50%, BE+10pp).
    q=qualification_probability_floor_v02(50.0,20.0,5.0)
    assert q["required_probability"] >= 0.50
    assert q["required_probability"] >= q["breakeven_probability"]+0.10-1e-12
    passed.append("v02_probability_gate")

    # Forecast-only markets must never expose executable economics.
    for s in FORECAST_ONLY_MARKETS:
        assert candidate_economics_v02(s,100.0,99.0)=={}
    passed.append("forecast_only_isolation")

    return passed
