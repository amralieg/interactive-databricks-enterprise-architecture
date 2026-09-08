#!/usr/bin/env node
'use strict';
/* Renders the social share cards (Open Graph / Twitter) as 1200x630 PNGs from
   deterministic HTML->PNG, so each card carries exact brand text, the official
   Databricks mark, and the industry's line-art silhouette (a large, faded
   watermark in Databricks red) — not AI-generated art.

     app/assets/og-cover.png        the reference / whole-site card
     app/assets/og/<industry>.png   one branded cover per industry (63)

   The per-industry cards are branded placeholders (silhouette + name) meant to
   be swapped for a real board render later; the filename is stable so a drop-in
   replacement needs no other change. Re-run after wording/brand/icon changes. */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const ICONS = require('../app/industry_icons.js');

const ASSETS = path.join(__dirname, '..', 'app', 'assets');
const OG_DIR = path.join(ASSETS, 'og');
const OUT = path.join(ASSETS, 'og-cover.png');
const URL = 'amralieg.github.io/interactive-databricks-enterprise-architecture';
const SUB = 'Databricks Data Intelligence Platform';
// The official Databricks lockup (brick mark + wordmark), white wordmark for the
// dark card. Same artwork the app header and deck covers use (IndustryIcons).
const LOGO = ICONS.dbxLogoSvg({ wordmark: '#ffffff', height: 52 });

function esc(s){ return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

// id -> clean display label, read from INDUSTRY_CATALOG in index.html so the
// cover text matches the picker exactly. Parentheticals are trimmed so a long
// qualifier does not shrink the title.
function loadLabels(){
  const html = fs.readFileSync(path.join(__dirname, '..', 'app', 'index.html'), 'utf8');
  const block = (html.match(/const INDUSTRY_CATALOG = \[([\s\S]*?)\];/) || [])[1] || '';
  const map = {};
  for (const m of block.matchAll(/\["([a-z0-9_]+)"\s*,\s*"([^"]+)"\]/g)){
    map[m[1]] = m[2].replace(/\s*\([^)]*\)\s*/g, ' ').trim();
  }
  return map;
}

// Auto-shrink the title so a long single word (e.g. Telecommunications) never
// overflows — single words cannot wrap, so they drive the size.
function fontFor(label){
  const maxWord = Math.max.apply(null, label.split(/\s+/).map(w => w.length));
  if (maxWord >= 15) return 66;
  if (maxWord >= 13) return 78;
  if (label.length >= 20) return 82;
  return 92;
}

function head(fs_){ return `<meta charset="utf-8"><style>
  *{margin:0;padding:0;box-sizing:border-box}html,body{width:1200px;height:630px}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:#EAF2F5;
    background:linear-gradient(125deg,#1B3139 0%,#0E232B 52%,#07161B 100%);position:relative;overflow:hidden}
  .accent{position:absolute;left:0;top:0;bottom:0;width:12px;background:#FF3621;z-index:3}
  .wm{position:absolute;left:63%;top:50%;transform:translate(-50%,-50%);width:940px;height:940px;z-index:0;
    -webkit-mask-image:linear-gradient(100deg,transparent 30%,#000 66%);mask-image:linear-gradient(100deg,transparent 30%,#000 66%)}
  .wm svg{width:100%;height:100%;fill:none;stroke:url(#g);stroke-width:.46;stroke-linecap:round;stroke-linejoin:round;opacity:.55}
  .wrap{position:absolute;inset:0;padding:72px 84px 62px;display:flex;flex-direction:column;z-index:2}
  .brand{display:flex;align-items:center}.brand svg{height:52px;width:auto;display:block}
  .mid{flex:1;display:flex;flex-direction:column;justify-content:center}
  .kick{margin:0;font-size:22px;font-weight:700;letter-spacing:.24em;text-transform:uppercase;color:#FF5F46}
  h1{margin:76px 0 76px;font-size:${fs_}px;line-height:1.02;font-weight:850;letter-spacing:-.025em;color:#fff;max-width:720px}
  p.sub{margin:0;font-size:31px;line-height:1.36;color:#C6D6DD;max-width:640px;font-weight:500}
  .url{margin:0;font-size:21px;font-weight:600;color:#8AA4AD}
</style>`; }

function watermark(glyph){
  return `<div class="wm"><svg viewBox="0 0 24 24"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#FF3621"/><stop offset="1" stop-color="#FF9A85"/></linearGradient></defs>${glyph}</svg></div>`;
}

function card(label, glyph){
  return `<!DOCTYPE html><html><head>${head(fontFor(label))}</head><body>
  <div class="accent"></div>
  ${watermark(glyph)}
  <div class="wrap">
    <div class="brand">${LOGO}</div>
    <div class="mid">
      <div class="kick">Reference Architecture</div>
      <h1>${esc(label)}</h1>
      <p class="sub">${SUB}</p>
    </div>
    <div class="url">${URL}</div>
  </div></body></html>`;
}

// The site-wide reference card: same system, generic silhouette, whole-portfolio wording.
function refCard(){
  const label = 'Enterprise Reference Architecture';
  return `<!DOCTYPE html><html><head>${head(fontFor(label))}</head><body>
  <div class="accent"></div>
  ${watermark(ICONS.svgFor('generic'))}
  <div class="wrap">
    <div class="brand">${LOGO}</div>
    <div class="mid">
      <div class="kick">63 Industries · 15 Languages</div>
      <h1>${esc(label)}</h1>
      <p class="sub">${SUB}</p>
    </div>
    <div class="url">${URL}</div>
  </div></body></html>`;
}

(async () => {
  fs.mkdirSync(ASSETS, { recursive: true });
  fs.mkdirSync(OG_DIR, { recursive: true });
  const labels = loadLabels();
  const ids = Object.keys(ICONS.ICON).sort();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  const clip = { x: 0, y: 0, width: 1200, height: 630 };

  await page.setContent(refCard(), { waitUntil: 'networkidle' });
  await page.screenshot({ path: OUT, clip });
  console.log('wrote ' + OUT);

  for (const id of ids){
    const label = labels[id] || id;
    await page.setContent(card(label, ICONS.svgFor(id)), { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(OG_DIR, id + '.png'), clip });
  }
  console.log('wrote ' + ids.length + ' per-industry covers to ' + OG_DIR);
  await browser.close();
})();
