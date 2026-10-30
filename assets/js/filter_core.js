// DOM-free filtering logic shared by filter.js and the JS/Python consistency test.
// Must stay in sync with scripts/validation/navidam_suggester.py.
import { criteria, compositeOptions, impliedOptions, ordinalCriteriaOrder } from './criteria.js';

export const NO_SPECIFIC_CRITERION = "Model specific";
export const NO_SPECIFIC_VALUE = "No specific assumption";

export function expandImplied(key, vals) {
  const implied = impliedOptions[key];
  if (!implied) return vals;
  const out = new Set(vals);
  vals.forEach(v => (implied[v] || []).forEach(c => out.add(c)));
  return [...out];
}

// Criteria in the order they are displayed to users (category order, "Assumptions" last).
export function displayOrderedCriteria() {
  const categoryOrder = [];
  criteria.forEach(c => {
    if (!categoryOrder.includes(c.category)) categoryOrder.push(c.category);
  });
  const idx = categoryOrder.indexOf("Assumptions");
  if (idx !== -1) {
    categoryOrder.splice(idx, 1);
    categoryOrder.push("Assumptions");
  }
  return categoryOrder.flatMap(category => criteria.filter(c => c.category === category));
}

// A selection with nothing meaningful (Any / Unsure / "No specific assumption") does not restrict.
export function isActiveSelection(key, selectedVals) {
  if (!selectedVals || selectedVals.length === 0) return false;
  return !(key === NO_SPECIFIC_CRITERION && selectedVals.includes(NO_SPECIFIC_VALUE));
}

// Keep the methods satisfying a single criterion; selectedVals excludes "" and "__unsure__".
export function filterByCriterion(methods, key, selectedVals) {
  if (!isActiveSelection(key, selectedVals)) return methods;

  // 1. Composite option logic (union of constituents for all selected composite opts)
  if (compositeOptions[key]) {
    const compositeForThis = compositeOptions[key];
    if (selectedVals.some(sv => compositeForThis[sv])) {
      const included = new Set();
      selectedVals.forEach(sv => {
        if (compositeForThis[sv]) {
          compositeForThis[sv].forEach(x => included.add(x));
        } else {
          included.add(sv);
        }
      });
      return methods.filter(m => {
        if (!m[key]) return false;
        const methodVals = expandImplied(key, m[key].split(",").map(x => x.trim()));
        return methodVals.some(opt => included.has(opt) || opt === "Don't know" || opt === "Inapplicable");
      });
    }
  }

  // 2. Ordinal logic: accept if method satisfies ANY selected threshold
  if (ordinalCriteriaOrder[key]) {
    const order = ordinalCriteriaOrder[key];
    return methods.filter(m => {
      if (!m[key]) return false;
      const methodVals = m[key].split(",").map(x => x.trim());
      return methodVals.some(opt => {
        if (opt === "Don't know" || opt === "Inapplicable") return true;
        return selectedVals.some(sv => order.indexOf(opt) >= order.indexOf(sv));
      });
    });
  }

  // 3. Default logic: accept methods that have ANY selected value
  const implied = impliedOptions[key] || {};
  return methods.filter(m => {
    if (!m[key]) return false;
    const methodVals = expandImplied(key, m[key].split(",").map(x => x.trim()));
    return methodVals.some(opt => opt === "Don't know" || opt === "Inapplicable")
      || selectedVals.some(sv => implied[sv]
        ? implied[sv].every(c => methodVals.includes(c))
        : methodVals.includes(sv));
  });
}

// selections: { criterionKey: [selected values] }; usedKeys: criteria applicable to the objective.
export function strictMethods(methods, selections, usedKeys, skipKey = null) {
  let filtered = methods;
  criteria.forEach(criterion => {
    if (criterion.key === skipKey || !usedKeys.includes(criterion.key)) return;
    filtered = filterByCriterion(filtered, criterion.key, selections[criterion.key] || []);
  });
  return filtered;
}

// Methods passing the objective and every selected criterion but exactly one.
// Returns [{ method, failedKey }] sorted by display order of the failed criterion, then table order.
export function nearMisses(methods, selections, usedKeys) {
  const named = m => m["Method"] && m["Method"].trim();
  const strictNames = new Set(strictMethods(methods, selections, usedKeys).filter(named).map(m => m["Method"].trim()));
  const found = new Map();
  displayOrderedCriteria().forEach(criterion => {
    const key = criterion.key;
    if (key === "Objective" || !usedKeys.includes(key) || !isActiveSelection(key, selections[key])) return;
    strictMethods(methods, selections, usedKeys, key).filter(named).forEach(m => {
      const name = m["Method"].trim();
      if (strictNames.has(name) || found.has(name)) return;
      found.set(name, { method: m, failedKey: key });
    });
  });
  return [...found.values()];
}
