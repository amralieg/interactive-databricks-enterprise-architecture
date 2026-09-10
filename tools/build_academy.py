#!/usr/bin/env python3
"""Scrape free Databricks Academy courses into app/resources/academy.json.

The Academy runs on Docebo, whose public catalog API needs no auth:

  GET /learn/v1/catalog_content/public?is_paid=0&catalog_ids[]=...&lang=en
      &language[]=<code>          # filter by course language
      &field_19[]=<26..29>        # filter by Skill Level facet
      &field_26[]=<34..42,121>    # filter by Role facet

The listing rows do NOT carry the skill level, role or language variants inline,
so those are recovered by querying each facet value and intersecting on item_id.
Language variants are separate course items; they are matched back to the English
catalogue by normalised name (their name is the English title plus a " - French"
style suffix). Where a name has drifted between languages the variant is dropped
and the English link is used, which is exactly the runtime's default-English rule.

Output (read by the runtime's ACADEMY global and the drawer learning tracks):

  { generated, source, catalog_ids, levels,
    courses:  { id: {t, slug, level, rank, roles[], langs:{code:url}} },
    byProduct:{ product_name: [id, ...] },     # 1-3 curated courses per product
    byPersona:{ team_name:    [id, ...] } }     # role-facet + product-use track,
                                                # deduped, sorted beginner->advanced

Usage:  python3 tools/build_academy.py [--check]
"""
import argparse, datetime, json, os, re, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "app", "resources", "academy.json")
HOST = "https://customer-academy.databricks.com"
API = HOST + "/learn/v1/catalog_content/public"
CATALOG_IDS = [39, 68, 141, 85, 79]
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125 Safari/537.36")

# Skill Level facet (field_19) in beginner -> advanced order; rank drives the sort.
SKILLS = [(26, "Introductory", 0), (27, "Onboarding", 1),
          (28, "Associate", 2), (29, "Professional", 3)]
RANK_UNTAGGED = 5   # an untagged course sorts after the labelled beginner levels

# Role facet (field_26).
ROLES = {34: "Data Analyst", 35: "Data Engineer", 36: "Machine Learning Practitioner",
         37: "Platform Administrator", 38: "Platform Architect", 39: "Apache Spark Developer",
         40: "Generative AI Engineer", 41: "Data Architect", 42: "Data Steward",
         121: "Data Warehousing Practitioner"}

# App content languages that Academy also ships courses in (the other app languages
# fall back to the English link). Academy code -> app T() language code.
LANG_CODES = ["en", "fr", "ja", "ko", "pt-br", "zh", "es"]
LANG_SUFFIX = {  # trailing name suffix a variant carries, stripped to match English
    "fr": "French", "ja": "Japanese", "ko": "Korean", "es": "Spanish",
    "pt-br": "Portuguese BR", "zh": "Simplified Chinese"}

# --- Curated product -> course keyword map (matched against the English title,
# lowercased). Best 1-3 free courses per board tile; capped and rank-sorted. ---
PRODUCT_KW = {
    "Databricks Data Intelligence Platform": ["databricks fundamentals", "get started with databricks: end to end", "create your first workspace"],
    "MLflow": ["machine learning operations", "machine learning model development", "machine learning model deployment"],
    "Model Serving": ["machine learning model deployment", "machine learning at scale"],
    "AI Functions": ["generative ai fundamentals", "get started with databricks for generative ai"],
    "Genie": ["business questions with genie", "business impact accelerator"],
    "Genie One": ["business questions with genie", "business impact accelerator"],
    "Genie Agents": ["business questions with genie", "business impact accelerator"],
    "Genie Agents & Business Use Cases": ["business impact accelerator"],
    "AI/BI Genie": ["business questions with genie", "business impact accelerator"],
    "AI/BI": ["ai/bi for data analysts", "sql analytics on databricks"],
    "Unity Catalog": ["get started with data governance", "data modeling strategies", "databricks data privacy"],
    "Unified Governance": ["get started with data governance", "databricks data privacy", "databricks ai security fundamentals"],
    "Lakeflow Connect": ["data ingestion with lakeflow connect"],
    "Lakeflow": ["build data pipelines", "deploy workloads with lakeflow jobs"],
    "Ingest": ["data ingestion with lakeflow connect"],
    "Apache Spark": ["introduction to apache spark", "developing applications with apache spark", "stream processing and analysis with apache spark"],
    "Delta Lake": ["build data pipelines"],
    "Lakebase": ["get started with lakebase"],
    "Agent Bricks": ["building rag agents with agent bricks", "building agentic applications", "get started with ai agents"],
    "Agentic Dev": ["building agentic applications", "deploying and monitoring agent applications", "get started with ai agents"],
    "Apps": ["get started with databricks apps"],
    "SQL Warehouses": ["sql analytics on databricks", "get started with databricks for data warehousing"],
    "Feature Store": ["data preparation for machine learning"],
    "Notebooks & IDEs": ["introduction to python for data science"],
    "Open Infrastructure": ["databricks compute resource administration", "databricks performance optimization"],
}

