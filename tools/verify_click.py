#!/usr/bin/env python3
"""Browser gate for the click-experience layer.

Drives the real board resolver, so it convicts exactly what a user would see:
for every industry it applies the board and checks that each use-case tile's
beneficiary (`who`) and architecture components (`comps`) resolve to real atoms,
that each team tile's driven use cases (`ucs`) resolve, and that Use Cases are
ordered stories-first. It also asserts the airlines reference renders all the new
drawer sections, because airlines is the template the 39 are authored against.

    python3 tools/verify_click.py            # audit every industry
    python3 tools/verify_click.py --json     # dump the raw report
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from html import unescape

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "app", "index.html")

DRIVER = r"""
<script>
window.addEventListener('load', function(){
  setTimeout(function(){
    var out = { industries: {}, airlines_render: {} };
    try {
      var cat = INDUSTRY_CATALOG.map(function(x){ return x[0]; });
      cat.forEach(function(iid){
        applyIndustry(iid, false);
        var rep = { who: [], comp: [], uc: [], order: true, stories: [] };
        var ucSec = (ARCH.top.secs || []).find(function(s){ return s.title === 'Use Cases'; });
        var tiles = ucSec ? ucSec.tiles : [];
        var flags = tiles.map(function(t){ return (t.stories && t.stories.length) ? 1 : 0; });
        for (var i = 1; i < flags.length; i++){ if (flags[i-1] < flags[i]){ rep.order = false; break; } }
        tiles.forEach(function(t){
          if (t.who && !resolveAtom(t.who)) rep.who.push(t.n + ' -> ' + t.who);
          (t.comps || []).forEach(function(c){ if (!resolveAtom(c)) rep.comp.push(t.n + ' -> ' + c); });
          (t.stories || []).forEach(function(s){ rep.stories.push(s.u); });
        });
        var pplRail = ARCH.rails && ARCH.rails.ppl;
        var ppl = pplRail ? (Array.isArray(pplRail) ? pplRail : (pplRail.groups || [])) : [];
        ppl.forEach(function(g){ (g.tiles || []).forEach(function(t){
          (t.ucs || []).forEach(function(u){ if (!nameIndex[u]) rep.uc.push(t.n + ' -> ' + u); });
        }); });
        out.industries[iid] = rep;
      });

      // airlines drawer render assertions
      applyIndustry('airlines', false);
      function body(name){ var id = nameIndex[name]; if (!id) return ''; openDetail(id); return document.getElementById('d-body').innerHTML; }
      out.airlines_render = {
        uc: body('IROPS Recovery'),
        uc_nostory: body('Cargo Yield'),
        team_biz: body('Operations Control'),
        team_tech: body('Data Engineers')
      };
    } catch (e){ out.error = String(e && e.stack || e); }
    var pre = document.createElement('pre');
    pre.id = 'RESULT';
    pre.textContent = JSON.stringify(out);
    document.body.appendChild(pre);
  }, 500);
});
</script>
</body>
"""


def run():
    html = open(APP, encoding="utf-8").read().replace("</body>", DRIVER, 1)
    tmp = tempfile.mkdtemp()
    page = os.path.join(tmp, "p.html")
    dom = os.path.join(tmp, "dom.html")
    profile = os.path.join(tmp, "profile")
    open(page, "w", encoding="utf-8").write(html)
    with open(dom, "wb") as sink:
        proc = subprocess.Popen(
            [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
             "--user-data-dir=" + profile, "--window-size=1728,1080",
             "--virtual-time-budget=180000", "--dump-dom", "file://" + page],
            stdout=sink, stderr=subprocess.DEVNULL)
        prev, stable = -1, 0
        for _ in range(240):
            time.sleep(0.5)
            size = os.path.getsize(dom)
            if size > 10000 and size == prev:
                stable += 1
                if stable >= 3:
                    break
            else:
                stable = 0
            prev = size
        proc.kill()
        proc.wait(timeout=20)
    text = open(dom, encoding="utf-8", errors="replace").read()
    shutil.rmtree(tmp, ignore_errors=True)
    m = re.search(r'<pre id="RESULT">(.*?)</pre>', text, re.S)
    if not m:
        raise SystemExit("no RESULT produced (dom bytes: %d)" % len(text))
    return json.loads(unescape(m.group(1)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    r = run()
    if args.json:
        print(json.dumps(r, indent=2))
        return 0
    if r.get("error"):
        raise SystemExit("driver error: " + r["error"])

    problems = []
    inds = r["industries"]
    authored = 0
    for iid in sorted(inds):
        rep = inds[iid]
        touched = rep["who"] or rep["comp"] or rep["uc"] or rep["stories"]
        for w in rep["who"]:
            problems.append(f"{iid}: unresolved beneficiary  {w}")
        for c in rep["comp"]:
            problems.append(f"{iid}: unresolved component    {c}")
        for u in rep["uc"]:
            problems.append(f"{iid}: unresolved team use-case {u}")
        if not rep["order"]:
            problems.append(f"{iid}: Use Cases not ordered stories-first")
        if rep["stories"]:
            authored += 1

    # airlines reference must render every section
    ar = r["airlines_render"]
    for h in ["The problem it solves", "Who benefits", "How it is built",
              "Architecture it uses", "Databricks customer stories"]:
        if h not in ar.get("uc", ""):
            problems.append(f"airlines drawer: use-case missing section {h!r}")
    if "databricks.com" not in ar.get("uc", ""):
        problems.append("airlines drawer: use-case has no databricks.com story link")
    if "Databricks customer stories" in ar.get("uc_nostory", ""):
        problems.append("airlines drawer: story-less use case should show no stories section")
    for h in ["Who is in this team", "Use cases they drive"]:
        if h not in ar.get("team_biz", ""):
            problems.append(f"airlines drawer: business team missing section {h!r}")
        if h not in ar.get("team_tech", ""):
            problems.append(f"airlines drawer: technical team missing section {h!r}")

    print(f"industries audited: {len(inds)}   with stories authored: {authored}/{len(inds)}")
    if problems:
        print("\nFAIL:")
        for p in problems:
            print("  - " + p)
        return 1
    print("PASS: every authored ref resolves, ordering is stories-first, airlines renders.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
