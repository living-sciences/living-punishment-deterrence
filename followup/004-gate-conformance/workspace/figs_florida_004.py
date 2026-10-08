import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd, numpy as np
RES="/workspace/eval/followup/004-gate-conformance/results"
WS="/workspace/eval/followup/004-gate-conformance/workspace"
OK=["#0072B2","#E69F00","#009E73","#D55E00","#CC79A7","#56B4E9","#F0E442","#000000"]
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"savefig.bbox":"tight","font.size":12,
    "axes.titlesize":13,"axes.labelsize":12,"axes.spines.top":False,"axes.spines.right":False,
    "axes.grid":True,"grid.alpha":0.25})

fl=pd.read_csv(f"{WS}/data/fl_analysis.csv")
n=len(fl)

# ---- FIG: histogram of FL running variable (deduplicated) ----
fig,ax=plt.subplots(figsize=(7.5,4.3))
ax.hist(fl.run_min, bins=np.arange(0,0.401,0.002), color=OK[0], alpha=0.85)
for c,lab in [(0.08,"0.08 (per se)"),(0.15,"0.15 (enhanced)")]:
    ax.axvline(c,color=OK[3],lw=1.5,ls="--"); ax.text(c+0.003,ax.get_ylim()[1]*0.9,lab,color=OK[3],fontsize=9)
ax.set_xlabel("running variable = min(sample1, sample2) BrAC (g/210L)")
ax.set_ylabel("Florida two-sample DUI tests")
ax.set_title(f"Florida 2021–2026 breath-test BAC (deduplicated, n={n:,})")
fig.savefig(f"{RES}/fig_florida_hist.png",facecolor="white"); plt.close(fig); print("hist ok", n)

# ---- FIG: FL vs WA no-sorting transport check (log-density jump + CI) ----
cmp=pd.read_csv(f"{RES}/fl_vs_wa_comparison.csv")
fig,ax=plt.subplots(figsize=(7.5,4.5))
ys=[1.0,0.0]  # 0.08 top, 0.15 bottom offset
labels=["0.08 threshold","0.15 threshold"]
for i,row in cmp.iterrows():
    base=i*1.6
    # FL (orange) and WA (blue), offset
    ax.errorbar(row.FL_logjump,[base+0.18],xerr=[[row.FL_logjump-row.FL_lo],[row.FL_hi-row.FL_logjump]],
                fmt="s",color=OK[1],capsize=4,ms=8,label="Florida 2021–2026 (this study, dedup)" if i==0 else None)
    ax.errorbar(row.WA_logjump,[base-0.18],xerr=[[row.WA_logjump-row.WA_lo],[row.WA_hi-row.WA_logjump]],
                fmt="o",color=OK[0],capsize=4,ms=8,label="Washington 1999–2007 (same rddensity)" if i==0 else None)
    ax.text(0.30, base+0.18, f"p={row.FL_p:.3f}, MDD={row.FL_MDD:.3f}", fontsize=8.5, color=OK[1], va="center")
    ax.text(0.30, base-0.18, f"p={row.WA_p:.3f}, MDD={row.WA_MDD:.3f}", fontsize=8.5, color=OK[0], va="center")
ax.axvline(0,color="black",lw=1)
ax.set_yticks([0.0,1.6]); ax.set_yticklabels(labels)
ax.set_xlim(-0.30,0.72)
ax.set_xlabel("log-density jump at threshold (rddensity), 95% CI  —  0 = no sorting")
ax.set_title("No-sorting transport check: Florida vs Washington")
ax.legend(loc="lower right",fontsize=8.5,framealpha=0.95)
fig.savefig(f"{RES}/fig_fl_vs_wa_density.png",facecolor="white"); plt.close(fig); print("fl_vs_wa ok")
