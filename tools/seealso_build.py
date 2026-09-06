#!/usr/bin/env python3
"""Build the docs' own "directly-linked related features" map. Curation helper.

For every feature that has a Databricks doc page, render that page with headless
Chrome, take ONLY the links inside the main <article> (never the sidebar nav or
footer, which list the whole doc tree), and map each in-article link to another
feature in our LINKS set by matching its doc path. The result is grounded twice
over: the source page really links the target (connection is real), and the URL
shown at runtime is the target feature's own known-good doc path (never invented).

Reads /tmp/feat_docpaths.json (name -> {doc,dbx}) and /tmp/path2name.json
(normalised-doc-path -> feature name). Writes name -> [related feature names]."""
import json, re, subprocess, sys

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
AWS = "https://docs.databricks.com/aws/en/"
FEAT = json.load(open("/tmp/feat_docpaths.json"))
PATH2NAME = json.load(open("/tmp/path2name.json"))
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/seealso_map.json"


def norm(p):
    p = re.sub(r"[#?].*$", "", p or "")            # drop fragment / query
    p = re.sub(r"^https?://[^/]+", "", p)          # drop host
    p = p.replace("/aws/en/", "").replace("/gcp/en/", "")
    return p.strip().strip("/").lower()


def dump(url):
    # Each page is a client-rendered Docusaurus SPA, so a cold headless Chrome is
    # the only way to see the in-article links (~50s/page). Runs SEQUENTIALLY:
    # a `--user-data-dir` makes headless=new hang on this machine, but without it
    # parallel Chromes deadlock on the shared default profile lock, so one page at
    # a time on the default profile is the only combination that both renders and
    # returns. virtual-time-budget caps hydration so a page that never idles still
    # dumps.
    res = subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
         "--virtual-time-budget=6000", "--dump-dom", url],
        capture_output=True, text=True, timeout=130)
    return res.stdout


def related_for(name):
    doc = FEAT.get(name, {}).get("doc")
    if not doc:
        return name, []
    self_norm = norm(doc)
    try:
        html = dump(AWS + doc.lstrip("/"))
    except Exception as e:
        sys.stderr.write(f"[{name}] dump error {e}\n")
        return name, []
    m = re.search(r"<article\b.*?</article>", html, re.S)
    if not m:
        return name, []
    hrefs = re.findall(r'href="([^"]+)"', m.group(0))
    out = []
    for h in hrefs:
        if "/aws/en/" not in h and not h.startswith("/aws/en/"):
            continue
        np = norm(h)
        tgt = PATH2NAME.get(np)
        if tgt and tgt != name and np != self_norm and tgt not in out:
            out.append(tgt)
    return name, out


sources = [n for n, d in FEAT.items() if d.get("doc")]
result, done = {}, 0
for name in sources:                       # sequential: see dump() for why
    _, rel = related_for(name)
    result[name] = rel
    done += 1
    json.dump(result, open(OUT, "w"), ensure_ascii=False, indent=1)
    sys.stderr.write(f"{done}/{len(sources)} {name}: {len(rel)} -> {rel}\n")
    sys.stderr.flush()

kept = {k: v for k, v in result.items() if v}
sys.stderr.write(f"\nDONE. {len(kept)}/{len(sources)} features have see-also; "
                 f"{sum(len(v) for v in kept.values())} edges.\n")
