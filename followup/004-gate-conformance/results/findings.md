# Findings — 004 gate-conformance corrective (supersedes 002 + 003)

## What was corrected, and why

This study is a corrective pass over the two Hansen (2015) follow-ups — `002-methods-and-transport`
(Study A: Washington methods re-analysis + Florida transport check) and `003-theory-update` (Study B:
the margin model) — triggered by the Phase-2d provenance audit
(`gate-conformance-inputs/hansen-provenance.md`). The audit found the **Washington computation sound and
zero name leakage**, but (i) one data-integrity defect in the Florida ingest, (ii) a substantive misreading
of the heaping evidence, (iii) several reporting-layer gate violations in 002, and (iv) in 003 one
fabricated claim, a sign model presented differently from the one on disk, and a hard-coded prediction.
Nothing fabricated survives here: a claim with no code behind it was either deleted or the code was
actually run and the true result reported. A failed or unmet check is reported as failed/unmet.

Corrections (full old→corrected→reason ledger in `card_corrections.csv`, 28 rows):

- **Florida dedup.** The 537-href FDLE index has 532 unique URLs; 5 STED files were listed (and ingested)
  twice. Working only from the existing 002 parquet shards (rows map 1:1 to manifest rows in processing
  order — verified 100% `src_year_month` match), the 2nd occurrence of each repeated sha256 was dropped:
  **165,162 → 162,875 tests**, **116,934 → 115,262 two-sample DUI**, **535 → 530 unique files**. Every
  density/balance/MDD/heaping/count number and figure was recomputed on the deduplicated data.
- **Heaping artifact.** The "~21% last-digit-0 ⇒ heaps on round values" reading was a **0.000-reading
  artifact** (12.08% of tests have sample1 = 0.000). Excluding zeros the digit-0 share is **10.25%**
  (uniform; no excess at or near either threshold). The round-value-heaping caveat is **retracted**.
- **002 reporting honesty.** B-pre relabelled post-hoc and restored to the report; the structural audit
  described honestly (token multisets, not fields; "100% agreement" removed); the full H2 template with
  kernel labels and the b=h note; the 0.15 era sentence fixed; the 0.08-strict A4 result surfaced;
  "robust" removed from the Florida notes; spec deviations disclosed.
- **003 corrections.** The fabricated in-sample appendix sentence was run for real (direction is the
  OPPOSITE of what was claimed); the sign model is presented exactly as persisted (record 2/0/2 ambiguous,
  Humphries in its own class, all 18 rows); the T3-H prediction is computed from the model; the
  "uninformative" clause is evaluated for 0.15 statutory; the 001 restatements are fixed; Finlay is no
  longer plotted at 0%.

**For the record (ops):** the orchestrator redacted transcript step [69] (a masked-page print exposing test day/time and masked surname lengths; no name disclosed) from the 002 transcript and host log on 2026-10-07, and deleted the host session copies; the audit's own quoted leak was likewise redacted from the staged audit copy, this study's transcript, and its log.

---

## Part A — Washington methods re-analysis (UNCHANGED; the audit verified it sound)

The Washington Panel A estimates are **reused verbatim** from `002…/results/` (same public
`hansen_dwi.dta`, same `rd_data.rds`); nothing was re-estimated. The corrections here are reporting-layer:
the full H2 template, kernel labels, the b=h note, the era fix, and the 0.08-strict A4 result.

Gate 1 (anchor) passes exactly: A0 at 0.08, bw 0.05, with controls = −0.0221 (SE 0.0041), N = 93,899; at
0.15 = −0.0073 (SE 0.0035), N = 139,033. Gate 2 (bin means): 0.1043 at L=79, 0.1241 at L=149.

### Full H2 template per threshold/coding (all values from `002…/estimates_headline.csv`, `headline_scalars.json`)

**0.08, statutory ≥.** A1 RBC point **−0.0173** (SE 0.0059) at MSE-optimal h = 0.0278 (27/28 mass points,
N 16,201/37,364), vs paper −0.021 and A0 −0.0221 on the same file. Sign negative at every h in [0.010,0.068].
RBC 95% CI **[−0.0307, −0.0023]**, excludes zero at the MSE-optimal h. Across the A3 grid (**triangular
kernel**) the RBC CI excludes zero for **h ≥ 0.038** and includes it below; **under the rectangular kernel**
it excludes zero for h ≥ 0.026 (with a gap at 0.030). The honest (Armstrong–Kolesár) CI is **[−0.0310,
0.0010]** at M = 120.1 and **[−0.0323, 0.0044]** at 2M. CI widths: RBC 0.0284, honest 0.0320, vs 0.0157 =
2·1.96·paper SE (honest 2.04× wider). *b=h note:* the "excludes at the MSE-optimal h (0.028) / includes
below 0.038 across the grid" pairing is not a contradiction — the A3 grid fixes the bias bandwidth **b = h**,
whereas the MSE-optimal fit uses **b = 0.043**.
> **Verdict:** bandwidth-dependent under 2026 inference; point estimate **stable** (−22.1% vs the same-file
> A0). The interval includes zero because it is honest 2.04× wider than the paper's, not because the estimate moved.

