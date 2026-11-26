---
layout: method
title: "Structural equation modelling (SEM)"
parent: "Ecology-guided Modelling"
date: 2025-11-19
author: Pierre Gaüzère, CNRS, reviewed by Cyrille Violle and Miriam Beck
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Description & principle

Structural equation modelling (SEM) is a family of multivariate
regression models used to evaluate hypothesized causal relationships
among variables. These relationships are represented as a network of
directed paths (path diagram), and all parameters are estimated
simultaneously within a unified modelling framework. SEM is particularly
useful for attribution because it allows the contribution of multiple
drivers to be decomposed along hypothesized causal pathways, making it
possible to quantify the mechanisms through which environmental drivers
influence ecological responses. In ecology, SEM is used to test how
multiple drivers (e.g. climate, land use, soil, management) jointly
influence biodiversity, ecosystem functions, or species traits, while
distinguishing direct effects and indirect effects transmitted through
intermediate variables (mediators). A SEM typically consists of two
parts:

1. A structural model, which specifies regressions among variables
   (observed or latent), and
2. A measurement model, which links latent variables (e.g. “habitat
   quality”, “disturbance intensity”) to observed indicators (e.g.
   vegetation structure, NDVI, grazing proxies).

SEM
differs from standard multiple regression by
1. allowing multiple responses and feedback structures in a single model,
2. including latent variables, which represent unobserved constructs measured by
   multiple indicators,
3. providing a global test of whether the hypothesized causal structure is consistent with the data (model fit),
4. explicitly partitioning effects into direct, indirect and total effects.

This explicit decomposition of total effects into direct and
indirect effects is what makes SEM particularly suitable for
attribution, as it allows to quantify how much of the total effect of a
driver is transmitted along specific pathways (e.g. “via productivity”
vs “via soil moisture”), and how much is direct.

## Major variants
{: .no_toc }
Many variants exist, but the most important in ecology are:

- **Covariance-based SEM (CB-SEM)**: Classical SEM framework using the
  covariance matrix and maximum likelihood (or robust alternatives).
  Supports full latent-variable models, multiple groups, and complex
  measurement structures. Implemented for example in [lavaan](https://cran.r-project.org/web/packages/lavaan/lavaan.pdf){:target="_blank"}.

- **Piecewise SEM (component-based SEM)**: The system is represented as a
  set of linked regression or mixed models (e.g. lm, glmer, gam) and
  evaluated using d-separation tests. This approach fits well with
  common ecological data structures (e.g. non-normal responses, random
  effects, hierarchical designs) and is widely used in ecology.
  [piecewiseSEM](https://cran.r-project.org/web/packages/piecewiseSEM/vignettes/piecewiseSEM.html){:target="_blank"}

- **Dynamic structural equation models (DSEM)**: Extensions of SEM to
  multivariate time series, allowing simultaneous and lagged effects
  (e.g. autoregressive paths, cross-lagged relationships) while
  preserving causal interpretation. Useful for attributing temporal
  dynamics of ecosystems to lagged drivers. [dsem](https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.14289){:target="_blank"}

- **Bayesian SEM**: Bayesian implementations of SEM allow incorporation of
  prior information, probabilistic uncertainty quantification of path
  coefficients, and straightforward model comparison via Bayes factors
  or information criteria. [blavaan](https://cran.r-project.org/web/packages/blavaan/blavaan.pdf){:target="_blank"}

## Further online resources
{: .no_toc }
- Book: *Structural equation modeling and natural systems* {% cite grace2006structural --style _bibliography/narrative %}. Comprehensive methodological and ecological introduction, with many
  worked examples.

- Article: {% cite grace2010specification --style _bibliography/narrative %} “On the specification of structural
  equation models for ecological systems.” *Ecological Monographs*.
  Guidance on specifying and evaluating SEMs in ecology

- R package piecewiseSEM vignette: “Piecewise Structural Equation
  Modeling in R” ({% cite lefcheck2016piecewisesem --style _bibliography/narrative %} and updates).

- R package [lavaan](https://cran.r-project.org/package=lavaan){:target="_blank"} website and reference manual.

- R package [dsem documentation](https://james-thorson-noaa.github.io/dsem/){:target="_blank"} for dynamic structural equation
  models.

## Reference articles

### Method
{: .no_toc }

- {% cite_resource grace2006structural --style _bibliography/narrative %}

- {% cite_resource grace2010specification --style _bibliography/narrative %}

- {% cite_resource lefcheck2016piecewisesem --style _bibliography/narrative %}

- {% cite_resource thorson2024dynamica --style _bibliography/narrative %}

- {% cite_resource zhu2024applications --style _bibliography/narrative %}

### Research applications
{: .no_toc }

#### With RS data in Ecology / Biodiversity
{: .no_toc }
- {% cite_resource gu2022quantifying --style _bibliography/narrative %}

- {% cite_resource yao2025quantifying --style _bibliography/narrative %}

#### Without RS data (Ecology domain)
{: .no_toc }
- {% cite_resource roland2019structural --style _bibliography/narrative %}

- {% cite_resource jonsson2009structural --style _bibliography/narrative %}

## Implementation

#### Python
{: .no_toc }
- [Semopy](https://semopy.com){:target="_blank"}. Provides a lavaan-like
  syntax, supports path analysis, latent-variable SEM, and growth
  models, with functions for model fitting, diagnostics, and
  visualization.

#### R
{: .no_toc }
- [lavaan](https://cran.r-project.org/package=lavaan){:target="_blank"}. General latent variable and SEM framework (path
  analysis, CFA, SEM, growth models). Uses a concise model syntax and
  supports ML/robust ML, WLS, FIML for missing data, multi-group models,
  and many fit indices and post-processing tools.

- [piecewiseSEM](https://cran.r-project.org/package=piecewiseSEM){:target="_blank"}. Implements piecewise structural
  equation modelling from a list of fitted models (lm, lmer, glmmTMB,
  gam, etc.). Provides d-separation tests, standardization, indirect
  effects, and plotting tools; particularly adapted to ecological data
  (non-normal, hierarchical).

- [blavaan](https://cran.r-project.org/package=blavaan){:target="_blank"}. Bayesian counterpart to lavaan: same syntax
  but fits models via Stan or JAGS, enabling Bayesian SEM with full
  posterior inference and Bayes-factor model comparison.

- [dsem](https://cran.r-project.org/package=dsem){:target="_blank"}. Implements dynamic structural equation models for
  multivariate ecological time series, combining SEM with
  state-space/vector autoregressive structures.

- [semTools](https://cran.r-project.org/package=semTools){:target="_blank"}. A toolbox of utilities that extend lavaan
  (e.g. reliability, invariance testing, multiple imputation, latent
  interactions), often useful in more advanced SEM workflows.

### Code Cells
{: .no_toc }

## Assessment table
