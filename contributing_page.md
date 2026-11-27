---
title: Contributing
layout: about
nav_order: 7
permalink: /contributing/
description: "Describe how to contribute to NaviDAM"
---

{% capture contributing_content %}{% include_relative CONTRIBUTING.md %}{% endcapture %}
{% capture contributing_toc %}
## Table of contents
{: .no_toc }

<nav aria-label="Contributing table of contents">
<ul>
{% for section in site.data.contributing_nav %}
  <li><a href="#{{ section.anchor }}">{{ section.title | escape }}</a></li>
{% endfor %}
</ul>
</nav>

<a id="at-a-glance-"></a>
{% endcapture %}
{{ contributing_content | replace_first: '<a id="at-a-glance-"></a>', contributing_toc }}

<a id="website-coverage"></a>
<a id="website-coverage-"></a>
## 11. Website coverage 📊

The table below is generated automatically at each site build from the assessment and panels tracking files, so it always reflects the current content.

{% include coverage_table.html %}

<a id="where-help"></a>
<a id="where-help-is-needed-"></a>
## 12. Where help is needed 🌱

The lists below are also generated automatically at each site build.

{% include contribution_lists.html %}
