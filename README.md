# Living paper: Punishment and Deterrence (Hansen 2015)

This repository holds the working files behind the living-paper page
**https://livingscience.ai/econ/living-punishment-deterrence**: an AI-agent replication of the
paper, plus the methods-and-transport and theory-update extension studies built on it.

**Paper.** Hansen, Benjamin. 2015. "Punishment and Deterrence: Evidence from Drunk Driving."
*American Economic Review* 105 (4): 1581–1617. DOI: [10.1257/aer.20130189](https://doi.org/10.1257/aer.20130189).

## What is in the repository

| Path | What it is |
|---|---|
| `replication/` | The replication run: a from-scratch R reimplementation of the paper's local-linear regression-discontinuity design (`codebase/*.R`), its outputs (`codebase/outputs/`), the run's evidence summary and the installed-package list. |
| `followup/002-methods-and-transport/` | Extension study: re-estimates the recidivism discontinuities on the same Washington file under current RD inference (robust bias-corrected and honest CIs, bandwidth curves, density tests, eras), and transports the no-sorting/density checks to Florida breath-test records (FDLE STED, 2021–2026). |
| `followup/003-theory-update/` | Extension study: fits a model of which sanction margins deter on the post-2015 literature *without* Hansen, then checks Hansen's thresholds against its out-of-sample prediction (plus a Utah BAC-share series). |
| `followup/004-gate-conformance/` | Corrective study that **supersedes 002 and 003**: deduplicates the Florida ingest (five STED files had been ingested twice), corrects the heaping reading, and restates every flagged number and claim honestly. |

**Which numbers to cite.** The published numbers on the living page come from
`004-gate-conformance`. Studies 002 and 003 are kept so the full trail is visible, but where they
differ from 004 (Florida counts and p-values, the heaping caveat, the 003 appendix claim, the
sign-model presentation), 004 is the one that stands. Inside 003 and 004, "001" refers to the
methods-and-transport study published here as 002: the original 001 launch was cut short before
producing anything and was relaunched as 002, so it is not included.

Each study directory contains its `instruction.md` (the specification it ran under), `workspace/`
(the code it wrote and its derived data), `results/` (tables, figures, `findings.md`), `report.md`,
`result_card.json` and `followup_summary.json`.

## Data

### Washington (the paper's setting)

`replication/codebase/data/hansen_dwi.dta` (9.4 MB, sha256 `08158875811feeac8b4b92604efc1a90f5f2b8181144c2880c0f4fb60743ecd1`)
is the **public** extract distributed with Scott Cunningham's *Causal Inference: The Mixtape*
(`github.com/scunning1975/mixtape`, file `hansen_dwi.dta`), a subset Hansen provided for teaching.
It is de-identified (no names or IDs). See `replication/codebase/data/DATA_README.md`.

It covers 214,558 of the paper's 512,964 Washington breath tests (1999–2007), with the two BAC
readings, the running variable, sex, race, age, accident-at-scene and the four-year recidivism
outcome. It does **not** contain county, the prior-test count or prior-offense flag, the PBT
indicator, recidivism-type splits, alternate windows, court outcomes, other-crime outcomes or a
person ID. Results that need those (columns 2–3 of Tables 3 and 4, the Prior/PBT rows of Table 2,
Figure 2's Prior/PBT panels, Figure 3 panels B and C, Tables 7 and 9) require the **restricted
Washington administrative records**, which are not public. **This repository contains no
restricted data.**

The authors' code deposit, openICPSR project 112907 (doi:10.3886/E112907V1), is code-only (Stata
do-files, no data) and sits behind an openICPSR login and terms acceptance. It was not obtained
for this work and is **not included**; the replication is a from-scratch reimplementation.

### Florida (extension study 002, corrected in 004)

The Florida analysis uses FDLE's publicly posted Subject Test Electronic Data (STED) reports.
Those PDFs carry subject surnames and officer names, so they were parsed in memory and discarded
file by file; no STED PDF or page text is in this repository. What ships is the de-identified
extract only:

- `workspace/data/fl_tests_deid.parquet` (and, in 002, the per-batch `_shards/`): one row per test
  with year-month, violation code, gender, the two BrAC readings, refusal and volume-not-met flags,
  the number of valid samples, and a random instrument pseudonym (the raw instrument serial was
  never stored and the pseudonym seed was discarded).
- `workspace/data/fl_analysis.csv`: the two-sample DUI analysis sample, numeric apart from year-month.
- `workspace/data/fl_manifest.csv`: the public FDLE file URLs, sha256s and per-file record counts.
- `workspace/data/DATA_DICTIONARY.json`: the fields kept and the fields dropped at parse time.

None of these files contain a name, instrument serial, agency, day-of-month or time-of-day field.
The 002 copies include the five duplicated files; the 004 copies are deduplicated (162,875 tests,
115,262 two-sample DUI) and are the ones the published numbers use.

### Staged inputs not included

The studies read a staging mirror (`shared-data/`, not shipped) holding: the FDLE STED index page,
an FDLE memo and 2022 statistics sheet; Utah CCJJ DUI annual reports and the derived
`ccjj_dui_arrests_by_bac_FY2016_2025.csv`; an NHTSA Traffic Tech note; and a hand-compiled
literature table `sanctions_reoffending_evidence.csv` with the source papers. All are public, and
each study's report records the paths and sha256s it used. 004 also read an internal provenance
audit, which is not included. Third-party software environments are also omitted; see
`LARGE_FILES_OMITTED.md`.

## Terms

Files derived from the authors' replication materials, including the Mixtape extract of Hansen's
data, remain under the authors' (and distributor's) terms. FDLE STED data are public records of
the State of Florida; please do not attempt to re-identify anyone from the derived files.

## Reproducing

R 4.6 with `haven`, `rdrobust`, `rdd`, `rddensity`, `lpdensity`, `RDHonest`, `fixest`, `sandwich`,
`dplyr`, `ggplot2` (exact versions in `replication/installed_packages.txt`,
`replication/evidence_summary.json` and each study's `followup_summary.json`), and Python 3.12
with `pandas`, `pyarrow` and `matplotlib`. Run the scripts in `replication/codebase/` from that
directory; the follow-up scripts expect the replication outputs and the staged inputs at the
paths named in their headers.
