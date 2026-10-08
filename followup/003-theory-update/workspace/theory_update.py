#!/usr/bin/env python3
"""Study 002/003 theory-update: a leave-Hansen-out model of which sanction margins deter.
All 001 numbers are read from disk (followup/002-methods-and-transport = the completed
methods-and-transport study; the 001 dir was cut short and relaunched as a continuation)."""
import json, os
import numpy as np, pandas as pd
import statsmodels.formula.api as smf

RUN = "/workspace/eval"
M001 = f"{RUN}/followup/002-methods-and-transport"          # completed 001-equivalent
OUT  = f"{RUN}/followup/003-theory-update/results"
SHARED = "/workspace/eval/followup/003-theory-update/workspace/shared-data"
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- 001 inputs (from disk)
card001 = json.load(open(f"{M001}/result_card.json"))
assert card001["status"] == "completed", "gate1: 001 card not completed"
hs = json.load(open(f"{M001}/results/headline_scalars.json"))
mean079 = hs["mean_at_079"]; mean149 = hs["mean_at_149"]          # gate2 means
H = hs["headline"]
def pack(key, mean):
    d = H[key]
    return dict(A1=d["A1"]["coef"], A1_lo=d["A1"]["ci_rbc_lo"], A1_hi=d["A1"]["ci_rbc_hi"],
                A2=d["A2"]["est"], A2_lo=d["A2"]["ci_lo"], A2_hi=d["A2"]["ci_hi"],
                A0=d["A0_bw05"]["coef"], mean=mean)
m = {"0.08": pack("0.08_statutory", mean079),
     "0.15_statutory": pack("0.15_statutory", mean149),
     "0.15_strict": pack("0.15_strict", mean149)}
def rel(x, mean): return 100.0*x/mean
print("=== 001 A1 relative (pt, A1 CI, A2 CI) ===")
for k,v in m.items():
    print(f"{k:14s} A1 {rel(v['A1'],v['mean']):+6.2f}%  A1CI[{rel(v['A1_lo'],v['mean']):+.2f},{rel(v['A1_hi'],v['mean']):+.2f}]"
          f"  A2CI[{rel(v['A2_lo'],v['mean']):+.2f},{rel(v['A2_hi'],v['mean']):+.2f}]")

# ---------------------------------------------------------------- evidence table
ev = pd.read_csv(f"{SHARED}/literature/sanctions_reoffending_evidence.csv")

# ======================= T0: Hansen margin codes (fixed BEFORE fit) =======================
T0 = pd.DataFrame([
 dict(margin="Hansen_0.08", sev_norecord=1.0, record_change=0.5, monetary_only=0.0,
      incap_in_window=0, dui_specific=1,
      note="short jail+suspension+treatment (sev); conviction changes only partly at 0.08 (rec=0.5); fines bundled; jail +3.84d in 4y window=no incap"),
 dict(margin="Hansen_0.15", sev_norecord=1.0, record_change=0.0, monetary_only=0.0,
      incap_in_window=0, dui_specific=1,
      note="suspension +78.8d, jail +1.40d (sev); conviction already fixed above 0.08 (rec=0); no incap in 4y window"),
])
T0.to_csv(f"{OUT}/_t0_hansen_codes.csv", index=False)

