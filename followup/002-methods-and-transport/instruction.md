# LAUNCH SCOPE: Execute ONLY Study A (the 001 methods-and-transport study). Study B sections are context for you, not tasks: do not execute them.

# Extension specs: Hansen (2015), "Punishment and Deterrence: Evidence from Drunk Driving"

**Status:** REVISED 2026-10-05 against the Phase 2b judge items H1–H11 (`econ3_papers/verdicts/phase2b-judge.md` §3). The first draft was written the same day by the recency-research agent. Every source below was verified live on 2026-10-05 (see `recency-research.md`). The changelog at the end maps each judge item to its change.

**What this pair is, in one sentence.** Study 001 re-analyses the same 1999–2007 Washington data the paper used, with current RD inference methods, and checks whether the design's no-sorting assumption transports to Florida's 2021–2026 breath tests. **The paper's recidivism headline has not been re-estimated on post-2007 or non-Washington data, because no public data allows it.** The requests that would allow it are pending and listed at the end of this file.

This file holds the standard pair. At launch, each part is copied to its own `--instruction-file`:
- **Part I → `001-methods-and-transport`** (launch with `--name methods-and-transport`). Panel A is a methods re-analysis of the public Washington file. Panel B is a transport check of the identifying assumption on Florida 2021–2026 public test-level data.
- **Part II → `002-theory-update`.** A quantitative synthesis that places Hansen's two sanction margins against the post-2015 sanctions–reoffending literature, written down as a model of which margins deter. Its headline test is an out-of-sample one: the model is fitted without Hansen's rows and then predicts Hansen's two margins.

**Data reality, stated up front.** No public, person-linked recidivism microdata exists for any state or year beyond Hansen's own 1999–2007 Washington extract (the Mixtape `hansen_dwi.dta`). Re-estimating the recidivism headline on other states or later Washington years is therefore **pending human gates**: records requests and the author's file (`recency-research.md` §4). A Florida, later-Washington or Utah-0.05 recidivism RD becomes a later study once those gates open.

---

# PRE-LAUNCH HUMAN INPUTS (for the orchestrator; not part of either instruction file)

Two steps need a human. No agent attempts either one: neither has an account, and neither sends outward email. The orchestrator surfaces both to the user before launching 001.

**HI-1. openICPSR 112907 V1 do-files (about 10 minutes, human).**
- What: log in to openICPSR with a free account, accept the AEA terms, and download `Do-Files/` from project 112907 V1. The terms are never bypassed and no agent logs in.
- Why: the Table 4 do-file shows whether the 0.15 treatment indicator is `bac>=0.15` or `bac>0.15`, and which sample filters were applied. That settles the open 0.15 coding question directly (`recency-research.md` §1.2).
- If obtained: place the files in `econ3_papers/corpus/hansen-2015-punishment-drunk-driving/extension-assets/icpsr-112907/`, with a `PROVENANCE.md` that records who downloaded them, the date, the openICPSR version, and the sha256 of each file. Then set the launch line in Part I to `DO-FILES: OBTAINED`.
- If not obtained by launch: set the launch line to `DO-FILES: NOT OBTAINED`. 001 then runs the pre-registered both-codings path (§4, Branch N).

**HI-2. Email Ben Hansen (human; he is the requester).**
- What: ask for the full 1999–2007 file, or at least the prior-test flag, county, PBT and outcome-split variables, and a person ID or post-2007 tests. Also ask him to confirm whether the Mixtape extract is the analysis sample and how the 0.15 indicator was coded.
- This is **non-blocking for 001** and does not change 001's scope, even if he replies before launch. A reply with data goes to a later study. A reply that confirms the 0.15 coding in writing counts as Branch D evidence only if the do-files are also obtained; otherwise it is quoted in 001's report as author correspondence, and Branch N still runs.

Suggested text for HI-2 (the human edits and sends it):

> Dear Professor Hansen, thank you for asking us to extend your 2015 AER paper. We are re-analysing the public Mixtape extract with current RD inference and checking the design on Florida's 2021–2026 breath-test records. Two things would help a great deal. First, could you confirm whether the Mixtape `hansen_dwi.dta` is your analysis sample, and whether the 0.15 indicator was coded as BAC ≥ 0.150 or BAC > 0.150? On the public file the 0.15 estimate moves from about −0.007 to about −0.009 between those two codings. Second, would you be able to share the prior-test flag, county and outcome-split variables, or any post-2007 tests, so that the recidivism result itself can be re-estimated? We would of course follow any data terms you need.

---

# PART I: Follow-up study 001, methods re-analysis and transport check

**LAUNCH LINE (filled by the orchestrator before launch):** `DO-FILES: NOT OBTAINED`

**Launcher settings:** `veritas followup <run_dir> --instruction-file <part-I.md> --name methods-and-transport --timeout 21600`. The timeout is 6 hours. The compute need is under 2 core-hours, and the remainder covers the Florida download at a polite rate.

**Continuation study.** The Florida ingest checkpoints after every batch (§B0). If this session ends early, the orchestrator relaunches the same instruction as the next free number with `--name methods-and-transport-cont`. That study reuses `followup/001-methods-and-transport/workspace/` (the manifest, the de-identified parquet and any results already written) and resumes from the first unparsed file. It never re-downloads a file the manifest marks as parsed.

## 0. What this study is (read first; this framing is binding)

- Panel A re-estimates the paper's two thresholds on **the same 1999–2007 Washington data** with current RD methods. This is a methods re-analysis. It is not an update of the paper to the current world, and nothing in the report, the card or `findings.md` may call Panel A "living", "updated" or "new evidence on recidivism".
- Panel B uses data that did not exist in 2015, but it tests only the design's identifying assumption (no sorting at 0.08 and 0.15) in another state. It does not test the recidivism headline.
- **The first sentence of `results/findings.md` and of `report.md` is, verbatim:** "The paper's recidivism headline has not been re-estimated on post-2007 or non-Washington data. No public data allows it; requests are pending (listed in Limitations)."
- The result card's `headline` opens with that same statement and then gives the key number in the same sentence (see §6).

## Workspace staging (do this first)

The launcher stages `extension-assets/{florida,utah,nhtsa,literature}` from `econ3_papers/corpus/hansen-2015-punishment-drunk-driving/` into `/workspace/eval/followup_staging/shared-data/`. If HI-1 succeeded, it also stages `extension-assets/icpsr-112907/`. FARS is not needed by 001 and is not staged.

FIRST action:
1. Symlink that directory into your own `workspace/`.
2. For every staged directory, verify that each file listed with a sha256 in its `PROVENANCE.md` is present and its sha256 matches. Rows without a sha256 (for example the PROVENANCE file itself) are not checked.
3. `florida/PROVENANCE.md` says that no STED data PDF is staged. That is intentional. Do not report it as missing, and do not fetch any STED file into `shared-data/` or `workspace/`.
4. Check the launch line against the staging: `DO-FILES: OBTAINED` requires `shared-data/icpsr-112907/` with a PROVENANCE file, and `NOT OBTAINED` requires its absence. If they disagree, stop and report the mismatch. Do not guess.

