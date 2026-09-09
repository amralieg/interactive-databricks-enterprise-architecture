#!/usr/bin/env node
/* Doc-grounded "see also" builder using Playwright's own isolated Chromium, so
 * it never touches the user's default Chrome profile (which locks headless).
 *
 * Same grounding as seealso_build.py: render the feature's real Databricks doc
 * page, take ONLY the links inside the main <article> (never the sidebar nav,
 * breadcrumb or footer, which list the whole doc tree), and map each in-article
 * link to another feature in our LINKS set by matching its doc path. Grounded
 * twice over: the source page really links the target, and the URL shown at
 * runtime is the target feature's own known-good doc path (never invented).
 *
 * Reads /tmp/feat_docpaths.json and /tmp/path2name.json. Writes name -> [names].
 */
const { chromium } = require('playwright');
const fs = require('fs');

const AWS = 'https://docs.databricks.com/aws/en/';
const FEAT = JSON.parse(fs.readFileSync('/tmp/feat_docpaths.json', 'utf8'));
const PATH2NAME = JSON.parse(fs.readFileSync('/tmp/path2name.json', 'utf8'));
const OUT = process.argv[2] || '/tmp/seealso_map.json';
const CONC = parseInt(process.env.SA_CONC || '4', 10);

function norm(p) {
  p = (p || '').replace(/[#?].*$/, '');          // drop fragment / query
  p = p.replace(/^https?:\/\/[^/]+/, '');         // drop host
  p = p.replace('/aws/en/', '').replace('/gcp/en/', '');
  return p.trim().replace(/^\/+|\/+$/g, '').toLowerCase();
}

async function relatedFor(context, name) {
  const doc = (FEAT[name] || {}).doc;
  if (!doc) return [name, []];
  const selfNorm = norm(doc);
  const url = AWS + doc.replace(/^\/+/, '');
  const page = await context.newPage();
  const out = [];
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    // Wait for the article body to hydrate; the SPA injects in-article links
    // after first paint. Fall back to whatever is present if it never settles.
    await page.waitForSelector('article a[href]', { timeout: 20000 }).catch(() => {});
    const hrefs = await page.$$eval('article a[href]', as => as.map(a => a.getAttribute('href')));
    for (const h of hrefs) {
      if (!h) continue;
      if (h.indexOf('/aws/en/') === -1 && h.indexOf('http') === 0) continue;
      const np = norm(h);
      const tgt = PATH2NAME[np];
      if (tgt && tgt !== name && np !== selfNorm && out.indexOf(tgt) === -1) out.push(tgt);
    }
  } catch (e) {
    process.stderr.write(`[${name}] ${e.message}\n`);
  } finally {
    await page.close().catch(() => {});
  }
  return [name, out];
}

(async () => {
  const names = Object.keys(FEAT).filter(n => FEAT[n].doc);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ userAgent:
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36' });
  const result = {};
  let done = 0;
  const queue = names.slice();
  async function worker() {
    while (queue.length) {
      const name = queue.shift();
      const [n, rel] = await relatedFor(context, name);
      result[n] = rel;
      done++;
      fs.writeFileSync(OUT, JSON.stringify(result, null, 1));
      process.stderr.write(`${done}/${names.length} ${n}: ${rel.length} -> ${JSON.stringify(rel)}\n`);
    }
  }
  await Promise.all(Array.from({ length: Math.min(CONC, names.length) }, worker));
  await browser.close();
  const kept = Object.entries(result).filter(([, v]) => v.length);
  process.stderr.write(`\nDONE. ${kept.length}/${names.length} features have see-also; ` +
    `${kept.reduce((s, [, v]) => s + v.length, 0)} edges.\n`);
})();
