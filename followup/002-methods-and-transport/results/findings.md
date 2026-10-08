The paper's recidivism headline has not been re-estimated on post-2007 or non-Washington data. No public data allows it; requests are pending (listed in Limitations).

**METHOD.** Same public Washington 1999–2007 data and the same thresholds as the paper, re-estimated with current RD inference (a methods re-analysis, not new data on recidivism), plus a check of the design's no-sorting assumption on Florida 2021–2026 breath tests.

**Branch:** `DO-FILES: NOT OBTAINED`. Coding unresolved; do-files not obtained. At 0.15 the statutory (≥ 0.150) and strict (> 0.150) codings are reported as a pre-registered pair of equal standing; neither is promoted.

## B-pre (pre-declared Florida reading, written before any Florida estimate)
- If sorting is found at 0.08 or 0.15 in Florida, it means "the design does not transport to Florida 2021–2026 as is".
- If no sorting is found **and** the test has the stated power, it means "a Florida recidivism RD (pending the person-ID records gate) is feasible on identification grounds".
- If no sorting is found but the test is underpowered by the B1 rule, it means "no sorting was detected, but the Florida test cannot rule out discontinuities of the size [MDD]", and nothing stronger.
- **Neither outcome bears on the validity of Hansen's Washington estimates.**

## Panel A — Washington methods re-analysis (headline: A1 RBC + A2 honest, co-equal)

Gate 1 (anchor) passes exactly: A0 at 0.08, bw 0.05, with controls = −0.0221 (SE 0.0041), N = 93,899; at 0.15 = −0.0073 (SE 0.0035), N = 139,033 (`replication/.../table3.json`, `table4.json`). Gate 2 (means) passes: recidivism mean at L=79 = 0.1043, at L=149 = 0.1241.

### 0.08 threshold
At 0.08, coding: statutory ≥: point estimate **-0.0173** (SE 0.0059) at the MSE-optimal h = 0.0278 (27 / 28 mass points, N 16,201 / 37,364), against the paper's -0.021 and -0.0221 by the paper's method on the same public file. The sign is negative at every bandwidth in [0.010, 0.068]. The RBC 95% CI is **[-0.0307, -0.0023]** and excludes zero at the MSE-optimal h; across the A3 grid it excludes zero for h ≥ 0.038 and includes it below. The honest (Armstrong–Kolesár) 95% CI is **[-0.0310, 0.0010]** at M = 120.1 and [-0.0323, 0.0044] at 2M. CI widths: RBC 0.0284, honest 0.0320, against 0.0157 = 2 × 1.96 × the paper's SE.

> **Verdict:** Significance is bandwidth-dependent under 2026 inference; the point estimate is stable (within ±25% of the A0 same-file estimate; ratio -22.1%). The interval includes zero because it is honest 2.04× wider than the paper's, not because the estimate moved.

### 0.15 threshold — statutory ≥ coding
At 0.15, coding: statutory ≥: point estimate **-0.0074** (SE 0.0048) at the MSE-optimal h = 0.0288 (28 / 29 mass points, N 45,138 / 39,087), against the paper's -0.01 and -0.0073 by the paper's method on the same public file. The sign is negative at every bandwidth in [0.010, 0.068]. The RBC 95% CI is **[-0.0185, 0.0043]** and includes zero at the MSE-optimal h; across the A3 grid it includes zero at every h in the grid (excludes at no h). The honest (Armstrong–Kolesár) 95% CI is **[-0.0193, 0.0068]** at M = 86.1 and [-0.0189, 0.0113] at 2M. CI widths: RBC 0.0227, honest 0.0262, against 0.0118 = 2 × 1.96 × the paper's SE.

> **Verdict:** Significance is bandwidth-dependent under 2026 inference; the point estimate is stable (within ±25% of the A0 same-file estimate; ratio +1.5%). The interval includes zero because it is RBC 1.93× and honest 2.22× wider than the paper's, not because the estimate moved.

### 0.15 threshold — strict > coding
At 0.15, coding: strict >: point estimate **-0.0112** (SE 0.0047) at the MSE-optimal h = 0.0304 (30 / 30 mass points, N 48,284 / 39,786), against the paper's -0.01 and -0.0090 by the paper's method on the same public file. The sign is negative at every bandwidth in [0.010, 0.068]. The RBC 95% CI is **[-0.0228, -0.0007]** and excludes zero at the MSE-optimal h; across the A3 grid it excludes zero for h ≥ 0.034 and includes it below. The honest (Armstrong–Kolesár) 95% CI is **[-0.0250, 0.0009]** at M = 83.4 and [-0.0261, 0.0038] at 2M. CI widths: RBC 0.0221, honest 0.0259, against 0.0118 = 2 × 1.96 × the paper's SE.

> **Verdict:** Significance is bandwidth-dependent under 2026 inference; the point estimate is stable (within ±25% of the A0 same-file estimate; ratio +24.6%). The interval includes zero because it is honest 2.21× wider than the paper's, not because the estimate moved.

