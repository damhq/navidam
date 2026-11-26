---
layout: method
title: Frescalo
parent: "Preliminary data correction"
date: 2025-07-29
author: "Romain Goury"
categories:
- methods
- detection
- preliminary_data_correction
---
<!-- This file was auto-generated from _data/method_assessments.tsv -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Description & principle 
Frescalo is a method developed by {% cite hill2012  --style _bibliography/narrative %}, that aims to consider and correct for spatio-temporal biases from unstructured (i.e., opportunistic) data. The method provides estimated of temporal trends when there has been enough sampling to at least estimate species’ local relative frequencies accurately. The Frescalo algorithm is divided in two main steps such as a spatial and temporal correction (see [Fig. 1](#fig-frescalo)). The first step aims to correct for variation in sampling effort across neighbourhoods for the overall time period being considered, while the second step relies in correcting for time-period specific variations in recording effort within and across sites.


![]({{ site.baseurl }}/assets/images/frescalo.png)
<a name="fig-frescalo"></a>
**Figure 1** An overview of the Frescalo method {% cite goury2025 %}


### Further online resources
{: .no_toc }

- [sparta R vignette on Frescalo](https://biologicalrecordscentre.github.io/sparta/articles/vignette.html#frescalo){:target="_blank"}


## Reference articles
### Method
{: .no_toc }
- *Local frequency as a key to interpreting species occurrence data when recording effort is not known* {% cite hill2012 %}
- *A practical guide to species trend detection with unstructured data using local frequency scaling (Frescalo)* {% cite goury2025 %}

### Research applications
{: .no_toc }
#### With RS data in Ecology / Biodiversity
{: .no_toc }
- {% cite_resource montras-janer2024  --style _bibliography/narrative %}

#### Without RS data (Ecology domain)
{: .no_toc }
{: .d-inline-block }

- {% cite_resource auffret2022  --style _bibliography/narrative %}
- {% cite_resource eichenberg2021  --style _bibliography/narrative %}
- {% cite_resource fox2014  --style _bibliography/narrative %}
- {% cite_resource britishbryologicalsociety2014  --style _bibliography/narrative %}
- {% cite_resource suggitt2023  --style _bibliography/narrative %}
- {% cite_resource white2019a  --style _bibliography/narrative %}
- {% cite_resource pescott2019  --style _bibliography/narrative %}
- {% cite_resource eichenberg2021  --style _bibliography/narrative %}
- {% cite_resource redhead2018  --style _bibliography/narrative %}
- {% cite_resource dyer2017  --style _bibliography/narrative %}
- {% cite_resource goury2025  --style _bibliography/narrative %}

## Implementation 

#### Python
{: .no_toc }

> *No Implementation in python are existing*

#### R
{: .no_toc }

- [https://www.brc.ac.uk/biblio/frescalo-computer-program-analyse-your-biological-records](https://www.brc.ac.uk/biblio/frescalo-computer-program-analyse-your-biological-records){:target="_blank"} (old package version) 

- [https://github.com/colinharrower/frescalo](https://github.com/colinharrower/frescalo){:target="_blank"} (package published in Goury et al., 2025)


### Code Cells
{: .no_toc }

- [https://github.com/colinharrower/frescalo](https://github.com/colinharrower/frescalo){:target="_blank"}
- [https://agauffret.github.io/FrescaloFun/FrescaloFun_tutorial250319.html](https://agauffret.github.io/FrescaloFun/FrescaloFun_tutorial250319.html){:target="_blank"} (from the old package) 
- [https://rpubs.com/sacrevert/simpleFresDemo](https://rpubs.com/sacrevert/simpleFresDemo){:target="_blank"} (old package) 
- [https://biologicalrecordscentre.github.io/sparta/articles/vignette.html](https://biologicalrecordscentre.github.io/sparta/articles/vignette.html){:target="_blank"} (some example for the old version)


<!-- For referencement in toc before automatic table -->
## Assessment table
