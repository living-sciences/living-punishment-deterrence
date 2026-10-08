#!/usr/bin/env python3
"""004 corrective — deduplicate Florida STED ingest.

The FDLE 537-href index has 532 unique URLs; 5 STED files were listed (and thus
ingested) twice. The 002 manifest has 535 STED rows but only 530 unique sha256.
Rows in fl_tests_deid.parquet map 1:1 to manifest rows in index/processing order
(verified: 100% src_year_month match), each file contributing record_count
consecutive rows. We drop the SECOND occurrence of each duplicated sha256 and
rebuild fl_tests_deid.parquet, fl_analysis.csv and a deduplicated manifest.
No new fetch: works entirely from the existing 002 parquet + manifest on disk."""
import pandas as pd, numpy as np, json, os

SRC = "/workspace/eval/followup/002-methods-and-transport/workspace/data"
OUT = "/workspace/eval/followup/004-gate-conformance/workspace/data"
RES = "/workspace/eval/followup/004-gate-conformance/results"
os.makedirs(OUT, exist_ok=True); os.makedirs(RES, exist_ok=True)

mf = pd.read_csv(f"{SRC}/fl_manifest.csv", dtype=str).fillna("")
mf["rc"] = pd.to_numeric(mf.record_count, errors="coerce").astype(int)
mf["symd"] = mf.apply(lambda r: f"{int(r.year)}-{int(r.month):02d}", axis=1)
df = pd.read_parquet(f"{SRC}/fl_tests_deid.parquet")
assert len(df) == mf.rc.sum(), "row-count mismatch"

# verify mapping
exp = np.repeat(mf.symd.values, mf.rc.values)
assert (exp == df.src_year_month.values).all(), "row->manifest mapping broke"

# cumulative row offset per manifest row
mf["start"] = np.concatenate([[0], np.cumsum(mf.rc.values)[:-1]])
mf["end"] = mf.start + mf.rc

# rows belonging to the SECOND (and later) occurrence of each sha256 -> drop
dup_mask = mf.duplicated("sha256", keep="first")
drop_idx = []
dup_files = []
for _, r in mf[dup_mask].iterrows():
    drop_idx.extend(range(r.start, r.end))
    dup_files.append(dict(filename=r.filename, year=int(r.year), month=int(r.month),
                          sha256=r.sha256, record_count=int(r.rc),
                          dropped_rows=f"[{r.start},{r.end})"))
drop_idx = np.array(sorted(drop_idx))
keep_mask = np.ones(len(df), dtype=bool); keep_mask[drop_idx] = False
dd = df.iloc[keep_mask].reset_index(drop=True)

print(f"raw parquet rows      : {len(df)}")
print(f"duplicate rows dropped: {len(drop_idx)}  ({len(dup_files)} file-occurrences)")
print(f"deduplicated rows     : {len(dd)}")
assert len(dd) == 162875, f"expected 162875 got {len(dd)}"

dd.to_parquet(f"{OUT}/fl_tests_deid.parquet", index=False)

# deduplicated manifest (first occurrence of each sha256)
mf_dd = mf[~dup_mask].drop(columns=["rc","symd","start","end"]).reset_index(drop=True)
mf_dd.to_csv(f"{OUT}/fl_manifest.csv", index=False)
print(f"deduplicated manifest rows (unique files): {len(mf_dd)}")

# rebuild fl_analysis.csv (two-sample DUI) -- same transform as 002 step [line 956]
dd["ty"] = dd.test_ym.str[:4]
dui = dd[(dd.violation == "DUI") & dd.sample1.notna() & dd.sample2.notna()].copy()
dui["run_min"] = dui[["sample1","sample2"]].min(axis=1)
dui["run_s1"]  = dui["sample1"]
dui["male"]    = (dui.gender == "M").astype(int)
dui["low_score"] = (dui["run_min"]*1000).round().astype(int)
dui["ls_s1"]     = (dui["run_s1"]*1000).round().astype(int)
out = dui[["ty","test_ym","run_min","run_s1","low_score","ls_s1","male",
           "instrument_pseudonym","sample1","sample2"]].rename(columns={"ty":"year"})
out.to_csv(f"{OUT}/fl_analysis.csv", index=False)
print(f"two-sample DUI rows   : {len(out)}")
assert len(out) == 115262, f"expected 115262 got {len(out)}"

# per-year counts (deduplicated), both all-tests and two-sample DUI
py_all = dd.assign(ty=dd.test_ym.str[:4]).groupby("ty").size()
py_dui = out.groupby("year").size()
counts = pd.DataFrame({"n_tests": py_all, "n_twosample_dui": py_dui}).fillna(0).astype(int)
counts.index.name = "year"
counts.to_csv(f"{RES}/florida_counts.csv")
print("\nper-year counts (deduplicated):")
print(counts)

# record the dedup provenance
prov = dict(
    raw_manifest_rows=len(mf), unique_sha256=int(mf.sha256.nunique()),
    duplicate_file_occurrences=dup_files,
    raw_test_records=int(len(df)), dedup_test_records=int(len(dd)),
    duplicate_records_dropped=int(len(drop_idx)),
    raw_twosample_dui=int(((df.violation=="DUI") & df.sample1.notna() & df.sample2.notna()).sum()),
    dedup_twosample_dui=int(len(out)),
)
json.dump(prov, open(f"{RES}/dedup_provenance.json","w"), indent=2)
print("\nwrote dedup_provenance.json, fl_tests_deid.parquet, fl_analysis.csv, fl_manifest.csv, florida_counts.csv")