**Reading.** No threshold/coding clears the joint bar for "confirmed/robust" (both CIs excluding zero) and none triggers "does not survive" (which also requires an A3 sign change; estimates stay negative across the whole grid). All three are bandwidth-dependent with point estimates **stable** relative to the paper-method estimate on the same file. The 0.15 result is coding-sensitive: under the strict (> 0.150) coding the RBC CI excludes zero at the MSE-optimal h (and for h ≥ 0.034), while under the statutory (≥ 0.150) coding the RBC CI includes zero at every bandwidth. The honest CI includes zero in all three cases, driven by intervals ~1.8–2.2× wider than the paper's clustered SEs, not by movement of the point estimate.

Other Panel A results: covariate balance (A7, A1 estimator) — male/white/age/accident RBC CIs all include zero at both thresholds (`balance_A1.csv`). Manipulation (A6): rddensity p = 0.144 (0.08) and 0.158 (0.15); discrete binomial tests (k=1,2,5,10) all p > 0.36; both consistent with the paper's no-sorting conclusion and with the modern test, unlike the replication's McCrary `DCdensity` which over-rejects (p≈0) on this discrete, curved, 214k-row subset (a local-linear density-fit artifact; see `_density_WA.json`). Eras (A5): estimates are negative across 1999–2007 with no significant era difference (`eras.csv`).

## Panel B — Florida 2021–2026 transport check (identifying assumption only)

Ingested all 535 monthly FDLE Intoxilyzer-8000 STED PDFs (2021-01 to 2026-07), 165,162 subject tests, one record per page, zero download/parse failures; **116,934 two-sample DUI tests** form the analysis sample. All name fields were dropped in memory and never written to disk (per-batch whole-word name assertion: 0 Florida-derived hits; final schema check: no name/serial/agency/day/time column). Two-extractor structural audit (`-layout` vs `-raw`, 30 pages/yr): BrAC-multiset, gender and flag agreement = 100% in every year. Per-year test counts ~29–30k (2026 partial), matching FDLE's 2022 figure of 30,182.

**No sorting at either threshold.** rddensity (pooled): p = 0.605 at 0.08 and p = 0.415 at 0.15 (WA on the same test: 0.144 / 0.158). Discrete binomial tests (k=1,2,5,10) all p > 0.6. Gender (predetermined covariate) is balanced: A1 RBC coef +0.0128 (p 0.558) at 0.08 and +0.0063 (p 0.402) at 0.15.

**Power.** Minimum detectable discontinuity (80% power, 5% two-sided) for the log-density jump: FL 0.196 vs WA 0.100 at 0.08; FL 0.123 vs WA 0.083 at 0.15. The pre-declared underpowered rule (FL MDD > 2× WA MDD) is **not** triggered at either threshold (0.08 is borderline: FL 0.196 vs 2×WA 0.199). So the non-rejections are adequately powered.

**Heaping (reported next to the density result it could affect).** There is **no excess mass at the exact cutoff bins** 0.080/0.150 (cutoff-bin share / neighbor-mean ratio 1.03 at both, vs WA 0.97/1.00). But sample readings heap strongly on round thousandths: the last digit of samples 1 and 2 is 0 in ~21% of tests (uniform = 10%; χ² p≈0), present per-instrument as well. Because the thresholds 0.080/0.150 sit on round values, this matters for a future Florida RD; however the no-sorting conclusion is robust to it: re-running rddensity with the cutoff bin dropped (donut) gives p = 0.65 (0.08) / 0.39 (0.15), and dropping all round bins gives p = 0.32 / 0.22 — still no discontinuity.

**Transport verdict (per B-pre):** no sorting is found at 0.08 or 0.15 and the test is adequately powered → *a Florida recidivism RD (pending the person-ID records gate) is feasible on identification grounds*, with the caveat that the running variable heaps on round BAC values at the thresholds (a donut/heaping-robust specification would be required). **Neither outcome bears on the validity of Hansen's Washington estimates.**

## Limitations / pending data gates
- The recidivism headline itself is **not** re-estimated on any new data: no public person-linked recidivism microdata exists beyond Hansen's 1999–2007 Washington extract. Pending gates (records requests): Utah GRAMA (arrest-level BAC for a 0.05 RD), WSP RCW 42.56 (WA tests after 2007), Florida dispositions + person ID + ethics (FL recidivism RD), FDLE STED 2014–2020, Arkansas OAT FOIA, MN/TX/MI.
- Not reproducible from the public file (absent variables): prior-test splits, PBT, recidivism-type/time-window/other-crime outcomes, county FE, court sanctions, border/interior. Washington estimates therefore omit county + prior-offense controls (paper App. Tables 1/2 report ~equivalent results without them).
- 0.15 coding unresolved (do-files not obtained; Branch N): both codings reported with equal standing.
- No Florida person linkage and no Florida recidivism outcome (out of scope / ethics-gated).
- The `notes/2026-09-09-followup-studies-handoff.md` contract file referenced by the spec is not present in this run directory; deliverables follow the schemas given in the instruction and the result-presentation skill.