#!/usr/bin/env python3
"""EXP-041 HistData timestamp-semantics diagnostic. No strategy labels or P&L."""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

from engine_k_v0_1 import EXECUTION_MARKETS, download_pinned
from run_exp041_third_source_adjudication import (
    START,
    END,
    adjudicate,
    load_csv,
    load_current,
    pair_stats,
)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research/results"
OUT.mkdir(parents=True, exist_ok=True)
DUKA = Path(os.environ.get("EXP041_DIAG_DIR", "/tmp/exp041-cross-feed"))
HIST = Path(os.environ.get("EXP041_HISTDATA_DIR", "/tmp/exp041-histdata"))
CACHE = Path("/tmp/exp041-histdata-time-current")
SHIFTS = tuple(range(-6, 7))


def shifted_hist(x: pd.DataFrame, hours: int) -> pd.DataFrame:
    z = x.copy()
    z["datetime"] = z["datetime"] + pd.Timedelta(hours=hours)
    z = z[(z["datetime"] >= START) & (z["datetime"] < END)].copy()
    return z.sort_values("datetime").drop_duplicates("datetime").reset_index(drop=True)


def support_counts(markets: dict) -> dict:
    supported = {"CURRENT_PINNED": 0, "DUKASCOPY": 0, "HISTDATA": 0}
    for m in markets.values():
        p = m["pairwise"]
        cd = p["CURRENT_PINNED__DUKASCOPY"]["pair_agreement_pass"]
        ch = p["CURRENT_PINNED__HISTDATA"]["pair_agreement_pass"]
        dh = p["DUKASCOPY__HISTDATA"]["pair_agreement_pass"]
        if cd or ch:
            supported["CURRENT_PINNED"] += 1
        if cd or dh:
            supported["DUKASCOPY"] += 1
        if ch or dh:
            supported["HISTDATA"] += 1
    return supported


def median_hist_anchor_1h(markets: dict) -> float:
    vals = []
    for m in markets.values():
        p = m["pairwise"]
        for key in ("CURRENT_PINNED__HISTDATA", "DUKASCOPY__HISTDATA"):
            v = p[key]["returns"]["1h"]["correlation"]
            if v is not None and np.isfinite(v):
                vals.append(float(v))
    return float(np.median(vals)) if vals else float("-inf")


def shift_sort_key(s: dict) -> tuple:
    return (
        int(s["feed_selection_gate_pass"]),
        len(s["eligible_consensus_sources"]),
        -int(s["no_two_source_consensus_markets"]),
        int(s["supported_markets_by_source"]["HISTDATA"]),
        float(s["median_histdata_anchor_1h_correlation"]),
        -abs(int(s["shift_hours"])),
        -int(s["shift_hours"]),
    )


def main() -> None:
    base = {}
    for symbol in EXECUTION_MARKETS:
        current = load_current(download_pinned(symbol, CACHE))
        duka = load_csv(DUKA / f"{symbol}.csv")
        hist = load_csv(HIST / f"{symbol}.csv")
        base[symbol] = {
            "CURRENT_PINNED": current,
            "DUKASCOPY": duka,
            "HISTDATA": hist,
            "CURRENT_PINNED__DUKASCOPY": pair_stats(current, duka),
        }

    shift_summaries = []
    shift_market_details = {}

    for hours in SHIFTS:
        markets = {}
        for symbol, src in base.items():
            hist = shifted_hist(src["HISTDATA"], hours)
            cd = src["CURRENT_PINNED__DUKASCOPY"]
            ch = pair_stats(src["CURRENT_PINNED"], hist)
            dh = pair_stats(src["DUKASCOPY"], hist)
            tag = adjudicate(
                cd["pair_agreement_pass"],
                ch["pair_agreement_pass"],
                dh["pair_agreement_pass"],
            )
            markets[symbol] = {
                "adjudication": tag,
                "pairwise": {
                    "CURRENT_PINNED__DUKASCOPY": cd,
                    "CURRENT_PINNED__HISTDATA": ch,
                    "DUKASCOPY__HISTDATA": dh,
                },
            }

        supported = support_counts(markets)
        no_consensus = sum(
            int(m["adjudication"] == "NO_TWO_SOURCE_CONSENSUS")
            for m in markets.values()
        )
        eligible = [s for s, n in supported.items() if n >= 7]
        gate_pass = bool(eligible and no_consensus <= 1)
        summary = {
            "shift_hours": int(hours),
            "supported_markets_by_source": supported,
            "no_two_source_consensus_markets": int(no_consensus),
            "eligible_consensus_sources": eligible,
            "feed_selection_gate_pass": gate_pass,
            "median_histdata_anchor_1h_correlation": median_hist_anchor_1h(markets),
            "adjudication": {s: m["adjudication"] for s, m in markets.items()},
        }
        shift_summaries.append(summary)
        shift_market_details[int(hours)] = markets

    best = max(shift_summaries, key=shift_sort_key)
    passing = [s["shift_hours"] for s in shift_summaries if s["feed_selection_gate_pass"]]

    result = {
        "stage": "EXP-041 HistData timestamp-semantics diagnostic v0.1",
        "tested_repository_sha": os.environ.get("GITHUB_SHA"),
        "target_labels_calculated": False,
        "pnl_calculated": False,
        "protected_periods": {
            "jul_aug_2026_loaded": False,
            "sep_2026_loaded": False,
        },
        "interval": [str(START), str(END)],
        "histdata_v01_timestamp_assumption": "fixed EST (UTC-5) converted to UTC before this diagnostic",
        "common_shift_grid_hours": list(SHIFTS),
        "pairwise_gate_unchanged": {
            "m1_overlap_ratio": 0.70,
            "corr_5m": 0.90,
            "corr_1h": 0.95,
            "corr_1d": 0.95,
            "sign_agreement_1h": 0.95,
        },
        "shift_summaries": shift_summaries,
        "passing_common_shifts_hours": passing,
        "best_descriptive_shift": best,
        "best_shift_market_details": shift_market_details[int(best["shift_hours"])],
        "feed_selection_gate_restorable_by_common_shift": bool(passing),
        "disposition": (
            "COMMON_TIMESTAMP_SHIFT_CAN_RESTORE_FROZEN_GATE_FREEZE_CORRECTED_ADJUDICATION_V02"
            if passing
            else "TIMESTAMP_SHIFT_DOES_NOT_EXPLAIN_FAILURE_REQUIRE_FOURTH_OR_BROKER_SOURCE"
        ),
    }

    p = OUT / "EXP-041-histdata-timestamp-semantics-diagnostic-v0.1.json"
    p.write_text(json.dumps(result, indent=2, default=str) + "\n")

    print(json.dumps({
        "passing_common_shifts_hours": passing,
        "best_descriptive_shift": best,
        "disposition": result["disposition"],
        "protected_periods": result["protected_periods"],
    }, indent=2))


if __name__ == "__main__":
    main()
