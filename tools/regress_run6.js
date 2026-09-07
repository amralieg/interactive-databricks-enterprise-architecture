const { chromium } = require('playwright');
const H = 'http://127.0.0.1:8021/app/index.html';
const BOARDS = ['generic', 'automotive', 'pharmaceuticals', 'banking', 'aerospace_defense', 'gaming', 'airlines'];

(async () => {
  const b = await chromium.launch();
  let fails = 0;

  // A. console + shape symmetry across boards
  for (const id of BOARDS) {
    const p = await b.newPage({ viewport: { width: 1720, height: 1080 } });
    const errs = []; p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    p.on('pageerror', e => errs.push('PAGEERR ' + e.message));
    const url = id === 'generic' ? H : `${H}?industry=${id}`;
    await p.goto(url, { waitUntil: 'networkidle' });
    await p.waitForTimeout(900);
    const m = await p.evaluate(() => {
      const h = s => { const el = document.getElementById(s); return el ? Math.round(el.getBoundingClientRect().height) : null; };
      const ov = [];
      ['rail-src', 'rail-ing', 'rail-ppl', 'rail-cons', 'topband'].forEach(id => {
        const el = document.getElementById(id); if (el && el.scrollHeight > el.clientHeight + 2) ov.push(id);
      });
      return { src: h('rail-src'), cons: h('rail-cons'), plat: h('platform'), overflow: ov };
    });
    const sym = m.src && m.cons ? Math.abs(m.src - m.cons) <= 2 : false;
    const ok = errs.length === 0 && m.plat > 0 && sym && m.overflow.length === 0;
    if (!ok) fails++;
    console.log((ok ? 'OK  ' : 'BAD ') + id.padEnd(18), 'src=' + m.src, 'cons=' + m.cons, 'plat=' + m.plat,
      'ov=' + JSON.stringify(m.overflow), 'errs=' + (errs.slice(0, 2).join(' | ') || 'none'));
    await p.close();
  }

  // B. stage filter across all stages on reference (guards panel-collapse change)
  const p = await b.newPage({ viewport: { width: 1720, height: 1080 } });
  const errs = []; p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  p.on('pageerror', e => errs.push('PAGEERR ' + e.message));
  await p.goto(H, { waitUntil: 'networkidle' });
  await p.waitForFunction(() => typeof setStages === 'function');
  const stageRes = await p.evaluate(() => {
    const roots = [document.getElementById('plat-top'), document.getElementById('platform')].filter(Boolean);
    const vis = el => el && el.offsetParent !== null;
    const genieVis = () => { const pn = roots.flatMap(r => Array.from(r.querySelectorAll('.panel'))).find(el => /genie/i.test(el.textContent)); return pn ? vis(pn) && !pn.classList.contains('st-off') : null; };
    const out = {};
    // Genie has: GA (One/Agents/Code/Designer) + Private Preview (ZeroOps/App Builder); no beta, no soon.
    setStages([], true); out.all = genieVis();                                  // visible
    setStages(['ga', 'pubpre', 'beta', 'privpre'], true); out.soonOnly = genieVis(); // collapse (nothing "soon" in Genie)
    setStages(['ga', 'pubpre', 'beta', 'soon'], true); out.privOnly = genieVis();    // visible (privpre tiles live)
    setStages(['ga', 'pubpre', 'privpre', 'soon'], true); out.betaOnly = genieVis(); // collapse (no beta in Genie)
    setStages([], true);
    out.platIntact = roots.every(r => r.offsetParent !== null);
    return out;
  });
  const passStage = stageRes.all === true && stageRes.soonOnly === false && stageRes.privOnly === true &&
    stageRes.betaOnly === false && stageRes.platIntact === true && errs.length === 0;
  if (!passStage) fails++;
  console.log((passStage ? 'OK  ' : 'BAD ') + 'stage-filter'.padEnd(18), JSON.stringify(stageRes), 'errs=' + (errs.slice(0, 2).join(' | ') || 'none'));
  await p.close();

  // C. French render of new automotive content (lang is set via localStorage, not URL)
  const p2 = await b.newPage({ viewport: { width: 1720, height: 1080 } });
  await p2.goto(`${H}?industry=automotive`, { waitUntil: 'domcontentloaded' });
  await p2.evaluate(() => localStorage.setItem('dbxarch.lang', 'fr'));
  await p2.goto(`${H}?industry=automotive`, { waitUntil: 'networkidle' });
  await p2.waitForFunction(() => /Achats et ERP/.test((document.getElementById('rail-src') || {}).textContent || ''), { timeout: 9000 }).catch(() => {});
  const fr = await p2.evaluate(() => {
    const txt = (document.getElementById('rail-src') || document.body).textContent;
    const top = (document.getElementById('topband') || document.body).textContent;
    return { procBox: /Achats et ERP/.test(txt), leadTime: /délais de livraison des fournisseurs/i.test(top),
      ivalua: /Ivalua/.test(txt) };
  });
  const passFr = fr.procBox && fr.leadTime;
  if (!passFr) fails++;
  console.log((passFr ? 'OK  ' : 'BAD ') + 'fr-render'.padEnd(18), JSON.stringify(fr));

  await b.close();
  console.log('\n' + (fails === 0 ? 'ALL REGRESSION CHECKS PASS' : fails + ' REGRESSION FAILURE(S)'));
  process.exit(fails === 0 ? 0 : 1);
})();
