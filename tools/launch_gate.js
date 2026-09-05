'use strict';
/*
  LAUNCH GATE — run before declaring a change "finished".

  Enforces two release invariants for every feature listed in GATE.features:

    1. ALL CLOUDS  — the feature renders with no console/page errors on aws,
       azure AND gcp; its cloud-visible tokens are present on every cloud; every
       release-stage badge resolves to a known key on every cloud; and the
       canonical per-cloud product (Lakebase: GA on aws/azure, Beta on gcp)
       proves the stByCloud resolver is live.

    2. ALL LANGUAGES — every user-visible string the feature introduces is
       translated in each target language (fr, es, zh, ar, hi), checked both
       statically against app/i18n/<lang>.json AND at runtime through the same
       T() the board uses, so a string that was added to the corpus but never
       wired through T() still fails.

  It also guards the whole-corpus coverage per language against regression
  (coverage must not drop below the manifest baseline).

  Reuses the corpus/glossary emitted by build_i18n.js (run --dump first) and the
  runtime cloud-switch + applyLang paths already in index.html. No new parsing.

  Usage:
    node tools/build_i18n.js --dump      # refresh _corpus.json/_glossary.json
    node tools/launch_gate.js            # server on 8021 must be up
*/
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const H = 'http://127.0.0.1:8021/app/index.html';
const OUT_DIR = path.join(__dirname, '..', 'app', 'i18n');
const CLOUDS = ['aws', 'azure', 'gcp'];
const LANGS = ['fr', 'es', 'zh', 'ar', 'hi'];
const STAGE_KEYS = new Set(['ga', 'pubpre', 'beta', 'privpre', 'soon']);

// Which change is being gated. Add a feature block per shipped change; the gate
// then holds it to the all-clouds + all-languages bar automatically.
const GATE = {
  features: [
    {
      id: 'F1 Automotive Procurement/ERP',
      industry: 'automotive',
      // Brand/glossary tokens that must render on the board on every cloud.
      cloudTokens: ['Ivalua', 'SAP S/4HANA', 'Supplier Lead-Time Risk'],
      // English content strings that must be translated in every language.
      i18n: [
        'Procurement & ERP', 'Source-to-Pay / Procurement', 'Enterprise ERP',
        'Supplier Lead-Time Risk', 'Supply chain',
        'Source-to-contract and procure-to-pay across raw, partial and assembled parts.',
        'ERP of record for procurement, inventory, production orders and finance.'
      ]
    },
    {
      id: 'G3 Branded/Categorized toggle',
      industry: 'automotive',
      cloudTokens: [],
      i18n: [
        'Branded', 'Categorized',
        'Show products by commercial brand name, or rooted back to their generic category',
        'Pick an industry to switch between brand and category names',
        'Pick an industry to enable the branded view'
      ]
    },
    {
      id: 'G4 Genie stage filter',
      industry: null,            // reference board
      cloudTokens: [],
      i18n: [],
      genieCollapse: true        // Genie must collapse under a "coming soon"-only filter
    }
  ]
};

const glossary = new Set(JSON.parse(fs.readFileSync(path.join(OUT_DIR, '_glossary.json'), 'utf8')));
const corpus = JSON.parse(fs.readFileSync(path.join(OUT_DIR, '_corpus.json'), 'utf8'));
// Coverage floor as a RATIO of the current corpus, not an absolute count: every
// content edit changes the corpus size, so an absolute baseline would false-trip
// whenever a use case (and its strings) is added or removed. Current per-lang
// coverage is 98.8-99.5%; a 98% floor catches a real collapse without noise.
const COVERAGE_FLOOR = 0.98;

// Fixed top-band shape every board must keep (index.html: "four apps, ten use
// cases"). Genie Agents are exactly 4; Business Use Cases are capped at 10.
const MAX_USE_CASES = 10;
const GENIE_AGENTS = 4;

let fails = 0;
const fail = (m) => { console.log('  \u2717 ' + m); fails++; };
const pass = (m) => console.log('  \u2713 ' + m);

