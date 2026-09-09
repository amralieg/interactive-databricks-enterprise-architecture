#!/usr/bin/env python3
"""Surgically add seealso:[...] and/or videos:[...] to LINKS entries in
app/index.html. One LINKS entry lives on one line as `"Name": { ... },`, so the
edit is per-line: insert/extend the two arrays without touching any other field.

Usage:
  inject_links.py --seealso /tmp/seealso_map.json --videos /tmp/videos_apply.json

Either input may be omitted. videos_apply.json is name -> [{id,t}] and is
APPENDED to any existing videos array (deduped by id). seealso is name -> [names]
and REPLACES any existing seealso.
"""
import argparse, json, re, sys

APP = "app/index.html"


def links_bounds(lines):
    """Locate the LINKS object so line edits never stray outside it, even as the
    block grows. Returns (lo, hi) 0-indexed: lo = line after `const LINKS = {`,
    hi = the closing `};` line."""
    lo = next(i for i, l in enumerate(lines) if l.strip().startswith("const LINKS"))
    hi = next(i for i in range(lo + 1, len(lines)) if lines[i].rstrip() == "};")
    return lo + 1, hi


def vobj(v):
    """Serialize a video to the LINKS shape, carrying the verified alias `a` only
    when the title matched a prior/component product name instead of the feature
    name itself (renamed products: AI Search<-Vector Search, etc). The gate reads
    `a` to accept the title; the renderer ignores it."""
    o = {"id": v["id"], "t": v["t"]}
    if v.get("a"):
        o["a"] = v["a"]
    return json.dumps(o, ensure_ascii=False)


def jsarr_videos(vids):
    return "[" + ", ".join(vobj(v) for v in vids) + "]"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seealso")
    ap.add_argument("--videos")
    ap.add_argument("--app", default=APP)
    args = ap.parse_args()

    seealso = json.load(open(args.seealso)) if args.seealso else {}
    videos = json.load(open(args.videos)) if args.videos else {}

    lines = open(args.app, encoding="utf-8").read().split("\n")
    lo, hi = links_bounds(lines)
    entry_re = re.compile(r'^(\s*)"((?:[^"\\]|\\.)*)":\s*\{')
    existing_vid_re = re.compile(r'videos:\[(.*?)\](,?)')
    changed_sa = changed_vid = 0

    for i in range(lo, hi):
        ln = lines[i]
        m = entry_re.match(ln)
        if not m:
            continue
        name = m.group(2)
        sa = seealso.get(name)
        vids = videos.get(name)
        if not sa and not vids:
            continue

        # --- videos: append net-new to existing array, or create one ---
        if vids:
            ex = existing_vid_re.search(ln)
            existing_ids = set(re.findall(r'"id":\s*"([^"]+)"', ex.group(1)) if ex else [])
            new_vids = [v for v in vids if v["id"] not in existing_ids]
            if new_vids:
                if ex:
                    add = ", ".join(vobj(v) for v in new_vids)
                    inner = ex.group(1).strip()
                    merged = "videos:[" + (inner + ", " if inner else "") + add + "]" + ex.group(2)
                    ln = ln[:ex.start()] + merged + ln[ex.end():]
                else:
                    prefix = m.group(1) + '"' + name + '": { '
                    rest = ln[len(m.group(0)):].lstrip()
                    ln = prefix + "videos:" + jsarr_videos(new_vids) + ", " + rest
                changed_vid += 1

        # --- seealso: replace/insert as first key after { ---
        if sa:
            # strip any pre-existing seealso first (there is none today, but be safe)
            ln = re.sub(r'seealso:\[(?:[^\]]*)\],?\s*', '', ln, count=1)
            m2 = entry_re.match(ln)
            prefix = m2.group(1) + '"' + name + '": { '
            rest = ln[len(m2.group(0)):].lstrip()
            ln = prefix + "seealso:" + json.dumps(sa, ensure_ascii=False) + ", " + rest
            changed_sa += 1

        lines[i] = ln

    open(args.app, "w", encoding="utf-8").write("\n".join(lines))
    sys.stderr.write(f"seealso entries changed: {changed_sa}; videos entries changed: {changed_vid}\n")


if __name__ == "__main__":
    main()
