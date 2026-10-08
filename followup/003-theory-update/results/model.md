# A model of which sanction margins deter — fitted without Hansen, then used to predict Hansen

**Study 002/003, theory-update.** Author requester: Ben Hansen, who asked for engagement with
post-2015 designs that question whether jail or prosecution reduces reoffending.

All of Hansen's re-analysed estimates are read from the completed methods-and-transport study on
disk (`followup/002-methods-and-transport/results/`; the `001-` directory was cut short and the
orchestrator relaunched it as the continuation study `002-methods-and-transport`, which carries
`result_card.json` status `completed`). That study ran **Branch N** (openICPSR do-files not obtained),
so the 0.15 margin is carried through under **both** codings (statutory ≥ 0.150 and strict > 0.150).

---

## 1. The equation

> Δ reoffending (%) = α + β_sev·[severity/certainty, no record change] + β_rec·[record change]
>                     + β_fine·[monetary only] + γ·[incapacitation in window] + ε

This is a **structured synthesis of ~20 heterogeneous study-margins, not a meta-analysis.** No pooled
p-values are reported. Hansen's two rows are **excluded from every fit**; the two general-deterrence
rows (NHTSA Utah, Li et al. 2026) are also excluded from the fit and used only in the general-deterrence
contrast (T5).

Two objects are estimated:
- a **sign model** — the direction (deter −1 / null 0 / criminogenic +1) by margin class, using
  **all** non-Hansen specific-deterrence rows regardless of `open_level`;
- a **weighted regression** — using only rows with a single verified numeric relative reoffending
  effect. There are **n = 7** such rows (< 8), so per the pre-declared rule (H8) the regression is
  reported **descriptively only** (coefficients/class means, no SEs, no p-values), and the **sign
  model carries the inference.** Weights are equal (SEs are not in most abstracts); this is disclosed.

---

## 2. The coded margins (T0 + T2, written before the fit)

`margin_codes.csv` was written to disk **before** any fit; its Hansen rows are flagged
`reg_eligible = False` and `direction_sign = NaN` (gate 4 confirms Hansen is absent from the fit).

### T0 — Hansen's two margins (codes fixed before the fit, used for the out-of-sample prediction)

| Margin | severity, no record | record change | monetary only | incap. in window | DUI-specific |
|---|---|---|---|---|---|
| Hansen 0.08 | yes (short jail, suspension, treatment) | **0.5** (conviction only partly changes at 0.08) | no (fines bundled) | no (+3.84 jail days in a 4-yr window) | yes |
| Hansen 0.15 | yes (suspension +78.8 d, jail +1.40 d) | **no** (conviction already fixed above 0.08) | no | no | yes |

Hansen 0.15 is the **cleanest "experienced severity, no record change" DUI margin in the literature** —
which is exactly why its fragility in the methods re-analysis (001) matters.

### T2 — the non-Hansen evidence, coded (full table in `margin_codes.csv`)

Regression-eligible rows (single verified numeric relative reoffending effect), by class:

| Margin class | Studies (relative effect of the harsher side) | class mean |
|---|---|---|
| **severity / certainty, no record** | Kilmer–Midgette 2020 −49%†, Rose–Shem-Tov 2021 −44%†, Gehrsitz 2017 −20%† | **−37.7%** |
| **record change — DUI-specific** | Sloan 2016 prosecution −6.6%†, conviction\|prosecuted −24.5%† | **−15.6%** |
| **record change — general crime** | Agan 2023 prosecution **+113%**†, Mueller-Smith–Schnepel 2021 conviction **+100%**† | **+106.5%** |
| **monetary only** | Finlay 2024 fines/fees ≈ 0 † | **≈ 0** |

