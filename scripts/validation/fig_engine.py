import json, sys, matplotlib, matplotlib.ticker
matplotlib.use("Agg")
import matplotlib.pyplot as plt
r=json.load(open(sys.argv[1] if len(sys.argv)>1 else "engine_eval/summary.json"))
B,O,INK,MUT="#2a78d6","#eb6834","#222222","#6b6b6b"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":8.5,"axes.edgecolor":"#9a9a9a","axes.labelcolor":INK,"xtick.color":MUT,"ytick.color":MUT,"axes.spines.top":False,"axes.spines.right":False})
fig=plt.figure(figsize=(7.2,7.4))
gs=fig.add_gridspec(2,2,height_ratios=[1,1.15],hspace=.75,wspace=.35)
# (a)
a=fig.add_subplot(gs[0,0]); bs=r["by_specification"]
k=[d["k_mean"] for d in bs]; med=[d["size_median"] for d in bs]
a.fill_between(k,[d["size_q25"] for d in bs],[d["size_q75"] for d in bs],color=B,alpha=.18,lw=0)
a.plot(k,med,color=B,lw=2,marker="o",ms=5)
for x,y,u in zip(k,med,[d["size_one"] for d in bs]):
    if u>0.1: a.annotate(f"{u:.0%}",(x,y),xytext=(0,8),textcoords="offset points",ha="center",fontsize=7,color=MUT)
a.text(17.5,9,"labels: share of studies\nwith a single candidate",ha="right",fontsize=6.5,color=MUT)
a.set_xlabel("Criteria specified by the user (mean)"); a.set_ylabel("Candidate methods returned")
a.set_title("a  Output size vs. specification",loc="left",fontsize=9,fontweight="bold",color=INK)
a.grid(axis="y",color="#e6e6e6",lw=.6); a.set_ylim(0,None)
# (b)
b=fig.add_subplot(gs[0,1])
ep=r["error_propagation"]
om={(d["e"],d["p_spec"]):d["recall"] for d in r["omission_errors"]}
es=[0,.05,.1,.2,.3]
for p,col,lab in [(.25,B,"~4 criteria"),(1.0,O,"all criteria (~17)")]:
    b.plot([e*100 for e in es],[next(d["recall"] for d in ep if d["e"]==e and d["p_spec"]==p) for e in es],color=col,lw=2,marker="o",ms=5,label=f"{lab}, contradictory errors")
    b.plot([e*100 for e in es],[om[(e,p)] for e in es],color=col,lw=2,ls="--",marker="s",ms=4.5,label=f"{lab}, omission errors")
b.set_xlabel("Assessment error rate per cell (%)"); b.set_ylabel("Recall of a correct method")
b.set_ylim(0,1.03); b.grid(axis="y",color="#e6e6e6",lw=.6)
b.set_title("b  Error propagation",loc="left",fontsize=9,fontweight="bold",color=INK)
b.legend(frameon=False,fontsize=6.5,loc="upper center",bbox_to_anchor=(0.45,-0.22),ncol=1)
# (c)
c=fig.add_subplot(gs[1,:])
lab={"Fonctional form":"Functional form","Handles huge datasets (n)":"Handles huge datasets","Propaguates uncertainty":"Propagates uncertainty","Common support (positivity)":"Common support","Minimal TS length":"Time-series length","Type":"Data type","Causal Markov Condition":"Causal Markov condition"}
sp={lab.get(k,k):v for k,v in r["single_criterion_power"].items()}
names=list(sp)[::-1]; vals=[sp[n] for n in names]
c.barh(names,vals,color=B,height=.68)
for i,v in enumerate(vals): c.text(v+.008,i,f"{v:.0%}",va="center",fontsize=6.5,color=MUT)
c.set_xlabel("Share of objective-compatible methods excluded when only this criterion is specified")
c.set_xlim(0,1); c.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0)); c.tick_params(axis="y",labelsize=7); c.grid(axis="x",color="#e6e6e6",lw=.6)
c.set_title("c  Filtering power of single criteria",loc="left",fontsize=9,fontweight="bold",color=INK)
fig.savefig("Fig4_engine_evaluation.png",dpi=300,bbox_inches="tight"); fig.savefig("Fig4_engine_evaluation.pdf",bbox_inches="tight")
