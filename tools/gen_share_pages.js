#!/usr/bin/env node
'use strict';
/* Generates app/share/<industry>.html static stubs, one per architectures/*.yaml.
   A social scraper (LinkedIn, Facebook, Slack, X) does not run JS, so it reads the
   per-industry Open Graph tags straight from the stub; a human is redirected to the
   live board (../index.html?industry=<id>) instantly. This is the only way to get a
   per-industry share card on a static host, which is why the Share button points its
   network links here for a named industry. Re-run whenever industries/wording change. */
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const APP = path.join(__dirname, '..', 'app');
const ARCH_DIR = path.join(APP, 'architectures');
const OUT_DIR = path.join(APP, 'share');
const BASE = 'https://amralieg.github.io/interactive-databricks-enterprise-architecture/';
const IMG = BASE + 'assets/og-cover.png';

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function stub(id, label, desc) {
  const title = 'Databricks Reference Architecture for ' + label;
  const target = '../index.html?industry=' + id;
  const url = BASE + 'share/' + id + '.html';
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
<meta property="og:image" content="${IMG}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="${esc(title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${esc(title)}">
<meta name="twitter:description" content="${esc(desc)}">
<meta name="twitter:image" content="${IMG}">
<link rel="canonical" href="${esc(target)}">
<meta http-equiv="refresh" content="0; url=${esc(target)}">
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
  fs.writeFileSync(path.join(OUT_DIR, id + '.html'), stub(id, label, desc));
  n++;
}
console.log('wrote ' + n + ' share stubs to ' + OUT_DIR);
