#!/usr/bin/env python3
"""Florida STED ingest (privacy-first). Processes unparsed files from the manifest
in time-budgeted batches, writes de-identified parquet shards, runs a per-batch name
assertion, deletes raw PDFs. Resumes from the manifest. Never prints raw page text."""
import subprocess, re, os, sys, time, hashlib, csv, random, glob
import pandas as pd

STUDY = "/workspace/eval/followup/002-methods-and-transport"
WS    = f"{STUDY}/workspace"
DATA  = f"{WS}/data"; SHARDS = f"{DATA}/_shards"; RAW = "/tmp/sted/raw"
MANIFEST = f"{DATA}/fl_manifest.csv"; SEEDF = "/tmp/sted/seed.txt"
INDEX = f"{WS}/shared-data/florida/subject-test-electronic-data_index.html"
BASE = "https://www.fdle.state.fl.us"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
TIME_BUDGET = int(os.environ.get("TIME_BUDGET", "420"))   # seconds per invocation
SLEEP = 0.5
os.makedirs(DATA, exist_ok=True); os.makedirs(SHARDS, exist_ok=True); os.makedirs(RAW, exist_ok=True)

# ephemeral pseudonym seed (in /tmp, never written under workspace/results/transcript)
if os.path.exists(SEEDF):
    SEED = open(SEEDF).read().strip()
else:
    SEED = hashlib.sha256(os.urandom(32)).hexdigest()
    open(SEEDF, "w").write(SEED)
def pseudonym(serial):
    return int(hashlib.sha1((SEED + "|" + str(serial)).encode()).hexdigest(), 16) % 1000000

# ---------- manifest ----------
def fname(h): return h.split("?")[0].rstrip("/").split("/")[-1]
def full(h): return h if h.startswith("http") else BASE + ("" if h.startswith("/") else "/") + h
def ym_of(fn):
    fu = fn.upper()
    m = re.search(r'STED[_-](\d{1,2})[_-](20\d{2})[_-]', fu)
    if m: return int(m.group(2)), int(m.group(1))
    m = re.search(r'STED[_-](20\d{2})(\d{2})[_-]', fu)
    if m: return int(m.group(1)), int(m.group(2))
    m = re.search(r'STED[_-](20\d{2})[_-](\d{1,2})[_-]', fu)
    if m: return int(m.group(1)), int(m.group(2))
    return 0, 0

def build_manifest():
    if os.path.exists(MANIFEST): return
    html = open(INDEX, encoding="utf-8", errors="replace").read()
    hrefs = re.findall(r'href="([^"]+?\.pdf[^"]*)"', html, flags=re.I)
    sted = [h for h in hrefs if fname(h).upper().startswith("STED")]
    rows = []
    for h in sted:
        fn = fname(h); y, mo = ym_of(fn)
        rows.append(dict(filename=fn, url=full(h), year=y, month=mo,
                         status="pending", sha256="", page_count="", record_count="",
                         kept_count="", parsed_ts=""))
    pd.DataFrame(rows).to_csv(MANIFEST, index=False)
    print(f"manifest built: {len(rows)} files")

# ---------- parser ----------
EVENT_RE = re.compile(r'AIR BLANK|CONTROL TEST|SUBJECT SAMPLE|DIAGNOSTIC|MOUTH ALCOHOL', re.I)
BRAC_RE = re.compile(r'\b\d\.\d{3}\b')
NAME_LABELS = ("LAST NAME", "BREATH TEST OPERATOR", "ARRESTING OFFICER")

def parse_page(pg):
    """Return (record dict or None, set of name tokens). Never returns raw text."""
    U = pg.upper()
    # fields we keep
    g = re.search(r'GENDER\s*:?\s*(MALE|FEMALE|UNKNOWN)', U)
    gender = {"MALE": "M", "FEMALE": "F"}.get(g.group(1), "U") if g else "U"
    v = re.search(r'VIOLATION CODE\s*:?\s*([A-Z]{2,5})', U)
    violation = v.group(1) if v else "NA"
    d = re.search(r'DATE/TIME OF TEST\s*:?\s*(\d{1,2})/(\d{1,2})/(20\d{2})', U)
    test_ym = f"{d.group(3)}-{int(d.group(1)):02d}" if d else "NA"
    s = re.search(r'SERIAL NUMBER\s*:?\s*([0-9][0-9\-]{2,})', U)
    serial = s.group(1) if s else "NA"
    refused = "SUBJECT TEST REFUSED" in U
    vnm = "VOLUME NOT MET" in U
    # subject-sample readings: same-line BrAC on SUBJECT SAMPLE lines not flagged refused/vnm
    readings = []
    for line in pg.splitlines():
        lu = line.upper()
        if "SUBJECT SAMPLE" in lu:
            nums = BRAC_RE.findall(line)
            if nums and "VOLUME NOT MET" not in lu and "REFUSED" not in lu:
                readings.append(float(nums[0]))
    s1 = readings[0] if len(readings) >= 1 else None
    s2 = readings[1] if len(readings) >= 2 else None
    rec = dict(test_ym=test_ym, violation=violation, gender=gender,
               sample1=s1, sample2=s2, refusal_flag=bool(refused),
               volume_not_met_flag=bool(vnm), instrument_pseudonym=pseudonym(serial),
               n_valid_samples=len(readings))
    # name tokens (for assertion only; never stored). Take ONLY the field value
    # (text up to the next 2+ space gap), so adjacent field labels are not captured.
    tokens = set()
    for line in pg.splitlines():
        lu = line.upper()
        for lab in NAME_LABELS:
            if lab in lu and "AGENCY" not in lu:
                after = line[lu.find(lab) + len(lab):]
                after = re.sub(r'^[\s:]+', '', after)
                value = re.split(r'\s{2,}', after)[0]       # first cell only
                for t in re.findall(r"[A-Za-z][A-Za-z'\-]{3,}", value):
                    tokens.add(t)
    return rec, tokens

