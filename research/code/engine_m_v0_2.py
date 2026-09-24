#!/usr/bin/env python3
"""Engine M v0.2 signal-first sizing/deployability utilities.

No future target labels or P&L outcomes are calculated here.
"""

from __future__ import annotations

import math
from typing import Optional

from engine_k_v0_1 import (
    REFERENCE_EQUITY_USD,
    PRIMARY_STOP_RISK_USD,
    RESEARCH_LOT_STEP,
    RESEARCH_LEVERAGE_REFERENCE,
    MAX_MARGIN_FRACTION_OF_EQUITY,
    MAX_NOTIONAL_TO_EQUITY,
    floor_lot,
    usd_value_per_native_unit_1lot,
    notional_usd_1lot,
)
from engine_k_v0_2 import native_target_distances_v02, research_costs_v02

GOLD_ANCHOR_LOT=0.10
RUNG="T40"


def safe_deployability_overlay(
    symbol:str,
    entry:float,
    stop:float,
    usd_jpy:Optional[float]=None,
)->dict:
    """Compute maximum safe lot under existing account gates, independent of outcome."""
    if not (math.isfinite(entry) and math.isfinite(stop)) or entry<=0 or stop<=0 or entry==stop:
        return {"deployable":False,"reason":"invalid_geometry"}

    v=usd_value_per_native_unit_1lot(symbol,entry,usd_jpy)
    n1=notional_usd_1lot(symbol,entry,usd_jpy)
    if v is None or n1 is None or v<=0 or n1<=0:
        return {"deployable":False,"reason":"value_or_notional_unavailable"}

    distances=native_target_distances_v02(symbol,entry,stop)
    d=distances.get(RUNG)
    if d is None or d<=0:
        return {"deployable":False,"reason":"target_geometry_unavailable"}

    stop_dist=abs(entry-stop)
    stop_loss_1lot=stop_dist*v
    if stop_loss_1lot<=0:
        return {"deployable":False,"reason":"invalid_stop_loss_per_lot"}

    max_notional=REFERENCE_EQUITY_USD*MAX_NOTIONAL_TO_EQUITY
    max_margin=REFERENCE_EQUITY_USD*MAX_MARGIN_FRACTION_OF_EQUITY

    lot_risk=PRIMARY_STOP_RISK_USD/stop_loss_1lot
    lot_notional=max_notional/n1
    lot_margin=(max_margin*RESEARCH_LEVERAGE_REFERENCE)/n1

    raw=min(lot_risk,lot_notional,lot_margin)
    if symbol=="XAUUSD":
        raw=min(raw,GOLD_ANCHOR_LOT)
    lot=floor_lot(raw)

    overlay={
        "deployable":bool(lot>=RESEARCH_LOT_STEP),
        "safe_lot":float(lot),
        "safe_lot_raw":float(raw),
        "lot_cap_risk":float(lot_risk),
        "lot_cap_notional":float(lot_notional),
        "lot_cap_margin":float(lot_margin),
        "target_distance":float(d),
        "reward_multiple":float(d/stop_dist),
        "stop_distance_native":float(stop_dist),
        "usd_value_per_native_unit_1lot":float(v),
        "notional_usd_1lot":float(n1),
    }
    if lot<RESEARCH_LOT_STEP:
        overlay.update({
            "reason":"safe_lot_below_minimum",
            "stop_risk_usd":0.0,
            "notional_usd":0.0,
            "margin_usd":0.0,
            "gross_target_usd":0.0,
            "primary_cost_usd":0.0,
            "stress_cost_usd":0.0,
            "utility_band":"NONDEPLOYABLE",
        })
        return overlay

    stop_risk=stop_dist*v*lot
    notional=n1*lot
    margin=notional/RESEARCH_LEVERAGE_REFERENCE
    gross=d*v*lot
    costs=research_costs_v02(gross)

    # Exact safety assertions; these are unchanged project gates.
    if stop_risk>PRIMARY_STOP_RISK_USD+1e-9:
        raise AssertionError("safe lot violates risk cap")
    if notional>max_notional+1e-9:
        raise AssertionError("safe lot violates notional cap")
    if margin>max_margin+1e-9:
        raise AssertionError("safe lot violates margin cap")
    if symbol=="XAUUSD" and lot>GOLD_ANCHOR_LOT+1e-12:
        raise AssertionError("Gold anchor exceeded")

    if gross>=40.0-1e-9:
        band="GE40"
    elif gross>=30.0-1e-9:
        band="GE30"
    else:
        band="LT30"

    overlay.update({
        "reason":"ok",
        "stop_risk_usd":float(stop_risk),
        "notional_usd":float(notional),
        "margin_usd":float(margin),
        "gross_target_usd":float(gross),
        "primary_cost_usd":float(costs["primary_cost_usd"]),
        "stress_cost_usd":float(costs["stress_cost_usd"]),
        "utility_band":band,
    })
    return overlay


def normalized_cost_units(reward_multiple:float)->dict:
    if not math.isfinite(reward_multiple) or reward_multiple<=0:
        raise ValueError("invalid reward multiple")
    return {
        "primary_cost_r":0.10*reward_multiple,
        "stress_cost_r":0.20*reward_multiple,
    }


def self_tests_engine_m_v02()->list[str]:
    tests=[]

    # EURUSD with 5-pip stop: risk cap governs and ~USD40 remains feasible.
    x=safe_deployability_overlay("EURUSD",1.17000,1.16950)
    assert x["deployable"]
    assert x["safe_lot"]<=0.40+1e-12
    assert x["stop_risk_usd"]<=20.0+1e-9
    assert x["notional_usd"]<=50000.0+1e-9
    assert x["margin_usd"]<=100.0+1e-9
    tests.append("eurusd_safe_overlay_respects_caps")

    # Tight stop can be a valid signal but reference-account target utility can be <USD30.
    y=safe_deployability_overlay("EURUSD",1.17000,1.16985)
    assert y["deployable"]
    assert y["utility_band"]=="LT30"
    assert y["gross_target_usd"]<30.0
    tests.append("tight_stop_signal_not_rejected_for_low_utility")

    # Gold never exceeds frozen 0.10-lot anchor.
    g=safe_deployability_overlay("XAUUSD",4600.0,4598.5)
    assert g["deployable"] and g["safe_lot"]<=0.10+1e-12
    tests.append("gold_anchor_cap_preserved")

    # At 1:500 and 20% equity margin, notional and margin caps are numerically equivalent.
    assert abs(x["lot_cap_notional"]-x["lot_cap_margin"])<1e-12
    tests.append("notional_margin_cap_equivalence")

    c=normalized_cost_units(2.0)
    assert abs(c["primary_cost_r"]-0.2)<1e-12
    assert abs(c["stress_cost_r"]-0.4)<1e-12
    tests.append("normalized_cost_units")

    return tests
