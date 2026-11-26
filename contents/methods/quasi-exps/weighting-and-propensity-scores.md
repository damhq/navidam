---
layout: method
title: "Weighting & Propensity scores"
parent: "Quasi-experiments"
date: 2026-03-05
author: Diana Bowler, UK Centre for Ecology & Hydrology
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

**Propensity score methods**

Propensity score (PS) methods are part of the Potential Outcomes
Framework for causal inference, which involves estimating the
hypothetical outcomes for sampling units with and without treatment to
estimate the causal effect of a treatment. Essentially, PS are the
modelled probability that a sampling unit receives a treatment
conditional on a set of covariates. These PS can be used in three
related but different approaches - matching, weighting, and
stratification/subclassification - that all aim to balance the covariate
distributions between treated and untreated units, reducing the impact
of confounding variables and bias in causal estimates.

Typically, there are two steps in the analysis:

1. a PS model, with treatment assignment as the response and
2. an outcome model, with the causal outcome variable as the response, that makes use of the PS scores
   (modelled treatment assignment probabilities from the PS model).

By
producing a single PS score, PS methods can integrate the effects of
multiple confounders into a single variable, making them applicable for
small datasets with many confounders. Propensity score methods do,
however, require the same assumption of no unmeasured confounding as
regression. PS methods can be used with any sort of spatial or temporal
data, but it must be considered whether the propensity scores remain
constant over time in a dynamic system.

The roles of variables in the system determine whether they should be
included in the PS (treatment probability) model. To reduce bias, the
key variables are those affecting both the treatment and the outcome,
since they create confounding effects leading to bias. Additionally,
variables related only to the outcome are often included – to reduce
variance rather than bias {% cite ramsey2019using --style _bibliography/narrative %}. Variables only related to the
treatment are less helpful to include since they have no effect on bias
and can increase variance {% cite ramsey2019using --style _bibliography/narrative %}, which can be explained by
leading to more accurately modelling treatment assignment probability
and pushing them towards zero or one. DAGs help identify which variables
have confounding potential, and which should be included in the PS model
to reduce bias and increase precision.

Propensity score methods have multiple advantages over traditional
covariate adjustment within multiple regression (Table 1). The main
advantage is explicit covariate balancing to reduce confounding, which
is at the heart of propensity score methods. Moreover, the PS approach
is practical since the bias-inducing effects of many confounders are
integrated and adjusted for by a single set of PS. Since covariate
balancing is done prior to estimating the causal effect of interest, PS
methods are also less sensitive to correct model specification e.g.,
whether confounder effects are linear, non-linear or interactive than
traditional regression {% cite ho2007matching --style _bibliography/narrative %}.

Another set of advantages is related to the transparency of the
generalizability of estimated effects. PS methods require specification
of an estimand of interest. In conservation, the target estimand is
often either the ATE (average treatment effects across all units) or the
ATT (average treatment effect across treated units), but the estimand is
rarely specified if causal inference approaches are not used. When
causal inference approachs, such as PS methods, are used, then weights
can be used to target any estimand of interest. If there is strong
placement bias of the treatment, some treated units may not have any
similar untreated units, meaning no data are available to inform on
treatment effects in some parts of the covariate space. The region where
there is overlap in the covariate distributions is the ‘region of common
support’ {% cite schafer2008average --style _bibliography/narrative %}. Through typical workflows for PS
methods, the region of common support is clearly assessed, which helps
report clear statements on limits of inference. By contrast, traditional
regression can lead to extrapolation of results into regions with no
supporting evidence, which is not made explicit then the results are
reported.

Even if the same statistical results are obtained, PS methods offer a
purpose and transparency to communicate the robustness and
generalizability of causal effect estimates that do not emerge from
traditional regression workflows.

**Weighting methods**

Weighting methods use the propensity scores to balance covariates across
treatment groups and target an estimate for a specific population (e.g.,
ATE - average treatment effect - or ATT - average treatment effect of
the treated). They do this by directly using the propensity scores to
weight data points in the model. Data points are weighted differently
depending on whether they are control or treatment group and which
estimand is desired. For the ATE, each unit is weighted based on the
inverse of their probability of receiving the treatment they actually
received i.e., for treated sites, the probability of being treated and
for control sites the probability of not being treated.

