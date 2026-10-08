import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, pandas as pd
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

OUT="/workspace/eval/followup/004-gate-conformance/results"
OKABE={"blue":"#0072B2","orange":"#E69F00","green":"#009E73","verm":"#D55E00",
       "pink":"#CC79A7","sky":"#56B4E9","yellow":"#F0E442","black":"#000000","gray":"#888888"}
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"savefig.bbox":"tight","font.size":11,
    "axes.titlesize":13,"axes.labelsize":11,"axes.spines.top":False,"axes.spines.right":False,
    "axes.grid":True,"grid.alpha":0.25})
scal=json.load(open(f"{OUT}/headline_scalars_003.json")); rel=scal["rel"]

# ---------------- FIG: margins forest (Finlay CORRECTED: annotated, not plotted at 0%) ----------------
studies=[  # (label, value%, class)
 ("Kilmer-Midgette 2020 — 24/7 testing+jail (DUI)",-49,"sev"),
 ("Rose-Shem-Tov 2021 — incarceration (gen.)",-44,"sev"),
 ("Gehrsitz 2017 — licence suspension (traffic)",-20,"sev"),
 ("Sloan 2016 — conviction|prosec. (DUI)",-24.5,"recDUI"),
 ("Sloan 2016 — prosecution (DUI)",-6.6,"recDUI"),
 ("Mueller-Smith–Schnepel 2021 — conviction (gen.)",100,"recGEN"),
 ("Agan 2023 — prosecution (gen.)",113,"recGEN"),
]
colmap={"sev":OKABE["blue"],"recDUI":OKABE["green"],"recGEN":OKABE["verm"]}
fig,ax=plt.subplots(figsize=(9.4,6.4))
order=["sev","recDUI","recGEN"]
studies_sorted=sorted(studies,key=lambda s:(order.index(s[2]), s[1]))
y=np.arange(len(studies_sorted))
for i,(lab,val,cls) in enumerate(studies_sorted):
    ax.scatter(val,i,color=colmap[cls],s=75,zorder=3,marker="o")
    ax.text(val+(3 if val>=0 else -3),i,f"{val:+.0f}%",va="center",
            ha="left" if val>=0 else "right",fontsize=8.5,color=colmap[cls])
ax.axvline(0,color="black",lw=1)
ax.axvspan(-130,0,color=OKABE["blue"],alpha=0.05,zorder=0)

# Hansen 001 estimates (A1 RBC + A2 honest CIs)
hoff=len(studies_sorted)+0.8
hrows=[("Hansen 0.08 (001 A1/A2) — consistent","0.08",hoff+2),
       ("Hansen 0.15 strict > (001 A1/A2) — consistent","0.15_strict",hoff+1),
       ("Hansen 0.15 statutory ≥ (001 A1/A2) — consistent*","0.15_statutory",hoff+0)]
for lab,key,yy in hrows:
    r=rel[key]
    ax.plot([r["A2_lo"],r["A2_hi"]],[yy,yy],color=OKABE["orange"],lw=3,alpha=0.35,zorder=4,solid_capstyle="butt")
    ax.plot([r["A1_lo"],r["A1_hi"]],[yy,yy],color=OKABE["orange"],lw=3,zorder=5,solid_capstyle="butt")
    ax.scatter(r["A1"],yy,color=OKABE["orange"],edgecolor="black",s=90,zorder=6,marker="s")
    ax.text(-132,yy,lab,va="center",ha="left",fontsize=8.3,fontweight="bold",color=OKABE["orange"])
ax.axhline(len(studies_sorted)-0.4,color="black",lw=0.6,ls=":")
ax.text(55,hoff+2.7,"model prediction: DETER (−)\n→ all 3 sign-consistent\n(*0.15 statutory: 001 CI incl. 0)",
        fontsize=8.5,color=OKABE["orange"],ha="center")

# Finlay 2024 (monetary-only): CANNOT be placed on a relative-% axis -> annotate, not a 0% point
ax.text(-132,-0.85,"Finlay 2024 (monetary class): conviction-count bounds,\n"
        "no relative effect → sign-model only, NOT plotted at 0%.",
        fontsize=7.8, color=OKABE["gray"], ha="left", va="center")

ax.set_xlim(-135,130); ax.set_ylim(-1.3,hoff+3.4)
ax.set_xlabel("Relative effect of the HARSHER sanction on reoffending (%)  —  negative = deters")
ax.set_yticks(list(y)+[r[2] for r in hrows])
ax.set_yticklabels([s[0] for s in studies_sorted]+["","",""],fontsize=8.5)
leg=[Patch(fc=OKABE["blue"],label="severity / certainty, no record change"),
     Patch(fc=OKABE["green"],label="record change — DUI-specific"),
     Patch(fc=OKABE["verm"],label="record change — general crime"),
     Line2D([0],[0],color=OKABE["orange"],marker="s",lw=3,label="Hansen (001) A1 RBC CI; faint=A2 honest CI")]
ax.legend(handles=leg,loc="lower right",fontsize=8,framealpha=0.95)
ax.set_title("Which sanction margins deter? Post-2015 evidence vs Hansen (out of sample)")
fig.savefig(f"{OUT}/fig_margins_forest.png",facecolor="white"); plt.close(fig)
print("fig_margins_forest.png (Finlay corrected) written")

# ---------------- FIG: Utah .05 ----------------
ut=pd.read_csv(f"{OUT}/utah_bac_shares.csv")
fig,ax=plt.subplots(figsize=(8,4.6))
fy=ut["fiscal_year"].values; sh=ut["share_005_007_of_reported"].values*100
cols=[OKABE["gray"] if y<2019 else (OKABE["yellow"] if y==2019 else OKABE["orange"]) for y in fy]
ax.bar(fy,sh,color=cols,zorder=3)
for x,yv in zip(fy,sh): ax.text(x,yv+0.2,f"{yv:.1f}",ha="center",fontsize=8)
ax.axvline(2018.5,color=OKABE["verm"],lw=1.5,ls="--",zorder=4)
ax.text(2018.6,10.5,".05 law effective\n2018-12-30 (mid-FY19)",fontsize=8.5,color=OKABE["verm"],va="top")
ax.axhline(scal["utah_share_before"]*100,color=OKABE["gray"],lw=1,ls=":")
ax.axhline(scal["utah_share_after"]*100,color=OKABE["orange"],lw=1,ls=":")
ax.set_xlabel("Utah fiscal year"); ax.set_ylabel("Share of reported-BAC DUI arrests in .05–.07 (%)")
ax.set_title("Utah .05 per se law: .05–.07 arrest share (partly MECHANICAL, not deterrence)")
leg=[Patch(fc=OKABE["gray"],label=f"pre-law FY16–18 (mean {scal['utah_share_before']*100:.1f}%)"),
     Patch(fc=OKABE["yellow"],label="FY19 transition"),
     Patch(fc=OKABE["orange"],label=f"post-law FY20–25 (mean {scal['utah_share_after']*100:.1f}%)")]
ax.legend(handles=leg,loc="upper left",fontsize=8.5,framealpha=0.95); ax.set_ylim(0,12.5)
fig.savefig(f"{OUT}/fig_utah_005.png",facecolor="white"); plt.close(fig)
print("fig_utah_005.png written")