# --- Curated persona -> {roles, kw}. Track = courses tagged with any mapped Academy
# role, plus keyword-matched extras (business personas have no Academy role, so they
# ride Genie / AI/BI / fundamentals). Deduped, rank-sorted, capped. ---
PERSONA_MAP = {
    "Executives":          {"roles": [], "kw": ["databricks fundamentals", "business impact accelerator", "generative ai fundamentals", "ai/bi for data analysts"]},
    "Business Teams":      {"roles": [], "kw": ["databricks fundamentals", "business impact accelerator", "ai/bi for data analysts", "get started with sql analytics"]},
    "Risk & Compliance":   {"roles": ["Data Steward", "Platform Administrator"], "kw": ["get started with data governance", "databricks data privacy", "databricks ai security fundamentals"]},
    "Data Engineers":      {"roles": ["Data Engineer", "Apache Spark Developer"], "kw": []},
    "Data Scientists":     {"roles": ["Machine Learning Practitioner", "Generative AI Engineer"], "kw": []},
    "Data Analysts":       {"roles": ["Data Analyst", "Data Warehousing Practitioner"], "kw": []},
    "Analytics Engineers": {"roles": ["Data Analyst", "Data Architect"], "kw": ["data modeling strategies"]},
    "App Developers":      {"roles": ["Generative AI Engineer"], "kw": ["get started with databricks apps", "building agentic applications", "get started with lakebase"]},
}
PRODUCT_CAP = 3
PERSONA_CAP = 8


