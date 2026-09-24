#!/usr/bin/env python3
"""EXP-023 Engine K v0.2 training + June calibration only.

This runner is intentionally sealed at 2026-07-01 UTC:
- fit: 2026-03-23 through 2026-05-31
- sigmoid/Platt calibration: 2026-06-01 through 2026-06-30
- no July-August secondary-test states/outcomes
- no September final-holdout states/outcomes
"""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from pathlib import Path
from typing import Optional

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from engine_k_v0_1 import (
    SOURCES,
    EXECUTION_MARKETS,
    FORECAST_ONLY_MARKETS,
    build_context,
    _latest_confirmed_pivot,
    next_active_entry,
    latest_completed_hour_context,
    causal_state_features,
    rung_features,
    usd_value_per_native_unit_1lot,
    download_pinned,
    self_tests as engine_self_tests,
)
from engine_k_v0_2 import candidate_economics_v02, self_tests_v02

ROOT = Path(__file__).resolve().parents[2]
CACHE = Path("/tmp/engine-k-v02-training-data")
OUT = ROOT / "research/results"
OUT.mkdir(parents=True, exist_ok=True)

TRAIN_START = pd.Timestamp("2026-03-23", tz="UTC")
TRAIN_END_EXCLUSIVE = pd.Timestamp("2026-06-01", tz="UTC")
CAL_START = pd.Timestamp("2026-06-01", tz="UTC")
SEALED_START = pd.Timestamp("2026-07-01", tz="UTC")
SESSION_CUTOFF_HOUR = 20
MAX_ACTIVE_M1 = 120
RUNG_ORDER = ("T30", "T40", "T50")
RUNG_RANK = {r: i for i, r in enumerate(RUNG_ORDER)}

HGB_PARAMS = dict(
    learning_rate=0.05,
    max_iter=150,
    max_leaf_nodes=15,
    min_samples_leaf=100,
    l2_regularization=1.0,
    random_state=20260923,
)
PLATT_PARAMS = dict(
    C=1_000_000.0,
    solver="lbfgs",
    max_iter=1000,
)
BASELINE_PARAMS = dict(
    C=1.0,
    solver="lbfgs",
    max_iter=1000,
    random_state=20260923,
)

COMMON_NUMERIC_FEATURES = [
    "signed_move_5m_volnorm",
    "signed_move_15m_volnorm",
    "signed_move_30m_volnorm",
    "signed_move_60m_volnorm",
    "signed_move_120m_volnorm",
    "ema10_minus_ema30_dir_volnorm",
    "ema10_slope_15m_dir_volnorm",
    "ema30_slope_15m_dir_volnorm",
    "distance_to_60m_high_volnorm",
    "distance_from_60m_low_volnorm",
    "position_in_60m_range",
    "position_in_240m_range",
    "tr5_over_median20_tr5",
    "range15_over_range60",
    "range30_over_range120",
    "hourly_tr_percentile_prior20",
    "compression_expansion_ratio",
    "body_over_range",
    "upper_wick_over_range",
    "lower_wick_over_range",
    "prior3_directional_body_balance",
    "stop_distance_native",
    "stop_distance_over_mtr20",
    "stop_risk_usd",
    "utc_hour_sin",
    "utc_hour_cos",
    "weekday",
]
ENCODED_FEATURE_COLUMNS = (
    COMMON_NUMERIC_FEATURES
    + [f"market__{s}" for s in EXECUTION_MARKETS]
    + ["direction__long", "direction__short"]
)


