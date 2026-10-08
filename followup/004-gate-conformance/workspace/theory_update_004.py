#!/usr/bin/env python3
"""004 corrective for 003 theory-update.

Fixes (per provenance audit Verdicts 7-10):
 (7) the in-sample appendix is ACTUALLY RUN (not a fabricated sentence) and its
     true direction reported;
 (8) the sign model is presented exactly as persisted (record 2/0/2 ambiguous,
     Humphries in its own class, all 18 rows); the DUI/general record split is
     written only as a disclosed variant (general-crime record = 0/0/3, Humphries
     included);
 (9) the T3-H prediction is COMPUTED from the sign model + T0 codes (no hard-coded
     predict_sign return), and the pre-declared 'uninformative' clause is evaluated
     explicitly for every margin;
 (10) handled in report/card text (not here).

Washington Panel A inputs are read unchanged from the completed 002 methods study
(the audit verified the WA computation sound; dedup does not touch Panel A)."""
import json, os
import numpy as np, pandas as pd
import statsmodels.formula.api as smf

M001 = "/workspace/eval/followup/002-methods-and-transport"      # WA Panel A (unchanged)
OUT  = "/workspace/eval/followup/004-gate-conformance/results"
SHARED = "/workspace/eval/followup/003-theory-update/workspace/shared-data"
os.makedirs(OUT, exist_ok=True)

card001 = json.load(open(f"{M001}/result_card.json"))
assert card001["status"] == "completed", "gate1: 001/002 card not completed"
hs = json.load(open(f"{M001}/results/headline_scalars.json"))
mean079 = hs["mean_at_079"]; mean149 = hs["mean_at_149"]
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

ev = pd.read_csv(f"{SHARED}/literature/sanctions_reoffending_evidence.csv")

# ===== T0 Hansen codes (fixed before fit) =====
T0 = pd.DataFrame([
 dict(margin="Hansen_0.08", sev_norecord=1.0, record_change=0.5, monetary_only=0.0,
      incap_in_window=0, dui_specific=1,
      note="short jail+suspension+treatment (sev); conviction changes only partly at 0.08 (rec=0.5); fines bundled; jail +3.84d in 4y window=no incap"),
 dict(margin="Hansen_0.15", sev_norecord=1.0, record_change=0.0, monetary_only=0.0,
      incap_in_window=0, dui_specific=1,
      note="suspension +78.8d, jail +1.40d (sev); conviction already fixed above 0.08 (rec=0); no incap in 4y window"),
])
T0.to_csv(f"{OUT}/_t0_hansen_codes.csv", index=False)

