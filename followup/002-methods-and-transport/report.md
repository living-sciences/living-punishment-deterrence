The paper's recidivism headline has not been re-estimated on post-2007 or non-Washington data. No public data allows it; requests are pending (listed in Limitations).

**METHOD.** Same public Washington 1999–2007 data and the same thresholds as the paper, re-estimated with current RD inference (a methods re-analysis, not new data on recidivism), plus a check of the design's no-sorting assumption on Florida 2021–2026 breath tests.

---

# Follow-up study 001 — methods re-analysis & transport check
### Hansen (2015), "Punishment and Deterrence: Evidence from Drunk Driving"

*Launch scope executed: Study A only (methods-and-transport). Branch **N** (`DO-FILES: NOT OBTAINED`) — the openICPSR 112907 do-files were not staged, so the 0.15 treatment coding is reported under both the statutory (≥ 0.150) and strict (> 0.150) definitions as a pre-registered pair of equal standing. Run directory is numbered `002` but the task is the methods-and-transport study.*

## Question

Two questions, no update of the recidivism result itself (no public data allows that):
- **A (methods re-analysis, same WA data):** how do the paper's two threshold estimates read under 2026 RD inference — data-driven MSE-optimal bandwidths with robust bias-corrected (RBC) CIs (Calonico–Cattaneo–Titiunik/Farrell), honest CIs for a discrete running variable (Kolesár–Rothe; Armstrong–Kolesár via `RDHonest`), and `rddensity` — and how fragile is the 0.15 estimate to the coding of the single 0.150 mass point?
- **B (transport check, new state/decade):** does the design's identifying assumption (no sorting of BAC at 0.08 and 0.15; a smooth predetermined covariate) hold in Florida's 2021–2026 FDLE Intoxilyzer-8000 breath-test records, under the same legal structure (Fla. Stat. §316.193)? This tests identification only, not recidivism.

## Approach

**Reused from the replication (read-only):** the public analysis file `hansen_dwi.dta` (sha256 `08158875…ecd1`, verified), the built RD dataset `outputs/rd_data.rds`, and the paper-era specification in `table3_dui_rd.R` / `table4_aggdui_rd.R` / `density_tests.R`. Original comparison values are read from `replication/codebase/outputs/{table3,table4,table2,density_tests,baseline}.json`.

**Added:** R `rdrobust` 4.0.0 (RBC), `rddensity` 3.0, `RDHonest` 1.0.2 (installed from CRAN); a privacy-first Florida STED ingest in Python (`pdftotext -layout`, de-identified parquet). `masspoints="adjust"` throughout. Validation gates 1 (anchor, ±0.0005) and 2 (bin means) pass exactly before any estimate.

### Panel A — Washington (headline = A1 RBC and A2 honest, co-equal; A0 = paper method on the same file)

| Threshold / coding | A0 paper-method bw 0.05 | A1 RBC (MSE-opt h) | RBC 95% CI | A2 honest (M) | Honest 95% CI | Verdict |
|---|---|---|---|---|---|---|
| 0.08 statutory ≥ | −0.0221 (0.0041) | −0.0173 (0.0059), h=0.028 | **[−0.0307, −0.0023]** excl. 0 | −0.0150 (M=120) | [−0.0310, 0.0010] incl. 0 | bandwidth-dependent, stable |
| 0.15 statutory ≥ | −0.0073 (0.0035) | −0.0074 (0.0048), h=0.029 | [−0.0185, 0.0043] incl. 0 | −0.0063 (M=86) | [−0.0193, 0.0068] incl. 0 | bandwidth-dependent, stable |
| 0.15 strict > | −0.0090 (0.0034) | −0.0112 (0.0047), h=0.030 | **[−0.0228, −0.0007]** excl. 0 | −0.0120 (M=83) | [−0.0250, 0.0009] incl. 0 | bandwidth-dependent, stable |

Mass points inside h: 27/28 (0.08), 28/29 and 30/30 (0.15). Paper values: 0.08 −0.021; 0.15 −0.010. Full templated statements (with 2M sensitivity and CI widths) are in `results/findings.md`; row-level numbers in `results/estimates_headline.csv`.

- **No threshold clears "confirmed/robust"** (which needs *both* the RBC and honest CI to exclude zero) and **none triggers "does not survive"** (which also needs an A3 sign change — the point estimate stays negative across the whole h-grid 0.010–0.068). Every case is **bandwidth-dependent** with a point estimate **stable** (within ±25% of the paper-method estimate on the same file; ratios −22%, +2%, +25%).
- **The 0.15 estimate is coding-sensitive**, which is the study's central methods point: under the strict (> 0.150) coding the RBC CI excludes zero at the MSE-optimal h (and for h ≥ 0.034); under the statutory (≥ 0.150) coding it includes zero at *every* bandwidth. The honest CI includes zero in all three cases — driven by intervals ≈1.8–2.2× wider than the paper's bin-clustered SEs (which Kolesár–Rothe 2018 show are invalid for a discrete running variable), not by any movement of the point estimate.
- **Bandwidth curve** (`fig_bandwidth_curve.png`, `bandwidth_curve.csv`): conventional estimate and RBC band vs h, with the paper's two points overlaid.
- **Manipulation (A6):** modern `rddensity` p = 0.144 (0.08), 0.158 (0.15) — no sorting, consistent with the paper. Discrete binomial tests (k=1,2,5,10) all p > 0.36. The replication's McCrary `DCdensity` over-rejects (p≈0) on this discrete, strongly-curved 214k-row subset — a local-linear density-fit artifact, not evidence of manipulation (`_density_WA.json`, `fig_density_WA_*.png`).
- **Covariate balance (A7, A1 estimator):** male/white/age/accident RBC CIs all include zero at both thresholds (`balance_A1.csv`).
- **Eras (A5):** negative across 1999–2007, no significant era difference (`eras.csv`, `fig_eras.png`).

