// Reads {rows, objectiveMap, studies} as JSON on stdin and prints the strict results and near
// misses computed with the website filtering code (assets/js/filter_core.js).
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const core = await import(pathToFileURL(path.join(root, 'assets/js/filter_core.js')).href);
const { rows, objectiveMap, studies } = JSON.parse(readFileSync(0, 'utf-8'));

const out = studies.map(study => {
  const objective = study.Objective;
  const usedKeys = objectiveMap[objective] ? objectiveMap[objective].concat(['Objective']) : null;
  const selections = {};
  Object.entries(study).forEach(([k, v]) => { selections[k] = Array.isArray(v) ? v : [v]; });
  const used = usedKeys || Object.keys(selections);
  const names = ms => [...new Set(ms.map(m => m.Method.trim()).filter(Boolean))];
  return {
    strict: names(core.strictMethods(rows, selections, used)),
    near: core.nearMisses(rows, selections, used).map(n => [n.method.Method.trim(), n.failedKey]),
  };
});
console.log(JSON.stringify(out));