The public Washington analysis file is the replication's own copy: `replication/codebase/data/hansen_dwi.dta` (sha256 `08158875…ecd1`). The replicated R code in `replication/codebase/` (`table3_dui_rd.R`, `table4_aggdui_rd.R`, `density_tests.R`) is the reference implementation of the paper-era specification. Reuse its definitions; do not re-derive them.

Do NOT open `extension-assets/prep-diagnostics/` until all of your own Panel A estimates are written to `results/`. It holds a pre-spec preview, which you may compare against afterwards in an appendix.

Do not read other studies under `followup/`.

## 1. The questions and the design

Hansen (2015) uses a sharp RD in breath-alcohol content (BAC; running variable = the lower of two breath readings, discrete in 0.001 steps) at Washington's DUI threshold (0.08) and aggravated-DUI threshold (0.15). Outcome: any later breath test or refusal within 4 years. Drivers are aged 21+, tested 1999–2007.

The paper's inference is 2015-era: a local linear fit, a rectangular kernel, hand-picked bandwidths of 0.05 and 0.025, and SEs clustered on BAC bins. Standards have since changed:
- Calonico, Cattaneo and Titiunik (2014) and Calonico, Cattaneo and Farrell (2020): data-driven MSE/CER-optimal bandwidths with robust bias-corrected (RBC) inference. CCT (2014) predates the paper's publication, which is one more reason Panel A is a methods re-analysis, not an update.
- Kolesár and Rothe (2018, *AER* 108(8)): clustering on a discrete running variable does not give valid coverage. Honest CIs under a bound on curvature do, and they are designed for discrete running variables.
- Cattaneo, Jansson and Ma (2020): `rddensity` replaces McCrary's `DCdensity`.

**Question A (methods re-analysis, same Washington data).** How do the paper's two estimates read on the same data under current RD inference, and how fragile is the 0.15 estimate to the treatment coding of the single mass point at 0.150?

**Question B (transport check, new state and decade).** Does the design's identifying assumption hold in a currently published, test-level breath dataset under the same legal structure in another state? The assumption is no sorting of BAC around 0.08 and 0.15, with a smooth predetermined covariate (gender). The dataset is Florida FDLE Intoxilyzer 8000 STED, 2021-01 to 2026-07. Florida's per se limit is 0.08 and its enhanced penalties start at 0.15 (Fla. Stat. §316.193(1),(4)).

**HARD PROHIBITIONS**
- No person linkage of any kind in the Florida data.
- The subject-name, operator-name and arresting-officer-name fields are discarded at parse time, in memory. Names are never written to disk, logs, stdout or outputs. Never attempt re-identification or joins to outside data.
- **Never print raw STED page text** to the terminal, a log or any file. That includes `head`, `cat`, `less`, `grep` with matching lines, or a Python `print` of a page. The terminal output is persisted in the transcript.
- No recidivism outcome for Florida (it would need surname linkage; out of scope and ethics-gated).
- No fetches beyond those listed in §3. Never log in anywhere, and never send email or any other outward message.

## 2. Claims being re-analysed (paper values)

| ID | Claim | Paper value | Home |
|---|---|---|---|
| C1 | Crossing 0.08 lowers 4-year recidivism, all drivers, with controls | −0.021 (0.004), N = 95,111, bw 0.05; −0.019 (0.005), N = 49,396, bw 0.025; mean at 0.079 = 0.103 | Table 3 col 1 |
| C1a | Same without controls | −0.020 (0.004) / −0.019 (0.005) | App. Table 1 |
| C2 | Crossing 0.15 lowers 4-year recidivism, all drivers, with controls | −0.010 (0.003), N = 146,626; −0.011 (0.005), N = 78,622; mean at 0.149 = 0.125 | Table 4 col 1 |
| C2a | Same without controls | −0.011 (0.003) / −0.011 (0.005) | App. Table 2 |
| C3 | No manipulation | McCrary p = 0.59 (0.08), 0.38 (0.15); Frandsen p = 0.795, 0.886 | text p. 1587; App. Fig. 2 |
| C4 | Covariate balance at both thresholds (male, white, age, accident) | all insignificant (Table 2) | Table 2 |
| C5 | Robust to bandwidth (significant for bw ≳ 0.02), polynomial order and kernel | e.g. triangular bw 0.05: −0.016 (0.08), −0.010 (0.15) | App. Fig. 3; App. Tables 5–6 |

Read every original-side comparison value from the replication artifacts on disk, citing the file in each comparison row:
- `replication/codebase/outputs/table3.json`, `table4.json`, `table2.json`, `density_tests.json`, `baseline.json`;
- the paper values above, which also appear in `analyze/paper_claims.json`.

**Not re-analysed, with reasons; list these as caveats:**
- The prior-test splits, PBT, recidivism-type outcomes, time-window outcomes, other-crime outcomes, county FE, court sanctions, and border/interior. None of these variables are in the public file.
- Recidivism in any state other than Washington, or in Washington after 2007. No public person-linked data exist; these are pending records requests.
- An RD at Utah's 0.05. Only fiscal-year aggregates are public; arrest-level data need a GRAMA request.

## 3. Pre-verified sources (verified 2026-10-05)

| Variable / asset | Source | Coverage verified | Access |
|---|---|---|---|
| WA test-level BAC, recidivism, male, white, age, accident, year | `hansen_dwi.dta`, the Mixtape extract (in the replication codebase) | 214,558 tests, 1999-01-02 to 2007-12-31, ages 21–80. **Within the paper's bandwidths it is ~95–99% of the paper's N, not a 42% draw.** | on disk |
| FL test-level breath tests | FDLE STED monthly PDFs. Link list in `shared-data/florida/subject-test-electronic-data_index.html`: 537 `.pdf` hrefs (keep only filenames starting `STED`; a few, e.g. `Memo-for-STED.pdf` and `StatementofAgencyOrg_October2021_Final.pdf`, are not data), all relative to `https://www.fdle.state.fl.us`. By year: 2021: 98, 2022: 95, 2023: 96, 2024: 95, 2025: 96, 2026: 56 (through 2026-07). Index page: https://www.fdle.state.fl.us/alcohol-testing-program/intoxilyzer-8000-records/subject-test-electronic-data | Pilot-parsed 2021-01 (343 tests) and 2026-03 (264 tests) with `pdftotext -layout`. One page per test. The field structure is documented in `florida/PROVENANCE.md`. About 75% of tests have two valid samples. ~1.1 MB per PDF, ~0.6 GB total. | keyless GET (send a browser User-Agent). **This is the one sanctioned bulk fetch.** Raw PDFs live only in `/tmp/sted/` (§B0) and are deleted per batch. |
| FL legal thresholds | Fla. Stat. §316.193(1) "0.08 or more"; §316.193(4) "0.15 or higher" (2026 Statutes, leg.state.fl.us) | fetched 2026-10-05 | cite only |
| WA aggravated threshold wording | RCW 46.61.5055(1)(b) "at least 0.15" (current text) | fetched 2026-10-05; the 1999–2007 text was not checked | cite only |
| Authors' do-files (Branch D only) | openICPSR 112907 V1 `Do-Files/`, staged by a human under `shared-data/icpsr-112907/` | per its PROVENANCE | on disk if staged; never fetched by the agent |