def parse_pdf(path):
    out = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
    pages = [p for p in out.stdout.split("\f") if p.strip()]
    recs = []; names = set()
    for pg in pages:
        r, tk = parse_page(pg); recs.append(r); names |= tk
    return pages_count(out.stdout), recs, names
def pages_count(txt): return len([p for p in txt.split("\f") if p.strip()])

# ---------- name assertion ----------
def name_assertion(tokens):
    """Whole-word case-sensitive search of name tokens (>=4 chars) across the study
    tree + transcript. Returns (n_tokens, text_hits, parquet_hits). Reports paths/counts
    only, never the matched text."""
    toks = sorted({t for t in tokens if len(t) >= 4})
    if not toks: return 0, [], []
    pat = re.compile(r'\b(' + "|".join(re.escape(t) for t in toks) + r')\b')
    text_hits = []; pq_hits = []
    SKIP = (f"{WS}/.venv", f"{WS}/rlib", f"{WS}/shared-data")
    for root, dirs, files in os.walk(STUDY):
        if any(root.startswith(s) for s in SKIP):
            dirs[:] = []; continue
        for f in files:
            fp = os.path.join(root, f)
            if f.endswith((".png", ".rds")): continue
            if f.endswith(".parquet"):
                try:
                    dfp = pd.read_parquet(fp)
                    objcols = [c for c in dfp.columns if dfp[c].dtype == object]
                    vals = set()
                    for c in objcols: vals |= set(dfp[c].dropna().astype(str).unique())
                    if any(pat.search(v) for v in vals): pq_hits.append(fp)
                except Exception:
                    pass
                continue
            if f.endswith(".pdf"): continue
            try:
                txt = open(fp, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            if pat.search(txt):
                text_hits.append((fp, len(set(pat.findall(txt)))))
    return len(toks), text_hits, pq_hits

# ---------- main ----------
def download(url, dest):
    for attempt in range(3):
        r = subprocess.run(["curl", "-s", "-f", "-A", UA, "-o", dest, url])
        if r.returncode == 0 and os.path.exists(dest) and os.path.getsize(dest) > 1000:
            return True
        time.sleep(1.0)
    return False

def run():
    build_manifest()
    mf = pd.read_csv(MANIFEST, dtype=str).fillna("")
    pending = mf[mf.status != "parsed"].index.tolist()
    print(f"pending files: {len(pending)} / {len(mf)}")
    t0 = time.time(); done_this_call = 0; shard_recs = []; shard_names = set()
    shard_id = len(glob.glob(f"{SHARDS}/batch_*.parquet"))
    for idx in pending:
        if time.time() - t0 > TIME_BUDGET:
            print("time budget reached; stopping this call"); break
        row = mf.loc[idx]; fn = row.filename; dest = f"{RAW}/{fn}"
        ok = download(row.url, dest)
        if not ok:
            mf.loc[idx, "status"] = "download_failed"; continue
        sha = hashlib.sha256(open(dest, "rb").read()).hexdigest()
        try:
            npages, recs, names = parse_pdf(dest)
        except Exception as e:
            mf.loc[idx, "status"] = "parse_failed"; os.remove(dest); continue
        for r in recs:
            r["src_year_month"] = f"{int(row.year)}-{int(row.month):02d}"
        shard_recs.extend(recs); shard_names |= names
        kept = sum(1 for r in recs if r["sample1"] is not None and r["sample2"] is not None)
        mf.loc[idx, ["status", "sha256", "page_count", "record_count", "kept_count", "parsed_ts"]] = \
            ["parsed", sha, str(npages), str(len(recs)), str(kept), time.strftime("%Y-%m-%dT%H:%M:%S")]
        os.remove(dest)
        done_this_call += 1
        time.sleep(SLEEP)
    # write shard + assertion
    if shard_recs:
        df = pd.DataFrame(shard_recs)
        assert not any(df.dtypes == object) or all(c in ("test_ym","violation","gender","src_year_month") for c in df.columns[df.dtypes==object]), "unexpected object column"
        shardpath = f"{SHARDS}/batch_{shard_id:04d}.parquet"
        df.to_parquet(shardpath, index=False)
        ntok, text_hits, pq_hits = name_assertion(shard_names)
        # FL-derived text files = csv/log/json written under /data/ by the ingest
        fl_text = [(fp, n) for fp, n in text_hits if "/workspace/data/" in fp]
        print(f"ASSERTION: {ntok} name tokens checked. parquet_hits={len(pq_hits)} "
              f"fl_derived_text_hits={len(fl_text)} other_text_collisions={len(text_hits)-len(fl_text)}")
        if pq_hits or fl_text:
            print("   FL-DERIVED HITS (STOP):", pq_hits, fl_text)
            raise SystemExit("NAME LEAK into Florida-derived file; stop and fix parser")
        for fp, n in text_hits:
            print(f"   non-florida collision: {fp} (whole-word matches={n})")
        shard_names.clear()
    mf.to_csv(MANIFEST, index=False)
    nparsed = (mf.status == "parsed").sum()
    print(f"this call parsed {done_this_call} files; total parsed {nparsed}/{len(mf)}")
    print("REMAINING" if nparsed < len(mf) else "ALL_DONE")

if __name__ == "__main__":
    run()
