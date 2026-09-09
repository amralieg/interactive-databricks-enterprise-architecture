#!/usr/bin/env node
'use strict';
/*
  Live T()-miss audit. Instruments T() to record every argument that is NOT in the
  translation corpus, then drives all industries x sampled languages x both display
  modes (LTR + RTL), opening a drawer per industry to exercise the prose path. Any
  distinct T() argument absent from the corpus is an extraction gap: the runtime
  intends to translate it but the extractor never captured it, so it renders English
  in every language. Prints the distinct misses; exits non-zero if any remain.

  This proves the REAL render path, complementing the static routing gate.
*/
const { chromium } = require('playwright');
const { serve, APP_ROOT: APP } = require('./lib_serve');
const fs = require('fs');
const path = require('path');

const corpus = JSON.parse(fs.readFileSync(path.join(APP, 'translations', '_corpus.json'), 'utf8'));
// Glossary terms (product/brand names) are deliberately NOT translated, so T()
// returning them unchanged is correct — exclude them from the miss set.
const glossary = JSON.parse(fs.readFileSync(path.join(APP, 'translations', '_glossary.json'), 'utf8'));

// Languages to drive: any that ship a _common.json. Cap at 2 (one RTL, one LTR)
// for speed — the miss set is language-independent (it depends on which strings
// the render path passes to T(), not on the target language).
const shipped = fs.readdirSync(path.join(APP, 'translations'))
  .filter(d => fs.existsSync(path.join(APP, 'translations', d, '_common.json')));
const drive = ['ar', 'fr'].filter(c => shipped.includes(c));

(async () => {
  const server = await serve();
  const port = server.address().port;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.addInitScript((payload) => {
    window.__CORPUS = new Set(payload.corpus);
    window.__GLOSSARY = new Set(payload.glossary);
    window.__i18nMiss = new Set();
  }, { corpus, glossary });
  await page.addInitScript(() => { try { localStorage.setItem('dbx-arch-tour-v1', '1'); } catch (e) {} });
  await page.goto('http://127.0.0.1:' + port + '/index.html', { waitUntil: 'networkidle' });

  // Wrap T() so every argument is checked against the corpus. Runs regardless of
  // active language (record the intent to translate, not the result).
  await page.evaluate(() => {
    const orig = window.T;
    window.T = function (s) {
      if (typeof s === 'string') { const t = s.trim(); if (t && /[A-Za-z]/.test(t) && !window.__CORPUS.has(t) && !window.__GLOSSARY.has(t)) window.__i18nMiss.add(t); }
      return orig.apply(this, arguments);
    };
  });

  const ids = await page.evaluate(() => INDUSTRY_CATALOG.map(x => x[0]));
  let combos = 0;
  for (const lang of drive) {
    await page.evaluate(async (l) => { await applyLang(l, false); }, lang);
    for (const mode of ['category', 'commercial']) {
      await page.evaluate((m) => { if (typeof setDisplay === 'function') setDisplay(m); else { displayMode = m; build(); } }, mode).catch(() => {});
      for (const id of ids) {
        await page.evaluate(async (i) => { await applyIndustry(i, false); }, id);
        // open the first atom's drawer to exercise the prose path, then close
        await page.evaluate(() => { const a = document.querySelector('#plat-top .atom') || document.querySelector('.atom'); if (a && a.dataset && a.dataset.id && typeof openDetail === 'function') openDetail(a.dataset.id, 'audit'); });
        await page.evaluate(() => { if (typeof closeDrawer === 'function') closeDrawer(); });
        combos++;
      }
    }
  }

  const miss = await page.evaluate(() => Array.from(window.__i18nMiss).sort());
  console.log('Audited ' + combos + ' (industry x lang x mode) combinations across ' + drive.join('+') + ', ' + ids.length + ' industries.');
  console.log('Distinct T() arguments absent from corpus: ' + miss.length);
  miss.slice(0, 60).forEach(m => console.log('  MISS: ' + JSON.stringify(m)));
  if (miss.length > 60) console.log('  ... and ' + (miss.length - 60) + ' more');

  await browser.close(); server.close();
  process.exit(miss.length ? 1 : 0);
})();
