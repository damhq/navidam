---
layout: method
title: "Quantile regression"
parent: "Linear regressions & extensions"
date: 2026-11-20
author: Risto K. Heikkinen, Syke
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Description & principle 

Classical quantile regression is an extension of linear regression which can be used in ecological modelling when the assumptions of linear regression are not met {% cite cade2003gentle --style _bibliography/narrative %}. Quantile regression can be particularly useful when the patterns in predictor - response variable data show unequal variation caused by unmeasured factors that interact in complex ways with the measured variables. Quantile regression uses several sections (conditional quantiles, or percentiles such as the 10th, 50th, or 90th percentiles) of the response variable data to develop multiple estimates for the rate of change (slopes) in the response variable. The model estimates are separately calculated for multiple medians (instead of conditional mean) of the response variable, each median represents a conditional median, and the outcome captures functional relationships between response and explanatory variables comprehensibly for all portions of the probability distribution.

The advantages of quantile regression include following:
1. Estimates of conditional quantiles of response variables provide a more flexible approach than ordinary least squares regression
2. Quantile regression accommodates data heteroscedasticity (unequal variance) occurring in ecological data shown as wedge-shaped or cone-shaped data patterns in scatter plots
3. The methods is more robust against data outliers than classical regression, operationalised via minimizing weighted absolute deviations rather than squared errors
4. Quantile regression provides a more complete view of relationships between the variables and also reveals specific patterns at the tails of the distribution, which may represent upper or lower physiological constraints
5. It is a semi-parametric method that makes no distributional assumptions and does not require the error terms to follow a normal (Gaussian) distribution
6. The option to determine the median of two or more quantiles in the data allows researchers to investigate different ecological questions within their stressor-response dataset and reveal trends missed by classical regression models.

The basic data requirements in quantile regression are the same as in linear regression models, including quantitative or categorical estimates for predictor variable(s) and quantative estimates for the response variable enabling division of response data into specific quantiles. Noticeably, conducting quantile regression comprise considerable computational load and require of larger number of data points than ordinary least squares regression. Unequal sampling near the extreme margins of variable range may cause uncertainties in the models and selection of the number and range of quantiles also need careful consideration; it is reasonable to avoid highly complicated models with several quantiles as well as overly simplified quantile profiles. Finally, as in all regression models, a starting point in quantile regression is carefully considered and ecologically plausible relationships between the studied predictor and response variables.  




### Major variants
{: .no_toc }
{: .d-inline-block }

A number of variants exists, some of which provide useful alternatives to the classical Quantile regression method in ecological modelling, including:

1. **Nonparametric and Additive Quantile Regression.** This approach extends classical quantile regression by allowing flexible, non-linear relationships between ecological response variables and environmental variables. Thus, instead of a straight-line relationship assumption, Nonparametric and Additive Quantile Regression use nonparametric smoothers, e.g. B-splines and kernel smoothing, which allows the data to guide the shape of the relationship between predictor variables and ecological quantiles. This enables capturing curved growth trajectories and complex patterns. See {% cite muggeo2013estimating --style _bibliography/narrative %} and the [quantregGrowth package](https://rdrr.io/cran/quantregGrowth/man/quantregGrowth-package.html){:target="_blank"}.

2. **Quantile Regression Forests (QRF).** Quantile Regression Forests (QRF) is a non-parametric tree-based ensemble extension of the Random Forests method, allowing the estimation of the entire conditional distribution and multiples quantiles in predictor – response variable relationships. In contrast to classical random forests, QRF retains all observation values in each classification tree leaf node rather than just the average. This allows the model to predict full conditional distributions for non-linear data, i.e. any conditional quantile can be computed based on a single trained model. QRF is well suited for high-dimensional data and can handle predictor variables of mixed classes. See {% cite meinshausen2006quantile --style _bibliography/narrative %} and the [quantregForest package](https://cran.r-project.org/web/packages/quantregForest/index.html){:target="_blank"}.

3. **Gradient Boosted Quantile Regression.** Gradient Boosted Quantile Regression is a machine learning technique that provides and extension of classical gradient boosted decision trees. The approach allows users to estimate conditional quantiles (e.g. prediction intervals τ = 0.05 and τ = 0.95) in addition to the conditional mean. Moreover, Gradient Boosted Quantile Regression is capable of handling non-linear relationships effectively, capture predictor variable interactions, works with mixed data types and handles missing values. Algorithms LightGBM, XGBoost, and CatBoost can perform high-dimensional predictive tasks and interval forecasting. See {% cite velthoen2021gradient --style _bibliography/narrative %} and {% cite zheng2012qboost --style _bibliography/narrative %}.

4. **Bayesian quantile regression.** This variant extends the basic quantile regression approach by integrating it within a probabilistic paradigm. This allows the users to develop direct inferences on conditional quantiles through prior-to-posterior updating. Bayesian quantile regression can accommodate flexible specification of uncertainty, hierarchical structures and complex data features such as non-normal errors and data censoring {% cite bayesian --style _bibliography/narrative %} {% cite lusiana2019application --style _bibliography/narrative %}.

### Further online resources
{: .no_toc }

Five online introductions to Quantile regression describing the basic requirements of the method, how it functions, and the different fields where the method can be applied include the following:

- [Quantile regression: A flexible alternative to linear regression](https://alfasoft.com/blog/products/statistics-and-data-analysis/quantile-regression-a-flexible-alternative-to-linear-regression/){:target="_blank"}
- [EPA CADDIS: Basic analyses (tab 3)](https://www.epa.gov/caddis/basic-analyses-2#tab-3){:target="_blank"}
- [EPA CADDIS: Basic analyses](https://www.epa.gov/caddis/basic-analyses){:target="_blank"}
- [scikit-learn quantile regression example](https://scikit-learn.org/stable/auto_examples/linear_model/plot_quantile_regression.html){:target="_blank"}
- [Introduction to quantile regression](https://blog.dailydoseofds.com/p/introduction-to-quantile-regression){:target="_blank"}


## Reference articles
### Method
{: .no_toc }
- {% cite_resource koenker2001quantile --style _bibliography/narrative %}
- {% cite_resource koenker2017handbook --style _bibliography/narrative %}

### Research applications
{: .no_toc }
#### With RS data in Ecology / Biodiversity
{: .no_toc }
- {% cite_resource rocchini2008quantile --style _bibliography/narrative %}

#### Without RS data (Ecology domain)
{: .no_toc }
- {% cite_resource cade2003gentle --style _bibliography/narrative %}
- {% cite_resource cade2005quantile --style _bibliography/narrative %}
- {% cite_resource hallfors2024recent --style _bibliography/narrative %}
- {% cite_resource schroder2005rejecting --style _bibliography/narrative %}
- {% cite_resource vaz2008modelling --style _bibliography/narrative %}

## Implementation 

#### Python
{: .no_toc }
- [XGBoost quantile regression example](https://xgboost.readthedocs.io/en/release_3.2.0/python/examples/quantile_regression.html){:target="_blank"}
- [quantile-forest](https://github.com/zillow/quantile-forest){:target="_blank"}

#### R
{: .no_toc }
- [quantreg](https://cran.r-project.org/web/packages/quantreg/index.html){:target="_blank"}
- [quantreg.nonpar](https://cran.r-project.org/web/packages/quantreg.nonpar/index.html){:target="_blank"}
- [Navigating quantile regression with R: A comprehensive guide](https://www.r-bloggers.com/2023/11/navigating-quantile-regression-with-r-a-comprehensive-guide/){:target="_blank"}

### Code Cells
{: .no_toc }
{: .d-inline-block }
optional
{: .label}


<!-- For referencement in toc before automatic table -->
## Assessment table
