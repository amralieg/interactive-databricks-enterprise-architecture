#!/usr/bin/env node
'use strict';
/*
  Externalise the data that bloats app/index.html into JSON modules the runtime
  fetches on demand, then strip those literals from the HTML so the reference
  board ships without them.

  Emits (all under app/, the served root):
    architectures/<id>.json   one per industry (all 63), loaded lazily on pick
    architectures/manifest.json  [{id,label,built}] for the picker
    resources/links.json         LINKS (incl. inline videos/seealso)
    resources/references.json    REFERENCES
    resources/accelerators.json  ACCEL_BY_NAME
    resources/connectors.json    CONNECTORS

  Then rewrites app/index.html, replacing each externalised literal body with an
  empty {} / [] that the runtime populates in place at boot (resources) or on
  demand (industries). INDUSTRY_CATALOG and ARCH/BASE stay inline: the picker and
  the reference board must render with zero fetches.

  Round-trip safe: it reads the ACTUAL literal in the HTML (not the batch source),
  so the JSON is byte-for-byte what shipped, and it re-parses every file and
  deep-compares before declaring success. Idempotent: re-running on an
  already-split HTML is a no-op for the (already empty) literals.

  Usage:
    node tools/split_modules.js            # emit + strip + verify
    node tools/split_modules.js --check    # verify only, do not write the HTML
*/
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const X = require('./lib_extract');

const ROOT = path.join(__dirname, '..');
const APP = path.join(ROOT, 'app', 'index.html');
const ARCH_DIR = path.join(ROOT, 'app', 'architectures');
const RES_DIR = path.join(ROOT, 'app', 'resources');
const CHECK_ONLY = process.argv.includes('--check');

function writeJson(p, obj) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, JSON.stringify(obj));
}
// CONNECTORS carry a RegExp `re` (c.re.test(name) at runtime), which JSON cannot
// hold. Store it as reSrc/reFlags strings; the runtime rebuilds `re = new
// RegExp(reSrc, reFlags)` at boot. Every other field passes through untouched.
function serializeConnectors(conn) {
  const out = {};
  for (const k in conn) {
    const c = conn[k], o = {};
    for (const f in c) { if (f !== 're') o[f] = c[f]; }
    o.reSrc = c.re.source; o.reFlags = c.re.flags;
    out[k] = o;
  }
  return out;
}
function rehydrateConnectors(json) {
  const out = {};
  for (const k in json) {
    const c = json[k], o = {};
    for (const f in c) { if (f !== 'reSrc' && f !== 'reFlags') o[f] = c[f]; }
    o.re = new RegExp(c.reSrc, c.reFlags);
    out[k] = o;
  }
  return out;
}
function deepEqual(a, b, label) {
  assert.deepStrictEqual(a, b, 'round-trip mismatch: ' + label);
}

function main() {
  const html = fs.readFileSync(APP, 'utf8');

  // ---- evaluate every literal we externalise, plus the catalog (kept inline) ----
  const INDUSTRIES = X.evalObject(html, 'const INDUSTRIES = {');
  const CATALOG = X.evalArray(html, 'const INDUSTRY_CATALOG = [');
  const LINKS = X.evalObject(html, 'const LINKS = {');
  const REFERENCES = X.evalArray(html, 'const REFERENCES = [');
  const ACCEL = X.evalObject(html, 'const ACCEL_BY_NAME = {');
  const CONNECTORS = X.evalObject(html, 'const CONNECTORS = {');

  const industryIds = Object.keys(INDUSTRIES);
  console.log('Industries: ' + industryIds.length +
    ' | LINKS ' + Object.keys(LINKS).length +
    ' | REFERENCES ' + REFERENCES.length +
    ' | ACCEL ' + Object.keys(ACCEL).length +
    ' | CONNECTORS ' + Object.keys(CONNECTORS).length);

  // ---- emit architecture modules + manifest ----
  fs.rmSync(ARCH_DIR, { recursive: true, force: true });
  for (const id of industryIds) writeJson(path.join(ARCH_DIR, id + '.json'), INDUSTRIES[id]);
  const manifest = CATALOG.map(pair => ({
    id: pair[0], label: pair[1], built: Object.prototype.hasOwnProperty.call(INDUSTRIES, pair[0]),
  }));
  writeJson(path.join(ARCH_DIR, 'manifest.json'), manifest);

  // Every catalog id that claims to be built must have a file, and every emitted
  // file must be in the catalog: the picker and the module set can never diverge.
  const builtIds = new Set(manifest.filter(m => m.built).map(m => m.id));
  for (const id of builtIds) assert(industryIds.includes(id), 'catalog built id has no module: ' + id);
  for (const id of industryIds) assert(builtIds.has(id), 'module has no catalog entry: ' + id);

  // ---- emit resource modules ----
  writeJson(path.join(RES_DIR, 'links.json'), LINKS);
  writeJson(path.join(RES_DIR, 'references.json'), REFERENCES);
  writeJson(path.join(RES_DIR, 'accelerators.json'), ACCEL);
  writeJson(path.join(RES_DIR, 'connectors.json'), serializeConnectors(CONNECTORS));

  // ---- round-trip: re-parse every file and deep-compare to the source literal ----
  for (const id of industryIds) {
    deepEqual(JSON.parse(fs.readFileSync(path.join(ARCH_DIR, id + '.json'), 'utf8')), INDUSTRIES[id], 'architectures/' + id);
  }
  deepEqual(JSON.parse(fs.readFileSync(path.join(RES_DIR, 'links.json'), 'utf8')), LINKS, 'links');
  deepEqual(JSON.parse(fs.readFileSync(path.join(RES_DIR, 'references.json'), 'utf8')), REFERENCES, 'references');
  deepEqual(JSON.parse(fs.readFileSync(path.join(RES_DIR, 'accelerators.json'), 'utf8')), ACCEL, 'accelerators');
  deepEqual(rehydrateConnectors(JSON.parse(fs.readFileSync(path.join(RES_DIR, 'connectors.json'), 'utf8'))), CONNECTORS, 'connectors');
  console.log('Round-trip OK: ' + industryIds.length + ' industries + 4 resource maps re-parsed and matched.');

  if (CHECK_ONLY) { console.log('--check: HTML not modified.'); return; }

  // ---- strip the externalised literals from the HTML (empty body in place) ----
  // Object property assignment / array push repopulate these `const` bindings at
  // runtime, so the declarations keep `const` and only the body is emptied.
  const strips = [
    { marker: 'const INDUSTRIES = {', kind: 'obj' },
    { marker: 'const LINKS = {', kind: 'obj' },
    { marker: 'const ACCEL_BY_NAME = {', kind: 'obj' },
    { marker: 'const CONNECTORS = {', kind: 'obj' },
    { marker: 'const REFERENCES = [', kind: 'arr' },
  ].map(s => {
    const b = s.kind === 'obj' ? X.extractObjectText(html, s.marker) : X.extractArrayText(html, s.marker);
    return { start: b.start, end: b.end, repl: s.kind === 'obj' ? '{}' : '[]' };
  }).sort((a, b) => b.start - a.start); // apply back-to-front so offsets hold

  let out = html;
  for (const s of strips) out = out.slice(0, s.start) + s.repl + out.slice(s.end);

  const before = Buffer.byteLength(html), after = Buffer.byteLength(out);
  fs.writeFileSync(APP, out);
  console.log('index.html: ' + before.toLocaleString() + ' -> ' + after.toLocaleString() +
    ' bytes (-' + (100 * (before - after) / before).toFixed(1) + '%)');
}

main();
