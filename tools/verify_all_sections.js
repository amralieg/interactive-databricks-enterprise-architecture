const { chromium } = require("playwright");
const path = require("path");
const FILE = "file://" + path.resolve(__dirname, "../app/index.html");
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  const errs = [];
  page.on("pageerror", e => errs.push(String(e)));
  await page.goto(FILE, { waitUntil: "load" });
  const ids = await page.evaluate(() => ["generic"].concat(Object.keys(INDUSTRIES)));
  const rows = [];
  for (const id of ids) {
    await page.evaluate((i) => { i === "generic" ? build() : applyIndustry(i, false); }, id);
    const r = await page.evaluate(() => {
      const s = deckSections();
      const by = k => { const x = s.find(z => z.kind === k); return x ? x.tiles.length : 0; };
      return { ind: ARCH.industry, sec: s.map(z => z.kind).join(","), uc: by("uc"), genie: by("genie"), dash: by("dash"), app: by("app") };
    });
    rows.push({ id, ...r });
  }
  await browser.close();
  let bad = 0;
  const short = rows.filter(r => !(r.uc >= 1 && r.genie >= 1 && r.dash >= 1 && r.app >= 1));
  rows.forEach(r => { if (!(r.uc && r.genie && r.dash && r.app)) bad++; });
  console.log(`industries scanned: ${rows.length}`);
  console.log(`missing a section (uc/genie/dash/app==0): ${short.length}`);
  short.slice(0, 30).forEach(r => console.log(`  ❌ ${r.id}  uc=${r.uc} genie=${r.genie} dash=${r.dash} app=${r.app}  [${r.sec}]`));
  // distribution of counts
  const dist = {};
  rows.forEach(r => { const k = `${r.uc}/${r.genie}/${r.dash}/${r.app}`; dist[k] = (dist[k] || 0) + 1; });
  console.log("count distribution uc/genie/dash/app -> #industries:");
  Object.entries(dist).sort((a, b) => b[1] - a[1]).forEach(([k, v]) => console.log(`  ${k}: ${v}`));
  console.log("page errors:", errs.length);
  errs.slice(0, 5).forEach(e => console.log("  ! " + e));
  process.exit(short.length || errs.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
