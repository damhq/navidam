import json, sys, numpy as np, matplotlib, matplotlib.ticker
from pathlib import Path
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
matplotlib.use("Agg")
import matplotlib.pyplot as plt
summary_path = Path(sys.argv[1]) if len(sys.argv) > 1 else (
    Path(__file__).resolve().parent
    / "engine_sensitivity"
    / "engine_eval_model_specific_20261029"
    / "summary.json"
)
with summary_path.open(encoding="utf-8") as f:
    r = json.load(f)
required_summary_fields = {
    "ordinal_criteria",
    "multiple_criteria",
    "multiple_option_criterion_power",
    "triple_option_criterion_power",
}
missing_summary_fields = required_summary_fields - r.keys()
if missing_summary_fields:
    raise SystemExit(
        f"{summary_path} predates the multiple-option analysis; "
        "rerun engine_sensitivity.py to regenerate it."
    )
B,O,INK,MUT="#0072B2","#D55E00","#222222","#6b6b6b"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":8.5,"axes.edgecolor":"#9a9a9a","axes.labelcolor":INK,"xtick.color":MUT,"ytick.color":MUT,"axes.spines.top":False,"axes.spines.right":False})
fig=plt.figure(figsize=(7.2,7.4))
gs=fig.add_gridspec(2,2,height_ratios=[1,1.15],hspace=.52,wspace=.35)
# (a)
a=fig.add_subplot(gs[0,0]); bs=r["by_specification"]
k=[d["k_mean"] for d in bs]; med=[d["size_median"] for d in bs]
a.fill_between(k,[d["size_q25"] for d in bs],[d["size_q75"] for d in bs],color=B,alpha=.18,lw=0,label="Interquartile range")
a.plot(k,med,color=B,lw=2,marker="o",ms=5,label="Median",zorder=3)
a.plot(k,[d["size_mean"] for d in bs],color="#56B4E9",lw=.9,ls=(0,(3,2)),marker="s",ms=2.5,alpha=.8,label="Mean",zorder=2)
h,l=a.get_legend_handles_labels(); o=[l.index(x) for x in ("Median","Interquartile range","Mean")]
a.legend([h[i] for i in o],[l[i] for i in o],loc="center right",bbox_to_anchor=(1.0,np.log(1000**.5/.55)/np.log(80/.55)),fontsize=6.5,frameon=False,handlelength=1.8)
for x,y,u in zip(k,med,[d["size_one"] for d in bs]):
    if u>0.1: a.annotate(f"{u:.0%}",(x,y),xytext=((-16,-10) if x<10 else (0,-14)),textcoords="offset points",ha="center",fontsize=7,color=MUT)
a.text(24,50**.5,"labels: share of simulations\nwith only the true method left",ha="right",va="center",fontsize=6.5,color=MUT)
a.set_xlabel("Number of specified criteria"); a.set_ylabel("Number of suggested methods\n[log scale]")
a.text(0.5,-0.205,"(in addition to the fixed objective)",transform=a.transAxes,ha="center",va="top",fontsize=6.5,color=MUT)
a.set_title("a  Output size vs. specification",loc="left",fontsize=9,fontweight="bold",color=INK)
a.grid(axis="y",color="#e6e6e6",lw=.6); a.set_yscale("log"); a.set_ylim(0.55,80); a.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter()); a.set_yticks([1,2,5,10,20,50])
# (b)
b=fig.add_subplot(gs[0,1])
ep=r["error_propagation"]
es=[.05,.15,.3]
e_colors=dict(zip(es,plt.cm.viridis([.05,.5,.85])))
for e in es:
    pts=sorted((d["k_mean"],d["recall"]) for d in ep if d["e"]==e)
    b.plot([0]+[x[0] for x in pts],[1]+[x[1] for x in pts],color=e_colors[e],lw=2,marker="o",ms=4.5)
nm_path=summary_path.parent/"near_miss.json"
nm=json.load(nm_path.open()) if nm_path.exists() else []
for e in es:
    pts=sorted((d["k_spec"],d["near_recall"]) for d in nm if d["e"]==e)
    if pts: b.plot([0]+[x[0] for x in pts],[1]+[x[1] for x in pts],color=e_colors[e],lw=.9,ls=(0,(1.5,1.5)),marker="s",ms=2.5,alpha=.85)