# ======================= T2: code each non-Hansen specific-deterrence margin =======================
# dims: sev_norecord, record_change, monetary_only, incap_in_window, dui_specific
# direction_sign: -1 deter, 0 null, +1 criminogenic  (sign model uses ALL rows)
rows = [
 # study_id, class_label, sev, rec, fin, incap, dui, dir, raw_rel, conv_note, reg_eligible, reason
 ("defigueiredo2015_008_deter","severity+partial record (DUI, 0.08)",1,0.5,0,0,1,-1,None,
    "pp -1.3 on ~1% base not convertible to a sensible relative; sign only", False,
    "FULL but pp effect exceeds vague ~1% base -> relative NA"),
 ("defigueiredo2015_015","licence increment (DUI, 0.15)",1,0,0,0,1,0,None,
    "range -0.1..+0.6pp, imprecise null; sign only", False,"range, no baseline -> NA"),
 ("rahman2022","interlock technology (DUI)",1,0,0,0,1,-1,None,
    "-3pp 2y post-removal, no baseline for a relative; sign only", False,"ABS, pp no baseline"),
 ("sloan2016_prosecution","prosecution record (DUI)",0,1,0,0,1,-1,-6.6,
    "published relative -6.6% (prosecution vs not), SEJ2016 abstract", True,"verified ABS relative"),
 ("sloan2016_conviction","conviction record (DUI)",0,1,0,0,1,-1,-24.5,
    "published relative -24.5% (conviction|prosecuted), SEJ2016 abstract", True,"verified ABS relative"),
 ("kilmer_midgette2020","swift-certain-modest testing+short jail (DUI)",1,0,0,0,1,-1,-49.0,
    "published relative -49% re-arrest/revocation", True,"verified ABS relative"),
 ("gehrsitz2017","automatic 1-month licence suspension (traffic)",1,0,0,0,0,-1,-20.0,
    "published relative -20%; authors attribute to deterrence not incap", True,"verified ABS relative"),
 ("jansson2025","prison length, intensive margin (DUI convicts)",1,0,0,0,1,-1,None,
    "-80% per MONTH of prison = dose slope, not a single total effect; sign only + T4", False,
    "per-month slope, not single comparable total effect"),
 ("suonpaa2021","suspended prison vs fine (DUI)",1,0,0,0,1,0,None,
    "'small, insignificant' null, no number; sign only", False,"no number, UNVERIFIED journal ver"),
 ("agan2023","prosecution record (general misdemeanor)",0,1,0,0,0,+1,+113.0,
    "published -53% for NON-prosecution; harsher side=prosecution: 1/(1-0.53)-1=+113%", True,
    "verified ABS; converted to harsher (prosecution) side"),
 ("dobbie2018","pretrial detention (general)",1,0,0,1,0,0,None,
    "~0 net effect, no number; sign only", False,"no number, null"),
 ("leslie_pope2017","pretrial detention (general)",1,0,0,1,0,+1,None,
    "incapacitation offset by later higher recidivism (null-to-criminogenic); sign only", False,"no number"),
 ("rose_shemtov2021","incarceration extensive+intensive (general felony)",1,0,0,1,0,-1,-44.0,
    "published relative -44% (3y); diminishing returns", True,"verified ABS relative"),
 ("bhuller2020","incarceration extensive (general)",1,0,0,1,0,-1,None,
    "-29pp, no baseline for relative; sign only", False,"ABS, pp no baseline"),
 ("mueller_smith_schnepel2021","conviction record vs diversion (general felony)",0,1,0,0,0,+1,+100.0,
    "diversion -50% -> harsher side=conviction: 1/(1-0.50)-1=+100% (record ~doubles reoffending)", True,
    "verified ABS; converted to harsher (conviction) side"),
 ("humphries2025","conviction record + incarceration (general felony)",0.5,1,0,1,0,+1,None,
    "conviction: large lasting increase; UNVERIFIED point estimates; sign only", False,
    "UNVERIFIED magnitudes (H8) -> sign only"),
 ("finlay2024","fines/fees only (traffic+criminal)",0,0,1,0,0,0,None,
    "bounds -0.001..0.01 annual CONVICTION COUNTS, no relative reoffending & no baseline; sign only", False,
    "conviction-count bounds, not relative reoffending (H8) -> sign only"),
 ("huttunen_ladder","fines vs probation vs prison (general)",1,0.5,1,0,0,+1,None,
    "mixed: fines raise, probation/prison lower; multi-margin, no single number; sign only (fines-class=criminogenic)", False,
    "mixed multi-margin, no single number"),
]
cols = ["study_id","margin_class_label","sev_norecord","record_change","monetary_only",
        "incap_in_window","dui_specific","direction_sign","raw_rel_pct","conversion_note",
        "reg_eligible","eligibility_reason"]
T2 = pd.DataFrame(rows, columns=cols)
# add open_level + citation + csv direction for traceability
meta = ev.set_index("study_id")[["citation","open_level","direction","verified_2026_10_05"]]
def base_id(s):  # map split sloan rows back to csv id
    return "sloan2016" if s.startswith("sloan2016") else s
