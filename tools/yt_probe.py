#!/usr/bin/env python3
"""Discover + verify official Databricks YouTube videos for a feature.

Curation helper (not runtime). Fetches YouTube search HTML, parses the embedded
ytInitialData for videoRenderer entries, keeps only videos whose channel is the
official Databricks channel AND whose title carries the feature name, then
cross-verifies each survivor via oEmbed so a parse glitch can never invent an id.

Usage:
  python3 tools/yt_probe.py "Unity Catalog"
  python3 tools/yt_probe.py "Unity Catalog" --query "databricks unity catalog deep dive"

Prints JSON: [{"id": ..., "t": <oembed title>, "channel": ...}, ...]
"""
import argparse, json, re, sys, urllib.parse, urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125 Safari/537.36")
OFFICIAL = {"Databricks"}


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def _norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def _title_has(feature, title):
    """True only if the feature name appears in the title as a whole phrase with
    word boundaries, so 'Serve' never matches 'serverless' and 'AI/BI' matches
    'What is AI/BI?'. Substring matching was the bug that let short generic names
    latch onto unrelated titles."""
    ft = _norm(feature)
    if not ft:
        return False
    return (" " + ft + " ") in (" " + _norm(title) + " ")


def _search(query):
    """Return list of (videoId, title, channel) from the search page."""
    html = _get("https://www.youtube.com/results?search_query=" + urllib.parse.quote(query))
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html)
    if not m:
        m = re.search(r'ytInitialData"\]\s*=\s*(\{.*?\});', html)
    if not m:
        return []
    data = json.loads(m.group(1))
    out, seen = [], set()

    def walk(o):
        if isinstance(o, dict):
            vr = o.get("videoRenderer")
            if isinstance(vr, dict) and vr.get("videoId"):
                vid = vr["videoId"]
                title = ""
                t = vr.get("title", {})
                if "runs" in t:
                    title = "".join(r.get("text", "") for r in t["runs"])
                elif "simpleText" in t:
                    title = t["simpleText"]
                chan = ""
                ot = vr.get("ownerText", {}) or vr.get("longBylineText", {})
                if "runs" in ot:
                    chan = "".join(r.get("text", "") for r in ot["runs"])
                if vid not in seen:
                    seen.add(vid)
                    out.append((vid, title, chan))
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(data)
    return out


def _oembed(vid):
    """Return (author_name, title) or (None, None)."""
    url = "https://www.youtube.com/watch?v=" + vid
    oe = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(url, safe="")
    try:
        meta = json.loads(_get(oe))
        return (meta.get("author_name", "").strip(), meta.get("title", ""))
    except Exception:
        return (None, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("feature")
    ap.add_argument("--query", default=None, help="search text (default: 'databricks <feature>')")
    ap.add_argument("--max", type=int, default=8)
    args = ap.parse_args()
    query = args.query or ("databricks " + args.feature)

    results, kept = _search(query), []
    for vid, title, chan in results:
        if chan not in OFFICIAL or not _title_has(args.feature, title):
            continue
        author, otitle = _oembed(vid)  # source-of-truth cross-check
        if author not in OFFICIAL or not _title_has(args.feature, otitle):
            continue
        kept.append({"id": vid, "t": otitle, "channel": author})
        if len(kept) >= args.max:
            break

    json.dump(kept, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
