# Evidence Matrix — Badar Current-Era Decision Model v0.1

This matrix records why each decision-model component exists. It is a source-evidence map, **not a profitability table**.

## Core decision components

| Component | Current-era evidence examples | What the evidence shows | v0.1 status |
|---|---|---|---|
| HTF direction / H1 anchor | `dOdvKLaBPaA`, `1E65DgTFxe0`, `WUblCihXgPU`, `EOBnMz2Y_9k` | H1/HTF defines direction, areas and whether a countertrend idea deserves reduced risk; Sep 30 bias changes after H1 close | CORE |
| Meaningful location required | `dOdvKLaBPaA`, `05t_eyqXfUU`, `mGJ4dtVjlxE`, `wQ5uxbmLlM4`, `WUblCihXgPU`, `1E65DgTFxe0` | Mid-range confirmation is ignored; wait for high/low, POI, retracement or liquidity area | CORE |
| No trade in the middle | `mGJ4dtVjlxE`, `wQ5uxbmLlM4`, `WUblCihXgPU` | Explicit middle/center/no-area rejections | CORE |
| Liquidity sweep / trap | `dOdvKLaBPaA`, `TYY0aNKVnZ8`, `2H9oOTKFGXA`, `WUblCihXgPU`, `CPGcMydNbbQ` | Common reversal context, strongest when sweep occurs into HTF POI | STRONG |
| Sweep not universal | continuation/retrace live entries including `mGJ4dtVjlxE`, `C18mm9p2oW4` | Some trades use continuation OB/FVG retracement without textbook sweep | COUNTEREVIDENCE TO HARD GATE |
| Candle closes matter | `kHYijXUkYWY`, `6GI6xuasKjo`, `dOdvKLaBPaA`, recent live streams | Distinguishes wicks/transient breaks from accepted closes; repeatedly waits for M15/M30/H1 | CORE |
| HTF close can change case | `1E65DgTFxe0`, `CPGcMydNbbQ`, `EOBnMz2Y_9k` | Higher-TF close can confirm, invalidate or flip the intraday plan | CORE |
| LTF execution after HTF gate | `TYY0aNKVnZ8`, `WUblCihXgPU`, `CPGcMydNbbQ`, `EOBnMz2Y_9k` | M1/M3/M5 used for precision after larger context; M1 common live despite older teaching caution | CORE CURRENT BEHAVIOR |
| Inverse closing | `05t_eyqXfUU`, `tveHWYC0l8o`, `2H9oOTKFGXA`, recent streams | Trap/fake break then close back is recurring trigger | STRONG |
| Two-candle rejection | `dOdvKLaBPaA`, `VOGDGiwGLjM`, `2H9oOTKFGXA` | Repeated rejection/close from a zone is recurring confirmation family | STRONG |
| Momentum/MSS | `dOdvKLaBPaA`, `TYY0aNKVnZ8`, `1E65DgTFxe0` | Strong confirmation after liquidity interaction; exact TF differs | STRONG |
| Same-zone second confirmation | `2H9oOTKFGXA`, `OEetzalNqSY`, `dOdvKLaBPaA` | Weak/failed first confirmation followed by second at same zone can upgrade setup | STRONG |
| Do not chase | `aEw6393GE1c`, `suuicaoUvDQ`, `wQ5uxbmLlM4`, `MbUagftbsIw`, `CPGcMydNbbQ` | Missed move is allowed to go; wait for next retracement/setup | CORE |
| Logical stop required | `9D7wgJCdP5c`, `CKTqdFza1HE`, `KsWpzeJhAVk`, `CPGcMydNbbQ` | Trades skipped when stop placement unclear/too large; outer structure often defines invalidation | CORE |
| Lower quality -> lower risk | `HOidQitTyAc`, `HwXIifB0P6o`, `WUblCihXgPU`, `EOBnMz2Y_9k` | Countertrend, weak/low-probability, news or large-stop trades often reduced | CORE |
| Active early invalidation | `CPGcMydNbbQ`, `qTSedn6hEp8`, `CKTqdFza1HE` and many live streams | Manually exits/reduces when later closes show premise is wrong | CORE |
| Partials + runner | `tveHWYC0l8o`, `1E65DgTFxe0`, `CPGcMydNbbQ` | TP1/partials + runner toward structural liquidity recur; exact management varies | STRONG |
| Environment/news modifies behavior | `ZPhq3RcGHz0`, FOMC/NFP streams, `EOBnMz2Y_9k` | News/month-end/session state changes risk/waiting, but is not universal skip | VARIABLE |

