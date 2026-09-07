#!/usr/bin/env node
'use strict';
/* Smoke test for the YAML architecture descriptor feature: an open board
   serialises to a readable YAML (download), that YAML parses + rehydrates + renders
   as an imported board (upload), and the imported board is structurally identical to
   the original. Runs in the real runtime over HTTP so js-yaml + ArchSchema + the
   accelerator/connector enrichment are all exercised exactly as a user hits them. */
const { chromium } = require('playwright');
const { serve } = require('./lib_serve');

const results = [];
function check(name, cond, detail) { results.push({ name, ok: !!cond, detail }); console.log((cond ? 'PASS ' : 'FAIL ') + name + (detail ? ' :: ' + detail : '')); }

(async () => {
  const server = await serve();
  const port = server.address().port;
  const base = 'http://127.0.0.1:' + port + '/index.html';
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
  await page.addInitScript(() => { try { localStorage.setItem('dbx-arch-tour-v1', '1'); } catch (e) {} });
  await page.goto(base, { waitUntil: 'networkidle' });
  await page.waitForTimeout(400);

  check('js-yaml + ArchSchema loaded', await page.evaluate(() => typeof jsyaml !== 'undefined' && typeof ArchSchema !== 'undefined'));

  // ---- open a board, produce the descriptor (download path). ecommerce carries
  //      both Lakeflow connectors and Solution Accelerators, so enrichment resolves. ----
  const IND = 'ecommerce';
  const dl = await page.evaluate(async (ind) => {
    await applyIndustry(ind, true);
    return { yaml: archDescriptorYaml(), label: industryLabel(ind) };
  }, IND);
  check('descriptor built for open board', typeof dl.yaml === 'string' && dl.yaml.length > 2000, 'bytes=' + (dl.yaml || '').length);
  check('descriptor uses readable top-level keys',
    /^name:/m.test(dl.yaml) && /^description:/m.test(dl.yaml) && /^sources:/m.test(dl.yaml) &&
    /^cloud_integrations:/m.test(dl.yaml) && /^agent_usecases:/m.test(dl.yaml) && /^consumers:/m.test(dl.yaml));
  check('descriptor uses readable tile keys',
    /what_it_is:/.test(dl.yaml) && /who_uses_it:/.test(dl.yaml) && /summary:/.test(dl.yaml) && /citation_index:/.test(dl.yaml));
  check('descriptor carries NO terse keys',
    !/\n\s+n:\s/.test(dl.yaml) && !/\bppl:/.test(dl.yaml) && !/\brails:/.test(dl.yaml) && !/\blong:/.test(dl.yaml));
  check('enriched accelerator + connector present',
    /accelerator:/.test(dl.yaml) && /connector:/.test(dl.yaml) && /url:/.test(dl.yaml));

  // ---- baseline counts for the original board. Count DIRECT tiles in rails/top only,
  //      so enrichment (which adds accel/conn fields ON tiles, not new tiles) does not
  //      shift the count. ----
  const orig = await page.evaluate((ind) => {
    const d = INDUSTRIES[ind];
    const tc = m => { let n = 0; for (const rid of ['src','ing','ppl','cons']) for (const g of (m.rails[rid]||[])) n += (g.tiles||[]).length; for (const s of (m.top||[])) n += (s.tiles||[]).length; return n; };
    return { tiles: tc(d), src: d.rails.src.length, top: d.top.length };
  }, IND);

  // ---- import the SAME yaml back (upload path) and render it ----
  const imp = await page.evaluate(async (yamlText) => {
    const y = jsyaml.load(yamlText);
    const d = ArchSchema.toTerse(y);
    INDUSTRIES['__import__'] = d;
    await applyIndustry('__import__', false);
    const tc = m => { let n = 0; for (const rid of ['src','ing','ppl','cons']) for (const g of (m.rails[rid]||[])) n += (g.tiles||[]).length; for (const s of (m.top||[])) n += (s.tiles||[]).length; return n; };
    return {
      arch: ARCH.industry,
      label: industryLabel('__import__'),
      atoms: document.querySelectorAll('#board .atom').length,
      tiles: tc(d), src: (d.rails.src || []).length, top: (d.top || []).length,
      // The re-imported accelerator/connector must survive as per-tile overrides.
      accelOverride: (function(){ let hit = false; for (const s of (d.top || [])) for (const t of (s.tiles || [])) if (t.accel && t.accel.n) hit = true; return hit; })(),
      connOverride: (function(){ let hit = false; for (const g of (d.rails.src || [])) for (const t of (g.tiles || [])) if (t.conn && t.conn.n) hit = true; return hit; })()
    };
  }, dl.yaml);

  check('imported board applied + named from descriptor', imp.arch === '__import__' && imp.label === dl.label, 'label=' + imp.label);
  check('imported board rendered atoms', imp.atoms > 0, 'atoms=' + imp.atoms);
  check('import structurally matches original', imp.tiles === orig.tiles && imp.src === orig.src && imp.top === orig.top,
    JSON.stringify({ orig, imp: { tiles: imp.tiles, src: imp.src, top: imp.top } }));
  check('accelerator + connector round-trip as overrides', imp.accelOverride && imp.connOverride,
    'accel=' + imp.accelOverride + ' conn=' + imp.connOverride);

  // ---- the reference/generic platform (no industry) also exports a descriptor ----
  const refYaml = await page.evaluate(async () => {
    document.querySelector('#tabs .tab[data-tab="reference"]').click();
    await applyIndustry('generic', true);
    return archDescriptorYaml();
  });
  check('reference/generic board exports a descriptor',
    typeof refYaml === 'string' && /^name:/m.test(refYaml) && /^sources:/m.test(refYaml) && /^agent_usecases:/m.test(refYaml),
    'bytes=' + (refYaml || '').length);

  // ---- YAML is split out of Download into its own descriptor menu ----
  const menu = await page.evaluate(() => ({
    dlYaml: !!document.querySelector('#dl-menu button[data-dl="yaml"]'),
    archExport: !!document.querySelector('#arch-menu button[data-arch="export"]'),
    archImport: !!document.querySelector('#arch-menu button[data-arch="import"]')
  }));
  check('YAML split out of Download into a dedicated descriptor menu',
    !menu.dlYaml && menu.archExport && menu.archImport, JSON.stringify(menu));

  // ---- import via the REAL file input opens a NEW tab, keeping the current board ----
  await page.evaluate(async () => { await applyIndustry('ecommerce', true); });
  const tabsBefore = await page.evaluate(() => document.querySelectorAll('#tabs .tab').length);
  await page.setInputFiles('#arch-import', { name: 'imp1.yaml', mimeType: 'text/yaml', buffer: Buffer.from(dl.yaml.replace('name: E-Commerce', 'name: Imported One')) });
  await page.waitForTimeout(700);
  const t1 = await page.evaluate(() => ({ tabs: document.querySelectorAll('#tabs .tab').length, active: (document.querySelector('#tabs .tab.active .tab-name') || {}).textContent, arch: ARCH.industry, atoms: document.querySelectorAll('#board .atom').length }));
  check('import opens a NEW tab named from the descriptor',
    t1.tabs === tabsBefore + 1 && t1.active === 'Imported One' && /^__import__/.test(t1.arch) && t1.atoms > 0, JSON.stringify(t1));

  // ---- a second import gets its own tab and a unique board id (own citation slot) ----
  await page.setInputFiles('#arch-import', { name: 'imp2.yaml', mimeType: 'text/yaml', buffer: Buffer.from(dl.yaml.replace('name: E-Commerce', 'name: Imported Two')) });
  await page.waitForTimeout(700);
  const t2 = await page.evaluate(() => ({ tabs: document.querySelectorAll('#tabs .tab').length, arch: ARCH.industry }));
  check('second import opens another tab with a unique id',
    t2.tabs === tabsBefore + 2 && t2.arch !== t1.arch, JSON.stringify(t2));

  // ---- the reference tab kept its own board through both imports ----
  const refIntact = await page.evaluate(() => { document.querySelector('#tabs .tab[data-tab="reference"]').click(); return { atoms: document.querySelectorAll('#board .atom').length }; });
  check('reference tab preserved after imports', refIntact.atoms > 0, JSON.stringify(refIntact));

  // ---- malformed YAML surfaces an error, does not blank the board ----
  const bad = await page.evaluate(() => {
    try { const y = jsyaml.load('name: [unterminated\n  : :'); ArchSchema.toTerse(y); return 'parsed-unexpectedly'; }
    catch (e) { return 'threw'; }
  });
  check('malformed YAML throws (handled by import catch)', bad === 'threw', bad);

  check('no console/page errors', errors.length === 0, errors.slice(0, 3).join(' | '));

  await browser.close();
  server.close();
  const passed = results.filter(r => r.ok).length;
  console.log('\n' + passed + '/' + results.length + ' checks passed');
  process.exit(passed === results.length ? 0 : 1);
})();
