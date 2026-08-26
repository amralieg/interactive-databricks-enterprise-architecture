#!/usr/bin/env python3
"""Export PNG from LIVE GitHub Pages HTML (same boardPngBlob(2) as Download)."""
import base64, json, os, re, shutil, subprocess, sys, tempfile, time
from html import unescape

import urllib.request

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LIVE = "https://amralieg.github.io/interactive-databricks-enterprise-architecture/app/index.html"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "docs", "verify-pages-live-download.png")

JS = """
document.body.classList.remove('theme-dark');
applyIndustry('airlines', false);
applyShape('z', false);
fitBoard();
boardPngBlob(2).then(function(r){
  return new Promise(function(res){
    var fr = new FileReader();
    fr.onload = function(){ res(JSON.stringify({w:r.w,h:r.h,data:fr.result})); };
    fr.readAsDataURL(r.blob);
  });
}).then(function(s){
  document.body.innerHTML = '<pre id="OUT">' + s + '</pre>';
});
"""

def main():
    url = LIVE + "?industry=airlines&shape=z&theme=light"
    html = urllib.request.urlopen(url, timeout=60).read().decode("utf-8")
    inject = "<script>window.addEventListener('load',function(){setTimeout(function(){" + JS + "},800)});</script>\n</body>"
    page_html = html.replace("</body>", inject, 1)
    tmp = tempfile.mkdtemp()
    page = os.path.join(tmp, "live.html")
    dom = os.path.join(tmp, "dom.html")
    open(page, "w", encoding="utf-8").write(page_html)
    with open(dom, "wb") as sink:
        proc = subprocess.Popen(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             "--force-device-scale-factor=1", "--no-first-run",
             "--user-data-dir=" + os.path.join(tmp, "prof"),
             "--window-size=1728,1180", "--virtual-time-budget=180000",
             "--dump-dom", "file://" + page],
            stdout=sink, stderr=subprocess.DEVNULL)
        prev, stable = -1, 0
        for _ in range(360):
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
        sys.exit("export failed (dom %d bytes)" % len(text))
    data = json.loads(unescape(m.group(1)))
    open(OUT, "wb").write(base64.b64decode(data["data"].split(",", 1)[1]))
    print(json.dumps({"path": OUT, "w": data["w"], "h": data["h"],
                      "bytes": os.path.getsize(OUT), "source": url}, indent=2))

if __name__ == "__main__":
    main()
