<!-- Logos (absolute URLs so they render both on GitHub and on the Jekyll site) -->
<div class="logo-row">
  <img src="https://damhq.github.io/navidam/assets/images/logos/Obsgession_text_logo.png" alt="Obsgession" style="width:250px; margin:0 18px; vertical-align:middle;">
  <img src="https://damhq.github.io/navidam/assets/images/logos/logo-FRB-Cesab-anglais_cropped.png" alt="FRB Cesab" style="width:175px; margin:0 18px; vertical-align:middle;">
  <img src="https://damhq.github.io/navidam/assets/images/logos/Logo_cnrs.png" alt="CNRS" style="width:60px; margin:0 18px; vertical-align:middle;">
  <img src="https://damhq.github.io/navidam/assets/images/logos/logo-leca.png" alt="LECA" style="width:150px; margin:0 18px; vertical-align:middle;">
</div>
--------------------------------

# Contributing to NaviDAM

Welcome, and thanks for your interest in NaviDAM!

NaviDAM is a collaborative effort. Method suggestions depend directly on the quality and number of method assessments: the more complete and accurate the assessments, the more useful the guidance.

All contributions are welcome, and your ideas matter more than perfect formatting. No coding skills are required for most contributions — fixing a typo, adding a reference, or sharing domain expertise is already valuable.

