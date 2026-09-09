#!/usr/bin/env node
'use strict';
/*
  Ship-blocking translation-coverage gate for the sharded i18n.

  Guarantees, per the plan's four completeness layers:
   1. Extraction completeness  — the corpus is rebuilt from the live data (deny-list
      walk of architectures/*.json + resources/*.json), so a newly added content
      field is in the corpus by default. (Re-run of build_i18n.js --dump.)
   2. Translation completeness — every corpus string is attempted in every shipped
      language (present in .cache or overrides). A never-attempted string is a
      provider FAILURE (e.g. rate-limit), counted as `missing`.
   3. Shard-routing completeness — for every (language, industry) the loaded shards
      (_common + that industry's shard) contain every TRANSLATED string the view can
      render. A translated string that a view needs but is not loaded is a routing
      bug (`routingMiss`) and is ALWAYS ship-blocking.
   4. Emit consistency — every string in a shard file is bucketed to that shard, and
      _common holds only _common-bucketed strings (no cross-contamination).

  Exit codes: non-zero on any routingMiss or emit inconsistency (structural bugs).
  `missing` (untranslated / provider gap) is reported and, with --strict, also
  ship-blocks. --runtime additionally drives a live T()-miss audit in a browser.

  Usage:
    node tools/verify_i18n_coverage.js            # static gate (fast)
    node tools/verify_i18n_coverage.js --strict    # also fail on any missing translation
    node tools/verify_i18n_coverage.js --runtime    # add the live Playwright T()-miss audit
*/
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = path.join(__dirname, '..');
const TR = path.join(ROOT, 'app', 'translations');
const CACHE = path.join(TR, '.cache');
const OVR = path.join(TR, 'overrides');
const STRICT = process.argv.includes('--strict');
const RUNTIME = process.argv.includes('--runtime');

function J(p, fb) { try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch (e) { return fb; } }
function overridesFor(code) {
  return Object.assign({}, J(path.join(OVR, code + '.json'), {}), J(path.join(OVR, 'labels', code + '.json'), {}), J(path.join(OVR, 'full', code + '.json'), {}));
}

// 1. Rebuild the corpus + routing metadata from the live data (fails non-zero if
//    the build-time routing invariant is violated).
console.log('Rebuilding corpus + routing metadata (build_i18n.js --dump)...');
execSync('node ' + JSON.stringify(path.join(__dirname, 'build_i18n.js')) + ' --dump', { cwd: ROOT, stdio: 'inherit' });

const corpus = J(path.join(TR, '_corpus.json'), []);
const bucketOf = J(path.join(TR, '_buckets.json'), {});
const indExtract = J(path.join(TR, '_ind_extract.json'), {});
const baseExtract = J(path.join(TR, '_base.json'), []);
const manifest = J(path.join(TR, 'manifest.json'), { languages: [], source: 'en' });
const corpusSet = new Set(corpus);
const industryIds = Object.keys(indExtract);

if (!corpus.length) { console.error('FAIL: empty corpus'); process.exit(2); }

// Languages to gate: manifest targets that have an emitted translations/<code>/ dir.
const targets = manifest.languages.filter(l => l.code !== manifest.source)
  .filter(l => fs.existsSync(path.join(TR, l.code, '_common.json')));

console.log('\nGating ' + targets.length + ' shipped language(s): ' + targets.map(l => l.code).join(', ') +
  ' | corpus ' + corpus.length + ' | industries ' + industryIds.length + '\n');

const rows = [];
let hardFail = 0, softFail = 0;

for (const lang of targets) {
  const L = lang.code;
  const cache = J(path.join(CACHE, L + '.json'), {});
  const overrides = overridesFor(L);
  const dir = path.join(TR, L);

  // load emitted buckets
  const common = J(path.join(dir, '_common.json'), {});
  const shards = {};
  for (const id of industryIds) shards[id] = J(path.join(dir, id + '.json'), {});
  const commonKeys = new Set(Object.keys(common));
  const fullDict = Object.assign({}, common);
  for (const id of industryIds) Object.assign(fullDict, shards[id]);
  const fullKeys = new Set(Object.keys(fullDict));

  // (2) translation completeness: never-attempted corpus strings = provider gap
  let missing = 0;
  for (const s of corpus) if (!(s in cache) && !(s in overrides)) missing++;
  const covered = fullKeys.size;                 // strings with a real translation
  const identical = corpus.length - covered - missing; // attempted but == source (glossary/identical)

  // (4) emit consistency: a shard file must hold only its own bucket's strings
  let emitBad = 0; const emitSample = [];
  for (const s of commonKeys) if (bucketOf[s] !== '_common') { emitBad++; if (emitSample.length < 5) emitSample.push('_common<-' + s); }
  for (const id of industryIds) for (const s of Object.keys(shards[id])) if (bucketOf[s] !== id) { emitBad++; if (emitSample.length < 5) emitSample.push(id + '<-' + s); }

  // (3) routing: every TRANSLATED string a view needs must be in its loaded shards
  let routingMiss = 0; const routeSample = [];
  // base (reference board + chrome) -> must be in _common
  for (const s of baseExtract) if (fullKeys.has(s) && !commonKeys.has(s)) { routingMiss++; if (routeSample.length < 5) routeSample.push('base:' + s); }
  for (const id of industryIds) {
    const activeHas = s => commonKeys.has(s) || (id in shards && s in shards[id]);
    for (const s of indExtract[id]) if (fullKeys.has(s) && !activeHas(s)) { routingMiss++; if (routeSample.length < 5) routeSample.push(id + ':' + s); }
  }

  const rag = (routingMiss || emitBad) ? 'RED' : (missing ? 'YEL' : 'GRN');
  if (routingMiss || emitBad) hardFail++;
  if (missing) softFail++;
  rows.push({ L, corpus: corpus.length, covered, identical, missing, routingMiss, emitBad, rag });
  if (routeSample.length) console.log('  [' + L + '] routing sample: ' + routeSample.join(' | '));
  if (emitSample.length) console.log('  [' + L + '] emit sample: ' + emitSample.join(' | '));
}

