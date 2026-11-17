---
title: "STOC & land cover changes"
parent: Examples
nav_order: 1
categories:
- examples
---

# Impacts of abrupt land cover changes on French common birds
{: .no_toc}

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}


{: .note}
>Biospace25 presentation introducing the study context and first results available on [HAL](https://hal.science/hal-04947333).

Observed biodiversity changes can be hard to attribute to their pressures since they are often highly entangled and barely measured.

*In this [example]({{ site.baseurl }}/examples) page, we showcase how **NaviDAM** can be used to guide method selection (with the [filtering motor]({{ site.baseurl }}/#user-input)) after introducing the [**data**]({{ site.baseurl }}/data) & [**objectives**]({{ site.baseurl }}/objective).*
{: .fs-6 .fw-300 }


# Data

## Temporal Monitoring of Common Birds | STOC

STOC is a standardized count protocol of common birds in France, with data available on the study period **2001-2019** (protocol change in 2001). Partipant observers focus on 2x2 km squares monitored according to an annual random draw, see [Figure 1](#fig1).

![]({{ site.baseurl }}/assets/images/STOC_1.png){: width="100%" }
<div style="text-align:center; font-style:normal;">
  <a id="fig1"></a>
  <a href="#fig1"><strong>Figure 1</strong></a>: STOC coverage in mainland France. <em>Source:</em> {% cite fontaine2020 --style _bibliography/narrative %}
</div>

This survey enables studying the evolution of specialization groups of birds through time:

![]({{ site.baseurl }}/assets/images/STOC_2.png){: width="100%" }
<div style="text-align:center; font-style:normal;">
  <a id="fig2"></a>
  <a href="#fig2"><strong>Figure 2</strong></a>: 75 species are used to construct indicators based on their specialized habitats.
  <em>Source:</em> {% cite fontaine2020 --style _bibliography/narrative %}
</div>


<!-- TODO: Add some STOC plots metrics -->
### Example abundance curves per observation plot
{: .no_toc}

On [Figure 3](#figA1) we plot the monitored abundance of one common species, *Picus viridis*, for a selection of observation squares to give a sense of sampling effort.

![]({{ site.baseurl }}/assets/images/Response-Picus viridis_NoDetections.png){: width="100%" }
<div style="text-align:center; font-style:normal;">
  <a id="figA1"></a>
  <a href="#figA1"><strong>Figure 3</strong></a>: <em>Picus viridis</em> abundance for a selection of observation squares.
</div>


Abundances can also be summed by bird specialization group like in [Figure 4](#figA2), but still appreciated by observation square:
![]({{ site.baseurl }}/assets/images/Response-agricoles_NoDetections.png){: width="100%" }
<div style="text-align:center; font-style:normal;">
  <a id="figA2"></a>
  <a href="#figA2"><strong>Figure 4</strong></a>: Abundance of bird species specialized in agricultural areas for a selection of observation squares.
</div>


{: .note }
It is on this type of bird abundance curves that we will test later in the [attribution](#attribution) section if the detected land cover changes (see [hands-on detection](#det-applied)) have an impact.



## Annual land cover products | GLC_FCS30D

The annual land cover data products originate from {% cite zhang2024  --style _bibliography/narrative %}. It has a 30-meter resolution as based on Landsat imagery, 35 land-cover categoties spanning from 1985 to 2022 (every 5 years before 2000, annual after), see [Figure 5](#fig3). The tiles were downloaded from the project's [Zenodo](https://doi.org/10.5281/zenodo.8239305) and merged as annual mosaics over France using GDAL command lines.

![]({{ site.baseurl }}/assets/images/GLC_figure.png){: width="100%" }
<div style="text-align:center; font-style:normal;">
  <a id="fig3"></a>
  <a href="#fig3"><strong>Figure 5</strong></a>: The overview of the GLC_FCS30D dataset during 1985 to 2022.
  <em>Source:</em> {% cite liu2023 --style _bibliography/narrative %}
</div>


## Intersection | STOC ∩ GLC_FCS30D

We extracted land cover data on the 2x2-km squares matching the STOC survey squares, see the example STOC squares on [Figure 6](#fig4). It results in short **time-series** as illustrated [Figure 7](#fig5).

![]({{ site.baseurl }}/assets/images/stoc_locations_example.png){: width="100%" }
<div style="text-align:center; font-style:normal;">
  <a id="fig4"></a>
  <a href="#fig4"><strong>Figure 6</strong></a>: Example STOC observation squares used to intersect the land cover products.
</div>



![]({{ site.baseurl }}/assets/images/100163.png){: width="100%" }
![]({{ site.baseurl }}/assets/images/100865.png){: width="100%" }
![]({{ site.baseurl }}/assets/images/100972.png){: width="100%" }
![]({{ site.baseurl }}/assets/images/101058.png){: width="100%" }
<div style="text-align:center; font-style:normal;">
  <a id="fig5"></a>
  <a href="#fig5"><strong>Figure 7</strong></a>: Example land cover time-series of STOC observation squares. Open in maps:
  <a href="https://maps.app.goo.gl/xK2LhbhoWW71mWgu6" target="_blank" rel="noopener noreferrer">1.</a>
  <a href="https://maps.app.goo.gl/MGj97EAVnhbihUSp6" target="_blank" rel="noopener noreferrer">2.</a>
  <a href="https://maps.app.goo.gl/3seu5bY1xnhzt5uD8" target="_blank" rel="noopener noreferrer">3.</a>
  <a href="https://maps.app.goo.gl/xZcrQVoNhVzUeX2YA" target="_blank" rel="noopener noreferrer">4.</a>
</div>



# Objectives

The objective of this work is twofold: 
1. `Detection` To identify STOC monitoring squares that have been affected by abrupt landscape changes. To achieve this, we first compute landscape metrics on the annual land cover squares, and second look for a suited detection method with **NaviDAM**.
2. `Effect estimation` To test if the detected landscape changes result in bird diversity metric shifts. If we succeed in estimating significant effects, we could therefore confidently **attribute** or not the diversity shifts to the land cover changes.


# Detection of abrupt landscape changes

- Using [PyLandStats](https://pylandstats.readthedocs.io/en/latest/#) {% cite bosch2019 %}, we computed landscape metrics on the successive land cover annual squares as depicted [Figure 7](#fig5). For the list of available metrics, see PylandStats publication's [Table S1](https://doi.org/10.1371/journal.pone.0225734.s002). We also relied on their user-friendly [notebooks](https://github.com/martibosch/pylandstats-notebooks/tree/main/notebooks) for easy implementation. The R equivalent package is [landscapemetrics](https://r-spatialecology.github.io/landscapemetrics/).


- Then, we tested several landscape metrics assumed to be ecologically relevant for bird populations (e.g. according to the [forest edge effect](https://en.wikipedia.org/wiki/Edge_effects)): `["proportion_of_landscape", "number_of_patches", "largest_patch_index", "total_edge", "landscape_shape_index", "contagion", "shannon_diversity_index"]`.

The objective now is to find a suitable detection method for identifying abrupt changes in landscape metrics. To achieve this, we can use the NaviDAM tool.

## **NaviDAM for detection**

On the <a href="{{ site.baseurl }}/" target="_blank" rel="noopener noreferrer">home</a> page, we reach the <a href="{{ site.baseurl }}/#user-input" target="_blank" rel="noopener noreferrer">User input invite</a> to evaluate the task needs:

- We start by choosing the objective `Detection`:

<a id="data-det"></a>
<div style="text-align:center;">
      <figure style="display:inline-block; border:2px solid #bdbdbd; padding:0.6rem; border-radius:6px; background:#ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
    <img src="{{ site.baseurl }}/assets/images/obj-data.png" style="width:85%; display:block; margin:0 auto;" />
    <figcaption style="text-align:center; font-size:normal; padding-top:0.4rem;">
      <a id="fig6"></a>
      <a href="#fig6"><strong>Figure 8</strong></a>: <em>Detection</em> user input | Objective and data options.
    </figcaption  >
  </figure>
</div>

- And now describe our data:
  - **Type:** We have `Panel data`, i.e. time-series for different samples (here the STOC observation squares).
  - **Time-series length:** We have 26 time steps, so `≥ 10` and `< 100`.
  - **Handles few samples:** `No need`, we have thousands of points.
  - **Scalable to big data:** `No need` idem. Even if we scale up the study to other monitoring programs, the relative scarcity of standardized data doesn't require big data approaches.
  - **Handles missing data:** `Simple corrections feasible` even if we have complete time-series here, we prefer imposing this condition in case remote sensing data would be missing when upscaling the study.
  - **RS-data proven:** `At least few RS applications exist` no special need to rely on a estbalished method with RS data (land cover here), few applications would be enough.


<p>&nbsp;</p>
<div style="text-align:center;">
      <figure style="display:inline-block; border:2px solid #bdbdbd; padding:0.6rem; border-radius:6px; background:#ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
    <img src="{{ site.baseurl }}/assets/images/model_props.png" style="width:85%; display:block; margin:0 auto;" />
    <figcaption style="text-align:center; font-size:normal; padding-top:0.4rem;">
      <a id="fig7"></a>
      <a href="#fig7"><strong>Figure 9</strong></a>: <em>Detection</em> user input | Model properties.
    </figcaption  >
  </figure>
</div>

- Next, the desired model properties (criteria have been adapted to the `Detection` objective):
  - **Requires explicit processes:** `Agnostic` No knowledge nor a priori on the expected change form apart than being abrupt.
  - **Exposure type:** `Binary` Monitoring abrupt land cover changes implies having a Before/After study design.
  - **Number of variables:** `Univariate` Even if we test various landscape metrics, we consider them one after the other.



<p>&nbsp;</p>
<div style="text-align:center;">
      <figure style="display:inline-block; border:2px solid #bdbdbd; padding:0.6rem; border-radius:6px; background:#ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
    <img src="{{ site.baseurl }}/assets/images/packages.png" style="width:85%; display:block; margin:0 auto;" />
    <figcaption style="text-align:center; font-size:normal; padding-top:0.4rem;">
      <a id="fig8"></a>
      <a href="#fig8"><strong>Figure 10</strong></a>: <em>Detection</em> user input | Implementation.
    </figcaption  >
  </figure>
</div>


- About the implementation, simple expectations :
  - **Language:** `Python`, `R` We prefer here these two common programming languages for running analyses in batch.
  - **Usage:** `User-friendly`, `Technical but well documented` To keep analyses easily reproducible.



<p>&nbsp;</p>
<div style="text-align:center;">
      <figure style="display:inline-block; border:2px solid #bdbdbd; padding:0.6rem; border-radius:6px; background:#ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
    <img src="{{ site.baseurl }}/assets/images/assumptions.png" style="width:85%; display:block; margin:0 auto;" />
    <figcaption style="text-align:center; font-size:normal; padding-top:0.4rem;">
      <a id="fig9"></a>
      <a href="#fig9"><strong>Figure 11</strong></a>: <em>Detection</em> user input | Assumptions.
    </figcaption  >
  </figure>
</div>


- Finally the assumptions, again adapted to the `Detection` objective:
  - **Functional form:** `Rule-based`, `Non-linear`, `Assumption-free` Expecting an abrupt change to be detected, the best option is likely `Rule-based` with a rule level fitted on the data. However, we also keep other options to avoid being too stringent on the method sub-selection & retain more candidate methods.
  - **Model specific:** `No specific` No particular expectation.


<p style="color:#28a745;"><em><strong>--></strong> All criteria have been assessed so the counter on the right turns to green.</em></p>



<p>&nbsp;</p>
<div style="text-align:center;">
      <figure style="display:inline-block; border:2px solid #bdbdbd; padding:0.6rem; border-radius:6px; background:#ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
    <img src="{{ site.baseurl }}/assets/images/results.png" style="width:85%; display:block; margin:0 auto;" />
    <figcaption style="text-align:center; font-size:normal; padding-top:0.4rem;">
      <a id="fig10"></a>
      <a href="#fig10"><strong>Figure 12</strong></a>: <em>Detection</em> user input | Result.
    </figcaption  >
  </figure>
</div>

{: .highlight-title}
> Status
>
> For now, only the method family [Outlier detection]({{ site.baseurl }}/contents/methods/detection/outlier-detection/) matches the specified criteria and the page hasn't been documented yet.
> To speed up NaviDAM implementation, see the [contributing]({{ site.baseurl }}/contributing) page.
> However, this case study page already illustrates how the filtering tool can be used to find candidate methods suited to your project.
> 
> **Eventually, different methods will be suggested after such an exercise, and users will then be able to consult the corresponding documentation pages and jump to the relevant resources to inform their method choice.**

<a id="det-applied"></a>

## Hands-on outlier detection

**Abrupt changes were defined as a deviation superior to *B* standard deviation to the average annual change. It allowed detecting plots affected by sudden landscape change and at which years.**

{: .new-title }
> Outlier detection as extreme deviation from mean annual change
>
> In this case study, we simply detected abrupt changes by:
> - Choosing a target level: `landscape` / `class` metrics
>   - If `class`, choosing a target class, e.g. `Impervious surfaces`
>  - Choosing a target metric and sign, e.g. `proportion_of_landscape` / `+` 
>  - Choosing a deviation level with *B*, see [this table](https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule#Table_of_numerical_values) for corresponding proportions.
> - Then, we compute the interval I of time-series within the tolerated deviation range  for the chosen metric as:
> `I = [avg - B*std, avg + B*std]` after standardizing the successive annual changes.
> - Finally, we identify the time series affected by extreme land cover changes that *i)* ∉ `I`, and *ii)* are either positive, negative or both depending on the chosen sign.


<p>&nbsp;</p>
### Example of detected abrupt change
{: .no_toc .text-delta }

<p>&nbsp;</p>
![]({{ site.baseurl }}/assets/images/class_Impervious surfaces_proportion_of_landscape_100B300_detect_2007-2016_NbSTOC2790_ID100824_sign+.png){: width="100%" }
<div style="text-align:center; font-style:normal;">
  <a id="fig11"></a>
  <a href="#fig11"><strong>Figure 13</strong></a>: Example 1 of detected abrupt change | class: Impervious surfaces, metric: proportion_of_landscape, Sign:+, B=3. <a href="https://maps.app.goo.gl/tYcrKoaYPKLMVAJ27" target="_blank" rel="noopener noreferrer">Open in maps.</a>
  <em>Solar panel site construction</em>
</div>


<p>&nbsp;</p>
<details markdown="block">
<summary><strong>More examples</strong></summary>

<p>&nbsp;</p>
![]({{ site.baseurl }}/assets/images/class_Impervious surfaces_proportion_of_landscape_100B300_detect_2007-2016_NbSTOC2790_ID101820_sign+.png){: width="100%" }
<div style="text-align:center; font-style:normal;">
  <a id="fig12"></a>
  <a href="#fig12"><strong>Figure 14</strong></a>: Example 2 of detected abrupt change | class: Impervious surfaces, metric: proportion_of_landscape, Sign:+, B=3. <a href="https://maps.app.goo.gl/drQSjKqau6ihNcBa7" target="_blank" rel="noopener noreferrer">Open in maps.</a>
  <em>Boat terminal construction</em>
</div>


<p>&nbsp;</p>
![]({{ site.baseurl }}/assets/images/class_Impervious surfaces_proportion_of_landscape_100B300_detect_2007-2016_NbSTOC2790_ID102495_sign+.png){: width="100%" }
<div style="text-align:center; font-style:normal;">
  <a id="fig13"></a>
  <a href="#fig13"><strong>Figure 15</strong></a>: Example 3 of detected abrupt change | class: Impervious surfaces, metric: proportion_of_landscape, Sign:+, B=3. <a href="https://maps.app.goo.gl/ZsTrFp8janyE7vfUA" target="_blank" rel="noopener noreferrer">Open in maps.</a>
  <em>Railroad construction</em>
</div>


</details>


## Detection events aligned on bird abundance curves

Once abrupt land cover changes detected, we can align them on the bird abundance curves as introduced [before](#Acurves). See for instance the abundance curve of *Picus viridis* from [Fig. 3](#figA1) but with the years detected as following abrupt class propotion increase of impervious surfaces:

![]({{ site.baseurl }}/assets/images/Response-Picus viridis_class_Impervious surfaces_proportion_of_landscape_100B200_detect_2007-2016_NbSTOC2790_sign+.csv.png){: width="100%" }
<div style="text-align:center; font-style:normal;">
  <a id="fig16"></a>
  <a href="#fig16"><strong>Figure 16</strong></a>: <em>Picus viridis</em> abundance for a selection of observation squares with detected events overlaid: abrupt class proportion increase of impervious surfaces.
</div>



<a id="attribution"></a>

# Bird diversity metric shifts attribution

The objective is now to determine whether detected changes in land cover affect bird biodiversity metrics, and if so, to quantify the impact.
To help us choose an appropriate method, we will use the NaviDAM filtering tool again, but this time for a different objective: `Effect estimation`.


## **NaviDAM for attribution**

As we did with the *Detection* objective, we will now go through the different criteria options of the <a href="{{ site.baseurl }}/#user-input" target="_blank" rel="noopener noreferrer">User input invite</a> for the `Effect estimation` objective and explain them when needed.


<p>&nbsp;</p>
<div style="text-align:center;">
      <figure style="display:inline-block; border:2px solid #bdbdbd; padding:0.6rem; border-radius:6px; background:#ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
    <img src="{{ site.baseurl }}/assets/images/attrib_0.png" style="width:85%; display:block; margin:0 auto;" />
    <figcaption style="text-align:center; font-size:normal; padding-top:0.4rem;">
      <a id="fig17"></a>
      <a href="#fig17"><strong>Figure 17</strong></a>: <em>Attribution</em> user input | Objective, outcome and data.
    </figcaption  >
  </figure>
</div>

- With this second objective to attribute & quantify the effect of landscape changes, we now specify:
  - **Estimand:** `ATE`, `ATT` as we are interested in general effects not local or conditional ones, nor in the other suggestions.


- About the criteria on data compatibility, the requirements are the same as for the `Detection` objective [above](#data-det), details are also collapsed here:
<details markdown="block">
<summary>Data compatibility details.</summary>
  - **Type:** We have `Panel data`, i.e. time-series for different samples (here the STOC observation squares).
  - **Time-series length:** We have 26 time steps, so `≥ 10` and `< 100`.
  - **Handles few samples:** `No need`, we have thousands of points.
  - **Scalable to big data:** `No need` idem. Even if we scale up the study to other monitoring programs, the relative scarcity of standardized data doesn't require big data approaches.
  - **Handles missing data:** `Simple corrections feasible` even if we have complete time-series here, we prefer imposing this condition in case remote sensing data would be missing when upscaling the study.
  - **RS-data proven:** `At least few RS applications exist` no special need to rely on a estbalished method with RS data (land cover here), few applications would be enough.
</details>



<p>&nbsp;</p>
<div style="text-align:center;">
      <figure style="display:inline-block; border:2px solid #bdbdbd; padding:0.6rem; border-radius:6px; background:#ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
    <img src="{{ site.baseurl }}/assets/images/attrib_1.png" style="width:85%; display:block; margin:0 auto;" />
    <figcaption style="text-align:center; font-size:normal; padding-top:0.4rem;">
      <a id="fig18"></a>
      <a href="#fig18"><strong>Figure 18</strong></a>: <em>Attribution</em> user input | Model properties.
    </figcaption  >
  </figure>
</div>


- Next come the desired model properties:
  - **Requires explicit processes:** `Agnostic`, `Optional` since we don't know how to model such process here
  - **Exposure type:** `Binary` as the before/after detected abrupt change from one year to the other
  - **Number of variables:** `Bivariate`, `Multivariate` Here we have at least two variables in the exposure and the tested biodiversity metrics. We can even consider more than two variables at a time, e.g. to make sure to isolate the impact of landscape changes and not bioclimatic variations.
  - **Propagates uncertainty:** `Model-specific tools` - We would like *at least* model-specific tools (or even `inherent-capacity` to deal with uncertainty as it is an *ordinal* criteria).
  - **Handles lag effects:** `No need` because we are interested here in immediate effects of land cover change
  - **Parametric nature:** `Unsure` - Any option would actually suits us, we have no expectation so `Unsure` allows overpassing this criterion while indicating it as been evaluated. Letting `Any` would lead to same result (but an uncomplete assessment flagged), just as selecting the four non-default options.


<p>&nbsp;</p>
<div style="text-align:center;">
      <figure style="display:inline-block; border:2px solid #bdbdbd; padding:0.6rem; border-radius:6px; background:#ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
    <img src="{{ site.baseurl }}/assets/images/attrib_2.png" style="width:85%; display:block; margin:0 auto;" />
    <figcaption style="text-align:center; font-size:normal; padding-top:0.4rem;">
      <a id="fig19"></a>
      <a href="#fig19"><strong>Figure 19</strong></a>: <em>Attribution</em> user input | Implementation.
    </figcaption  >
  </figure>
</div>

- About the expectations on the implementation:
  - **Language:** `Python`, `R`, same as for detection
  - **Usage:** `Domain-specific skills` added to `User-friendly` and `Technical but well documented` to keep maximum suggested methods and assuming the user is used to such impact analysis


<p>&nbsp;</p>

{: .important }
> Investigators are invited to specify method assumptions at the end of the filtering process.
> This way, when assumptions are not (fully) specified with `Any` or `Unsure` options, NaviDAM suggests a **set of methods** relying on **different assumptions**. This enables users to **compare results** across methods, assess the robustness or sensitivity of findings to assumptions, and interpret their results with multiple lines of evidence.

<div style="text-align:center;">
      <figure style="display:inline-block; border:2px solid #bdbdbd; padding:0.6rem; border-radius:6px; background:#ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
    <img src="{{ site.baseurl }}/assets/images/attrib_3.png" style="width:85%; display:block; margin:0 auto;" />
    <figcaption style="text-align:center; font-size:normal; padding-top:0.4rem;">
      <a id="fig20"></a>
      <a href="#fig20"><strong>Figure 20</strong></a>: <em>Attribution</em> user input | Assumptions.
    </figcaption  >
  </figure>
</div>


- Finally, the assumptions:
  - As indicated in the above box, a number of criteria are only informed with `Unsure`: It avoids filtering based on their options when the user does not want to emphasise an assumption. The opposite would be looking for a method that explicitly *relaxes* or firmly *requires* an assumption. Criteria with `Unsure` are note detailed here.
  - **No unobserved confounders:** `Recommended / Desirable`, `No need: method relaxes assumption`. In our case study, we certainly have unobserved confounders impacting both the tested outcome and our exposure. We also have *observed* confounders like climatic variables that will be controlled for, but others are unobserved, e.g. land use intensity. We therefore need a method that can deal with such bias, hence the chosen options.
  - **IID:** `Assumption required`, `Recommended / Desirable` - We can reasonably assume having IID samples regarding the semi-standardized sampling protocol.


<p style="color:#008080;"><em><strong>--></strong> All criteria have been assessed or at least considered with `Unsure`, so the counter on the right turns to teal.</em></p>


<p>&nbsp;</p>
<div style="text-align:center;">
    <figure style="display:inline-block; border:2px solid #bdbdbd; padding:0.6rem; border-radius:6px; background:#ffffff; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
    <img src="{{ site.baseurl }}/assets/images/attrib_4.png" style="width:85%; display:block; margin:0 auto;" />
    <figcaption style="text-align:center; font-size:normal; padding-top:0.4rem;">
      <a id="fig21"></a>
      <a href="#fig21"><strong>Figure 21</strong></a>: <em>Attribution</em> user input | Result.
    </figcaption  >
  </figure>
</div>

{: .new-title}
> Result
>
> A set of candidate methods belonging to three different families is suggested. As for `Detection`, lots of methods have still to be assessed in order to be included in NaviDAM filtering tool and we invite interested users to look at the [contributing]({{ site.baseurl }}/contributing) page or contact.
>
> Since Experiments are impossible in this project, we can choose between the remaining adjusted and quasi-experimental method suggestions. We choose [**synthetic controls**]({{ site.baseurl }}/contents/methods/quasi-exps/synthetic-controls/) and can now consult the associated documentation page before applying them in next section.




## Hands-on synthetic controls

- According to the synthetic control methodology, we gathered and aligned covariate data (bioclimatic variables, PatriNat anthropogenic pressures) on our treated sites and donor pools to then best identify suited control observation squares.
- We also computed several bird community metrics (`Alpha, Beta (turnover), Shannon diversity, Pielou index`) to explore the impact of land cover changes on aggregated metrics.

{: .highlight-title }
> Status
>
> Several variants of synthetic controls have already been applied and results will be integrated here later.


## Perspectives

We plan to further exploit {% cite reif2021 santini2017assessing %} to guide tests on:
- *i)* which bird species and populations, monitored with 
- *ii)* which diversity metric, are sensitive to
- *iii)* which landscape changes.

{: .note }
In this example, we don't cover the significance and robustness tests independently as it could be done in the filtering tool as the page is already large. However, synthetic controls already present model-specific inherent placebo and significance tests.


# References
<!-- Add References section here -->
<div class="references-section">
  {% bibliography --cited_in_order %}
</div>