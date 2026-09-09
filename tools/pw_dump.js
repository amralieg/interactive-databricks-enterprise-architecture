#!/usr/bin/env node
/* Playwright-based dump for linkgate.py: loads app/index.html in Playwright's own
 * isolated Chromium (never the user's default Chrome profile, which locks
 * --headless=new on this machine) and extracts the SAME { LINKS, prodNames,
 * genSrc, inds } structure that linkgate's in-page DUMP_JS produces. Written to
 * the file given as argv[2] so `linkgate.py --dump-file <f>` can gate without a
 * browser launch of its own. Extraction logic mirrors linkgate.DUMP_JS. */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const APP = path.resolve(__dirname, '..', 'app', 'index.html');
const OUT = process.argv[2] || '/tmp/gate_dump.json';

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newContext().then(c => c.newPage());
  const errs = [];
  page.on('pageerror', e => errs.push(String(e.message)));
  await page.goto('file://' + APP, { waitUntil: 'load', timeout: 60000 });
  const out = await page.evaluate(() => {
    function vol(t){ return t.dataOut && ((t.dataOut.batch&&t.dataOut.batch.vol)||(t.dataOut.stream&&t.dataOut.stream.vol)); }
    function srow(t){ return {n:t.n, what:!!t.what, users:!!t.users, dataOut:!!t.dataOut, vol:!!vol(t)}; }
    var out = { LINKS:{}, prodNames:[], genSrc:[], inds:{} };
    try { out.LINKS = (typeof LINKS!=='undefined') ? LINKS : {}; } catch(e){ out.links_error=String(e); }
    try {
      var seen={};
      (function walk(o){ if(!o||typeof o!=='object')return;
        if(typeof o.n==='string'){ seen[o.n]=1; }
        (Array.isArray(o)?o:Object.values(o)).forEach(walk); })(ARCH.bands);
      out.prodNames = Object.keys(seen);
    } catch(e){ out.prod_error=String(e); }
    try { (ARCH.rails.src.groups||[]).forEach(function(g){ (g.tiles||[]).forEach(function(t){ out.genSrc.push(srow(t)); }); }); } catch(e){ out.gen_error=String(e); }
    try {
      Object.keys(INDUSTRIES).forEach(function(id){
        var ind=INDUSTRIES[id], o={uc:[], src:[], cites:[]};
        ((ind.rails&&ind.rails.src)||[]).forEach(function(g){ (g.tiles||[]).forEach(function(t){ o.src.push(srow(t)); }); });
        (ind.top||[]).forEach(function(s){ if(/Business Use Cases|Use Cases/i.test(s.title)){ (s.tiles||[]).forEach(function(t){
          o.uc.push({n:t.n, stories:(t.stories||[]).map(function(x){return x.u;})}); }); } });
        var src=ind.sources||{}; Object.keys(src).forEach(function(k){ if(src[k]&&src[k].u) o.cites.push(src[k].u); });
        out.inds[id]=o;
      });
    } catch(e){ out.ind_error=String(e); }
    return out;
  });
  await browser.close();
  if (errs.length) process.stderr.write('PAGE ERRORS: ' + JSON.stringify(errs.slice(0, 5)) + '\n');
  fs.writeFileSync(OUT, JSON.stringify(out));
  process.stderr.write(`dump written: ${OUT}  LINKS=${Object.keys(out.LINKS).length} prod=${out.prodNames.length} inds=${Object.keys(out.inds).length}\n`);
  if (out.links_error || out.prod_error || out.ind_error)
    process.stderr.write('EXTRACT ERRORS: ' + JSON.stringify({l:out.links_error,p:out.prod_error,i:out.ind_error}) + '\n');
})();