### Panel B — Florida 2021–2026 (transport check only)

Ingested **all 535** monthly FDLE STED PDFs (2021-01→2026-07): **165,162** subject tests (one record per page, zero download/parse failures), of which **116,934** are two-sample DUI tests (the analysis sample). Per-year counts ~29–30k (2026 partial), matching FDLE's 2022 figure (30,182). Privacy: subject/operator/officer names dropped in memory, never written; raw serial/agency/day/time not kept; per-batch whole-word name assertion = 0 Florida-derived hits; final schema check = no name-bearing column. Two-extractor audit (`-layout` vs `-raw`, 30 pages/yr): BrAC-multiset, gender, flag agreement = 100% every year (`florida_parse_audit.json`).

| Metric (pooled) | 0.08 | 0.15 |
|---|---|---|
| FL rddensity no-sorting p | 0.605 | 0.415 |
| WA rddensity p (same test) | 0.144 | 0.158 |
| FL log-density jump | −0.036 | −0.036 |
| FL MDD (80% power) | 0.196 | 0.123 |
| WA MDD | 0.100 | 0.083 |
| FL MDD > 2× WA MDD? | No (vs 0.199) | No (vs 0.167) |
| FL cutoff-bin share / neighbor mean | 1.03 | 1.03 |
| FL gender balance (A1) coef (p) | +0.013 (0.56) | +0.006 (0.40) |

- **No sorting** at either threshold (rddensity p = 0.61 / 0.42; discrete binomial k=1..10 all p > 0.6). **Gender balanced.** **Adequately powered** (FL MDD not > 2× WA at either threshold; 0.08 borderline).
- **Heaping, reported next to the density result:** no excess mass at the exact cutoff bins 0.080/0.150 (ratio 1.03), but readings heap on round thousandths (last digit = 0 in ~21% of samples vs 10% uniform, χ² p≈0, also per-instrument). Because the thresholds are round values this matters for a *future* Florida RD; the no-sorting conclusion is robust to it — donut re-runs give rddensity p = 0.65/0.39 (drop cutoff bin) and 0.32/0.22 (drop all round bins). (`florida_heaping_shares.csv`, `florida_lastdigit*.csv`, `florida_density_donut.csv`.)
- **Transport verdict (per pre-declared B-pre):** no sorting + adequate power ⟹ *a Florida recidivism RD (pending the person-ID records gate) is feasible on identification grounds*, with the caveat that a donut/heaping-robust specification would be needed. **Neither outcome bears on the validity of Hansen's Washington estimates.**

Figures: `fig_florida_hist.png`, `fig_florida_refusal.png`, `fig_fl_vs_wa_density.png`.

## Results — comparison to the replication/paper

| Quantity | Original (source) | This study | Note |
|---|---|---|---|
| 0.08, bw 0.05, controls | −0.0221 (0.0041) `table3.json` | −0.0221 (0.0041) | anchor reproduced exactly (gate 1) |
| 0.08 under 2026 inference | paper −0.021***; A0 −0.0221 | A1 −0.0173, RBC CI excl. 0; A2 honest incl. 0 | significance bandwidth-dependent; estimate stable |
| 0.15, bw 0.05, controls | −0.0073 (0.0035) `table4.json` | −0.0073 (0.0035) | anchor reproduced exactly |
| 0.15 under 2026 inference | paper −0.010***; A0 −0.0073/−0.0090 | statutory: both CIs incl. 0; strict: RBC excl. 0, honest incl. 0 | coding-sensitive; estimate stable |
| WA manipulation p | McCrary 0.59/0.38 (paper); `DCdensity` ≈0 (repl) | rddensity 0.144/0.158 | modern test agrees with paper, not with repl's McCrary |
| FL identification (new) | — | no sorting (p 0.61/0.42), balanced, powered | design transports (caveat: round-value heaping) |

## Deviations & limitations

- **The recidivism headline is not re-estimated on any new data** — no public person-linked recidivism microdata exists beyond the 1999–2007 Washington extract. Pending human gates (records requests): Utah GRAMA (0.05 RD), WSP RCW 42.56 (WA post-2007), Florida dispositions + person ID + ethics, FDLE STED 2014–2020, Arkansas OAT FOIA, MN/TX/MI.
- **Branch N:** the 0.15 coding is unresolved (do-files not obtained); both codings carry equal standing.
- **Absent public variables:** prior-test splits, PBT, recidivism-type/time-window/other-crime outcomes, county FE, court sanctions, border/interior. WA regressions omit county + prior-offense controls (paper App. Tables 1/2 report ~equivalent results without them); the subset is 214,558 of the paper's 512,964 tests.
- **Florida:** no person linkage, no recidivism outcome (out of scope / ethics-gated). The running variable heaps on round BAC values at the thresholds — a future RD needs donut/heaping-robust methods.
- **Honest-CI implementation:** `RDHonest` installed from CRAN; its default Hölder-class rule-of-thumb M (Armstrong–Kolesár) is used, with 2M reported as sensitivity.
- The `notes/2026-09-09-followup-studies-handoff.md` contract file referenced by the spec is not present in this run directory; deliverables follow the schemas in the instruction and the `result-presentation` skill.
- Part II (002 theory-update) was **not** executed, per the binding launch-scope line.

*Artifacts: all CSV/JSON/PNG under `results/`; de-identified data + dictionary under `workspace/data/` (`fl_tests_deid.parquet`, `fl_manifest.csv`, `DATA_DICTIONARY.json`).*
