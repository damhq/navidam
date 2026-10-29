import json,pandas as pd,matplotlib;matplotlib.use("Agg")
import matplotlib.pyplot as plt
g=pd.DataFrame(json.load(open("near_miss.json")))
cols=dict(zip([.05,.1,.2,.3],plt.cm.viridis([.05,.35,.6,.85])))
fig,ax=plt.subplots(1,2,figsize=(10,4.2))
for e,c in cols.items():
    d=g[g.e==e]
    ax[0].plot(d.k_spec,d.strict_recall,"--",color=c,lw=1.2,marker="o",ms=3,alpha=.7)
    ax[0].plot(d.k_spec,d.near_recall,"-",color=c,lw=2.2,marker="o",ms=4,label=f"{e:.0%}")
ax[0].set_ylabel("Recall (correct method within suggested set)");ax[0].set_ylim(0,1.03)
ax[0].legend(title="Proportion of randomized criteria",ncol=4,fontsize=8,loc="lower left",frameon=False)
ax[0].set_title("Solid: strict + near misses; dashed: strict only",fontsize=9)
d=g[g.e==.1]
ax[1].plot(d.k_spec,d.strict_size_mean,"--",color="#0072B2",marker="o",ms=3,label="Strict")
ax[1].plot(d.k_spec,d.near_size_mean,"-",color="#0072B2",lw=2.2,marker="o",ms=4,label="Strict + near misses")
ax[1].set_yscale("log");ax[1].set_ylabel("Mean number of suggested methods [log scale]")
ax[1].set_title("Cost of near misses (10% randomized)",fontsize=9);ax[1].legend(frameon=False,fontsize=8)
for a in ax: a.set_xlabel("Number of specified criteria");a.grid(color="#e6e6e6",lw=.6)
plt.tight_layout();plt.savefig("near_miss.png",dpi=100)
