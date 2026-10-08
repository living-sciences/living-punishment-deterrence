# 004 — Gate-conformance corrective for the Hansen (2015) follow-ups
### Supersedes `002-methods-and-transport` and `003-theory-update`

## Question

The Phase-2d provenance audit (`gate-conformance-inputs/hansen-provenance.md`, authoritative) found the
two Hansen (2015) follow-ups sound in their Washington computation and privacy handling, but flagged: a
**data defect in the Florida ingest** (5 STED files ingested twice), a **misread of the heaping evidence**,
several **reporting-layer gate violations** in 002, and in 003 **one fabricated claim**, a sign model shown
differently from the one on disk, and a hard-coded prediction. This corrective rebuilds the Florida numbers
on deduplicated data, reports the honest versions of every flagged check, runs (rather than asserts) the one
fabricated claim, and publishes a single card superseding both. No new fetches; existing shards/outputs
reused; foreground only.

## Approach

- **Reused unchanged (read-only):** the Washington Panel A estimates (same `hansen_dwi.dta` / `rd_data.rds`;
  the audit verified the WA computation sound, so **nothing in Panel A was re-estimated**) from
  `002…/results/`; the 002 Florida parquet shards and manifest; the 003 literature/Utah CSVs; all Hansen
  codes and the sign model logic from `theory_update.py`.
- **Deduplication (no fetch):** the 537-href FDLE index has 532 unique URLs; 5 STED files were listed and
  ingested twice. The merged parquet maps 1:1 to manifest rows in processing order (verified: 100%
  `src_year_month` match, each file contributing `record_count` consecutive rows), so the 2nd occurrence of
  each repeated sha256 was dropped. `fl_tests_deid.parquet`, `fl_analysis.csv` and the manifest were rebuilt.
- **Recomputed on deduplicated data:** density/MDD/power, the by-year discrete test 002 omitted, gender
  balance, heaping (now excluding 0.000 readings), the round-value check, and all Florida figures (R
  `rddensity`/`rdrobust` in the 002 rlib; Python for the parse and figures).
- **003 corrections:** the T3-H prediction is now **computed from the sign model + T0 codes**; the
  pre-declared "uninformative" clause is evaluated; the sign model is presented exactly as persisted; the
  in-sample appendix is **actually run**; Finlay is annotated rather than plotted at 0%.

## Results

### 1. Washington recidivism RD under 2026 inference — the headline (UNCHANGED; full H2 template)

| Threshold / coding | A0 paper-method (bw 0.05) | A1 RBC (MSE-opt h) | RBC 95% CI | A2 honest (M) | Honest 95% CI | Verdict |
|---|---|---|---|---|---|---|
| 0.08 statutory ≥ | −0.0221 (0.0041) | −0.0173 (0.0059), h=0.028 | **[−0.0307, −0.0023]** excl. 0 | −0.0150 (M=120) | [−0.0310, 0.0010] incl. 0 | bw-dependent, stable (−22.1%) |
| 0.15 statutory ≥ | −0.0073 (0.0035) | −0.0074 (0.0048), h=0.029 | [−0.0185, 0.0043] incl. 0 | −0.0063 (M=86) | [−0.0193, 0.0068] incl. 0 | bw-dependent, stable (+1.5%) |
| 0.15 strict > | −0.0090 (0.0034) | −0.0112 (0.0047), h=0.030 | **[−0.0228, −0.0007]** excl. 0 | −0.0120 (M=83) | [−0.0250, 0.0009] incl. 0 | bw-dependent, stable (+24.6%) |

No case clears "confirmed/robust" (both CIs excluding zero); none triggers "does not survive" (estimate stays
negative across the whole h-grid). All three are **bandwidth-dependent with stable point estimates**; honest
CIs are ≈1.9–2.2× wider than the paper's bin-clustered SEs. **Bandwidth-significance ranges are triangular-
kernel** (0.08: RBC excludes zero for h ≥ 0.038; 0.15 statutory: at no h; 0.15 strict: h ≥ 0.034). **Under the
rectangular kernel** the picture differs: **0.15 statutory RBC excludes zero for h ≥ 0.060** (so "includes at
every h" is a triangular-only claim), 0.15 strict is non-monotone, and 0.08 excludes for h ≥ 0.026 (gap at
0.030). *b=h note:* the A3 grid fixes the bias bandwidth b = h, whereas the MSE-optimal fit uses b = 0.043 —
which is why the RBC CI can exclude zero at the MSE-optimal h (0.028) yet include it below 0.038 across the
grid. **Coding unresolved; do-files not obtained** (Branch N — both 0.15 codings equal standing).