**† = value from the study's abstract only (`open_level = ABS`), verified 2026-10-05.** Every numeric
non-Hansen effect used in the regression is abstract-verified: Sloan (×2), Kilmer–Midgette, Gehrsitz,
Rose–Shem-Tov, Agan, Mueller-Smith–Schnepel. The two Hansen rows and de Figueiredo are `FULL`;
Jansson and Humphries are `FULL_intro`. See `margin_codes.csv` (`open_level`, `dagger_abs_snip`).

Sign-convention conversions (shown in `harmonised_effects.csv`):
- **Agan 2023**: reports −53% for *non*-prosecution. Harsher side = prosecution:
  1/(1−0.53) − 1 = **+113%** (prosecution ~doubles new complaints).
- **Mueller-Smith–Schnepel 2021**: diversion −50%. Harsher side = conviction record:
  1/(1−0.50) − 1 = **+100%** ("conviction record roughly doubles reoffending").

Sign-model-only rows (no verified single relative number): de Figueiredo 2015 (×2), Rahman 2022,
Jansson et al. 2025 (per-month dose slope), Suonpää 2021, Dobbie et al. 2018, Leslie–Pope 2017,
Bhuller et al. 2020, Humphries et al. 2025 (UNVERIFIED), Finlay 2024, Huttunen–Kaila–Nix.

---

## 3. What the model says (the sign pattern)

| Margin class | n (all rows) | deter | null | criminogenic | **majority** |
|---|---|---|---|---|---|
| severity / certainty, no record | 12 | 7 | 3 | 2 | **DETER** |
| record change | 4 numeric | 2 | 0 | 2 | **splits by domain** |
| monetary only | 1 | 0 | 1 | 0 | null |

**The central result is the domain split inside the record-change class.** Record/stigma change is
criminogenic for **general crime** (Agan +113%, Mueller-Smith–Schnepel +100%, Humphries large lasting
increase) but deterrent for **DUI** (Sloan prosecution −6.6%, conviction −24.5%). The severity /
certainty / experienced-punishment class — short jail, licence suspension, interlock, 24/7 testing,
incarceration length — **deters essentially everywhere** (Kilmer–Midgette, Gehrsitz, Rose–Shem-Tov,
Bhuller, Jansson, Rahman), with the nulls confined to pretrial-detention and imprecise short-window
designs. Fines-only effects are null (Finlay).

The descriptive regression design matrix is rank-deficient at n = 7 (each eligible row loads on exactly
one class dummy), so the **class means above are the descriptive model**; the raw OLS coefficients
(α ≈ +3.7, β_sev ≈ −38, β_rec ≈ +42, γ ≈ −9.5) are not uniquely identified and are reported only as a
footnote, not as inference.

**So the model's reading of the newer "prosecution/jail raises reoffending" studies:** they identify a
**record/stigma channel in general criminal courts** (a felony or misdemeanor record creates
employment/stigma traps), which is a *different margin* from the ones Hansen's RD moves.

---

## 4. Headline test — out-of-sample prediction of Hansen's two margins (T3-H)

Prediction from the sign model + the T0 codes (fixed before the fit). Hansen's A1/A2 estimates are
expressed in relative terms by dividing by the bin means **001 confirmed in gate 2** (mean at
0.079 = 0.10432, at 0.149 = 0.12405). Full arithmetic in `hansen_oos_test.csv`.

| Hansen margin | predicted sign | 001 A1 (relative) | 001 A1 CI | 001 A2 CI | **classification** |
|---|---|---|---|---|---|
| 0.08 | **DETER (−)** | −16.6% | [−29.4%, −2.2%] | [−29.7%, +0.9%] | **consistent** |
| 0.15 statutory ≥ | **DETER (−)** | −6.0% | [−14.9%, +3.4%] | [−15.6%, +5.5%] | **consistent** |
| 0.15 strict > | **DETER (−)** | −9.1% | [−18.4%, −0.5%] | [−20.2%, +0.7%] | **consistent** |

Classification rule (pre-declared): **consistent** = predicted sign equals the sign of 001's point
estimate (no regression prediction interval exists, since n < 8, so that clause is vacuous).

