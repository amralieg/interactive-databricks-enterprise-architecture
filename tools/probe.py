#!/usr/bin/env python3
"""Run a JS probe against app/index.html in headless Chrome and print what it
writes into <pre id="OUT">. Chrome's --dump-dom never closes the stream on its
own here, so the DOM is piped to a file and the process is killed once the file
size stops growing."""
import os, re, shutil, subprocess, sys, tempfile, time
from html import unescape

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "app", "index.html")


def run(js, app=APP, size="1728,1080", budget=120000):
    page_html = open(app, encoding="utf-8").read()
    inject = ("<script>window.addEventListener('load',function(){" + js
              + "});</script>\n</body>")
    page_html = page_html.replace("</body>", inject, 1)
    tmp = tempfile.mkdtemp()
    page = os.path.join(tmp, "p.html")
    open(page, "w", encoding="utf-8").write(page_html)
    dom = os.path.join(tmp, "dom.html")
    with open(dom, "wb") as sink:
        proc = subprocess.Popen(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             "--force-device-scale-factor=1", "--no-first-run",
             "--user-data-dir=" + os.path.join(tmp, "prof"),
             "--window-size=" + size, "--virtual-time-budget=%d" % budget,
             "--dump-dom", "file://" + page],
            stdout=sink, stderr=subprocess.DEVNULL)
        prev, stable = -1, 0
        for _ in range(300):
            time.sleep(0.5)
            s = os.path.getsize(dom)
            if s > 10000 and s == prev:
                stable += 1
                if stable >= 2:
                    break
            else:
                stable = 0
            prev = s
        proc.kill()
        proc.wait(timeout=20)
    text = open(dom, encoding="utf-8", errors="replace").read()
    shutil.rmtree(tmp, ignore_errors=True)
    m = re.search(r'<pre id="OUT"[^>]*>(.*?)</pre>', text, re.S)
    if not m:
        sys.exit("probe produced no output (dom bytes: %d)" % len(text))
    return unescape(m.group(1))


if __name__ == "__main__":
    print(run(open(sys.argv[1], encoding="utf-8").read(),
              sys.argv[2] if len(sys.argv) > 2 else APP))
