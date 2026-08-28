const { chromium } = require("playwright");
const path = require("path");
const FILE = "file://" + path.resolve(__dirname, "../app/index.html");
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  const errs = [];
  page.on("pageerror", e => errs.push(String(e)));
  await page.goto(FILE, { waitUntil: "load" });

  const clouds = ["azure", "aws", "gcp"];
  const missing = [];
  for (const cp of clouds) {
    const r = await page.evaluate((cloud) => {
      ARCH.cloud.provider = cloud;
      build();
      const bad = [];
      Object.values(byId).forEach(rec => {
        if (rec.section !== "Sources") return;
        const t = rec.tile;
        const gaps = [];
        if (!t.what) gaps.push("what");
        if (!t.users) gaps.push("users");
        if (!t.dataOut) gaps.push("dataOut");
        if (gaps.length) bad.push(t.n + " [" + gaps.join(",") + "]");
      });
      const total = Object.values(byId).filter(r => r.section === "Sources").length;
      return { total, bad };
    }, cp);
    console.log(`cloud=${cp}: source tiles=${r.total}, unenriched=${r.bad.length}`);
    r.bad.forEach(x => { console.log("   ❌ " + x); missing.push(cp + ": " + x); });
  }
  await browser.close();
  console.log("page errors:", errs.length);
  errs.slice(0, 5).forEach(e => console.log("  ! " + e));
  process.exit(missing.length || errs.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
