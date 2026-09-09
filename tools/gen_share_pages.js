#!/usr/bin/env node
'use strict';
/* Generates app/share/ static stubs so a social scraper (LinkedIn, Facebook,
   Slack, X) — which does not run JS — reads a per-industry, per-cloud Open Graph
   card straight from the stub, while a human is redirected to the live board.
   This is the only way to get a specialised share card on a static host, which is
   why the Share button points its network links here.

   For every architectures/<id>.yaml we write, per cloud (aws|azure|gcp):
     app/share/<id>_<cloud>.html   card titled "... for <Industry> on <Cloud>"
   plus a backward-compatible
     app/share/<id>.html           (AWS default; keeps links shared before clouds)

   Each card's og:image is the industry's own placeholder cover
   (assets/og/<id>.png). Re-run whenever industries/wording/clouds change. */
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const APP = path.join(__dirname, '..', 'app');
const ARCH_DIR = path.join(APP, 'architectures');
const OUT_DIR = path.join(APP, 'share');
/* GitHub Pages serves the repo ROOT; the board and its assets live under /app/
   (the root index.html just redirects there). Absolute OG URLs a scraper fetches
   MUST therefore include /app/, or the image 404s and the card renders blank. */
const BASE = 'https://amralieg.github.io/interactive-databricks-enterprise-architecture/app/';
const CLOUDS = { aws: 'AWS', azure: 'Azure', gcp: 'GCP' };

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

/* file = the stub's own filename (<id>.html or <id>_<cloud>.html); cloud is the
   provider key that the human is landed on. */
function stub(id, label, desc, file, cloud) {
  const cloudLabel = CLOUDS[cloud] || 'AWS';
  const title = 'Databricks Reference Architecture for ' + label + ' on ' + cloudLabel;
  const target = '../index.html?industry=' + id + '&cloud=' + cloud;
  const url = BASE + 'share/' + file;
  const img = BASE + 'assets/og/' + id + '.png';
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Databricks Reference Architecture">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(desc)}">
<meta property="og:url" content="${esc(url)}">
<meta property="og:image" content="${img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="${esc(title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${esc(title)}">
<meta name="twitter:description" content="${esc(desc)}">
<meta name="twitter:image" content="${img}">
<!-- Self-canonical, and deliberately no server/meta redirect: social scrapers
     (LinkedIn, Facebook) follow a refresh redirect and a canonical that points
     elsewhere, then scrape the TARGET page's tags instead of this stub's
     per-industry card. They do not run JS, so the script below moves a human onto
     the board while a scraper still reads this page's own Open Graph tags. -->
<link rel="canonical" href="${esc(url)}">
<script>location.replace(${JSON.stringify(target)} + location.hash);</script>
</head>
<body style="font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:#071820;color:#EAF2F5;margin:0;display:flex;min-height:100vh;align-items:center;justify-content:center;text-align:center">
<div><p>Opening the ${esc(title)}&hellip;</p><p><a style="color:#FF6A54" href="${esc(target)}">Continue</a></p></div>
</body>
</html>
`;
}

const files = fs.readdirSync(ARCH_DIR).filter(f => f.endsWith('.yaml'));
fs.mkdirSync(OUT_DIR, { recursive: true });
let n = 0;
for (const f of files) {
  const id = f.replace(/\.yaml$/, '');
  const doc = yaml.load(fs.readFileSync(path.join(ARCH_DIR, f), 'utf8')) || {};
  const label = (doc.name && String(doc.name).trim()) || id;
  const desc = (doc.description && String(doc.description).trim()) ||
    ('The Databricks Data Intelligence Platform reference architecture for ' + label + ': sources, ingestion, governance, AI/BI, Genie agents, apps and consumers.');
  for (const cloud of Object.keys(CLOUDS)) {
    const file = id + '_' + cloud + '.html';
    fs.writeFileSync(path.join(OUT_DIR, file), stub(id, label, desc, file, cloud));
    n++;
  }
  // Backward-compatible default (links shared before clouds existed): AWS.
  fs.writeFileSync(path.join(OUT_DIR, id + '.html'), stub(id, label, desc, id + '.html', 'aws'));
  n++;
}
console.log('wrote ' + n + ' share stubs to ' + OUT_DIR + ' (' + files.length + ' industries x ' + (Object.keys(CLOUDS).length + 1) + ')');