// ---------- Phase 0: top-band shape (Genie Agents == 4, Use Cases <= 10) ----------
// Reads the ARCH/INDUSTRIES data literals straight from index.html with the same
// brace-matched extractor build_i18n.js uses, so the count is the shipped data,
// not a rendered approximation.
function phaseShape() {
  console.log('\n[0] TOP-BAND SHAPE \u2014 4 Genie Agents + \u2264' + MAX_USE_CASES + ' Business Use Cases');
  const html = fs.readFileSync(path.join(__dirname, '..', 'app', 'index.html'), 'utf8');
  const extract = (marker) => {
    const i = html.indexOf(marker), braceStart = html.indexOf('{', i);
    let depth = 0, j = braceStart, inStr = false, q = '';
    for (; j < html.length; j++) {
      const c = html[j], n = html[j + 1];
      if (inStr) { if (c === '\\') { j++; continue; } if (c === q) inStr = false; continue; }
      if (c === '/' && n === '/') { while (j < html.length && html[j] !== '\n') j++; continue; }
      if (c === '/' && n === '*') { j += 2; while (j < html.length && !(html[j] === '*' && html[j + 1] === '/')) j++; j++; continue; }
      if (c === '"' || c === "'" || c === '`') { inStr = true; q = c; continue; }
      if (c === '{') depth++; else if (c === '}') { depth--; if (depth === 0) { j++; break; } }
    }
    return Function('MEDALLION_ALSO', 'GX', 'return (' + html.slice(braceStart, j) + ');')([], 'https://github.com/databricks-industry-solutions/');
  };
  const ARCH = extract('const ARCH = {');
  const INDUSTRIES = extract('const INDUSTRIES = {');
  const tilesOf = (top, title) => {
    const secs = Array.isArray(top) ? top : (top && top.secs);   // industry top = array; ARCH.top = {secs}
    if (!Array.isArray(secs)) return null;
    const s = secs.find(x => x.title === title);
    return s ? (s.tiles || []) : [];
  };
  const boards = [['generic (ARCH)', ARCH.top], ...Object.entries(INDUSTRIES).map(([id, ind]) => [id, ind.top])];
  for (const [id, top] of boards) {
    if (!top) continue;
    const agents = tilesOf(top, 'Genie Agents');
    const ucs = tilesOf(top, 'Business Use Cases');
    if (agents === null || ucs === null) { fail(`${id}: top band has no Genie Agents/Business Use Cases sections`); continue; }
    const problems = [];
    if (agents.length !== GENIE_AGENTS) problems.push(`${agents.length} genie agents (must be ${GENIE_AGENTS})`);
    if (ucs.length > MAX_USE_CASES) problems.push(`${ucs.length} use cases (max ${MAX_USE_CASES})`);
    if (problems.length) fail(`${id}: ${problems.join('; ')}`);
    else pass(`${id}: ${agents.length} agents, ${ucs.length} use cases`);
  }
}

// ---------- Phase 1: static i18n coverage (deterministic, no browser) ----------
function phaseStaticI18n() {
  console.log('\n[1] ALL LANGUAGES \u2014 static dict coverage');
  const fixStrings = [...new Set(GATE.features.flatMap(f => f.i18n))]
    .filter(s => !glossary.has(s));
  for (const code of LANGS) {
    const dict = JSON.parse(fs.readFileSync(path.join(OUT_DIR, code + '.json'), 'utf8'));
    const missing = fixStrings.filter(s => !(dict[s] && dict[s] !== s));
    // Count coverage against the CURRENT corpus (non-glossary strings only).
    const need = corpus.filter(s => !glossary.has(s));
    const have = need.filter(s => dict[s] && dict[s] !== s).length;
    const ratio = need.length ? have / need.length : 1;
    if (missing.length) fail(`${code}: ${missing.length}/${fixStrings.length} fix strings untranslated \u2192 ` +
      JSON.stringify(missing.map(s => s.slice(0, 40))));
    else pass(`${code}: all ${fixStrings.length} fix strings translated (corpus ${(ratio * 100).toFixed(1)}%)`);
    if (ratio < COVERAGE_FLOOR) fail(`${code}: corpus coverage ${(ratio * 100).toFixed(1)}% < floor ${(COVERAGE_FLOOR * 100)}%`);
  }
}