**0.15, statutory ≥.** A1 RBC **−0.0074** (SE 0.0048), h = 0.0288 (28/29 mass points, N 45,138/39,087),
vs paper −0.010 / A0 −0.0073. Sign negative at every h. RBC 95% CI **[−0.0185, 0.0043]**, includes zero.
Across the A3 grid (**triangular**) it includes zero at **every** h; **under the rectangular kernel it
EXCLUDES zero for h ≥ 0.060** — so "includes zero at every h" is a triangular-only statement. Honest CI
**[−0.0193, 0.0068]** at M = 86.1, **[−0.0189, 0.0113]** at 2M. CI widths RBC 0.0227, honest 0.0262 (RBC
1.93×, honest 2.22× wider).
> **Verdict:** bandwidth-dependent; point estimate **stable** (+1.5% vs A0).

**0.15, strict >.** A1 RBC **−0.0112** (SE 0.0047), h = 0.0304 (30/30 mass points, N 48,284/39,786),
vs paper −0.010 / A0 −0.0090. Sign negative at every h. RBC 95% CI **[−0.0228, −0.0007]**, excludes zero at
the MSE-optimal h; across the A3 grid (**triangular**) for h ≥ 0.034; **under the rectangular kernel it is
non-monotone**. Honest CI **[−0.0250, 0.0009]** at M = 83.4, **[−0.0261, 0.0038]** at 2M (honest 2.21× wider).
> **Verdict:** bandwidth-dependent; point estimate **stable** (+24.6% vs A0).

No threshold/coding clears "confirmed/robust" (both CIs excluding zero) and none triggers "does not survive"
(which also needs an A3 sign change — the estimate stays negative across the whole grid). All three are
bandwidth-dependent with stable point estimates. The 0.15 result is **coding-sensitive** (strict RBC
excludes zero at the MSE-optimal h; statutory includes it under the triangular kernel at every h, excludes
it under the rectangular kernel for h ≥ 0.060).

**Coding unresolved; do-files not obtained.** (Branch N: both 0.15 codings carry equal standing.)

**A4 sensitivity — 0.08 strict (surfaced per audit):** moving the 0.08 cutoff to the strict (> 0.080)
coding moves A1 from −0.0173 to **−0.0111 (SE 0.0063), RBC CI [−0.0233, 0.0063] which INCLUDES zero**
(`sensitivity_008.csv`).

**Eras (A5, corrected):** at 0.08 the A0 year estimates are negative across 1999–2007; **at 0.15 they are
NOT — 2001 = +0.004 and 2004 = +0.012** (`eras.csv`). There is no significant era difference at either
threshold (0.08 diff −0.0078, p ≈ 0.31; 0.15 diff −0.0064).

Other Panel A (unchanged): manipulation rddensity p = 0.144/0.158 (modern test agrees with the paper, unlike
the replication's over-rejecting McCrary `DCdensity`); covariate balance RBC CIs all include zero.

---

## Part B — Florida 2021–2026 transport check (RECOMPUTED on deduplicated data)

**B-pre (pre-declared reading) — NOTE: this block was written AFTER the Florida estimates (002 step [128],
after the estimates at [111]–[117]); it therefore CANNOT claim pre-declaration. It is restored here and in
report.md with that sequencing stated plainly.**
- If sorting is found at 0.08 or 0.15 in Florida → "the design does not transport to Florida 2021–2026 as is".
- If no sorting is found **and** the test has the power stated in B1 → "a Florida recidivism RD (pending the
  person-ID records gate) is feasible on identification grounds".
- If no sorting is found but the test is underpowered by the B1 rule → "no sorting was detected, but the
  Florida test cannot rule out discontinuities of the size [MDD]", and nothing stronger.
- **Neither outcome bears on the validity of Hansen's Washington estimates.**