T2["csv_id"] = T2["study_id"].map(base_id)
T2 = T2.merge(meta, left_on="csv_id", right_index=True, how="left")
T2["dagger_abs_snip"] = T2["open_level"].isin(["ABS","SNIP"])
# write combined margin_codes.csv (T0 Hansen rows + T2 rows) BEFORE fitting
T0w = T0.rename(columns={"margin":"study_id","sev_norecord":"sev_norecord"}).copy()
T0w["margin_class_label"]="Hansen margin (OOS target, coded in T0)"
T0w["direction_sign"]=np.nan; T0w["raw_rel_pct"]=np.nan
T0w["reg_eligible"]=False; T0w["eligibility_reason"]="Hansen rows EXCLUDED from every fit (T3)"
T0w["open_level"]="FULL"; T0w["dagger_abs_snip"]=False
margin_codes = pd.concat([T0w, T2], ignore_index=True, sort=False)
keep = ["study_id","margin_class_label","sev_norecord","record_change","monetary_only",
        "incap_in_window","dui_specific","dui_specific","direction_sign","raw_rel_pct",
        "reg_eligible","eligibility_reason","open_level","dagger_abs_snip","citation","conversion_note","note"]
keep = [c for c in dict.fromkeys(keep) if c in margin_codes.columns]
margin_codes[keep].to_csv(f"{OUT}/margin_codes.csv", index=False)
print("\nmargin_codes.csv written BEFORE fit. Hansen rows reg_eligible:",
      list(margin_codes[margin_codes.study_id.str.startswith("Hansen")].reg_eligible))

# ======================= T1: harmonise (raw -> conversion -> result) =======================
harm = []
for _,r in T2.iterrows():
    harm.append(dict(study_id=r.study_id, outcome_from_csv=meta.loc[r.csv_id,"direction"],
                     raw_value=r.raw_rel_pct if pd.notna(r.raw_rel_pct) else "see note",
                     conversion=r.conversion_note,
                     result_rel_pct=r.raw_rel_pct if pd.notna(r.raw_rel_pct) else np.nan,
                     horizon_yrs=ev.set_index("study_id").loc[r.csv_id,"horizon_years"],
                     population=ev.set_index("study_id").loc[r.csv_id,"population"],
                     open_level=r.open_level))
pd.DataFrame(harm).to_csv(f"{OUT}/harmonised_effects.csv", index=False)

# ======================= T3: model fitted LEAVING HANSEN OUT =======================
reg = T2[T2.reg_eligible].copy()
reg["y"] = reg["raw_rel_pct"].astype(float)
print(f"\n=== T3 regression rows (n={len(reg)}) ===")
print(reg[["study_id","y","sev_norecord","record_change","monetary_only","incap_in_window"]].to_string(index=False))
assert not reg.study_id.str.startswith("Hansen").any(), "gate4: Hansen in regression!"
n = len(reg)
# monetary_only has no variation among eligible -> drop; fit descriptive OLS (n<8)
mod = smf.ols("y ~ sev_norecord + record_change + incap_in_window", data=reg).fit()
coef = mod.params.to_dict()
print(f"\nT3 OLS (DESCRIPTIVE, n={n}<8 -> no SE/p reported): {coef}")

# Sign model: ordinal direction by margin class, ALL non-Hansen specific-deterrence rows
sd = T2.copy()   # all non-Hansen specific-deterrence rows (general-deterrence not in T2)
def classify(r):
    if r.record_change>=1 and r.sev_norecord==0: return "record_change"
    if r.monetary_only==1 and r.sev_norecord==0: return "monetary_only"
    if r.sev_norecord>=1 and r.record_change<1:  return "severity_norecord"
    return "mixed"
sd["class"]=sd.apply(classify,axis=1)
signtab=[]
for cls,g in sd.groupby("class"):
    nd=(g.direction_sign<0).sum(); nn=(g.direction_sign==0).sum(); nc=(g.direction_sign>0).sum()
    # domain split for record_change
    maj = "deter" if nd>nc and nd>=nn else ("criminogenic" if nc>nd and nc>=nn else "ambiguous/null")
    signtab.append(dict(margin_class=cls, n=len(g), n_deter=nd, n_null=nn, n_criminogenic=nc,
                        majority=maj, studies="; ".join(g.study_id)))
signdf=pd.DataFrame(signtab)
print("\n=== SIGN MODEL (all non-Hansen specific-deterrence rows) ===")
print(signdf.to_string(index=False))
# domain split within record_change
rec=sd[sd["class"]=="record_change"]
dui_rec=rec[rec.dui_specific==1]; gen_rec=rec[rec.dui_specific==0]
print(f"\nrecord_change DUI-specific dir: {list(zip(dui_rec.study_id,dui_rec.direction_sign))}")
print(f"record_change general-crime dir: {list(zip(gen_rec.study_id,gen_rec.direction_sign))}")
signdf.to_csv(f"{OUT}/_sign_model.csv", index=False)

