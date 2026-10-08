import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd, json, numpy as np

RES = "/workspace/eval/followup/002-methods-and-transport/results"
OKABE = ["#0072B2","#E69F00","#009E73","#D55E00","#CC79A7","#56B4E9","#F0E442","#000000"]
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"savefig.bbox":"tight",
    "font.size":11,"axes.titlesize":12,"axes.labelsize":11,
    "axes.spines.top":False,"axes.spines.right":False,"axes.grid":True,"grid.alpha":0.25})

bw = pd.read_csv(f"{RES}/bandwidth_curve.csv")
scal = json.load(open(f"{RES}/headline_scalars.json"))
H = scal["headline"]

panels = [("0.08","statutory","0.08  (statutory ≥)", H["0.08_statutory"]["A1"]["h"], (-0.021,-0.019)),
          ("0.15","statutory","0.15  (statutory ≥)", H["0.15_statutory"]["A1"]["h"], (-0.010,-0.011)),
          ("0.15","strict","0.15  (strict >)", H["0.15_strict"]["A1"]["h"], (-0.010,-0.011))]

fig, axes = plt.subplots(1,3, figsize=(13,4.3), sharey=False)
for ax,(thr,cod,title,hopt,paper) in zip(axes,panels):
    d = bw[(bw.threshold==float(thr))&(bw.coding==cod)&(bw.kernel=="triangular")].sort_values("h")
    ax.axhline(0,color="#888",lw=0.9,ls="--")
    ax.fill_between(d.h, d.ci_rbc_lo, d.ci_rbc_hi, color=OKABE[0], alpha=0.18, label="RBC 95% CI")
    ax.plot(d.h, d.est_conv, color=OKABE[0], lw=1.8, label="conventional est.")
    ax.axvline(hopt,color=OKABE[2],lw=1.2,ls=":",label=f"MSE-opt h={hopt:.3f}")
    # paper points at bw 0.05 and 0.025
    ax.scatter([0.05,0.025],[paper[0],paper[1]], color=OKABE[1], zorder=5, s=45, marker="D", label="paper (Table 3/4)")
    ax.set_title(title); ax.set_xlabel("bandwidth h (BAC units)")
    ax.set_xlim(0.009,0.069)
axes[0].set_ylabel("RD estimate on 4-yr recidivism")
h1,l1 = axes[0].get_legend_handles_labels()
axes[0].legend(fontsize=8.5, loc="lower left", framealpha=0.9)
fig.suptitle("A3 bandwidth curve: WA 1999–2007 recidivism RD under 2026 inference (triangular kernel)", y=1.02, fontsize=12.5)
fig.savefig(f"{RES}/fig_bandwidth_curve.png", facecolor="white")
print("saved fig_bandwidth_curve.png")

# ---- eras figure ----
era = pd.read_csv(f"{RES}/eras.csv")
fig, axes = plt.subplots(1,2, figsize=(12,4.3))
paper_pooled = {0.08:-0.021, 0.15:-0.010}
for ax,thr in zip(axes,[0.08,0.15]):
    yr = era[(era.threshold==thr)&(era.estimator=="A0_year")].copy()
    yr["y"]=yr.period.astype(int)
    yr=yr.sort_values("y")
    ax.axhline(0,color="#888",lw=0.9,ls="--")
    ax.axhline(paper_pooled[thr],color=OKABE[1],lw=1.4,ls="-",label=f"paper pooled ({paper_pooled[thr]})")
    ax.errorbar(yr.y, yr.est, yerr=1.96*yr.se, fmt="o-", color=OKABE[0], capsize=3, label="A0 by year (±95% CI)")
    # era points A0
    er = era[(era.threshold==thr)&(era.estimator=="A0")]
    for _,row in er.iterrows():
        xr = [1999,2003] if row.period.startswith("1999") else [2004,2007]
        ax.hlines(row.est, xr[0],xr[1], color=OKABE[3], lw=2.5, alpha=0.8,
                  label="era A0" if row.period.startswith("1999") else None)
    ax.set_title(f"{thr} threshold (statutory)"); ax.set_xlabel("year")
axes[0].set_ylabel("RD estimate on 4-yr recidivism")
axes[0].legend(fontsize=8.5, loc="lower left")
fig.suptitle("A5 over-time structure: year-by-year and era A0 estimates vs paper pooled", y=1.02, fontsize=12.5)
fig.savefig(f"{RES}/fig_eras.png", facecolor="white")
print("saved fig_eras.png")
