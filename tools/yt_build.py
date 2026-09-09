#!/usr/bin/env python3
"""Run yt_probe discovery across a list of feature names and emit a verified
name -> [{id,t}] map. Curation helper (not runtime).

Discovery trusts YouTube's own ytInitialData (channel + title) to keep it to one
HTTP call per feature; every kept video is then independently re-verified by
tools/linkgate.py --urls via oEmbed (official Databricks channel + title match)
before anything ships, so discovery being generous here cannot ship a bad video.
Parallelised because each search page is ~2 MB and takes ~25 s to serve."""
import concurrent.futures as cf, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yt_probe as yp

KEYS = json.load(open("/tmp/links_keys.json"))["all"]
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/videos_map.json"
CAP = int(os.environ.get("YT_CAP", "6"))


def probe(name):
    vids = []
    try:
        for vid, title, chan in yp._search("databricks " + name):
            if chan not in yp.OFFICIAL or not yp._title_has(name, title):
                continue
            if any(v["id"] == vid for v in vids):
                continue
            vids.append({"id": vid, "t": title})
            if len(vids) >= CAP:
                break
    except Exception as e:
        sys.stderr.write(f"[{name}] error {e}\n")
    return name, vids


result = {}
done = 0
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    for name, vids in ex.map(probe, KEYS):
        result[name] = vids
        done += 1
        json.dump(result, open(OUT, "w"), ensure_ascii=False, indent=1)
        sys.stderr.write(f"{done}/{len(KEYS)} {name}: {len(vids)}\n")
        sys.stderr.flush()

kept = {k: v for k, v in result.items() if v}
sys.stderr.write(f"\nDONE. {len(kept)} features have videos; "
                 f"{sum(len(v) for v in kept.values())} total.\n")
