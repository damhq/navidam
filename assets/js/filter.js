import { criteria, criteriaOptionLabelMap, compositeOptions, impliedOptions, ordinalCriteriaOrder, hideCompositeConstituents, multipleAllowedCriteria } from './criteria.js';
import { NO_SPECIFIC_CRITERION, strictMethods, nearMisses } from './filter_core.js';

console.log("Filter.js loaded!");

const siteBaseurl = JSON.parse(document.getElementById('site-baseurl').textContent);
const objectiveCriteriaMap = JSON.parse(document.getElementById('objective-criteria-map').textContent);
const choicesInstances = {};
let currentFilteredMethods = [];
let currentNearMisses = [];


function updateCriteriaStatus() {
  let anyCount = 0;
  let unsureCount = 0;
  let assessedCount = 0;

  // Determine which criteria are currently used
  const objectiveSelect = document.getElementById("filter-Objective");
  let usedCriteriaKeys;
  if (objectiveSelect && objectiveSelect.value && objectiveCriteriaMap[objectiveSelect.value]) {
    usedCriteriaKeys = objectiveCriteriaMap[objectiveSelect.value].concat(["Objective"]);
  } else {
    // If no objective selected, use all criteria
    usedCriteriaKeys = criteria.map(c => c.key);
  }

  criteria.forEach(criterion => {
    if (!usedCriteriaKeys.includes(criterion.key)) return; // skip unused criteria
    const select = document.getElementById("filter-" + criterion.key);
    if (!select) return;
    if (select.value === "") {
      anyCount++;
    } else if (select.value === "__unsure__") {
      unsureCount++;
    } else {
      assessedCount++;
    }
  });

  const statusDiv = document.getElementById("criteria-status");
  if (statusDiv) {
    statusDiv.classList.remove("green", "intermediary");
    statusDiv.innerHTML =
      `<span style="margin-right:1em;">Any: <strong>${anyCount}</strong></span>` +
      `<span style="margin-right:1em;">Unsure: <strong>${unsureCount}</strong></span>` +
      `<span>Assessed: <strong>${assessedCount}</strong></span>`;
    if (anyCount === 0 && unsureCount === 0) {
      statusDiv.classList.add("green");
    } else if (anyCount === 0 && unsureCount > 0) {
      statusDiv.classList.add("intermediary");
    }
  }
}


function getUsedCriteriaKeys() {
  const objectiveSelect = document.getElementById("filter-Objective");
  if (objectiveSelect && objectiveSelect.value && objectiveCriteriaMap[objectiveSelect.value]) {
    return objectiveCriteriaMap[objectiveSelect.value].concat(["Objective"]);
  } else {
    return criteria.map(c => c.key);
  }
}



