---
layout: method
title: "GAMs"
parent: "Linear regressions & extensions"
date: 2025-11-18
author: Luca Santini, Sapienza University of Rome
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

<!-- category-note:start -->

{: .note }
This method also belongs to [Adjusted methods (Backdoor C.)]({{ site.baseurl }}/adjusted).

<!-- category-note:end -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Description & principle 
Generalized Additive Models (GAMs) are semi-parametric extensions of Generalized Linear Models (GLMs) that allow the inclusion of smooth functions to describe the relationship between predictors and the response variable. The shape of each effect is estimated from the data while balancing goodness of fit and smoothness to avoid overfitting.

Smooth functions are typically estimated using penalized regression splines. These are constructed from sets of basis functions (e.g., cubic splines), whose flexibility is controlled by both the basis dimension and a roughness penalty. The placement of knots is handled automatically, and users specify only the maximum complexity of each smoother through the basis dimension k.

The degree of smoothness is regulated by a penalty on the wiggliness of the function, scaled by a smoothing parameter λ. This parameter determines how strongly departures from smoothness are penalized. λ is usually estimated automatically during model fitting, commonly via Generalized Cross-Validation (GCV) or via Restricted Maximum Likelihood (REML).

In ecological time-series applications, the choice of smoothing should still be checked explicitly rather than treated as purely automatic. A commonly cited rule of thumb is to limit the effective flexibility of the smoother relative to the length of the series, for example by setting the maximum basis dimension to roughly one third of the number of sampling years, then verifying that the fitted trend is not driven by short-term noise rather than the signal of interest. This pragmatic guidance is often traced to {% cite fewster2000analysis --style _bibliography/narrative %}, but it should be treated as a starting point for sensitivity analysis rather than as a universal rule.

GAMs has an additive structure, where the linear predictor is the sum of smooth functions of the explanatory variables, and the response variable is linked to this predictor via the chosen link function. Interactions can also be modeled, either between smooth and parametric terms or between smooth terms. In the latter case, tensor-product smooths are often employed, particularly when interacting variables have different scales. As in GLMs, GAMs allow for various error families and link functions (e.g., Binomial, Poisson, Gamma).

As with collinearity in GLMs, GAMs can suffer from identifiability issues due to concurvity, a nonlinear form of dependence between predictors or smooths. Concurvity should be assessed, as high concurvity levels may affect interpretability and model stability.



### Further online resources
{: .no_toc }

- [https://m-clark.github.io/generalized-additive-models/index.html](https://m-clark.github.io/generalized-additive-models/index.html)
- [https://www.ncrm.ac.uk/resources/online/all/?id=20851](https://www.ncrm.ac.uk/resources/online/all/?id=20851)


## Reference articles
### Method
{: .no_toc }
- {% cite_resource hastie1986generalized  --style _bibliography/narrative %}
- {% cite_resource hastie1992generalized  --style _bibliography/narrative %}
- {% cite_resource fewster2000analysis  --style _bibliography/narrative %}

### Research applications
{: .no_toc }
#### With RS data in Ecology / Biodiversity
{: .no_toc }

- {% cite_resource park2008quantitative  --style _bibliography/narrative %}
- {% cite_resource frescino2001modeling  --style _bibliography/narrative %}
- {% cite_resource opsomer2007modelassisted  --style _bibliography/narrative %}
- {% cite_resource wang2017application  --style _bibliography/narrative %}

#### Without RS data (Ecology domain)
{: .no_toc }
{: .d-inline-block }
optional
{: .label}

- {% cite_resource guisan2002generalized  --style _bibliography/narrative %}
- {% cite_resource suarez-seoane2002largescale  --style _bibliography/narrative %}
- {% cite_resource dimarco2023elevational  --style _bibliography/narrative %}
- {% cite_resource conenna2021global  --style _bibliography/narrative %}

## Implementation 

#### Python
{: .no_toc }

- [pyGAM](https://pygam.readthedocs.io/en/latest/){:target="_blank"}
- [Statsmodels](https://www.statsmodels.org/stable/index.html){:target="_blank"}
- [pymgcv](https://smoothforge.github.io/pymgcv/){:target="_blank"}


#### R
{: .no_toc }
- [mgcv: Mixed GAM Computation Vehicle with Automatic Smoothness Estimation](https://cran.r-project.org/web/packages/mgcv/index.html){:target="_blank"}
- [gam: Generalized Additive Models](https://cran.r-project.org/web/packages/gam/index.html){:target="_blank"}


<!-- For referencement in toc before automatic table -->
## Assessment table
