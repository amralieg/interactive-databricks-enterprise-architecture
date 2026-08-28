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

  const violations = [];       // category mode: commercial name leaked into an export chip
  const proseViolations = [];  // category mode: commercial name leaked into an export sentence
  let commercialUniverse = 0;
  let industriesWithMapping = 0;

  for (const id of ids) {
    await page.evaluate((i) => { i === "generic" ? build() : applyIndustry(i, false); }, id);

    const r = await page.evaluate(() => {
      // Authoritative commercial->category map from the RAW industry definition,
      // independent of what renders. Any tile with a `cat` is a commercial product
      // that MUST relabel to its category in Categorical mode.
      const comm2cat = {};
      ["src", "ing", "ppl", "cons"].forEach(k => {
        const rail = ARCH.rails[k];
        (rail && rail.groups ? rail.groups : []).forEach(g => {
          (g.tiles || []).forEach(t => { if (t && t.cat) comm2cat[t.n] = t.cat; });
        });
      });

      const gatherChips = () => {
        const out = [];
        deckSections().forEach(sec => (sec.tiles || []).forEach(t => {
          (t.comps || []).forEach(x => out.push(x));
          (t.feeds || []).forEach(x => out.push(x));
        }));
        return out;
      };
      const gatherProse = () => {
        const out = [];
        deckSections().forEach(sec => (sec.tiles || []).forEach(t => {
          ["long", "what", "problem", "how", "users"].forEach(k => { if (t[k]) out.push(t[k]); });
          (t.questions || []).forEach(q => out.push(q));
        }));
        return out;
      };

      displayMode = "category";
      const cat = gatherChips();
      // A chip is a leak iff it is still a commercial name that owns a category.
      const leaked = Array.from(new Set(cat.filter(x => !!comm2cat[x])));
      // Prose leak: a commercial name that owns a category still appears verbatim
      // in a relabelled sentence.
      const prose = gatherProse().join(" \u0001 ");
      // Skip names whose OWN category label embeds them (e.g. "Core Ledger" ->
      // "Core Ledger / Accounting System"): a substring test cannot tell the
      // replaced-and-embedded case from an un-replaced one, and the former is correct.
      const proseLeaked = Object.keys(comm2cat).filter(name => !comm2cat[name].includes(name) && prose.includes(name));
      return { ind: ARCH.industry, universe: Object.keys(comm2cat).length, leaked, proseLeaked };
    });

    if (r.universe > 0) industriesWithMapping++;
    commercialUniverse += r.universe;
    if (r.leaked.length) violations.push({ id, ind: r.ind, leaked: r.leaked });
    if (r.proseLeaked.length) proseViolations.push({ id, ind: r.ind, leaked: r.proseLeaked });
  }

  await browser.close();

  console.log(`industries scanned: ${ids.length}`);
  console.log(`industries with commercial products (own a category): ${industriesWithMapping}`);
  console.log(`total commercial products across all industries: ${commercialUniverse}`);
  console.log(`category-mode export CHIPS still showing a commercial name: ${violations.length} industries`);
  violations.slice(0, 60).forEach(v => console.log(`  ❌ ${v.id} (${v.ind}): ${v.leaked.join(" | ")}`));
  console.log(`category-mode export PROSE still showing a commercial name: ${proseViolations.length} industries`);
  proseViolations.slice(0, 60).forEach(v => console.log(`  ❌ ${v.id} (${v.ind}): ${v.leaked.join(" | ")}`));
  console.log("page errors:", errs.length);
  errs.slice(0, 5).forEach(e => console.log("  ! " + e));

  process.exit(violations.length || proseViolations.length || errs.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