document.addEventListener('DOMContentLoaded', function() {

  // Only run if method-data and criteria-filters exist
  if (!document.getElementById('method-data') || !document.getElementById('criteria-filters')) {
    console.log("Required elements not found, script not running.");
    return;
  }
  console.log("Script started");

  // 1. Load method data
  const methodData = JSON.parse(document.getElementById('method-data').textContent);

  const NO_SPECIFIC_VALUE = "No specific assumption";

  // 2. Define the criteria you want dropdowns for (column names from your TSV)
  //  Replaced by an import
  

  // 3. Get unique options for each criterion
  const optionsByCriterion = {};
  criteria.forEach(criterion => {
    const opts = new Set();
    methodData.forEach(m => {
      if (m[criterion.key]) {
        m[criterion.key].split(",").forEach(val => {
          const trimmed = val.trim();
          if (trimmed !== "Don't know" && trimmed !== "Inapplicable") {
            opts.add(trimmed);
          }
        });
      }
    });

    // Add composite options if defined
    if (compositeOptions[criterion.key]) {
      Object.keys(compositeOptions[criterion.key]).forEach(opt => opts.add(opt));
    }

    let optsArr = Array.from(opts);

    // Remove "Any" and "Unsure" for custom sorting
    const anyIdx = optsArr.indexOf("");
    const unsureIdx = optsArr.indexOf("__unsure__");
    let anyOpt = null, unsureOpt = null;
    if (anyIdx !== -1) anyOpt = optsArr.splice(anyIdx, 1)[0];
    if (unsureIdx !== -1) unsureOpt = optsArr.splice(optsArr.indexOf("__unsure__"), 1)[0];

    // Remove individual options that are included in a composite ONLY if flagged in hideCompositeConstituents
    if (compositeOptions[criterion.key] && hideCompositeConstituents[criterion.key]) {
      const compositeIncluded = new Set();
      Object.entries(compositeOptions[criterion.key]).forEach(([compOpt, arr]) => {
        if (hideCompositeConstituents[criterion.key][compOpt]) {
          arr.forEach(opt => compositeIncluded.add(opt));
        }
      });
      optsArr = optsArr.filter(opt => !compositeIncluded.has(opt));
    }

    // Needs-side only: no assumption restriction (methods with empty cells included)
    if (criterion.key === NO_SPECIFIC_CRITERION) {
      optsArr = optsArr.filter(opt => opt !== NO_SPECIFIC_VALUE);
    }

    // Custom sort for ordinal criteria
    if (ordinalCriteriaOrder[criterion.key]) {
      const order = ordinalCriteriaOrder[criterion.key];
      optsArr.sort((a, b) => order.indexOf(a) - order.indexOf(b));
    } else {
      optsArr.sort(); // default alphabetical for non-ordinal
    }

    if (criterion.key === NO_SPECIFIC_CRITERION) optsArr.unshift(NO_SPECIFIC_VALUE);

    // Re-add "Any" at the start and "Unsure" at the end
    if (anyOpt !== null) optsArr.unshift(anyOpt);
    if (unsureOpt !== null) optsArr.push(unsureOpt);

    optionsByCriterion[criterion.key] = optsArr;
  });


  // Mapping of category names to permalinks
  const categoryLinks = {
    "Outcome": `${siteBaseurl}/outcome`,
    "Data compatibility": `${siteBaseurl}/data`,
    "Assumptions": `${siteBaseurl}/assumptions`,
    "Model properties": `${siteBaseurl}/properties`,
    "Implementation": `${siteBaseurl}/implementation`
  };
  // 4. Render dropdowns
  const filtersDiv = document.getElementById("criteria-filters");
  console.log("filtersDiv:", filtersDiv);
  

  let lastCategory = null;
  let categoryContainers = {}; // Store containers for each category

  // Build category order array in the order they appear in criteria
  const categoryOrder = [];
  criteria.forEach(c => {
      if (!categoryOrder.includes(c.category)) categoryOrder.push(c.category);
  });

  // Move "Assumptions" to the end of categoryOrder
  const idx = categoryOrder.indexOf("Assumptions");
  if (idx !== -1) {
    categoryOrder.splice(idx, 1); // Remove "Assumptions"
    categoryOrder.push("Assumptions"); // Add it at the end
  }

  categoryOrder.forEach(category => {
    criteria.filter(c => c.category === category).forEach(criterion => {
      // Insert category heading and collapsible container if this is a new category
      if (criterion.category !== lastCategory && criterion.category !== "__standalone__") {
        const catHeading = document.createElement("div");
        catHeading.style.marginTop = "1.5em";
        catHeading.style.marginLeft = "0em";
        catHeading.style.fontSize = "1.3em";
        catHeading.style.cursor = "pointer";
        catHeading.style.display = "flex";
        catHeading.style.alignItems = "center";

        // Category name (as span, not link)
        const catName = document.createElement("span");
        catName.textContent = criterion.category;
        catName.style.fontWeight = "bold";

        // Add expand/collapse indicator
        const arrow = document.createElement("span");
        arrow.textContent = " ▶";
        arrow.style.marginLeft = "0.5em";
        arrow.style.marginRight = "0.5em";

        // Create the help link (?)
        const catHelp = document.createElement("a");
        catHelp.href = categoryLinks[criterion.category] || "#";
        catHelp.target = "_blank";
        catHelp.rel = "noopener noreferrer";
        catHelp.title = `More info about ${criterion.category}`;
        catHelp.style.marginLeft = "0.5em";
        catHelp.style.fontSize = "0.75em";
        catHelp.innerHTML = "(?)";

        // Collapsible container for this category's criteria
        const catContainer = document.createElement("div");
        catContainer.style.display = "none";
        catContainer.dataset.category = criterion.category;
        categoryContainers[criterion.category] = catContainer;

        // Toggle on heading click (but not when clicking the help link)
        catHeading.addEventListener("click", function(e) {
          if (e.target === catHelp) return; // Don't toggle if help clicked
          const isOpen = catContainer.style.display === "block";
          catContainer.style.display = isOpen ? "none" : "block";
          arrow.textContent = isOpen ? " ▶" : " ▼";
        });

        catHeading.appendChild(catName);
        catHeading.appendChild(arrow);
        catHeading.appendChild(catHelp);
        filtersDiv.appendChild(catHeading);
        filtersDiv.appendChild(catContainer);
        lastCategory = criterion.category;
      }

      const label = document.createElement("label");
      label.style.display = "inline-block";
      label.style.whiteSpace = "nowrap";
      if (criterion.key === "Objective") {
        label.classList.add("objective-highlight");
      }
      label.appendChild(document.createTextNode(criterion.label + ": "));

      // Create a container for (?) and select, and indent it
      const rightContainer = document.createElement("span");
      rightContainer.className = "criteria-select-container";

      const criterionSlug = slugify(criterion.key);
      const helpLink = document.createElement("a");
      const criteriaMapping = JSON.parse(document.getElementById('criteria-mapping').textContent);

      // When creating the help link for a criterion:
      const helpHref = criteriaMapping[criterion.key]
        ? siteBaseurl + criteriaMapping[criterion.key]
        : `${siteBaseurl}/contents/criteria/${criterionSlug}`;
      helpLink.href = helpHref;
      helpLink.target = "_blank";
      helpLink.rel = "noopener noreferrer";
      helpLink.title = `More info about ${criterion.label}`;
      helpLink.style.position = "absolute";
      helpLink.style.left = "220px"; // Adjust this value to align all (?) marks vertically
      helpLink.style.marginLeft = "0"; // Remove any previous margin-left
      helpLink.style.marginRight = "6px";
      helpLink.style.fontSize = "0.75em";
      // helpLink.style.color = "#a89cc8";
      helpLink.innerHTML = "(?)";

      label.style.position = "relative";
      label.style.minWidth = "220px";

      const select = document.createElement("select");
      select.id = "filter-" + criterion.key;


      // Allow multiple selection if in multipleAllowedCriteria
      if (multipleAllowedCriteria.includes(criterion.key)) {
        select.multiple = true;
        select.size = Math.min(optionsByCriterion[criterion.key].length, 6); // or any preferred size
        select.value = ""; // Select "Any" by default
      }


      if (criterion.key === "Objective") {
        select.classList.add("objective-highlight");
      }
      let optionsHtml = `<option value="" style="font-style:italic;">Any</option>` +
      optionsByCriterion[criterion.key].map(opt => {
        const displayLabel = criteriaOptionLabelMap[criterion.key] && criteriaOptionLabelMap[criterion.key][opt]
          ? criteriaOptionLabelMap[criterion.key][opt]
          : opt;
        return `<option value="${opt}">${displayLabel}</option>`;
      }).join("");
      if (criterion.key !== "Objective") {
        optionsHtml += `<option value="__unsure__" style="font-style:italic;">Unsure</option>`;
      }
      select.innerHTML = optionsHtml;

      // When a selection is made, expand the next category
      select.addEventListener("change", function() {
      // Find all VISIBLE criteria in this category
      const currentCategory = criterion.category;
      // Only consider divs that are visible and in this category
      if (!categoryContainers[currentCategory]) return;
      const visibleCriteriaInCategory = Array.from(categoryContainers[currentCategory].children)
        .filter(child => child.dataset.criterionKey && child.style.display !== "none");
      // Check if this is the last visible criterion in the category
      if (
        visibleCriteriaInCategory.length > 0 &&
    visibleCriteriaInCategory[visibleCriteriaInCategory.length - 1] === rowDiv
      ) {
        // Find the next category in order
        const idx = categoryOrder.indexOf(currentCategory);
        if (idx !== -1 && idx < categoryOrder.length - 1) {
          for (let nextIdx = idx + 1; nextIdx < categoryOrder.length; nextIdx++) {
            const nextCat = categoryOrder[nextIdx];
            if (nextCat === "__standalone__") continue;
            const nextContainer = categoryContainers[nextCat];
            const nextHeading = Array.from(filtersDiv.children).find(
              el => el.querySelector && el.querySelector("span") && el.querySelector("span").textContent === nextCat
            );
            const hasVisibleCriteria = nextContainer && Array.from(nextContainer.children)
              .some(child => child.dataset.criterionKey && child.style.display !== "none");
            if (nextContainer && nextHeading && nextHeading.style.display !== "none" && hasVisibleCriteria) {
              nextContainer.style.display = "block";
              const arrow = nextHeading.querySelector("span:nth-child(2)");
              if (arrow) arrow.textContent = " ▼";
              break;
            }
          }
        }
      }
    });

      label.appendChild(helpLink);
      rightContainer.appendChild(select);

      // Choices.js initialization for multi-select
      if (multipleAllowedCriteria.includes(criterion.key)) {
        const choicesInstance = new Choices(select, {
          removeItemButton: true,
          shouldSort: false,
          position: 'bottom',
          placeholder: true,
          placeholderValue: 'Select options',
          searchEnabled: false
        });
        choicesInstances[criterion.key] = choicesInstance;
        // Ensure "Any" is visually selected on load
        choicesInstance.setChoiceByValue('');

        let prevSelectedValues = Array.from(select.selectedOptions).map(opt => opt.value);
        select.addEventListener('change', function(e) {
          const anyOption = select.querySelector('option[value=""]');
          const selectedValues = Array.from(select.selectedOptions).map(opt => opt.value);

          // Only remove "Any" if it was previously selected and now another option is selected
          if (
            anyOption &&
            prevSelectedValues.includes("") && // "Any" was previously selected
            selectedValues.includes("") &&
            selectedValues.length > 1
          ) {
            setTimeout(() => {
              anyOption.selected = false;
              choicesInstances[criterion.key].removeActiveItemsByValue('');
              // Reselect all other selected values to ensure Choices.js UI is correct
              selectedValues.filter(v => v !== "").forEach(val => {
                choicesInstances[criterion.key].setChoiceByValue(val);
              });
            }, 0);
          }

          // If nothing is selected, select "Any" by default
          if (selectedValues.length === 0 && anyOption) {
            setTimeout(() => {
              anyOption.selected = true;
              choicesInstances[criterion.key].setChoiceByValue('');
            }, 0);
          }

          // Update prevSelectedValues for next change
          prevSelectedValues = selectedValues;
        });
    }

      // Create a container for tags (right-aligned)
    const tagContainer = document.createElement("span");
    tagContainer.className = "criteria-tag-container";

    // Ordinal tag
    if (ordinalCriteriaOrder[criterion.key]) {
      const ordinalTag = document.createElement("span");
      ordinalTag.className = "ordinal-tag";
      ordinalTag.title = "Ordinal: options are ordered from most to least permissive. Selecting an option also includes the options below it.";
      ordinalTag.textContent = "Ordinal";
      tagContainer.appendChild(ordinalTag);
    }

    // Multiple allowed tag
    if (multipleAllowedCriteria.includes(criterion.key)) {
      const multiTag = document.createElement("span");
      multiTag.className = "multiple-tag";
      multiTag.title = "Multiple: select all options that apply. A method qualifies when it matches any selected option.";
      multiTag.textContent = "Multiple";
      tagContainer.appendChild(multiTag);
    }

    const rowDiv = document.createElement("div");
    rowDiv.className = "criteria-row";
    rowDiv.appendChild(label);
    rowDiv.appendChild(rightContainer);
    rowDiv.appendChild(tagContainer);
    rowDiv.dataset.criterionKey = criterion.key;

      if (criterion.category === "__standalone__") {
        filtersDiv.appendChild(rowDiv);
      } else {
        categoryContainers[criterion.category].appendChild(rowDiv);
      }
    });

    if (category !== "__standalone__") {
      const rationaleToggle = document.createElement("button");
      rationaleToggle.type = "button";
      rationaleToggle.className = "criteria-rationale-toggle";
      rationaleToggle.textContent = `Describe the rationale behind the ${category} choices`;
      rationaleToggle.setAttribute("aria-expanded", "false");

      const rationaleRow = document.createElement("div");
      rationaleRow.className = "criteria-rationale-row";
      rationaleRow.style.display = "none";

      const rationale = document.createElement("textarea");
      rationale.id = `rationale-${slugify(category)}`;
      rationale.className = "criteria-rationale";
      rationale.rows = 3;
      rationale.placeholder = "Explain the reasoning behind your choices in this category (optional)";
      rationale.setAttribute("aria-label", `Describe the rationale behind the ${category} choices`);

      rationaleRow.appendChild(rationale);
      rationaleToggle.addEventListener("click", function() {
        const isOpen = rationaleRow.style.display !== "none";
        rationaleRow.style.display = isOpen ? "none" : "";
        rationaleToggle.setAttribute("aria-expanded", String(!isOpen));
      });
      categoryContainers[category].appendChild(rationaleToggle);
      categoryContainers[category].appendChild(rationaleRow);
    }
  });

  // After the rendering loop, add this Objective change handler:
  const objectiveSelect = document.getElementById("filter-Objective");
  objectiveSelect.addEventListener("change", function() {
  const selectedObjective = objectiveSelect.value;
  if (!selectedObjective) {
    // Find the currently open category (if any)
    let openCat = null;
    categoryOrder.forEach(cat => {
      if (cat === "__standalone__") return;
      const container = categoryContainers[cat];
      const heading = Array.from(filtersDiv.children).find(
        el => el.querySelector && el.querySelector("span") && el.querySelector("span").textContent === cat
      );
      if (container && heading && heading.style.display !== "none" && container.style.display === "block") {
        openCat = cat;
      }
    });

    // Show all criteria and all category headings, collapse all containers
    document.querySelectorAll('[data-criterion-key]').forEach(div => {
      div.style.display = "";
    });
    categoryOrder.forEach(cat => {
      if (cat === "__standalone__") return;
      const container = categoryContainers[cat];
      const heading = Array.from(filtersDiv.children).find(
        el => el.querySelector && el.querySelector("span") && el.querySelector("span").textContent === cat
      );
      if (container) container.style.display = "none";
      if (heading) heading.style.display = "";
      // Set arrow to collapsed
      if (heading) {
        const arrow = heading.querySelector("span:nth-child(2)");
        if (arrow) arrow.textContent = " ▶";
      }
      const rationaleToggle = container && container.querySelector(".criteria-rationale-toggle");
      if (rationaleToggle) rationaleToggle.style.display = "block";
    });

    // Restore previously open category, if any
    if (openCat) {
      const container = categoryContainers[openCat];
      const heading = Array.from(filtersDiv.children).find(
        el => el.querySelector && el.querySelector("span") && el.querySelector("span").textContent === openCat
      );
      if (container && heading) {
        container.style.display = "block";
        const arrow = heading.querySelector("span:nth-child(2)");
        if (arrow) arrow.textContent = " ▼";
      }
    }
    return;
  }

  // Show only criteria relevant to the selected objective
  const relevant = objectiveCriteriaMap[selectedObjective] || [];
  document.querySelectorAll('[data-criterion-key]').forEach(div => {
    if (relevant.includes(div.dataset.criterionKey) || div.dataset.criterionKey === "Objective") {
      div.style.display = "";
    } else {
      div.style.display = "none";
    }
  });
  
  // After updating criterion visibility:
  categoryOrder.forEach(cat => {
    if (cat === "__standalone__") return;
    const container = categoryContainers[cat];
    const heading = Array.from(filtersDiv.children).find(
      el => el.querySelector && el.querySelector("span") && el.querySelector("span").textContent === cat
    );
    // Check if any visible criterion in this category
    const hasVisible = Array.from(container.children).some(child => child.dataset.criterionKey && child.style.display !== "none");
    const rationaleToggle = container.querySelector(".criteria-rationale-toggle");
    if (rationaleToggle) rationaleToggle.style.display = hasVisible ? "block" : "none";
    const rationaleRow = container.querySelector(".criteria-rationale-row");
    if (!hasVisible && rationaleRow) {
      rationaleRow.style.display = "none";
      rationaleToggle?.setAttribute("aria-expanded", "false");
    }
    if (!hasVisible) {
      container.style.display = "none";
      if (heading) heading.style.display = "none";
    } else {
      if (heading) heading.style.display = "";
    }
  });
  // Find and expand the first non-empty category
  for (const cat of categoryOrder) {
    if (cat === "__standalone__") continue;
    const container = categoryContainers[cat];
    const heading = Array.from(filtersDiv.children).find(
      el => el.querySelector && el.querySelector("span") && el.querySelector("span").textContent === cat
    );
    if (container && heading && heading.style.display !== "none") {
      container.style.display = "block";
      // Update arrow
      const arrow = heading.querySelector("span:nth-child(2)");
      if (arrow) arrow.textContent = " ▼";
      break;
    }
  }

  // Finally, re-filter methods based on new visibility
  filterMethods();
  updateCriteriaStatus();

  });



  // 5. Filter and display methods
  function getSelections() {
    const selections = {};
    criteria.forEach(criterion => {
      const selectEl = document.getElementById("filter-" + criterion.key);
      if (!selectEl) return;
      // collect selected values (exclude Any "" and __unsure__)
      if (selectEl.multiple) {
        selections[criterion.key] = Array.from(selectEl.selectedOptions)
          .map(o => o.value)
          .filter(v => v !== "" && v !== "__unsure__");
      } else {
        const v = selectEl.value;
        selections[criterion.key] = v && v !== "__unsure__" ? [v] : [];
      }
    });
    return selections;
  }

  function filterMethods() {
    const filtered = strictMethods(methodData, getSelections(), getUsedCriteriaKeys());
    currentFilteredMethods = filtered;
    displayMethods(filtered);
    renderNearMisses(filtered);
  }

  function optionLabel(key, value) {
    return criteriaOptionLabelMap[key]?.[value] || value;
  }

  // Near misses: methods failing exactly one selected criterion (strict results are untouched).
  function nearMissFailure(entry, selections) {
    const criterion = criteria.find(c => c.key === entry.failedKey);
    const methodVals = (entry.method[entry.failedKey] || "").split(",").map(x => x.trim()).filter(Boolean);
    return {
      key: entry.failedKey,
      label: criterion.label,
      method: methodVals.map(v => optionLabel(entry.failedKey, v)).join(", "),
      asked: selections[entry.failedKey].map(v => optionLabel(entry.failedKey, v)).join(", ")
    };
  }

  function renderNearMisses(strict) {
    const strictDiv = document.getElementById("filtered-methods");
    if (!strictDiv) return;
    let details = document.getElementById("near-misses");
    const strictEmpty = strict.filter(m => m["Method"] && m["Method"].trim()).length === 0;
    const selections = getSelections();
    currentNearMisses = nearMisses(methodData, selections, getUsedCriteriaKeys())
      .map(entry => ({ method: entry.method, failure: nearMissFailure(entry, selections) }));

    if (currentNearMisses.length === 0 && !strictEmpty) {
      if (details) details.remove();
      return;
    }
    if (!details) {
      details = document.createElement("details");
      details.id = "near-misses";
      details.className = "near-misses";
      strictDiv.insertAdjacentElement("afterend", details);
    }
    // Expanded by default only when there is no strict result; collapse again once there is one
    if (strictEmpty) {
      details.open = true;
      details.dataset.autoOpened = "1";
    } else if (details.dataset.autoOpened) {
      details.open = false;
      delete details.dataset.autoOpened;
    }

    const summary = document.createElement("summary");
    summary.append(`Near misses (${currentNearMisses.length})`);
    const help = document.createElement("a");
    help.href = `${siteBaseurl}/about#near-misses`;
    help.target = "_blank";
    help.rel = "noopener noreferrer";
    help.title = "Near misses are methods failing exactly one of your criteria. They are not matches: check the failed criterion before using one. Click for details.";
    help.style.marginLeft = "0.5em";
    help.style.fontWeight = "normal";
    help.textContent = "(?)";
    // Following the link must not toggle the details element
    help.addEventListener("click", e => e.stopPropagation());
    summary.appendChild(help);
    const note = document.createElement("p");
    note.className = "near-misses-note";
    note.textContent = strictEmpty
      ? (currentNearMisses.length
        ? "No method matches all criteria. These methods match all but one."
        : "No method matches all criteria, and none matches all but one. Try relaxing some criteria.")
      : "These methods do not match your criteria: each fails exactly one criterion and matches all the others.";
    const list = document.createElement("ul");
    list.className = "near-misses-list";
    currentNearMisses.forEach(({ method, failure }) => {
      const li = document.createElement("li");
      const link = document.createElement("a");
      link.href = nearMissUrl(method);
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = method["Method"];
      const tag = document.createElement("span");
      tag.className = ordinalCriteriaOrder[failure.key] ? "ordinal-tag" : "multiple-tag";
      tag.classList.add("near-miss-tag");
      tag.textContent = `Fails: ${failure.label} (method: ${failure.method}, you asked: ${failure.asked})`;
      li.append(link, tag);
      list.appendChild(li);
    });
    details.replaceChildren(summary, note, list);
  }

  function nearMissUrl(m) {
    const catDicts = JSON.parse(document.getElementById('cat-dicts').textContent);
    const category = m["Category"] ? m["Category"].split(",")[0].trim() : "";
    const subcat = m["Sub-category"] ? m["Sub-category"].split(",")[0].trim() : "";
    const subcatLabel = Object.keys(catDicts.SUBCAT_FOLDER_MAP).find(k => catDicts.SUBCAT_FOLDER_MAP[k] === slugify(subcat)) || subcat;
    const categoryLabel = (subcatLabel && catDicts.SUBCAT_PARENT[subcatLabel])
      || Object.keys(catDicts.CATEGORY_FOLDER_MAP).find(k => catDicts.CATEGORY_FOLDER_MAP[k] === slugify(category))
      || category;
    const categoryFolder = catDicts.CATEGORY_FOLDER_MAP[categoryLabel] || slugify(categoryLabel);
    const methodSlug = slugify(m["Method"]);
    if (!subcatLabel) return `${siteBaseurl}/contents/methods/${categoryFolder}/${methodSlug}/`;
    const subcatFolder = catDicts.SUBCAT_FOLDER_MAP[subcatLabel] || slugify(subcatLabel);
    return m["Method"] === subcatLabel
      ? `${siteBaseurl}/contents/methods/${categoryFolder}/${subcatFolder}/`
      : `${siteBaseurl}/contents/methods/${categoryFolder}/${subcatFolder}/${methodSlug}/`;
  }


  
  function displayMethods(methods) {
      const div = document.getElementById("filtered-methods");
      if (!div) {
          console.log("filtered-methods div not found!");
          return;
      }

      // Load category/subcat mappings
      const catDicts = JSON.parse(document.getElementById('cat-dicts').textContent);
      const CATEGORY_FOLDER_MAP = catDicts.CATEGORY_FOLDER_MAP;
      const SUBCAT_FOLDER_MAP = catDicts.SUBCAT_FOLDER_MAP;
      const SUBCAT_PARENT = catDicts.SUBCAT_PARENT;

      // Filter out methods with missing "Method" (e.g. trailing placeholder rows in the TSV)
      const validMethods = methods.filter(m => m["Method"] && m["Method"].trim());
      const validTotal = methodData.filter(m => m["Method"] && m["Method"].trim());
      currentFilteredMethods = validMethods;
      if (validMethods.length === 0) {
          div.innerHTML = "<div class=\"no-methods-message\">No methods match your criteria.</div>";
          return;
      }
      if (validMethods.length === validTotal.length) {
          div.innerHTML = `<div class="any-method-message">Any <a href="${siteBaseurl}/methods" target="_blank" rel="noopener noreferrer">method</a>!</div>`;
          return;
      }

      // Group methods by category and subcategory
      const grouped = {};
      validMethods.forEach(m => {
          // Get label for category and subcategory
          let category = m["Category"] ? m["Category"].split(",")[0].trim() : "";
          let subcat = m["Sub-category"] ? m["Sub-category"].split(",")[0].trim() : "";

          // Map folder to label
          let categoryLabel = Object.keys(CATEGORY_FOLDER_MAP).find(
              k => CATEGORY_FOLDER_MAP[k] === slugify(category)
          ) || category;

          let subcatLabel = Object.keys(SUBCAT_FOLDER_MAP).find(
              k => SUBCAT_FOLDER_MAP[k] === slugify(subcat)
          ) || subcat;

          // If subcat exists, get its parent category label
          if (subcatLabel && SUBCAT_PARENT[subcatLabel]) {
              categoryLabel = SUBCAT_PARENT[subcatLabel];
          }

          if (!grouped[categoryLabel]) grouped[categoryLabel] = {};
          if (subcatLabel) {
              if (!grouped[categoryLabel][subcatLabel]) grouped[categoryLabel][subcatLabel] = [];
              grouped[categoryLabel][subcatLabel].push(m);
          } else {
              if (!grouped[categoryLabel]["__no_subcat__"]) grouped[categoryLabel]["__no_subcat__"] = [];
              grouped[categoryLabel]["__no_subcat__"].push(m);
          }
      });

      // Build HTML
      let html = "<div class='method-categories'>";
      Object.keys(grouped).forEach(cat => {
          html += `<div class="method-category-block"><h3>${cat}</h3>`;
          // 1. Display methods with no subcategory first
          if (grouped[cat]["__no_subcat__"]) {
              html += "<ul>";
              grouped[cat]["__no_subcat__"].forEach(m => {
                  const methodName = m["Method"];
                  const methodSlug = slugify(methodName);
                  const categoryFolder = CATEGORY_FOLDER_MAP[cat] || slugify(cat);
                  
                  // No subcategory for these methods
                  const url = `${siteBaseurl}/contents/methods/${categoryFolder}/${methodSlug}/`;

                  html += `<li><a href="${url}" target="_blank" rel="noopener noreferrer">${methodName}</a></li>`;
              });
              html += "</ul>";
          }
          
          // 2. Then display all subcategories
          Object.keys(grouped[cat]).forEach(subcat => {
              if (subcat === "__no_subcat__") return;
              html += `<h4 style="margin-left:1em">${subcat}</h4>`;
              html += "<ul>";
              grouped[cat][subcat].forEach(m => {
                  const methodName = m["Method"];
                  const methodSlug = slugify(methodName);
                  const categoryFolder = CATEGORY_FOLDER_MAP[cat] || slugify(cat);
                  const subcatFolder = SUBCAT_FOLDER_MAP[subcat] || slugify(subcat);

                  let url;
                  if (methodName === subcat) {
                      // Link to the subcategory folder (index.md)
                      url = `${siteBaseurl}/contents/methods/${categoryFolder}/${subcatFolder}/`;
                  } else if (subcat !== "__no_subcat__") {
                      url = `${siteBaseurl}/contents/methods/${categoryFolder}/${subcatFolder}/${methodSlug}/`;
                  } else {
                      url = `${siteBaseurl}/contents/methods/${categoryFolder}/${methodSlug}/`;
                  }

                  html += `<li><a href="${url}" target="_blank" rel="noopener noreferrer">${methodName}</a></li>`;
                });
            html += "</ul>";
        });
        html += "</div>";
    });
    html += "</div>";
    div.innerHTML = html;
  }

  function csvCell(value) {
    return `"${String(value ?? "").replace(/"/g, '""')}"`;
  }

  function selectedCriterionValues(criterion) {
    const select = document.getElementById("filter-" + criterion.key);
    if (!select) return [];
    return Array.from(select.selectedOptions || [select.selectedOptions?.[0]])
      .filter(option => option && option.value !== "")
      .map(option => {
        if (option.value === "__unsure__") return "Unsure";
        return criteriaOptionLabelMap[criterion.key]?.[option.value] || option.textContent;
      });
  }

  function exportAssessment() {
    const titleInput = document.getElementById("evaluation-title");
    const title = titleInput ? titleInput.value.trim() : "";
    const safeTitle = title.replace(/[\\/:*?"<>|]+/g, "-").replace(/\s+/g, " ").replace(/[. ]+$/, "");
    const rows = [
      [title.toUpperCase()],
      [],
      ["", "CONSULT THE GOOD PRACTICES PANEL AND ESPECIALLY THE BEYOND METHOD SELECTION PAGE FOR GUIDANCE ON HOW TO DESIGN A ROBUST STUDY AND REACH CREDIBLE RESULTS."],
      [],
      ["Section", "Category", "Item", "Selection or rationale"]
    ];
    const usedCriteriaKeys = getUsedCriteriaKeys();

    criteria.forEach(criterion => {
      if (!usedCriteriaKeys.includes(criterion.key)) return;
      rows.push(["Criteria", criterion.category === "__standalone__" ? "" : criterion.category, criterion.label, selectedCriterionValues(criterion).join("; ")]);
    });
    rows.push([]);

    categoryOrder.forEach(category => {
      if (category === "__standalone__") return;
      const rationale = document.getElementById(`rationale-${slugify(category)}`);
      rows.push(["Rationale", category, "", rationale ? rationale.value : ""]);
    });
    rows.push([]);

    currentFilteredMethods.filter(method => method["Method"]).forEach(method => {
      const category = method["Category"] ? method["Category"].split(",")[0].trim() : "";
      rows.push(["Suggested method", category, method["Method"], ""]);
    });

    // Near misses do NOT match all criteria: kept apart and labelled as such
    if (currentNearMisses.length) {
      rows.push([]);
      rows.push(["Near miss (NOT a match)", "", "", "Methods below fail exactly one selected criterion; they are not part of the suggested methods above."]);
      currentNearMisses.forEach(({ method, failure }) => {
        const category = method["Category"] ? method["Category"].split(",")[0].trim() : "";
        rows.push(["Near miss (NOT a match)", category, method["Method"], `Fails: ${failure.label} (method: ${failure.method}, you asked: ${failure.asked})`]);
      });
    }

    const csv = rows.map(row => row.map(csvCell).join(",")).join("\r\n");
    const blob = new Blob(["\uFEFF", csv], { type: "text/csv;charset=utf-8" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = safeTitle ? `${safeTitle}_NavidamResults.csv` : "NavidamResults.csv";
    link.click();
    URL.revokeObjectURL(link.href);
    const status = document.getElementById("export-evaluation-status");
    if (status) status.textContent = "Evaluation exported.";
  }

  const exportBtn = document.getElementById("export-evaluation-btn");
  if (exportBtn) exportBtn.addEventListener("click", exportAssessment);

  // 7. Attach event listeners
  criteria.forEach(criterion => {
  document.getElementById("filter-" + criterion.key).addEventListener("change", function() {
      filterMethods();
      updateCriteriaStatus();
    });
  });

  // 8. Initial display
  displayMethods(methodData);
  renderNearMisses(methodData);
  console.log("Initial methods displayed");
  updateCriteriaStatus();
  // });

  // Add this at the end, after your other event listeners:
    const resetBtn = document.getElementById("reset-filters-btn");
    if (resetBtn) {
      resetBtn.addEventListener("click", function(e) {
        e.preventDefault();
        criteria.forEach(criterion => {
          const select = document.getElementById("filter-" + criterion.key);
          if (!select) return;
          if (multipleAllowedCriteria.includes(criterion.key) && choicesInstances[criterion.key]) {
            choicesInstances[criterion.key].removeActiveItems();
            choicesInstances[criterion.key].setChoiceByValue('');
          } else {
            select.value = "";
          }
        });
        document.querySelectorAll(".criteria-rationale").forEach(rationale => {
          rationale.value = "";
        });
        filterMethods();
        updateCriteriaStatus();

        // Collapse all criteria categories
        categoryOrder.forEach(cat => {
          if (cat === "__standalone__") return;
          const container = categoryContainers[cat];
          const heading = Array.from(filtersDiv.children).find(
            el => el.querySelector && el.querySelector("span") && el.querySelector("span").textContent === cat
          );
          if (container) container.style.display = "none";
          if (heading) heading.style.display = "";
          // Set arrow to collapsed
          if (heading) {
            const arrow = heading.querySelector("span:nth-child(2)");
            if (arrow) arrow.textContent = " ▶";
          }
        });

      });
    }

});




// Helper for slugifying (if needed)
function slugify(text) {
  if (!text) return '';
  return text
    .toString()
    .trim()
    .toLowerCase()
    .replace(/\//g, "-")         // replace "/" with "-"
    .replace(/&/g, "and")        // replace "&" with "and"
    .replace(/[^\w\- ]/g, "")    // remove all non-word, non-hyphen, non-space chars
    .replace(/\s+/g, "-");       // replace spaces with "-"
}