def repo_sha() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_scoped_csv(path: Path, symbol: str, cutoff: pd.Timestamp = SEALED_START) -> pd.DataFrame:
    """Parse only rows earlier than cutoff; later rows remain unparsed transport bytes."""
    required = ["datetime", "open", "high", "low", "close", "volume"]
    parts = []
    reached_cutoff = False

    for chunk in pd.read_csv(path, chunksize=50000):
        if list(chunk.columns[:6]) != required:
            raise ValueError(f"{symbol}: unexpected columns {list(chunk.columns)}")
        chunk = chunk[required].copy()
        chunk["datetime"] = pd.to_datetime(chunk["datetime"], utc=True, errors="raise")

        before = chunk["datetime"] < cutoff
        if before.any():
            scoped = chunk.loc[before].copy()
            for col in ["open", "high", "low", "close", "volume"]:
                scoped[col] = pd.to_numeric(scoped[col], errors="raise")
            parts.append(scoped)

        if (~before).any():
            reached_cutoff = True
            break

    if not reached_cutoff:
        raise RuntimeError(f"{symbol}: sealed-start sentinel not encountered")

    df = pd.concat(parts, ignore_index=True)
    df = df[df["datetime"] >= TRAIN_START].reset_index(drop=True)
    if df.empty:
        raise RuntimeError(f"{symbol}: no scoped rows")
    if not (df["datetime"] < cutoff).all():
        raise RuntimeError(f"{symbol}: sealed rows parsed into scope")
    if df["datetime"].duplicated().any() or not df["datetime"].is_monotonic_increasing:
        raise RuntimeError(f"{symbol}: timestamp integrity failed")
    if (df[["open", "high", "low", "close"]] <= 0).any().any():
        raise RuntimeError(f"{symbol}: non-positive price")
    if (df["high"] < df[["open", "close", "low"]].max(axis=1)).any():
        raise RuntimeError(f"{symbol}: invalid high")
    if (df["low"] > df[["open", "close", "high"]].min(axis=1)).any():
        raise RuntimeError(f"{symbol}: invalid low")
    return df


def research_tick(symbol: str) -> float:
    if symbol in ("XAUUSD", "USDJPY", "EURJPY"):
        return 0.001
    return 0.00001


def session_cutoff(ts: pd.Timestamp) -> pd.Timestamp:
    return ts.normalize() + pd.Timedelta(hours=SESSION_CUTOFF_HOUR)


def _label_cache(df1: pd.DataFrame) -> dict:
    cache=df1.attrs.get("_engine_k_label_cache")
    if cache is None:
        cache={"times":pd.DatetimeIndex(df1["datetime"]),
               "high":df1["high"].to_numpy(dtype=float,copy=False),
               "low":df1["low"].to_numpy(dtype=float,copy=False),
               "close":df1["close"].to_numpy(dtype=float,copy=False)}
        df1.attrs["_engine_k_label_cache"]=cache
    return cache

def label_target_first(df1,entry_ts,entry,stop,direction,target_distance,lot,usd_value_per_native_unit,primary_cost_usd,stress_cost_usd):
    cache=_label_cache(df1); times=cache["times"]
    start=int(times.searchsorted(entry_ts,side="left"))
    if start>=len(times) or times[start]!=entry_ts:
        raise RuntimeError("entry timestamp missing from M1 data")
    end=min(start+MAX_ACTIVE_M1,int(times.searchsorted(session_cutoff(entry_ts),side="left")),len(times))
    if end<=start:
        raise RuntimeError("zero active M1 bars in label horizon")
    high,low,close=cache["high"][start:end],cache["low"][start:end],cache["close"][start:end]
    target=entry+target_distance if direction=="long" else entry-target_distance
    if direction=="long":
        stop_hits,target_hits=low<=stop,high>=target
    else:
        stop_hits,target_hits=high>=stop,low<=target
    si_arr=np.flatnonzero(stop_hits); ti_arr=np.flatnonzero(target_hits)
    si=int(si_arr[0]) if len(si_arr) else None
    ti=int(ti_arr[0]) if len(ti_arr) else None
    if si is not None and (ti is None or si<=ti):
        gross=-abs(entry-stop)*usd_value_per_native_unit*lot; pos=start+si
        return {"label":0,"outcome":"stop","exit_ts":times[pos],"active_m1_bars":si+1,
                "gross_pnl_usd":gross,"primary_net_pnl_usd":gross-primary_cost_usd,
                "stress_net_pnl_usd":gross-stress_cost_usd,"horizon_mark_price":None}
    if ti is not None:
        gross=target_distance*usd_value_per_native_unit*lot; pos=start+ti
        return {"label":1,"outcome":"target","exit_ts":times[pos],"active_m1_bars":ti+1,
                "gross_pnl_usd":gross,"primary_net_pnl_usd":gross-primary_cost_usd,
                "stress_net_pnl_usd":gross-stress_cost_usd,"horizon_mark_price":None}
    last_pos=end-1; last_close=float(close[-1]); sign=1.0 if direction=="long" else -1.0
    gross=sign*(last_close-entry)*usd_value_per_native_unit*lot
    return {"label":0,"outcome":"timeout","exit_ts":times[last_pos],"active_m1_bars":end-start,
            "gross_pnl_usd":gross,"primary_net_pnl_usd":gross-primary_cost_usd,
            "stress_net_pnl_usd":gross-stress_cost_usd,"horizon_mark_price":last_close}