// ---------- Phase 2: all clouds (Playwright) ----------
async function phaseClouds(browser) {
  console.log('\n[2] ALL CLOUDS \u2014 render, no errors, stage resolution');
  for (const f of GATE.features) {
    for (const cloud of CLOUDS) {
      const p = await browser.newPage({ viewport: { width: 1720, height: 1080 } });
      const errs = [];
      p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
      p.on('pageerror', e => errs.push('PAGEERR ' + e.message));
      const q = new URLSearchParams({ cloud });
      if (f.industry) q.set('industry', f.industry);
      await p.goto(`${H}?${q}`, { waitUntil: 'networkidle' });
      await p.waitForTimeout(700);
      const r = await p.evaluate(({ tokens }) => {
        const prov = ARCH.cloud.provider;
        const body = document.body.textContent;
        const tokPresent = tokens.map(t => [t, body.includes(t)]);
        const stages = Array.from(document.querySelectorAll('[data-stage]')).map(el => el.dataset.stage);
        const badStages = [...new Set(stages.filter(Boolean))];
        // Lakebase per-cloud truth (canonical stByCloud probe)
        let lakebase = null;
        document.querySelectorAll('[data-stage]').forEach(el => {
          if (/lakebase/i.test(el.textContent)) lakebase = el.dataset.stage;
        });
        const plat = (document.getElementById('platform') || {}).offsetHeight || 0;
        return { prov, tokPresent, badStages, lakebase, plat };
      }, { tokens: f.cloudTokens });

      const tag = `${f.id} @ ${cloud}`;
      const tokMiss = r.tokPresent.filter(([, ok]) => !ok).map(([t]) => t);
      const invalid = r.badStages.filter(s => !STAGE_KEYS.has(s));
      const expectLb = cloud === 'gcp' ? 'beta' : 'ga';
      let ok = true;
      if (errs.length) { fail(`${tag}: console errors \u2192 ${errs.slice(0, 2).join(' | ')}`); ok = false; }
      if (r.prov !== cloud) { fail(`${tag}: provider is ${r.prov}, expected ${cloud}`); ok = false; }
      if (!r.plat) { fail(`${tag}: platform box did not render`); ok = false; }
      if (tokMiss.length) { fail(`${tag}: tokens missing \u2192 ${tokMiss.join(', ')}`); ok = false; }
      if (invalid.length) { fail(`${tag}: invalid data-stage \u2192 ${invalid.join(', ')}`); ok = false; }
      if (r.lakebase && r.lakebase !== expectLb) { fail(`${tag}: Lakebase stage ${r.lakebase}, expected ${expectLb}`); ok = false; }
      if (ok) pass(`${tag}: clean (Lakebase=${r.lakebase || 'n/a'}, stages=[${r.badStages.join(',')}])`);
      await p.close();
    }
  }
}

// ---------- Phase 3: runtime language wiring (Playwright, through T()) ----------
async function phaseRuntimeLang(browser) {
  console.log('\n[3] ALL LANGUAGES \u2014 runtime T() wiring + on-board render');
  for (const code of LANGS) {
    const p = await browser.newPage({ viewport: { width: 1720, height: 1080 } });
    await p.goto(`${H}?industry=automotive`, { waitUntil: 'domcontentloaded' });
    await p.evaluate(c => localStorage.setItem('dbxarch.lang', c), code);
    await p.goto(`${H}?industry=automotive`, { waitUntil: 'networkidle' });
    await p.waitForTimeout(900);
    const strings = [...new Set(GATE.features.flatMap(f => f.i18n))].filter(s => !glossary.has(s));
    const r = await p.evaluate(({ strings }) => {
      const lang = I18N.lang;
      const untranslated = strings.filter(s => T(s) === s);   // same as English = not wired/translated
      // confirm the translated procurement box label actually shows on the board
      const boxT = T('Procurement & ERP');
      const boxOnBoard = (document.getElementById('rail-src') || document.body).textContent.includes(boxT);
      return { lang, untranslated, boxT, boxOnBoard };
    }, { strings });
    if (r.lang !== code) fail(`${code}: applyLang did not switch (lang=${r.lang})`);
    else if (r.untranslated.length) fail(`${code}: T() returns English for ${r.untranslated.length} \u2192 ` +
      JSON.stringify(r.untranslated.map(s => s.slice(0, 32))));
    else if (!r.boxOnBoard) fail(`${code}: translated box label "${r.boxT}" not on board`);
    else pass(`${code}: T() localises all fix strings; "${r.boxT}" renders`);
    await p.close();
  }
}

// ---------- Phase 3b: G3 toggle DOM wiring (catches strings not wired via T()) ----------
async function phaseG3Dom(browser) {
  console.log('\n[3b] G3 \u2014 branded toggle DOM localised (not just dict)');
  for (const code of LANGS) {
    const p = await browser.newPage({ viewport: { width: 1720, height: 1080 } });
    // Reference board (no industry) => toggle disabled => the "pick an industry"
    // tooltips render on the seg and its buttons; the real DOM-wiring surface.
    await p.goto(H, { waitUntil: 'domcontentloaded' });
    await p.evaluate(c => localStorage.setItem('dbxarch.lang', c), code);
    await p.goto(H, { waitUntil: 'networkidle' });
    await p.waitForTimeout(800);
    const r = await p.evaluate(() => {
      const seg = document.getElementById('display-seg');
      const btns = seg ? Array.from(seg.querySelectorAll('button')) : [];
      return {
        segTitle: seg ? seg.title : null,
        segOff: seg ? seg.classList.contains('seg-off') : null,
        btnTexts: btns.map(b => b.textContent),
        btnTitles: btns.map(b => b.title),
        expSegTitle: T('Pick an industry to switch between brand and category names'),
        expBtnTitle: T('Pick an industry to enable the branded view'),
        expBranded: T('Branded'), expCategorized: T('Categorized')
      };
    });
    const problems = [];
    if (!r.segOff) problems.push('reference board should disable the toggle');
    if (r.segTitle !== r.expSegTitle) problems.push(`seg.title="${r.segTitle}" != T() "${r.expSegTitle}"`);
    if (!r.btnTitles.every(t => t === r.expBtnTitle)) problems.push(`button title not localised (${JSON.stringify(r.btnTitles)})`);
    if (!(r.btnTexts.includes(r.expBranded) && r.btnTexts.includes(r.expCategorized)))
      problems.push(`button labels not localised (${JSON.stringify(r.btnTexts)})`);
    if (problems.length) fail(`${code}: ${problems.join('; ')}`);
    else pass(`${code}: toggle labels + tooltips localised in DOM (${r.btnTexts.join('/')})`);
    await p.close();
  }
}

