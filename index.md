---
title: Home
layout: home
nav_order: 1
description: "NaviDAM provides a criteria-based engine to allow users describing their case-study properties and identify a set of suited attribution methods."
permalink: /
---

<!-- Logos -->
<div class="logo-row">
  <img src="{{ site.baseurl }}/assets/images/logos/Obsgession_text_logo.png" alt="Obsgession" style="width:250px; margin:0 18px; vertical-align:middle;">
  <img src="{{ site.baseurl }}/assets/images/logos/logo-FRB-Cesab-anglais_cropped.png" alt="FRB Cesab" style="width:175px; margin:0 18px; vertical-align:middle;">
  <img src="{{ site.baseurl }}/assets/images/logos/Logo_cnrs.png" alt="CNRS" style="width:60px; margin:0 18px; vertical-align:middle;">
  <img src="{{ site.baseurl }}/assets/images/logos/logo-leca.png" alt="LECA" style="width:150px; margin:0 18px; vertical-align:middle;">
</div>
--------------------------------

<!-- Choices.js CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/choices.js/public/assets/styles/choices.min.css" />
<!-- Choices.js JS -->
<script src="https://cdn.jsdelivr.net/npm/choices.js/public/assets/scripts/choices.min.js"></script>


# **NaviDAM** - A decision tool to help you navigate *Detection* and *Attribution* Methods


## Welcome !

NaviDAM is a collaborative decision-support platform designed to help users explore, compare, and select appropriate detection and attribution methods based on the nature of their project.
{: .fs-6 .fw-300 }


- **Users are invited [below](#user-input) to qualify their _objective_, _data at hands_ and affordable _assumptions_ between others by assessing different <a href="{{ site.baseurl }}/criteria" target="_blank" rel="noopener noreferrer">criteria</a>**
- ***<u>A set of</u>* [suited methods](#candidate-methods) is provided and methods are described in more detail on <a href="{{ site.baseurl }}/methods" target="_blank" rel="noopener noreferrer">documentation pages</a>, allowing users to get started on their project using relevant resources**

*Learn more about NaviDAM on the [About page]({{ site.baseurl }}/about).*

<p style="text-align: right;"><em>Latest release: v2.1</em><br><a href="https://doi.org/10.5281/zenodo.23396723"><img src="https://img.shields.io/badge/DOI-10.5281%2Fzenodo.23396723-blue?logo=doi&logoColor=white" alt="DOI: 10.5281/zenodo.23396723" width="205" height="20" style="vertical-align: middle;"></a></p>

{: .important }
Consult the [Good practices]({{ site.baseurl }}/practices) panel and **especially** the <a href="{{ site.baseurl }}/contents/practices/box1/" target="_blank" rel="noopener noreferrer">Beyond method selection page</a> for guidance on how to design a robust study and reach credible results.

--------------------------------


<a id="user-input"></a>
## [User input invite](#user-input){: .btn .btn-purple } <span style="font-size:1em;">&#8594;</span> Evaluating your project's needs

Choose the [criteria]({{ site.baseurl }}/criteria) options that **best describe your project**. Criteria are adapted to each objective.

{: .new-title }
> Tips for reliable assessments
> 
> 1. Specify only what your study clearly requires; leave doubtful criteria on `Unsure`.
> 2. Beyond about **8-12** criteria, extra ones rarely narrow the list but can wrongly exclude a suitable method.
> 3. Check the [near misses](#near-misses): methods failing exactly one criterion.
> 4. If no method matches, re-check your answers before concluding none fits.


<script type="module" src="assets/js/filter.js"></script>

<script id="site-baseurl" type="application/json">
  "{{ site.baseurl }}"
</script>

<script id="cat-dicts" type="application/json">
  {{ site.data.cat_dicts | jsonify }}
</script>

<script id="criteria-mapping" type="application/json">
  {{ site.data.criteria_mapping | jsonify }}
</script>

<script id="method-data" type="application/json">
  {{ site.data.method_assessments_clean | jsonify }}
</script>

<script id="objective-criteria-map" type="application/json">
  {{ site.data.objective_criteria_map | jsonify }}
</script>

<div id="criteria-filters"></div>

<details markdown="block">
<summary>Note on assumptions</summary>

{: .important }
> Investigators are invited to specify method assumptions at the end of the filtering process. This way, when assumptions are not (fully) specified with `Any` or `Unsure` options, NaviDAM suggests a **set of methods** relying on **different assumptions**. This enables users to **compare results** across methods, assess the robustness or sensitivity of findings to assumptions, and interpret their results with multiple lines of evidence.
</details>


<div class="criteria-status-row">
  <div id="criteria-status"></div>
</div>

<div class="reset-btn-row">
  <a href="#" id="reset-filters-btn" class="btn">Reset all criteria</a>
</div>


--------------------------------
## Candidate methods

{: .important }
> Consult the [Good practices](http://127.0.0.1:4000/practices) panel and especially the [Beyond method selection page](http://127.0.0.1:4000/contents/practices/box1/) for guidance on how to design a robust study and reach credible results.

<div style="text-align:center; font-size:0.9em; font-style:italic; font-style:bold;">
Rather than suggesting a single 'unicorn' method, NaviDAM provides a subset of candidate methods that meet the specified criteria and offer complementary insights into the studied system
</div>

<a id="suggested-methods"></a>
<div id="filtered-methods"></div>


<div class="evaluation-export-panel">
  <h3>Export evaluation</h3>
  <p>Download the selected criteria options, category rationales, and suggested methods.</p>
  <label for="evaluation-title">Title</label>
  <input type="text" id="evaluation-title" maxlength="120" placeholder="project_name" />
  <button type="button" id="export-evaluation-btn" class="btn">Export (.csv)</button>
  <span id="export-evaluation-status" role="status" aria-live="polite"></span>
</div>




------------------------------------

{: .note-title }
> Credits
> 
> This is a joint developpement of the <a href="https://obsgession.eu/" target="_blank" rel="noopener noreferrer">OBSGESSION</a> Horizon Europe project and of the <a href="https://www.fondationbiodiversite.fr/en/the-frb-in-action/programs-and-projects/le-cesab/impacts/" target="_blank" rel="noopener noreferrer">IMPACTS</a> research group.



[Just the Docs]: https://just-the-docs.github.io/just-the-docs/
[GitHub Pages]: https://docs.github.com/en/pages
[Jekyll]: https://jekyllrb.com
[Bundler]: https://bundler.io/
[Markdown]: https://daringfireball.net/projects/markdown/
<!-- [**Neo4j**]: https://neo4j.com/docs/getting-started/graph-database/ -->