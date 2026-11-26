---
layout: method
title: "GLMMs, GAMMs"
parent: "Linear regressions & extensions"
date: 2025-11-09
author: Andrea Zampetti, Sapienza University of Rome
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Description & principle 
Generalized Linear Mixed Models (GLMMs; Breslow & Clayton, 1993) and Generalized Additive Mixed Models (GAMMs; Lin & Zhang, 1999) extend [GLMs]({{ site.baseurl }}/contents/methods/ecology-guided/linear_regressions/glms-gees/){:target="_blank"} and [GAMs]({{ site.baseurl }}/contents/methods/ecology-guided/linear_regressions/gams/){:target="_blank"} by incorporating random effects, which account for non-independence and hierarchical structure in the modelled data. In real-world monitoring scenarios, observations are rarely independent: species counts come from repeated visits to the same site, plots are nested within regions, or individuals are observed across years. Ignoring these structures can lead to biased parameter estimates and misleading inference (Figure 1). To mitigate this issue, GLMMs and GAMMs integrate random components (i.e. random intercepts and/or slopes) that help separate within-group variation from between-group variations, reducing pseudoreplication and improving estimates for the predictors of interest (which in a mixed-effects model are called fixed effects). This allows disentangling the true signals of fixed effects from noise and unmeasured heterogeneity associated with grouping factors or hierarchical structure in the data. 

![]({{ site.baseurl }}/assets/images/GLMM_GAMM.png)
<a name="fig-glmm"></a>

**Figure 1**  A visual representation of the “Simpson paradox”, which arises when the direction of an association between two variables changes drastically upon accounting for group-level structure in the data ({% cite simpson1951interpretation --style _bibliography/narrative %}). In (A), a single regression is fitted on the whole data, showing a clear negative relationship between predictor variable $x$ and response variable $y$. In (B) however, when accounting for the grouped structure of the observations by fitting group-specific regression lines, the nature of the relationship changes in sign. This illustrates how ignoring underlying group structure can lead to misleading conclusions about the overall relationship between variables. In this case, while the pooled data suggests a negative association between $x$ and $y$, the within-group relationships are actually positive. A comparable mixed-model example arises with repeated observations on the same individuals: a pooled regression can confound between-individual differences with within-individual effects, whereas mixed models help separate these two components ({% cite vandepol2009simple --style _bibliography/narrative %}).


Specifically, **random intercepts** allow each group specified in the random effect structure to have its own baseline for the response (Figure 2A): 

$$
y_i= a_j+ bx_i
$$

Where $y$ and $x$ are, respectively the response and predictor variables for the $i$th observation, $b$ is the coefficient representing the effect of the predictor on the response (the slope coefficient in linear models), and $a_j$ is the group-specific intercept, usually sampled from a Normal distribution $N(0, \sigma_a^2)$. Hence, different groups can have higher or lower baseline values than the overall mean, capturing group-specific offsets. In addition to random intercepts, mixed-effects models can also accommodate **random slopes** that allow each group specified in the random effect structure to have varying effects of the predictor on the response (Figure 2B):

$$
y_i= a_j+ b_j x_i
$$

Where $b_j$ is the group-specific slope, usually sampled from a Normal distribution $N(0,\sigma_b^2)$. The examples reported in these two equations and in Figure 2 are referring for simplicity and ease of visualization to a linear mixed-effects model (LMM) which assumes that the response variable is continuous and normally-distributed; however, the same principles apply to GLMMs (through the use of link functions to allow for different distributions in the response variable; see [GLMs]({{ site.baseurl }}/contents/methods/ecology-guided/linear_regressions/glms-gees/){:target="_blank"}) and GAMMs (through the use of smooth terms that allow non-linear trends between predictors and the response variable; see [GAMs]({{ site.baseurl }}/contents/methods/ecology-guided/linear_regressions/gams/){:target="_blank"}).

![]({{ site.baseurl }}/assets/images/GLMM_GAMM2.png)
<a name="fig-glmm2"></a>

**Figure 2**  Visual representations of random intercepts and random slopes in a simple linear mixed-effects model (LMM) predicting the effect of variable $x$ on the response $y$. Here, $\mu_{\text{group}}$ is the regression line fitted on the overall data, and $a_n$ are the group-specific regression lines based on the specified random effects structure. In panel (A) only random intercepts are specified, so that each group has its own baseline, but all groups share the same slope (i.e. same effect of the predictor $x$ on the response $y$). In panel (B), both random intercepts and random slopes are used, which results in each group having its own baseline and effect on the response variable $y$. Image taken from Harrison et al. (2018).



### Major variants
{: .no_toc }

- **Distribution families**: supported in most GLMM/GAMM software and allow modelling of different types of response variables. The most common include:
    - Gaussian: for continuous, normally distributed response
    - Binomial: for binary outcomes (0/1) or proportions
    - Poisson: for count data where variance ≈ mean
    - Negative Binomial/Quasi-Poisson: for count data with over-dispersion (variance > mean)
    - Gamma: for continuous positive and skewed data
    - Beta: for continuous proportions bounded between 0 and 1
    - Tweedie: for flexible mean-variance relationships
- **Zero-inflated variants**: available for many of the above families (Poisson, Binomial, Negative Binomial,…), allow to account for excess zeros in the response
- **Bayesian GLMMs and GAMMs**: the same family structure applies, but inference is conducted through Bayesian methods (i.e. prior distributions can be specified for parameters to be estimated) instead (or in addition to) maximum likelihood (ML) or restricted maximum likelihood (REML).




