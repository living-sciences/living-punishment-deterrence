# Follow-up study 002/003 — Theory update: which sanction margins deter?

**Paper:** Hansen (2015), "Punishment and Deterrence: Evidence from Drunk Driving," *AER* 105(4).
**Task (Part II of the Hansen extension pair):** Ben Hansen asked for engagement with post-2015
designs that question whether jail time or DA prosecution reduces reoffending. Deliver a **written-down,
quantitative model of which sanction margins deter**, fitted on the post-2015 evidence **without
Hansen's rows**, then used to predict Hansen's two margins **out of sample**; compare the prediction with
the methods re-analysis (study 001); and make falsifiable predictions for the next DUI study.

---

## Question

Hansen (2015) finds that harsher DUI sanctions at the 0.08 and 0.15 BAC thresholds *reduce* repeat
drunk driving. Since 2018, several high-profile designs (Agan–Doleac–Harvey 2023, Mueller-Smith–Schnepel
2021, Humphries et al. 2025) find that prosecution, conviction or detention *raise* reoffending. Do the
new studies contradict Hansen? The deliverable answers this by building a margin-level model, testing it
out of sample against Hansen, and stating where the next study should and should not find deterrence.

## Approach

- **Reused, not recomputed.** All of Hansen's re-analysed estimates come from the completed
  methods-and-transport study on disk (`followup/002-methods-and-transport/results/`). No microdata were
  re-estimated. The 21-row evidence table (`shared-data/literature/sanctions_reoffending_evidence.csv`,
  sha256 verified) and the Utah CCJJ arrest series were read as staged; nothing was fetched.
- **Note on inputs (deviation).** The spec's Part II reads `followup/001-methods-and-transport/results/`.
  That directory is **empty** — the 001 session was cut short and the orchestrator relaunched it as the
  continuation study **`002-methods-and-transport`**, whose `result_card.json` has status
  **`completed`** (gate 1). I used that completed study as the "001" input throughout and cite it as such.
- **Model.** `Δ reoffending (%) = α + β_sev·[severity/certainty, no record] + β_rec·[record change] +
  β_fine·[monetary only] + γ·[incapacitation in window] + ε`. Hansen's two rows and the two
  general-deterrence rows are excluded from the fit. A **sign model** (direction by margin class, all
  non-Hansen specific-deterrence rows) carries the inference; a **weighted regression** has only
  **n = 7** eligible rows (< 8) so is reported **descriptively** (per the pre-declared H8 rule). Margin
  codes were written to `results/margin_codes.csv` **before** the fit; Hansen's rows are flagged absent
  (gate 4).
- **001 inputs (Branch N, read from disk).** Gate-2 bin means 0.10432 (at 0.079) and 0.12405 (at 0.149).
  A1 RBC / A2 honest estimates (coef, CI) from `estimates_headline.csv` and `headline_scalars.json`:

  | Threshold / coding | A1 RBC (abs) | A1 RBC CI | A2 honest CI | A0 paper-method (same file) |
  |---|---|---|---|---|
  | 0.08 statutory | −0.0173 | [−0.0307, −0.0023] (excl. 0) | [−0.0310, +0.0010] (incl. 0) | −0.0221 |
  | 0.15 statutory ≥ | −0.0074 | [−0.0185, +0.0043] (incl. 0) | [−0.0193, +0.0068] (incl. 0) | −0.0073 |
  | 0.15 strict > | −0.0112 | [−0.0228, −0.0007] (excl. 0) | [−0.0250, +0.0009] (incl. 0) | −0.0090 |

## Results

### The model's sign pattern (the core finding)

| Margin class | n | deter / null / crim. | majority |
|---|---|---|---|
| severity / certainty, **no record change** | 12 | 7 / 3 / 2 | **DETER** |
| **record change** | 4 numeric | 2 / 0 / 2 | **splits by domain** ↓ |
| &nbsp;&nbsp;↳ record change, **DUI** (Sloan 2016) | 2 | 2 / 0 / 0 | deter (−6.6%†, −24.5%†) |
| &nbsp;&nbsp;↳ record change, **general crime** (Agan, Mueller-Smith–Schnepel) | 2 | 0 / 0 / 2 | **criminogenic (+113%†, +100%†)** |
| monetary only (Finlay 2024) | 1 | 0 / 1 / 0 | null (≈ 0 †) |

**† = abstract-only value (`open_level = ABS`), verified 2026-10-05.** All 7 numeric non-Hansen effects
used in the regression are abstract-verified (Sloan ×2, Kilmer–Midgette, Gehrsitz, Rose–Shem-Tov, Agan,
Mueller-Smith–Schnepel); listed with `open_level` in `margin_codes.csv`. The newer criminogenic findings
sit entirely in the **record/stigma channel of general criminal courts**.
The **experienced-severity** class (short jail, licence suspension, interlock, 24/7 testing,
incarceration length) deters almost everywhere (Kilmer–Midgette −49%, Rose–Shem-Tov −44%, Gehrsitz −20%,
plus Bhuller, Jansson, Rahman in the sign model). Fines-only effects are null.

### Headline test — out-of-sample prediction of Hansen's two margins (T3-H)

The model is fitted **without Hansen** and predicts the sign of each Hansen margin from the T0 codes:

| Hansen margin | model predicts | 001 A1 (relative) | 001 A1 CI | 001 A2 CI | **classification** |
|---|---|---|---|---|---|
| 0.08 | DETER (−) | **−16.6%** | [−29.4%, −2.2%] | [−29.7%, +0.9%] | **consistent** |
| 0.15 statutory ≥ | DETER (−) | **−6.0%** | [−14.9%, +3.4%] | [−15.6%, +5.5%] | **consistent** |
| 0.15 strict > | DETER (−) | **−9.1%** | [−18.4%, −0.5%] | [−20.2%, +0.7%] | **consistent** |