def fetch(extra):
    p = {"my_catalogs": 1, "get_total_count": 1, "page": 1, "page_size": 200, "cursor": 0,
         "sort_attr": "item_name", "sort_dir": "asc", "is_paid": 0, "show_item_list": 1,
         "list_catalogs_content": 1, "lang": "en"}
    qs = urllib.parse.urlencode(p) + "".join("&catalog_ids[]=%d" % c for c in CATALOG_IDS) + extra
    req = urllib.request.Request(API + "?" + qs, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.load(r)
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(1.5)


def courses_in(node):
    out = []
    if isinstance(node, dict):
        if node.get("item_type") == "learning_course_type":
            out.append(node)
        for v in node.values():
            out += courses_in(v)
    elif isinstance(node, list):
        for v in node:
            out += courses_in(v)
    return out


def ids_for(extra):
    return {c["item_id"] for c in courses_in(fetch(extra))}


def norm_name(s):
    s = (s or "").lower()
    for lab in LANG_SUFFIX.values():
        s = re.sub(r"\s*-\s*" + re.escape(lab.lower()) + r"\s*$", "", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def course_url(cid, slug):
    return "%s/learn/course/%s/%s" % (HOST, cid, slug)


def build():
    # English canonical catalogue.
    eng = {c["item_id"]: c for c in courses_in(fetch("&language[]=en"))}
    sys.stderr.write("english free courses: %d\n" % len(eng))

    # Skill + role facets, recovered per facet value.
    skill = {}
    for key, label, rank in SKILLS:
        for cid in ids_for("&field_19[]=%d" % key):
            skill[cid] = (label, rank)
    roles = {}
    for key, label in ROLES.items():
        for cid in ids_for("&field_26[]=%d" % key):
            roles.setdefault(cid, []).append(label)

    # Language variants -> {norm_name: {code: (id, slug)}}.
    variants = {}
    for code in LANG_CODES:
        if code == "en":
            continue
        for c in courses_in(fetch("&language[]=" + code)):
            variants.setdefault(norm_name(c["item_name"]), {})[code] = (c["item_id"], c["item_slug"])

    # Assemble a course record for an English course id.
    by_norm = {norm_name(c["item_name"]): c for c in eng.values()}

    def record(cid):
        c = eng[cid]
        nm = norm_name(c["item_name"])
        lvl, rank = skill.get(cid, (None, RANK_UNTAGGED))
        langs = {"en": course_url(cid, c["item_slug"])}
        for code, (vid, vslug) in variants.get(nm, {}).items():
            langs[code] = course_url(vid, vslug)
        return {"t": c["item_name"], "slug": c["item_slug"], "level": lvl,
                "rank": rank, "roles": sorted(roles.get(cid, [])), "langs": langs}

    def match_kw(kws):
        hits = []
        for nm, c in by_norm.items():
            if any(k in nm for k in (norm_name(x) for x in kws)):
                hits.append(c["item_id"])
        return hits

    def order_dedup(cand, cap):
        # Beginner -> advanced, then collapse duplicate-named courses (the catalogue
        # carries e.g. an ILT and a self-paced item under one title) to the first.
        ids = sorted(cand, key=lambda i: (skill.get(i, (None, RANK_UNTAGGED))[1], eng[i]["item_name"], i))
        out, seen = [], set()
        for i in ids:
            nm = norm_name(eng[i]["item_name"])
            if nm in seen:
                continue
            seen.add(nm)
            out.append(i)
        return out[:cap]

    used = set()
    by_product = {}
    for prod, kws in PRODUCT_KW.items():
        ids = order_dedup(set(match_kw(kws)), PRODUCT_CAP)
        if ids:
            by_product[prod] = ids
            used.update(ids)

    by_persona = {}
    role_index = {}
    for cid, rs in roles.items():
        for r in rs:
            role_index.setdefault(r, set()).add(cid)
    for persona, spec in PERSONA_MAP.items():
        cand = set(match_kw(spec["kw"]))
        for r in spec["roles"]:
            cand |= (role_index.get(r, set()) & set(eng))   # free english only
        ids = order_dedup(cand, PERSONA_CAP)
        if ids:
            by_persona[persona] = ids
            used.update(ids)

    catalog = {cid: record(cid) for cid in used}
    return {
        "generated": datetime.date.today().isoformat(),
        "source": API,
        "catalog_ids": CATALOG_IDS,
        "levels": [s[1] for s in SKILLS],
        "courses": catalog,
        "byProduct": by_product,
        "byPersona": by_persona,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="scrape and diff vs committed file; exit 1 on drift")
    args = ap.parse_args()
    data = build()

    if not data["courses"]:
        raise SystemExit("0 courses scraped — Academy catalog API changed")
    if not data["byProduct"] or not data["byPersona"]:
        raise SystemExit("product/persona map produced nothing — curation drifted")
    sys.stderr.write("courses:%d  products:%d  personas:%d\n" %
                     (len(data["courses"]), len(data["byProduct"]), len(data["byPersona"])))

    new = json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True)
    if args.check:
        old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        strip = lambda s: re.sub(r'"generated":\s*"[^"]*"', '"generated":""', s)
        if strip(old) != strip(new):
            sys.stderr.write("academy.json is stale — re-run tools/build_academy.py\n")
            sys.exit(1)
        sys.stderr.write("academy.json up to date\n")
        return
    open(OUT, "w", encoding="utf-8").write(new)
    sys.stderr.write("wrote %s\n" % OUT)


if __name__ == "__main__":
    main()