- **0.08** — Hansen bundles conviction (partial), short jail, fines and treatment. Severity class →
  deter; the DUI-specific record evidence (Sloan) → deter. Both point to **deter**; 001's point is
  −16.6% (A1 CI excludes zero, A2 includes it). **Consistent.**
- **0.15** — pure experienced-severity, no record change, DUI-specific → severity class majority
  **deter**; 001's point is negative under both codings (strict A1 CI excludes zero; statutory
  bandwidth-dependent). **Consistent under both codings.**

**All three Hansen margins are classified *consistent* with a model fitted without them.** The
prediction could have failed: had the severity-class evidence been mixed, or had 001's point estimates
come out positive, the margins would have been *inconsistent* or *uninformative*.

The prediction is on **sign**, not magnitude. Hansen's relative effects (−6% to −17%) sit on the
*small* end of the severity cluster (−20% to −49%), consistent with his high-base outcome (a 4-year
any-breath-test indicator on all tested drivers, base ~10–12%) versus the arrestee/defendant bases in
the comparison studies.

---

## 5. Re-analysed Hansen elasticities and a labelled jail-day upper bound (T4)

Holding Hansen's sanction jumps fixed (the sanction scale is the paper's own recid%÷elasticity:
77.3% at 0.08, 75% at 0.15) and swapping in 001's A1 estimate (`updated_elasticities.csv`):

| Threshold | paper elasticity | re-analysed (A1) | A1 CI | survives |
|---|---|---|---|---|
| 0.08 | −0.22 | **−0.214** | [−0.38, −0.028] | ~97% |
| 0.15 statutory ≥ | −0.12 | **−0.080** | [−0.199, +0.046] (incl. 0) | ~66% |
| 0.15 strict > | −0.12 | **−0.121** | [−0.245, −0.007] | ~100% |

So the paper's "a 10% increase in sanctions is associated with a 2.3% decline in drunk driving" is
**largely intact at 0.08 (~2.1% per 10%) and under the strict 0.15 coding (~1.2% per 10%), but
attenuates to ~0.8% per 10% under the statutory 0.15 coding** — i.e. the headline elasticity survives
2026 inference on the same data except where the 0.15 statutory coding makes the estimate smaller and
its interval cover zero.

**Jail-day comparison with Jansson et al. — an UPPER BOUND, under the assumption that jail is the only
active channel** (Hansen's margins bundle conviction, fines, treatment and licence actions, so dividing
the *whole* effect by jail days *overstates* any per-day jail effect; Jansson et al. make exactly this
exclusion-restriction critique of Hansen-style designs):

- **0.08**: −16.6% ÷ 3.84 jail days = **−4.3% per jail day (upper bound).**
- **0.15**: −6.0% ÷ 1.40 jail days = **−4.3% per jail day (upper bound, statutory)** / −9.1% ÷ 1.40 =
  **−6.5% (strict)**. The same margin also carries **+78.8 days of licence suspension**; attributing
  the whole effect to suspension gives an alternative **−0.076% to −0.115% per suspension-day.**
- **Jansson et al.**: −80% per *month* of prison ⇒ −80%/30 = **−2.67% per prison day** (if linear).
  Populations differ sharply: Sweden vs Washington; DUI convicts with prison sentences of days-to-months
  vs all tested drivers with ~3.8 added jail days; a 5-year **all-crime** outcome vs Hansen's 4-year
  **DUI-test** outcome. Hansen's upper-bound per-day figure (−4.3%) exceeds Jansson's realised per-day
  figure (−2.67%) — consistent with Hansen's being an *upper bound* that loads other channels onto jail.

---

## 6. General-deterrence contrast — Utah's 0.05 per se limit (T5)

From the CCJJ arrest series (`utah_bac_shares.csv`), the share of reported-BAC DUI arrests in the
.05–.07 band rose from **4.7% (FY2016–2018, pre-law)** to **10.1% (FY2020–2025, post-law)** — a
**2.1× increase** (FY2019 is the transition year; the .05 limit took effect 2018-12-30).

