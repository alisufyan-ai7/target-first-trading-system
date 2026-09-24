#!/usr/bin/env python3
"""Engine N v0.2 — rolling intraday drive-pullback scanner.

Reuses Engine N v0.1 drive qualification and pullback execution, changing only
the prospectively frozen anchor schedule.
"""

from __future__ import annotations

from engine_n_v0_1 import (
    DRIVE_MINUTES,
    SESSION_HORIZON_MINUTES,
    ORDER_ACTIVE_M1_BARS,
    session_anchor,
    session_setup,
    find_session_pullback_fill,
    self_tests_engine_n_v01,
)

ROLLING_ANCHORS=tuple((hour,0,f"H{hour:02d}") for hour in range(6,18))


def self_tests_engine_n_v02()->list[str]:
    tests=[]
    assert len(ROLLING_ANCHORS)==12
    assert ROLLING_ANCHORS[0][:2]==(6,0)
    assert ROLLING_ANCHORS[-1][:2]==(17,0)
    tests.append("twelve_hourly_anchors_06_to_17")

    # decision = anchor+30m, horizon = anchor+90m; next anchor decision is
    # exactly one hour later -> equal to prior horizon.
    assert SESSION_HORIZON_MINUTES-DRIVE_MINUTES==60
    tests.append("adjacent_anchor_nonoverlap")

    assert ORDER_ACTIVE_M1_BARS==45
    tests.append("unchanged_pullback_order_life")

    tests.extend([f"v01:{x}" for x in self_tests_engine_n_v01()])
    return tests
