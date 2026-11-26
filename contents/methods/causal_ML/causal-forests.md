---
layout: method
title: "Causal forests"
parent: "Causal ML"
date: 2025-11-18
author: Franziska Schrodt, University of Nottingham, reviewed by Mickaël Hedde, INRAE Montpellier
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Description & principle 
Causal Forest models are a machine learning technique that extends traditional Random Forests to estimate conditional average treatment effects (CATE) in causal inference settings. The core principle behind causal forests is to estimate the causal effect of a treatment or intervention on an outcome, but with the added nuance of heterogeneity, i.e., how this effect might vary across different subpopulations or individuals.

A key strength of causal forests is that they do not assume a homogeneous treatment effect across all units in the data, unlike many classical methods such as linear regression. Instead, they use decision trees to partition the data into subgroups with distinct treatment effects. Aggregating over many trees yields flexible, data-driven estimates of how effects vary. The model typically produces an effect estimate for each observation, often loosely called the Individual Treatment Effect (ITE). Strictly, this is the CATE for a unit with that observation's covariate values, rather than the effect for that unit alone.

When are causal forests useful? They are most useful when a "treatment" has been applied to some units and not others, when you have many covariates that might modify its effect, and when you do not know in advance which of them matter. Typical situations include:

- **Policy interventions:** for example, whether the designation of a protected area reduced deforestation, and whether the effect differs with accessibility, land tenure, or forest type.
- **Management practices:** for example, whether prescribed burning, grazing exclusion, or habitat restoration increased species richness, and where it worked best.
- **Environmental changes:** for example, whether exposure to drought, warming, or land-use change altered vegetation cover or abundance, and which sites were most vulnerable.

Classical approaches such as linear regression typically report a single average effect, or require the analyst to specify interactions in advance. Causal forests are preferable when the goal is to discover where, and for whom, an intervention works, for example to target conservation funding at the sites where it will have the greatest impact.

Whilst Causal Forests are a promising method for application in ecology, there are some limitations. Biodiversity change often involves feedback, lagged effects, and nonstationarity, which are not straightforward to model with standard causal forests designed for static “treatment” settings. While causal forests can adjust for confounders, remote-sensing data and ecological covariates are noisy, and the assumptions of unconfoundedness may not hold easily.


### Major variants
{: .no_toc }

1. **Generalized Random Forests {% cite athey2019generalized %}:**
Generalized Random Forests (GRF) is a framework that generalizes the causal forest method to handle a wider range of causal inference tasks, such as instrumental variable analysis, quantile treatment effects, and more. GRF is highly flexible and allows for user-defined loss functions and non-standard data structures.

2. **Bayesian Causal Forest:**
A Bayesian variant of causal forests that uses a probabilistic model to estimate treatment effects, incorporating uncertainty into the estimates. This approach provides a more robust measure of uncertainty around causal effect estimates.

3. **Targeted Causal Forests:**
A more recent variant that focuses on improving the accuracy of treatment effect estimation in high-dimensional settings by using targeted regularization. This approach is especially useful when the number of covariates is large.


### Further online resources
{: .no_toc }
- Blog explaining Causal Forests applications to Social Science/clinical data: [https://lorentzen.ch/index.php/2024/09/02/explaining-a-causal-forest/](https://lorentzen.ch/index.php/2024/09/02/explaining-a-causal-forest/){:target="_blank"}
- Causal Inference and Machine Learning Blog detailing many machine learning based approaches, including causal forests: [https://causalml.readthedocs.io/en/latest/](https://causalml.readthedocs.io/en/latest/){:target="_blank"}
- Generalised Random Forest R package and tutorial with good, detailed examples and explanations: [https://grf-labs.github.io/grf/](https://grf-labs.github.io/grf/){:target="_blank"}


## Reference articles
### Method
{: .no_toc }
- {% cite_resource athey2016recursive --style _bibliography/narrative %}
- {% cite_resource athey2019generalized --style _bibliography/narrative %}
- {% cite_resource jawadekar2023practical --style _bibliography/narrative %}
- {% cite_resource rehill2024how --style _bibliography/narrative %}
- {% cite_resource arif2025estimating --style _bibliography/narrative %}

### Research applications
{: .no_toc }

#### With RS data in Ecology / Biodiversity
{: .no_toc }
- {% cite_resource defries2022improved --style _bibliography/narrative %}: Direct example of combining remote sensing outcomes with causal-forest estimation to infer treatment effects on forest condition in the Amazon (socio-ecological study)

#### Without RS data (Ecology domain)
{: .no_toc }
- {% cite_resource arif2025estimating --style _bibliography/narrative %}: Applied case study of causal forests: What is the effect of depth on Laminaria digitata across Atlantic Canada?
- {% cite_resource hodler2023institutions --style _bibliography/narrative %}: Large-N econometric application showing how causal forests are used for spatial heterogeneity and policy effect heterogeneity (Economics rather than Ecology)
- {% cite_resource crommelynck2025fiscal --style _bibliography/narrative %}: Protection effect on population and fiscal outcomes. Combined with difference-in-difference and matching approaches (socio-economic study)


## Implementation 

#### Python
{: .no_toc }
- [CausalML](https://causalml.readthedocs.io/en/latest/about.html){:target="_blank"}: A Python library for causal machine learning, including support for causal forests.
- [EconML](https://www.pywhy.org/EconML/){:target="_blank"}: Another Python package developed by Microsoft that implements generalized random forests and other causal inference methods.
- [GRF (Generalized Random Forests)](https://pypi.org/project/skgrf/){:target="_blank"}: A Python wrapper for the GRF R package.
- [Causalfe](https://github.com/haytug/causalfe){:target="_blank"}: a Python package implementing causal forests with fixed effect for the analysis of panel data

#### R
{: .no_toc }
- [grf](https://grf-labs.github.io/grf/){:target="_blank"}: R package implementing generalized random forests.
- [causalTree](https://github.com/susanathey/causaltree){:target="_blank"}: An older, simpler R package for causal trees (related to causal forests).
- [twang](https://cran.r-project.org/web/packages/twang/index.html){:target="_blank"}: R package for estimating causal treatment effects using random forests among other techniques.


<!-- For referencement in toc before automatic table -->
## Assessment table
