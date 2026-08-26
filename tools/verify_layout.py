#!/usr/bin/env python3
"""Capture airlines Z board and assert layout void budgets before ship."""
import json, os, subprocess, sys, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from probe import run as probe_run

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
APP = os.path.join(ROOT, "app", "index.html")
OUT = os.path.join(ROOT, "docs", "verify-airlines-z.png")

LIMITS = {
  "fitH": 1700,
  "panelVoidBelowCols": 12,
  "mixedVoidBelow": 44,
  "ingestCardHMax": 72,
  "bodyBandGapMax": 8,
}

def shoot():
    html = open(APP, encoding="utf-8").read()
    setup = ("applyIndustry('airlines', false); applyShape('z', false); fitBoard();"
             "document.querySelectorAll('.tip,.drawer.open').forEach(function(e){"
             "e.classList.remove('open')});")
    boot = ("<script>window.addEventListener('load',function(){setTimeout(function(){"
            + setup + "},400)});</script>\n</body>")
    tmp = tempfile.mkdtemp()
    page = os.path.join(tmp, "p.html")
    open(page, "w", encoding="utf-8").write(html.replace("</body>", boot, 1))
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=2", "--no-first-run",
         "--window-size=1728,1180", "--virtual-time-budget=12000",
         "--screenshot=" + OUT, "file://" + page],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    shutil.rmtree(tmp, ignore_errors=True)
    print("screenshot", OUT, os.path.getsize(OUT) if os.path.exists(OUT) else "FAIL")

if __name__ == "__main__":
    js = open(os.path.join(ROOT, "tools", "layout_void_probe.js"), encoding="utf-8").read()
    data = json.loads(probe_run(js, APP, "1728,1180"))
    fails = []
    if data["fitH"] > LIMITS["fitH"]:
        fails.append("fitH %d > %d" % (data["fitH"], LIMITS["fitH"]))
    if data["panelVoidBelowCols"] > LIMITS["panelVoidBelowCols"]:
        fails.append("panelVoidBelowCols %d" % data["panelVoidBelowCols"])
    if data["mixedVoidBelow"] > LIMITS["mixedVoidBelow"]:
        fails.append("mixedVoidBelow %d" % data["mixedVoidBelow"])
    for c in data["ingestCards"]:
        if c["h"] > LIMITS["ingestCardHMax"]:
            fails.append("ingest %s h=%d" % (c["n"], c["h"]))
    for b in data["bodyBands"]:
        if b["gapIn"] > LIMITS["bodyBandGapMax"]:
            fails.append("band %s gapIn=%d" % (b["id"], b["gapIn"]))
    print(json.dumps(data, indent=2))
    shoot()
    if fails:
        print("FAIL:", ", ".join(fails), file=sys.stderr)
        sys.exit(1)
    print("PASS layout verify")
