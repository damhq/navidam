---
layout: method
title: "Sensitivity analyses"
parent: "Robustness & significance tests"
date: 2025-11-19
author: Tamara Münkemüller, CNRS
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

<!-- category-note:start -->

{: .note }
This method also belongs to [Ecology-guided Modelling]({{ site.baseurl }}/ecology-guided). It also belongs to the sub-category [Uncertainty tools]({{ site.baseurl }}/tools/uncertainty_tools).

<!-- category-note:end -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Description & principle

Sensitivity analysis is used for model parametrization and calibration
in mechanistic simulation modelling and is an important method for
identifying the most important drivers of simulated ecological
processes. The idea is to explore how changes of values of model input
parameters change the output parameters of a model. In principle, the
input parameters that influence the output parameters most are the most
“sensitive” or most important parameters. Thus, calibrating them
correctly is also more important for the simulations than calibrating
less sensitive parameters correctly.

## Major variants
{: .no_toc }
One can differentiate between local sensitivity analysis and global
sensitivity analysis. In local sensitivity analysis, input parameters
are varied over a small range of values around specific reference values
independently one by one. In global sensitivity analysis, multiple input
parameters are varied over larger regions of the parameter space at the
same time. One challenge is that it is often too time consuming to run
all combinations of all parameter values of interest. Here, methods from
experimental design can be used for a stratified subsampling of the
complete parameter space (e.g. Latin Hypercube). Another challenge is to
analyse the results of the different simulations. Here, statistical
regression methods from observational data analyses can be used to
identify parameter importance.

## Further online resources
{: .no_toc }

## Reference articles

### Method
{: .no_toc }

- {% cite_resource saltelli2002sensitivity --style _bibliography/narrative %}

- {% cite_resource cariboni2007role --style _bibliography/narrative %}

- {% cite_resource tarantola2024annotated --style _bibliography/narrative %}

- {% cite_resource razavi2016new --style _bibliography/narrative %}

### Research applications
{: .no_toc }

#### With RS data in Ecology / Biodiversity
{: .no_toc }

#### Without RS data (Ecology domain)
{: .no_toc }
- {% cite_resource manlik2018applicability --style _bibliography/narrative %}

- {% cite_resource tenbroeke2016detecting --style _bibliography/narrative %}

## Implementation

#### Python
{: .no_toc }
- [SALib](https://salib.readthedocs.io/){:target="_blank"}

#### R
{: .no_toc }
- [sensitivity](https://cran.r-project.org/package=sensitivity){:target="_blank"}

### Code Cells
{: .no_toc }

## Assessment table
