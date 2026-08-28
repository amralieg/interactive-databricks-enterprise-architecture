#!/usr/bin/env python3
"""Completeness + live-URL gate for every clickable entity in the board.

Dumps the app's in-memory ARCH / LINKS / INDUSTRIES via headless Chrome, then:
  * every Databricks product (a band tile whose LINKS entry has a `doc` path)
    must also carry `site` and `blog` (Bronze/Silver/Gold exempt from `site`,
    they are medallion concepts); the four late-added products must exist.
  * every generic Source tile must carry what / users / dataOut(+vol).
  * every industry use case must carry at least one customer story.
With --urls it HEAD-checks every outbound URL (YouTube via oEmbed) in parallel
and fails on any dead link. Exit non-zero on any failure so it gates a push.
"""
import argparse, concurrent.futures as cf, html as _html, json, os, re, subprocess, tempfile, urllib.request, urllib.error

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "app", "index.html")

# Medallion tiers are architecture concepts, not products with a landing page.
SITE_EXEMPT = {"Bronze", "Silver", "Gold"}
# Products added this pass that MUST have a full LINKS entry (doc/site/blog).
REQUIRED_PRODUCTS = ["Document Parsing", "Knowledge Assistant", "Text Classification", "Omnigent OSS"]
DOC_HOSTS = {"aws": "https://docs.databricks.com/aws/en/",
             "azure": "https://learn.microsoft.com/azure/databricks/",
             "gcp": "https://docs.databricks.com/gcp/en/"}
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36"

DUMP_JS = r"""
<script>
window.addEventListener('load', function(){ setTimeout(function(){
  function vol(t){ return t.dataOut && ((t.dataOut.batch&&t.dataOut.batch.vol)||(t.dataOut.stream&&t.dataOut.stream.vol)); }
  function srow(t){ return {n:t.n, what:!!t.what, users:!!t.users, dataOut:!!t.dataOut, vol:!!vol(t)}; }
  var out = { LINKS:{}, prodNames:[], genSrc:[], inds:{} };
  try { out.LINKS = (typeof LINKS!=='undefined') ? LINKS : {}; } catch(e){ out.links_error=String(e); }
  try {
    var seen={};
    (function walk(o){ if(!o||typeof o!=='object')return;
      if(typeof o.n==='string'){ seen[o.n]=1; }
      (Array.isArray(o)?o:Object.values(o)).forEach(walk); })(ARCH.bands);
    out.prodNames = Object.keys(seen);
  } catch(e){ out.prod_error=String(e); }
  try { (ARCH.rails.src.groups||[]).forEach(function(g){ (g.tiles||[]).forEach(function(t){ out.genSrc.push(srow(t)); }); }); } catch(e){ out.gen_error=String(e); }
  try {
    Object.keys(INDUSTRIES).forEach(function(id){
      var ind=INDUSTRIES[id], o={uc:[], src:[], cites:[]};
      ((ind.rails&&ind.rails.src)||[]).forEach(function(g){ (g.tiles||[]).forEach(function(t){ o.src.push(srow(t)); }); });
      (ind.top||[]).forEach(function(s){ if(/Business Use Cases|Use Cases/i.test(s.title)){ (s.tiles||[]).forEach(function(t){
        o.uc.push({n:t.n, stories:(t.stories||[]).map(function(x){return x.u;})}); }); } });
      var src=ind.sources||{}; Object.keys(src).forEach(function(k){ if(src[k]&&src[k].u) o.cites.push(src[k].u); });
      out.inds[id]=o;
    });
  } catch(e){ out.ind_error=String(e); }
  var el=document.createElement('script'); el.type='application/json'; el.id='GATEOUT';
  el.textContent = JSON.stringify(out);
  document.body.appendChild(el);
}, 600); });
</script>
</body>
"""


def dump():
    html = open(APP, encoding="utf-8").read().replace("</body>", DUMP_JS, 1)
    tmp = tempfile.mkdtemp()
    page = os.path.join(tmp, "p.html")
    open(page, "w", encoding="utf-8").write(html)
    res = subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
         "--virtual-time-budget=16000", "--dump-dom", "file://" + page],
        capture_output=True, text=True, timeout=180)
    m = re.search(r'id="GATEOUT"[^>]*>(.*?)</script>', res.stdout, re.S)
    import shutil; shutil.rmtree(tmp, ignore_errors=True)
    if not m:
        raise SystemExit("dump failed; chrome stderr tail:\n" + res.stderr[-800:])
    return json.loads(_html.unescape(m.group(1)))


