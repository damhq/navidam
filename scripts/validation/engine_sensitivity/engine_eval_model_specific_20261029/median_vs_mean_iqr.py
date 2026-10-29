import pandas as pd,numpy as np,matplotlib;matplotlib.use("Agg")
import matplotlib.pyplot as plt
d=pd.read_csv("benchmark_runs.csv");B="#0072B2"
ks=sorted(d.k_spec.unique())
g=[d[d.k_spec==k]["size"].values for k in ks]
med=[np.median(s) for s in g];m=[s.mean() for s in g]
q=np.array([np.percentile(s,[25,75]) for s in g])
fig,ax=plt.subplots(1,2,figsize=(11,4.5),sharey=True)
ax[0].plot(ks,med,"o-",c=B);ax[0].set_title("Median, IQR")
ax[1].plot(ks,m,"o-",c=B);ax[1].set_title("Mean, IQR")
for a in ax:
    a.fill_between(ks,q[:,0],q[:,1],color=B,alpha=.2)
    a.set_yscale("log");a.set_xlabel("Number of specified criteria");a.grid(alpha=.3)
ax[0].set_ylabel("Number of suggested methods [log scale]")
plt.tight_layout();plt.savefig("median_vs_mean_iqr.png",dpi=90)