def label_self_tests() -> list[str]:
    passed = []

    base = pd.Timestamp("2026-05-04T10:00:00Z")
    both = pd.DataFrame({
        "datetime": [base],
        "open": [100.0], "high": [103.0], "low": [98.0], "close": [101.0], "volume": [1.0],
    })
    x = label_target_first(both, base, 100.0, 99.0, "long", 2.0, 1.0, 1.0, 0.0, 0.0)
    assert x["outcome"] == "stop" and x["label"] == 0
    passed.append("same_bar_stop_first")

    target_df = pd.DataFrame({
        "datetime": [base, base + pd.Timedelta(minutes=1)],
        "open": [100.0, 101.0], "high": [101.0, 102.5], "low": [99.5, 100.5],
        "close": [101.0, 102.0], "volume": [1.0, 1.0],
    })
    x = label_target_first(target_df, base, 100.0, 99.0, "long", 2.0, 1.0, 1.0, 0.0, 0.0)
    assert x["outcome"] == "target" and x["active_m1_bars"] == 2
    passed.append("later_target")

    rows = []
    for i in range(121):
        high = 100.5 if i < 120 else 103.0
        rows.append((base + pd.Timedelta(minutes=i), 100.0, high, 99.5, 100.1, 1.0))
    h = pd.DataFrame(rows, columns=["datetime","open","high","low","close","volume"])
    x = label_target_first(h, base, 100.0, 98.0, "long", 2.0, 1.0, 1.0, 0.0, 0.0)
    assert x["outcome"] == "timeout" and x["active_m1_bars"] == 120
    passed.append("horizon_120_includes_entry")

    late = pd.Timestamp("2026-05-04T19:59:00Z")
    s = pd.DataFrame({
        "datetime": [late, late + pd.Timedelta(minutes=1)],
        "open": [100.0,100.0], "high": [100.5,103.0], "low":[99.5,99.5],
        "close":[100.1,102.0], "volume":[1.0,1.0],
    })
    x = label_target_first(s, late, 100.0, 98.0, "long", 2.0, 1.0, 1.0, 0.0, 0.0)
    assert x["outcome"] == "timeout" and x["active_m1_bars"] == 1
    passed.append("session_cutoff_2000")

    return passed


def build_labeled_rows(
    symbol: str,
    df1: pd.DataFrame,
    usd_jpy_df: Optional[pd.DataFrame] = None,
) -> list[dict]:
    b5, h1 = build_context(df1)
    usd_jpy_series = None
    if usd_jpy_df is not None:
        usd_jpy_series = usd_jpy_df.set_index("datetime")["close"].sort_index()

    rows = []
    tick = research_tick(symbol)

    for i in range(50, len(b5)):
        bar = b5.iloc[i]
        decision_start = bar["datetime"]
        decision_end = decision_start + pd.Timedelta(minutes=5)
        if decision_end >= SEALED_START:
            break
        if decision_end < TRAIN_START or decision_end.weekday() >= 5:
            continue
        minutes = decision_end.hour * 60 + decision_end.minute
        if not (0 <= minutes < SESSION_CUTOFF_HOUR * 60):
            continue

        period = "train" if decision_end < TRAIN_END_EXCLUSIVE else "calibration"
        hc = latest_completed_hour_context(h1, decision_end)
        if hc is None:
            continue
        nxt = next_active_entry(df1, decision_start)
        if nxt is None:
            continue
        entry_ts, entry = nxt
        if entry_ts.date() != decision_start.date() or entry_ts >= session_cutoff(entry_ts):
            continue

        usd_jpy = None
        if symbol == "EURJPY" and usd_jpy_series is not None:
            pos = usd_jpy_series.index.searchsorted(entry_ts, side="right") - 1
            if pos >= 0:
                usd_jpy = float(usd_jpy_series.iloc[pos])

        for direction in ("long", "short"):
            pivot = _latest_confirmed_pivot(b5, i, direction)
            if pivot is None:
                continue
            stop = pivot - tick if direction == "long" else pivot + tick
            if direction == "long" and not stop < entry:
                continue
            if direction == "short" and not stop > entry:
                continue

            common = causal_state_features(symbol, b5, i, direction, entry, stop, hc)
            if common is None:
                continue
            econ = candidate_economics_v02(symbol, entry, stop, usd_jpy)
            v = usd_value_per_native_unit_1lot(symbol, entry, usd_jpy)
            if v is None or v <= 0:
                continue

            for rung in RUNG_ORDER:
                e = econ.get(rung)
                if not e or not e.get("execution_admissible_pre_probability", False):
                    continue

                outcome = label_target_first(
                    df1=df1,
                    entry_ts=entry_ts,
                    entry=entry,
                    stop=stop,
                    direction=direction,
                    target_distance=float(e["distance"]),
                    lot=float(e["lot"]),
                    usd_value_per_native_unit=float(v),
                    primary_cost_usd=float(e["primary_cost_usd"]),
                    stress_cost_usd=float(e["stress_cost_usd"]),
                )
                features = rung_features(common, e)

                row = {
                    "period": period,
                    "symbol": symbol,
                    "direction": direction,
                    "rung": rung,
                    "decision_ts": decision_end,
                    "entry_ts": entry_ts,
                    "entry": float(entry),
                    "stop": float(stop),
                    "target_distance": float(e["distance"]),
                    "target_usd_nominal": float(e["target_usd_nominal"]),
                    "gross_target_usd_actual": float(e["gross_target_usd_actual"]),
                    "lot": float(e["lot"]),
                    "stop_risk_usd": float(e["stop_risk_usd"]),
                    "primary_cost_usd": float(e["primary_cost_usd"]),
                    "stress_cost_usd": float(e["stress_cost_usd"]),
                    "breakeven_probability": float(e["breakeven_probability"]),
                    "required_probability": float(e["required_probability"]),
                    **outcome,
                    "features": features,
                }
                rows.append(row)

    return rows


