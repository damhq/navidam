---
layout: method
title: "S-Map"
parent: "Alternative paradigms"
date: 2025-09-17
author: Miriam Beck, FRB-CESAB, Montpellier, France
---
<!-- This file was auto-generated from DetectionAttribution methods - Method Assessment.tsv -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Description & principle

S-Map (sequential locally weighted global linear maps, {% cite sugihara1994nonlinear --style _bibliography/narrative %},
{% cite sugihara2012detecting --style _bibliography/narrative %}) is an equation-free modeling technique within the Empirical
Dynamical Modeling (EDM) framework, designed to quantify and explore
dynamic, potentially time-varying relationships between variables in
complex systems. The method relies on the concept of state space
reconstruction, where the system's "state" at any given time is
represented as a vector of time-lagged observations from one or more
variables.

S-Map models the system's behavior by fitting linear equations within
local neighborhoods of this state space, using nearby points (=similar
past system states) to predict future values. Depending on how strongly
the model weights nearby states the model behaves like a global linear
regression or emphasizes local structure and captures nonlinear
dynamics. The estimated regression coefficients reflect local
interaction strengths, allowing to investigate the strength and
direction of interactions among variables change over time or across
system states.

## Major variants
{: .no_toc }
- **Baysian versions of EDM** rely on (Gaussian Processes (GP) regressions, combining short time series in a hierarchical model structure to increase forecast precision, addressing cases of short time series or noisy data {% cite munch2017circumventing --style _bibliography/narrative %}. This extension includes S-Map {% cite yukihira2025quantifying --style _bibliography/narrative %}.
- **Variable step size EDM** (VS-EDM; {% cite johnson2022empirical --style _bibliography/narrative %}) incorporates the actual temporal spacing between observations into delay-coordinate vectors rather than assuming a fixed lag. Under irregular sampling or missing data, the reconstructed state-space reflects true dynamics more faithfully. The introduction of regularization schemes (e.g. ridge, lasso, elastic net) improves the inference and forecasting when process noise is high (**regularized S-Map**, {% cite cenci2019regularized --style _bibliography/narrative %}). Further variants or tweaks are discussed in {% cite munch2023recent --style _bibliography/narrative %}.

## Further online resources
{: .no_toc }
The [rEDM package documentations](https://ha0ye.github.io/rEDM/articles/rEDM.html){:target="_blank"} provide walk through examples across
methods and workflows in EDM, including CCM and highlighting its
integration in EDM workflow.

## Reference articles

### Method
{: .no_toc }

- {% cite_resource sugihara2012detecting --style _bibliography/narrative %}

- {% cite_resource sugihara1994nonlinear --style _bibliography/narrative %}

- {% cite_resource ushio2020forecasting --style _bibliography/narrative %}

### Research applications
{: .no_toc }

#### With RS data in Ecology / Biodiversity
{: .no_toc }

#### Without RS data (Ecology domain)
{: .no_toc }
- {% cite_resource kawatsu2021are --style _bibliography/narrative %}

- {% cite_resource wang2020causala --style _bibliography/narrative %}

- {% cite_resource mcgowan2017predicting --style _bibliography/narrative %}

- {% cite_resource rogers2020trophic --style _bibliography/narrative %}

- {% cite_resource zhao2023relationships --style _bibliography/narrative %}

## Implementation

#### Python
{: .no_toc }
- [pyEDM](https://pypi.org/project/pyEDM/){:target="_blank"}
  ([https://sugiharalab.github.io/EDM_Documentation/](https://sugiharalab.github.io/EDM_Documentation/){:target="_blank"})

- [fastEDM](https://edm-developers.github.io/fastEDM-python/){:target="_blank"}

#### R
{: .no_toc }
- [rEDM](https://ha0ye.github.io/rEDM/articles/rEDM.html){:target="_blank"}

- [fastEDM](https://github.com/EDM-Developers/fastEDM-r){:target="_blank"} allow to process
  panel data (‘multispatial EDM’)

### Code Cells
{: .no_toc }

## Assessment table
