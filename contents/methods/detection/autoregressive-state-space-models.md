---
layout: method
title: "Autoregressive state-space models"
parent: "Independent detection"
date: 2025-09-29
author: Jussi Mäkinen, Finnish Environment Research Institute
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

{% if page.category_note != '' %}
{: .note }
This method also belongs to [Alternative paradigms]({{ site.baseurl }}/alternative).
{% endif %}


## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Description & principle 
In state-space models, observation and ecological processes are on separate hierarchical levels. In practice, this means that dependence between observations can be modeled on the ecological process level, for example intraspecific competition, whereas observation model deals only with survey-related factors, for example detection probability. Autoregressive means that there is a an autoregressive component, for example spatio-temporal random effect, which explains spatio-temporal correlation between the values of the ecological process. Commonly, autoregressive components are applied at the level of the ecological process and not at the level of the observation process.
                                                                    

## Reference articles
### Method
{: .no_toc }
- {% cite_resource auger-methe2021guide --style _bibliography/narrative %}

### Research applications
{: .no_toc }
#### With RS data in Ecology / Biodiversity
{: .no_toc }
- {% cite_resource jonsen2005robust --style _bibliography/narrative %}


## Implementation 

#### Python
{: .no_toc }
- [Statsmodels](https://www.statsmodels.org/devel/statespace.html){:target="_blank"}

#### R
{: .no_toc }
- [MARSS](https://atsa-es.github.io/MARSS/){:target="_blank"}
- [INLA](https://www.r-inla.org/){:target="_blank"}


<!-- For referencement in toc before automatic table -->
## Assessment table
