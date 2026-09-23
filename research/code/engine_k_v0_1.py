#!/usr/bin/env python3
"""Engine K v0.1 causal market-state utilities.

This module intentionally separates:
- causal data/state construction (safe for preflight)
from
- future target labeling/model evaluation (development runner only).

External datasets are research-data transport, not project context.
"""

from __future__ import annotations

import hashlib
import io
import math
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Optional

import numpy as np
import pandas as pd

REFERENCE_EQUITY_USD = 500.0
PRIMARY_STOP_RISK_USD = 20.0
RESEARCH_LOT_STEP = 0.01

# Pre-outcome cleanup checkpoint: research-only feasibility conventions.
# These are deliberately not claimed to be broker specifications.
EXECUTION_MARKETS = (
    "XAUUSD","EURUSD","GBPUSD","USDJPY",
    "EURJPY","AUDUSD","USDCAD","USDCHF",
)
FORECAST_ONLY_MARKETS = ("XAGUSD","NAS100","US30","SPX500")
PRIMARY_PROBABILITY_FLOOR = 0.60
BREAKEVEN_PROBABILITY_BUFFER = 0.05
PRIMARY_COST_FRACTION_OF_GROSS_TARGET = 0.10
STRESS_COST_FRACTION_OF_GROSS_TARGET = 0.20
RESEARCH_LEVERAGE_REFERENCE = 500.0
MAX_MARGIN_FRACTION_OF_EQUITY = 0.20
MAX_NOTIONAL_TO_EQUITY = 100.0
MAX_NEXT_ENTRY_GAP_MINUTES = 5

SOURCES = {
    "XAUUSD": {
        "repo": "getdata-finance/xauusd-1m-ohlcv-metals-historical-data",
        "commit": "8b1cea156045bda7aefa2245d202cf0a8fd04bb1",
        "file": "XAUUSD_1m.csv",
        "blob": "8ff56a9776ab68d2aad4f2ef5d039874603a06e2",
        "rows": 179921,
        "kind": "xau",
    },
    "EURUSD": {
        "repo": "getdata-finance/eurusd-1m-ohlcv-forex-historical-data",
        "commit": "d7c7be3ebabea6829ac0828ff0fe14c2e567e1e3",
        "file": "EURUSD_1m.csv",
        "blob": "a3b314549440faabf0f6ef3051087a6ba72582b5",
        "rows": 189940,
        "kind": "usd_quote",
    },
    "GBPUSD": {
        "repo": "getdata-finance/gbpusd-1m-ohlcv-forex-historical-data",
        "commit": "2ff10e3bfd0160a93afe6c867158083e07d966d6",
        "file": "GBPUSD_1m.csv",
        "blob": "c08632a8c65e358efcb0146a2ab27084ef12b75a",
        "rows": 189876,
        "kind": "usd_quote",
    },
    "USDJPY": {
        "repo": "getdata-finance/usdjpy-1m-ohlcv-forex-historical-data",
        "commit": "ff31183928d89096d08cd3cf32316d3b42397bcb",
        "file": "USDJPY_1m.csv",
        "blob": "acd5f7e96c69a69f1193ae9c95fbfc6cdbfb777d",
        "rows": 189765,
        "kind": "jpy_quote",
    },
    "EURJPY": {
        "repo": "getdata-finance/eurjpy-1m-ohlcv-forex-historical-data",
        "commit": "eb85398a913fb6304b1ea17c661f9ec58891ce31",
        "file": "EURJPY_1m.csv",
        "blob": "f79f4acc7fd140a63a2c120f08516fb239b489f5",
        "rows": 189916,
        "kind": "eurjpy",
    },
    "AUDUSD": {
        "repo": "getdata-finance/audusd-1m-ohlcv-forex-historical-data",
        "commit": "97b572279e9f4cf83d8e40e69afb8d9a3b05d39f",
        "file": "AUDUSD_1m.csv",
        "blob": "d1604b891bbd4fb65cc4c06b8ec7b6d5813eeff3",
        "rows": 189815,
        "kind": "usd_quote",
    },
    "USDCAD": {
        "repo": "getdata-finance/usdcad-1m-ohlcv-forex-historical-data",
        "commit": "108c13fa875437fde58c11d89d987b1c64ee1e5d",
        "file": "USDCAD_1m.csv",
        "blob": "901411b8fdc223ec14ce473429e15ff58b62e83d",
        "rows": 189719,
        "kind": "cad_quote",
    },
    "USDCHF": {
        "repo": "getdata-finance/usdchf-1m-ohlcv-forex-historical-data",
        "commit": "545c371fd14537cff8cf52ca4ac8c67cae46f80f",
        "file": "USDCHF_1m.csv",
        "blob": "6ebec50b4c26380526b25f3d6ad3c65c0de11918",
        "rows": 189553,
        "kind": "chf_quote",
    },
    "XAGUSD": {
        "repo": "getdata-finance/xagusd-1m-ohlcv-metals-historical-data",
        "commit": "5e3f6bdee52b79ce0006d459fce7d324bb1fe36a",
        "file": "XAGUSD_1m.csv",
        "blob": "ef933e44d0430195d0d477f83ad5b8b7d690b900",
        "rows": 180106,
        "kind": "xag_forecast_only",
    },
    "NAS100": {
        "repo": "getdata-finance/nas100-1m-ohlcv-index-historical-data",
        "commit": "5260d251ecc38918fa3d464c4a2988f7dec25f0d",
        "file": "NAS100_1m.csv",
        "blob": "204a04ca70579a0ea89953e9bd4dc1f35b30a336",
        "rows": 180750,
        "kind": "index_forecast_only",
    },
    "US30": {
        "repo": "getdata-finance/us30-1m-ohlcv-index-historical-data",
        "commit": "66841c6540c1d7b6a22b908c5977cf738f8737e8",
        "file": "US30_1m.csv",
        "blob": "28e9d0c5b00bface9117f393b2184b2c87319806",
        "rows": 180658,
        "kind": "index_forecast_only",
    },
    "SPX500": {
        "repo": "getdata-finance/spx500-1m-ohlcv-index-historical-data",
        "commit": "71f7399603f3ba6ee931668dad58c4b323f83f81",
        "file": "SPX500_1m.csv",
        "blob": "1fd0ae9813edc333da5c2b831555c791b7310d6f",
        "rows": 180576,
        "kind": "index_forecast_only",
    },
}


