---
layout: method
title: "Double Machine learning"
parent: "Causal ML"
date: 2025-09-19
author: Andrea Zampetti, Sapienza University of Rome, reviewed by Pierre Gaüzère, CNRS
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Description & principle 

Double (or debiased) machine learning (DML) is a causal effect estimation framework introduced by Chernozhukov et al. (2018). It uses machine learning (ML) to control for a high-dimensional set of confounders and obtain unbiased estimates of target parameters. The aim is to isolate a causal effect (for example, the linear coefficient on the path $T \rightarrow Y$, where $T$ is the treatment or causal variable of interest, and $Y$ is the outcome) while controlling for multiple confounding variables that affect both the treatment and the outcome. For example:

$$
Y = \theta_0 T + g_0(X) + \zeta

T = m_0(X) + V
$$


Where  $Y$ is the outcome variable, $T$ is the causal variable of interest, $X$ is the high-dimensional vector consisting of confounding covariates, and $\zeta$ and $V$ are error terms. Both the outcome and the treatment are affected by confounding variables through so-called nuisance functions ($g_0$ and $m_0$, respectively), which can be highly non-linear and could bias the estimation process of the causal path, if not properly accounted for. The goal is to isolate $\theta_0$, the path coefficient on $T \rightarrow Y$, by estimating the nuisance functions through flexible ML learners, which are not bound to parametric forms and can thus adapt to complex scenarios. To obtain $\theta_0$, double ML proceeds in two stages: 

1. First, it uses ML regressors to predict both $Y$ from $T$ and $T$ from $X$. Then, it extracts residuals from the two models (orthogonalization): those represent the variation in the treatment and in the outcome that is not explained by the confounders. 
2. Finally, it regresses the two sets of residuals: the slope of the regression represents the causal effect coefficient $\theta_0$. 

Since ML algorithms are highly flexible to non-parametric relationships, they can adapt to many scenarios where the confounders exhibit complex effects through $g_0$ and $m_0$. To avoid overfitting and to ensure that errors in the first stage do not bias the second stage, the orthogonalization procedure undergoes repeated sample-splitting and K-fold cross-fitting, where nuisance functions are learned on training folds and used to predict held-out folds. Any flexible ML algorithm can be used for nuisance estimation, making it broadly applicable to a wide range of scenarios: examples include lasso, [random forests, boosted trees, neural networks](/contents/methods/ecology-guided/predictive_models/), or ensembles of these methods.

### Major variants
{: .no_toc }
- **Partially Linear Regression (PLR):** models the outcome as a linear function of the treatment and a flexible (i.e. non-linear) function of covariates
- **PLR with Instrument Variables (PLR-IV):** same as PLR, but uses instrumental variables to address endogeneity in the treatment variable
- **Interactive Regression Model (IRM):** extension of PLR to allow interaction between treatment and covariates
- **IRM with Instrument Variables (IRM-IV):** IRM combined with instrumental variables to address endogeneity in the treatment variable


### Further online resources
{: .no_toc }
- User guide: [https://docs.doubleml.org/stable/guide/guide.html](https://docs.doubleml.org/stable/guide/guide.html){:target="_blank"}
- Estimating causal effects with machine learning: A guide for  ecologists {% cite arif2025estimating  %}
- Blog post: [https://matheusfacure.github.io/python-causality-handbook/22-Debiased-Orthogonal-Machine-Learning.html](https://matheusfacure.github.io/python-causality-handbook/22-Debiased-Orthogonal-Machine-Learning.html){:target="_blank"}


## Reference articles
### Method
{: .no_toc }
- {% cite_resource chernozhukov2018double  --style _bibliography/narrative %}
- {% cite_resource bach2022doubleml  --style _bibliography/narrative %}
- {% cite_resource bach2024doubleml  --style _bibliography/narrative %}

### Research applications
{: .no_toc }
#### With RS data in Ecology / Biodiversity
{: .no_toc }
- {% cite_resource jian2025identification  --style _bibliography/narrative %}

#### Without RS data (Ecology domain)
{: .no_toc }
- {% cite_resource fink2023double --style _bibliography/narrative %}

## Implementation 

#### Python
{: .no_toc }
- **DoubleML:** official Python library, developed by {% cite bach2022doubleml  --style _bibliography/narrative %}. Documentation at [https://docs.doubleml.org/stable/](https://docs.doubleml.org/stable/){:target="_blank"}
- **EconML:** Microsoft’s official library, developed for causal econometrics. Documentation at [https://www.pywhy.org/EconML/](https://www.pywhy.org/EconML/){:target="_blank"}

#### R
{: .no_toc }
- **DoubleML:** twin version of the official Python library in R, developed by {% cite bach2024doubleml  --style _bibliography/narrative %}. Documentation at [https://docs.doubleml.org/r](https://docs.doubleml.org/r) and [https://cran.r-project.org/web/packages/DoubleML/index.html](https://cran.r-project.org/web/packages/DoubleML/index.html){:target="_blank"}
- **causalDML:** R package for double ML frameworks in binary or multiple treatments scenario, based on {% cite heiler2021effect  --style _bibliography/narrative %} and {% cite knaus2022double  --style _bibliography/narrative %}. GitHub page [https://github.com/MCKnaus/causalDML](https://github.com/MCKnaus/causalDML){:target="_blank"}
- **dmlmt:** R package for double ML frameworks in multiple treatments scenario, based on {% cite farrell2015robust --style _bibliography/narrative %} and {% cite knaus2022double  --style _bibliography/narrative %}. GitHub page [https://github.com/MCKnaus/dmlmt](https://github.com/MCKnaus/dmlmt){:target="_blank"}

### Code Cells
{: .no_toc }
- R tutorial vignette: [https://cran.r-project.org/web/packages/DoubleML/vignettes/getstarted.html](https://cran.r-project.org/web/packages/DoubleML/vignettes/getstarted.html){:target="_blank"}
- Python/R tutorial vignette: [https://docs.doubleml.org/stable/intro/intro.html](https://docs.doubleml.org/stable/intro/intro.html){:target="_blank"}
- Python/R worked examples: [https://docs.doubleml.org/stable/examples](https://docs.doubleml.org/stable/examples){:target="_blank"}


<!-- For referencement in toc before automatic table -->
## Assessment table
