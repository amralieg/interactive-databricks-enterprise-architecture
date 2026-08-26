#!/usr/bin/env python3
"""Regenerate the README screenshots from app/index.html.

Each shot injects a little setup JS, waits for the board to settle, then asks
Chrome for a full-page capture. Chrome is run the same way probe.py runs it,
since --screenshot on its own occasionally returns before the board has fitted.
"""
import os, shutil, subprocess, sys, tempfile, time

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "app", "index.html")
DOCS = os.path.join(ROOT, "docs")

SETTLE = ("document.querySelectorAll('.tip,.drawer.open,#shape-menu.open')"
          ".forEach(function(e){e.classList.remove('open')});")

SHOTS = {
    "screenshot-light": "document.body.classList.remove('theme-dark');",
    "screenshot-dark": "document.body.classList.add('theme-dark');",
    "screenshot-h90": ("document.body.classList.remove('theme-dark');"
                       "applyShape('h90', false);"),
    "screenshot-detail": ("document.body.classList.remove('theme-dark');"
                          "openDetail(nameIndex['Unity Catalog']);"),
}


def shoot(name, setup, size="1728,1180"):
    html = open(APP, encoding="utf-8").read()
    boot = ("<script>window.addEventListener('load',function(){setTimeout(function(){"
            + setup + SETTLE + "},250)});</script>\n</body>")
    tmp = tempfile.mkdtemp()
    page = os.path.join(tmp, "p.html")
    open(page, "w", encoding="utf-8").write(html.replace("</body>", boot, 1))
    out = os.path.join(DOCS, name + ".png")
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=2", "--no-first-run",
         "--window-size=" + size, "--virtual-time-budget=12000",
         "--screenshot=" + out, "file://" + page],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    shutil.rmtree(tmp, ignore_errors=True)
    print(name, os.path.getsize(out) if os.path.exists(out) else "FAILED")


def pal(k):
    return ("document.body.classList.remove('theme-dark');"
            "document.body.className=document.body.className"
            ".replace(/\\bpal-[a-z]+\\b/g,'').trim();"
            + ("document.body.classList.add('pal-%s');" % k if k else ""))


"""The two montages tile board-only captures, so one image can show five shapes
or six palettes without six README figures. The toolbar is hidden in each cell:
repeated five times it reads as chrome, and hiding it lets the whitespace trim
land on the board itself."""
NO_BAR = ("var h=document.querySelector('header.top'); if(h) h.style.display='none';"
          "fitBoard();")
MONTAGES = {
    "screenshot-shapes": {
        "cols": 3,
        "cells": [(k, "document.body.classList.remove('theme-dark');"
                      "applyShape('%s', false);" % k)
                  for k in ("z", "s", "t", "rt", "h90")],
    },
    "screenshot-palettes": {
        "cols": 3,
        "cells": [(k or "spectrum", pal(k))
                  for k in ("", "mono", "nordic", "ocean", "jewel", "neon")],
    },
}


def montage(name, spec, size="1500,1000"):
    from PIL import Image
    tmp = tempfile.mkdtemp()
    tiles = []
    for key, setup in spec["cells"]:
        p = os.path.join(tmp, key + ".png")
        html = open(APP, encoding="utf-8").read()
        boot = ("<script>window.addEventListener('load',function(){setTimeout("
                "function(){" + setup + SETTLE + NO_BAR + "},250)});</script>\n</body>")
        page = os.path.join(tmp, key + ".html")
        open(page, "w", encoding="utf-8").write(html.replace("</body>", boot, 1))
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             "--force-device-scale-factor=1", "--no-first-run",
             "--window-size=" + size, "--virtual-time-budget=12000",
             "--screenshot=" + p, "file://" + page],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
        im = Image.open(p).convert("RGB")
        bg = im.getpixel((4, im.height - 4))
        tiles.append(im.crop(im.getbbox() or (0, 0, im.width, im.height)))
        tiles[-1].bg = bg
    cols = spec["cols"]
    rows = (len(tiles) + cols - 1) // cols
    cw = max(t.width for t in tiles)
    ch = max(t.height for t in tiles)
    gap = 18
    sheet = Image.new("RGB", (cols * cw + gap * (cols + 1),
                              rows * ch + gap * (rows + 1)), tiles[0].bg)
    for i, t in enumerate(tiles):
        x = gap + (i % cols) * (cw + gap) + (cw - t.width) // 2
        y = gap + (i // cols) * (ch + gap) + (ch - t.height) // 2
        sheet.paste(t, (x, y))
    out = os.path.join(DOCS, name + ".png")
    sheet.save(out, optimize=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print(name, os.path.getsize(out))


if __name__ == "__main__":
    want = sys.argv[1:] or list(SHOTS) + list(MONTAGES)
    for n in want:
        if n in SHOTS:
            shoot(n, SHOTS[n])
        elif n in MONTAGES:
            montage(n, MONTAGES[n])
        else:
            sys.exit("unknown shot %r, have: %s"
                     % (n, ", ".join(list(SHOTS) + list(MONTAGES))))
