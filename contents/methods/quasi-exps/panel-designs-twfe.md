---
layout: method
title: "Panel designs, TWFE"
parent: "Quasi-experiments"
date: 2025-11-18
author: Romain Goury, reviewed by Mike Hedde and Miriam Beck
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

*Method* ***[Mike Hedde: The description of the method is clear, but it
might help readers if typical use cases were stated more explicitly.
For instance, in which types of ecological or environmental studies
would TWFE models be particularly appropriate (e.g. repeated monitoring
data, policy interventions, management changes)?]***

Two-Way Fixed Effects (TWFE) models are a generalisation of
difference-in-difference (DID) models {% cite angrist2009mostlya --style _bibliography/narrative %},
that use added ‘fixed effects’ to control for several dimensions of
confounding. Generally, it is used to account for multiple groups and
time periods by including unit and time fixed effects (although these
fixed effects may consider other variables).. *The 'unit' fixed effect
controls for all confounding variables that are time-invariant and only
vary spatially (e.g. topographic variables), while the 'time' fixed
effect controls for all confounding variables that vary over time, but
not in space.* ***[Mike Hedde: The explanation of unit and time fixed
effects is helpful, but I might benefit from a short intuitive
explanation (e.g. controlling for all stable differences between sites
and all shocks affecting all sites in a given year).]*** ***[Mike Hedde: It
might also help readers if the typical data structure required for TWFE
models (e.g. panel data with repeated observations over time) was
briefly highlighted.]***

By adding both unit and time fixed effects, the model estimates the
average causal effect of variation in the driver?predictor? within
units? and within years on the outcome. In other words, TWFE
adresses?captures? anomalies in both the explanatory and response
variables, *so these models focus more strongly on individuals with a
lot of variation over time and/or space.* ***[Miriam Beck: Not sure if that
is need as it should be also the case in other models (i.e. sites with
stronger trends etc 'driving' the model?]***

Methodologically, TWFE comes with the strong assumption of effect (or
treatment) homogeneity, i.e. that the treatment effect does not vary
across units or over time, which might not always be the case in
ecological scenarios.. In contrast, compared to for example
mixed-effect models with unit/year random intercepts, TWFE do not assume
uncorrelation between fixed effect and predictor variable(s) which could
be relevant with strong climatic gradients across study areas.

- **No dynamic treatment effects:** The model requires that the
  treatment effect does not evolve over time.

- **No unit-level differences:** The treatment effect must be constant
  across all units.

- **Linear additive effects:** TWFE assumes that the underlying
  data-generating process is captured by additive fixed effects plus a
  constant treatment effect {% cite imai2021use --style _bibliography/narrative %}.

What happens to our data when we apply *OWFE*/TWFE models? ***[Mike Hedde: The acronym
OWFE appears before it is clearly introduced, which might be slightly
confusing for readers unfamiliar with the terminology.]***

![Raw data, one-way fixed effects and two-way fixed effects]({{ site.baseurl }}/assets/images/twfe-fixed-effects.png)

*Fig. 1:* This plot shows how the effect of X on Y changes according to
the applied model. The left panel shows the raw data, simply regressing
x~Y. The middle panel illustrates the OWFE adding a 'unit' fixed effect.
The X and Y values both correspond to anomalies with a mean value of 0.
and the right panel represents the TWFE, adding both ‘unit’ and ‘year’
fixed effects (right panel). represents the anomalies of the OWFE,
centring the data at 0 and effectively removing the trends present in
both the X and Y values. ***[Mike Hedde: The figure is helpful. However, a
slightly more intuitive explanation of what happens to the data (e.g.
“removing average differences between units and years”) might make the
figure easier to interpret for non-specialists.]***

## *Major variants*
{: .no_toc }
*A variant of the method uses only single fixed effect, i.e. for time or
unit (one-way fixed effect, OWFE). This model makes the same assumptions
as the TWFE, but we keep the temporal trajectories (anomaly, trends) in
the data.* ***[Miriam Beck: I'd just move this before the plot since the
plot includes OWFE]***

## Further online resources
{: .no_toc }
- [https://bookdown.org/mike/data_analysis/sec-two-way-fixed-effects.html#ref-goodman2021difference](https://bookdown.org/mike/data_analysis/sec-two-way-fixed-effects.html#ref-goodman2021difference){:target="_blank"}
- [https://theeffectbook.net/ch-FixedEffects.html?panelset_001=r-code#how-does-it-work](https://theeffectbook.net/ch-FixedEffects.html?panelset_001=r-code#how-does-it-work){:target="_blank"}

## Reference articles

### Method
{: .no_toc }

- {% cite_resource dee2023clarifying --style _bibliography/narrative %}

- {% cite_resource dudney2025causal --style _bibliography/narrative %}

### Research applications
{: .no_toc }

#### With RS data in Ecology / Biodiversity
{: .no_toc }

#### Without RS data (Ecology domain)
{: .no_toc }
- {% cite_resource dee2023clarifying --style _bibliography/narrative %}

- {% cite_resource dudney2021nonlinear --style _bibliography/narrative %}

## Implementation

#### Python
{: .no_toc }

#### R
{: .no_toc }
- [https://lrberge.github.io/fixest/index.html](https://lrberge.github.io/fixest/index.html){:target="_blank"}

### Code Cells
{: .no_toc }
```r
library(tidyverse)
library(modelsummary)
library(fixest)

gm <- causaldata::gapminder

# Run our two-way fixed effects model (TWFE).
# First the non-fixed effects part of the model
# Then a |, then the fixed effects we want
twfe <- feols(lifeExp ~ log(gdpPercap) | country + year,
              data = gm)

# Note that standard errors will be clustered by the first
# fixed effect by default. Set se = 'standard' to not do this
msummary(twfe, stars = c('*' = .1, '**' = .05, '***' = .01))
```

## Assessment table