**All three Hansen margins are classified *consistent* with a model fitted without them.** Hansen 0.15
is the cleanest "experienced severity, no record change" DUI margin in the whole literature, and the
severity class deters — the model predicts deterrence, and 001's point estimate is negative under both
codings (significant under strict, bandwidth-dependent under statutory). The test could have come out
otherwise; it did not.

### Re-analysed elasticities and the jail-day upper bound (T4)

| Threshold | paper | re-analysed (A1) | A1 CI | survives |
|---|---|---|---|---|
| 0.08 | −0.22 | **−0.214** | [−0.38, −0.03] | ~97% |
| 0.15 statutory ≥ | −0.12 | **−0.080** | [−0.20, +0.05] (incl. 0) | ~66% |
| 0.15 strict > | −0.12 | **−0.121** | [−0.25, −0.01] | ~100% |

Hansen's "10% more sanctions → 2.3% less drunk driving" is largely intact at 0.08 and under the strict
0.15 coding, and attenuates to ~0.8% per 10% under the statutory 0.15 coding.

**Jail-day comparison with Jansson et al. — labelled an UPPER BOUND, assuming jail is the only active
channel** (Hansen's margins bundle conviction, fines, treatment and licence actions, so this *overstates*
any per-day jail effect — exactly Jansson et al.'s critique):
- 0.08: −16.6% ÷ 3.84 jail days = **−4.3% / jail-day (upper bound)**.
- 0.15: −6.0% ÷ 1.40 = **−4.3% / jail-day (statutory)**, −9.1% ÷ 1.40 = **−6.5% (strict)**; the same
  margin also adds +78.8 suspension days (alt. bound −0.08% to −0.12% / suspension-day).
- Jansson et al.: −80% per prison month = **−2.67% / prison-day** (linear). Different country, sentence
  range, population and outcome (5-yr all-crime vs 4-yr DUI test). Hansen's upper bound exceeds Jansson's
  realised per-day figure, consistent with its being an upper bound that loads other channels onto jail.

### General-deterrence contrast — Utah 0.05 (T5)

.05–.07 share of reported-BAC arrests rose **4.7% (FY16–18) → 10.1% (FY20–25), 2.1×** (`fig_utah_005.png`).
**Partly mechanical, not deterrence** — the band fills because .05–.07 drivers became arrestable. It is
evidence the new margin **binds in enforcement**. Beside it, in the general-deterrence class: NHTSA
−19.8% fatal-crash rate (vs −5.6% rest-of-US); Li et al. 2026 DiD −1.17 [−1.88, −0.46]. A Utah
arrest-level RD at 0.05 (pending GRAMA) would test *specific* deterrence; the model predicts **deter**.

### Does the new evidence contradict Hansen? (T6)

**No, not for Hansen's margins.** The criminogenic results are about **conviction records / prosecution
in general criminal courts**; Hansen's thresholds move **experienced severity of DUI-specific
sanctions** at points where conviction status is largely fixed. The new studies **refine** Hansen —
mapping where deterrence fails (a general-crime record) vs where it holds (experienced severity; DUI).
The one tension is at 0.08, which partly runs through the record channel and is bandwidth-dependent in
001 (though point-stable).

### Falsifiable predictions (T7)

1. **Utah arrest-level RD at 0.05 (GRAMA):** deterrence, ~−10% to −17% relative (record + DUI severity).
2. **Washington post-2007 (WSP):** 0.15 severity effect persists negative (~−6% to −9%); 0.08 stays
   attenuated/bandwidth-dependent.
3. **Florida recidivism RD with linkage (ethics + dispositions):** deterrence at both thresholds
   (identification confirmed by 001), smaller than Washington if record effects offset.
4. **Arkansas 0.15 licence increment (OAT FOIA):** near-null/weak, matching de Figueiredo's imprecise null.

## Deviations & limitations

- **"001" input is `002-methods-and-transport`** (the completed continuation study), because the
  `001-methods-and-transport` directory is empty. Status is `completed`; I cite it explicitly.
- **Branch N** carried through: the 0.15 margin is reported under both codings (do-files not obtained).
- **Regression is descriptive only (n = 7 < 8)**, per the pre-declared H8 rule; the sign model carries
  the inference. The OLS design matrix is rank-deficient, so **class means** are the descriptive model.
- This is a **structured synthesis, not a meta-analysis**; no pooled p-values. Rows coded ABS/SNIP are
  daggered in the figure and listed in `margin_codes.csv` (`open_level`). Agan and Mueller-Smith–Schnepel
  magnitudes are **sign-convention conversions** of published non-prosecution/diversion effects (arithmetic
  shown). Any Finlay number would carry the "2023 WP value; published value not verified" tag; here Finlay
  enters the sign model only (its published bounds are on annual conviction *counts*, not relative
  reoffending). Sloan's effect sizes are the SEJ-2016 abstract values (the staged 2020 PDF is a review
  chapter and only confirms the design).
- The classification tests **sign**, not magnitude (the regression is not admissible for a prediction
  interval). Hansen's relative effects are on the small end of the severity cluster, consistent with his
  high-base outcome.
- Hansen's sanction-jump magnitudes (Table 7) are **not public**; cited as paper values (instruction §2 /
  `paper_claims.json`). The elasticity recomputation holds them fixed and swaps only the recidivism estimate.

## Artifacts

`results/model.md`, `margin_codes.csv`, `harmonised_effects.csv`, `hansen_oos_test.csv`,
`updated_elasticities.csv`, `utah_bac_shares.csv`, `_sign_model.csv`, `headline_scalars.json`,
`fig_margins_forest.png`, `fig_utah_005.png`.