Please follow the [Code of Conduct](https://github.com/damhq/navidam/blob/main/CODE_OF_CONDUCT.md) in all interactions. Be kind, use inclusive language, and assume good intent, especially when discussing methods or assessments where opinions may differ.

## At a glance 💡

| Goal | How |
|------|-----|
| New assessment or revision of an existing assessment | 📝 [Method assessment issue](#assess-method) |
| New documentation page or completion of an existing one | 📝 [Method documentation issue](#document-method) |
| Revision of an existing [documentation page](https://damhq.github.io/navidam/methods) | 🔍 [Pull request](#revise-doc) |
| Brand-new method from scratch (assess + document) | ✨ [Both issues, in order](#new-method) |
| Revise or add a [Good practices](https://damhq.github.io/navidam/practices) or [Examples](https://damhq.github.io/navidam/examples) page | 🔍 [Pull request](#practices-examples) |
| Question, site bug, or infrastructure suggestion | 💬 [Blank issue](https://github.com/damhq/navidam/issues/new/choose) |

> Go to **Issues > New issue** and choose the matching template: <https://github.com/damhq/navidam/issues/new/choose>.

- Before opening a new issue, please search [existing issues](https://github.com/damhq/navidam/issues) to avoid duplicates and consider joining an ongoing discussion.

<a id="assess-method"></a>
## 1. Assess a method (new or revision) 📝

Use the **Method assessment** issue template for both cases. Assessments position [methods](https://damhq.github.io/navidam/methods) against the [criteria](https://damhq.github.io/navidam/criteria).

- **New assessment:** choose `Is the method already included in NaviDAM? > No`, give the method name, and fill in the criteria.
- **Revision / second opinion:** choose `Is the method already included in NaviDAM? > Yes`, give the exact existing method name, and fill in the full form with **your own** values. Your assessment is recorded next to the existing one(s), and the method page shows whether assessors agree (see [how the status is computed](#assessment-status)). Only criteria whose published value would change are proposed as changes for maintainer review.
- **Author:** give your name, or tick `Anonymous contribution` (or leave the name empty) to appear as *Anonymous* on the website.
- **Confidence:** rate how confident you are from 1 to 5. It weights your assessment when several assessors disagree, so please be honest rather than generous.

💡 **Tips for a good assessment:**
- Base family-level assessments on the most common or original variant, and add options matching major, widespread variants.
- Use the [criteria pages](https://damhq.github.io/navidam/criteria) to check definitions before answering.
- Add rationale or comments at the end of the form to justify choices — this greatly helps review.

What happens next: a pull request is opened automatically. New rows are added directly; revisions are listed as old → new suggestions to accept or reject. A maintainer reviews and may ask for clarification in the issue thread. Nothing is published before the pull request is merged. If you edit your issue, your assessment is updated rather than counted twice. Likewise, only **one assessment per method and author name** is kept: submitting again under the same name (case-insensitive) replaces your previous assessment of that method. The author field is required: tick *Anonymous contribution* to keep your name off the website (it then appears as *Anonymous*). Only a short non-reversible key of the name is stored, so an anonymous re-submission under the same name still replaces your earlier assessment. The GitHub issue itself is public and keeps what you typed, so use a consistent pseudonym if you want to stay unidentifiable.

<details markdown="1">
<summary><strong>How assessments are combined: Consensus / Debated status</strong></summary>
<a id="assessment-status"></a>

Several people can assess the same method. Each method page then shows a status badge next to the assessor line, a ⚠️ next to debated criteria in the assessment table, and a collapsible breakdown listing every assessor's answer per criterion.

#### Status badge

| Badge | Meaning |
|-------|---------|
| **Single assessment** · confidence *n*/5 | Only one assessment exists. The badge shows the confidence score given by the assessor (1 = least, 5 = most confident). |
| **Consensus** (*k* assessors) | At least **80% of the compared criteria** reach an agreement of at least 80% between assessors (20 of 25 when all criteria are compared). |
| **Debated** (*k* assessors) | Fewer than 80% of the compared criteria reach that agreement: assessors give contrasting assessments. |

Two assessors are enough to get a Consensus or Debated status. There is no intermediate status. Methods assessed before this system existed also show the **Single assessment** badge, using the confidence score of their initial assessment (2/5 for AI-assisted assessments, 3/5 for assessments made by contributors).

#### How agreement is computed

1. **One vote per assessor.** Every submitted assessment issue is one vote, anonymous ones included. Votes are stored in `_data/assessment_votes/`.
2. **Confidence affects the weight, but its influence is softened.** A vote's weight is `√(confidence ÷ 5)`: a 5/5 score has weight 1, while a 1/5 score has weight about 0.45 (rather than 0.2). This lets higher confidence count more without letting it dominate as strongly.
3. **Similarity of two answers on a criterion** is a number between 0 and 1. The raw score is **squared**, so partial matches count less while exact matches (1) and complete disagreements (0) stay unchanged:
   - *Ordinal criteria* (e.g. IID, Handles lag effects, Minimal TS length) use a **distance-based score**: `(1 − distance ÷ (number of levels − 1))²`. Neighbouring options such as `Required` vs `Recommended` score 0.25 (not 0.5); the extremes `Required` vs `Relaxes assumption` score 0. `Inapplicable` only matches itself. Older assessments that ticked several options on an ordinal criterion count as the most permissive one.
   - *Multiple-choice criteria* (e.g. Objective, Language) use the **squared overlap** of the selected options: `(shared options ÷ all selected options)²`. For *Exposure type*, **All** is read as the union of Binary, Categorical, Continuous / Time-varying, Compositional and Multivariate.
   - *Model-specific assumptions*: ticking nothing is a valid answer ("no specific assumption"). It is compared as the answer **None**: two assessors ticking nothing agree fully, while *None* versus any ticked assumption has no overlap (0%). If *None* is retained, the published cell is left empty.
4. **Agreement of a criterion.** Each given answer is tested as the "reference": every assessor supports it in proportion to the similarity of their own answer to it (fully if identical, partly if close, not at all if opposite), multiplied by their weight. The reference with the highest support, divided by the total weight of all assessors, gives the agreement. When answers are identical or totally different, this is simply the weighted share of assessors giving the most common answer, so *"at least 80% of the assessors agree"* is read literally. A criterion is **agreed** when this is **≥ 80%**, and **debated** otherwise. Only criteria answered by at least two assessors are compared.
5. **Method status** is the share of compared criteria that are agreed: **≥ 80% → Consensus**, **< 80% → Debated**. Each criterion still needs at least **80% agreement** to count as agreed. There are 25 criteria in total, so if all are compared, at least **20 must be agreed** for Consensus.

*Examples.* Three assessors answer IID with `Required` (confidence 5), `Required` (4) and `Relaxes assumption` (2): their weights are 1, about 0.89 and 0.63, so agreement is (1 + 0.89) ÷ (1 + 0.89 + 0.63) ≈ 75% → debated. Two equally weighted assessors answering `Required` and `Relaxes assumption` reach 50%, while `Required` and `Recommended` reach 62.5% after squaring partial similarity → both debated. For *Handles lag effects*, `No` (confidence 3) and `Possible` (5) produce about 67% agreement after softening confidence and squaring partial similarity, so the criterion is debated.

#### Published assessment

The values displayed in the assessment table are, for each criterion, the **softened-confidence-weighted majority** across assessors (on an exact tie, e.g. two equally confident but diverging assessors, the currently published value is kept), and the displayed confidence score is the average of the assessors' scores. In practice, when two assessors diverge, the answer of the **more confident** one is retained; with **equal confidence** the answer already published stays (the new assessment is still recorded and the status becomes Debated), and if neither is the published one the earliest assessment wins. For criteria where several options can be ticked, one of the actual answers is retained, never a merge of both.

The method page header lists **all assessors** (legacy ones included), and the *Assessment agreement* panel shows each assessor's answer per criterion. Contributing a revision therefore never removes an earlier assessor. A submission that changes the published values is turned into a pull request listing every old → new value, which a maintainer reviews before anything changes on the website. A submission that only adds an agreeing or disagreeing opinion is still recorded (it updates the status) through a pull request.

#### Anonymity

Anonymous assessors appear as *Anonymous* on the website, and no issue numbers are shown. The issue and pull request themselves are still created from your GitHub account and are visible to anyone on GitHub.

</details>

<a id="document-method"></a>
## 2. Document a method (new or completion) 📝

Use the **Method documentation** issue template for both cases. Documentation fills the [methods](https://damhq.github.io/navidam/methods) pages (description, references, implementation).

- **New page:** choose `Is the method already included in NaviDAM? > No`. A page is created from the submission.
- **Completion:** choose `Yes`, give the exact page title, and fill in only the sections to add. Placeholders are replaced on first contribution; later contributions are appended.
- **Author:** the name is optional. If you leave it empty, the contribution is considered anonymous and credited as *Anonymous*.

💡 **Tips for good documentation:**
- Follow the standard page structure: *Description & principle*, *Major variants*, *Reference articles* (method + research applications), *Implementation* (Python / R), and the *Assessment table*.
- Prefer one clear, well-commented implementation example per language over an exhaustive list of variants.
- Cite key references (method paper + ecological applications where possible) and link useful tutorials or blogs.
- Keep language clear and accessible: readers range from beginners to experts.

### What methods need help? 🌱

Good first contributions include completing thin pages, adding references, or documenting a method you know well. If unsure where to start, browse the [methods panel](https://damhq.github.io/navidam/methods) for pages with placeholders and follow sections 1–2 above.

> 📊 The live [Website coverage](https://damhq.github.io/navidam/contributing/#website-coverage) section on the website shows automatically updated coverage numbers and the lists of methods needing assessment review, documentation, or review.

<a id="revise-doc"></a>
## 3. Revise an existing documentation page 🔍

Revisions of existing [documentation pages](https://damhq.github.io/navidam/methods) are made via pull requests, not issues. Even small fixes (typos, broken links, clearer wording) are welcome — there is no minimum size for a useful contribution. ✨

From the website:

1. Scroll to the bottom and click **Edit this page on GitHub**.
2. Click the pencil icon ✏️ to edit the `.md` file.
3. Propose changes on a new `doc/<short-topic>` branch (e.g. `doc/synthetic-controls-refs`), then open a pull request against `main` with a clear title (e.g. `docs: clarify assumptions on Synthetic controls`).

💡 **Pull request best practices:**
- Keep changes focused: one topic per pull request is much easier to review.
- Write a clear title and describe what you changed and why.
- If the work is still in progress, open a draft pull request to get early feedback.
- Be responsive to reviewer comments — discussion is part of the process.

For assessment corrections, use the **Method assessment** issue template instead (see section [1.](#assess-method)).

<a id="new-method"></a>
## 4. Add a brand-new method from scratch ✨

Fully positioning a new method requires two steps, in order:

1. **Assess it** with the **Method assessment** issue template.
2. **Document it** with the **Method documentation** issue template.

Assessment first ensures the method becomes filterable; documentation then provides description, references, and implementation details.

<a id="practices-examples"></a>
## 5. Good practices and Examples pages 🔍

Revisions of [Good practices](https://damhq.github.io/navidam/practices) and [Examples](https://damhq.github.io/navidam/examples) pages follow the same process as [method documentation pages](#revise-doc):

1. Scroll to the bottom of the page and click **Edit this page on GitHub**.
2. Click the pencil icon ✏️ to edit the `.md` file.
3. Propose changes on a new `doc/<short-topic>` branch, then open a pull request against `main`.

New pages are added the same way: create a `.md` file under `contents/practices/` or `contents/examples/` on a `doc/<short-topic>` branch and open a pull request against `main`.

💡 For new pages, look at an existing page in the same panel as a template (front-matter + section structure), keep filenames in lower-case with hyphens, and link to related [criteria](https://damhq.github.io/navidam/criteria) or [methods](https://damhq.github.io/navidam/methods) where relevant.

## Roles and promotions

NaviDAM is community-built, and regular contributors are invited to take on more responsibility. Roles are granted **by invitation**, never automatically, so that scientific quality and repository security stay under control.

| Role | GitHub permission | Typical responsibilities | Usual path to it |
| --- | --- | --- | --- |
| **Contributor** | None needed | Submit assessments, documentation, and pull requests | Anyone |
| **Reviewer** | Write | Revise, accept or reject the PRs generated from assessment and documentation issues; label and close issues | About 5 accepted contributions, including reviews of others' work, over at least 1 month |
| **Maintainer** | Admin | Settings, rulesets, releases, security, access and governance | Invited by existing maintainers after sustained, high-quality review activity |

**What counts as an accepted contribution:** an assessment, documentation page or revision that was merged, or a substantial review of someone else's contribution. Counts are a guideline. Quality, reliability and communication matter more than quantity.

**Principles**
- Promotions are proposed by any reviewer or maintainer, or self-nominated through a blank issue, and are agreed by the maintainers. The invitation is announced in the project's issues or pull requests.
- Reviewers don't merge their own pull requests. Changes to `.github/`, `scripts/` and `_config.yml` are reviewed by a maintainer (see [`CODEOWNERS`](https://github.com/damhq/navidam/blob/main/.github/CODEOWNERS)).
- Releases (version tags and GitHub releases, which also mint Zenodo DOIs) are made by maintainers only.
- Roles can be paused or stepped down after about 12 months of inactivity, or on request. Past contributions stay credited.
- Everyone, whatever the role, follows the [Code of Conduct](https://github.com/damhq/navidam/blob/main/CODE_OF_CONDUCT.md).

## Recognition 🙌

Contributors are credited as page authors on the pages they create or substantially complete, and every issue and pull request is part of the public record. If you contributed and are not credited, please let us know in the relevant thread.

## Licensing 📄

By contributing, you agree that your contributions will be shared under the repository's licenses: code under GPLv3+, documentation and scientific text under CC BY 4.0. See [`LICENSE`](https://github.com/damhq/navidam/blob/main/LICENSE) for details.

## Questions? 💬

- Open a [blank issue](https://github.com/damhq/navidam/issues/new/choose) for questions, bug reports, or suggestions about the site itself.
- For direct contact, see the [About page](https://damhq.github.io/navidam/about).

Thanks for improving NaviDAM! 🎉