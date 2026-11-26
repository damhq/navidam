---
layout: method
title: "Frontdoor criterion"
parent: "Alternative effect identification methods"
date: 2026-03-18
author: Miriam Beck
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Description & principle

The front-door criterion (or front-door adjustment) is not an estimation
method *per se*. Rather, like the back-door criterion, it is an
identification strategy that, under certain assumptions, enables the
estimation of causal effects from observational data. While the
backdoor-criterion applies when confounders of the exposure-outcome
relationship are observed and can be adjusted for, the front-door
criterion comes in play when such confounders are unobserved or cannot
be measured. In this case, identification can instead rely on observed
mediating variables.

The idea is simple:

If the causal pathway of interest between an exposure ‘X’ and an outcome
‘Y’ passes through one (or multiple) mediators (‘M’), we can decompose
the causal effect into two parts: the effects X 🡪 M and M 🡪 Y. Under
front-door conditions, they can be estimated separately and then
combined via the ‘front-door formula’ (in simple, linear cases:
multiplied) to obtain the total causal effect X 🡪 Y.

Three conditions need to be fulfilled:

- All causal paths from X 🡪 Y pass through M (i.e. there is no direct
  effect X 🡪 Y)

- There are no unobserved confounders for X 🡪 M

- All confounders of the M 🡪 Y relationship are blocked by conditioning
  on X

Importantly, the adjustment must comprise all mediating variables that
lie on the causal pathway.

Practical considerations:

Although the front-door criterion was formalized by {% cite pearl2009causality --style _bibliography/narrative %}
and is well established in causal inference theory, its practical
application across disciplines remains limited. This is mainly because
the required assumptions are often difficult to satisfy in real-world
scenarios. For example, it is rare to be confident that there is no
(substantial) direct effect of X on Y or no unmeasured confounders
affect the mediator-outcome relationship.

## Major variants
{: .no_toc }
- Generalized front-door criterion, which relaxes the assumption of no
  direct effect between exposure and outcome, as described by {% cite fulcher2020robust --style _bibliography/narrative %}.

## Further online resources
{: .no_toc }
- Nice walk-through example, visualisation with DAG and toy example:
  [https://www.kenkoonwong.com/blog/frontdoor/](https://www.kenkoonwong.com/blog/frontdoor/)

## Reference articles

### Method
{: .no_toc }

- {% cite_resource arif2023applying --style _bibliography/narrative_full %}
- {% cite_resource bellemare2024paper --style _bibliography/narrative_full %}


### Research applications
{: .no_toc }

#### With RS data in Ecology / Biodiversity
{: .no_toc }

#### Without RS data (Ecology domain)
{: .no_toc }

## Implementation

#### Python
{: .no_toc }

#### R
{: .no_toc }


## Assessment table
