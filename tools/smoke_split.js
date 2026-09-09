#!/usr/bin/env node
'use strict';
/* Smoke test for the data-modularisation split: reference board renders with the
   industry/resource literals externalised, resources load at boot, industries
   lazy-load on demand, a bad id falls back to generic, and a deep link loads its
   industry. Serves app/ with the production server's semantics: an unknown path
   returns index.html (HTML, 200), so the loadIndustry content-type guard is
   exercised for a bad industry id. */
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
  // Count fetches per URL to prove the in-memory industry cache prevents any
  // re-fetch on revisit (the no-store resilience case: HTTP headers are moot
  // because loadIndustry short-circuits when INDUSTRIES[id] is already present).
  const reqCount = {};
  page.on('request', r => { const u = r.url(); reqCount[u] = (reqCount[u] || 0) + 1; });
  await page.addInitScript(() => { try { localStorage.setItem('dbx-arch-tour-v1', '1'); } catch (e) {} });

  // ---- boot: reference board + resources ----
  await page.goto(base, { waitUntil: 'networkidle' });
  await page.waitForTimeout(500);
  check('reference platform rendered', await page.$('#platform') && (await page.$$('#platform .atom')).length > 0);
  const res = await page.evaluate(() => ({
    links: Object.keys(LINKS).length,
    refs: REFERENCES.length,
    accel: Object.keys(ACCEL_BY_NAME).length,
    conn: Object.keys(CONNECTORS).length,
    connRe: Object.values(CONNECTORS).every(c => c.re instanceof RegExp),
    inds: Object.keys(INDUSTRIES).length,
    built: (typeof INDUSTRY_BUILT !== 'undefined' && INDUSTRY_BUILT) ? INDUSTRY_BUILT.size : -1,
  }));
  check('resources loaded (links>100)', res.links > 100, 'links=' + res.links);
  check('references loaded', res.refs > 0, 'refs=' + res.refs);
  check('accelerators loaded', res.accel > 0, 'accel=' + res.accel);
  check('connectors loaded + regex rehydrated', res.conn > 0 && res.connRe, 'conn=' + res.conn + ' reOk=' + res.connRe);
  check('INDUSTRIES empty at boot (lazy)', res.inds === 0, 'inds=' + res.inds);
  check('manifest built-set loaded (63)', res.built === 63, 'built=' + res.built);

  // ---- lazy industry switch ----
  const healthcareLoad = await page.evaluate(async () => {
    await applyIndustry('healthcare', true);
    return { arch: ARCH.industry, cached: !!INDUSTRIES.healthcare };
  });
  check('healthcare lazy-loaded + applied', healthcareLoad.arch === 'healthcare' && healthcareLoad.cached, JSON.stringify(healthcareLoad));

  // ---- bad id falls back to generic (content-type guard) ----
  const bad = await page.evaluate(async () => {
    await applyIndustry('nonexistent_industry_xyz', false);
    return ARCH.industry;
  });
  check('bad industry id -> generic fallback', bad === 'generic', 'arch=' + bad);

  // ---- rapid A->B->A: last one wins ----
  const race = await page.evaluate(async () => {
    const p1 = applyIndustry('banking', false);
    const p2 = applyIndustry('healthcare', false);
    await Promise.all([p1, p2]);
    return ARCH.industry;
  });
  check('rapid switch settles on last (healthcare)', race === 'healthcare', 'arch=' + race);

  // ---- deep link loads its industry ----
  const page2 = await browser.newPage();
  page2.on('pageerror', e => errors.push('PAGEERROR(deep): ' + e.message));
  await page2.addInitScript(() => { try { localStorage.setItem('dbx-arch-tour-v1', '1'); } catch (e) {} });
  await page2.goto('http://127.0.0.1:' + port + '/index.html?industry=retail', { waitUntil: 'networkidle' });
  await page2.waitForTimeout(500);
  const deep = await page2.evaluate(() => ({ arch: ARCH.industry, cached: !!INDUSTRIES.retail }));
  check('deep link ?industry=retail loaded', deep.arch === 'retail' && deep.cached, JSON.stringify(deep));

  // ---- no-store resilience: revisiting a loaded industry never re-fetches ----
  await page.evaluate(async () => { await applyIndustry('banking', false); await applyIndustry('healthcare', false); });
  const hcReq = Object.keys(reqCount).filter(u => u.includes('/architectures/healthcare.yaml')).reduce((a, u) => a + reqCount[u], 0);
  check('industry fetched once then in-memory (no-store safe)', hcReq === 1, 'healthcare.json fetches=' + hcReq);

  // ---- language switch while an industry is applied re-localizes its tiles ----
  const langOpen = await page.evaluate(async () => {
    await applyIndustry('healthcare', false);
    const before = (typeof I18N !== 'undefined' && I18N.dict) ? Object.keys(I18N.dict).length : 0;
    await applyLang('ar', false);
    const after = (typeof I18N !== 'undefined' && I18N.dict) ? Object.keys(I18N.dict).length : 0;
    const dir = (typeof I18N !== 'undefined') ? I18N.dir : null;   // authoritative RTL flag
    await applyLang('en', false);   // restore for the no-error check
    return { before, after, dir };
  });
  check('lang switch while industry open merges shard (ar rtl)', langOpen.after > langOpen.before && langOpen.dir === 'rtl', JSON.stringify(langOpen));

  check('no console/page errors', errors.length === 0, errors.slice(0, 10).join(' | '));

  await browser.close();
  server.close();
  const failed = results.filter(r => !r.ok).length;
  console.log('\n' + (results.length - failed) + '/' + results.length + ' checks passed');
  process.exit(failed ? 1 : 0);
})();
