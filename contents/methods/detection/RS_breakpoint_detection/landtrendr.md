---
layout: method
title: "LandTrendr"
parent: "RS breakpoint detection"
date: 2026-04-28
author: Lori Giagnacovo, VITO
---
<!-- This file was auto-generated from _data/Attribution methods - Method Assessment.tsv -->

## Table of Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Description & principle

The strategy of the LandTrendr algorithm is to distill a multi-year
spectral trajectory into sequential straight-line segments that
adequately capture the character of spectral progressive changes, and
then to leverage that simplified rendition of the time-series to extract
useful information. The LandTrendr algorithm attempts to isolate the
underlying shape of the trajectory while removing the noise (i.e.,
temporal segmentation). This achieved in two broad steps: a breakpoint
identification step, and a model-fitting step (fitting parameters can be
decided by the user). A single disturbance requires three segments: a
pre-disturbance segment, the change segment, and a post-disturbance
segment.

The LandTrendr algorithm was built to use imagery from the Landsat
family of sensors, however, it can be presented time-series of any
numeric sequence, whether from Landsat sensors, other satellite sensors,
or an entirely different source. The algorithm assumes that there is one
entry per year; if you use a different time step, you will need to
"trick" the algorithm into thinking it is looking at yearly data. If
there are not enough observations over time from a given sensor, it will
not be appropriate for LandTrendr. As a rule of thumb, there should be
roughly three to four times as many observations as the maximum number
of periods you wish the algorithm to discriminate.

## Major variants
{: .no_toc }
{: .d-inline-block }
optional
{: .label}

## Further online resources
{: .no_toc }
[https://openmrv.org/web/guest/w/modules/mrv/modules_2/landtrendr](https://openmrv.org/web/guest/w/modules/mrv/modules_2/landtrendr){:target="_blank"}

## Reference articles

### Method
{: .no_toc }

- {% cite_resource kennedy2010detecting --style _bibliography/narrative %}

- {% cite_resource kennedy2018implementation --style _bibliography/narrative %}

- {% cite_resource kennedy2024interpreting --style _bibliography/narrative %}

### Research applications
{: .no_toc }

#### With RS data in Ecology / Biodiversity
{: .no_toc }
- {% cite_resource yang2018detecting --style _bibliography/narrative %}

- {% cite_resource cohen2018landtrendr --style _bibliography/narrative %}

- {% cite_resource zhu2019longterm --style _bibliography/narrative %}

- {% cite_resource parracciani2024land --style _bibliography/narrative %}

#### Without RS data (Ecology domain)
{: .no_toc }

## Implementation

#### Python
{: .no_toc }
- [lt-gee-py](https://pypi.org/project/lt-gee-py/){:target="_blank"} (Python interface to the Google Earth Engine implementation
  of the LandTrendr spectral-temporal segmentation algorithm)

- The LandTrendr class from lt-gee-py is a light wrapper around the
  Google Earth Engine API that includes convenience methods to generate
  images and collections in the format required for LandTrendr on GEE
  (be aware this package is in alpha and may change).

#### R
{: .no_toc }
- [LandTrendR-Package](https://github.com/IFGI-Project/LandTendR-Package){:target="_blank"}

- The package help users to run Landtrendr Algorithm in R, this package
  use GEE python API and requires the user to have a GEE account. The
  package creates a Collection with all the preprocessing and
  Harmonizing required to run Landtrendr, also allows the user to have
  control on the main parameters for the algorithm and the
  ImageCollection creation.

### Code Cells
{: .no_toc }
[https://github.com/eMapR/LT-GEE](https://github.com/eMapR/LT-GEE){:target="_blank"}

## Assessment table