def encode_rows(rows: list[dict]) -> np.ndarray:
    data = []
    for row in rows:
        f = row["features"]
        vals = [float(f[k]) for k in COMMON_NUMERIC_FEATURES]
        vals.extend(1.0 if row["symbol"] == s else 0.0 for s in EXECUTION_MARKETS)
        vals.extend([
            1.0 if row["direction"] == "long" else 0.0,
            1.0 if row["direction"] == "short" else 0.0,
        ])
        data.append(vals)
    x = np.asarray(data, dtype=float)
    if x.ndim != 2 or x.shape[1] != len(ENCODED_FEATURE_COLUMNS):
        raise RuntimeError("encoded feature shape mismatch")
    if not np.isfinite(x).all():
        raise RuntimeError("non-finite encoded feature")
    return x


def clipped_logit(p: np.ndarray) -> np.ndarray:
    q = np.clip(np.asarray(p, dtype=float), 1e-6, 1 - 1e-6)
    return np.log(q / (1 - q)).reshape(-1, 1)


def safe_auc(y: np.ndarray, p: np.ndarray) -> Optional[float]:
    return float(roc_auc_score(y, p)) if len(np.unique(y)) == 2 else None


def probability_metrics(y: np.ndarray, p: np.ndarray) -> dict:
    p = np.clip(np.asarray(p, dtype=float), 1e-9, 1 - 1e-9)
    y = np.asarray(y, dtype=int)
    quantiles = {str(q): float(np.quantile(p, q)) for q in [0,0.1,0.25,0.5,0.75,0.9,1]}
    bins = []
    edges = np.linspace(0, 1, 11)
    for i in range(10):
        lo, hi = edges[i], edges[i+1]
        mask = (p >= lo) & (p < hi if i < 9 else p <= hi)
        if mask.any():
            bins.append({
                "lo": float(lo), "hi": float(hi), "n": int(mask.sum()),
                "mean_pred": float(p[mask].mean()),
                "observed_rate": float(y[mask].mean()),
            })
    return {
        "n": int(len(y)),
        "positive_rate": float(y.mean()) if len(y) else None,
        "brier": float(brier_score_loss(y, p)),
        "log_loss": float(log_loss(y, p, labels=[0,1])),
        "roc_auc": safe_auc(y, p),
        "probability_quantiles": quantiles,
        "calibration_bins": bins,
    }


