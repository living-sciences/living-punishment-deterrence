import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd, numpy as np
RES="/workspace/eval/followup/002-methods-and-transport/results"
WS="/workspace/eval/followup/002-methods-and-transport/workspace"
OK=["#0072B2","#E69F00","#009E73","#D55E00","#CC79A7","#56B4E9","#F0E442","#000000"]
plt.rcParams.update({"figure.dpi":150,"savefig.dpi":150,"savefig.bbox":"tight","font.size":11,
    "axes.titlesize":12,"axes.labelsize":11,"axes.spines.top":False,"axes.spines.right":False,
    "axes.grid":True,"grid.alpha":0.25})

fl=pd.read_csv(f"{WS}/data/fl_analysis.csv")
full=pd.read_parquet(f"{WS}/data/fl_tests_deid.parquet")

# ---- B3: histogram of FL running variable with thresholds ----
fig,ax=plt.subplots(figsize=(8,4.3))
ax.hist(fl.run_min, bins=np.arange(0,0.401,0.002), color=OK[0], alpha=0.85)
for c,lab in [(0.08,"0.08 (per se)"),(0.15,"0.15 (enhanced)")]:
    ax.axvline(c,color=OK[3],lw=1.5,ls="--"); ax.text(c+0.002,ax.get_ylim()[1]*0.9,lab,color=OK[3],fontsize=9)
ax.set_xlabel("running variable = min(sample1, sample2) BrAC (g/210L)")
ax.set_ylabel("Florida two-sample DUI tests")
ax.set_title("B3  Florida 2021–2026 breath-test BAC distribution (n=116,934)")
fig.savefig(f"{RES}/fig_florida_hist.png",facecolor="white"); print("hist ok")

# ---- B3: refusal share by month ----
full["ym"]=full.test_ym
g=full.groupby("ym").agg(refusal=("refusal_flag","mean"),n=("refusal_flag","size")).reset_index()
g=g[g.ym!="NA"].sort_values("ym")
fig,ax=plt.subplots(figsize=(10,3.6))
x=range(len(g))
ax.plot(x,100*g.refusal,color=OK[0],lw=1.4)
ax.set_xticks(list(x)[::3]); ax.set_xticklabels(g.ym[::3],rotation=90,fontsize=7)
ax.set_ylabel("refusal share (%)"); ax.set_title("B3  Florida breath-test refusal share by month")
ax.set_ylim(0,30)
fig.savefig(f"{RES}/fig_florida_refusal.png",facecolor="white"); print("refusal ok")

# ---- B4: FL vs WA density comparison (small multiples with MDD) ----
dens=pd.read_csv(f"{RES}/density_tests.csv")
dd=dens[(dens.test=="rddensity_jk")&(dens.year=="pooled")&(dens.state.isin(["WA","FL"]))]
fig,axes=plt.subplots(1,2,figsize=(11,4.3))
for ax,thr in zip(axes,[0.08,0.15]):
    sub=dd[dd.threshold==thr]
    labels=[];
    for i,st in enumerate(["WA","FL"]):
        r=sub[sub.state==st].iloc[0]
        ax.errorbar(i, r.log_density_jump, yerr=1.96*(r.ldj_ci_hi-r.log_density_jump)/1.96,
                    fmt="o",color=OK[1] if st=="FL" else OK[0],capsize=4,ms=8)
        ax.errorbar(i, r.log_density_jump, yerr=[[r.log_density_jump-r.ldj_ci_lo],[r.ldj_ci_hi-r.log_density_jump]],
                    fmt="o",color=OK[1] if st=="FL" else OK[0],capsize=4,ms=8)
        labels.append(f"{st}\np={r.p:.2f}\nMDD={r.MDD:.2f}")
    ax.axhline(0,color="#888",ls="--",lw=0.9)
    ax.set_xticks([0,1]); ax.set_xticklabels(labels,fontsize=9)
    ax.set_title(f"log-density jump at {thr}")
    ax.set_xlim(-0.5,1.5)
axes[0].set_ylabel("log-density jump (McCrary-type)")
fig.suptitle("B4  FL vs WA (2026 tests): no-sorting test at both thresholds (95% CIs)",y=1.02,fontsize=12.5)
fig.savefig(f"{RES}/fig_fl_vs_wa_density.png",facecolor="white"); print("fl_vs_wa ok")
