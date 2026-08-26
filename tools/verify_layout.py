#!/usr/bin/env python3
"""Capture airlines Z export PNG (same path as Download) and assert layout budgets."""
import base64, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from probe import run as probe_run

OUT = os.path.join(ROOT, "docs", "verify-airlines-z-export.png")
EXPORT_JS = os.path.join(ROOT, "tools", "export_png_probe.js")
PROBE_JS = os.path.join(ROOT, "tools", "layout_void_probe.js")

LIMITS = {
  "fitH": 1650,
  "workBodyVoid": 8,
  "contentToFoot": 120,
  "armVoid": 8,
  "infraH": 220,
  "infraVoid": 12,
}

def export_png():
    raw = probe_run(open(EXPORT_JS, encoding="utf-8").read(), size="1728,1180", budget=180000)
    data = json.loads(raw)
    open(OUT, "wb").write(base64.b64decode(data["data"].split(",", 1)[1]))
    print("export_png", OUT, data["w"], data["h"], os.path.getsize(OUT))

if __name__ == "__main__":
    data = json.loads(probe_run(open(PROBE_JS, encoding="utf-8").read(), size="1728,1180"))
    fails = []
    for key, lim in LIMITS.items():
        if key not in data:
            fails.append("%s missing" % key)
        elif data[key] > lim:
            fails.append("%s %d > %d" % (key, data[key], lim))
    print(json.dumps(data, indent=2))
    export_png()
    if fails:
        print("FAIL:", ", ".join(fails), file=sys.stderr)
        sys.exit(1)
    print("PASS layout verify (export PNG, light mode)")
