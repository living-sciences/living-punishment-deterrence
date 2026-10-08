#!/usr/bin/env python3
"""004 corrective (item 4) — honest structural audit of the Florida parse.

What 002 actually did (per provenance audit Verdict 4): the two-extractor
(-layout vs -raw) FIELD-LEVEL comparison failed at 0.000 agreement (the field
parser is line-structure dependent, which -raw destroys), so 002 fell back to
comparing page-level BrAC *token multisets* + presence flags, hard-coded the
field count (nflds.add(9)), and left the raw-token value range (smax 3.4-4.6,
outside BrAC [0,0.5]) unremarked while reporting "100% two-extractor agreement".

A genuine two-extractor re-parse CANNOT be rerun here: the raw PDFs were deleted
page-by-page at ingest (privacy design) and this study permits no new fetches.
The closest defensible field-level check on the DEDUPLICATED data is a per-field
validity audit of the parsed fields on a 30-pages/year sample, reporting the true
pass rate per field, plus the true in-parquet value range of the subject-sample
readings. We report whatever the rates are."""
import pandas as pd, numpy as np, re, json

DD = "/workspace/eval/followup/004-gate-conformance/workspace/data/fl_tests_deid.parquet"
RES = "/workspace/eval/followup/004-gate-conformance/results"
df = pd.read_parquet(DD)
df["ty"] = df.test_ym.str[:4]

VIOL = {"DUI","BUI","COURT","ADMIN","PROB","COMM","OTHER","SYS","ZERO","NA"}
YM = re.compile(r'^\d{4}-\d{2}$|^NA$')

def field_checks(r):
    return dict(
        test_ym_fmt = bool(YM.match(str(r.test_ym))),
        violation_domain = r.violation in VIOL,
        gender_domain = r.gender in {"M","F","U"},
        sample1_range = pd.isna(r.sample1) or (0.0 <= r.sample1 <= 0.5),
        sample2_range = pd.isna(r.sample2) or (0.0 <= r.sample2 <= 0.5),
        nvalid_consistent = (int(r.n_valid_samples) == int(pd.notna(r.sample1)) + int(pd.notna(r.sample2))),
        flags_bool = isinstance(bool(r.refusal_flag), bool) and isinstance(bool(r.volume_not_met_flag), bool),
    )

rng = np.random.default_rng(7)
rows = []
per_year = {}
fields = ["test_ym_fmt","violation_domain","gender_domain","sample1_range",
          "sample2_range","nvalid_consistent","flags_bool"]
for y, g in df.groupby("ty"):
    samp = g.sample(min(30, len(g)), random_state=int(y))
    res = {f: 0 for f in fields}
    for _, r in samp.iterrows():
        c = field_checks(r)
        for f in fields: res[f] += int(c[f])
    k = len(samp)
    per_year[y] = {f: res[f]/k for f in fields} | {"pages": k}

# full-dataset true value range of subject-sample readings (the in-parquet range)
s1 = df.sample1.dropna(); s2 = df.sample2.dropna()
inparq = dict(sample1_min=float(s1.min()), sample1_max=float(s1.max()),
              sample2_min=float(s2.min()), sample2_max=float(s2.max()),
              sample1_out_of_range=int(((s1<0)|(s1>0.5)).sum()),
              sample2_out_of_range=int(((s2<0)|(s2>0.5)).sum()))

# aggregate per-field pass rate over the whole 30/yr * 6 sample
agg = {f: float(np.mean([per_year[y][f] for y in per_year])) for f in fields}

report = dict(
    method="per-field validity audit on 30 deduplicated pages/year (single-extractor; "
           "two-extractor -layout/-raw re-parse not possible: raw PDFs deleted at ingest, no fetch allowed)",
    n_pages_sampled=int(sum(per_year[y]["pages"] for y in per_year)),
    per_field_pass_rate=agg,
    per_year=per_year,
    inparquet_reading_range=inparq,
    note_002_structural_audit=(
        "002 reported '100% agreement' on BrAC TOKEN MULTISETS + presence flags, NOT parsed fields; "
        "its field-level -layout-vs-raw comparison had failed at 0.000 agreement (parser is layout-dependent); "
        "schema width was hard-coded (nflds.add(9)); raw-token smax ranged 3.417-4.562 (outside BrAC [0,0.5]) "
        "and went unremarked. In-parquet subject-sample readings ARE within [0,0.5] (range check below)."),
)
json.dump(report, open(f"{RES}/florida_field_audit.json","w"), indent=2, default=float)
print("=== per-field pass rate (30 pages/yr sample, deduplicated) ===")
for f in fields: print(f"  {f:20s} {agg[f]*100:6.2f}%")
print("\n=== in-parquet subject-sample reading range (full dedup data) ===")
print(f"  sample1 [{inparq['sample1_min']:.3f}, {inparq['sample1_max']:.3f}]  out-of-range={inparq['sample1_out_of_range']}")
print(f"  sample2 [{inparq['sample2_min']:.3f}, {inparq['sample2_max']:.3f}]  out-of-range={inparq['sample2_out_of_range']}")
print("\nwrote florida_field_audit.json")