The advantage of weighting is that all sampled units can be used, unlike
with matching. Moreover, the target estimand can be the average
treatment effect (ATE) or the ATT. For the ATE, every individual must
have some non-zero probability of receiving the treatment. However,
extreme weights, caused by very low or high probabilities of being
treated, can reduce effective sample size and make the outputs sensitive
to extremes. The approach is also more sensitive to model
misspecification than matching. Weights with low variability are
desirable because they improve the precision of the estimator. This
variability is presented in several ways, but the most important is the
effective sample size (ESS) computed from the weights, which we hope is
as close to the original sample size as possible. Weight trimming is
often applied to reduce the variability of treatment effect estimates by
down-weighting or removing units that have extreme weights. The survey
package can be used to estimate robust SEs incorporating weights and
strata.

Propensity score methods are suitable when data are available on
confounding variables. They can still lead to bias if there are
unmeasured confounding variables, but we note that if these unmeasured
variables are correlated with observed variables, they can still be
useful.

Subclassication is a related method: the propensity scores are used to
divide the sample into strata of subclass, usually based on its
quantiles. The causal estimates are produced by comparing the treated
and untreated units within each strata, and the separate estimates are
then aggregated across strata. During the aggregation step,
stratum-specific weights can be used to calculate different estimands of
interest e.g., the ATE or ATT, even if some units are discarded. Because
the propensity scores are grouped into strata, covariance balance is
only approximate and imbalance can remain within the strata. Narrower
strata would lead to greater balance, but might result in discarded
units (e.g., if they are in a strata without multiple treatment levels).
However, compared to matching, subclassification usually leads to fewer
discarded units. Subclassification is a simple and transparent approach
to deal with covariate imbalance and non-random treatment
assignment.Subclassification approaches also lend themselves to studying
treatment effect heterogeneity, if treatment effects are allowed to vary
by strata in the outcome model (e.g., with a treatment-strata
interaction term). In this case, subclassification can increase the
precision of the estimated causal effects.

Propensity scores can also be used to derive a more representative
estimate for a population from an unrepresentative sample e.g., when
estimating biodiversity trends for a region. MrP (multi-level regression
with post-stratification) is commonly used in social surveys, involving
first estimating strata-specific effects of interest (in which the
strata are defined by the PS and then taking a weighted mean of these
effects according to the representation of the strata in the target
population.

## Further online resources
{: .no_toc }
- [Weighting for Covariate Balance in Observational Studies • WeightIt](https://ngreifer.github.io/WeightIt/){:target="_blank"}

## Reference articles

### Method
{: .no_toc }

- {% cite_resource ramsey2019using --style _bibliography/narrative %}

### Research applications
{: .no_toc }
- {% cite_resource ramsey2019using --style _bibliography/narrative %}

- {% cite_resource butsic2017quasiexperimental --style _bibliography/narrative %}

- {% cite_resource fink2023double --style _bibliography/narrative %}

- {% cite_resource boyd2025using --style _bibliography/narrative %}

## Implementation

#### R
{: .no_toc }
- [WeightIt](https://cran.r-project.org/web/packages/WeightIt/refman/WeightIt.html){:target="_blank"} – Flexible package for generating weights (including IPTW, ATT, overlap, and more) using various methods (logistic, GBM, etc.) - modern workflows

- [CBPS](https://cran.r-project.org/web/packages/CBPS/refman/CBPS.html){:target="_blank"} – Covariate Balancing Propensity Scores: directly targets covariate balance when estimating weights.

- [survey](https://cran.r-project.org/web/packages/survey/refman/survey.html){:target="_blank"}/[srvyr](https://cran.r-project.org/web/packages/srvyr/refman/srvyr.html){:target="_blank"} - functions to add design weights (known weights that stem from the sampling design) or propensity score weights (unknown weights derived from the available data) in glm models.

- [PSweight](https://cran.r-project.org/web/packages/PSweight/refman/PSweight.html){:target="_blank"}: This package offers a comprehensive platform for propensity score weighting.

- [cobalt](https://cran.r-project.org/web/packages/cobalt/refman/cobalt.html){:target="_blank"}: This package is useful for creating covariate balance tables and plots.

- [twang](https://cran.r-project.org/web/packages/twang/refman/twang.html){:target="_blank"}: uses generalized boosted models to estimate propensity scores and provides tools for assessing balance and creating weights.

## Assessment table
