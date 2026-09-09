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

  // ---- default OG tags on index.html (the reference-board card LinkedIn scrapes) ----
  const head = await page.evaluate(() => document.head.innerHTML);
  check('index has default og:title', /property="og:title" content="Databricks Reference Architecture"/.test(head));
  check('index has og:image under /app/ (1200x630)',
    /property="og:image" content="[^"]+\/app\/assets\/og-cover\.png"/.test(head) && /property="og:image:width" content="1200"/.test(head), head.match(/og:image" content="([^"]+)"/) ? head.match(/og:image" content="([^"]+)"/)[1] : 'missing');
  check('index has twitter summary_large_image', /name="twitter:card" content="summary_large_image"/.test(head));
  check('og-cover.png is served', (await page.evaluate(async () => (await fetch('assets/og-cover.png')).status)) === 200);

  // ---- open an industry (default cloud = AWS), open the menu, read title/hrefs ----
  const IND = 'banking';
  const data = await page.evaluate(async (ind) => {
    await applyIndustry(ind, true);
    document.getElementById('share-btn').click();
    const menu = document.getElementById('share-menu');
    const title = menu.querySelector('.sh-title').textContent;
    const land = shareLandingUrl();
    const rows = Array.from(menu.querySelectorAll('button[data-share]')).map(b => b.dataset.share);
    const T = SHARE_TARGETS.reduce((a, t) => { a[t.k] = t.copy ? null : t.href(shareLandingUrl(), shareTitle()); return a; }, {});
    /* the menu row icon is a Lucide line-art SVG (not an emoji text node), so
       "carries an icon" means the .ind-ic holds a rendered <svg> glyph */
    const icon = document.querySelector('#ind-menu button[data-ind="banking"] .ind-ic svg') ? 'svg' : '';
    return { title, land, rows, hrefs: T, label: industryLabel(ind), pageTitle: document.title, cloud: cloudLabelNow(), cloudKey: ARCH.cloud.provider, icon };
  }, IND);

  // the share card is English and now names the whatever cloud is selected
  const wantTitle = 'Databricks Reference Architecture for ' + data.label + ' on ' + data.cloud;
  check('menu titles the post with industry + cloud', data.title === wantTitle, data.title);
  check('share link is the per-industry, per-cloud stub', new RegExp('/share/banking_' + data.cloudKey + '\\.html$').test(data.land), data.land);
  check('industry menu row carries an icon glyph', data.icon.trim().length > 0, JSON.stringify(data.icon));

  // the browser-tab / page title carries the industry glyph + industry + cloud
  check('page title names industry + cloud', new RegExp('Databricks Reference Architecture for Banking on ' + data.cloud).test(data.pageTitle), data.pageTitle);
  check('page title leads with the industry glyph', data.pageTitle.trim().indexOf('Databricks') > 0, data.pageTitle);

  const want = ['linkedin', 'x', 'facebook', 'reddit', 'hn', 'whatsapp', 'telegram', 'email', 'copy'];
  check('all networks present', want.every(k => data.rows.includes(k)), data.rows.join(','));

  const enc = encodeURIComponent(data.land);
  const encT = encodeURIComponent(wantTitle);
  check('linkedin href carries the stub link', data.hrefs.linkedin.includes('share-offsite') && data.hrefs.linkedin.includes(enc), data.hrefs.linkedin);
  check('x href carries title + stub link', data.hrefs.x.includes('intent/tweet') && data.hrefs.x.includes(encT) && data.hrefs.x.includes(enc));
  check('facebook href carries the stub link', data.hrefs.facebook.includes('sharer') && data.hrefs.facebook.includes(enc));
  check('reddit href carries title + stub link', data.hrefs.reddit.includes('reddit.com/submit') && data.hrefs.reddit.includes(encT) && data.hrefs.reddit.includes(enc));
  check('hn href carries title + stub link', data.hrefs.hn.includes('ycombinator') && data.hrefs.hn.includes(encT) && data.hrefs.hn.includes(enc));
  check('whatsapp href carries title + stub link', data.hrefs.whatsapp.includes('whatsapp') && data.hrefs.whatsapp.includes(encodeURIComponent(wantTitle + ' ' + data.land)));
  check('telegram href carries title + stub link', data.hrefs.telegram.includes('t.me/share') && data.hrefs.telegram.includes(encT) && data.hrefs.telegram.includes(enc));
  check('email mailto carries title + stub link', data.hrefs.email.startsWith('mailto:') && data.hrefs.email.includes(encT) && data.hrefs.email.includes(enc));

  // ---- the localized page title follows the on-screen language ----
  const deTitle = await page.evaluate(async () => { await applyLang('de', false); const t = document.title; await applyLang('en', false); return t; });
  check('page title localizes with language (de)', /Referenzarchitektur f/.test(deTitle) && /auf (AWS|Azure|GCP)/.test(deTitle), deTitle);

  // ---- switching cloud re-points the stub + page title (switch to GCP, a cloud
  //      that differs from whatever the default is) ----
  const gcp = await page.evaluate(async () => {
    const seg = document.getElementById('cloud-seg');
    const b = Array.from(seg.querySelectorAll('button')).find(x => x.textContent === 'GCP');
    b.click();
    return { land: shareLandingUrl(), pageTitle: document.title };
  });
  check('cloud switch re-points the stub to _gcp', /\/share\/banking_gcp\.html$/.test(gcp.land), gcp.land);
  check('cloud switch updates the page title to GCP', /on GCP$/.test(gcp.pageTitle), gcp.pageTitle);

  // ---- the stub carries per-industry, per-cloud OG tags AND redirects onto the board ----
  //      Read the RAW bytes via fetch (navigating would execute its redirect script
  //      and hand back index.html instead of the stub).
  const stub = await page.evaluate(async () => {
    const r = await fetch('share/banking_aws.html');
    return { status: r.status, html: await r.text() };
  });
  check('stub served (200)', stub.status === 200, 'status=' + stub.status);
  check('stub has per-industry + cloud og:title', /og:title" content="Databricks Reference Architecture for Banking on AWS"/.test(stub.html));
  check('stub og:image is the per-industry cover under /app/', /og:image" content="[^"]+\/app\/assets\/og\/banking\.png"/.test(stub.html), (stub.html.match(/og:image" content="([^"]+)"/) || [])[1]);
  check('stub og:url is under /app/', /og:url" content="[^"]+\/app\/share\/banking_aws\.html"/.test(stub.html), (stub.html.match(/og:url" content="([^"]+)"/) || [])[1]);
  check('stub redirect carries the cloud', /industry=banking&cloud=aws/.test(stub.html));
  // A meta-refresh (or a canonical pointing at index.html) makes scrapers follow to
  // index.html and scrape ITS default card, losing the per-industry title. Lock both.
  check('stub has NO meta-refresh (scrapers follow it)', !/http-equiv=["']?refresh/i.test(stub.html));
  check('stub is self-canonical (not index.html)', /rel="canonical" href="[^"]+\/app\/share\/banking_aws\.html"/.test(stub.html) && !/rel="canonical" href="[^"]*index\.html/.test(stub.html));

  const landed = await (async () => {
    const p2 = await browser.newPage();
    await p2.addInitScript(() => { try { localStorage.setItem('dbx-arch-tour-v1', '1'); } catch (e) {} });
    await p2.goto('http://127.0.0.1:' + port + '/share/banking_azure.html', { waitUntil: 'networkidle' });
    await p2.waitForTimeout(600);
    const st = await p2.evaluate(() => ({ ind: (typeof ARCH !== 'undefined' ? ARCH.industry : null), cloud: (typeof ARCH !== 'undefined' ? ARCH.cloud.provider : null) }));
    await p2.close();
    return st;
  })();
  check('stub redirects and reopens the industry on its cloud', landed.ind === IND && landed.cloud === 'azure', JSON.stringify(landed));

  // ---- backward-compatible plain stub still resolves (links shared before clouds) ----
  const compat = await page.evaluate(async () => (await fetch('share/banking.html')).status);
  check('legacy /share/<id>.html still served (200)', compat === 200, 'status=' + compat);

  // ---- generic board titles without an industry (still names the cloud) ----
  const gen = await page.evaluate(async () => {
    await applyIndustry('generic', true);
    document.getElementById('share-wrap').classList.remove('open'); // close first (outside-click does this for a real user)
    document.getElementById('share-btn').click();                    // reopen -> rebuild with the current board
    return { title: document.getElementById('share-menu').querySelector('.sh-title').textContent, land: shareLandingUrl(), pageTitle: document.title };
  });
  check('generic board titles without an industry (with cloud)', /^Databricks Reference Architecture on (AWS|Azure|GCP)$/.test(gen.title), gen.title);
  check('generic board shares index.html (not a stub)', /\/index\.html$/.test(gen.land) && !/\/share\//.test(gen.land), gen.land);
  check('generic page title has no "for"', !/ for /.test(gen.pageTitle) && /Databricks Reference Architecture on (AWS|Azure|GCP)/.test(gen.pageTitle), gen.pageTitle);

  check('no console errors', errors.length === 0, errors.slice(0, 3).join(' | '));

  await browser.close();
  server.close();
  const failed = results.filter(r => !r.ok);
  console.log('\n' + (results.length - failed.length) + '/' + results.length + ' checks passed');
  process.exit(failed.length ? 1 : 0);
})();
