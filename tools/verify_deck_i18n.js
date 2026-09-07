#!/usr/bin/env node
'use strict';
/*
  Runtime deck-export i18n gate. The static DECK_TPL check in verify_i18n_coverage
  proves every shipped language HAS the template keys; this proves the runtime path
  that assembles the exported PPTX/PDF (deckSections + deckCount, the same code both
  exporters call) actually emits localized strings, for every shipped language over
  real industries. It exists because the original runtime audit only drove the web
  UI drawers and never the deck path, which let the automotive-JA deck ship its
  blurbs in English. Fails non-zero if any section blurb or count caption renders as
  the English template with the placeholders merely filled in.
*/
const { chromium } = require('playwright');
const path = require('path');
const { serve } = require('./lib_serve');

const LANGS = ['de', 'pt', 'nl', 'ja', 'it', 'sv', 'ko', 'da', 'fi', 'he'];
const INDS = ['automotive', 'banking', 'healthcare'];
// Non-Latin scripts: any pure-ASCII string is unambiguously an English leak there.
// For Latin scripts, a short count caption may legitimately equal English as a
// loanword (Danish "apps"/"dashboards"), so captions are only script-checked, while
// long blurbs (real prose) must always differ from English in every language.
const NON_LATIN = new Set(['ja', 'ko', 'zh', 'ar', 'he', 'hi']);
const isAsciiOnly = s => !/[^\x00-\x7f]/.test(s);

(async () => {
  const server = await serve();
  const base = 'http://127.0.0.1:' + server.address().port + '/index.html';
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const errs = [];
  page.on('pageerror', e => errs.push('PAGEERR ' + e.message));
  await page.addInitScript(() => { try { localStorage.setItem('dbx-arch-tour-v1', '1'); } catch (e) {} });
  await page.goto(base, { waitUntil: 'networkidle' });

  let fails = 0, checks = 0;
  for (const ind of INDS) {
    await page.evaluate(async id => { await applyIndustry(id, false); }, ind);
    for (const L of LANGS) {
      const r = await page.evaluate(async lang => {
        await applyLang(lang, false);
        // English reference for the same key/vars, computed against DECK_TPL.en
        const enFill = (key, vars) => { let s = DECK_TPL.en[key] || ''; if (vars) for (const k in vars) s = s.split('{' + k + '}').join(vars[k]); return s; };
        const secs = deckSections();
        const out = [];
        for (const s of secs) {
          // reconstruct the vars each blurb was built with
          const vars = s.key === 'arch' ? { ind: deckIndustry() }
            : s.key === 'uc' ? { n: (s.tiles || []).length, ind: deckIndustry() }
            : s.key === 'genie' ? { ind: deckIndustry() } : null;
          const enKey = s.key === 'arch' ? 'archBlurb' : s.key === 'uc' ? 'ucBlurb' : s.key === 'genie' ? 'genieBlurb' : s.key === 'dash' ? 'dashBlurb' : 'appBlurb';
          out.push({ key: s.key, blurb: s.blurb || '', en: enFill(enKey, vars), n: (s.tiles || []).length });
        }
        // one count caption per content section
        const caps = [];
        for (const s of secs) if (s.key !== 'arch') caps.push({ key: s.key, cap: deckCount(s.key, (s.tiles || []).length), en: (function () { let x = DECK_TPL.en[(s.key === 'uc' ? 'ucCount' : s.key === 'genie' ? 'genieCount' : s.key === 'dash' ? 'dashCount' : 'appCount')]; return x.split('{n}').join((s.tiles || []).length); })() });
        return { dir: I18N.dir, secs: out, caps };
      }, L);

      for (const s of r.secs) {
        checks++;
        // A blurb (long prose) equal to the English-template fill is an untranslated
        // leak in every language — real prose never legitimately matches English.
        if (s.blurb.trim() === s.en.trim()) { fails++; console.log('FAIL blurb ' + L + '/' + ind + '/' + s.key + ' :: ' + s.blurb.slice(0, 60)); }
      }
      for (const c of r.caps) {
        checks++;
        // Count captions: only a definite leak when a non-Latin-script language
        // renders pure ASCII (e.g. a Japanese "10 use cases"). A Latin-script
        // caption equal to English is an accepted loanword (Danish "4 apps").
        if (NON_LATIN.has(L) && isAsciiOnly(c.cap)) { fails++; console.log('FAIL count ' + L + '/' + ind + '/' + c.key + ' :: ' + c.cap); }
      }
    }
  }
  await browser.close();
  server.close();
  if (errs.length) { console.log('page errors:\n  ' + errs.slice(0, 5).join('\n  ')); fails += errs.length; }
  console.log('\n' + (checks - fails) + '/' + checks + ' deck i18n checks passed across ' + LANGS.length + ' langs x ' + INDS.length + ' industries');
  console.log(fails ? 'DECK I18N GATE FAILED (' + fails + ')' : 'DECK I18N GATE PASSED');
  process.exit(fails ? 1 : 0);
})();
