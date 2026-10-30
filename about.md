---
title: About
layout: about
nav_order: 2
description: "The DAM Navigator is an interactive decision-support tool designed to help researchers explore, compare, and select appropriate detection and attribution modelling methods based on their data, assumptions, and goals."
---

<!-- Logos -->
<div class="logo-row">
  <img src="{{ site.baseurl }}/assets/images/logos/Obsgession_text_logo.png" alt="Obsgession" style="width:250px; margin:0 18px; vertical-align:middle;">
  <img src="{{ site.baseurl }}/assets/images/logos/logo-FRB-Cesab-anglais_cropped.png" alt="FRB Cesab" style="width:175px; margin:0 18px; vertical-align:middle;">
  <img src="{{ site.baseurl }}/assets/images/logos/Logo_cnrs.png" alt="CNRS" style="width:60px; margin:0 18px; vertical-align:middle;">
  <img src="{{ site.baseurl }}/assets/images/logos/logo-leca.png" alt="LECA" style="width:150px; margin:0 18px; vertical-align:middle;">
</div>
--------------------------------


## Table of Contents
{: .no_toc .text-delta }
1. TOC
{:toc}


## Objective
- **NaviDAM** (the Detection and Attribution Modeling Navigator) serves the goal to orient users looking methods for detecting and disentangling the drivers of observed biodiversity change.
It **situates methods**, both *widespread* methods used in ecological studies and approaches inherited from *causal inference* or econometrics, against a set of [criteria]({{ site.baseurl }}/criteria).

- The different [criteria]({{ site.baseurl }}/criteria) also [**invite users**]({{ site.baseurl }}/#user-input) to **specify** what they are looking for and what they have at hands thanks to **dropdown lists**.

- This enables the **narrowing down** of detection and/or attribution [**methods**]({{ site.baseurl }}/methods) and [**tools**]({{ site.baseurl }}/tools) suited to their study.


------------------------------------
## Website structure

NaviDAM is implemented in this collaborative website and is organized around a dynamical filtering tool on the landing page:

1. [Landing page (Home)]({{ site.baseurl }}/):
    - Brief description of the navigator
    - Invite users to fill in [criteria]({{ site.baseurl }}/criteria) to describe their case study
        - Criteria default to `Any`, including all options and therefore not filtering the set of suggested methods

        {: .highlight}
        Incomplete assessments are reported in the output.
    
        {: .note-title }
        > **?** signs
        > 
        > Along each criterion, a **(?)** sign redirects to the description page in the [criteria]({{ site.baseurl }}/criteria) panel.

    - **Candidate methods** is the resulting list of methods that match the user requirements, organised by category. Each method can be clicked on to open the corresponding documentation page.

        <details id="near-misses" markdown="block">
        <summary>Near misses</summary>

        Below the candidate methods, a collapsed **Near misses** section lists the methods that match all the specified criteria but exactly one. Each one is tagged with the single criterion it fails, e.g. *Fails: Handles lag effects (method: Possible, you asked: Yes)*, and the tags are ordered as the criteria are displayed. Near misses are **not** matches: they are shown to help when an assessment is uncertain or too strict, since a single mis-assessed criterion can otherwise hide a suitable method. The section appears when at least one near miss exists, and is expanded by default when no method matches all criteria. Near misses are listed separately and labelled *Near miss (NOT a match)* in the exported `.csv`; the candidate methods and their export are unchanged. In simulations, near misses recover most of the recall lost to assessment errors (when up to about 15% of criteria are mis-assessed), at the cost of a list typically 2-3 times longer: check each failed criterion before considering a near miss.
        </details>
        <script>
        (function () {
          var d = document.getElementById("near-misses");
          function openIfTargeted() { if (d && location.hash === "#near-misses") d.open = true; }
          openIfTargeted();
          window.addEventListener("hashchange", openIfTargeted);
        })();
        </script>

    - The **Graph Explorer** allows exploring, vizualizing and querying the network of methods and criteria (work in progress).
            
        - Exportable outputs: Method scheme `.png`, criteria assessment + methods `.csv`, suited method list `.txt` (work in progress)


{: .important-title}
> The sidebar
>
> The sidebar provides access to different panels grouping resource pages logically.
> Its exploration in regards with the landing page is key for good use of the navigator.


{:style="counter-reset:none"}
1. This *About* page providing a brief introduction to this website

1. [Criteria panel]({{ site.baseurl }}/criteria)

    This panel provides information on every criterion used to subset detection & attribution methods when using the navigator. Pages follow a common documentation structure: *Definition*, *Explanation*, *Tools/rationale for helping assessment* and *Example*.


1. [Method panel]({{ site.baseurl }}/methods)

    This panel provides information on every method listed in the navigator. The methods are described along a common documentation structure: *Description & principle*, *Reference articles*, *Implementation and the *Assessment table* reflecting how the method is filtered against the user's criteria evaluation.



1. [Good practices panel]({{ site.baseurl }}/practices)
    
    This panel provides general resources that aim to help conceptualising and applying attribution methods. Here are page examples that will eventually fit this category:
    - Causal diagrams
    - Getting started 
    - Review articles
    - Comparing multiple methods etc.


1. [Examples]({{ site.baseurl }}/examples)

    This final panel illustrates how the DAM can be used with examples, from the question + data at hands, to the criteria assessment and the method application. Examples will include:
    - STOC + synthetic controls 
    - Other T3.2 applications and project’s voluntary studies

1. The [Contributing]({{ site.baseurl }}/contributing) page that will eventually describe how to contribute to the website's content.


------------------------------------
## Website coverage 📊

The table below is generated automatically at each site build from the assessment and panels tracking files, so it always reflects the current content.

{% include coverage_table.html %}

Want to help fill the gaps? See the [Contributing page]({{ site.baseurl }}/contributing/#website-coverage) for the lists of methods needing contributions. 🌱


------------------------------------
## Contact

- Joaquim Estopinan: firstname.surname @ univ-grenoble-alpes.fr


------------------------------------
## Credits

This is a joint developpement of the <a href="https://obsgession.eu/" target="_blank" rel="noopener noreferrer">OBSGESSION</a> Horizon Europe project and of the <a href="https://www.fondationbiodiversite.fr/en/the-frb-in-action/programs-and-projects/le-cesab/impacts/" target="_blank" rel="noopener noreferrer">IMPACTS</a> research group.