**Data (deduplicated).** 530 unique STED files (535 downloads), **162,875** subject tests, of which
**115,262** are two-sample DUI tests (the analysis sample). Per-year test counts: 2021 29,374 / 2022 29,668 /
2023 28,980 / 2024 29,025 / 2025 27,891 / 2026 17,937 (`florida_counts.csv`). Privacy unchanged (names
dropped in memory, never written).

**No sorting at either threshold.** rddensity (pooled): **p = 0.593 (0.08), 0.308 (0.15)** (WA 0.144/0.158).
Discrete binomial tests (k = 1,2,5,10, pooled) all p > 0.50; the **by-year** discrete tests that 002 omitted
were run (both thresholds, k = 2,5, every year) and all p > 0.18 (`density_tests.csv`). Gender balanced:
A1 coef **+0.0104 (p 0.640)** at 0.08, **+0.0065 (p 0.394)** at 0.15 (both CIs include zero).

**Power.** FL MDD **0.1978 (0.08), 0.1234 (0.15)** vs WA 0.0995/0.0834. The underpowered rule (FL MDD >
2×WA MDD) is **not** triggered at either threshold — but **at 0.08 the margin is razor-thin: FL 0.1978 vs
2×WA 0.1991, a gap of only 0.0013**. So the 0.08 non-rejection is adequately powered by the rule, but barely.

**Heaping (CORRECTED).** No excess mass at the exact cutoff bins (ratio 1.05 at 0.080, 1.02 at 0.150 vs WA
0.97/1.00) **and no round-value excess near the thresholds** (counts/neighbour-mean: 0.070 → 0.93, 0.090 →
0.95, 0.100 → 0.995, 0.150 → 1.02; `florida_roundvalue_check.csv`). The earlier "~21% last-digit-0 ⇒ heaps
on round values" was a **0.000-reading artifact**: 12.08% of two-sample DUI tests have sample1 = 0.000;
**excluding zeros the digit-0 share is 10.25%** (uniform; χ² p = 0.085, no single digit dominant), and the
same holds per-instrument (top-3, digit-0 9.4–10.2%, all p > 0.3). The donut re-run dropping only the cutoff
bin leaves no discontinuity (p 0.640 / 0.268). **The round-value-heaping caveat is retracted**, and the
all-round-bins donut (which was motivated by the misread) is removed.

**Structural audit (honest).** 002's "100% two-extractor agreement" referred to page-level **BrAC token
multisets + presence flags**, *not* parsed fields; its field-level `-layout`-vs-`-raw` comparison had failed
at **0.000** agreement (the parser is line-structure dependent, which `-raw` destroys); the schema width was
hard-coded (`nflds.add(9)`); and the raw-token value range **smax 3.4–4.6** (outside BrAC [0,0.5]) went
unremarked. A genuine two-extractor re-parse **cannot be rerun** (raw PDFs deleted page-by-page at ingest;
no fetch permitted). The closest defensible check — a per-field validity audit on 30 deduplicated pages/year
— gives per-field pass rates of 100% except **n_valid_samples 99.44%** (pages with 3+ readings store only
the first two), and the in-parquet subject-sample readings are all within **[0, 0.478]** (0 out of range),
confirming the parsed fields are in range even though the raw token stream was not (`florida_field_audit.json`).

**Transport verdict (per B-pre, deduplicated):** no sorting at 0.08 or 0.15, test adequately powered (0.08
razor-thin) ⟹ *a Florida recidivism RD (pending the person-ID records gate) is feasible on identification
grounds*. **Neither outcome bears on the validity of Hansen's Washington estimates.** (No "robust" claimed.)

---

## Part C — Theory update (003 corrections)

**Sign model, exactly as persisted (`_sign_model.csv`, all 18 non-Hansen rows):**

| Margin class | n | deter / null / crim | majority |
|---|---|---|---|
| severity / certainty, no record | 12 | 7 / 3 / 2 | **deter** |
| record change | 4 | 2 / 0 / 2 | **ambiguous/null** |
| mixed (Humphries 2025) | 1 | 0 / 0 / 1 | criminogenic |
| monetary only (Finlay 2024) | 1 | 0 / 1 / 0 | null |

The card's earlier **DUI/general split of the record class (2/0/0 and 0/0/2) exists in no persisted output
and dropped Humphries**. As a *disclosed post-hoc variant* (`_sign_model_recordsplit_variant.csv`): record-
change DUI = 2/0/0 (deter; Sloan ×2); record-change general = **0/0/3 (criminogenic; Agan, Mueller-Smith,
and Humphries counted honestly)**. Note: **Huttunen-Kaila-Nix** is coded criminogenic on its *fines* finding
but sits in the severity_norecord class in the persisted model — flagged here, not silently moved.