# ======================= T3-H: OOS prediction of Hansen's two margins =======================
# predicted sign from sign model, using T0 codes (fixed before fit)
def predict_sign(margin):
    if margin=="Hansen_0.08":
        # severity(deter) + partial DUI-record(deter) -> deter
        return -1, "severity_norecord majority=deter AND DUI-specific record (Sloan)=deter -> predict DETER"
    if margin=="Hansen_0.15":
        return -1, "pure severity_norecord, DUI-specific; severity class majority=deter -> predict DETER"
oos=[]
targets=[("Hansen_0.08","0.08",None),
         ("Hansen_0.15","0.15_statutory","statutory >=0.150"),
         ("Hansen_0.15","0.15_strict","strict >0.150")]
for margin,key,coding in targets:
    psign,prationale=predict_sign(margin)
    v=m[key]
    a1=rel(v["A1"],v["mean"]); a1lo=rel(v["A1_lo"],v["mean"]); a1hi=rel(v["A1_hi"],v["mean"])
    a2lo=rel(v["A2_lo"],v["mean"]); a2hi=rel(v["A2_hi"],v["mean"])
    psign_est = -1 if v["A1"]<0 else (1 if v["A1"]>0 else 0)
    a1_excl0 = (a1lo<0)==(a1hi<0)
    a2_excl0 = (a2lo<0)==(a2hi<0)
    # classification (pre-declared). No regression PI (n<8 descriptive) -> sign-based.
    if psign==psign_est:
        cls="consistent"
    elif psign==-psign_est and a1_excl0 and a2_excl0:
        cls="inconsistent"
    else:
        cls="uninformative"
    oos.append(dict(margin=margin, coding=coding or "n/a", predicted_sign=("deter(-)" if psign<0 else "crim(+)"),
                    predicted_interval="none (n<8: descriptive regression, sign model carries inference)",
                    rel_A1_pct=round(a1,2), A1_CI_rel=f"[{a1lo:+.2f},{a1hi:+.2f}]",
                    A2_CI_rel=f"[{a2lo:+.2f},{a2hi:+.2f}]",
                    A1_excludes0=a1_excl0, A2_excludes0=a2_excl0,
                    classification=cls, rationale=prationale))
oosdf=pd.DataFrame(oos)
oosdf.to_csv(f"{OUT}/hansen_oos_test.csv", index=False)
print("\n=== T3-H OOS classification ===")
print(oosdf[["margin","coding","predicted_sign","rel_A1_pct","A1_CI_rel","A2_CI_rel","classification"]].to_string(index=False))

# ======================= T4: re-analysed elasticities + jail-day upper bounds =======================
# sanction scale fixed from paper (recid_rel / paper_elasticity): isolates swap of recid estimate
PAPER_EL={"0.08":-0.22,"0.15":-0.12}; PAPER_RECID_REL={"0.08":-17.0,"0.15":-9.0}
sanction_scale={k: PAPER_RECID_REL[k]/PAPER_EL[k] for k in PAPER_EL}  # % sanction increase
print(f"\nsanction scale %: {sanction_scale}")
JAIL={"0.08":3.84,"0.15":1.40}; SUSP_015=78.8
el=[]
for key,base in [("0.08","0.08"),("0.15_statutory","0.15"),("0.15_strict","0.15")]:
    v=m[key]; ss=sanction_scale[base]
    for lab,val in [("A1_point",v["A1"]),("A1_lo",v["A1_lo"]),("A1_hi",v["A1_hi"]),
                    ("A2_lo",v["A2_lo"]),("A2_hi",v["A2_hi"])]:
        rpct=rel(val,v["mean"])
        el.append(dict(threshold=key, quantity="deterrence_elasticity", endpoint=lab,
                       recid_rel_pct=round(rpct,2), sanction_pct=round(ss,1),
                       value=round(rpct/ss,4),
                       note=f"paper elasticity {PAPER_EL[base]}"))
    # jail-day upper bound (relative % per jail day)
    rp=rel(v["A1"],v["mean"])
    el.append(dict(threshold=key, quantity="UPPER_BOUND_rel_pct_per_jail_day", endpoint="A1_point",
                   recid_rel_pct=round(rp,2), sanction_pct=JAIL[base], value=round(rp/JAIL[base],3),
                   note="UPPER BOUND: assumes jail is the only active channel (bundle incl conviction/fines/treatment)"))
    if base=="0.15":
        el.append(dict(threshold=key, quantity="ALT_UPPER_BOUND_rel_pct_per_suspension_day", endpoint="A1_point",
                       recid_rel_pct=round(rp,2), sanction_pct=SUSP_015, value=round(rp/SUSP_015,4),
                       note="ALT upper bound attributing whole effect to +78.8 suspension days"))