// ---- deck-template completeness (miss class: exported PPTX/PDF blurbs) ----
// The five section blurbs, the count captions, the model-link, close-title and
// cloud-line carry {ind}/{n}/{plat}/{cloud} placeholders, so they live in DECK_TPL
// (index.html), keyed by language, rather than in the value-keyed corpus. dt()
// falls back to English for any missing key, so a shipped language absent from
// DECK_TPL renders those blurbs in English in EVERY export (the automotive-JA deck
// regression). The corpus gate above never sees these strings, so they get their
// own structural, ALWAYS ship-blocking check here.
const { evalObject } = require('./lib_extract');
const DECK = evalObject(fs.readFileSync(path.join(ROOT, 'app', 'index.html'), 'utf8'), 'const DECK_TPL =');
const deckKeys = Object.keys(DECK.en || {});
const phSig = s => (String(s).match(/\{\w+\}/g) || []).sort().join(',');
let deckFail = 0; const deckRows = [];
for (const lang of targets) {
  const L = lang.code;
  const pack = DECK[L];
  let missKeys = 0, emptyKeys = 0, phLost = 0;
  if (!pack) { missKeys = deckKeys.length; }
  else for (const k of deckKeys) {
    if (!(k in pack)) { missKeys++; }
    else if (!String(pack[k]).trim()) { emptyKeys++; }
    else if (phSig(DECK.en[k]) !== phSig(pack[k])) { phLost++; }
  }
  const bad = missKeys + emptyKeys + phLost;
  if (bad) { deckFail++; console.log('  [' + L + '] DECK_TPL missing=' + missKeys + ' empty=' + emptyKeys + ' placeholderLoss=' + phLost); }
  deckRows.push({ L, bad });
}
hardFail += deckFail;

// ---- report ----
console.log('\n' + 'lang  corpus  translated  identical  missing  routingMiss  emitBad  status');
for (const r of rows) {
  console.log(
    r.L.padEnd(5) + ' ' + String(r.corpus).padStart(6) + ' ' + String(r.covered).padStart(11) + ' ' +
    String(r.identical).padStart(10) + ' ' + String(r.missing).padStart(8) + ' ' + String(r.routingMiss).padStart(12) + ' ' +
    String(r.emitBad).padStart(8) + '  ' + r.rag);
}

console.log('\nDECK_TPL export coverage (' + deckKeys.length + ' keys/lang): ' +
  (deckFail ? deckFail + ' language(s) fall back to English in exports  <-- SHIP-BLOCKING' : 'all ' + targets.length + ' shipped langs complete'));
console.log('Structural (routing + emit + deck) failures: ' + hardFail + (hardFail ? '  <-- SHIP-BLOCKING' : '  (none)'));
console.log('Languages with untranslated strings (provider/MT gap): ' + softFail + (STRICT ? '  <-- SHIP-BLOCKING (--strict)' : '  (reported)'));

if (RUNTIME) {
  console.log('\n--runtime: driving the live T()-miss audit...');
  try { execSync('node ' + JSON.stringify(path.join(__dirname, 'audit_i18n_runtime.js')), { cwd: ROOT, stdio: 'inherit' }); }
  catch (e) { console.error('runtime audit FAILED'); hardFail++; }
}

const fail = hardFail + (STRICT ? softFail : 0);
console.log('\n' + (fail ? 'GATE FAILED (' + fail + ')' : 'GATE PASSED') +
  (softFail && !STRICT ? ' — but ' + softFail + ' language(s) have untranslated strings pending MT' : ''));
process.exit(fail ? 1 : 0);