- **A4 (surfaced):** at 0.08 the strict (> 0.080) coding gives A1 = −0.0111 (0.0063), **RBC CI [−0.0233,
  0.0063] includes zero**.
- **Eras (corrected):** negative across 1999–2007 **at 0.08 only**; at **0.15, 2001 = +0.004 and 2004 =
  +0.012** (positive). No significant era difference at either threshold.

Figure: `results/fig_bandwidth_curve.png` (A3 curve, both points overlaid — reused from 002, unchanged).

### 2. Florida 2021–2026 transport check — DEDUPLICATED

B-pre (the pre-declared reading) was **written after the Florida estimates** (002 step [128]) and so cannot
claim pre-declaration; it is restored with that sequencing stated, in full, in `results/findings.md`.

| Metric (pooled) | 0.08 | 0.15 | 002 value (superseded) |
|---|---|---|---|
| FL rddensity no-sorting p | **0.593** | **0.308** | 0.605 / 0.415 |
| WA rddensity p (same test) | 0.144 | 0.158 | 0.144 / 0.158 |
| FL MDD (80% power) | **0.1978** | **0.1234** | 0.196 / 0.123 |
| 2 × WA MDD | 0.1991 | 0.1668 | — |
| FL MDD > 2×WA? | No (by **0.0013**) | No | No |
| FL gender balance coef (p) | **+0.0104 (0.640)** | **+0.0065 (0.394)** | +0.0128 (0.558) / +0.0063 (0.402) |

- **No sorting** at either threshold (rddensity, pooled discrete k=1..10 all p > 0.50, **and the by-year
  discrete tests 002 omitted — all p > 0.18**). **Gender balanced** (both CIs include zero). **Adequately
  powered**, but the 0.08 margin to 2×WA is **razor-thin (0.0013)**.
- **Heaping (corrected):** no excess at the cutoff bins (ratio 1.05 / 1.02) **and no round-value excess**
  near the thresholds (0.070→0.93, 0.090→0.95, 0.100→0.995, 0.150→1.02). The earlier "~21% last-digit-0"
  was a **0.000-reading artifact** (12.08% of tests have sample1 = 0.000); **excluding zeros the digit-0
  share is 10.25%** (uniform). The round-value-heaping caveat is **retracted**; the all-round-bins donut is
  removed; the cutoff-bin donut leaves no discontinuity (p 0.640 / 0.268).
- **Structural audit (honest):** 002's "100% agreement" was **BrAC token-multiset** agreement, not fields;
  its field-level `-layout`/`-raw` comparison had failed at 0.000; the schema width was hard-coded; the
  raw-token smax 3.4–4.6 (outside BrAC [0,0.5]) went unremarked. A two-extractor re-parse is **impossible**
  (PDFs deleted at ingest; no fetch); the closest check — a per-field validity audit on 30 dedup pages/year —
  gives 100% per field except **n_valid_samples 99.44%**, with in-parquet readings all within [0, 0.478].
- **Verdict (per B-pre, deduplicated):** no sorting + adequate power ⟹ *a Florida recidivism RD (pending the
  person-ID records gate) is feasible on identification grounds*. **Neither outcome bears on the validity of
  Hansen's Washington estimates.**

Data: 530 unique files (535 downloads), **162,875 tests**, **115,262 two-sample DUI**. Figures:
`fig_florida_hist.png`, `fig_fl_vs_wa_density.png`.

### 3. Theory update — margin model (003 corrections)

The model fitted **without Hansen** predicts **deterrence** at both his thresholds (both map to the severity/
no-record class, majority **deter 7/12**), and classifies all three margins **consistent** with the 001
re-analysis — with one honest caveat at 0.15 statutory (below). The sign model is presented **exactly as
persisted**: record-change class **2/0/2 (ambiguous)**, Humphries in its own class, all 18 rows. The DUI/
general split the 002/003 card showed exists in no persisted output and dropped Humphries; it is reported
only as a **disclosed variant** (general-crime record = **0/0/3**, Humphries included).

| Hansen margin | model predicts | 001 A1 (rel) | 001 A1 CI | 001 A2 CI | classification |
|---|---|---|---|---|---|
| 0.08 | deter (−) | −16.6% | [−29.4, −2.2] | [−29.7, +0.9] | consistent |
| 0.15 statutory ≥ | deter (−) | −6.0% | [−14.9, +3.4] | [−15.6, +5.5] | consistent* |
| 0.15 strict > | deter (−) | −9.1% | [−18.4, −0.5] | [−20.2, +0.7] | consistent |

