const { chromium } = require('playwright');
const inds = ['crypto_digital_assets','insurance_pandc','media_broadcasting','consumer_goods','health_insurance','clinical_trials','genomics_biotech','chemical_mfg','apparel_fashion','retail','wholesale_distribution','pharmaceuticals','life_insurance','food_beverage','diagnostics_labs'];
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  for (const ind of inds) {
    try {
      await page.goto('http://localhost:8021/app/index.html?industry=' + ind, { waitUntil: 'networkidle' });
      await page.waitForTimeout(600);
      await page.evaluate(() => { document.querySelectorAll('.tour-pop,.tour-catch,.tour-mask').forEach(e => e.remove()); });
      const marked = await page.$$eval('button.ctile', els => els.filter(e => e.querySelector('.accel-dot')).map(e => (e.querySelector('.ct-name')||{}).textContent));
      console.log(ind.padEnd(16), marked.length, '=>', marked.join(' | '));
    } catch (e) { console.log(ind.padEnd(16), 'ERR', e.message.split('\n')[0]); }
  }
  await browser.close();
})();