**This rise is partly mechanical, not deterrence:** after the law, officers can arrest .05–.07 drivers
who were not arrestable before, so the band mechanically fills. The series is evidence that the **new
margin binds in enforcement**, not that it deters. Placed in the **general-deterrence class** beside it:
NHTSA (2022) reports Utah's fatal-crash rate fell **−19.8%** vs **−5.6%** in the rest of the US; Li et
al. (2026) report a county DiD of **−1.17** alcohol-involved fatalities (95% CI [−1.88, −0.46]). These
are *general* deterrence (the threshold deters the population), categorically distinct from Hansen's
*specific* deterrence (sanctions deter the person sanctioned).

A **Utah arrest-level RD at 0.05** (pending a GRAMA request) would test specific deterrence at the new
threshold. The model predicts **deter** there: 0.05 adds a conviction + the DUI sanction bundle at a new
per-se line — structurally Hansen's 0.08 margin (record + experienced severity, DUI-specific).

---

## 7. Does the new evidence contradict Hansen? (T6)

**No — not for the margins Hansen's design identifies.** The criminogenic findings that motivated the
question (Agan et al. 2023, Mueller-Smith–Schnepel 2021, Humphries et al. 2025) are about **conviction
records and prosecution in general criminal courts**, where a lasting record imposes employment and
stigma costs that *raise* later offending. Hansen's thresholds move **experienced severity of
DUI-specific sanctions** — jail days, licence suspension, treatment — at points where conviction status
is largely already determined (entirely so at 0.15). The experienced-severity class deters almost
uniformly in the post-2015 evidence, and the one DUI study of the record margin itself (Sloan 2016)
*also* finds deterrence. So the new studies **refine rather than refute** Hansen: they map **where
deterrence fails** (adding a criminal record for general crime) versus **where it holds** (experienced
severity; DUI).

The single genuine point of tension is at **0.08**, which does run partly through the conviction/record
channel (coded 0.5). If that channel behaved like the general-crime record channel, it would *attenuate*
Hansen's 0.08 effect — and 001 does find 0.08 bandwidth-dependent (honest CI includes zero), though the
point estimate is stable (−22% vs the paper-method estimate on the same file). The cleaner 0.15 severity
margin is where the model and Hansen agree most squarely, and it is negative under both codings.

---

## 8. Falsifiable predictions (T7), each tied to a pending-gate dataset

1. **Utah arrest-level RD at 0.05 (pending GRAMA).** The model predicts **deterrence** (record + DUI
   severity bundle, like Hansen's 0.08): a negative recidivism discontinuity at 0.05, relative magnitude
   roughly **−10% to −17%** (Hansen-0.08 scale). A null or positive discontinuity would falsify it.
2. **Washington tests after 2007 (pending WSP RCW 42.56).** The model predicts the **0.15
   experienced-severity effect persists negative (~−6% to −9% relative)**, while **0.08 stays
   bandwidth-dependent / attenuated** as the record channel weakens — a testable sign+ordering pattern.
3. **Florida recidivism RD with person linkage (pending ethics + FDLE dispositions).** Given that 001
   confirmed the no-sorting identification holds in Florida 2021–2026, the model predicts **deterrence
   at both 0.08 and 0.15** (DUI severity), negative, but **smaller than Washington** if Florida's
   post-conviction record effects partly offset.
4. **Arkansas 0.15 licence increment (de Figueiredo extension / OAT FOIA).** The model predicts a
   **near-null / weak** effect at the pure short-window licence-increment margin — matching de
   Figueiredo's imprecise null, and distinct from the strong effects at the conviction + severity line.

---

*Secondary (appendix, not a test): an in-sample fit including Hansen's two rows pulls the DUI
severity-class mean slightly more negative but changes no class sign; it is not used for any
classification.*
