---
title: Model-specific
parent: Assumptions
nav_order: 9
permalink: /modelspecific
categories:
- criteria
- assumptions
---

# Model-specific assumption

|  **Option**        | **Description**            |
|:------------------:|----------------------------|
| `Parallel trends` | Requires that, in the absence of intervention, treated and control groups would follow the same time‐trend in the outcome (critical for DiD and BACI designs). |
| `Stationarity` | Assumes statistical properties (mean, variance, autocorrelation) remain constant over time, enabling reliable time‐series or panel inference. |
| `Demographic rates` | Dispersal, reproduction and mortality rates must be explicitly specified and realistic in mechanistic models. |
| `Instrument validity` | The instrument influences the outcome only through its effect on treatment, with no direct or backdoor pathways. |
| `Normality of random effects` | Random intercepts or slopes in mixed models are assumed to follow a Gaussian distribution for correct variance‐component estimation. |
| `No M-O confounding` | In mediation analysis, the mediator–outcome relationship must be free of unmeasured confounders. |
| `Good covariate balance` | Assumes treated and control units are comparable on observed covariates after adjustment. |
| `Effect entirely mediated` | For frontdoor approaches, all of the treatment’s effect on the outcome must pass through the specified mediator with no direct path. |
| `Cutoff + PO continuity` | A clearly defined assignment cutoff and continuity of potential outcomes at that threshold. |
| `B/A treatment obs.` | Assumes a sufficient number of observations both before and after the intervention to establish stable trends. |
| `Good pretreatment fit` | Validity relies on closely matching pre‐intervention trajectories between treated and control units. |
| `Time-varying OR site-varying` | Assumes confounding is either time‐invariant and site-specific or time-varying but common to all sites. |
| `Non-Gaussian noise` | Disturbances must be non-Gaussian, which makes the causal direction identifiable (e.g., LiNGAM). |
| `Independent noise` | The effect is a restricted function of its cause (e.g., additive) plus noise independent of the cause, which makes the causal direction identifiable. |
| `Invariance across environments` | The causal mechanism from causes to outcome stays the same across environments or interventions (e.g., invariant causal prediction). |

## Definition
Any critical assumption unique to the method’s structure and validity (e.g., parallel trends for DiD, stationarity for time‐series, instrument validity for IV). 

## Explanation
These distinctive assumptions determine when the method yields valid estimates. Understanding these domain‐specific criteria is crucial for correct application and interpretation of certain methods.

## Tools/rationale for helping assessment
- `Parallel trends`: Compare pre-disturbance response variable (e.g. RS indices) for treatment vs. control sites to check if this assumption is reasonable. 
- `Stationarity`: Consider whether your ecological process has stable mean/variance over time.   	  
- `Demographic rates`: Check field literature for existing rates that could be used in a process-based model. 
- Instrument validity: Assess whether your instrument affects outcome only through treatment. 
- `No M–O confounding`:
    1. List all variables that could simultaneously influence your mediator and your outcome.
    2. Check your data to see which of these are actually measured.
    3. If you have measured every plausible mediator-outcome confounder, the assumption is valid; if any remain unmeasured, it is invalid. 
- `Good covariate balance`:
    1. After matching or weighting, calculate standardized mean differences (SMD) for each key covariate.
    2. If all SMDs < 0.1, balance is valid; if any exceed 0.1, it is invalid. 
- `Effect entirely mediated`:
    1. Fit a model that includes both treatment and mediator as predictors of the outcome.
    2. Test whether the direct effect coefficient (treatment → outcome controlling for mediator) is statistically non-significant (e.g., p>0.05).
    3. If non-significant, the entirely mediated assumption is valid; if significant, it is invalid. 
- `Cutoff + PO continuity`:
    1. For your running variable, conduct a density test at the cutoff (e.g., McCrary test) to check for manipulation.
    2. Plot and test whether other covariates are continuous at the cutoff (e.g., no jump in pre-treatment NDVI).
    3. If both tests show no discontinuities, the assumption is valid; otherwise, it is invalid. 
- `B/A treatment observations`:
    1. Count the number of pre-treatment and post-treatment observations per unit (e.g., years or RS scenes).
    2. If both counts meet or exceed your chosen threshold (e.g., ≥ 8 each), the assumption is valid; if not, it is invalid. 
- `Good pretreatment fit`:
    1. For synthetic control or time‐series forecasting, calculate the pre-intervention root mean squared prediction error (RMSPE). 
    2. Define a threshold, if RMSPE is below it, the assumption is valid; if above, it is invalid. 

## Example
- `Parallel trends`: You plot pre-harvest NDVI at logged and unlogged sites and see near-identical slopes → you can afford this assumption. 
- `Instrument validity`: You use distance to logging road as an instrument; based on construction records and no other road impacts, you judge this instrument acceptable. 
- `No M–O confounding`: In an analysis of logging → soil moisture (mediator) → seedling survival, the researcher identifies soil compaction as a potential confounder but has no compaction data. Consequently, they mark the No M–O confounding assumption as invalid for their dataset. 
- `Effect entirely mediated`: In a mediation analysis of logging → canopy loss (mediator) → understory diversity, the direct logging term in the model controlling for canopy loss has p=0.72; thus, the researcher considers the effect entirely mediated valid in their study. 
- `Cutoff + PO continuity`: 
    - *Set-up*: Elevation is the running variable with a cutoff at 1,000 m to assign “protected” vs. “unprotected” status to forest plots and then measuring canopy density as your outcome. 
    - *Check*: You run the McCrary test on the distribution of elevation across all plots. You also plot a histogram of elevation with a vertical line at 1,000 m. 
    - *Interpretation*: If the density is smooth at 1,000 m, i.e. no spike or gap—then you have evidence against manipulation of elevation data and can consider the assumption valid. If you see a spike right above 1,000 m, that suggests some plots might have been mis-reported or specifically placed to gain protection, it is invalid. 
- `B/A treatment obs.`: For an interrupted time‐series of insect outbreaks, the ecologist has 10 years of species counts before and 12 years after the outbreak—both ≥8—so the `Before/After treatment observations` assumption is valid. 
- `Good pretreatment fit`: A researcher builds a synthetic control for mangrove area: the pre-treatment RMSPE is 3 % of mean area—below their 5 % cutoff, so the assumption is valid. 