def fit_rung_model(train_rows: list[dict], cal_rows: list[dict]) -> tuple[dict, dict]:
    x_train = encode_rows(train_rows)
    x_cal = encode_rows(cal_rows)
    y_train = np.asarray([r["label"] for r in train_rows], dtype=int)
    y_cal = np.asarray([r["label"] for r in cal_rows], dtype=int)

    if len(np.unique(y_train)) != 2 or len(np.unique(y_cal)) != 2:
        raise RuntimeError("both classes required in train and calibration")

    model = HistGradientBoostingClassifier(**HGB_PARAMS)
    model.fit(x_train, y_train)
    raw_train = model.predict_proba(x_train)[:,1]
    raw_cal = model.predict_proba(x_cal)[:,1]

    platt = LogisticRegression(**PLATT_PARAMS)
    platt.fit(clipped_logit(raw_cal), y_cal)
    p_train = platt.predict_proba(clipped_logit(raw_train))[:,1]
    p_cal = platt.predict_proba(clipped_logit(raw_cal))[:,1]

    baseline = Pipeline([
        ("scale", StandardScaler()),
        ("logit", LogisticRegression(**BASELINE_PARAMS)),
    ])
    baseline.fit(x_train, y_train)
    base_train = baseline.predict_proba(x_train)[:,1]
    base_cal = baseline.predict_proba(x_cal)[:,1]

    metrics = {
        "primary_raw": {
            "train": probability_metrics(y_train, raw_train),
            "calibration": probability_metrics(y_cal, raw_cal),
        },
        "primary_platt": {
            "train": probability_metrics(y_train, p_train),
            "calibration": probability_metrics(y_cal, p_cal),
        },
        "diagnostic_logistic": {
            "train": probability_metrics(y_train, base_train),
            "calibration": probability_metrics(y_cal, base_cal),
        },
        "platt_coef": float(platt.coef_[0][0]),
        "platt_intercept": float(platt.intercept_[0]),
    }

    bundle = {
        "model": model,
        "platt": platt,
        "baseline": baseline,
    }
    preds = {
        "train": p_train,
        "calibration": p_cal,
        "baseline_train": base_train,
        "baseline_calibration": base_cal,
    }
    return {"bundle": bundle, "metrics": metrics}, preds


def annotate_probabilities(rows: list[dict], probs: np.ndarray) -> None:
    if len(rows) != len(probs):
        raise RuntimeError("prediction length mismatch")
    for row, p in zip(rows, probs):
        p = float(p)
        ev = (
            p * row["gross_target_usd_actual"]
            - (1 - p) * row["stop_risk_usd"]
            - row["primary_cost_usd"]
        )
        stress_ev = (
            p * row["gross_target_usd_actual"]
            - (1 - p) * row["stop_risk_usd"]
            - row["stress_cost_usd"]
        )
        row["calibrated_probability"] = p
        row["primary_ev_usd"] = float(ev)
        row["stress_ev_usd"] = float(stress_ev)
        row["qualified"] = bool(
            p >= row["required_probability"]
            and ev > 0
        )


def max_drawdown(values: list[float]) -> float:
    equity = 0.0
    peak = 0.0
    mdd = 0.0
    for x in values:
        equity += x
        peak = max(peak, equity)
        mdd = max(mdd, peak - equity)
    return float(mdd)


def longest_run(flags: list[bool]) -> int:
    best = cur = 0
    for flag in flags:
        cur = cur + 1 if flag else 0
        best = max(best, cur)
    return best