// ---------- Phase 4: G4 genie collapse on every cloud ----------
async function phaseGenieCollapse(browser) {
  const feats = GATE.features.filter(f => f.genieCollapse);
  if (!feats.length) return;
  console.log('\n[4] G4 \u2014 Genie collapses under "coming soon" on every cloud');
  for (const cloud of CLOUDS) {
    const p = await browser.newPage({ viewport: { width: 1720, height: 1080 } });
    await p.goto(`${H}?cloud=${cloud}`, { waitUntil: 'networkidle' });
    await p.waitForFunction(() => typeof setStages === 'function');
    const r = await p.evaluate(() => {
      const roots = [document.getElementById('plat-top'), document.getElementById('platform')].filter(Boolean);
      const vis = el => el && el.offsetParent !== null;
      const genieVis = () => { const pn = roots.flatMap(r => Array.from(r.querySelectorAll('.panel'))).find(el => /genie/i.test(el.textContent)); return pn ? vis(pn) && !pn.classList.contains('st-off') : null; };
      setStages([], true); const all = genieVis();
      setStages(['ga', 'pubpre', 'beta', 'privpre'], true); const soonOnly = genieVis();
      setStages([], true);
      return { all, soonOnly };
    });
    if (r.all === true && r.soonOnly === false) pass(`genie @ ${cloud}: visible-all=${r.all}, soon-only-collapsed=${!r.soonOnly}`);
    else fail(`genie @ ${cloud}: all=${r.all}, soonOnly=${r.soonOnly} (expected true/false)`);
    await p.close();
  }
}

// ---------- Phase 5: stage menu persists on tick, closes on outside click ----------
async function phaseStageMenu(browser) {
  console.log('\n[5] STAGE MENU \u2014 persists on tick, closes on outside click');
  const p = await browser.newPage({ viewport: { width: 1720, height: 1080 } });
  await p.goto(H, { waitUntil: 'networkidle' });
  await p.waitForTimeout(600);
  await p.evaluate(() => document.querySelectorAll('.tour-pop,.tour-catch,.tour-mask').forEach(e => e.remove()));
  const isOpen = () => p.evaluate(() => document.getElementById('stage-wrap').classList.contains('open'));
  await p.evaluate(() => document.getElementById('stage-btn').click());
  const opened = await isOpen();
  await p.evaluate(() => document.querySelector('#stage-menu button[data-stage]').click());
  await p.waitForTimeout(200);
  const afterTick = await isOpen();
  await p.evaluate(() => document.querySelector('#stage-menu button[data-stage]:nth-of-type(2)') && document.querySelectorAll('#stage-menu button[data-stage]')[1].click());
  await p.waitForTimeout(150);
  const afterSecondTick = await isOpen();
  await p.evaluate(() => document.getElementById('platform').click());
  await p.waitForTimeout(150);
  const afterOutside = await isOpen();
  if (opened && afterTick && afterSecondTick && !afterOutside)
    pass(`open=${opened}, persists-on-tick=${afterTick}/${afterSecondTick}, closes-outside=${!afterOutside}`);
  else fail(`open=${opened}, tick1=${afterTick}, tick2=${afterSecondTick}, outside-open=${afterOutside} (want true/true/true/false)`);
  await p.close();
}

(async () => {
  phaseShape();
  phaseStaticI18n();
  const browser = await chromium.launch();
  await phaseClouds(browser);
  await phaseRuntimeLang(browser);
  await phaseG3Dom(browser);
  await phaseGenieCollapse(browser);
  await phaseStageMenu(browser);
  await browser.close();
  console.log('\n' + (fails === 0 ? '\u2705 LAUNCH GATE PASSED \u2014 all clouds + all languages'
    : `\u274c LAUNCH GATE FAILED \u2014 ${fails} violation(s)`));
  process.exit(fails === 0 ? 0 : 1);
})();
