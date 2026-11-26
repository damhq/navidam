---
layout: method
title: Synthetic controls
parent: "Quasi-experiments"
nav_order: 1
date: 2025-06-23
author: Joaquim Estopinan
# assessor: Mr. Smith
---
<!-- category-note:start -->

{: .note }
This method also belongs to [Adjusted methods (Backdoor C.)]({{ site.baseurl }}/adjusted).

<!-- category-note:end -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Description & principle 

The synthetic control (SC) method originates from the early 2000s, with its first introduction in the influential {% cite abadie2003 --style _bibliography/narrative %} article. It consists in combining a selection of control sites to best mimick the treatment site's counterfactual, based on the pre-intervention similarity of their respective outcome and covariates. It is an effect estimation method shifting the `causal sufficiency` assumption (no unobserved confounders) to the `good pre-intervention fit` condition, still assuming no time-varying unobserved confoundinfing after the intervention.

### Major variants
{: .no_toc }
{: .d-inline-block }

The success of this method has also led to numerous variants. We can cite among others:
- **Robust SC** from {% cite amjad2018 --style _bibliography/narrative %}: Adds de-noising, uncertainty estimation and handles missing data
- **Augmented SC** from {% cite ben-michael2020 --style _bibliography/narrative %} {% cite ben-michael2022 --style _bibliography/narrative --suppress_author %}: Relaxes constraints on the synthetic control combination to improve pre-treatment fit and allows staggered adoption of treatment between various units
- **Sparse SC** from {% cite quistorff2021 --style _bibliography/narrative %}: Helps pre-treatment variables selection and add regularization to meet big data context needs
- **Penalized SC** from {% cite abadie2021a --style _bibliography/narrative %}: An adaptation of the SC method to deal with disaggregated data gathering varied treated units
- Finally, a number of recent developement merge the SC method with other approaches:
    - **Generalized SC** relaxes the parallel trend assumption and unifies the SC method with linear fixed effects models {% cite xu2017 %}
    - **Synthetic Diff-in-diffs** combines SCs with the difference-in-differences estimator {% cite arkhangelsky2021 %}
    - {% cite_resource chernozhukov2021 --style _bibliography/narrative %} exploit conformal prediction and structural breaks in conjunction with SCs
    - {% cite_resource imai2023 --style _bibliography/narrative %} developped a flexible estimation procedure combining matching and SCs ideas with diff-and-diffs.



### Further online resources
{: .no_toc }

- A pedagocial blog decomposing the method: [15 - Synthetic Control](https://matheusfacure.github.io/python-causality-handbook/15-Synthetic-Control.html){:target="_blank"}
- On the covariate selection: {% cite botosaru2019 --style _bibliography/narrative %}
- Discussion on the violation of the parallel trends assumption and its consequences: [Cross Validated](https://stats.stackexchange.com/questions/649162/unparallel-pre-treatment-trends-in-synthetic-control-method){:target="_blank"}
 

## Reference articles
### Method
{: .no_toc }
An updated review paper positioning the method by its original author: {% cite abadie2021  --style _bibliography/narrative %}

### Research applications
{: .no_toc }
#### With RS data in Ecology / Biodiversity
{: .no_toc }
- {% cite_resource fick2021  --style _bibliography/narrative %}
- {% cite_resource sharma2023  --style _bibliography/narrative %}
- {% cite_resource rana2019  --style _bibliography/narrative %}
- {% cite_resource west2020  --style _bibliography/narrative %}

#### Without RS data (Ecology domain)
{: .no_toc }
- {% cite_resource lepissier2021  --style _bibliography/narrative %}
- {% cite_resource nakanishi2022  --style _bibliography/narrative %}
- {% cite_resource kaiser2026synthetic  --style _bibliography/narrative %}

## Implementation 

#### Python
{: .no_toc }
- [pysyncon](https://github.com/sdfordham/pysyncon){:target="_blank"}

#### R
{: .no_toc }
- [Synth](https://cran.r-project.org/web/packages/Synth/index.html){:target="_blank"}
- [augsynth](https://github.com/ebenmichael/augsynth){:target="_blank"}
- [tidysynth](https://cran.r-project.org/web/packages/tidysynth/index.html){:target="_blank"}
- [microsynth](https://cran.r-project.org/web/packages/microsynth/index.html){:target="_blank"}
- [gsynth](https://github.com/xuyiqing/gsynth){:target="_blank"}
- [SparseSC](https://github.com/microsoft/SparseSC){:target="_blank"}



<!-- ### Code Cells
{: .no_toc }
{: .d-inline-block }
optional
{: .label}

```r
Example R/Python code or GitHub Gist links. 
``` -->









<!-- For referencement in toc before automatic table -->
## Assessment table
