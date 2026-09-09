#!/usr/bin/env python3
"""Fail if any industry board is taller than the standard reference architecture.

The board is fitted to the viewport by whichever of width or height binds first,
and every board here is height-bound. The two corner pockets (People, External
Ingestion) are single narrow columns, and the platform block beside a
pocket grows to whatever height the pocket needs. So a pocket row added by an
industry is paid for by every label on the diagram: the airlines pocket at four
groups and thirteen tiles took the board from 1126 design px to 1677 and the
fitted scale from 0.819 to 0.550, shrinking all text by a third.

Height is therefore a budget, not an outcome, and this is the gate on it. Run it
after editing INDUSTRIES; it drives a real browser because the numbers come from
layout, not from counting tiles in the source.

    python3 tools/heightgate.py [--tolerance 8] [--app app/index.html]

Exits non-zero when any industry exceeds the reference height by more than the
tolerance, so it can be chained with && in a release step.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from html import unescape

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

DRIVER = r"""
(function(){
  function measure(){
    if(typeof fitBoard === "function") fitBoard();
    document.body.getBoundingClientRect();
    var board = document.getElementById("board");
    var dw = parseFloat(getComputedStyle(document.body).getPropertyValue("--designw"));
    var clip = 0, squeezed = 0, clipped = [];
    /* .rg-label is in this list because it is the one label on the board that
       cannot wrap: a group header is nowrap, so an over-long industry group name
       is silently cut rather than reflowed, and a clip check that skipped it
       passed "OPERATIONS & TECHNI" as clean. */
    document.querySelectorAll(".t-name,.p-name,.bl-name,.rg-label,.pcard .p-cap,.t-cap").forEach(function(n){
      if(n.scrollWidth > n.clientWidth + 1){
        clip++;
        if(clipped.length < 4) clipped.push(n.textContent.trim());
      }
      var lh = parseFloat(getComputedStyle(n).lineHeight) || 14;
      if(Math.round(n.getBoundingClientRect().height / lh) >= 3 &&
         n.textContent.trim().split(/\s+/).length <= 2) squeezed++;
    });
    return { h: board.offsetHeight,
             scale: Math.round(board.getBoundingClientRect().width / dw * 1000) / 1000,
             clip: clip, squeezed: squeezed, clipped: clipped };
  }
  /* Every shape, not just the one the board opens on. The pockets are half-width
     in h90, so a group name that fits the Z clips there; checking only the
     default shape passed "Industry Messaging" as clean. */
  var SHAPES = ["z", "s", "t", "rt", "h90"];
  var jobs = [];
  ["generic"].concat(Object.keys(INDUSTRIES)).forEach(function(id){
    SHAPES.forEach(function(sh){ jobs.push([id, sh]); });
  });
  var res = {}, i = 0;
  (function step(){
    if(i >= jobs.length){
      var pre = document.createElement("pre");
      pre.id = "GATE";
      pre.textContent = JSON.stringify(res);
      document.body.appendChild(pre);
      return;
    }
    var id = jobs[i][0], sh = jobs[i][1];
    applyIndustry(id, false);
    try { applyShape(sh, false); } catch(e){}
    setTimeout(function(){ res[id + "@" + sh] = measure(); i++; step(); }, 300);
  })();
})();
"""


def render(app_path):
    page_html = open(app_path, encoding="utf-8").read()
    inject = ("<script>window.addEventListener('load',function(){"
              + DRIVER + "});</script>\n</body>")
    page_html = page_html.replace("</body>", inject, 1)
    tmp = tempfile.mkdtemp()
    page = os.path.join(tmp, "gate.html")
    open(page, "w", encoding="utf-8").write(page_html)
    dom = os.path.join(tmp, "dom.html")
    profile = os.path.join(tmp, "profile")

    # Chrome streams --dump-dom to stdout and then keeps the process alive, so
    # waiting for it to exit is waiting forever. Watch the dump until it stops
    # growing, then kill it.
    with open(dom, "wb") as sink:
        proc = subprocess.Popen(
            [CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
             "--force-device-scale-factor=1", "--user-data-dir=" + profile,
             "--window-size=1728,1080", "--virtual-time-budget=120000",
             "--dump-dom", "file://" + page],
            stdout=sink, stderr=subprocess.DEVNULL)
        prev, stable = -1, 0
        for _ in range(240):
            time.sleep(0.5)
            size = os.path.getsize(dom)
            if size > 10000 and size == prev:
                stable += 1
                if stable >= 2:
                    break
            else:
                stable = 0
            prev = size
        proc.kill()
        proc.wait(timeout=20)

    text = open(dom, encoding="utf-8", errors="replace").read()
    shutil.rmtree(tmp, ignore_errors=True)
    m = re.search(r'<pre id="GATE"[^>]*>(.*?)</pre>', text, re.S)
    if not m:
        sys.exit("gate driver produced no output (dom bytes: %d)" % len(text))
    return json.loads(unescape(m.group(1)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default="app/index.html")
    # 32px sits between the two things this gate has to tell apart. A row added to
    # a corner pocket costs ~45px and is the regression worth failing on, because
    # the platform block beside the pocket grows to match it. A top band carrying
    # more industry tiles legitimately measures up to ~25px taller in h90, where
    # its tiles are narrow enough for a sublabel to take a second line, and that
    # is content, not a layout fault. Verified: airlines fails at 8 on the top
    # band alone, and still fails at 32 with one pocket tile added.
    ap.add_argument("--tolerance", type=int, default=32,
                    help="design px an industry may exceed the reference by; "
                         "under one pocket row, over a top-band content difference")
    args = ap.parse_args()

    res = render(args.app)
    # The reference board is the budget, per shape: a shape legitimately has its
    # own height, so comparing an industry in h90 against the reference in z
    # would convict the shape rather than the industry.
    ref = {k.split("@")[1]: v for k, v in res.items() if k.startswith("generic@")}
    for key in [k for k in res if k.startswith("generic@")]:
        shape = key.split("@")[1]
        r = res.pop(key)
        print("reference@%-4s h=%-5d scale=%.3f  clip=%-3d squeezed=%-3d %s"
              % (shape, r["h"], r["scale"], r["clip"], r["squeezed"],
                 r["clipped"] or ""))

    bad = []
    for name in sorted(res):
        r = res[name]
        shape = name.split("@")[1]
        over = r["h"] - ref[shape]["h"]
        fail = over > args.tolerance or r["clip"] or r["squeezed"]
        print("%-18s h=%-5d %+5d  scale=%.3f  clip=%-3d squeezed=%-3d  %-4s %s"
              % (name, r["h"], over, r["scale"], r["clip"], r["squeezed"],
                 "FAIL" if fail else "ok", r["clipped"] or ""))
        if fail:
            bad.append(name)

    if bad:
        print("\nFAIL: " + ", ".join(bad))
        print("An industry may not outgrow the reference board. Consolidate the "
              "People and Ingestion pockets: fold roles into a tile's detail text "
              "rather than giving each one a row.")
        return 1
    print("\nPASS: every industry fits the reference height.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
