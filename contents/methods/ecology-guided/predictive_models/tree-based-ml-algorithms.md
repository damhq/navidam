---
layout: method
title: "Tree-based ML algorithms"
parent: "Predictive models + interpretability metrics"
date: 2025-09-23
author: Luca Santini (Sapienza University of Rome), reviewed by Franziska Schrodt (University of Nottingham)
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Description & principle 

**Decision trees**

Decision trees are non-parametric supervised learning algorithms based on recursive partitioning. The algorithm splits a dataset into smaller, more homogeneous subsets with respect to the response variable, based on a set of predictors. The algorithm returns a set of simple rules, based on splits of predictor variables, that link predictor values to a group of the response variable. Decision trees can handle any type of variable for both predictors and response, making them extremely flexible tools. They are commonly referred to as classification trees when the response variable is categorical, and regression trees when the response variable is numerical. The splitting rules are derived based on thresholds that maximize the homogeneity of the resulting groups. The Gini Impurity index or Entropy are typically used in classification problems, whereas the mean squared error (MSE) or mean absolute error (MAE) is more commonly applied in regression problems. Conditional inference trees use a significance test procedure in order to select variables, making them more robust to overfitting.
Predictions are produced by traversing the tree's structure from the root node down to a leaf node, following the decision rules at each internal node. The leaf node is a category in the case of classification trees, or an average group value for a regression tree. 
While decision trees excel at explaining a dataset, they’re prone to overfitting. Two possible approaches to deal with overfitting is pre-pruning or post-pruning. In pre-pruning, a rule is applied that the recursive partitioning stops when the gain in predictive accuracy is limited. In post-pruning the classification tree is pruned by a certain amount after fitting. These two approaches allow to increase the generality of the trees. Yet, despite these approaches, classification trees remain quite sensitive to overfitting. 


**Combining multiple trees**

Random forest and boosted trees are machine learning techniques that address overfitting using two different approaches: bagging and boosting. Both rely on the combination of many different underfitted trees (commonly referred to as weak learners), which are characterized by low bias and high variance. Bagging consists of training many different weak learners based on subsets of the original dataset, and then combines them to produce a prediction. The principle lies in what is known as the “wisdom of the crowd”, where a large group of people are collectively better at predicting than an expert individual. In contrast, boosting consists in the concatenation of many weak learners, each one improving the prediction of the previous one. 


**Random forests**

Random forests predict on the basis of many weak learners (hence a “forest” of weak learners). At each iteration, random forest bootstraps the dataset with replacement, and uses the non-sampled data as a validation set (out of bag sample). Subsequently, it only samples a subset of the covariates for fitting a tree. These two conditions enable the algorithm to produce many different classification trees, which are not very good at predicting when taken individually, but collectively show a good balance between variance and bias. Predictions are produced by combining the individual predictions from the weak learners in two possible ways. If the response is numerical, the prediction is the average of individual predictions. If instead the response is categorical, the prediction will be obtained by vote counting across all weak learners. 
Random forest requires some tuning in relation to the number of trees and the number of predictors sampled at each split. The optimal tuning parameters are determined by evaluating different parameter combinations and selecting those that minimize prediction error. The number of trees in a forest will increase performance until a certain number, to then stabilize.
The relationships identified by Random Forest can be inspected through predictions using partial response curves. Random Forest produces a variable importance score, which can be obtained as a measure of decrease in node impurity by using a given variable for splitting, or by estimating the effect of individual variable permutation on the predictive accuracy. A more in-depth estimation of variable importance on individual predictions can be obtained by using Shapley values.


**Gradient Boosted Decision trees**

Gradient Boosting differs from Random Forest in how the algorithm proceeds and how trees are combined. Regression trees are not independent but build on each other sequentially, gradually improving the predictions along the way. Yet, because this would quickly overfit the data, the trees have limited complexity and are penalized at each step to behave as weak learners.
First, the algorithm bootstraps a fraction of the dataset without replacement, and uses the left-out observations as the out of bag fraction for validation. Then, starting from a best guess estimate (e.g. average of the response variable), it builds a weak learner on the residuals, and applies a penalization term (learning rate) to decrease the predictive accuracy of the individual tree. Subsequently, it bootstraps a new fraction to fit a new tree from the residuals of the previous tree. The algorithm proceeds this way until all trees have been built. There are alternative versions of boosted trees, which differ from this basic model (e.g. Light Boost, AdaBoost, XGboost). Boosted trees require careful tuning as they depend on a larger number of parameters than Random Forest, such as tree complexity, learning rate, bag-fraction, and the total number of trees. Since trees are used sequentially, the higher the number of trees the higher the risk of overfit, which must be balanced with the amount of regularization (learning rate) and tree complexity. However, if applied carefully, they can reduce the risk of overfitting compared to Random Forest.
As for Random Forest, Boosted decision tree relationships are not directly interpretable but can be inspected through partial response curves. Variable importance measures can be estimated in several ways, such as through split frequency of each variable, or cumulative loss function reduction of using a variable. Here too, Shapley values can be used to further investigate relative variable contributions on the individual predictions.



### Further online resources
{: .no_toc }

- [Scikit learn: 1.10. Decision Trees](https://scikit-learn.org/stable/modules/tree.html){:target="_blank"}
- [Scikit learn: 1.11. Ensemble Methods](https://scikit-learn.org/stable/modules/ensemble.html){:target="_blank"}


## Reference articles
### Method
{: .no_toc }
- {% cite_resource breiman2001random  --style _bibliography/narrative_full %}
- {% cite_resource cutler2007random  --style _bibliography/narrative_full %}
- {% cite_resource death2007boosted  --style _bibliography/narrative_full %}
- {% cite_resource elith2008working  --style _bibliography/narrative_full %}


### Research applications
{: .no_toc }
#### With RS data in Ecology / Biodiversity
{: .no_toc }
- {% cite_resource ham2005investigation  --style _bibliography/narrative_full %}
- {% cite_resource pal2005random  --style _bibliography/narrative_full %}
- {% cite_resource gislason2006random  --style _bibliography/narrative_full %}
- {% cite_resource lawrence2004classification  --style _bibliography/narrative_full %}
- {% cite_resource ghatkar2019classification  --style _bibliography/narrative_full %}


#### Without RS data (Ecology domain)
{: .no_toc }
- {% cite_resource bland2015predicting  --style _bibliography/narrative_full %}
- {% cite_resource cazalis2023prioritizing  --style _bibliography/narrative_full %}

## Implementation 

#### Python
{: .no_toc }
- [scikit-learn](https://scikit-learn.org/stable/modules/tree.html){:target="_blank"}
- [XGBoost](https://xgboost.readthedocs.io/en/stable/){:target="_blank"}

#### R
{: .no_toc }
- [rpart](https://cran.r-project.org/web/packages/rpart/index.html){:target="_blank"}
- [party](https://cran.r-project.org/web/packages/party/index.html){:target="_blank"}
- [randomForest](https://cran.r-project.org/web/packages/randomForest/index.html){:target="_blank"}
- [ranger](https://cran.r-project.org/web/packages/ranger/index.html){:target="_blank"}
- [gbm](https://cran.r-project.org/web/packages/gbm/index.html){:target="_blank"}
- [xgboost](https://cran.r-project.org/web/packages/xgboost/index.html){:target="_blank"}


<!-- For referencement in toc before automatic table -->
## Assessment table