def collect_urls(d):
    """Every outbound URL a click can reach, tagged with where it came from."""
    urls = {}
    def add(u, where):
        if u and isinstance(u, str) and u.startswith("http"):
            urls.setdefault(u, set()).add(where)
    LINKS = d["LINKS"]
    for name, L in LINKS.items():
        if not isinstance(L, dict):
            continue
        if L.get("doc"):
            for cl, hostp in DOC_HOSTS.items():
                add(hostp + str(L["doc"]).lstrip("/"), f"LINKS[{name}].doc/{cl}")
        if L.get("dbx"):
            add(DOC_HOSTS["aws"] + str(L["dbx"]).lstrip("/"), f"LINKS[{name}].dbx")
        for k in ("site", "blog", "url", "video"):
            if L.get(k):
                add(L[k], f"LINKS[{name}].{k}")
        for pair in (L.get("also") or []):
            if isinstance(pair, list) and len(pair) == 2:
                add(pair[1], f"LINKS[{name}].also")
    for iid, o in d["inds"].items():
        for uc in o["uc"]:
            for u in uc["stories"]:
                add(u, f"{iid}:uc:{uc['n']}")
        for u in o["cites"]:
            add(u, f"{iid}:cite")
    return urls


def check_url(u):
    """Return (ok, code). YouTube via oEmbed existence check; others HEAD->GET."""
    try:
        if "youtube.com/watch" in u or "youtu.be/" in u:
            oe = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(u, safe="")
            req = urllib.request.Request(oe, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=20) as r:
                return (r.status == 200, r.status)
        for method in ("HEAD", "GET"):
            req = urllib.request.Request(u, method=method, headers={"User-Agent": UA})
            try:
                with urllib.request.urlopen(req, timeout=25) as r:
                    return (200 <= r.status < 400, r.status)
            except urllib.error.HTTPError as e:
                if e.code in (403, 405, 429) and method == "HEAD":
                    continue  # some hosts block HEAD; retry GET
                return (e.code in (403, 429), e.code)  # 403/429 = bot-blocked, treat as WARN-ok
        return (False, 0)
    except Exception as e:
        return (False, str(e)[:60])


import urllib.parse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", action="store_true", help="live-check every outbound URL")
    args = ap.parse_args()
    d = dump()
    fails = []

    # ---- Products ----
    LINKS = d["LINKS"]
    prod = [n for n in d["prodNames"] if isinstance(LINKS.get(n), dict) and LINKS[n].get("doc")]
    for n in prod:
        L = LINKS[n]
        if n not in SITE_EXEMPT and not L.get("site"):
            fails.append(f"product '{n}' missing site (landing)")
        if not L.get("blog"):
            fails.append(f"product '{n}' missing blog")
    for n in REQUIRED_PRODUCTS:
        L = LINKS.get(n)
        if not isinstance(L, dict) or not L.get("doc") or not L.get("site") or not L.get("blog"):
            fails.append(f"required product '{n}' missing LINKS doc/site/blog")
    print(f"products checked: {len(prod)} (doc-bearing) + {len(REQUIRED_PRODUCTS)} required")

    # ---- Generic sources ----
    gbad = [r["n"] for r in d["genSrc"] if not (r["what"] and r["users"] and r["dataOut"] and r["vol"])]
    if gbad:
        fails.append(f"generic sources missing what/users/dataOut+vol: {gbad}")
    print(f"generic sources: {len(d['genSrc'])} tiles, incomplete: {len(gbad)}")

    # ---- Industry sources + use-case stories ----
    src_bad = uc_bad = 0
    for iid, o in d["inds"].items():
        for r in o["src"]:
            if not (r["what"] and r["users"] and r["dataOut"] and r["vol"]):
                src_bad += 1; fails.append(f"{iid}: source '{r['n']}' incomplete")
        for uc in o["uc"]:
            if not uc["stories"]:
                uc_bad += 1; fails.append(f"{iid}: use case '{uc['n']}' has no story")
    print(f"industry sources incomplete: {src_bad}")
    print(f"industry use cases without a story: {uc_bad}")

    # ---- Live URL check ----
    if args.urls:
        urls = collect_urls(d)
        print(f"\nlive-checking {len(urls)} unique URLs ...")
        bad = []
        with cf.ThreadPoolExecutor(max_workers=24) as ex:
            futs = {ex.submit(check_url, u): u for u in urls}
            for fut in cf.as_completed(futs):
                u = futs[fut]; ok, code = fut.result()
                if not ok:
                    bad.append((u, code, sorted(urls[u])[:3]))
        for u, code, where in sorted(bad):
            fails.append(f"DEAD [{code}] {u}  <- {where}")
        print(f"dead URLs: {len(bad)}")

    print("\n" + "=" * 72)
    if fails:
        print(f"FAIL ({len(fails)} issues)")
        for f in fails:
            print("  -", f)
        raise SystemExit(1)
    print("PASS — every clickable entity is complete" + (" and every URL is live" if args.urls else ""))


if __name__ == "__main__":
    main()
