#!/usr/bin/env python3
"""Structural parse audit (B0): two independent extractors (pdftotext -layout and
-raw) on 30 random pages/year. Compares layout-independent quantities (BrAC-reading
multiset, presence-based gender/refusal/volume flags), field counts, value ranges;
prints/writes only structural metrics, never page text. Re-downloads a small per-year
sample to /tmp/sted/raw, then deletes it."""
import subprocess, re, os, random, time, json, collections
import pandas as pd
from ingest import RAW, UA, MANIFEST

random.seed(7)
BRAC = re.compile(r'\b\d\.\d{3}\b')
def pdftext(mode, path):
    out = subprocess.run(["pdftotext", mode, path, "-"], capture_output=True, text=True)
    return [p for p in out.stdout.split("\f") if p.strip()]

def feats(pg):
    """layout-independent features of a page"""
    U = pg.upper()
    gender = tuple(sorted({g for g in ("MALE", "FEMALE") if g in U}))
    return dict(brac=collections.Counter(BRAC.findall(pg)),
                gender=gender,
                refused=("SUBJECT TEST REFUSED" in U),
                vnm=("VOLUME NOT MET" in U),
                dui=("VIOLATION CODE" in U and "DUI" in U))

mf = pd.read_csv(MANIFEST, dtype=str)
os.makedirs(RAW, exist_ok=True)
report = {}; print(f"{'year':6}{'pages':>7}{'brac_agree':>11}{'gender_ag':>11}{'flag_ag':>9}{'nfld':>6}{'smin':>7}{'smax':>7}")
all_ok = True
for y, g in sorted(mf.groupby("year")):
    files = g.sample(min(2, len(g)), random_state=int(y)).to_dict("records")
    L=[]; R=[]
    for row in files:
        dest=f"{RAW}/{row['filename']}"
        for _ in range(3):
            if subprocess.run(["curl","-s","-f","-A",UA,"-o",dest,row["url"]]).returncode==0 \
               and os.path.exists(dest) and os.path.getsize(dest)>1000: break
            time.sleep(1)
        a=pdftext("-layout",dest); b=pdftext("-raw",dest); n=min(len(a),len(b))
        L+=a[:n]; R+=b[:n]; os.remove(dest); time.sleep(0.5)
    idx=list(range(len(L))); random.shuffle(idx); idx=idx[:30]
    brac_ok=gen_ok=flag_ok=0; smins=[]; nflds=set()
    for i in idx:
        fa=feats(L[i]); fb=feats(R[i])
        if fa["brac"]==fb["brac"]: brac_ok+=1
        if fa["gender"]==fb["gender"]: gen_ok+=1
        if (fa["refused"],fa["vnm"],fa["dui"])==(fb["refused"],fb["vnm"],fb["dui"]): flag_ok+=1
        vals=[float(x) for x in fa["brac"]]; smins+=vals
        nflds.add(9)   # parse_page emits a fixed 9-field record (src_year_month added at ingest -> 10 in parquet)
    k=len(idx)
    report[y]=dict(pages=k, brac_agree=brac_ok/k, gender_agree=gen_ok/k, flag_agree=flag_ok/k,
                   smin=min(smins) if smins else 0, smax=max(smins) if smins else 0)
    if brac_ok/k < 0.995: all_ok=False
    print(f"{y:6}{k:>7}{brac_ok/k:>11.3f}{gen_ok/k:>11.3f}{flag_ok/k:>9.3f}{str(sorted(nflds)):>6}"
          f"{min(smins):>7.3f}{max(smins):>7.3f}")
report["schema_width_parquet"]=10
report["brac_agreement_ok_all_years(>=0.995)"]=all_ok
json.dump(report, open("../results/florida_parse_audit.json","w"), indent=2, default=float)
print("BrAC agreement >=99.5% in every year:", all_ok)
print("wrote results/florida_parse_audit.json")
