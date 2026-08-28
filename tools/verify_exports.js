const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const FILE = "file://" + path.resolve(__dirname, "../app/index.html");
const OUT = "/tmp/arch_exports";
fs.rmSync(OUT, { recursive: true, force: true });
fs.mkdirSync(OUT, { recursive: true });

// industry id, cloud
const CASES = [
  ["public_sector", "aws"],
  ["public_sector", "azure"],
  ["public_sector", "gcp"],
  ["airlines", "aws"],
  ["banking", "azure"],
  ["retail", "gcp"],
  ["generic", "aws"],
];

function u8FromB64(b64) { return Buffer.from(b64, "base64"); }

// count "/Type /Page" (not /Pages) occurrences in a PDF buffer
function pdfPageCount(buf) {
  const s = buf.toString("latin1");
  const m = s.match(/\/Type\s*\/Page(?![s])/g);
  return m ? m.length : 0;
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 } });
  const errors = [];
  page.on("pageerror", e => errors.push(String(e)));
  page.on("console", m => { if (m.type() === "error") errors.push("console: " + m.text()); });

  const results = [];
  for (const [ind, cloud] of CASES) {
    const url = `${FILE}?industry=${ind}&cloud=${cloud}`;
    await page.goto(url, { waitUntil: "load" });
    await page.waitForTimeout(700);

    const summary = await page.evaluate(() => {
      const secs = deckSections().map(s => ({ key: s.key, kind: s.kind, title: s.title, n: (s.tiles || []).length }));
      return {
        industry: (typeof ARCH !== "undefined" && ARCH.industry) || null,
        cloud: (typeof ARCH !== "undefined" && ARCH.cloud && ARCH.cloud.provider) || null,
        label: (typeof deckIndustry === "function") ? deckIndustry() : null,
        secs,
        uc: (typeof useCaseTiles === "function") ? useCaseTiles().length : -1,
        genie: (typeof genieTiles === "function") ? genieTiles().length : -1,
        dash: (typeof dashboardTiles === "function") ? dashboardTiles().length : -1,
        apps: (typeof appTiles === "function") ? appTiles().length : -1,
      };
    });

    const pptxB64 = await page.evaluate(async () => {
      const blob = await exportPptx();
      const buf = new Uint8Array(await blob.arrayBuffer());
      let bin = ""; for (let i = 0; i < buf.length; i++) bin += String.fromCharCode(buf[i]);
      return btoa(bin);
    });
    const pdfB64 = await page.evaluate(async () => {
      const blob = await boardPdfBlob();
      if (!blob) return null;
      const buf = new Uint8Array(await blob.arrayBuffer());
      let bin = ""; for (let i = 0; i < buf.length; i++) bin += String.fromCharCode(buf[i]);
      return btoa(bin);
    });

    const tag = `${ind}_${cloud}`;
    const pptxPath = path.join(OUT, tag + ".pptx");
    const pdfPath = path.join(OUT, tag + ".pdf");
    fs.writeFileSync(pptxPath, u8FromB64(pptxB64));
    if (pdfB64) fs.writeFileSync(pdfPath, u8FromB64(pdfB64));

    // PPTX slide count + content grep (zipStore is stored, so text is greppable in unzip -p)
    const slideList = execSync(`unzip -l "${pptxPath}" | grep -c 'ppt/slides/slide'`).toString().trim();
    const slideXml = execSync(`unzip -p "${pptxPath}" "ppt/slides/slide*.xml" 2>/dev/null || true`).toString();
    const hasGenie = /Genie/i.test(slideXml);
    const hasDash = /Dashboard/i.test(slideXml);
    const hasApp = /\bApp/i.test(slideXml);
    // pull the first use case tile name to confirm it lands in the deck
    const firstUc = await page.evaluate(() => { const t = useCaseTiles()[0]; return t ? t.n : null; });
    const ucInDeck = firstUc ? slideXml.includes(firstUc.replace(/&/g, "&amp;").slice(0, 12)) : false;

    const pdfPages = pdfB64 ? pdfPageCount(u8FromB64(pdfB64)) : 0;

    results.push({ tag, ...summary, slides: Number(slideList), pptxHasGenie: hasGenie, pptxHasDash: hasDash, pptxHasApp: hasApp, firstUc, ucInDeck, pdfPages, pptxBytes: u8FromB64(pptxB64).length, pdfBytes: pdfB64 ? u8FromB64(pdfB64).length : 0 });
  }

  await browser.close();

  console.log("\n================ EXPORT VERIFICATION ================\n");
  let fail = 0;
  for (const r of results) {
    const secLine = r.secs.map(s => `${s.key}:${s.n}`).join("  ");
    // expected content-page count in deck: uc tiles + genie tiles + 1(dash grid if dash) + 1(app grid if app) + breaks + cover + index + board
    const hasUc = r.uc > 0, hasGenieS = r.genie > 0, hasDashS = r.dash > 0, hasAppS = r.apps > 0;
    // narrative slides = per-section break(1) + pages; board is its own; cover+index
    let narr = 0, breaks = 0;
    r.secs.forEach(s => {
      if (s.kind === "board") return;
      breaks += 1;
      if (s.kind === "uc" || s.kind === "genie" || s.kind === "dash") narr += s.n; else narr += 1; // apps grid = 1
    });
    const expSlides = 1 /*cover*/ + 1 /*index*/ + 1 /*board*/ + breaks + narr + 1 /*closing*/;

    const checks = [];
    checks.push(["uc>0", hasUc]);
    checks.push(["ucInDeck", r.ucInDeck]);
    checks.push(["genie>0", hasGenieS]);
    checks.push(["dash>0", hasDashS]);
    checks.push(["apps>0", hasAppS]);
    checks.push(["pptx has Genie", r.pptxHasGenie]);
    checks.push(["pptx has Dashboard", r.pptxHasDash]);
    checks.push(["slides==exp(" + expSlides + ")", r.slides === expSlides]);
    checks.push(["pdf pages==exp(" + expSlides + ")", r.pdfPages === expSlides]);

    const bad = checks.filter(c => !c[1]);
    if (bad.length) fail++;
    console.log(`● ${r.tag}  [${r.label}]  ${bad.length ? "❌" : "✅"}`);
    console.log(`   secs: ${secLine}`);
    console.log(`   uc=${r.uc} genie=${r.genie} dash=${r.dash} apps=${r.apps}  slides=${r.slides}(exp ${expSlides})  pdfPages=${r.pdfPages}  pptx=${(r.pptxBytes/1024).toFixed(0)}KB pdf=${(r.pdfBytes/1024).toFixed(0)}KB`);
    console.log(`   firstUc=${JSON.stringify(r.firstUc)} inDeck=${r.ucInDeck}`);
    if (bad.length) console.log("   FAILS: " + bad.map(b => b[0]).join(", "));
  }
  console.log("\nPage errors captured: " + errors.length);
  errors.slice(0, 10).forEach(e => console.log("   ! " + e));
  console.log(`\nRESULT: ${results.length - fail}/${results.length} cases passed`);
  console.log("Artifacts in " + OUT);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