# ===== T2 non-Hansen margins (identical codes to 003 margin_codes.csv) =====
rows = [
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
meta = ev.set_index("study_id")[["citation","open_level","direction","verified_2026_10_05"]]
def base_id(s): return "sloan2016" if s.startswith("sloan2016") else s
T2["csv_id"] = T2["study_id"].map(base_id)
T2 = T2.merge(meta, left_on="csv_id", right_index=True, how="left")
T2["dagger_abs_snip"] = T2["open_level"].isin(["ABS","SNIP"])
T0w = T0.rename(columns={"margin":"study_id"}).copy()
T0w["margin_class_label"]="Hansen margin (OOS target, coded in T0)"
T0w["direction_sign"]=np.nan; T0w["raw_rel_pct"]=np.nan
T0w["reg_eligible"]=False; T0w["eligibility_reason"]="Hansen rows EXCLUDED from every fit (T3)"
T0w["open_level"]="FULL"; T0w["dagger_abs_snip"]=False
margin_codes = pd.concat([T0w, T2], ignore_index=True, sort=False)
keep = ["study_id","margin_class_label","sev_norecord","record_change","monetary_only",
        "incap_in_window","dui_specific","direction_sign","raw_rel_pct",
        "reg_eligible","eligibility_reason","open_level","dagger_abs_snip","citation","conversion_note","note"]
keep = [c for c in dict.fromkeys(keep) if c in margin_codes.columns]
margin_codes[keep].to_csv(f"{OUT}/margin_codes.csv", index=False)

# ===== T1 harmonise =====
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

# ===== T3 descriptive regression (n=7, Hansen out) =====
reg = T2[T2.reg_eligible].copy(); reg["y"] = reg["raw_rel_pct"].astype(float)
assert not reg.study_id.str.startswith("Hansen").any(), "gate4: Hansen in regression!"
n = len(reg)
mod = smf.ols("y ~ sev_norecord + record_change + incap_in_window", data=reg).fit()
coef = mod.params.to_dict()
print(f"T3 descriptive OLS (n={n}<8): {coef}")

# ===== sign model (ALL non-Hansen rows) -- identical classify() to 003 =====
sd = T2.copy()
def classify(r):
    if r.record_change>=1 and r.sev_norecord==0: return "record_change"
    if r.monetary_only==1 and r.sev_norecord==0: return "monetary_only"
    if r.sev_norecord>=1 and r.record_change<1:  return "severity_norecord"
    return "mixed"
sd["class"]=sd.apply(classify,axis=1)
signtab=[]
for cls,g in sd.groupby("class"):
    nd=int((g.direction_sign<0).sum()); nn=int((g.direction_sign==0).sum()); nc=int((g.direction_sign>0).sum())
    maj = "deter" if nd>nc and nd>=nn else ("criminogenic" if nc>nd and nc>=nn else "ambiguous/null")
    signtab.append(dict(margin_class=cls, n=len(g), n_deter=nd, n_null=nn, n_criminogenic=nc,
                        majority=maj, studies="; ".join(g.study_id)))
signdf=pd.DataFrame(signtab)
signdf.to_csv(f"{OUT}/_sign_model.csv", index=False)
print("\n=== SIGN MODEL (persisted, all 18 non-Hansen rows) ===")
print(signdf.to_string(index=False))
assert int(signdf.n.sum())==18, "sign model must cover all 18 rows"

# disclosed variant: record-change class split by domain, Humphries counted as general-crime record
rec = sd[sd["class"]=="record_change"]
hum = sd[sd.study_id=="humphries2025"]   # lives in 'mixed'; counted here only in the disclosed variant
dui_rec = rec[rec.dui_specific==1]
gen_rec = pd.concat([rec[rec.dui_specific==0], hum])
def tri(g): return (int((g.direction_sign<0).sum()), int((g.direction_sign==0).sum()), int((g.direction_sign>0).sum()))
var_rows = [
 dict(variant="record_change_DUI", n=len(dui_rec), deter=tri(dui_rec)[0], null=tri(dui_rec)[1], crim=tri(dui_rec)[2],
      studies="; ".join(dui_rec.study_id), note="DISCLOSED post-hoc split; not a persisted class"),
 dict(variant="record_change_general", n=len(gen_rec), deter=tri(gen_rec)[0], null=tri(gen_rec)[1], crim=tri(gen_rec)[2],
      studies="; ".join(gen_rec.study_id), note="DISCLOSED post-hoc split; INCLUDES Humphries (persisted 'mixed')"),
]
pd.DataFrame(var_rows).to_csv(f"{OUT}/_sign_model_recordsplit_variant.csv", index=False)
print("\n=== disclosed record-change domain split (variant) ===")
print(pd.DataFrame(var_rows).to_string(index=False))

# clear-majority helper on the sign model
def class_majority(cls_name):
    row = signdf[signdf.margin_class==cls_name].iloc[0]
    counts = {"deter":row.n_deter, "null":row.n_null, "criminogenic":row.n_criminogenic}
    top = max(counts, key=counts.get); topn = counts[top]
    simple = topn > row.n/2.0                       # >50%
    supermaj = topn >= (2.0/3.0)*row.n              # >=2/3 (stricter sensitivity)
    return top, topn, int(row.n), simple, supermaj

# ===== T3-H prediction COMPUTED from the sign model + T0 codes =====
def predict_from_model(t0):
    cls = classify(pd.Series(t0))                   # primary class from T0 codes
    top, topn, nn, simple, supermaj = class_majority(cls)
    sign = {"deter":-1, "criminogenic":+1}.get(top, 0)
    detail = f"primary class={cls}; class majority={top} ({topn}/{nn})"
    # DUI-record support for Hansen_0.08 (partial record coding): DUI record studies deter
    if t0.get("record_change",0) and t0.get("record_change") >= 0.5 and t0.get("dui_specific"):
        dui_dirs = sd[(sd["class"]=="record_change") & (sd.dui_specific==1)].direction_sign
        if len(dui_dirs) and (dui_dirs<0).all():
            detail += "; DUI-specific record studies (Sloan) all deter -> reinforces DETER"
    return sign, simple, supermaj, cls, detail

targets=[("Hansen_0.08", dict(sev_norecord=1.0,record_change=0.5,monetary_only=0.0,dui_specific=1), "0.08", None),
         ("Hansen_0.15", dict(sev_norecord=1.0,record_change=0.0,monetary_only=0.0,dui_specific=1), "0.15_statutory","statutory >=0.150"),
         ("Hansen_0.15", dict(sev_norecord=1.0,record_change=0.0,monetary_only=0.0,dui_specific=1), "0.15_strict","strict >0.150")]
oos=[]
for margin,t0,key,coding in targets:
    psign, maj_simple, maj_super, pcls, detail = predict_from_model(t0)
    v=m[key]
    a1=rel(v["A1"],v["mean"]); a1lo=rel(v["A1_lo"],v["mean"]); a1hi=rel(v["A1_hi"],v["mean"])
    a2lo=rel(v["A2_lo"],v["mean"]); a2hi=rel(v["A2_hi"],v["mean"])
    psign_est = -1 if v["A1"]<0 else (1 if v["A1"]>0 else 0)
    a1_excl0 = (a1lo<0)==(a1hi<0); a2_excl0 = (a2lo<0)==(a2hi<0)
    both_incl0 = (not a1_excl0) and (not a2_excl0)
    # pre-declared rule (spec T3-H): uninformative carve-out evaluated FIRST
    if psign==0:
        cls="uninformative"; why="model predicts no clear sign"
    elif both_incl0 and not maj_simple:
        cls="uninformative"; why="both 001 CIs include zero AND no clear class majority"
    elif psign==psign_est:
        cls="consistent"
        why="predicted sign == sign(001 point)"
        if both_incl0:
            why += f"; both 001 CIs include zero but class majority IS clear ({'simple' if maj_simple else 'no'}-maj); uninformative clause does NOT fire"
    elif psign==-psign_est and a1_excl0 and a2_excl0:
        cls="inconsistent"; why="predicted sign opposite 001 point AND both CIs exclude zero"
    else:
        cls="uninformative"; why="neither consistent nor inconsistent conditions met"
    # supermajority sensitivity label (documented, not the headline)
    cls_super = cls
    if both_incl0 and (not maj_super) and psign==psign_est and psign!=0:
        cls_super = "uninformative"
    oos.append(dict(margin=margin, coding=coding or "n/a",
                    predicted_sign=("deter(-)" if psign<0 else ("crim(+)" if psign>0 else "none")),
                    predicted_interval="none (n<8: descriptive regression, sign model carries inference)",
                    rel_A1_pct=round(a1,2), A1_CI_rel=f"[{a1lo:+.2f},{a1hi:+.2f}]",
                    A2_CI_rel=f"[{a2lo:+.2f},{a2hi:+.2f}]",
                    A1_excludes0=a1_excl0, A2_excludes0=a2_excl0, both_CIs_include0=both_incl0,
                    class_majority_clear_simple=bool(maj_simple), class_majority_clear_super=bool(maj_super),
                    classification=cls, classification_supermajority_defn=cls_super,
                    rule_detail=why, prediction_detail=detail))
oosdf=pd.DataFrame(oos)
oosdf.to_csv(f"{OUT}/hansen_oos_test.csv", index=False)
print("\n=== T3-H OOS classification (computed from model) ===")
print(oosdf[["margin","coding","predicted_sign","rel_A1_pct","both_CIs_include0",
             "class_majority_clear_simple","classification","classification_supermajority_defn"]].to_string(index=False))

# ===== T4 elasticities + jail-day bounds (unchanged construction) =====
PAPER_EL={"0.08":-0.22,"0.15":-0.12}; PAPER_RECID_REL={"0.08":-17.0,"0.15":-9.0}
sanction_scale={k: PAPER_RECID_REL[k]/PAPER_EL[k] for k in PAPER_EL}
JAIL={"0.08":3.84,"0.15":1.40}; SUSP_015=78.8
el=[]
for key,base in [("0.08","0.08"),("0.15_statutory","0.15"),("0.15_strict","0.15")]:
    v=m[key]; ss=sanction_scale[base]
    for lab,val in [("A1_point",v["A1"]),("A1_lo",v["A1_lo"]),("A1_hi",v["A1_hi"]),("A2_lo",v["A2_lo"]),("A2_hi",v["A2_hi"])]:
        rpct=rel(val,v["mean"])
        el.append(dict(threshold=key, quantity="deterrence_elasticity", endpoint=lab,
                       recid_rel_pct=round(rpct,2), sanction_pct=round(ss,1), value=round(rpct/ss,4),
                       note=f"paper elasticity {PAPER_EL[base]}"))
    rp=rel(v["A1"],v["mean"])
    el.append(dict(threshold=key, quantity="UPPER_BOUND_rel_pct_per_jail_day", endpoint="A1_point",
                   recid_rel_pct=round(rp,2), sanction_pct=JAIL[base], value=round(rp/JAIL[base],3),
                   note="UPPER BOUND: assumes jail is the only active channel"))
    if base=="0.15":
        el.append(dict(threshold=key, quantity="ALT_UPPER_BOUND_rel_pct_per_suspension_day", endpoint="A1_point",
                       recid_rel_pct=round(rp,2), sanction_pct=SUSP_015, value=round(rp/SUSP_015,4),
                       note="ALT upper bound attributing whole effect to +78.8 suspension days"))
jansson_per_day = -80.0/30.0
el.append(dict(threshold="jansson2025_prison", quantity="rel_pct_per_prison_day", endpoint="per_month_-80%/30",
               recid_rel_pct=-80.0, sanction_pct=30, value=round(jansson_per_day,3),
               note="Sweden DUI convicts, 5y all-crime; -80% per prison MONTH /30 (if linear)"))
pd.DataFrame(el).to_csv(f"{OUT}/updated_elasticities.csv", index=False)

# ===== T5 Utah shares =====
ut=pd.read_csv(f"{SHARED}/utah/ccjj_dui_arrests_by_bac_FY2016_2025.csv")
ut["reported"]=ut["total"]-ut["bac_not_reported"]-ut["refused"]
ut["share_calc"]=ut["bac_005_007"]/ut["reported"]
before=ut[ut.fiscal_year.isin([2016,2017,2018])]; after=ut[ut.fiscal_year.isin(range(2020,2026))]
sh_before=before["bac_005_007"].sum()/before["reported"].sum()
sh_after =after["bac_005_007"].sum()/after["reported"].sum()
ut[["fiscal_year","bac_005_007","reported","share_calc","share_005_007_of_reported"]].to_csv(f"{OUT}/utah_bac_shares.csv", index=False)
print(f"\nT5 Utah .05-.07 share before={sh_before:.3%} after={sh_after:.3%} ratio={sh_after/sh_before:.2f}x")

# ===== APPENDIX (item 7): in-sample fit INCLUDING Hansen -- ACTUALLY RUN, not a test =====
# severity class numeric values (reg-eligible severity rows) + Hansen's two rows.
sev_numeric = reg[(reg.sev_norecord>=1)&(reg.record_change<1)]["y"].tolist()   # kilmer, gehrsitz, rose
sev_mean_excl = float(np.mean(sev_numeric))
# Hansen's two rows in relative terms: use the PAPER relative effects (-17,-9) as coded in T0/paper,
# matching the audit's arithmetic; also report the 001 re-analysed variant.
hansen_paper = [PAPER_RECID_REL["0.08"], PAPER_RECID_REL["0.15"]]   # -17, -9
sev_mean_incl_paper = float(np.mean(sev_numeric + hansen_paper))
hansen_001 = [rel(m["0.08"]["A1"],m["0.08"]["mean"]), rel(m["0.15_strict"]["A1"],m["0.15_strict"]["mean"])]
sev_mean_incl_001 = float(np.mean(sev_numeric + hansen_001))
appendix = dict(
  note="APPENDIX, NOT A TEST. In-sample severity-class mean with vs without Hansen's two rows.",
  severity_numeric_rows={"kilmer_midgette2020":-49.0,"gehrsitz2017":-20.0,"rose_shemtov2021":-44.0},
  severity_mean_excl_hansen=round(sev_mean_excl,1),
  hansen_rows_paper_rel=hansen_paper,
  severity_mean_incl_hansen_paper=round(sev_mean_incl_paper,1),
  hansen_rows_001_rel=[round(x,1) for x in hansen_001],
  severity_mean_incl_hansen_001=round(sev_mean_incl_001,1),
  direction="LESS negative (mean moves toward zero) when Hansen is added; the 002/003 model.md "
            "sentence claiming 'more negative' was FABRICATED (no code) and directionally wrong",
  class_signs_unchanged=True,
)
json.dump(appendix, open(f"{OUT}/insample_appendix.json","w"), indent=2)
print(f"\nAPPENDIX in-sample fit: severity mean excl Hansen = {sev_mean_excl:.1f}%, "
      f"incl Hansen (paper -17/-9) = {sev_mean_incl_paper:.1f}%  -> LESS negative")
print(f"  (incl Hansen using 001 A1 {[round(x,1) for x in hansen_001]} = {sev_mean_incl_001:.1f}%)")

# ===== headline scalars =====
scal=dict(
  mean_at_079=mean079, mean_at_149=mean149,
  rel={k:dict(A1=rel(v["A1"],v["mean"]),A1_lo=rel(v["A1_lo"],v["mean"]),A1_hi=rel(v["A1_hi"],v["mean"]),
              A2_lo=rel(v["A2_lo"],v["mean"]),A2_hi=rel(v["A2_hi"],v["mean"])) for k,v in m.items()},
  sanction_scale=sanction_scale,
  reanalysed_elasticity={k: rel(m[k]["A1"],m[k]["mean"])/sanction_scale["0.08" if k=="0.08" else "0.15"] for k in m},
  jail_day_ub={"0.08":rel(m["0.08"]["A1"],m["0.08"]["mean"])/3.84,
               "0.15_statutory":rel(m["0.15_statutory"]["A1"],m["0.15_statutory"]["mean"])/1.40,
               "0.15_strict":rel(m["0.15_strict"]["A1"],m["0.15_strict"]["mean"])/1.40},
  jansson_per_day=jansson_per_day, utah_share_before=sh_before, utah_share_after=sh_after,
  reg_n=n, reg_coef=coef, oos=oosdf.to_dict(orient="records"),
  sign_model=signdf.to_dict(orient="records"), appendix=appendix,
)
json.dump(scal, open(f"{OUT}/headline_scalars_003.json","w"), indent=1)
print("\nAll 003-corrective CSVs + headline_scalars_003.json written.")