## 4. Pre-declared estimands and reporting rule

Notation: L = `low_score` (integer, 0.001 BAC units), c ∈ {80, 150}, x = (L − c)/1000. The statutory coding is "treated if L ≥ c" ("at least"). The strict coding is "treated if L ≥ c + 1" ("> c"). Outcome: `recidivism`.

### The do-file conditional (decided by the launch line, before any estimate is computed)

**Branch D: `DO-FILES: OBTAINED`.**
1. Before running any estimator, open the Table 3 and Table 4 do-files in `shared-data/icpsr-112907/` and find the treatment-indicator definitions and the sample filters.
2. Write `results/dofile_coding.md`. It quotes the indicator lines verbatim with file name and line number, states the coding at each threshold (`>=` or `>`), and lists every sample filter, marking each as "reproducible on the public file" or "needs a variable the public file lacks". Quote only those lines. Do not copy the do-files into `results/`.
3. **The authors' coding becomes the headline coding for A1 and A2 at that threshold.** The other coding is reported in A4 as a sensitivity, not as a co-headline.
4. Apply every reproducible sample filter to A1–A7 as well, and report A0 both with and without them. Gate 1 (below) is unchanged and always runs on the replication's own specification.
5. Card and findings wording: "0.15 coding resolved from the authors' do-file (`<file>`, line `<n>`: `<quoted line>`)". If the authors coded `>=`, also say plainly that the coding does not explain why the public file's 0.15 estimate is smaller than the paper's, and that the gap stays open.

**Branch N: `DO-FILES: NOT OBTAINED`.**
1. The coding is reported as an open specification question. Never present either coding as the correct one.
2. **At 0.15, A1 and A2 are reported under both codings, as a pre-registered pair with equal standing.** Each coding gets the full reporting template below. Neither is promoted after the results are seen. At 0.08 the statutory coding is the headline and the strict coding stays in A4.
3. The card and findings state, verbatim: "coding unresolved; do-files not obtained."
4. If author correspondence from HI-2 confirms a coding, quote it in the report as correspondence. It does not move the study to Branch D.

### Panel A: Washington public file (methods re-analysis)

**A0. Gate anchor (paper spec).**
- OLS of recidivism on T, x and T·x, plus male, white, age FE and year FE.
- Rectangular kernel, windows |x| ≤ 0.05 and ≤ 0.025, SEs clustered on L.
- Also run without controls.

**A1. HEADLINE ESTIMATOR, part 1 (RBC).**
- `rdrobust` (Python `rdrobust`, version 2.1.0 used in prep, or R `rdrobust`): `p=1`, `kernel='triangular'`, `bwselect='mserd'`, `vce='hc1'`, **no clustering**, no covariates.
- The running variable is discrete: about 13–19 mass points lie inside the MSE-optimal h on each side. Record the `masspoints` setting used (the package default is `'adjust'`; keep it), and report the number of distinct mass points inside h on each side of each estimate.
- Report the conventional estimate, its SE, the **RBC 95% CI**, h, the effective N on each side, and the mass-point counts.
- Also report the covariate-adjusted version (`covs` = male, white, age, year dummies) and `bwselect='cerrd'`.

**A2. HEADLINE ESTIMATOR, part 2 (honest). Co-equal with A1, not secondary.**
- R `RDHonest` (CRAN; install from CRAN into a writable user library if absent).
- Sharp RD, triangular kernel, MSE-optimal h, the package's default rule-of-thumb curvature bound M (Armstrong–Kolesár). Report the honest 95% CI, h and M.
- Sensitivity: report the CI again at 2M.
- If `RDHonest` cannot be installed, say so in the report and implement the Kolesár–Rothe (2018) bounded-misspecification CI from its formulas. Never silently drop A2.

**A3. Bandwidth curve.**
- Conventional and RBC estimates for h ∈ {0.010, 0.012, …, 0.068}, for both rectangular and triangular kernels, at both thresholds (and under both codings at 0.15 in Branch N).
- This is the figure.

