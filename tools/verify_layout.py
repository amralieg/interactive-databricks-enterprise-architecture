#!/usr/bin/env python3
"""Capture airlines Z in LIGHT mode and assert layout void budgets before ship."""
import json, os, subprocess, sys, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from probe import run as probe_run

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
APP = os.path.join(ROOT, "app", "index.html")
OUT = os.path.join(ROOT, "docs", "verify-airlines-z-light.png")

LIMITS = {
  "fitH": 1650,
  "contentToFoot": 24,
  "armVoid": 8,
  "infraH": 220,
  "infraVoid": 12,
}

def shoot():
    html = open(APP, encoding="utf-8").read()
    setup = ("document.body.classList.remove('theme-dark');"
             "applyIndustry('airlines', false); applyShape('z', false); fitBoard();"
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
    if data["contentToFoot"] > LIMITS["contentToFoot"]:
        fails.append("contentToFoot %d > %d" % (data["contentToFoot"], LIMITS["contentToFoot"]))
    if data["armVoid"] > LIMITS["armVoid"]:
        fails.append("armVoid %d > %d" % (data["armVoid"], LIMITS["armVoid"]))
    if data["infraH"] > LIMITS["infraH"]:
        fails.append("infraH %d > %d" % (data["infraH"], LIMITS["infraH"]))
    if data["infraVoid"] > LIMITS["infraVoid"]:
        fails.append("infraVoid %d > %d" % (data["infraVoid"], LIMITS["infraVoid"]))
    print(json.dumps(data, indent=2))
    shoot()
    if fails:
        print("FAIL:", ", ".join(fails), file=sys.stderr)
        sys.exit(1)
    print("PASS layout verify (light mode)")
