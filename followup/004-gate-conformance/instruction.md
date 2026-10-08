# Corrective study: 004-gate-conformance — dedup Florida, honest gates, corrected 003

The provenance audit (staged at `/workspace/eval/gate-conformance-inputs/hansen-provenance.md`
— read fully; its recommendations section is the authoritative list) found the Washington
computation sound and zero name leakage, but a data defect in the Florida ingest, several
reporting-layer gate violations in 002, and in 003 one fabricated claim, a sign model that
differs from the one on disk, and a hard-coded prediction. This study supersedes both cards.
No new fetches: the dedup works from the existing parquet shards (rows map to manifest rows).

Framing rules (binding): a failed or unmet check is reported as failed/unmet, never
relabelled; nothing fabricated survives — a claim with no code behind it is deleted or the
code is actually run and the TRUE result reported, whichever the original intent was;
complete everything, continuation finishes any remainder.

## 002 corrections

1. **Deduplicate Florida**: the 537-href index has 532 unique URLs; 5 files were ingested
   twice (+2,287 duplicate records). Rebuild `fl_analysis.csv` deduplicated (audit gives
   corrected counts: 162,875 tests / 115,262 two-sample DUI), re-run the density, balance,
   MDD and heaping numbers on the deduplicated data, and update every count/figure.
2. **Heaping**: the "21% last digit 0" was the 0.000-readings artifact (12% of tests).
   Recompute excluding zeros (audit's check: 10.25%, uniform; no round-value excess at
   thresholds). RETRACT the "heaps on round values at the thresholds" caveat from the
   transport verdict, report and card, and state the artifact that produced it.
3. **B-pre block honesty**: it was written AFTER the Florida estimates. Relabel it
   post-hoc (it cannot claim pre-declaration), restore the spec's original wording where
   paraphrased, include it in report.md, and state the sequencing plainly.
4. **Structural audit honesty**: describe what was actually compared (page-level BrAC token
   multisets after the field-level comparison failed at 0.000 agreement; field count
   hard-coded; the smax 3.4-4.6 range unremarked). Remove "100% agreement" from card and
   report; run a genuine field-level agreement check on a sample of deduplicated pages and
   report the true rate, whatever it is.
5. **Full H2 template everywhere**: card metric 2 gets point estimates for BOTH 0.15
   codings; every bandwidth-significance range states its kernel (triangular; note the
   rectangular-kernel exception where 0.15 statutory excludes zero for h ≥ 0.060); the
   "excludes at MSE-optimal h / includes below 0.038" pairing gets the b=h grid note.
6. **Smaller**: correct "estimates negative across 1999-2007" (0.15: 2001 +0.004, 2004
   +0.012); surface the 0.08 strict-coding RBC-includes-zero result in the narrative;
   remove "robust" from the Florida notes; move gate-3 version info into
   followup_summary.json; disclose the spec deviations the audit lists (ingest batch
   sizes, the seed-file write, the name-assertion grep -v filtering, the missing by-year
   discrete density run — run it if cheap, else state the gap).

## 003 corrections

7. **Delete or truly run the in-sample appendix claim.** If run, report the real
   direction (audit's arithmetic: including Hansen makes the DUI severity-class mean LESS
   negative, −37.7% → −27.8%). The fabricated sentence must be named as such in
   card_corrections.csv.
8. **Present the sign model exactly as persisted** (`_sign_model.csv`): record class
   2/0/2 majority ambiguous, Humphries in its separate class, all 18 rows, Huttunen's
   fines row in the right class. The DUI/general split shown on the card exists in no
   output — remove or recompute it as a disclosed variant.
9. **Compute the prediction from the model** (no hard-coded `predict_sign()` return), and
   apply the pre-declared "uninformative" clause to 0.15 statutory (both 001 CIs include
   zero; severity majority 7 of 12) — report the classification that rule actually gives.
10. **Fix restatements of 001**: honest CI co-reported with RBC on card metric 1;
    "attenuates" → 001's pre-declared "stable" labels; remove "identification confirmed by
    001" (banned word + overstates the Florida reading); plot Finlay at its bound values,
    not 0%, or annotate why a point cannot be shown.

## Deliverables

report.md; results/findings.md opening with what was corrected and why (including the
orchestrator's transcript redaction of the step-69 masked-page print, noted for the record);
result_card.json superseding 002+003 for publication (summary leads with the Washington
result under the full H2 template, then the deduplicated Florida transport reading);
results/card_corrections.csv (old → corrected → reason, including the fabricated-claim row);
the deduplicated fl_analysis.csv and recomputed artifacts; updated figures.

## Rules

Foreground only; no fetches; no new packages; reuse existing shards/outputs;
`--timeout 10800`.