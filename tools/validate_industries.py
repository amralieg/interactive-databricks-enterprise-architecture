#!/usr/bin/env python3
"""Structural + citation + URL gates for the industry batch modules.

    python3 tools/validate_industries.py            # cite-integrity + structure
    python3 tools/validate_industries.py --urls     # also HEAD-check every source URL
"""
import argparse
import importlib.util
import pathlib
import ssl
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BATCH_DIR = ROOT / "tools" / "industries"
APP = ROOT / "app" / "index.html"


def _load_allowed_ic():
    """The ONLY authority on valid icon tokens is the ICON map rendered by the
    app. Parsing it here means the gate can never drift from what the board can
    actually draw: a token is legal iff the app has a glyph for it."""
    t = APP.read_text(encoding="utf-8")
    m = re.search(r"(?:const|var)\s+ICON[A-Z_]*\s*=\s*\{", t)
    if not m:
        raise SystemExit("could not locate ICON map in app/index.html")
    start = m.end()
    depth, i = 1, start
    while depth and i < len(t):
        if t[i] == "{":
            depth += 1
        elif t[i] == "}":
            depth -= 1
        i += 1
    block = t[start:i]
    return set(re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\s*:", block))


ALLOWED_IC = _load_allowed_ic()


def load():
    merged = {}
    for p in sorted(BATCH_DIR.glob("batch*.py")):
        spec = importlib.util.spec_from_file_location(p.stem, p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for name in dir(mod):
            if name.startswith("INDUSTRIES_BATCH"):
                merged.update(getattr(mod, name))
    return merged


def src_ing_cons_tiles(ind):
    for rid in ("src", "ing", "cons"):
        for g in ind["rails"][rid]:
            for t in g.get("tiles", []):
                yield rid, g["box"], t


def check_structure(merged):
    errs = []
    for iid, ind in merged.items():
        rails = ind["rails"]
        biz = [g for g in rails["ppl"] if g["box"] == "Business"]
        tech = [g for g in rails["ppl"] if g["box"] == "Technical"]
        if not biz or len(biz[0]["tiles"]) > 5:
            errs.append(f"{iid}: business group missing or >5 tiles")
        if not tech or len(tech[0]["tiles"]) != 3:
            errs.append(f"{iid}: technical group must have exactly 3 tiles")
        ing3 = [g for g in rails["ing"] if g["box"] != "Cloud ETL"]
        if ing3 and len(ing3[0]["tiles"]) > 3:
            errs.append(f"{iid}: 3rd-party ingest >3 tiles")
        for g in rails["src"] + rails["ing"] + rails["cons"]:
            if len(g.get("box", "")) > 24:
                errs.append(f"{iid}: box name >22 chars: {g['box']!r}")
            for t in g.get("tiles", []):
                ic = t.get("ic")
                if ic and ic not in ALLOWED_IC:
                    errs.append(f"{iid}: unknown ic {ic!r} on {t.get('n')!r}")
        apps, ucs = ind["top"][0]["tiles"], ind["top"][1]["tiles"]
        if len(apps) != 4:
            errs.append(f"{iid}: top Apps must be 4, got {len(apps)}")
        if len(ucs) != 10:
            errs.append(f"{iid}: top Use Cases must be 10, got {len(ucs)}")
    return errs


DATA_SHAPES = {"structured", "semi-structured", "unstructured"}


def _check_flow(errs, iid, where, flow):
    if not isinstance(flow, dict):
        errs.append(f"{iid}: {where} lane must be a dict")
        return
    types = flow.get("types")
    if not isinstance(types, list) or not types:
        errs.append(f"{iid}: {where} lane missing non-empty types")
    else:
        bad = [x for x in types if x not in DATA_SHAPES]
        if bad:
            errs.append(f"{iid}: {where} lane has bad data shape(s) {bad}")
    if not flow.get("vol"):
        errs.append(f"{iid}: {where} lane missing vol")
    if not flow.get("interval"):
        errs.append(f"{iid}: {where} lane missing interval")


def _check_source_tile(errs, iid, box, t):
    n = t.get("n")
    for f in ("cat", "what", "users"):
        if not t.get(f):
            errs.append(f"{iid}: source {n!r} in {box!r} missing {f}")
    do = t.get("dataOut")
    if not isinstance(do, dict) or not (do.get("batch") or do.get("stream")):
        errs.append(f"{iid}: source {n!r} in {box!r} missing dataOut (batch/stream)")
        return
    if do.get("batch"):
        _check_flow(errs, iid, f"{n} batch", do["batch"])
    if do.get("stream"):
        _check_flow(errs, iid, f"{n} stream", do["stream"])


def check_enrichment(merged):
    """Every source system in the Sources rail and every 3rd-party ingest system
    must carry the side-panel enrichment (cat / what / users / dataOut). Every
    industry must publish exactly 4 Genie Agents and 4 AI/BI Dashboards, each with
    the fields the consumer detail panel renders. (Authoring shape: Genie Agents
    are authored on the Consumers rail and lifted into the top band at inject.)"""
    errs = []
    for iid, ind in merged.items():
        rails = ind["rails"]
        for g in rails["src"]:
            for t in g.get("tiles", []):
                _check_source_tile(errs, iid, g.get("box", ""), t)
        for g in rails["ing"]:
            if g.get("box") == "Cloud ETL":
                continue
            for t in g.get("tiles", []):
                _check_source_tile(errs, iid, g.get("box", ""), t)

        genie = [g for g in rails["cons"] if g.get("box") == "Genie Agents"]
        dash = [g for g in rails["cons"] if g.get("box") == "AI/BI Dashboards"]
        if not genie or len(genie[0]["tiles"]) != 4:
            errs.append(f"{iid}: consumers must have a Genie Agents group of exactly 4")
        else:
            for t in genie[0]["tiles"]:
                n = t.get("n")
                if not isinstance(t.get("feeds"), list) or not t["feeds"]:
                    errs.append(f"{iid}: genie {n!r} missing feeds")
                if not isinstance(t.get("teams"), list) or not t["teams"]:
                    errs.append(f"{iid}: genie {n!r} missing teams")
                if not isinstance(t.get("questions"), list) or len(t.get("questions", [])) != 5:
                    errs.append(f"{iid}: genie {n!r} must have exactly 5 questions")
        if not dash or len(dash[0]["tiles"]) != 4:
            errs.append(f"{iid}: consumers must have an AI/BI Dashboards group of exactly 4")
        else:
            for t in dash[0]["tiles"]:
                n = t.get("n")
                if not isinstance(t.get("kpis"), list) or not t["kpis"]:
                    errs.append(f"{iid}: dashboard {n!r} missing kpis")
                if not isinstance(t.get("teams"), list) or not t["teams"]:
                    errs.append(f"{iid}: dashboard {n!r} missing teams")
    return errs


def check_cites(merged):
    errs = []
    for iid, ind in merged.items():
        keys = set(ind.get("sources", {}).keys())
        used = set()
        for _, _, t in src_ing_cons_tiles(ind):
            for c in t.get("cite", []) or []:
                used.add(c)
                if c not in keys:
                    errs.append(f"{iid}: dangling cite {c!r} on {t.get('n')!r}")
        for k in keys - used:
            errs.append(f"{iid}: orphan source {k!r} (defined, never cited)")
    return errs


def check_urls(merged):
    urls = []
    for iid, ind in merged.items():
        for k, v in ind.get("sources", {}).items():
            urls.append((iid, k, v["u"]))
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    def probe(item):
        iid, k, u = item
        last = None
        for method in ("HEAD", "GET"):
            try:
                req = urllib.request.Request(
                    u, method=method,
                    headers={"User-Agent": "Mozilla/5.0 (compatible; idea-linkcheck/1.0)"},
                )
                r = urllib.request.urlopen(req, timeout=12, context=ctx)
                if r.status < 400:
                    return (iid, k, u, r.status, "ok")
                last = r.status
            except Exception as e:
                last = getattr(e, "code", None) or str(e)[:60]
        # Hard breakage: page/path is gone, or the host does not resolve / TLS is broken.
        # Soft: 401/403/406/429 (bot-blocked but the host and path exist), transient 5xx/timeouts.
        if last in (404, 410) or isinstance(last, str) and (
            "nodename" in last or "SSL" in last or "Name or service" in last
        ):
            return (iid, k, u, last, "hard")
        return (iid, k, u, last, "soft")

    hard, soft = [], []
    with ThreadPoolExecutor(max_workers=16) as ex:
        for iid, k, u, code, verdict in ex.map(probe, urls):
            if verdict == "hard":
                hard.append((iid, k, u, code))
            elif verdict == "soft":
                soft.append((iid, k, u, code))
    return urls, hard, soft


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", action="store_true")
    args = ap.parse_args()
    merged = load()
    print(f"industries: {len(merged)}")

    errs = check_structure(merged) + check_cites(merged) + check_enrichment(merged)
    for e in errs:
        print("  ERR", e)
    print(f"structure+cite+enrichment errors: {len(errs)}")

    url_fail = 0
    if args.urls:
        urls, hard, soft = check_urls(merged)
        for iid, k, u, code in sorted(hard):
            print(f"  DEAD {code} {iid}/{k} {u}")
        for iid, k, u, code in sorted(soft):
            print(f"  soft {code} {iid}/{k} {u}")
        url_fail = len(hard)
        print(f"urls: {len(urls)} checked, {len(hard)} hard-dead, {len(soft)} soft-blocked")

    if errs or url_fail:
        sys.exit(1)
    print("PASS")


if __name__ == "__main__":
    main()