**A4. Coding and donut sensitivity panel** (at 0.15 and, for symmetry, at 0.08):
- (i) statutory coding vs strict coding (in Branch D, the authors' coding vs the other one);
- (ii) donuts dropping |L − c| ≤ d for d ∈ {0, 1, 2, 3, 5}, plus a drop of the single bin c;
- (iii) with and without controls;
- (iv) the A1 estimator under each of (i)–(ii).

**A5. Eras (over-time structure).**
- Re-estimate A0 (bw 0.05) and A1 for the eras 1999–2003 and 2004–2007, and year by year 1999–2007.
- Give an era-difference test for each threshold.

**A6. Manipulation.**
- `rddensity` at both thresholds (report p_jk and the `rdplotdensity` figure).
- A discrete-support test in the spirit of Frandsen (2017). R `rdd` has no Frandsen implementation, so implement the binomial test of the cutoff bin's share among the adjacent k bins on each side, for k ∈ {1, 2, 5, 10}, with the paper-style smoothness allowance. Show a grid, not one k.
- Report the `DCdensity` result from the replication beside them, with a one-paragraph explanation of the divergence.

**A7. Covariate balance with the A1 estimator.** Male, white, age, accident, at both thresholds.

### Panel B: Florida 2021–2026 (transport check of the identifying assumption only)

**B-pre. Pre-declared reading (written before any Florida estimate).** Copy this block into `results/findings.md` and into the report before running B1, and do not edit it afterwards:
- If sorting is found at 0.08 or 0.15 in Florida, it means "the design does not transport to Florida 2021–2026 as is".
- If no sorting is found **and** the test has the power stated in B1, it means "a Florida recidivism RD (pending the person-ID records gate) is feasible on identification grounds".
- If no sorting is found but the test is underpowered by the B1 rule, it means "no sorting was detected, but the Florida test cannot rule out discontinuities of the size [MDD]", and nothing stronger.
- **Neither outcome bears on the validity of Hansen's Washington estimates.** This sentence appears in `findings.md` and on the card, next to the Florida density metric.

**B0. Ingest (privacy-first; read every bullet).**
- **Where raw files live.** Download STED PDFs only to `/tmp/sted/raw/`, which is container-local scratch outside `workspace/`, outside the study directory and outside anything the transcript or the portal copies. Never write a STED PDF, or any text extracted from one, under `workspace/`, `results/` or the study directory.
- **Batching (each tool call under about 8 minutes).** Process the 537 links in batches of about 50 files per foreground tool call, roughly 11 calls in all. Each call: (1) download its batch with ≥ 0.5 s between requests and up to 3 retries; (2) parse; (3) append records to the de-identified parquet; (4) run the per-batch name assertion; (5) delete that batch's PDFs from `/tmp/sted/raw/`; (6) update the manifest and `followup_summary.json`. If a batch nears 8 minutes, end the call after finishing the current file and continue in the next call.
- **Resume.** `workspace/data/fl_manifest.csv` has one row per link: filename, URL, download status, sha256 of the PDF, page count, record count, parsed timestamp. A file marked parsed is skipped. This is the checkpoint the continuation study uses.
- **Parse in memory.** Run `pdftotext -layout <pdf> -` and read its stdout into Python directly. No intermediate text file, and no printing. Split pages on form feeds. For each page, extract only these fields: year-month of the test, instrument serial, violation code, gender, Subject Sample #1 and #2 (BrAC to 0.001), the refusal flag and the volume-not-met flag. The three name fields (subject surname, operator, arresting officer) are recognised by their labels and dropped before the record is built. They never enter a DataFrame.
- **Fields kept in the de-identified parquet** (`workspace/data/fl_tests_deid.parquet`): year-month (no day, no time), violation code, gender, sample 1, sample 2, refusal flag, volume-not-met flag, the source filename's year-month, and an **instrument pseudonym** (a random integer per serial, drawn in memory from a seed that is never saved). The raw instrument serial and the registered agency are **not kept**: together with a date they are quasi-identifying against public arrest logs. Neither is needed for B1–B4.
- **Sample.** Keep DUI tests with two numeric samples. Running variable = min(sample 1, sample 2) in 0.001 units (Hansen's convention). Variant: sample 1 only.
- **Per-batch name assertion.** While a batch's name strings are still in memory, collect every name token of 4 or more characters and search, as whole-word case-sensitive matches, every file under the study directory (`workspace/`, `results/`, logs, `followup_summary.json`) and the study's transcript file if it is accessible. The assertion is zero hits. Report only the count and the file paths, never the matched text or line. If a hit lands in a Florida-derived file (parquet, manifest, a CSV or a log written by the ingest), stop: delete that file, fix the parser and re-run the batch. If a hit lands in prose that does not come from Florida data (for example the token also occurs in a cited author's surname), record "token collision in non-Florida text" with the file path and the token's SHA-256 prefix only. Then discard the names.
- **Structural parse audit (replaces any page spot-check; nothing printed from pages).** Per year, on 30 random pages, parse each page twice with independent extractors (`pdftotext -layout` and `pdftotext -raw`, both read in memory). Report only:
  - the field-by-field agreement rate between the two parses;
  - the number of extracted fields per record (it must equal the schema width every time);
  - value ranges and domains: samples in [0.000, 0.500], gender in a fixed small set, violation code in a fixed small set, refusal and volume flags boolean;
  - one test record per page (page count = record count for every file);
  - a schema assertion that the parquet has no column whose name or content type could hold a name (no free-text string column at all).
  If agreement on the BrAC fields is below 99.5% in any year, stop and diagnose without printing page text.
- Report counts by year: parsed, refused, volume-not-met, two-sample.

**B1. Density tests, with power and heaping.**
- `rddensity` and the A6 discrete test at 0.08 and 0.15, pooled 2021–2026 and by year.
- **Power.** Florida has about 5k tests near 0.08, against about 100k in Washington. For each pooled Florida test, report the rddensity estimate of the log-density jump with its 95% CI, and a minimum detectable discontinuity: MDD = (1.96 + 0.84) × SE of the log-density jump (80% power, 5% two-sided). Report the same MDD for Washington at each threshold. **Pre-declared rule:** if the Florida MDD exceeds 2× the Washington MDD at a threshold, a non-rejection there is reported as "underpowered: no sorting detected, discontinuities up to [MDD] not ruled out".
- **Heaping.** Report the share of two-sample tests at exactly 0.080 and 0.150, beside the mean share of the 5 bins on each side. Also report the last-digit distribution of sample 1 and sample 2 (0.001 units), with a chi-square test against uniform, overall and for the instrument pseudonyms with the most tests. The Intoxilyzer 8000 reports to 0.001 but may truncate. Instrument heaping on round values looks like manipulation in density tests, so any heaping found is reported next to the density result it could affect, and the density test is re-run with the heaped bins dropped (a donut of the cutoff bin).

**B2.** Gender balance at both thresholds (A1 estimator with outcome = male).

**B3. Descriptive.** The BAC histogram with 0.08 and 0.15 marked; the refusal share by month.

**B4. Comparison table.** Florida density, MDD, heaping and balance results beside Washington 1999–2007 (A6/A7) in one table, labelled "FL vs WA (2026 tests)".

### Reporting rule (fixed now; this replaces the draft's rule)

**The headline is the A1 and A2 pair, reported together on one line, at each threshold.** The A0 numbers are the "paper method on the same file" column. All A3/A4 variants are reported in full, and no variant may be promoted to headline after seeing results.

**Required template.** Every statement of a headline result, in `findings.md`, `report.md` and the card, uses this template in full. Fill every bracket; drop none.

> "At [0.08 | 0.15][, coding: statutory ≥ | strict > | authors' (do-file)]: point estimate [x] (SE [se]) at the MSE-optimal h = [h] ([n_L] / [n_R] mass points), against the paper's [paper value] and [A0 value] by the paper's method on the same public file. The sign is [negative at every bandwidth in [h_min, h_max] | negative for h in [range] and positive for h in [range]]. The RBC 95% CI is [lo, hi] and [excludes | includes] zero at the MSE-optimal h; across the A3 grid it excludes zero for h ≥ [h*] and includes it below [or: at no h | at every h]. The honest (Armstrong–Kolesár) 95% CI is [a, b] at M = [M] and [a', b'] at 2M. CI widths: RBC [w1], honest [w2], against [w0] = 2 × 1.96 × the paper's SE."

Then exactly one verdict sentence, chosen by these pre-declared conditions:

| Condition (A1 = the RBC CI at the MSE-optimal h; A2 = the honest CI at M) | Allowed verdict wording |
|---|---|
| A1 **and** A2 both exclude zero | "confirmed under 2026 RD inference on the same data" / "robust". |
| A1 **and** A2 both include zero, **and** the A3 point estimates change sign within the reported h range | "does not survive 2026 RD inference on the same data" / "no detectable effect on the same data". |
| Anything else | "Significance is bandwidth-dependent under 2026 inference; the point estimate is [stable / attenuates / grows]." |

- **Banned words outside their row:** "does not survive", "overturned", "no effect", "null", "confirmed", "robust", "holds up". Also never write "not distinguishable from zero" as a standalone headline. It may appear only inside the full template.
- **Stable / attenuates / grows** (pre-declared): compare the A1 conventional point estimate with A0 by the paper's method on the same file at bw 0.05. "Stable" if within ±25% of it, "attenuates" if smaller in magnitude by more than 25%, "grows" if larger by more than 25%.
- **When the CI width explains a null.** If A1 or A2 includes zero while the point estimate stays within ±25% of A0, add: "the interval includes zero because it is [w1/w0]× wider than the paper's, not because the estimate moved."
- **The 0.15 panel uses the same template and table.** In Branch N it is filled twice, once per coding, on consecutive lines, and the verdict row is applied to each coding separately. If the two codings get different verdict rows, the card states both, coding by coding.
- Do not spin a wide CI as "no effect". The point estimate and both CIs are always reported.

## 5. Validation gates (in order)

1. **Anchor (gate 1, must pass before anything else).** A0 at 0.08, bw 0.05, with controls must reproduce the replication's **−0.0221 (SE 0.0041), N = 93,899** (`replication/codebase/outputs/table3.json`) to within ±0.0005. That figure is itself within 0.0011 of the paper's −0.021. Also reproduce 0.15, bw 0.05: −0.0073 (0.0035), N = 139,033 (`table4.json`). If gate 1 fails, stop and diagnose: running-variable units (`low_score` is ×1000), integer rounding, and window inclusivity. Do not proceed on a mismatched anchor. This gate runs on the replication's own specification in both branches.
2. **Mean check.** Recidivism mean in bin L = 79 ≈ 0.103 (paper: "Mean (at 0.079)"); bin L = 149 ≈ 0.125. This confirms the paper's mean definition, which the replication's C15 compared against a window mean.
3. **Package versions and settings.** The versions of rdrobust, rddensity and RDHonest, and the rdrobust `masspoints` setting, are recorded in `followup_summary.json`.
4. **Florida structural audit** (B0) passes, and per-year counts are plausible (~25–35k tests per full year; FDLE's 2022 stats report 30,182 tests). Flag any month with zero tests as a gap and keep it as missing. Never interpolate.
5. **No names anywhere persisted.** Before finishing:
   - every per-batch name assertion logged zero Florida-derived hits;
   - a final grep of the study directory, `results/` and the study transcript (if accessible) for the name-field layout pattern the parser uses to find name lines returns zero matches, excluding the parser's own source file and the instruction text;
   - `/tmp/sted/` is deleted, and its absence is checked;
   - the parquet schema check from B0 passes.
   Report counts only.

## 6. Deliverables

- `report.md`, `followup_summary.json` and `result_card.json`, per the contracts in `notes/2026-09-09-followup-studies-handoff.md` §5.
- `results/findings.md`. It opens with the verbatim sentence in §0. The METHOD paragraph follows: "Same public Washington 1999–2007 data and the same thresholds as the paper, re-estimated with current RD inference (a methods re-analysis, not new data on recidivism), plus a check of the design's no-sorting assumption on Florida 2021–2026 breath tests." The B-pre block follows it.
- `results/estimates_headline.csv`: threshold, coding, estimator (A0/A1/A2), h, M (A2 only), estimate, se, ci_low, ci_high, ci_width, mass_points_left, mass_points_right, N_left, N_right, verdict_row.
- `results/bandwidth_curve.csv` and `results/fig_bandwidth_curve.png`: estimate and CI against h, with the paper's two points overlaid.
- `results/sensitivity_015.csv` (A4).
- `results/dofile_coding.md` (Branch D only).
- `results/eras.csv` and `results/fig_eras.png`: estimates by year and era at both thresholds, with the paper's pooled estimate as a reference line.
- `results/density_tests.csv`: state, test, threshold, year or pooled, statistic, p, log-density jump, its CI, MDD.
- `results/florida_heaping.csv`, `results/florida_counts.csv` and `results/fig_florida_hist.png`.
- `results/headline_scalars.json`.
- `workspace/data/fl_tests_deid.parquet` with a data dictionary, and `workspace/data/fl_manifest.csv`. No names, no serials, no agencies, no days or times.

**Result card (at most 5 metrics; each pairs the new number with its baseline on the same data and definition, and names the baseline's file):**
- `headline`: one sentence that opens with "The paper's recidivism headline has not been re-estimated on post-2007 or non-Washington data (no public data allows it);" and continues with the 0.08 verdict-row wording and its point estimate.
- Metric 1: 0.08, A1 RBC CI **and** A2 honest CI on the same line, with the point estimate, against A0 by the paper's method on the same file (−0.0221, `table3.json`) and the paper's −0.021.
- Metric 2: the same for 0.15 (in Branch N, both codings in the one metric), against A0 on the same file (−0.0073, `table4.json`) and the paper's −0.010. The coding status sentence from §4 goes in this metric's note.
- Metric 3: WA rddensity p (2026 test) against the paper's McCrary p, same data (`density_tests.json`).
- Metric 4: "FL vs WA (2026 tests)" at 0.08: the Florida rddensity p and MDD beside the Washington rddensity p and MDD. Its note carries the sentence "Neither outcome bears on the validity of Hansen's Washington estimates."
- Metric 5: "FL vs WA (2026 tests)" at 0.15, in the same form.

## 7. Out of scope

- Any recidivism outcome outside the public Washington file.
- Florida person linkage.
- Utah, FARS and crash-based designs (these are context for 002).
- Court-sanction outcomes.
- The prior-test splits.
- Any fetch other than the Florida STED PDFs. No logins and no outward messages (the do-files and the email to Hansen are human steps).
- Structural deterrence models (002 handles the theory).

## 8. Environment and compute

- CPU only. Python 3 with pandas, statsmodels, `rdrobust`, `rddensity` and `pyarrow`; `pdftotext` (poppler) for parsing. R is allowed for `RDHonest`, `rdrobust`, `rddensity` and the discrete density test; the container R already has fixest and haven per the replication log. No Stata.
- The Washington estimates take seconds each; the full A3 grid takes under 5 minutes. The Florida download is ~0.6 GB; parsing ~537 PDFs takes about 10–20 core-minutes. Total compute is under 2 core-hours.
- **Tool-call limit.** A single shell call is capped at 10 minutes. Keep every call under about 8 minutes; the Florida batching in B0 is sized for that.
- **FOREGROUND RULE:** run every command in the foreground and wait for it to finish. Never background a job (`&`, `nohup`, background-task tools) and never end your turn "to wait". Write `followup_summary.json` incrementally after each batch.

---

# PART II: Follow-up study 002, theory update

**Launcher settings:** `veritas followup <run_dir> --instruction-file <part-II.md> --name theory-update --timeout 10800` (3 hours; compute is under 0.5 core-hours). 002 has no checkpoint mechanism. If it is cut short, it is rerun from scratch as the next number with the instruction unchanged.

## Workspace staging

Same staging as 001. You also need `followup/001-methods-and-transport/results/` (read-only), `shared-data/literature/` (the evidence CSV and PDFs), `shared-data/utah/` and `shared-data/nhtsa/`.

**Fetch nothing new.** The literature values were verified on 2026-10-05 and are staged. **Read `literature/PROVENANCE.md` before using any staged PDF**, because two staged PDFs are not the exact source of their CSV row:
- `finlay_etal_2023_NBER_w31581.pdf` is the 2023 pre-publication version of the 2024 *AER: Insights* paper. The CSV's bounds come from the published abstract. A number read only from this WP is tagged "2023 WP value; published value not verified".
- `sloan_2020_NBER_w26779.pdf` is Sloan's 2020 review chapter, not the 2016 SEJ study. The CSV's −6.6 / −24.5 come from the SEJ abstract. Use the chapter only to confirm the design.

If you believe a staged value is wrong, check it against the staged PDF that actually is its source, and log any correction. Do not substitute numbers from memory.

## 1. The question

Ben Hansen, the paper's author, asked for engagement with newer studies that question whether jail time or DA prosecution reduces reoffending. Hansen (2015) finds that harsher DUI sanctions at the margin *reduce* repeat drunk driving. Since 2018, several high-profile designs find that prosecution, conviction or detention *raise* reoffending, or have no effect.

**Deliverable:** a written-down, quantitative **model of which sanction margins deter**, fitted on the post-2015 evidence **without Hansen's rows**, and then used to predict Hansen's two margins out of sample. The prediction is compared with 001's re-analysed estimates. This is the study's headline test, because it can come out either way. The model must also make falsifiable statements about where the next DUI study should find deterrence and where it should not.

## 2. Inputs

**From 001** (`results/estimates_headline.csv`, `sensitivity_015.csv`, `eras.csv`, and `dofile_coding.md` if it exists): the 0.08 and 0.15 estimates with A1/A2 CIs and the coding status. If 001 is not completed, stop. Do not use the paper's numbers alone. If 001 ran Branch N, carry both 0.15 codings through every 0.15 step below.

**Hansen's sanction jumps** (paper Table 7, court-linked; not public, so cite as paper values from `analyze/paper_claims.json` or the paper):
- At 0.08: fine +$159.7, jail +3.84 days (mean 8.61), any jail +0.112, probation +0.081, alcohol treatment +0.154.
- At 0.15: fine +$73.5, jail +1.40 days, suspension +78.8 days, probation length +25.9.
- Hansen's implied elasticities (C14): −0.22 (0.08), −0.12 (0.15 specific deterrence).

**`literature/sanctions_reoffending_evidence.csv`** (21 rows, 18 columns, sha256 `6c2675ec…7c38`). One row per study-margin, with design, horizon, effect (pp and/or %), direction, and `open_level`:
- FULL = full text read; FULL_intro = abstract and introduction read;
- ABS = abstract only;
- SNIP = search snippet only;
- UNVERIFIED magnitudes are flagged in `notes`.

Studies covered: Hansen ×2, de Figueiredo ×2, Rahman, Sloan et al., Kilmer–Midgette, Gehrsitz, Jansson et al. 2025, Suonpää et al., Agan et al. 2023, Dobbie et al., Leslie–Pope, Rose–Shem-Tov, Bhuller et al., Mueller-Smith–Schnepel, Humphries et al. 2025, Finlay et al. 2024, Huttunen–Kaila–Nix, NHTSA Utah, and Li et al. 2026.

**Utah.** `utah/ccjj_dui_arrests_by_bac_FY2016_2025.csv`: arrests by BAC bin by fiscal year, with the .05 limit effective mid-FY2019. Also `nhtsa/NHTSA_TrafficTech_DOT-HS-813-234_Utah05.pdf`.

## 3. Pre-declared analysis

**T0. Pre-declared codes for Hansen's two margins (fixed now, before any fit).** These are the T2 codes used for the out-of-sample prediction. They may not be changed after the fit.

| Margin | (a) experienced severity/certainty, no record change | (b) record/stigma change | (c) monetary only | incapacitation in window | DUI-specific |
|---|---|---|---|---|---|
| Hansen 0.08 | yes (short jail, suspension, treatment) | partial (conviction status changes only partly at 0.08, since sub-0.08 drivers can still be charged); coded 0.5 | no (fines are bundled, not alone) | no (jail +3.84 days in a 4-year window) | yes |
| Hansen 0.15 | yes (suspension +78.8 days, jail +1.40 days) | no (conviction is already fixed above 0.08) | no | no | yes |

**T1. Harmonise.**
- Express each row as the relative change in reoffending (%) at its stated horizon, and in pp where available.
- Record horizon, population and sanction margin.
- Do not convert units you cannot convert. Leave them NA with a reason.
- Sign convention: the effect of the *harsher* side of the margin. Agan et al. report non-prosecution; convert explicitly and show the arithmetic.

**T2. Code each non-Hansen margin on the T0 dimensions:** (a) experienced severity or certainty of a non-record sanction (licence loss, interlock, short jail, testing); (b) record or stigma change (conviction, felony record, prosecution); (c) monetary-only sanctions; plus incapacitation possible during the outcome window (y/n) and DUI-specific (y/n). Write the coded table to `results/margin_codes.csv` before fitting T3.

**T3. The model, fitted leaving Hansen out.**

> Δ reoffending (%) = α + β_sev·[severity/certainty, no record change] + β_rec·[record change] + β_fine·[monetary only] + γ·[incapacitation in window] + ε

- Hansen's two rows are **excluded from every fit**. The general-deterrence rows (NHTSA Utah, Li et al.) are also excluded from the fit; they enter only T5.
- **Row eligibility, pre-declared now (H8):**
  - The **sign model** (an ordinal model of direction by margin class) uses every non-Hansen specific-deterrence row, whatever its `open_level`.
  - The **weighted regression** uses only rows that (1) have a single numeric relative effect on reoffending, or a pp effect with a baseline stated in the same source, (2) have a verified magnitude: `open_level` FULL, FULL_intro, or ABS where the number appears in the verified abstract, and no UNVERIFIED or snippet flag on the magnitude, and (3) have a reoffending outcome (re-arrest, reconviction, new offence). Rows whose magnitude is UNVERIFIED or SNIP (for example Humphries et al., whose point estimates were not extracted) enter the sign model only. Finlay et al. reports bounds on annual conviction counts with no baseline in the verified abstract, so it enters the sign model only.
  - Print the regression's n and list its rows. **If n < 8, the regression is reported descriptively only** (coefficients shown, no SEs, p-values or significance language), and the sign model carries the inference.
  - Weight by inverse variance where SEs exist; otherwise use equal weights, and disclose that.
- With about 20 heterogeneous rows, this is a structured synthesis, not a meta-analysis. Say so. Do not report pooled p-values as if from a meta-analysis.

**T3-H. HEADLINE TEST: out-of-sample prediction of Hansen's two margins.**
1. Using the leave-Hansen-out fit and the T0 codes, predict the sign of each Hansen margin from the sign model. If the regression is admissible (n ≥ 8), also predict the relative effect (%) with a prediction interval.
2. Express 001's A1 point estimate and its A1 and A2 CIs in relative terms, dividing by the bin means at 0.079 and 0.149 that 001 confirmed in gate 2. Show the arithmetic.
3. Classify each margin, by this pre-declared rule:
   - **consistent**: the predicted sign equals the sign of 001's point estimate, and (if a regression prediction exists) the prediction interval overlaps the A1 CI or the A2 CI;
   - **inconsistent**: the predicted sign is the opposite of 001's point estimate and both A1 and A2 exclude zero; or the regression prediction interval lies entirely outside both A1 and A2;
   - **uninformative**: anything else, including any case where both 001 CIs include zero and the sign model has no clear majority for that margin class.
4. In Branch N, classify the 0.15 margin under each coding separately and report both.
5. This classification is the card's headline test.

The model's reading must still state where Hansen's margins sit. 0.08 bundles conviction, short jail, fines and treatment. 0.15 holds conviction fixed and adds severity, so it is the cleanest "experienced severity, no record change" margin in the literature, which is why its fragility in 001 matters.

A secondary, in-sample fit **including** Hansen's rows may be shown in an appendix, labelled "in-sample, not a test".

**T4. Re-analysed Hansen elasticities, and an upper bound per jail day.**
- Recompute C14's deterrence elasticities with 001's A1 point estimates and CI endpoints, holding Hansen's sanction jumps fixed. Show how much of the "10% more sanctions → 2.3% less drunk driving" survives on the same data under current inference.
- **Jail-day comparison with Jansson et al., labelled as an upper bound.** Compute the per-jail-day effect as (relative effect at the threshold) ÷ (jail-day jump). Label it, everywhere it appears: "an upper bound on the per-day effect, under the assumption that jail is the only active channel". The 0.08 margin bundles conviction, fines, treatment and jail, and Jansson et al. make exactly this exclusion critique of Hansen-style designs.
  - At 0.08: divide by +3.84 days.
  - At 0.15: divide by +1.40 days, and state that the same margin carries +78.8 days of licence suspension. Also show the alternative upper bound that attributes the whole effect to suspension (per suspension-day).
  - Jansson et al.: −80% per month of prison, i.e. about −2.7% per prison day if linear (show the arithmetic). State the population differences: mean BAC, country, sentence range, and their 5-year all-crime outcome vs Hansen's 4-year DUI-test outcome.

**T5. The general-deterrence contrast (Utah 0.05).**
- From the CCJJ series, compute the share of reported-BAC arrests in .05–.07 before (FY2016–2018) and after (FY2020–2025; FY2019 is a transition year).
- **Say plainly that the rise is partly mechanical:** after the law, officers arrest drivers in the .05–.07 range who were not arrestable before. The series is evidence that the new margin binds in enforcement. It is not evidence of deterrence.
- Place the NHTSA and Li et al. crash results beside it as a general-deterrence class.
- State what a Utah arrest-level RD at 0.05 (pending GRAMA) would test, and what the model predicts for it.

**T6. Answer the reader's question directly.** One section, plain language: "Do the new prosecution and jail studies contradict Hansen?" The answer must follow from T3-H and T4, including whatever 001 found about the 0.15 margin's robustness and coding.

**T7. Falsifiable predictions.** At least 3, each tied to a pending-gate dataset (Washington after 2007, Florida with linkage, Utah 0.05, Arkansas), stating the sign and rough magnitude the leave-Hansen-out model predicts.

## 4. Validation gates

1. 001 `result_card.json` has status completed. Read its A1/A2 numbers from disk and cite the file.
2. Every literature number in the synthesis traces to a CSV row or to a staged PDF page that is that row's actual source (see `literature/PROVENANCE.md`). Any value with `open_level` = ABS or SNIP is marked in tables with a dagger and listed in the limitations. Any Finlay number from the staged WP carries its "2023 WP value" tag.
3. The T1 conversion arithmetic is shown in `results/harmonised_effects.csv` (columns: raw value, conversion, result).
4. `results/margin_codes.csv` and the T0 table are written before the T3 fit, and the fit's row list confirms that Hansen's rows are absent.

## 5. Deliverables

- `report.md`, `followup_summary.json` and `result_card.json`.
- `results/model.md`: the equation, the coded margins table, the leave-Hansen-out estimates or sign pattern, the T3-H prediction and classification, the reading, and the predictions. Written as a model, not a list of numbers.
- `results/margin_codes.csv`, `results/harmonised_effects.csv`, `results/hansen_oos_test.csv` (margin, coding, predicted sign, prediction interval if any, 001 relative estimate, A1 CI, A2 CI, classification).
- `results/fig_margins_forest.png`: relative effect by study, grouped and coloured by margin class, with Hansen's 001 estimates highlighted (A1 and A2 CIs) and the leave-Hansen-out predictions overlaid.
- `results/updated_elasticities.csv`, including the labelled upper-bound per-day rows at 0.08 and 0.15.
- `results/utah_bac_shares.csv` and `results/fig_utah_005.png`.
- Headline for the card: one sentence giving the T3-H classification for each Hansen margin, with the key number. Every card metric pairs a value with its baseline on the same definition (for example, the predicted relative effect against 001's relative estimate).

## 6. Out of scope

- New fetches.
- New estimation on microdata beyond reading 001 outputs.
- Formal meta-analytic pooling across non-comparable outcomes.
- Structural estimation of a Becker model with unobserved detection probabilities. Describe it qualitatively if useful.
- Any claim about Florida recidivism.

## 7. Environment and compute

Python (pandas, statsmodels, matplotlib) and `pdftotext` for checking staged PDFs. Compute is under 0.5 core-hours. **FOREGROUND RULE** as in Part I: no backgrounding and no ending the turn to wait.

---

# Pending human gates (not part of either study; tracked for later studies)

Full details are in `recency-research.md` §4. HI-1 and HI-2 above come first. Then, in priority order:

1. Utah GRAMA for arrest-level BAC, enabling an RD at 0.05.
2. WSP RCW 42.56 for Washington tests after 2008.
3. Florida dispositions with a person ID, plus ethics sign-off, enabling a Florida recidivism RD.
4. FDLE STED April 2014 to 2020 (Ch. 119), for a longer Florida series.
5. Arkansas OAT FOIA.
6. MN, TX and MI requests and portal checks.

---

## Revision changelog (2026-10-05)

| Judge item | Change |
|---|---|
| H1 (honest framing) | Study renamed `001-methods-and-transport` (`--name methods-and-transport`; 002 now reads `followup/001-methods-and-transport/results/`). A one-sentence statement at the top of the file and a binding §0 say Panel A re-analyses the same 1999–2007 Washington data with current methods and that the recidivism headline has not been re-estimated on new data. The verbatim first sentence is required in `findings.md`, `report.md` and the card headline. The METHOD paragraph now calls Panel A "a methods re-analysis, not new data on recidivism". Question A was reworded from "do the effects survive" to "how do the estimates read". CCT 2014 predating the paper is noted. |
| H2 (reporting rule) | §4 reporting rule replaced by the judge's joint template, expanded with mass-point counts, the A0 same-file baseline and CI widths against 2 × 1.96 × the paper's SE. The verdict table bans "does not survive / overturned / no effect" unless A1 and A2 both include zero and A3 changes sign, and bans "confirmed / robust" unless both exclude zero. Otherwise the bandwidth-dependent sentence is used, with stable/attenuates/grows pre-defined (±25% of A0). A2 is labelled co-equal; rdrobust's `masspoints` setting and per-side mass-point counts are recorded (also gate 3). The 0.15 panel uses the same template, once per coding in Branch N. Card metrics 1–2 carry A1 and A2 on one line. |
| H3 (do-files, email) | Both are now listed as pre-launch human inputs (HI-1, HI-2), with no agent attempt at either; the prohibitions add "no logins, no outward messages". Part I gets a launch line and a Branch D / Branch N conditional: D quotes the authors' indicator line, makes their coding the headline and the other coding A4; N reports both codings with equal standing and the verbatim "coding unresolved; do-files not obtained". A staging check stops on a launch-line/staging mismatch. A draft email for HI-2 is included; a reply does not change 001's scope. |
| H4 (Florida reading, power, heaping) | New B-pre block, written before any Florida estimate, with the three readings and the sentence "Neither outcome bears on the validity of Hansen's Washington estimates" in findings and on the card. Card pairing changed to "FL vs WA (2026 tests)". B1 adds the log-density jump CI, an MDD for both states, and a pre-declared underpowered rule (FL MDD > 2× WA MDD). B1 adds heaping checks: shares at exactly 0.080 and 0.150, last-digit tests overall and per instrument pseudonym, and a donut re-run. |
| H5 (PII) | (a) `florida/PROVENANCE.md` rewritten: the STED sample row is removed, the file is documented as deliberately not staged and deleted, and the format is documented from field structure only. (b) The name-bearing `STED_202603_868-997.pdf` was deleted from the corpus tree, along with a scratchpad copy and a scratchpad `pdftotext` dump of it. (c) Raw PDFs go only to `/tmp/sted/raw/`, outside the workspace, study directory and transcript, and are deleted per batch. (d) The 3-page spot-check is replaced by a structural audit that prints no page text (two-extractor agreement rates, field counts, value ranges, one record per page, no string column). A per-batch whole-word name-token assertion covers the study tree and the transcript and reports counts and paths only; gate 5 adds a final layout-pattern grep and checks that `/tmp/sted/` is gone. A hard prohibition bans printing raw page text. (e) Only year-month is kept. Serial and agency are dropped from the parquet; the serial is replaced by an in-memory pseudonym whose seed is never saved, so no restricted side file is needed. |
| H6 (execution) | B0 specifies batches of about 50 files per foreground call (about 11 calls), each kept under about 8 minutes: download, parse, append, assert, delete, checkpoint. A manifest drives skip-if-parsed resume. §8 states the 10-minute tool-call cap. |
| H7 (circular placement) | T3 is now fitted leaving Hansen's rows out. A new T3-H predicts the sign (and the size, if the regression is admissible) of both Hansen margins from T0 codes fixed in the spec, compares the prediction with 001's A1/A2 in relative terms, and classifies each margin as consistent, inconsistent or uninformative by a pre-declared rule. T3-H is the card's headline test; an in-sample fit is allowed only in an appendix, labelled "not a test". Gate 4 checks that the codes are written before the fit and that Hansen's rows are absent. |
| H8 (row eligibility) | Pre-declared rule: the sign model takes all non-Hansen specific-deterrence rows; the regression takes only rows with a single verified numeric relative reoffending effect. UNVERIFIED or SNIP magnitudes (Humphries et al.) and Finlay's conviction-count bounds go to the sign model only. The regression's n is printed with its row list; if n < 8 it is descriptive only. |
| H9a (Finlay) | The superseded `finlay_etal_2022_DRF_WP.pdf` was removed from `literature/`. The published 2024 full text returns 403 to scripted fetches, so the NBER w31581 (Aug 2023) version of the same paper is staged instead (sha256 `ab04b342…de7d`). The published abstract was read live on aeaweb.org: it confirms the CSV bounds (−0.001 to 0.01 annual convictions), so the row's "snippet, UNVERIFIED" note was replaced by an ABS-verified note. Any WP-only number carries the tag "2023 WP value; published value not verified". `literature/PROVENANCE.md` and the CSV sha256 were updated. |
| H9b (Sloan) | Checked: w26779 is Sloan's 2020 review chapter "Drinking and Driving", not the 2016 study. It describes the design (pp. 13–14) but reports none of the −6.6 / −24.5 numbers. Those numbers were re-verified from the SEJ 2016 abstract (Wiley, doi 10.1002/soej.12159). The CSV row's note and `literature/PROVENANCE.md` now say which source holds the values; the spec tells the agent to use the chapter only for design. |
| H10 (jail-day upper bound) | T4 labels the per-jail-day comparison "an upper bound on the per-day effect, under the assumption that jail is the only active channel", adds the comparison at 0.15 (+1.40 jail days beside +78.8 suspension days, with an alternative per-suspension-day bound), and shows the Jansson per-day arithmetic. |
| H11 (Utah) | T5 now states that the post-2019 rise in the .05–.07 arrest share is partly mechanical and is evidence the margin binds in enforcement, not evidence of deterrence. |
| Cross-cutting 1 | Explicit `--timeout` for both parts (21600 s for 001, 10800 s for 002). 001 names its continuation study (`methods-and-transport-cont`, resuming from the manifest); 002 states that it has no checkpoint and is rerun whole. |
| Cross-cutting 2 | Card metrics pair the A1/A2 headline with A0 by the paper's method on the same public file, as well as the paper value. Florida is paired with Washington under the same 2026 test. 002's card pairs predictions with 001 estimates on the same relative scale. |
| Unchallenged gates | Gate 1 (anchor ±0.0005), gate 2 (mean check), the Florida count plausibility check, the ban on Florida linkage and recidivism, the prep-diagnostics embargo, and "no new fetches" for 002 are unchanged. FARS is no longer staged for 001, so the PROVENANCE check no longer meets a missing optional zip. |