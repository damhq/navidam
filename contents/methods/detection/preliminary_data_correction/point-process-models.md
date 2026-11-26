---
layout: method
title: "Point process models"
parent: "Preliminary data correction"
date: 2025-09-29
author: Jussi Mäkinen, Finnish Environment Research Institute
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

<!-- category-note:start -->

{: .note }
This method also belongs to [Ecology-guided Modelling]({{ site.baseurl }}/ecology-guided), [Adjusted methods (Backdoor C.)]({{ site.baseurl }}/adjusted), and [Versatile tools]({{ site.baseurl }}/tools).

<!-- category-note:end -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Description & principle

Point process models are used for studying an occurrence pattern, such
as species occurrence or landscape characteristic, estimating the
association between the occurrence intensity and explanatory variables
and predicting occurrence intensity to new locations. Point process
models are fitted using presence occurrences without information of
where the feature of interest was absent. Due to the lack of absence
information, values of explanatory variables in presence locations are
compared with the overall distributions of explanatory variables across
the landscape. In practice, this is done with quadrature points which
are used for approximating the marginal likelihood of the data given the
model. Poisson point process models are generalized linear models (GLMs)
with a poisson error distribution and log-link function. These models
differ from conventional log-link GLMs by that they approximate the
likelihood with quadrature points.

## Reference articles

### Method
{: .no_toc }

- {% cite_resource renner2015point --style _bibliography/narrative %}

### Research applications
{: .no_toc }

#### With RS data in Ecology / Biodiversity
{: .no_toc }

- {% cite_resource martino2021integration --style _bibliography/narrative %}

## Implementation

#### Python
{: .no_toc }
- [statsmodels](https://www.statsmodels.org/){:target="_blank"} for full model and [pointpats](https://pysal.org/pointpats/){:target="_blank"} for
  exploratory analysis

#### R
{: .no_toc }
- [stats](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/00Index.html){:target="_blank"} for GLMs and [spatstat](https://cran.r-project.org/package=spatstat){:target="_blank"} specifically for point
  process models

## Assessment table