# Jansson comparison
jansson_per_day = -80.0/30.0
el.append(dict(threshold="jansson2025_prison", quantity="rel_pct_per_prison_day", endpoint="per_month_-80%/30",
               recid_rel_pct=-80.0, sanction_pct=30, value=round(jansson_per_day,3),
               note="Sweden DUI convicts, 5y all-crime; -80% per prison MONTH /30 days (if linear); contrast w/ Hansen bundle"))
pd.DataFrame(el).to_csv(f"{OUT}/updated_elasticities.csv", index=False)
print("\n=== T4 elasticities ===")
for r in el:
    if r["quantity"]=="deterrence_elasticity" and r["endpoint"]=="A1_point":
        print(f"{r['threshold']:14s} elasticity {r['value']:+.3f} (paper {r['note']})")
print(f"jail-day upper bounds: 0.08={el and [x['value'] for x in el if x['threshold']=='0.08' and 'jail_day' in x['quantity']]}")

# ======================= T5: Utah .05 shares =======================
ut=pd.read_csv(f"{SHARED}/utah/ccjj_dui_arrests_by_bac_FY2016_2025.csv")
ut["reported"]=ut["total"]-ut["bac_not_reported"]-ut["refused"]
ut["share_calc"]=ut["bac_005_007"]/ut["reported"]
before=ut[ut.fiscal_year.isin([2016,2017,2018])]
after =ut[ut.fiscal_year.isin(range(2020,2026))]
sh_before=before["bac_005_007"].sum()/before["reported"].sum()
sh_after =after["bac_005_007"].sum()/after["reported"].sum()
ut[["fiscal_year","bac_005_007","reported","share_calc","share_005_007_of_reported"]].to_csv(f"{OUT}/utah_bac_shares.csv", index=False)
print(f"\n=== T5 Utah .05-.07 share: before(FY16-18)={sh_before:.3%}  after(FY20-25)={sh_after:.3%}  ratio={sh_after/sh_before:.2f}x ===")

# ======================= headline scalars for report/card =======================
scal=dict(
  mean_at_079=mean079, mean_at_149=mean149,
  rel={k:dict(A1=rel(v["A1"],v["mean"]),A1_lo=rel(v["A1_lo"],v["mean"]),A1_hi=rel(v["A1_hi"],v["mean"]),
              A2_lo=rel(v["A2_lo"],v["mean"]),A2_hi=rel(v["A2_hi"],v["mean"])) for k,v in m.items()},
  sanction_scale=sanction_scale,
  reanalysed_elasticity={"0.08":rel(m["0.08"]["A1"],m["0.08"]["mean"])/sanction_scale["0.08"],
                         "0.15_statutory":rel(m["0.15_statutory"]["A1"],m["0.15_statutory"]["mean"])/sanction_scale["0.15"],
                         "0.15_strict":rel(m["0.15_strict"]["A1"],m["0.15_strict"]["mean"])/sanction_scale["0.15"]},
  jail_day_ub={"0.08":rel(m["0.08"]["A1"],m["0.08"]["mean"])/3.84,
               "0.15_statutory":rel(m["0.15_statutory"]["A1"],m["0.15_statutory"]["mean"])/1.40,
               "0.15_strict":rel(m["0.15_strict"]["A1"],m["0.15_strict"]["mean"])/1.40},
  jansson_per_day=jansson_per_day,
  utah_share_before=sh_before, utah_share_after=sh_after,
  reg_n=n, reg_coef=coef,
  oos=oosdf.to_dict(orient="records"),
  sign_model=signdf.to_dict(orient="records"),
)
json.dump(scal, open(f"{OUT}/headline_scalars.json","w"), indent=1)
print("\nAll result CSVs + headline_scalars.json written to results/.")
