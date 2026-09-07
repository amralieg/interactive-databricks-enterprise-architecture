#!/usr/bin/env node
'use strict';
/* Smoke test for the social Share control: the button sits to the right of the
   feedback button, its menu titles the post "Databricks Reference Architecture
   for <industry>", every network href carries the deep link that reopens THAT
   industry, and the deep link actually lands on the industry via seedFromUrl. */
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

  // ---- structure: share button exists and sits immediately after feedback ----
  check('share button exists', await page.evaluate(() => !!document.getElementById('share-btn')));
  check('share button is to the right of feedback', await page.evaluate(() => {
    const fb = document.getElementById('feedback-btn');
    const sw = document.getElementById('share-wrap');
    if (!fb || !sw) return false;
    // share-wrap is the next element sibling after the feedback button
    return fb.nextElementSibling === sw;
  }));

  // ---- open an industry, open the menu, read the title + hrefs ----
  const IND = 'banking';
  const data = await page.evaluate(async (ind) => {
    await applyIndustry(ind, true);
    document.getElementById('share-btn').click();
    const menu = document.getElementById('share-menu');
    const title = menu.querySelector('.sh-title').textContent;
    const url = liveUrl();
    const rows = Array.from(menu.querySelectorAll('button[data-share]')).map(b => b.dataset.share);
    // resolve each network href off the live target/title
    const T = SHARE_TARGETS.reduce((a, t) => { a[t.k] = t.copy ? null : t.href(liveUrl(), shareTitle()); return a; }, {});
    return { title, url, rows, hrefs: T, label: industryLabel(ind) };
  }, IND);

  check('menu titles the post with the industry',
    data.title === 'Databricks Reference Architecture for ' + data.label, data.title);
  check('deep link points at the industry', /[?&]industry=banking(&|$)/.test(data.url), data.url);
  const want = ['linkedin', 'x', 'facebook', 'reddit', 'hn', 'whatsapp', 'telegram', 'email', 'copy'];
  check('all networks present', want.every(k => data.rows.includes(k)), data.rows.join(','));

  const enc = encodeURIComponent(data.url);
  const encT = encodeURIComponent('Databricks Reference Architecture for ' + data.label);
  check('linkedin href carries the deep link', data.hrefs.linkedin.includes('share-offsite') && data.hrefs.linkedin.includes(enc), data.hrefs.linkedin);
  check('x href carries title + deep link', data.hrefs.x.includes('intent/tweet') && data.hrefs.x.includes(encT) && data.hrefs.x.includes(enc));
  check('facebook href carries the deep link', data.hrefs.facebook.includes('sharer') && data.hrefs.facebook.includes(enc));
  check('reddit href carries title + deep link', data.hrefs.reddit.includes('reddit.com/submit') && data.hrefs.reddit.includes(encT) && data.hrefs.reddit.includes(enc));
  check('hn href carries title + deep link', data.hrefs.hn.includes('ycombinator') && data.hrefs.hn.includes(encT) && data.hrefs.hn.includes(enc));
  check('whatsapp href carries title + deep link', data.hrefs.whatsapp.includes('whatsapp') && data.hrefs.whatsapp.includes(encodeURIComponent('Databricks Reference Architecture for ' + data.label + ' ' + data.url)));
  check('telegram href carries title + deep link', data.hrefs.telegram.includes('t.me/share') && data.hrefs.telegram.includes(encT) && data.hrefs.telegram.includes(enc));
  check('email mailto carries title + deep link', data.hrefs.email.startsWith('mailto:') && data.hrefs.email.includes(encT) && data.hrefs.email.includes(enc));

  // ---- the deep link genuinely lands on the industry (seedFromUrl round-trip) ----
  const landed = await (async () => {
    const p2 = await browser.newPage();
    await p2.addInitScript(() => { try { localStorage.setItem('dbx-arch-tour-v1', '1'); } catch (e) {} });
    await p2.goto('http://127.0.0.1:' + port + '/' + data.url.split('/').pop(), { waitUntil: 'networkidle' });
    await p2.waitForTimeout(500);
    const ind = await p2.evaluate(() => ARCH.industry);
    await p2.close();
    return ind;
  })();
  check('deep link reopens the industry', landed === IND, 'landed=' + landed);

  // ---- generic board titles without an industry ----
  const gen = await page.evaluate(async () => {
    await applyIndustry('generic', true);
    document.getElementById('share-wrap').classList.remove('open'); // close first (outside-click does this for a real user)
    document.getElementById('share-btn').click();                    // reopen -> rebuild with the current board
    return document.getElementById('share-menu').querySelector('.sh-title').textContent;
  });
  check('generic board titles without an industry', gen === 'Databricks Reference Architecture', gen);

  check('no console errors', errors.length === 0, errors.slice(0, 3).join(' | '));

  await browser.close();
  server.close();
  const failed = results.filter(r => !r.ok);
  console.log('\n' + (results.length - failed.length) + '/' + results.length + ' checks passed');
  process.exit(failed.length ? 1 : 0);
})();