## Recent live decision traces used as anchors

### 2026-09-25 — `1E65DgTFxe0`

Accepted hierarchy:

```text
H1 bearish / premium area
-> high/equal-high liquidity taken
-> H1 close
-> M1 reversal execution
-> structural stop
-> partial / liquidity target
```

Rejected/wait logic:
- do not sell after market already extended down;
- wait for retracement into FVG/sell area;
- not every hidden OB is tradable;
- structure must support the OB;
- stop after completed Friday opportunity.

### 2026-09-28 — `WUblCihXgPU`

Accepted:
- countertrend scalp from lower area at reduced risk;
- lower sweep + M1 close enables re-entry;
- later with-trend sell from premium/supply after buy-trap;
- M5/H1 close adds sell confirmation.

Rejected:
- do not sell at low after extended decline;
- middle = no sell area / no buy area;
- do not sell directly without another sweep/confirmation;
- do not add another trade merely because requested.

### 2026-09-29 — `CPGcMydNbbQ`

Accepted:
- repeated selling from intraday highs/sweeps;
- SL beyond outer high;
- reduce risk when M5 confirmation fails;
- re-entry if structure recreates setup.

Rejected:
- large M1 candle at level causes wait for another close;
- no chase after missed retest;
- no buy at top despite broader bullish context;
- wickless/high-volume push against sell premise triggers exit.

### 2026-09-30 — `EOBnMz2Y_9k`

Newest evidence in v0.1.

Accepted:

```text
H1 close changes active bias
-> retracement into H1 gap / M15 hidden OB
-> main short
-> M1 fake-buy / sell-close confirmation
-> smaller second entry with tighter stop
```

Rejected/wait:
- pre-session buy idea waits for zone sweep + M1 bullish sign;
- potential high-sweep sell never occurs, so no trade;
- no buy from low when he believes retail is already buying there;
- waits on H1/M30/M15 closes;
- trend-conflicting buy is lower risk;
- month-end increases caution.

## Contradiction matrix

| Topic | Source conflict | v0.1 treatment |
|---|---|---|
| MSS timeframe | older course says M1 unreliable; recent live execution often M1 | Preserve HTF-context/LTF-execution hierarchy; no fixed MSS TF |
| 2CR timeframe | older source prefers 15m+; live includes lower-TF rejections | No fixed TF |
| BOS validity | 2 closes vs pip thresholds vs proportional rules | Close-based structure confirmation only |
| ICC threshold | 30%, 30–40%, 50–60%, >50% | Preserve close-back concept; no percentage |
| Session preference | London best / London+NY / NY only / Asian+NY | Session is context, not hard direction |
| News | avoid/gambling vs actual news trades | Event-risk modifier; no universal ban in Badar model |
| Risk % | multiple percentages | Quality-based risk class only; Target-First sets its own risk |
| SL widening | taught never widen; several live widenings | Unresolved; do not encode |
| RR | 1:2, 1:3, 1:6–1:10 and live 1:1 risk trades | Structural target + quality classification; no single RR |
| Trades/day | 1–2/max 3 vs live 3–5+ on some days | No fixed Badar count |

## Interpretation

The contradictions suggest that any transferable edge is more likely to reside in the **higher-order decision hierarchy** than in exact constants copied from one lesson.
