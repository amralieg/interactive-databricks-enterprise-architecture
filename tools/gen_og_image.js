#!/usr/bin/env node
'use strict';
/* Renders the social share cards (Open Graph / Twitter) as 1200x630 PNGs, from
   deterministic HTML->PNG so each card carries exact brand text and the Databricks
   mark, not AI-generated art.

     app/assets/og-cover.png        the reference / whole-site card
     app/assets/og/<industry>.png   one placeholder card per industry (63)

   The per-industry cards are intentionally DUMMY placeholders (a branded cover
   showing the industry glyph + name) meant to be swapped for a real board render
   later; the filename is stable so a drop-in replacement needs no other change.
   Re-run after wording/brand/icon changes. */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const ICONS = require('../app/industry_icons.js');

const ASSETS = path.join(__dirname, '..', 'app', 'assets');
const OG_DIR = path.join(ASSETS, 'og');
const OUT = path.join(ASSETS, 'og-cover.png');
const BRICK = "M12 2.2 21.4 7v3.1L12 15.4 4.4 11.1v1.6L12 17l9.4-5.3v3.1L12 20.1 2.6 14.8v-3.1L12 17l-.02-.01L2.6 11.6V8.5L12 13.8l7.6-4.3v-1.6L12 12.2 2.6 6.9 12 2.2Z";

function esc(s){ return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

// id -> clean display label, read from the INDUSTRY_CATALOG in index.html so the
// cover text matches the picker exactly (single source). Parentheticals are
// trimmed for the cover so a long qualifier does not shrink the title.
function loadLabels(){
  const html = fs.readFileSync(path.join(__dirname, '..', 'app', 'index.html'), 'utf8');
  const block = (html.match(/const INDUSTRY_CATALOG = \[([\s\S]*?)\];/) || [])[1] || '';
  const map = {};
  for (const m of block.matchAll(/\["([a-z0-9_]+)"\s*,\s*"([^"]+)"\]/g)){
    map[m[1]] = m[2].replace(/\s*\([^)]*\)\s*/g, ' ').trim();
  }
  return map;
}

const HEAD = `<meta charset="utf-8"><style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html,body { width:1200px; height:630px; }
  body { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Apple Color Emoji","Segoe UI Emoji",Helvetica,Arial,sans-serif;
    color:#EAF2F5; background:radial-gradient(1100px 700px at 78% -12%, #123543 0%, #0B222B 42%, #071820 100%);
    position:relative; overflow:hidden; }
  .accent { position:absolute; left:0; top:0; bottom:0; width:14px; background:#FF3621; }
  .wrap { position:absolute; inset:0; padding:70px 84px 58px; display:flex; flex-direction:column; }
  .brand { display:flex; align-items:center; gap:16px; }
  .brand svg { width:52px; height:52px; }
  .brand .wm { font-size:30px; font-weight:800; letter-spacing:-.01em; color:#fff; }
  .kick { margin-top:44px; font-size:19px; font-weight:700; letter-spacing:.22em; text-transform:uppercase; color:#FF6A54; }
  h1 { margin-top:14px; font-size:66px; line-height:1.04; font-weight:820; letter-spacing:-.02em; color:#fff; max-width:880px; }
  p.sub { margin-top:24px; font-size:26px; line-height:1.4; color:#B7CBD3; max-width:900px; font-weight:500; }
  .chips { margin-top:auto; display:flex; flex-wrap:wrap; gap:9px 10px; max-width:720px; }
  .chip { font-size:17px; font-weight:650; color:#CFE0E6; background:rgba(255,255,255,.06);
    border:1px solid rgba(255,255,255,.12); border-radius:999px; padding:6px 14px; }
  .url { margin-top:20px; font-size:19px; font-weight:600; color:#7C97A0; }
  .foot { position:absolute; right:84px; bottom:74px; text-align:right; }
  .foot .n { font-size:56px; font-weight:850; color:#FF3621; line-height:1; }
  .foot .l { margin-top:8px; font-size:18px; font-weight:650; color:#8FA9B2; letter-spacing:.01em; }
  /* per-industry glyph panel on the right */
  .glyph { position:absolute; right:80px; top:150px; width:300px; height:300px; border-radius:36px;
    background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.12);
    display:flex; align-items:center; justify-content:center; font-size:168px; line-height:1; }
  .tag { position:absolute; right:84px; bottom:70px; font-size:16px; font-weight:650; color:#5F7A83;
    letter-spacing:.03em; }
</style>`;

const REF_HTML = `<!DOCTYPE html><html><head>${HEAD}</head><body>
  <div class="accent"></div>
  <div class="wrap">
    <div class="brand">
      <svg viewBox="0 0 24 24"><rect width="24" height="24" rx="5.5" fill="#FF3621"/><path transform="translate(3 3)" fill="#fff" d="${BRICK}"/></svg>
      <span class="wm">Databricks</span>
    </div>
    <div class="kick">Reference Architecture</div>
    <h1>The enterprise blueprint on the Data Intelligence Platform</h1>
    <p class="sub">Sources, ingestion, governance, AI/BI, Genie agents, apps and consumers, mapped end to end and specialised for your industry.</p>
    <div class="chips">
      <span class="chip">Banking</span><span class="chip">Healthcare</span><span class="chip">Retail</span>
      <span class="chip">Manufacturing</span><span class="chip">Insurance</span><span class="chip">Telecom</span>
      <span class="chip">+ 57 more</span>
    </div>
    <div class="url">amralieg.github.io/interactive-databricks-enterprise-architecture</div>
  </div>
  <div class="foot"><div class="n">63</div><div class="l">industries · 15 languages</div></div>
</body></html>`;

function industryHtml(label, glyph){
  return `<!DOCTYPE html><html><head>${HEAD}</head><body>
  <div class="accent"></div>
  <div class="glyph">${glyph}</div>
  <div class="wrap">
    <div class="brand">
      <svg viewBox="0 0 24 24"><rect width="24" height="24" rx="5.5" fill="#FF3621"/><path transform="translate(3 3)" fill="#fff" d="${BRICK}"/></svg>
      <span class="wm">Databricks</span>
    </div>
    <div class="kick">Reference Architecture</div>
    <h1>${esc(label)}</h1>
    <p class="sub">The enterprise blueprint for ${esc(label)} on the Databricks Data Intelligence Platform.</p>
    <div class="url">amralieg.github.io/interactive-databricks-enterprise-architecture</div>
  </div>
  <div class="tag">Placeholder cover · replace with your board render</div>
</body></html>`;
}

(async () => {
  fs.mkdirSync(ASSETS, { recursive: true });
  fs.mkdirSync(OG_DIR, { recursive: true });
  const labels = loadLabels();
  const ids = Object.keys(ICONS.ICON).sort();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  const clip = { x: 0, y: 0, width: 1200, height: 630 };

  await page.setContent(REF_HTML, { waitUntil: 'networkidle' });
  await page.screenshot({ path: OUT, clip });
  console.log('wrote ' + OUT);

  for (const id of ids){
    const label = labels[id] || id;
    await page.setContent(industryHtml(label, ICONS.iconFor(id)), { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(OG_DIR, id + '.png'), clip });
  }
  console.log('wrote ' + ids.length + ' per-industry covers to ' + OG_DIR);
  await browser.close();
})();