### Further online resources
{: .no_toc }

- [*A simple method for distinguishing within- versus between-subject effects using mixed models*](https://doi.org/10.1016/j.anbehav.2008.11.006){:target="_blank"} {% cite vandepol2009simple %}
- [*Fitting Linear Mixed-Effects Models Using lme4*](https://doi.org/10.18637/jss.v067.i01){:target="_blank"} {% cite bates2015fitting %}
- [*Hierarchical generalized additive models in ecology: An introduction with mgcv*](https://doi.org/10.7717/peerj.6876){:target="_blank"} {% cite pedersen2019hierarchical %}
- [*An Introduction to Linear Mixed-Effects Modeling in R*](https://doi.org/10.1177/2515245920960351){:target="_blank"} {% cite brown2021introduction %}


## Reference articles
### Method
{: .no_toc }
- *Approximate Inference in Generalized Linear Mixed Models* {% cite breslow1993approximate %}
- *Inference in Generalized Additive Mixed Models by Using Smoothing Splines* {% cite lin1999inference %}
- *Generalized Linear Mixed Models: A Practical Guide for Ecology and Evolution* {% cite bolker2009generalized %}
- *Mixed Effects Models and Extensions in Ecology with R* {% cite zuur2009mixed %}
- *A Brief Introduction to Mixed Effects Modelling and Multi-Model Inference in Ecology* {% cite harrison2018brief %}


### Research applications
{: .no_toc }
Since their introduction, GLMMs and GAMMs became nearly ubiquitous in ecology and biodiversity monitoring thanks to their ability in dealing with the inherent hierarchy typical of biological systems. Thus, it is difficult to identify specific research applications since they are used across a wide range of systems, taxa and monitoring applications. Below, only a small sample is proposed:

#### With RS data in Ecology / Biodiversity
{: .no_toc }
- {% cite_resource caughlin2016integrating  --style _bibliography/narrative %}
- {% cite_resource rickbeil2018changing  --style _bibliography/narrative %}
- {% cite_resource saunders2022unraveling  --style _bibliography/narrative %}
- {% cite_resource sommerfeld2018patterns  --style _bibliography/narrative %}
- {% cite_resource stevens-rumann2018evidence  --style _bibliography/narrative %}

#### Without RS data (Ecology domain)
{: .no_toc }
- {% cite_resource benitez-lopez2010impacts  --style _bibliography/narrative %}
- {% cite_resource falaschi2025differences  --style _bibliography/narrative %}
- {% cite_resource ingersoll2016effects  --style _bibliography/narrative %}
- {% cite_resource santini2018global  --style _bibliography/narrative %}
- {% cite_resource venter2018bias  --style _bibliography/narrative %}

## Implementation 

#### Python
{: .no_toc }
- [statsmodels](https://www.statsmodels.org/){:target="_blank"}: supports mixed-effects modelling, including linear mixed models and some Bayesian generalized mixed-model workflows.
- [Pymer4](https://eshinjolly.com/pymer4/){:target="_blank"}: Python interface to the classic `lme4`-style R backend for mixed models.
- [GPBoost](https://gpboost.readthedocs.io/en/latest/){:target="_blank"}: combines tree-based learning and mixed-effects components.
- [Bambi](https://bambinos.github.io/bambi/){:target="_blank"} and [PyMC](https://www.pymc.io/){:target="_blank"}: Bayesian mixed-effects modelling libraries for Python.

#### R
{: .no_toc }
- [lme4](https://cran.r-project.org/package=lme4){:target="_blank"}: standard R package for LMMs and GLMMs.
- [glmmTMB](https://cran.r-project.org/package=glmmTMB){:target="_blank"}: supports zero-inflated and otherwise extended GLMM formulations.
- [mgcv](https://cran.r-project.org/package=mgcv){:target="_blank"}: standard R package for GAMs and GAMMs.
- [gamm4](https://cran.r-project.org/package=gamm4){:target="_blank"}: combines `mgcv` smooths with `lme4` random-effects syntax.
- [brms](https://paulbuerkner.com/brms/){:target="_blank"}, [rstanarm](https://mc-stan.org/rstanarm/){:target="_blank"}, and [blme](https://cran.r-project.org/package=blme){:target="_blank"}: Bayesian extensions for mixed-effects modelling in R.

### Code Cells
{: .no_toc }
- [R tutorial vignette for LMMs and GLMMs using lme4](https://cran.r-project.org/web/packages/lme4/vignettes/lmer.pdf){:target="_blank"}
- [R tutorial vignette for zero-inflated GLMMs using glmmTMB](https://cran.r-project.org/web/packages/glmmTMB/vignettes/glmmTMB.pdf){:target="_blank"}
- [R introduction for GAMMs using mgcv](https://r.qcbs.ca/workshop08/book-en/introduction-to-generalized-additive-mixed-models-gamms.html){:target="_blank"}
- [R detailed application vignette of GAMMs to time-series data using mgcv](https://jacolienvanrij.com/Tutorials/GAMM.html){:target="_blank"}
- [R tutorial vignette for Bayesian LMMs using brms](https://www.r-bloggers.com/2019/09/bayesian-linear-mixed-models-random-intercepts-slopes-and-missing-data/){:target="_blank"}
- [Python tutorial vignette for LMMs using statsmodels](https://www.statsmodels.org/stable/mixed_linear.html){:target="_blank"}


<!-- For referencement in toc before automatic table -->
## Assessment table