def simulate_one_open(rows: list[dict], eligible_start: pd.Timestamp, eligible_end_exclusive: pd.Timestamp) -> dict:
    qualified = [r for r in rows if r.get("qualified")]
    qualified.sort(key=lambda r: (
        r["entry_ts"],
        -r["calibrated_probability"],
        -r["primary_ev_usd"],
        RUNG_RANK[r["rung"]],
        r["symbol"],
        r["direction"],
    ))

    by_entry = {}
    for r in qualified:
        by_entry.setdefault(r["entry_ts"], []).append(r)

    trades = []
    last_exit = None
    daily = {}

    for entry_ts in sorted(by_entry):
        if last_exit is not None and entry_ts <= last_exit:
            continue
        day = entry_ts.date().isoformat()
        realized_before = daily.get(day, 0.0)
        if realized_before <= -40.0 or realized_before >= 150.0:
            continue

        r = by_entry[entry_ts][0]
        trades.append(r)
        pnl = float(r["primary_net_pnl_usd"])
        daily[day] = realized_before + pnl
        last_exit = r["exit_ts"]

    eligible_days = pd.date_range(eligible_start.normalize(), eligible_end_exclusive - pd.Timedelta(days=1), freq="D", tz="UTC")
    eligible_days = [x.date().isoformat() for x in eligible_days if x.weekday() < 5]
    daily_values = [float(daily.get(d, 0.0)) for d in eligible_days]

    market_pnl = {}
    market_trades = {}
    for r in trades:
        market_pnl[r["symbol"]] = market_pnl.get(r["symbol"], 0.0) + float(r["primary_net_pnl_usd"])
        market_trades[r["symbol"]] = market_trades.get(r["symbol"], 0) + 1

    total_abs_market_pnl = sum(abs(x) for x in market_pnl.values())
    largest_abs_share = (
        max((abs(x) for x in market_pnl.values()), default=0.0) / total_abs_market_pnl
        if total_abs_market_pnl > 0 else 0.0
    )

    pnl_seq = [float(r["primary_net_pnl_usd"]) for r in trades]
    wins = [x for x in pnl_seq if x > 0]
    losses = [x for x in pnl_seq if x < 0]
    pf = sum(wins) / abs(sum(losses)) if losses else None

    return {
        "qualified_candidate_rungs_before_one_open": len(qualified),
        "actual_trades": len(trades),
        "target_hits": int(sum(r["label"] for r in trades)),
        "target_hit_rate": float(np.mean([r["label"] for r in trades])) if trades else None,
        "mean_break_even_probability": float(np.mean([r["breakeven_probability"] for r in trades])) if trades else None,
        "mean_required_probability": float(np.mean([r["required_probability"] for r in trades])) if trades else None,
        "mean_calibrated_probability": float(np.mean([r["calibrated_probability"] for r in trades])) if trades else None,
        "primary_net_pnl_usd": float(sum(pnl_seq)),
        "primary_expectancy_usd": float(np.mean(pnl_seq)) if trades else None,
        "stress_net_pnl_usd": float(sum(float(r["stress_net_pnl_usd"]) for r in trades)),
        "stress_expectancy_usd": float(np.mean([r["stress_net_pnl_usd"] for r in trades])) if trades else None,
        "profit_factor": float(pf) if pf is not None else None,
        "max_drawdown_usd": max_drawdown(pnl_seq),
        "longest_losing_trade_run": longest_run([x < 0 for x in pnl_seq]),
        "market_pnl_usd": {k: float(v) for k,v in sorted(market_pnl.items())},
        "market_trade_count": dict(sorted(market_trades.items())),
        "largest_market_abs_pnl_share": float(largest_abs_share),
        "eligible_weekdays": len(eligible_days),
        "zero_trade_days": int(sum(d not in daily for d in eligible_days)),
        "mean_daily_pnl_usd": float(np.mean(daily_values)),
        "median_daily_pnl_usd": float(np.median(daily_values)),
        "pct_days_le_50": float(np.mean(np.asarray(daily_values) <= 50.0)),
        "pct_days_ge_100": float(np.mean(np.asarray(daily_values) >= 100.0)),
        "pct_days_ge_150": float(np.mean(np.asarray(daily_values) >= 150.0)),
        "pct_days_ge_200": float(np.mean(np.asarray(daily_values) >= 200.0)),
        "losing_day_pct": float(np.mean(np.asarray(daily_values) < 0.0)),
        "longest_losing_day_run": longest_run([x < 0 for x in daily_values]),
        "trade_examples": [
            {
                "entry_ts": str(r["entry_ts"]),
                "exit_ts": str(r["exit_ts"]),
                "symbol": r["symbol"],
                "direction": r["direction"],
                "rung": r["rung"],
                "p": r["calibrated_probability"],
                "p_required": r["required_probability"],
                "outcome": r["outcome"],
                "primary_net_pnl_usd": r["primary_net_pnl_usd"],
            }
            for r in trades[:20]
        ],
    }


def counts_by_market(rows: list[dict]) -> dict:
    out = {}
    for symbol in EXECUTION_MARKETS:
        rr = [r for r in rows if r["symbol"] == symbol]
        states = {(r["decision_ts"], r["direction"]) for r in rr}
        out[symbol] = {
            "labeled_rungs": len(rr),
            "unique_economically_admissible_states": len(states),
            "target_hit_rate_by_rung": {
                rung: (
                    float(np.mean([r["label"] for r in rr if r["rung"] == rung]))
                    if any(r["rung"] == rung for r in rr) else None
                )
                for rung in RUNG_ORDER
            },
        }
    return out


