const { chromium } = require('playwright');
const BASE = 'http://127.0.0.1:8021/app/index.html?industry=automotive&theme=light';

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1720, height: 1080 } });
  const errs = [];
  p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  p.on('pageerror', e => errs.push('PAGEERROR ' + e.message));
  await p.goto(BASE, { waitUntil: 'networkidle' });
  await p.waitForTimeout(1200);
  await p.evaluate(() => { document.querySelectorAll('.tour-pop,.tour-catch,.tour-mask').forEach(e => e.remove()); });

  const m = await p.evaluate(() => {
    const rect = s => { const el = document.querySelector(s); return el ? Math.round(el.getBoundingClientRect().height) : null; };
    const railH = {};
    ['rail-src', 'rail-ing', 'rail-ppl', 'rail-cons'].forEach(id => {
      const el = document.getElementById(id);
      if (el) railH[id] = Math.round(el.getBoundingClientRect().height);
    });
    // top band use-case section: count tiles + rows
    const secs = Array.from(document.querySelectorAll('#topband .tsec, #topband .band, #topband .tgrid, #topband .top-sec'));
    // fallback: find the Business Use Cases grid by counting .ucard/.ttile-like
    const ucTiles = document.querySelectorAll('#topband .uctile, #topband .ucard, #topband .ttile');
    // source rail boxes + tiles
    const srcBoxes = document.querySelectorAll('#rail-src .rgroup, #rail-src .rbox, #rail-src .side-box').length;
    const srcTiles = document.querySelectorAll('#rail-src .rtile').length;
    // overflow within rails
    const overflow = [];
    ['rail-src', 'rail-ing', 'rail-ppl', 'rail-cons', 'topband'].forEach(id => {
      const el = document.getElementById(id);
      if (el && el.scrollHeight > el.clientHeight + 2) overflow.push(id + ' sH=' + el.scrollHeight + ' cH=' + el.clientHeight);
    });
    const fitScale = getComputedStyle(document.getElementById('board') || document.body).getPropertyValue('--fit') ||
                     (document.getElementById('board') ? document.getElementById('board').style.transform : '');
    return {
      platformH: rect('#platform'), platTopH: rect('#plat-top'), boardH: rect('#board') || rect('.stage'),
      railH, srcBoxes, srcTiles,
      ucTiles: ucTiles.length,
      topbandH: rect('#topband'),
      overflow, fitScale
    };
  });
  console.log(JSON.stringify(m, null, 2));
  console.log('console errors:', errs.length ? errs.slice(0, 6) : 'none');
  await p.screenshot({ path: '/tmp/auto_shape.png', fullPage: false });
  await b.close();
})();
