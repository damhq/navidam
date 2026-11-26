---
layout: method
title: "Instrumental variables"
parent: "Quasi-experiments"
date: 2026-03-05
author: Laura Dee, University of Colorado Boulder, reviewed by Emmanuelle Porcher
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

<!-- category-note:start -->

{: .note }
This method also belongs to [Adjusted methods (Backdoor C.)]({{ site.baseurl }}/adjusted), [Causal ML]({{ site.baseurl }}/causal_ML), and [Experiments]({{ site.baseurl }}/experiments).

<!-- category-note:end -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Description & principle

Instrumental variable regression deals with multiple forms of bias from
endogeneity: measurement error, reverse causality or simultaneity (where
Y affects X or both affect each other), and all sources of confounding.

To replicate the process of random treatment assignment, instrumental
variable regression aims to take advantage of a source of a driver (the
instrument) of “plausible random variation” in X. An instrument is an
observable variable that is correlated with *X*, but otherwise has no
impact on *Y*, except through its impact on *X*. Intuitively, an
instrument, which we call variable *Z*, should cause a shift in *X*, or
be a significant driver of variation in *X*, that is independent or
conditionally independent from *Y*. To isolate the causal effect of *X*
on *Y*, the approach is intuitive: find a measurable variable *Z* that
makes *X* vary but does not influence *Y*, except through its effect on
*X* (*reviewed in* {% cite imbens2014instrumental --style _bibliography/narrative %}; see {% cite kendall2015statistical --style _bibliography/narrative %} for a description for
ecologists; and ecological applications of IV are also cited below).

IVs can identify the effect for the units of
*X* that respond to variation in *Z*, known as the
“complier population” -- therefore it only measures a local
average treatment effect (LATE) as its estimand (see {% cite angrist1996identification --style _bibliography/narrative %}; {% cite angrist2009mostlya --style _bibliography/narrative %}; {% cite imbens2014instrumental --style _bibliography/narrative %}).

To use IV, two important requirements are needed for a “valid
instrument”:

1. instrument relevance, meaning the instrumental
   variable, *Z*, is strongly correlated with the *X* variable (which is
   testable with a “first-stage test”, see below) and
2. exclusion:
   that the instrument only affects the outcome variable *Y* through its
   effect on *X*.

In addition, IV and the variable it is instrumenting for
(*X*) *have a monotonic relationship (i.e., no defiers).* ***[Laura Dee: I
need to check if recent methods have relaxed this]*** These assumptions are
made regardless of the exact estimation approach (i.e., ordinary least
squares, SEM, or maximum likelihood). (Also SUTVA)

Only an instrument’s relevance is directly testable from data in what is
called a “first-stage test,” which is essentially an F-test. Because
exclusion is untestable, choosing an instrument carefully, based on
theory and system knowledge, is critical. In addition, further
assumptions required for a causal estimate of the LATE are conditional
independence (meaning that conditioned on the other variables in the
model, *Z* and *Y* are independent).

*Important* ***[Laura Dee: How deep to go?]*** considerations: weak
instruments can actually make bias worse in some cases {% cite
staiger1997instrumental --style _bibliography/narrative %}. The guidance
for “how strong” an instrument needs to be related to the *X* variable,
in terms of an F-statistic of the first stage text, seems to keep
varying/increasing.

## Major variants
{: .no_toc }
If the method has variants that seem important, either already
widespread or promising and well documented.

TO EDIT / FINISH / DISCUSS WHAT “COUNTS” here

- *Weak instrument tests and discussion*
- *Conditional independence*
- *Finite sample corrections* ***[Laura Dee: How deep to go?]***
- [Non-linear IV](https://benjamindwilliams.weebly.com/uploads/6/8/5/7/68575765/lecture9.pdf){:target="_blank"}

From: [https://rpubs.com/wsundstrom/t_ivreg](https://rpubs.com/wsundstrom/t_ivreg){:target="_blank"}

The top part of the table just presents the coefficients, etc. But the
bottom portion, *Diagnostic tests*, contains some new information. Note
the following:

- Weak instruments: This is an F-test on the instruments in the first
  stage. The null hypothesis is essentially that we have weak
  instruments, so a rejection means our instruments are not weak, which
  is good.

- *Wu-Hausman: This tests the consistency of the OLS estimates under the
  assumption that the IV is consistent. When we reject, it means OLS is
  not consistent, suggesting endogeneity is present. If we accept the
  null, it essentially means that the OLS and IV estimates are similar,
  and endogeneity may not have been a big problem.*

- *Sargan: This is a test of instrument exogeneity using overidentifying
  restrictions, called the J-statistic in Stock and Watson. It can only
  be used if you have more instruments than endogenous regressors, as we
  do in iv2. If the null is rejected, it means that at least one of our
  instruments is invalid, and possibly all of them.* ***[Laura Dee: These
  exist but are not widfely accepted as trustworthy...]***

## Further online resources
{: .no_toc }

- [https://github.com/katherinesiegel/EBIOcausalinference/blob/main/exercises/iv_demo.Rmd](https://github.com/katherinesiegel/EBIOcausalinference/blob/main/exercises/iv_demo.Rmd){:target="_blank"}

## Reference articles

### Method
{: .no_toc }

- {% cite_resource angrist2001instrumental --style _bibliography/narrative %}

- {% cite_resource imbens2014instrumental --style _bibliography/narrative %}

- {% cite_resource angrist1996identification --style _bibliography/narrative %}

- {% cite_resource angrist2009mostlya --style _bibliography/narrative %}

### Research applications
{: .no_toc }

#### With RS data in Ecology / Biodiversity
{: .no_toc }
- {% cite_resource sims2010conservation --style _bibliography/narrative %}

- {% cite_resource macdonald2019amazon --style _bibliography/narrative %}

#### Without RS data (Ecology domain)
{: .no_toc }
- {% cite_resource kendall2015statistical --style _bibliography/narrative %}

- {% cite_resource creel2009density --style _bibliography/narrative %}

## Implementation

#### Python
{: .no_toc }

#### R
{: .no_toc }
- [ivreg](https://cran.r-project.org/web/packages/ivreg/vignettes/ivreg.html){:target="_blank"}

- **library**(AER)

### Code Cells
{: .no_toc }

## Assessment table