**\* 0.15 statutory:** the pre-declared "uninformative" clause (both 001 CIs include zero AND no clear class
majority) was evaluated. Both CIs **do** include zero, but severity has a clear majority (7/12 deter > 50%),
so the clause does not fire → **consistent on sign**; this is the **weakest** of the three (001 cannot reject
zero here) and flips to **uninformative** under a ⅔-supermajority reading of "clear majority". The prediction
is now **computed** from the model, not hard-coded.

- **001 restatements fixed:** A2 honest CI co-reported with RBC; "attenuates/attenuated" → the pre-declared
  **stable** labels (−22.1% / +1.5% / +24.6%); "identification confirmed by 001" removed (banned word + it
  overstated the B-pre reading).
- **In-sample appendix (item 7), actually run:** the 003 claim that adding Hansen makes the severity-class
  mean "more negative" was **fabricated and directionally wrong** — running it, the mean moves **−37.7% →
  −27.8% (LESS negative)**, class signs unchanged (appendix, not a test).
- T4 elasticities (unchanged inputs): 0.08 −0.214 (~97% of −0.22), 0.15 strict −0.121 (~100%), 0.15 statutory
  −0.080 (~66%, CI incl. 0); jail-day UPPER BOUND −4.3%/day at 0.08 vs Jansson −2.67%/prison-day; Utah .05–.07
  share 4.7% → 10.1%. Figures: `fig_margins_forest.png` (Finlay annotated, not plotted at 0%), `fig_utah_005.png`.

### Comparison table (corrected vs 002/003 on disk)

| Quantity | 002/003 (superseded) | 004 (corrected) | Source read |
|---|---|---|---|
| FL tests / two-sample DUI / files | 165,162 / 116,934 / 535 | **162,875 / 115,262 / 530** | `002…/DATA_DICTIONARY.json`, manifest |
| FL rddensity p (0.08/0.15) | 0.605 / 0.415 | **0.593 / 0.308** | `002…/density_tests.csv` |
| FL MDD (0.08/0.15) | 0.196 / 0.123 | **0.1978 / 0.1234** | `002…/florida_power.csv` |
| FL gender balance p (0.08/0.15) | 0.558 / 0.402 | **0.640 / 0.394** | `002…/florida_gender_balance.csv` |
| Last-digit-0 share | 21% ("heaps on round values") | **10.25% excl. 0.000 (uniform)** | `002…/florida_lastdigit.csv` |
| Structural audit | "100% two-extractor agreement" | **token-multiset only; field validity 99.44%** | `002…/florida_parse_audit.json` |
| Era sign at 0.15 | "negative across 1999–2007" | **2001 +0.004, 2004 +0.012** | `002…/eras.csv` |
| 003 in-sample appendix | "more negative" (fabricated) | **−37.7% → −27.8% (less negative), run** | 003 `model.md` (no code) |
| 003 record-change class | DUI 2/0/0 & general 0/0/2 (no output; drops Humphries) | **2/0/2 ambiguous; Humphries separate; 18 rows** | `003…/_sign_model.csv` |
| 003 T3-H 0.15 statutory | consistent (hard-coded) | **consistent\* (uninformative clause evaluated)** | `003…/hansen_oos_test.csv` |

## Deviations & limitations
- **Item 4 cannot be done as written:** no two-extractor field-level re-audit is possible — the raw PDFs
  were deleted page-by-page at ingest (privacy) and no fetch is allowed. The closest defensible version (an
  in-parquet per-field validity audit on a 30-pages/year deduplicated sample) was run and its true rates
  reported. This is the one substituted check; it does not change any conclusion.
- **0.15 statutory classification is borderline** (consistent on simple-majority, uninformative on
  supermajority); both are reported and the card notes it.
- Washington Panel A was not re-estimated (unchanged, verified sound). The recidivism headline is not
  re-estimated on new data (none exists). Branch N: both 0.15 codings equal standing.
- **Spec deviations disclosed** (from the audit): 002's ingest ran in 4 time-budgeted batches (not ~11×50),
  the pseudonym seed was briefly written to `/tmp/sted/seed.txt` and deleted, the per-batch name-assertion
  logged collisions through `grep -v` so the required collision paths/hashes were not recorded, and the
  by-year discrete density test was missing — **run here** (all p > 0.18). Gate-3 package versions are in
  `followup_summary.json`.
- **Ops (for the record):** the orchestrator redacted transcript step [69] (a masked-page print exposing test day/time and masked surname lengths; no name disclosed) from the 002 transcript and host log on 2026-10-07, and deleted the host session copies; the audit's own quoted leak was likewise redacted from the staged audit copy, this study's transcript, and its log.

*Artifacts: all CSV/JSON/PNG under `results/`; deduplicated data + dictionary under `workspace/data/`.
Full old→corrected ledger in `results/card_corrections.csv` (28 rows). Detailed H2 template and B-pre in
`results/findings.md`.*