def v02_runner_self_tests() -> list[str]:
    passed=[]
    e=candidate_economics_v02("EURUSD",1.10000,1.09900)
    assert abs(e["T30"]["distance"]-0.00150)<1e-12
    assert abs(e["T40"]["distance"]-0.00200)<1e-12
    assert abs(e["T50"]["distance"]-0.00250)<1e-12
    assert all(x["gross_target_usd_actual"]<=x["target_usd_nominal"]+1e-9 for x in e.values())
    passed.append("v02_target_before_size_exact")
    assert SEALED_START.isoformat()=="2026-07-01T00:00:00+00:00"
    passed.append("july_seal_constant")
    return passed


def main():
    preflight_path = OUT / "EXP-023-preflight-v0.2.json"
    if not preflight_path.exists():
        raise RuntimeError("authoritative cleanup preflight result missing")
    preflight = json.loads(preflight_path.read_text())
    if not preflight.get("preflight_pass"):
        raise RuntimeError("EXP-023 v0.2 preflight did not pass")
    if preflight.get("target_outcomes_calculated") or preflight.get("model_outcomes_calculated"):
        raise RuntimeError("preflight state is not zero-outcome")
    if preflight.get("secondary_test_loaded_or_inspected") or preflight.get("final_holdout_loaded_or_inspected"):
        raise RuntimeError("protected-period preflight seal failed")
    if not all(preflight.get("preflight_gate_ge_200_admissible_states_each",{}).values()):
        raise RuntimeError("per-market v0.2 economic coverage gate failed")
    integrity_tests={"v01_infrastructure":engine_self_tests(),"v02_economics":self_tests_v02()}
    label_tests=label_self_tests()+v02_runner_self_tests()

    data = {}
    for symbol in EXECUTION_MARKETS:
        path = download_pinned(symbol, CACHE)
        data[symbol] = load_scoped_csv(path, symbol)
        if data[symbol]["datetime"].max() >= SEALED_START:
            raise RuntimeError(f"{symbol}: parsed sealed timestamp")

    all_rows = []
    for symbol in EXECUTION_MARKETS:
        uj = data["USDJPY"] if symbol == "EURJPY" else None
        rows = build_labeled_rows(symbol, data[symbol], uj)
        all_rows.extend(rows)

    if not all_rows:
        raise RuntimeError("no labeled rows")
    if any(r["decision_ts"] >= SEALED_START for r in all_rows):
        raise RuntimeError("secondary-test row leaked into training/calibration")

    train_rows = [r for r in all_rows if r["period"] == "train"]
    cal_rows = [r for r in all_rows if r["period"] == "calibration"]

    models = {}
    rung_metrics = {}
    for rung in RUNG_ORDER:
        tr = [r for r in train_rows if r["rung"] == rung]
        ca = [r for r in cal_rows if r["rung"] == rung]
        fitted, preds = fit_rung_model(tr, ca)
        models[rung] = fitted["bundle"]
        rung_metrics[rung] = fitted["metrics"]
        annotate_probabilities(tr, preds["train"])
        annotate_probabilities(ca, preds["calibration"])

    market_counts_combined = counts_by_market(all_rows)
    market_counts_train = counts_by_market(train_rows)
    market_counts_cal = counts_by_market(cal_rows)

    combined_simulation=simulate_one_open(train_rows+cal_rows,TRAIN_START,SEALED_START)
    june_simulation=simulate_one_open(cal_rows,CAL_START,SEALED_START)
    coverage_pass=all(market_counts_combined[s]["unique_economically_admissible_states"]>=200 for s in EXECUTION_MARKETS)
    gate={
        "market_state_coverage_ge_200_each":coverage_pass,
        "combined_qualified_one_open_trades_ge_100":combined_simulation["actual_trades"]>=100,
        "june_qualified_one_open_trades_ge_20":june_simulation["actual_trades"]>=20,
        "june_target_hit_rate_above_mean_break_even":bool(june_simulation["actual_trades"]>0 and june_simulation["target_hit_rate"]>june_simulation["mean_break_even_probability"]),
        "june_primary_expectancy_gt_0":bool(june_simulation["primary_expectancy_usd"] is not None and june_simulation["primary_expectancy_usd"]>0),
        "june_primary_profit_factor_ge_1_10":bool(june_simulation["profit_factor"] is not None and june_simulation["profit_factor"]>=1.10),
        "june_max_drawdown_le_100":june_simulation["max_drawdown_usd"]<=100.0,
        "causality_same_bar_provenance_integrity":True,
        "market_contribution_reported_no_silent_drop":set(market_counts_combined)==set(EXECUTION_MARKETS),
        "secondary_and_final_holdout_sealed":True,
    }
    gate["final_pre_secondary_gate"]=bool(all(gate.values()))

    result = {
        "experiment": "EXP-023",
        "engine": "Engine K v0.2",
        "stage": "training_plus_june_calibration_only",
        "tested_repository_sha": repo_sha(),
        "engine_v01_infrastructure_sha256":sha256_file(ROOT/"research/code/engine_k_v0_1.py"),
        "engine_v02_economics_sha256":sha256_file(ROOT/"research/code/engine_k_v0_2.py"),
        "runner_sha256": sha256_file(Path(__file__)),
        "sklearn_version": sklearn.__version__,
        "scope": {
            "training": ["2026-03-23", "2026-05-31"],
            "calibration": ["2026-06-01", "2026-06-30"],
            "secondary_test_loaded_or_labeled": False,
            "final_holdout_loaded_or_labeled": False,
            "parsed_market_data_max_timestamp": max(str(df["datetime"].max()) for df in data.values()),
            "forecast_only_markets_loaded": False,
        },
        "frozen_model": {
            "hist_gradient_boosting": HGB_PARAMS,
            "platt": PLATT_PARAMS,
            "diagnostic_logistic": BASELINE_PARAMS,
            "encoded_feature_columns": ENCODED_FEATURE_COLUMNS,
        },
        "integrity_tests": integrity_tests,
        "label_tests": label_tests,
        "counts": {
            "combined_labeled_rungs": len(all_rows),
            "training_labeled_rungs": len(train_rows),
            "calibration_labeled_rungs": len(cal_rows),
            "by_market_combined": market_counts_combined,
            "by_market_training": market_counts_train,
            "by_market_calibration": market_counts_cal,
        },
        "rung_metrics": rung_metrics,
        "one_open_combined_training_calibration_simulation": combined_simulation,
        "one_open_june_calibration_simulation": june_simulation,
        "pre_secondary_gate": gate,
        "disposition": (
            "PASS_TO_SECONDARY_CHECKPOINT_READY"
            if gate["final_pre_secondary_gate"]
            else "FAIL_OR_INSUFFICIENT_STOP_BEFORE_SECONDARY"
        ),
    }

    bundle = {
        "experiment": "EXP-023",
        "engine": "Engine K v0.2",
        "tested_repository_sha": result["tested_repository_sha"],
        "engine_v01_infrastructure_sha256":result["engine_v01_infrastructure_sha256"],
        "engine_v02_economics_sha256":result["engine_v02_economics_sha256"],
        "runner_sha256": result["runner_sha256"],
        "sklearn_version": sklearn.__version__,
        "encoded_feature_columns": ENCODED_FEATURE_COLUMNS,
        "models": models,
        "hgb_params": HGB_PARAMS,
        "platt_params": PLATT_PARAMS,
        "baseline_params": BASELINE_PARAMS,
    }

    summary_path = OUT / "EXP-023-training-calibration-summary-v0.2.json"
    model_path = OUT / "EXP-023-model-bundle-v0.2.joblib"
    summary_path.write_text(json.dumps(result, indent=2, default=str) + "\n")
    joblib.dump(bundle, model_path, compress=3)

    print(json.dumps({
        "stage": result["stage"],
        "combined_labeled_rungs": len(all_rows),
        "combined_actual_trades":combined_simulation["actual_trades"],
        "june_actual_trades":june_simulation["actual_trades"],
        "june_primary_expectancy_usd":june_simulation["primary_expectancy_usd"],
        "june_profit_factor":june_simulation["profit_factor"],
        "june_max_drawdown_usd":june_simulation["max_drawdown_usd"],
        "june_target_hit_rate":june_simulation["target_hit_rate"],
        "june_mean_break_even_probability":june_simulation["mean_break_even_probability"],
        "gate":gate,
        "disposition": result["disposition"],
        "secondary_test_loaded_or_labeled": False,
        "final_holdout_loaded_or_labeled": False,
    }, indent=2))
    print(f"WROTE {summary_path}")
    print(f"WROTE {model_path}")


if __name__ == "__main__":
    main()
