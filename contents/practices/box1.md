---
layout: baserefs
title: "Beyond method selection: Good practices for credible inference"
practice_status_key: "Beyond method selection"
nav_title: "Beyond method selection"
parent: "Good practices"
nav_order: 2
date: 2026-06-15
author: Joaquim Estopinan
categories:
- practices
---
Robust biodiversity change studies rely on sound study design and transparent reasoning. In practice, this means defining a precise research question and estimand (<a href="{{ site.baseurl }}/outcome">objective + estimand criteria</a>), as well as adhering to the principles below outlined in best-practice checklists {% cite schrodt2025advancing dee2026open elm2007strengthening %}.

<div style="display:grid; grid-template-columns:78px 1fr; column-gap:14px; align-items:stretch; margin:16px 0;">
	<div style="display:flex; flex-direction:column; justify-content:center; align-items:center; gap:6px;">
		<img src="{{ '/assets/images/logos/assumptions.png' | relative_url }}" alt="Assumptions icon" width="58" style="display:block;" />
		<img src="{{ '/assets/images/logos/dag_green.png' | relative_url }}" alt="DAG icon" width="58" style="display:block;" />
	</div>
	<div>
		<p><strong>1. Make all assumptions explicit.</strong> All methods rely on assumptions (data-generating process, interactions, independence etc.):</p>
		<ul style="font-size:0.94em;">
			<li>Draw and justify a causal model (DAG), clarify variable roles (confounders, mediators, etc.)</li>
			<li>State the identification strategy, which variables are controlled, which are unobserved</li>
			<li>Introduce any model-specific assumptions, e.g. parallel trends when using designs like difference-in-differences</li>
			<li>Remind any common but often implicit statistical assumptions (e.g. IID)</li>
		</ul>
        <p style="text-align:right; margin:0 0 6px 0;">&rarr; <a href="{{ site.baseurl }}/assumptions/index.md" >Assumptions criteria</a></p>
	</div>
</div>

<div style="display:grid; grid-template-columns:78px 1fr; column-gap:14px; align-items:stretch; margin:16px 0;">
	<div style="display:flex; flex-direction:column; justify-content:center; align-items:center; gap:6px;">
		<img src="{{ '/assets/images/logos/hammer.png' | relative_url }}" alt="Robustness icon" width="58" style="display:block;" />
		<img src="{{ '/assets/images/logos/sensitivity.png' | relative_url }}" alt="Sensitivity icon" width="58" style="display:block;" />
	</div>
	<div>
		<p><strong>2. Check robustness and perform sensitivity analyses.</strong> Verify that conclusions do not hinge on a particular model choice or untestable assumption:</p>
		<ul style="font-size:0.94em;">
			<li>Run robustness analyses: alternative covariates, sample subsets, estimators, functional forms</li>
			<li>Test partial identification, report how results shift under plausible assumption violations, provide unadjusted estimates for comparison</li>
			<li>Compute sensitivity measures (e.g. Rosenbaum bounds, E-values) for hidden confounding</li>
			<li>Use falsification tests (e.g. placebo outcomes or treatments, balance tests) to quantify how much hidden biases or modeling choices could alter results</li>
		</ul>
        <p style="text-align:right; margin:0 0 6px 0;">&rarr; <a href="{{ site.baseurl }}/objective">Significance and robustness tests objective </a></p>
	</div>
</div>

<div style="display:grid; grid-template-columns:78px 1fr; column-gap:14px; align-items:stretch; margin:16px 0;">
	<div style="display:flex; flex-direction:column; justify-content:center; align-items:center; gap:6px;">
		<img src="{{ '/assets/images/logos/comparison.png' | relative_url }}" alt="Comparison icon" width="58" style="display:block;" />
		<img src="{{ '/assets/images/logos/balance.png' | relative_url }}" alt="Balance icon" width="58" style="display:block;" />
	</div>
	<div>
		<p><strong>3. Triangulate evidence across approaches.</strong> No single method is definitive. Gain confidence by comparing independent lines of evidence:</p>
		<ul style="font-size:0.94em;">
			<li>Compare results from different statistical methods (e.g. matching vs. regression)</li>
			<li>Complement an observational analysis with a controlled experiment or a mechanistic model when possible, check if related studies show consistent patterns</li>
			<li>Interpret results conservatively and in regard to assumptions: If different approaches point to the same conclusion, it bolsters credibility. Conversely, if methods diverge, report that it may reveal hidden biases (model misspecifications, uncontrolled confounding, etc.)</li>
		</ul>
        <p style="text-align:right; margin:0 0 6px 0;">&rarr; <a href="{{ site.baseurl }}/contents/practices/usage_diagram/">Usage diagram</a></p>
	</div>
</div>

<div style="display:grid; grid-template-columns:78px 1fr; column-gap:14px; align-items:stretch; margin:16px 0;">
	<div style="display:flex; flex-direction:column; justify-content:center; align-items:center; gap:6px;">
		<img src="{{ '/assets/images/logos/transparency.png' | relative_url }}" alt="Transparency icon" width="58" style="display:block;" />
		<img src="{{ '/assets/images/logos/checklist.png' | relative_url }}" alt="Checklist icon" width="58" style="display:block;" />
	</div>
	<div>
		<p><strong>4. Report analyses transparently and acknowledge limitations.</strong> Enable readers to understand, reproduce, and critically evaluate your findings by:</p>
		<ul style="font-size:0.94em;">
			<li>Precisely document all analysis and data decisions (covariates, data sources, sample exclusions, identification strategy)</li>
			<li>Share data and code</li>
			<li>Describe study limitations (e.g. biased study design, unmeasured confounders, measurement errors, unaddressed uncertainty, limitation to generalizability)</li>
		</ul>
        <p style="text-align:right; margin:0 0 6px 0;">&rarr; <a href="{{ site.baseurl }}/contents/practices/usage_diagram/">Usage diagram</a></p>
	</div>
</div>