def raw_url(meta: dict) -> str:
    return f"https://raw.githubusercontent.com/{meta['repo']}/{meta['commit']}/{meta['file']}"


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def download_pinned(symbol: str, cache_dir: Path) -> Path:
    meta = SOURCES[symbol]
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{symbol}_{meta['commit'][:12]}.csv"
    if path.exists():
        data = path.read_bytes()
        if git_blob_sha(data) == meta["blob"]:
            return path
        path.unlink()

    req = urllib.request.Request(
        raw_url(meta),
        headers={"User-Agent": "target-first-trading-system-engine-k/0.1"},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = resp.read()

    got = git_blob_sha(data)
    if got != meta["blob"]:
        raise RuntimeError(f"{symbol}: blob SHA mismatch: expected {meta['blob']} got {got}")
    path.write_bytes(data)
    return path


def load_csv(path: Path, symbol: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = ["datetime", "open", "high", "low", "close", "volume"]
    if list(df.columns[:6]) != required:
        raise ValueError(f"{symbol}: unexpected columns {list(df.columns)}")

    df = df[required].copy()
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="raise")
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = pd.to_numeric(df[c], errors="raise")

    if len(df) != SOURCES[symbol]["rows"]:
        raise ValueError(f"{symbol}: expected {SOURCES[symbol]['rows']} rows, got {len(df)}")
    if df["datetime"].duplicated().any():
        raise ValueError(f"{symbol}: duplicate timestamps")
    if not df["datetime"].is_monotonic_increasing:
        raise ValueError(f"{symbol}: timestamps not monotonic")
    if (df[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError(f"{symbol}: non-positive price")
    if (df["high"] < df[["open", "close", "low"]].max(axis=1)).any():
        raise ValueError(f"{symbol}: invalid high geometry")
    if (df["low"] > df[["open", "close", "high"]].min(axis=1)).any():
        raise ValueError(f"{symbol}: invalid low geometry")

    # Freeze experiment to complete days through Sep 22.
    df = df[df["datetime"] < pd.Timestamp("2026-09-23", tz="UTC")].reset_index(drop=True)
    return df


def resample_ohlc(
    df: pd.DataFrame,
    rule: str,
    required_count: Optional[int] = None,
) -> pd.DataFrame:
    x = df.set_index("datetime")
    out = x.resample(rule, label="left", closed="left").agg(
        open=("open", "first"),
        high=("high", "max"),
        low=("low", "min"),
        close=("close", "last"),
        volume=("volume", "sum"),
        n=("close", "count"),
    )
    out = out.dropna(subset=["open", "high", "low", "close"])
    if required_count is not None:
        out = out[out["n"] == required_count]
    return out.reset_index()


def add_true_range(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    prev = out["close"].shift(1)
    out["tr"] = np.maximum.reduce([
        (out["high"] - out["low"]).to_numpy(),
        (out["high"] - prev).abs().fillna(0).to_numpy(),
        (out["low"] - prev).abs().fillna(0).to_numpy(),
    ])
    return out


def build_context(df1: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    # Structural/feature bars must be complete. Incomplete bins around closures
    # are excluded rather than silently treated as ordinary 5m/1h bars.
    b5 = add_true_range(resample_ohlc(df1, "5min", required_count=5))
    h1 = add_true_range(resample_ohlc(df1, "1h", required_count=60))

    # Hourly statistics become available only after the hour completes.
    h1["available_ts"] = h1["datetime"] + pd.Timedelta(hours=1)
    h1["mtr20"] = h1["tr"].rolling(20, min_periods=20).median()

    # 5m feature foundations, all based on current/past completed bars.
    b5["ema10"] = b5["close"].ewm(span=10, adjust=False).mean()
    b5["ema30"] = b5["close"].ewm(span=30, adjust=False).mean()
    b5["ret5"] = b5["close"].pct_change(1)
    b5["ret15"] = b5["close"].pct_change(3)
    b5["ret30"] = b5["close"].pct_change(6)
    b5["ret60"] = b5["close"].pct_change(12)
    b5["ret120"] = b5["close"].pct_change(24)
    b5["range60_high"] = b5["high"].rolling(12, min_periods=12).max()
    b5["range60_low"] = b5["low"].rolling(12, min_periods=12).min()
    b5["range240_high"] = b5["high"].rolling(48, min_periods=48).max()
    b5["range240_low"] = b5["low"].rolling(48, min_periods=48).min()
    b5["median_tr20_5m"] = b5["tr"].rolling(20, min_periods=20).median()

    # Strict 2-left / 2-right pivot. A pivot at j is only known after j+2 is complete.
    b5["pivot_high_raw"] = (
        (b5["high"] > b5["high"].shift(1))
        & (b5["high"] > b5["high"].shift(2))
        & (b5["high"] > b5["high"].shift(-1))
        & (b5["high"] > b5["high"].shift(-2))
    )
    b5["pivot_low_raw"] = (
        (b5["low"] < b5["low"].shift(1))
        & (b5["low"] < b5["low"].shift(2))
        & (b5["low"] < b5["low"].shift(-1))
        & (b5["low"] < b5["low"].shift(-2))
    )
    return b5, h1


def _latest_confirmed_pivot(
    b5: pd.DataFrame, i: int, direction: str, max_age_bars: int = 12
) -> Optional[float]:
    # At decision bar i, pivot j can be used only if j+2 <= i.
    jmax = i - 2
    if jmax < 2:
        return None
    jmin = max(2, i - max_age_bars)
    col = "pivot_low_raw" if direction == "long" else "pivot_high_raw"
    px = "low" if direction == "long" else "high"
    for j in range(jmax, jmin - 1, -1):
        if bool(b5.iloc[j][col]):
            return float(b5.iloc[j][px])
    return None


def next_active_entry(df1: pd.DataFrame, decision_start: pd.Timestamp) -> Optional[tuple[pd.Timestamp, float]]:
    end = decision_start + pd.Timedelta(minutes=5)
    # Keep pandas' timezone-aware Timestamp semantics; numpy datetime64 would
    # strip timezone metadata and can create tz-aware/tz-naive comparison errors.
    k = int(df1["datetime"].searchsorted(end, side="left"))
    if k >= len(df1):
        return None
    row = df1.iloc[k]
    entry_ts = row["datetime"]
    if entry_ts - end > pd.Timedelta(minutes=MAX_NEXT_ENTRY_GAP_MINUTES):
        return None
    return entry_ts, float(row["open"])


def latest_completed_hour_context(h1: pd.DataFrame, decision_end: pd.Timestamp) -> Optional[dict]:
    # Search directly on the timezone-aware pandas Series to avoid stripping UTC.
    k = int(h1["available_ts"].searchsorted(decision_end, side="right")) - 1
    if k < 0:
        return None
    row = h1.iloc[k]
    if pd.isna(row["mtr20"]) or float(row["mtr20"]) <= 0:
        return None
    return {"mtr20": float(row["mtr20"]), "hour_ts": row["datetime"]}


def usd_value_per_native_unit_1lot(
    symbol: str,
    entry: float,
    usd_jpy: Optional[float] = None,
) -> Optional[float]:
    kind = SOURCES[symbol]["kind"]
    if kind == "xau":
        return 100.0  # USD per $1 XAU move at 1 lot under 100oz convention.
    if kind == "usd_quote":
        return 100000.0
    if kind in ("jpy_quote", "cad_quote", "chf_quote"):
        return 100000.0 / entry
    if kind == "eurjpy":
        if usd_jpy is None or usd_jpy <= 0:
            return None
        return 100000.0 / usd_jpy
    return None


def notional_usd_1lot(
    symbol: str,
    entry: float,
    usd_jpy: Optional[float] = None,
) -> Optional[float]:
    kind = SOURCES[symbol]["kind"]
    if kind == "xau":
        return entry * 100.0
    if kind == "usd_quote":
        return entry * 100000.0
    if kind in ("jpy_quote", "cad_quote", "chf_quote"):
        return 100000.0
    if kind == "eurjpy":
        if usd_jpy is None or usd_jpy <= 0:
            return None
        eurusd_cross = entry / usd_jpy
        return eurusd_cross * 100000.0
    return None


def research_costs(target_usd: float) -> dict:
    return {
        "primary_cost_usd": target_usd * PRIMARY_COST_FRACTION_OF_GROSS_TARGET,
        "stress_cost_usd": target_usd * STRESS_COST_FRACTION_OF_GROSS_TARGET,
    }


def qualification_probability_floor(
    target_usd: float,
    stop_risk_usd: float,
    primary_cost_usd: float,
) -> dict:
    denom = target_usd + stop_risk_usd
    if denom <= 0:
        return {"breakeven_probability": None, "required_probability": None}
    p_be = (stop_risk_usd + primary_cost_usd) / denom
    required = max(PRIMARY_PROBABILITY_FLOOR, p_be + BREAKEVEN_PROBABILITY_BUFFER)
    return {"breakeven_probability": p_be, "required_probability": required}


def floor_lot(x: float, step: float = RESEARCH_LOT_STEP) -> float:
    if not math.isfinite(x) or x <= 0:
        return 0.0
    return math.floor((x + 1e-12) / step) * step


def candidate_economics(
    symbol: str,
    entry: float,
    stop: float,
    mtr20: float,
    usd_jpy: Optional[float] = None,
) -> Dict[str, dict]:
    if SOURCES[symbol]["kind"] in ("xag_forecast_only", "index_forecast_only"):
        return {}
    if symbol == "XAUUSD":
        distances = {"T30": 3.0, "T40": 4.0, "T50": 5.0}
        lots = {"T30": 0.10, "T40": 0.10, "T50": 0.10}
        targets = {"T30": 30.0, "T40": 40.0, "T50": 50.0}
    else:
        distances = {"T30": 0.14*mtr20, "T40": 0.19*mtr20, "T50": 0.23*mtr20}
        targets = {"T30": 30.0, "T40": 40.0, "T50": 50.0}
        v = usd_value_per_native_unit_1lot(symbol, entry, usd_jpy)
        if v is None or v <= 0:
            return {}
        lots = {k: floor_lot(targets[k] / (distances[k] * v)) for k in distances}

    v = usd_value_per_native_unit_1lot(symbol, entry, usd_jpy)
    n1 = notional_usd_1lot(symbol, entry, usd_jpy)
    if v is None or n1 is None:
        return {}
    stop_dist = abs(entry-stop)
    out = {}
    for k in distances:
        lot = lots[k]
        risk = stop_dist * v * lot
        notional = n1 * lot
        margin = notional / RESEARCH_LEVERAGE_REFERENCE
        costs = research_costs(targets[k])
        probs = qualification_probability_floor(
            targets[k], risk, costs["primary_cost_usd"]
        )
        risk_ok = lot >= RESEARCH_LOT_STEP and risk <= PRIMARY_STOP_RISK_USD
        notional_ok = notional <= REFERENCE_EQUITY_USD * MAX_NOTIONAL_TO_EQUITY
        margin_ok = margin <= REFERENCE_EQUITY_USD * MAX_MARGIN_FRACTION_OF_EQUITY
        out[k] = {
            "target_usd": targets[k],
            "distance": distances[k],
            "lot": lot,
            "stop_risk_usd": risk,
            "notional_usd": notional,
            "notional_to_equity": notional / REFERENCE_EQUITY_USD,
            "research_margin_usd_at_1_500": margin,
            **costs,
            **probs,
            "admissible_risk": bool(risk_ok),
            "admissible_notional": bool(notional_ok),
            "admissible_margin": bool(margin_ok),
            "execution_admissible_pre_probability": bool(risk_ok and notional_ok and margin_ok),
        }
    return out


def preflight_states(
    symbol: str,
    df1: pd.DataFrame,
    usd_jpy_df: Optional[pd.DataFrame] = None,
) -> dict:
    b5, h1 = build_context(df1)
    # Exclude weekends and only score 00:00-20:00 decision-bar completion.
    candidate_count = 0
    long_structural = 0
    short_structural = 0
    economic_rungs = 0
    state_examples = []

    usd_jpy_series = None
    if usd_jpy_df is not None:
        usd_jpy_series = usd_jpy_df.set_index("datetime")["close"].sort_index()

    for i in range(50, len(b5)):
        row = b5.iloc[i]
        decision_start = row["datetime"]
        decision_end = decision_start + pd.Timedelta(minutes=5)
        if decision_end.weekday() >= 5:
            continue
        minutes = decision_end.hour*60 + decision_end.minute
        if not (0 <= minutes < 20*60):
            continue
        hc = latest_completed_hour_context(h1, decision_end)
        if hc is None:
            continue
        nxt = next_active_entry(df1, decision_start)
        if nxt is None:
            continue
        entry_ts, entry = nxt
        if entry_ts.date() != decision_start.date():
            continue

        usd_jpy = None
        if symbol == "EURJPY" and usd_jpy_series is not None:
            pos = usd_jpy_series.index.searchsorted(entry_ts, side="right") - 1
            if pos >= 0:
                usd_jpy = float(usd_jpy_series.iloc[pos])

        for direction in ("long", "short"):
            p = _latest_confirmed_pivot(b5, i, direction)
            if p is None:
                continue
            stop = p
            # One research tick buffer.
            if symbol in ("USDJPY","EURJPY"):
                tick = 0.001
            elif symbol == "XAUUSD":
                tick = 0.001
            else:
                tick = 0.00001
            stop = stop - tick if direction == "long" else stop + tick
            if direction == "long" and not stop < entry:
                continue
            if direction == "short" and not stop > entry:
                continue

            if direction == "long":
                long_structural += 1
            else:
                short_structural += 1
            candidate_count += 1

            econ = candidate_economics(symbol, entry, stop, hc["mtr20"], usd_jpy)
            economic_rungs += sum(
                1 for x in econ.values()
                if x.get("execution_admissible_pre_probability", False)
            )

            if len(state_examples) < 5:
                state_examples.append({
                    "decision": str(decision_end),
                    "direction": direction,
                    "entry": entry,
                    "stop": stop,
                    "mtr20": hc["mtr20"],
                    "economic": econ,
                })

    return {
        "symbol": symbol,
        "universe_class": (
            "execution"
            if symbol in EXECUTION_MARKETS
            else "forecast_only"
        ),
        "m1_rows_after_cut": len(df1),
        "first_ts": str(df1["datetime"].iloc[0]),
        "last_ts": str(df1["datetime"].iloc[-1]),
        "bars_5m": len(b5),
        "bars_1h": len(h1),
        "structural_states": candidate_count,
        "long_states": long_structural,
        "short_states": short_structural,
        "admissible_target_rungs": economic_rungs,
        "examples": state_examples,
    }


def self_tests() -> list[str]:
    passed = []

    # Git blob computation sanity.
    data = b"hello\n"
    expected = hashlib.sha1(f"blob {len(data)}\0".encode()+data).hexdigest()
    assert git_blob_sha(data) == expected
    passed.append("git_blob_sha")

    # Lot floor never rounds upward.
    for x in [0.001,0.019,0.021,1.237]:
        y = floor_lot(x)
        assert y <= x + 1e-12
        assert abs((y / RESEARCH_LOT_STEP) - round(y/RESEARCH_LOT_STEP)) < 1e-9
    passed.append("lot_floor")

    # USD quote P&L math.
    assert abs(usd_value_per_native_unit_1lot("EURUSD",1.2)-100000.0) < 1e-9
    passed.append("usd_quote_value")

    # XAU convention.
    assert abs(usd_value_per_native_unit_1lot("XAUUSD",4000)-100.0) < 1e-9
    passed.append("xau_value")

    # JPY conversion.
    assert abs(usd_value_per_native_unit_1lot("USDJPY",150)-666.6666666667) < 1e-6
    passed.append("jpy_quote_value")

    # Universe separation is frozen before outcomes.
    assert set(EXECUTION_MARKETS).isdisjoint(set(FORECAST_ONLY_MARKETS))
    assert set(EXECUTION_MARKETS) | set(FORECAST_ONLY_MARKETS) == set(SOURCES)
    passed.append("universe_separation")

    # Primary and stress cost conventions are target-relative research stresses.
    cc = research_costs(50.0)
    assert abs(cc["primary_cost_usd"] - 5.0) < 1e-12
    assert abs(cc["stress_cost_usd"] - 10.0) < 1e-12
    passed.append("research_cost_schedule")

    # Probability gate is never below 60% and carries a break-even buffer.
    pq = qualification_probability_floor(50.0,20.0,5.0)
    assert pq["required_probability"] >= 0.60
    assert pq["required_probability"] >= pq["breakeven_probability"] + 0.05 - 1e-12
    passed.append("probability_floor")

    # Notional/margin research gate is internally consistent at the frozen 1:500 reference.
    max_notional = REFERENCE_EQUITY_USD * MAX_NOTIONAL_TO_EQUITY
    assert abs(max_notional / RESEARCH_LEVERAGE_REFERENCE - REFERENCE_EQUITY_USD * MAX_MARGIN_FRACTION_OF_EQUITY) < 1e-9
    passed.append("notional_margin_gate")

    # Entry must not jump across a long closure.
    toy = pd.DataFrame({
        "datetime": pd.to_datetime([
            "2026-01-05T10:00:00Z","2026-01-05T10:01:00Z",
            "2026-01-05T10:02:00Z","2026-01-05T10:03:00Z",
            "2026-01-05T10:04:00Z","2026-01-05T10:20:00Z",
        ]),
        "open":[1,1,1,1,1,2],
    })
    assert next_active_entry(toy, pd.Timestamp("2026-01-05T10:00:00Z")) is None
    passed.append("entry_gap_reject")

    return passed
