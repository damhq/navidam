---
layout: method
title: "Matching methods"
parent: "Quasi-experiments"
date: 2026-02-27
author: Diana Bowler, UK Centre for Ecology & Hydrology, 27th Feb 2026
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
Statistical matching is one of several related propensity score (PS) methods (see the [Weighting method]({{ site.baseurl }}/contents/methods/quasi-exps/weighting-and-propensity-scores/){:target="_blank"} for a more general description of PS). These methods are attractive since they are intuitive: they broadly aim to reverse-engineer quasi-experimental conditions out of observational data. Essentially, PS are the modelled probability that a sampling unit receives the treatment conditional on a set of covariates. The usual aim of statistical matching is to pair treated sampling units with one or more control units with similar propensity scores. Matching is most suited for testing the effects of interventions since they are most well-developed for binary treatments. In ecology, these are commonly used in studies of the effectiveness of protected areas {% cite andam2008measuring ribas2020global %}. Matching is already used informally in field study designs e.g. to identify comparable control sites to compare against an intervention/impact site.

Various matching algorithms are available that affect the quality of the matching. The *nearest neighbour algorithm* pairs treated units with its nearest untreated unit in terms of propensity scores. It is described as ‘greedy’ since pairing occurs sequentially and does not aim to optimize total distances across all pairs. The most typical matching order is to begin with the highest propensity score so that potentially difficult-to-match units are matched first. *Optimal matching* is a non-greedy option that does seek to minimize the distance between all pairs, but can be time-consuming and often yields similar results. A “caliper width” can be specified that determines the maximum tolerable difference between the treated and matched untreated units, which can improve performance but also result in more discarded unmatched units that exceed the width. Such choices often trade-off bias and variance of the derived estimand i.e., closer matching might reduce bias but increase variance when units are discarded. Matching with replacement can overcome the problem of unmatched treated units by reusing untreated units as controls but decreases the effective sample size.

The propensity scores themselves are usually estimated using either simple logistic regression, with treated or not as the response, or a more complex machine learning algorithm e.g. random forest or boosted regression tree. The roles of variables in the system determine which should be included in the PS model. To reduce bias, the key variables should be those affecting both the treatment and the outcome, since they create confounding effects causing bias. Additionally, variables related only to the outcome are often included – to reduce variance rather than bias {% cite ramsey2019using --style _bibliography/narrative %}. Variables only related to the treatment are less helpful to include since they have no effect on bias and can increase variance {% cite ramsey2019using --style _bibliography/narrative %}.

Covariate balance plots are a useful part of the workflow when using PS methods. Covariate balance is the degree to which the distribution of covariates is similar across levels of the treatment. Covariate balance plots essentially compare the distribution of confounder covariate variables in the treated and untreated units. Before analysis, the distributions of the raw values can help identify confounders with the largest difference in covariate distributions. Poor balance may arise due to systematic bias or simply by chance due to low sample size. Covariate balance plots can also be used after matching to assess how successfully they have reduced potential confounding.

### Advantages and limitations
{: .no_toc }
Matching reduces model dependence on correct assumptions about confounder relationships (e.g., whether they are linear or interact with other variables) since analysis is done on matched data in which the covariate distributions are balanced. 

If there is strong placement bias of the treatment, some treated units may not have any similar untreated units, meaning no data are available to inform on treatment effects in some parts of the covariate space. This means that it might not be possible to draw inference about the whole population (i.e., average treatment effect, ATE). The ATT, average treatment effect at treated units, is a good estimand if all treated units can be paired with an untreated unit. To achieve this, matching works best when there are more untreated units than treated units, because all treated units can be matched. 

The region where there is overlap in the covariate distributions between treated and untreated units is called the ‘region of common support’ {% cite schafer2008average %}. Through typical workflows for PS methods, the region of common support is clearly assessed, allowing clear reporting on limits of inference. By contrast, traditional regression can lead to extrapolation of results into regions with no supporting evidence.

Like other propensity score methods, matching is only suitable when data are available on confounding variables. They can lead to bias if there are unmeasured confounding variables, but they can still be useful if these unmeasured variables are correlated with observed variables.  Matching is more commonly used with a binary treatment, although continuous treatments can be stratified, and there is ongoing development of approaches for continuous treatments {% cite brown2021propensity fong2018covariate hirano2004propensity %}.

Even if the same statistical results are obtained, PS methods such as matching offer a purpose and transparency to communicate the robustness and generalizability of causal effect estimates that do not emerge from traditional regression workflows.



### Major variants
{: .no_toc }
Matching can be applied with weighing to target different estimands e.g., ATT or ATE.
For dynamic systems, propensity scores might be allowed to vary over time, with matching repeated at multiple time units e.g., using [PanelMatch](https://cran.r-project.org/web/packages/PanelMatch/index.html){:target="_blank"}.

### Further online resources
{: .no_toc }

- [MatchIt: Nonparametric Preprocessing for Parametric Causal Inference](https://kosukeimai.github.io/MatchIt/){:target="_blank"}
- [Chapter 14 - Matching, The Effect](https://theeffectbook.net/ch-Matching.html){:target="_blank"}



## Reference articles
### Method
{: .no_toc }
- {% cite_resource ramsey2019using --style _bibliography/narrative %} presented the first review of propensity score methods in ecology and highlighted the importance of treatment heterogeneity as a scenario when propensity score methods outperform multiple regression.


### Research applications
{: .no_toc }

- {% cite_resource andam2008measuring --style _bibliography/narrative %}
- {% cite_resource ribas2020global --style _bibliography/narrative %}
- {% cite_resource schleicher2020statistical --style _bibliography/narrative %}
- {% cite_resource ribas2021estimating --style _bibliography/narrative %}
- {% cite_resource ramsey2019using --style _bibliography/narrative %}
- {% cite_resource butsic2017quasiexperimental --style _bibliography/narrative %}

## Implementation 


#### R
{: .no_toc }
- [MatchIt](https://kosukeimai.github.io/MatchIt/){:target="_blank"}: offers a range of matching algorithms
- [optmatch](https://cran.r-project.org/web/packages/optmatch/index.html){:target="_blank"}: offers a range of matching algorithms
- [cobalt](https://cran.r-project.org/web/packages/cobalt/index.html){:target="_blank"}: creating covariate balance tables and plots.
- [PanelMatch](https://cran.r-project.org/web/packages/PanelMatch/index.html){:target="_blank"}: for matching in dynamic systems.


### Code Cells
{: .no_toc }
{: .d-inline-block }
optional
{: .label}


<!-- For referencement in toc before automatic table -->
## Assessment table
