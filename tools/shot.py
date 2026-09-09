#!/usr/bin/env python3
"""Regenerate the README screenshots from app/index.html.

Each shot injects a little setup JS, waits for the board to settle, then asks
Chrome for a full-page capture. Chrome is run the same way probe.py runs it,
since --screenshot on its own occasionally returns before the board has fitted.

The board lazy-loads its industry descriptors, reference JSON and translations
over fetch(), which browsers block on file://, so the app folder is served over
a local http server for the duration of the run and Chrome loads the temp page
from inside it, where those relative fetches resolve.
"""
import glob, os, shutil, subprocess, sys, tempfile, threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(ROOT, "app")
APP = os.path.join(APP_DIR, "index.html")
DOCS = os.path.join(ROOT, "docs")

SETTLE = ("document.querySelectorAll('.tip,.drawer.open,#shape-menu.open')"
          ".forEach(function(e){e.classList.remove('open')});")

# The first-visit tour auto-starts when its localStorage key is unset, which a
# fresh temp page always is, so every capture would otherwise carry the tour
# popover. Set the key in <head> before the tour reads it on load.
HEAD = ("<head><script>try{localStorage.setItem('dbx-arch-tour-v1','1');}"
        "catch(e){}</script>")


def prep(html):
    return html.replace("<head>", HEAD, 1)


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def serve():
    """Serve app/ on an ephemeral local port so lazy-loaded descriptors,
    resources and translations resolve. Returns (httpd, port)."""
    httpd = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(_QuietHandler, directory=APP_DIR))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


# The board is built after its descriptors land, so a setup that touches
# nameIndex or the tiles has to wait for that rather than fire on load. Poll for
# a populated board, then run the setup, then the settle. Under Chrome's virtual
# time the poll pauses while fetches are pending, so it does not race the network.
def _boot(setup, extra=""):
    ready = "window.nameIndex&&Object.keys(window.nameIndex).length>10"
    return ("<script>window.addEventListener('load',function(){var n=0;"
            "var iv=setInterval(function(){n++;if((" + ready + ")||n>80){"
            "clearInterval(iv);try{" + setup + "}catch(e){}"
            "try{" + SETTLE + extra + "}catch(e){}}},100);});</script>\n</body>")


def _capture(boot, out, size, scale, port, budget=20000, src=APP, subdir=""):
    html = prep(open(src, encoding="utf-8").read()).replace("</body>", boot, 1)
    dest = os.path.join(APP_DIR, subdir) if subdir else APP_DIR
    fd, page = tempfile.mkstemp(prefix="_shot_", suffix=".html", dir=dest)
    os.write(fd, html.encode("utf-8"))
    os.close(fd)
    rel = (subdir + "/" if subdir else "") + os.path.basename(page)
    url = "http://127.0.0.1:%d/%s" % (port, rel)
    try:
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             "--force-device-scale-factor=" + scale, "--no-first-run",
             "--window-size=" + size, "--virtual-time-budget=" + str(budget),
             "--screenshot=" + out, url],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    finally:
        os.remove(page)


SHOTS = {
    "screenshot-light": "document.body.classList.remove('theme-dark');",
    "screenshot-dark": "document.body.classList.add('theme-dark');",
    "screenshot-h90": ("document.body.classList.remove('theme-dark');"
                       "applyShape('h90', false);"),
    "screenshot-detail": ("document.body.classList.remove('theme-dark');"
                          "openDetail(nameIndex['Unity Catalog']);"),
    "screenshot-source": ("document.body.classList.remove('theme-dark');"
                          "openDetail(nameIndex['Business Applications']);"),
    "screenshot-genie": ("document.body.classList.remove('theme-dark');"
                         "openDetail(nameIndex['Customer & Revenue Agent']);"),
    "screenshot-dashboard": ("document.body.classList.remove('theme-dark');"
                             "openDetail(nameIndex['Revenue & Growth']);"),
    "screenshot-language": ("document.body.classList.remove('theme-dark');"
                            "document.getElementById('lang-wrap').classList.add('open');"
                            "if(typeof syncLangMenu==='function')syncLangMenu();"),
    "screenshot-share": ("document.body.classList.remove('theme-dark');"
                         "if(typeof buildShareMenu==='function')buildShareMenu();"
                         "document.getElementById('share-wrap').classList.add('open');"),
}


def shoot(name, setup, port, size="1728,1180"):
    out = os.path.join(DOCS, name + ".png")
    _capture(_boot(setup), out, size, "2", port)
    print(name, os.path.getsize(out) if os.path.exists(out) else "FAILED")


# The assistant lives in app/ai/index.html as a docked panel over the board. Show
# it open with the status set to its normal connected appearance, the way it reads
# in a real deployment (the backend is not running during a capture).
AI_SETUP = ("var f=document.querySelector('.ai-fab');if(f)f.classList.add('hide');"
            "var p=document.querySelector('.ai-panel');if(p)p.classList.add('show');"
            "var d=document.querySelector('.ai-dot');if(d){d.classList.remove('busy');"
            "d.classList.add('on');}var c=document.querySelector('.ai-conn');"
            "if(c)c.textContent='Connected';")


def shoot_ai(name, port, size="1728,1180"):
    out = os.path.join(DOCS, name + ".png")
    _capture(_boot(AI_SETUP), out, size, "2", port,
             src=os.path.join(APP_DIR, "ai", "index.html"), subdir="ai")
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


def montage(name, spec, port, size="1500,1000"):
    from PIL import Image
    tmp = tempfile.mkdtemp()
    tiles = []
    for key, setup in spec["cells"]:
        p = os.path.join(tmp, key + ".png")
        _capture(_boot(setup, extra=NO_BAR), p, size, "1", port)
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
    for pat in ("_shot_*.html", os.path.join("ai", "_shot_*.html")):
        for stale in glob.glob(os.path.join(APP_DIR, pat)):
            os.remove(stale)
    want = sys.argv[1:] or list(SHOTS) + list(MONTAGES) + ["screenshot-ai"]
    httpd, port = serve()
    try:
        for n in want:
            if n in SHOTS:
                shoot(n, SHOTS[n], port)
            elif n in MONTAGES:
                montage(n, MONTAGES[n], port)
            elif n == "screenshot-ai":
                shoot_ai(n, port)
            else:
                sys.exit("unknown shot %r, have: %s"
                         % (n, ", ".join(list(SHOTS) + list(MONTAGES) + ["screenshot-ai"])))
    finally:
        httpd.shutdown()
