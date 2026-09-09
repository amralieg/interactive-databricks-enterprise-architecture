#!/usr/bin/env python3
"""Build the shared input files for seealso_build.py and yt_build.py from the
live LINKS object, reusing linkgate.dump() so there is a single source of truth
for what the board's features and their doc paths actually are.

Writes:
  /tmp/feat_docpaths.json  name -> {doc,dbx}   (only doc-bearing features)
  /tmp/path2name.json      normalised-doc-path -> feature name
  /tmp/links_keys.json     {"all":[names], "doc":[doc-bearing names]}
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import linkgate as lg


def norm(p):
    p = re.sub(r"[#?].*$", "", p or "")
    p = re.sub(r"^https?://[^/]+", "", p)
    p = p.replace("/aws/en/", "").replace("/gcp/en/", "")
    return p.strip().strip("/").lower()


d = lg.dump()
LINKS = d["LINKS"]

feat_docpaths, path2name = {}, {}
for name, L in LINKS.items():
    if not isinstance(L, dict):
        continue
    doc, dbx = L.get("doc"), L.get("dbx")
    if doc:
        feat_docpaths[name] = {"doc": doc, "dbx": dbx}
        path2name.setdefault(norm(doc), name)
    if dbx:
        path2name.setdefault(norm(dbx), name)

all_names = [n for n, L in LINKS.items() if isinstance(L, dict)]
doc_names = list(feat_docpaths.keys())

json.dump(feat_docpaths, open("/tmp/feat_docpaths.json", "w"), ensure_ascii=False, indent=1)
json.dump(path2name, open("/tmp/path2name.json", "w"), ensure_ascii=False, indent=1)
json.dump({"all": all_names, "doc": doc_names}, open("/tmp/links_keys.json", "w"), ensure_ascii=False, indent=1)

sys.stderr.write(
    f"feat_docpaths: {len(feat_docpaths)}  path2name: {len(path2name)}  "
    f"all_names: {len(all_names)}  doc_names: {len(doc_names)}\n")
