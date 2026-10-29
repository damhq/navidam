import pandas as pd,numpy as np,matplotlib;matplotlib.use("Agg")
import matplotlib.pyplot as plt
d=pd.read_csv("benchmark_runs.csv");rng=np.random.default_rng(1)
ks=sorted(d.k_spec.unique());B="#0072B2"
fig,ax=plt.subplots(1,2,figsize=(11,4.5),sharey=True)
med=[];q=[];m=[];ci=[]
for k in ks:
    s=d[d.k_spec==k].size.values if False else d[d.k_spec==k]["size"].values
    med.append(np.median(s));q.append(np.percentile(s,[25,75]));m.append(s.mean())
    bs=rng.choice(s,(2000,len(s))).mean(1);ci.append(np.percentile(bs,[2.5,97.5]))
q=np.array(q);ci=np.array(ci)
ax[0].plot(ks,med,"o-",c=B);ax[0].fill_between(ks,q[:,0],q[:,1],color=B,alpha=.2)
ax[0].set_title("Median, IQR")
ax[1].plot(ks,m,"o-",c=B);ax[1].fill_between(ks,ci[:,0],ci[:,1],color=B,alpha=.3)
ax[1].set_title("Mean, bootstrap 95% CI (CI very narrow)")
for a in ax:
    a.set_yscale("log");a.set_xlabel("Number of specified criteria");a.grid(alpha=.3)
ax[0].set_ylabel("Number of suggested methods [log scale]")
plt.tight_layout();plt.savefig("/tmp/cmp1.png",dpi=90)
print(np.c_[ks,m,ci])
