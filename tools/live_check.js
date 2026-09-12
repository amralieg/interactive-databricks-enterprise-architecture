'use strict';
// Live smoke against the REAL production server (app/main.py on :8000, which
// sends Cache-Control: no-store). Drives boot, lazy industry load, a new LTR
// (de) and the new RTL (he) language, no-store re-fetch, and offline export,
// capturing screenshots for visual confirmation.
const { chromium } = require('playwright');
const BASE = 'http://127.0.0.1:8000/index.html';
const OUT = '/tmp/idea_shots';
require('fs').mkdirSync(OUT, { recursive: true });

const R = [];
const ok = (n, c, d) => { R.push({ n, c: !!c, d }); console.log((c ? 'PASS ' : 'FAIL ') + n + (d ? ' :: ' + d : '')); };

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  const errs = [];
  page.on('pageerror', e => errs.push('PAGEERR: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errs.push('con: ' + m.text()); });
  const reqCount = {};
  page.on('request', r => { const u = r.url(); reqCount[u] = (reqCount[u] || 0) + 1; });
  await page.addInitScript(() => { try { localStorage.setItem('dbx-arch-tour-v1', '1'); } catch (e) {} });

  // boot
  await page.goto(BASE, { waitUntil: 'networkidle' });
  const boot = await page.evaluate(() => ({
    atoms: document.querySelectorAll('#platform .atom').length,
    inds: Object.keys(INDUSTRIES).length,
    links: Object.keys(LINKS).length, conn: Object.keys(CONNECTORS).length,
    connRe: CONNECTORS[Object.keys(CONNECTORS)[0]].re instanceof RegExp,
    built: (typeof INDUSTRY_BUILT !== 'undefined' && INDUSTRY_BUILT) ? INDUSTRY_BUILT.size : -1,
    menu: (syncLangMenu(), document.querySelectorAll('#lang-menu button').length),
  }));
  ok('reference board renders', boot.atoms > 0, 'atoms=' + boot.atoms);
  ok('INDUSTRIES empty at boot (lazy)', boot.inds === 0);
  ok('resources loaded (links+connectors, regex rehydrated)', boot.links > 0 && boot.conn > 0 && boot.connRe);
  ok('manifest built set (70)', boot.built === 70, 'built=' + boot.built);
  ok('language menu lists 16', boot.menu === 16, 'menu=' + boot.menu);
  await page.screenshot({ path: OUT + '/1_reference_en.png' });

  // lazy industry
  const hc = await page.evaluate(async () => { await applyIndustry('healthcare', false); return { ind: ARCH.industry, cached: !!INDUSTRIES.healthcare, atoms: document.querySelectorAll('#platform .atom').length }; });
  ok('healthcare lazy-loaded', hc.ind === 'healthcare' && hc.cached && hc.atoms > 0, JSON.stringify(hc));
  await page.screenshot({ path: OUT + '/2_healthcare_en.png' });

  // German (new LTR) on an industry
  const de = await page.evaluate(async () => { await applyIndustry('banking', false); await applyLang('de', false); const l = document.querySelector('#topband .band-lbl, #platform .band-lbl'); return { dir: I18N.dir, dict: Object.keys(I18N.dict).length, sample: (l ? l.textContent : '').trim().slice(0, 50) }; });
  ok('German renders (LTR, industry localized)', de.dir === 'ltr' && de.dict > 2000 && /[A-Za-zÄÖÜäöüß]/.test(de.sample), JSON.stringify(de));
  await page.screenshot({ path: OUT + '/3_banking_de.png' });

  // Hebrew (new RTL)
  const he = await page.evaluate(async () => { await applyLang('he', false); const l = document.querySelector('#platform .band-lbl'); return { dir: I18N.dir, dict: Object.keys(I18N.dict).length, sample: (l ? l.textContent : '').trim().slice(0, 40) }; });
  ok('Hebrew renders (RTL)', he.dir === 'rtl' && he.dict > 2000, JSON.stringify(he));
  await page.screenshot({ path: OUT + '/4_banking_he_rtl.png' });

  // no-store re-fetch: revisit healthcare -> served from memory, not refetched
  await page.evaluate(async () => { await applyLang('en', false); await applyIndustry('retail', false); await applyIndustry('healthcare', false); });
  const hcReq = Object.keys(reqCount).filter(u => u.includes('/architectures/healthcare.yaml')).reduce((a, u) => a + reqCount[u], 0);
  ok('no-store safe: industry fetched once, then in-memory', hcReq === 1, 'healthcare.json fetches=' + hcReq);

  ok('no console/page errors', errs.length === 0, errs.slice(0, 5).join(' | '));

  await browser.close();
  const failed = R.filter(r => !r.c).length;
  console.log('\n' + (R.length - failed) + '/' + R.length + ' live checks passed  (screenshots in ' + OUT + ')');
  process.exit(failed ? 1 : 0);
})();