**T3-H prediction — computed from the model (no hard-coded return).** Both Hansen margins map (from the T0
codes fixed before the fit) to the **severity_norecord** class, whose majority is **deter (7/12)** → predict
**DETER (−)**. For Hansen 0.08 the partial DUI-record component also deters (Sloan). Classification under the
pre-declared rule:

| Hansen margin | predicted | 001 A1 (rel) | 001 A1 CI | 001 A2 CI | classification |
|---|---|---|---|---|---|
| 0.08 | deter (−) | −16.6% | [−29.4, −2.2] | [−29.7, +0.9] | **consistent** |
| 0.15 statutory ≥ | deter (−) | −6.0% | [−14.9, +3.4] | [−15.6, +5.5] | **consistent\*** |
| 0.15 strict > | deter (−) | −9.1% | [−18.4, −0.5] | [−20.2, +0.7] | **consistent** |

**\* 0.15 statutory — the uninformative clause, evaluated.** The clause is "both 001 CIs include zero AND the
sign model has no clear majority." Here **both CIs do include zero** (True), but the severity class **does**
have a clear majority (7/12 deter > 50%), so the clause does **not** fire and the rule returns **consistent**
on sign. This is the **weakest of the three**: 001 cannot reject zero at this coding, and under a stricter
⅔-supermajority reading of "clear majority" (7/12 = 58% < 67%) the rule would return **uninformative**
(`hansen_oos_test.csv`, column `classification_supermajority_defn`). We report consistent with this caveat
rather than asserting it as the hard-coded 003 card did.

**001 restatements (fixed).** Card metric 1 now co-reports the A2 honest CI with the RBC CI. The pre-declared
±25% labels are **stable** for all three (0.08 −22.1%, 0.15 statutory +1.5%, 0.15 strict +24.6%) — the words
"attenuates/attenuated" are removed. "Identification confirmed by 001" is removed (banned word; and it
overstated the B-pre reading, which is "feasible on identification grounds", now on deduplicated FL data).

**Re-analysed elasticities (T4, unchanged inputs):** 0.08 −0.214 (~97% of paper −0.22); 0.15 strict −0.121
(~100% of −0.12); 0.15 statutory −0.080 (~66%, CI includes zero). Jail-day UPPER BOUND −4.3%/jail-day at
0.08 vs Jansson et al. −2.67%/prison-day. Utah .05–.07 arrest share 4.71% → 10.06% (2.14×; partly mechanical).

**In-sample appendix (item 7) — ACTUALLY RUN, not a test.** The 003 model.md sentence "an in-sample fit
including Hansen's two rows pulls the DUI severity-class mean slightly **more** negative" was **fabricated**
(no code computed any in-sample fit) **and directionally wrong**. Running it: the severity-class numeric mean
(Kilmer-Midgette −49, Gehrsitz −20, Rose-Shem-Tov −44 → **−37.7%**) becomes **−27.8%** when Hansen's two rows
(paper relative −17 / −9) are added — i.e. **LESS negative** (−27.7% using 001's A1 relatives). Class signs
unchanged (`insample_appendix.json`). This is an appendix, not a classification input.

**Answer to the reader (T6).** The newer "prosecution/jail raises reoffending" studies (Agan, Mueller-Smith,
Humphries) act on a **general-crime conviction/record channel** — criminogenic in the data — whereas Hansen's
thresholds move **DUI experienced-severity** (jail days, suspension), which deters across the post-2015
evidence; the one DUI record study (Sloan) also deters. The new evidence **refines rather than refutes**
Hansen. The genuine tension is at 0.08 (partly a record margin), where 001 is bandwidth-dependent though the
point estimate is stable.

---

## Deviations & limitations
- **No two-extractor structural re-audit** (item 4): the raw PDFs were deleted page-by-page at ingest
  (privacy design) and this study permits no new fetches, so a genuine `-layout`/`-raw` field-level
  comparison cannot be rerun. The closest defensible version — an in-parquet per-field validity audit on a
  30-pages/year deduplicated sample — was run and its true rates reported.
- **0.15 statutory classification is borderline**: consistent under a simple-majority reading of the
  pre-declared "clear majority", uninformative under a ⅔-supermajority reading; both are reported.
- Washington Panel A was **not** re-estimated (unchanged; audit verified sound); the recidivism headline is
  not re-estimated on any new data (none exists). Branch N: both 0.15 codings carry equal standing.
- The in-sample appendix uses the paper's relative effects (−17/−9) to match the audit's arithmetic; the
  001-A1 variant (−27.7%) is reported alongside.