b.set_xlabel("Number of specified criteria"); b.set_ylabel("Recall\n(correct method within suggested set)")
b.text(0.5,-0.205,"(in addition to the fixed objective)",transform=b.transAxes,ha="center",va="top",fontsize=6.5,color=MUT)
b.set_ylim(0,1.03); b.grid(axis="y",color="#e6e6e6",lw=.6)
b.set_title("b  Error propagation",loc="left",fontsize=9,fontweight="bold",color=INK)
b.legend(handles=[Line2D([0],[0],color=e_colors[e],lw=2,marker="o",ms=4.5,label=f"{e:.0%}") for e in es],
         title="Proportion of randomized criteria",title_fontsize=7,alignment="left",
         frameon=False,fontsize=6.5,loc="upper left",bbox_to_anchor=(0.0,-0.27),ncol=3,columnspacing=1.0,handlelength=1.6)
if nm:
    b.add_artist(b.get_legend())
    b.legend(handles=[Line2D([0],[0],color=MUT,lw=2,marker="o",ms=4.5,label="Strict matches"),
                            Line2D([0],[0],color=MUT,lw=.9,ls=(0,(1.5,1.5)),marker="s",ms=2.5,label="Incl. near misses")],
                   frameon=False,fontsize=6.5,loc="lower left",handlelength=2.2,borderaxespad=.2)
SHIFT=-.055  # top row shifted left so it looks centered
for ax in (a,b):
    p=ax.get_position(); ax.set_position([p.x0+SHIFT,p.y0,p.width,p.height])
# (c)
c=fig.add_subplot(gs[1,:])
lab={"Fonctional form":"Functional form","Handles huge datasets (n)":"Handles huge datasets","Propaguates uncertainty":"Propagates uncertainty","Common support (positivity)":"Common support","Minimal TS length":"Time-series length","Type":"Data type","Causal Markov Condition":"Causal Markov condition"}
sp=r["single_criterion_power"]
multiple_power=r.get("multiple_option_criterion_power",{})
triple_power=r.get("triple_option_criterion_power",{})
names=list(sp)[::-1]
labels=[lab.get(name,name) for name in names]
vals=[sp[name] for name in names]
multiple_color="#E69F00"
triple_color="#CC79A7"
c.barh(range(len(names)),vals,color=B,height=.68,zorder=2)
for i,name in enumerate(names):
    if name in multiple_power:
        c.barh(i,multiple_power[name]["removed"],color=multiple_color,height=.68,zorder=3)
    if name in triple_power:
        c.barh(i,triple_power[name]["removed"],color=triple_color,height=.68,zorder=4)
    c.text(vals[i]+.008,i,f"{vals[i]:.0%}",va="center",fontsize=6.5,color=MUT)
c.set_yticks(range(len(names)),labels)
type_colors={"Multiple":"#2d7a4a","Ordinal":"#6c4f99"}  # same as website tags
for tick,name in zip(c.get_yticklabels(),names):
    criterion_type=(
        "Ordinal" if name in r.get("ordinal_criteria",[])
        else "Multiple" if name in r.get("multiple_criteria",[])
        else None
    )
    if criterion_type is None:
        raise ValueError(f"No Multiple/Ordinal type recorded for criterion {name!r}.")
    tick.set_color(type_colors[criterion_type])
c.set_xlabel("Share of objective-compatible methods excluded when only this criterion is specified")
c.set_xlim(0,1.15); c.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0)); c.tick_params(axis="y",labelsize=7); c.grid(axis="x",color="#e6e6e6",lw=.6)
c.set_title("c  Filtering power by criterion",loc="left",fontsize=9,fontweight="bold",color=INK)
leg_sel=c.legend(handles=[
    Patch(facecolor=B,label="1"),
    Patch(facecolor=multiple_color,label="2"),
    Patch(facecolor=triple_color,label="3"),
],title="Number of selected options",title_fontsize=7,frameon=False,fontsize=6.5,loc="upper left",bbox_to_anchor=(0,-0.2),ncol=3,alignment="left")
c.add_artist(leg_sel)
c.legend(handles=[
    Patch(facecolor=type_colors["Multiple"],label="Multiple"),
    Patch(facecolor=type_colors["Ordinal"],label="Ordinal"),
],title="Criterion type",title_fontsize=7,frameon=False,fontsize=6.5,loc="upper left",bbox_to_anchor=(0.3,-0.2),ncol=2,alignment="left")
output_dir = summary_path.parent
fig.savefig(output_dir / "Fig4_engine_evaluation.png", dpi=300, bbox_inches="tight")
fig.savefig(output_dir / "Fig4_engine_evaluation.pdf", bbox_inches="tight")
