#!/usr/bin/env python3
"""Region-data gate for app/resources/regions.json.

Verifies the file the Region menu and drawer read is internally consistent and
matches the runtime resolver in app/index.html:

  * structure: every cloud has a non-empty regions[] (code+loc) and a features{}
    map whose columns are {region_code: bool} over that cloud's region codes;
  * alias parity: every ALIAS value resolves to a real feature column on at least
    one cloud by the SAME case-insensitive substring rule regionFeatureLabel()
    uses, so no alias silently maps to nothing (which would look "available
    everywhere" and hide a real regional limit);
  * product parity: every ALIAS key is a real Databricks product tile in
    links.json (an entry carrying a `doc` path), so the map cannot drift to a
    product the board does not draw;
  * a limited feature actually excludes at least one region (else the alias is
    pointless and should be dropped).

With --live it also HEAD-checks the source doc pages so a doc-side move is caught.
Exit code is non-zero on any failure so it chains in a gate pipeline.
"""
import argparse
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGIONS = os.path.join(ROOT, "app", "resources", "regions.json")
LINKS = os.path.join(ROOT, "app", "resources", "links.json")


def feature_label(features, want):
    w = want.lower()
    for lab in features:
        if w in lab.lower():
            return lab
    return None


def check_url(u):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(u, method=method,
                                         headers={"User-Agent": "regiongate/1.0"})
            with urllib.request.urlopen(req, timeout=25) as r:
                return (200 <= r.status < 400, r.status)
        except urllib.error.HTTPError as e:
            if e.code in (403, 405, 429) and method == "HEAD":
                continue
            return (False, e.code)
        except Exception as e:
            return (False, str(e)[:60])
    return (False, "no-response")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true",
                    help="also HEAD-check the source doc pages")
    args = ap.parse_args()

    d = json.load(open(REGIONS))
    links = json.load(open(LINKS))
    fails, warns = [], []

    clouds = d.get("clouds") or {}
    if set(clouds) != {"aws", "azure", "gcp"}:
        fails.append(f"clouds must be exactly aws/azure/gcp, got {sorted(clouds)}")

    for cl, cv in clouds.items():
        regions = cv.get("regions") or []
        codes = {r.get("code") for r in regions}
        if not regions:
            fails.append(f"{cl}: no supported regions")
        for r in regions:
            if not r.get("code") or not r.get("loc"):
                fails.append(f"{cl}: region missing code/loc: {r}")
        feats = cv.get("features") or {}
        for lab, col in feats.items():
            if not isinstance(col, dict) or not col:
                fails.append(f"{cl}: feature '{lab}' has no per-region map")
                continue
            stray = set(col) - codes
            if stray:
                fails.append(f"{cl}: feature '{lab}' references unknown regions {sorted(stray)}")
            if all(bool(v) for v in col.values()):
                warns.append(f"{cl}: feature '{lab}' excludes no region (alias would be a no-op)")

    alias = d.get("alias") or {}
    if not alias:
        fails.append("alias map is empty")
    for prod, want in alias.items():
        L = links.get(prod)
        if not (isinstance(L, dict) and L.get("doc")):
            fails.append(f"alias key '{prod}' is not a Databricks product tile in links.json")
        hits = [cl for cl, cv in clouds.items()
                if feature_label(cv.get("features") or {}, want)]
        if not hits:
            fails.append(f"alias '{prod}' -> '{want}' resolves to NO feature column on any cloud")

    if args.live:
        for cl, src in (d.get("sources") or {}).items():
            for kind, u in src.items():
                ok, code = check_url(u)
                if not ok:
                    fails.append(f"{cl}:{kind} source dead: {u} ({code})")

    for w in warns:
        print("WARN:", w)
    if fails:
        print(f"\nREGIONGATE FAIL ({len(fails)}):")
        for f in fails:
            print("  -", f)
        sys.exit(1)
    print(f"REGIONGATE OK — {len(clouds)} clouds, "
          f"{sum(len(c.get('regions', [])) for c in clouds.values())} regions, "
          f"{len(alias)} aliases, {len(warns)} warnings")


if __name__ == "__main__":
    main()
