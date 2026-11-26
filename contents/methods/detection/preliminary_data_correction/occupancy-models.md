---
layout: method
title: "Occupancy models"
parent: "Preliminary data correction"
date: 2025-11-18
author: Diana Bowler, reviewed by Mickaël Hedde (INRAE) and Lisa Nicvert (FRB-CESAB)
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

{% if page.category_note != '' %}
{: .note }
This method also belongs to [Ecology-guided Modelling]({{ site.baseurl }}/ecology-guided).
{% endif %}


## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Description & principle 

Occupancy models – or Occupancy-detection models — aim to account for imperfect detection of species observations. Species observation data can suffer from two main forms of imperfect detection: false absences — when a species present at a site is not detected during a survey, and false positives — when a species is not present at a site but is erroneously reported as detected (e.g., due to misidentification). The primary focus of occupancy models is the first form of imperfect detection i.e., false absences (but see major variants below for models that have been extended to accommodate the second form). 

Occupancy models explicitly model detection probability, allowing separation of the ecological process (true occurrence) from the observation process (detection). Predictions can be interpreted in absolute terms — as estimates of species occurrence probability — rather than in relative terms, like classic SDMs such as Maxent, that ‘only’ estimate relative occurrence probabilities. Detection probability can be modelled with covariates, so that unbiased occurrence probabilities can be obtained even when detection probability varies across sites, observers or sampling effort.

Statistically, an occupancy model comprises two linked models: 
- A model for detection probability that estimates the probability of detecting a species (𝑝)  given it is present; 
- And a model for occupancy probability (𝜓), used to describe the true presence/absence state (a latent variable, typically represented as 𝑧). 

At their simplest, these two models have the form of a binomial GLM. Both the true state ($z$) and the detection probability ($p$) influences the observed species detection data  ($y$), as follows:

- **Occupancy state model:**

$$
\begin{aligned}
z_i &\sim \operatorname{Bernoulli}(\psi_i) \\
\operatorname{logit}(\psi_i) &= \beta_0 + \beta_1 \cdot \text{covariate}
\end{aligned}
$$

- **Detection model:**

$$ 
\begin{aligned}
y_{ij} \mid z_i &\sim \operatorname{Bernoulli}(p_i \cdot z_i) \\
\operatorname{logit}(p_{ij}) &= \alpha_0 + \alpha_1 \cdot \text{covariate}
\end{aligned}
$$

Where $i$ represents the index for a site, and $j$ represents the index of the visit for this site.


![]({{ site.baseurl }}/assets/images/occupancy_scheme.png)
<a name="fig-occupancy"></a>


Occupancy models estimate detection probabilities using data collected over repeated visits during a period of closure, when the true state is not assumed to change. For instance, a bird monitoring program might conduct 3 visits to each site during the breeding season. Detection probability is estimated using the frequency of times that a species is detected over the repeat visits. The final occupancy probabilities are higher than the observed frequencies of species since they adjust for the missed detections. Occupancy probability estimates might also be above zero at sites where species were never detected, especially if species detection probabilities are low.


The key assumptions are that the true occurrence of each species does not change over the visits (i.e. closure during the repeat surveys), and that the detections at each visit are independent of each other. Hence, the main data requirement is that there are repeated visits, at least at some sites, to estimate detection probability. In most occupancy models, species identifications are assumed to be correct (see major variants below).


In the context of detection-attribution of biodiversity change, occupancy models are often used for detection, especially estimating trends from heterogeneous data {% cite isaac2014statistics altwegg2019occupancy %}. In these cases, the detection model can include covariates that aim to account for sampling heterogeneity (e.g., distance to roads to account for biased sampling). When occupancy-models are applied to opportunistic  data, the detection probability integrates both probability to detect (i.e., see or hear) as well probability to report when detected {% cite isaac2014statistics %}. Occupancy models can also be used for attribution, with occupancy models in which covariate adjustment is used to account for the effects of confounding variables {% cite guzman2024impact %}. 

#### Limitations
{: .no_toc }
Occupancy models rely on repeated surveys to estimate detection probability and therefore require sampling designs that include multiple visits or replicate observations. In addition, their performance may be limited at the extreme of species prevalence. For widespread species (occupancy close to 1), the model provides limited information on spatial variation in occurrence. Conversely, for extremely rare or elusive species with few detections, separating detection and occupancy probability becomes a statistical issue, leading to large uncertainties. Finally, models estimate occurrence probability rather than abundance, with results depending on how well detection covariates are captured in the model. Most of the variation in detection probabilities is due to variation in abundance.


### Major variants
{: .no_toc }

- *Dynamic occupancy models* – Dynamic models are used for temporal data to estimate extinction and colonization rates while accounting for the fact that lack of detections in a temporal unit (most often, year) might not mean lack of true occurrence. In these models, separate covariates can be specified for the extinction (or its reverse, persistence) and colonization probability models {% cite broms2016dynamic %}.

- *Multi-species occupancy models* – Multi-species models can be fitted to community datasets, with species typically treated as random effects. These have the advantage of borrowing information across species e.g., on detection probabilities or effects of covariates. Using data augmentation approaches, they also offer opportunities to predict the occurrence of species that were never detected, deriving community richness and other community parameters {% cite devarajan2020multispecies %}.

- *False positive occupancy models* – Some approaches have been developed to deal with both false positives and false absences in species observation data, aided if some subset of the data can be assumed to have no false positives, e.g. see {% cite royle2006generalized --style _bibliography/narrative %}.

### Further online resources
{: .no_toc }
- See package resources below.
- {% cite kery2021applied --style _bibliography/narrative %}. *Applied hierarchical modeling in ecology: Analysis of distribution, abundance and species richness in R and BUGS: Volume 2: Dynamic and advanced models.* Academic Press.


## Reference articles
### Method
{: .no_toc }
- {% cite_resource mackenzie2002estimating --style _bibliography/narrative %}

### Research applications
{: .no_toc }
#### With RS data in Ecology / Biodiversity
{: .no_toc }
- {% cite_resource kalle2018when --style _bibliography/narrative %}

#### Without RS data (Ecology domain)
{: .no_toc }
- {% cite_resource vanstrien2013opportunistic --style _bibliography/narrative %}

## Implementation

#### R
{: .no_toc }

- [CRAN: Package unmarked](https://cran.r-project.org/web/packages/unmarked/){:target="_blank"}
- [spOccupancy](https://doserlab.com/files/spoccupancy-web/){:target="_blank"} – Single-Species, Multi-Species, and Integrated Spatial Occupancy Models
- [flocker](https://jsocolar.github.io/flocker/articles/flocker_tutorial.html){:target="_blank"} – Fitting occupancy models with flocker
- Any Bayesian method using JAGS, nimble, stan, INLA etc.
    - {% cite belmont2024spatiotemporal --style _bibliography/narrative %} - *Spatio‐temporal occupancy models with INLA* - Methods in Ecology and Evolution - Wiley Online Library

<!-- For referencement in toc before automatic table -->
## Assessment table
