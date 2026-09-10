#!/usr/bin/env python3
"""Attach interactive product tours and hands-on tutorials to the board's
Databricks products in app/resources/links.json.

Truth source is the live Databricks demo-center sitemap, so the URL set is never
invented and stays current: the script pulls every /resources/demos/tours/* and
/resources/demos/tutorials/* URL, fetches each page's real <title>, applies the
curated path -> tile MAP below, and writes a `demos` array onto the matching
LINKS entry:

    "Lakeflow Connect": { ..., "demos": [
        {"t": "<real page title>", "u": "<live url>", "kind": "tour"},
        {"t": "...", "u": "...", "kind": "tutorial"} ] }

Only the path->tile MAP is hand-maintained. Any live URL missing from MAP is
reported as UNMAPPED (map it, or it is dropped); any MAP path missing from the
live sitemap is reported as STALE. linkgate.py --urls HEAD-checks every emitted
URL so a dead demo link fails the push.

Usage:  python3 tools/build_demos.py            # fetch live, write links.json
        python3 tools/build_demos.py --titles /tmp/demo_titles.json   # reuse cache
        python3 tools/build_demos.py --check    # report mapping, do not write
"""
import argparse, concurrent.futures as cf, json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINKS = os.path.join(ROOT, "app", "resources", "links.json")
SITEMAP = "https://www.databricks.com/en-demo-center-assets/sitemap/sitemap-0.xml"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125 Safari/537.36")
BASE = "https://www.databricks.com/resources/demos/"

# Curated map: the demo path AFTER /resources/demos/ -> the board tile name(s) it
# belongs on. A path may serve more than one tile (a Genie+AI/BI dashboard tour
# sits on both). End-to-end lakehouse demos with no single product home go on the
# umbrella "Databricks Data Intelligence Platform". Keep in sync with the sitemap
# via --check (STALE = remove, UNMAPPED = add).
MAP = {
    # ---- tours ----
    "tours/aibi/databricks-embedded-analytics": ["AI/BI", "Embedded Analytics"],
    "tours/appdev/databricks-lakebase": ["Lakebase"],
    "tours/appdev/databricks-one": ["Databricks Data Intelligence Platform", "Consumers"],
    "tours/appdev/lakeflow-workday-connect": ["Lakeflow Connect"],
    "tours/bi/databricks-aibi-aibi-genie-developer": ["AI/BI", "Genie"],
    "tours/bi/fabric-integration-with-uc": ["Unity Catalog"],
    "tours/bi/introducing-databricks-aibi-genie-enduser": ["AI/BI", "Genie One"],
    "tours/data-engineering/databricks-asset-bundles": ["Lakeflow"],
    "tours/data-engineering/databricks-workflows": ["Lakeflow"],
    "tours/data-engineering/introducing-lakeflow-designer": ["Lakeflow Designer"],
    "tours/data-engineering/lakeflow-declarative-pipelines": ["Lakeflow"],
    "tours/data-engineering/volumes-in-unity-catalog": ["Unity Catalog"],
    "tours/data-science-and-ai/agent-bricks": ["Agent Bricks"],
    "tours/data-science-and-ai/databricks-automl": ["MLflow"],
    "tours/data-science-and-ai/databricks-dbrx-instruct-playground": ["Model Serving"],
    "tours/data-science-and-ai/databricks-llama2-lakehouse": ["Model Serving"],
    "tours/data-science-and-ai/finetuning": ["Model Serving"],
    "tours/data-science-and-ai/model-serving-databricks": ["Model Serving"],
    "tours/data-science-and-ai/mosaic-ai-agent-framework-evaluation": ["Agent Bricks", "MLflow"],
    "tours/data-science/mosaic-ai-gateway": ["Unity AI Gateway"],
    "tours/data-sharing/managing-consumer-requests": ["OpenSharing"],
    "tours/data-sharing/marketplace-for-data-providers": ["OpenSharing"],
    "tours/data-sharing/multi-cloud-delta-sharing": ["OpenSharing"],
    "tours/datascience/mosaic-ai-agent-tool-catalog": ["Agent Bricks"],
    "tours/delta-lake-reprise": ["Delta Lake"],
    "tours/deploy-llm-chatbots-rag-and-databricks-ai-vector-search": ["AI Search"],
    "tours/developer-experience/databricks-lakehouseiq-databricks-assistant": ["Agentic Dev"],
    "tours/governance-uc/row-and-column-level-security-with-unity-catalog": ["Unity Catalog"],
    "tours/governance/databricks-clean-rooms": ["Unified Governance"],
    "tours/governance/dbsql": ["SQL Warehouses"],
    "tours/governance/introducing-unity-catalog": ["Unity Catalog"],
    "tours/governance/metric-views-with-uc": ["Unity Catalog"],
    "tours/governance/query-federation-product-tour": ["Unity Catalog"],
    "tours/governance/uc/data-classification": ["Unity Catalog"],
    "tours/governance/uc/enforce-policy": ["Unity Catalog"],
    "tours/governance/unity-catalog-and-lineage": ["Unity Catalog"],
    "tours/governance/unity-catalog-setup": ["Unity Catalog"],
    "tours/governance/unity-catalog-upgrade-utility-tour": ["Unity Catalog"],
    "tours/horizontal/introducing-databricks-intelligence-platform": ["Databricks Data Intelligence Platform"],
    "tours/lakeflow/connector/zerobus-ingest": ["Zerobus"],
    "tours/lakehouse-platform/create-cluster-policy-to-restrict-users": ["Classic & Serverless Compute"],
    "tours/lakehouse-platform/lakehouse-monitoring-databricks": ["Unified Governance"],
    "tours/lakehouse-platform/workspace-creation": ["Databricks Data Intelligence Platform"],
    "tours/platform/databricks-apps": ["Apps"],
    "tours/platform/discover-databricks-lakeflow-connect-demo": ["Lakeflow Connect"],
    "tours/platform/google-analytics-lakeflow-connect": ["Lakeflow Connect"],
    "tours/platform/serverless-egress-control": ["Classic & Serverless Compute"],
    "tours/platform/servicenow-lakeflow-connect": ["Lakeflow Connect"],
    "tours/platform/sql-server-lakeflow-connect": ["Lakeflow Connect"],
    # ---- tutorials ----
    "tutorials/aibi-analytics-in-capital-markets": ["AI/BI"],
    "tutorials/aibi-customer-support-review-dashboards-and-genie": ["AI/BI", "Genie"],
    "tutorials/aibi-genie-marketing-campaign-effectiveness": ["AI/BI", "Genie"],
    "tutorials/aibi-genomic-patient-data-analysis": ["AI/BI"],
    "tutorials/aibi-sales-pipeline-overview": ["AI/BI"],
    "tutorials/aibi-supply-chain-optimization": ["AI/BI"],
    "tutorials/data-engineering/cdc-pipeline-with-delta": ["Lakeflow", "Delta Lake"],
    "tutorials/data-science-and-ai/Image-classification-deep-learning": ["MLflow"],
    "tutorials/data-science-and-ai/databricks-autoloader": ["Auto Loader"],
    "tutorials/data-science-and-ai/delta-lake": ["Delta Lake"],
    "tutorials/data-science-and-ai/feature-store-and-online-inference": ["Feature Store"],
    "tutorials/data-science-and-ai/lakehouse-ai-deploy-your-llm-chatbot": ["AI Search", "Model Serving"],
    "tutorials/data-science-and-ai/llm-tools-functions": ["AI Functions", "Agent Bricks"],
    "tutorials/data-science-and-ai/mlops-end-to-end-pipeline": ["MLflow"],
    "tutorials/data-science-and-ai/pandas-api-with-spark-backend": ["Apache Spark"],
    "tutorials/data-science-and-ai/unit-testing-delta-live-table-for-production-grade-pipelines": ["Lakeflow"],
    "tutorials/data-science/ai-agent": ["Agent Bricks"],
    "tutorials/data-sharing/delta-sharing-airlines": ["OpenSharing"],
    "tutorials/data-warehouse-and-bi/monitor-your-data-quality-with-lakehouse-monitoring": ["Unified Governance"],
    "tutorials/data-warehouse/data-warehousing-with-identity-primary-key-and-foreign-key": ["SQL Warehouses"],
    "tutorials/data-warehouse/query-llm-with-dbsql": ["AI Functions", "SQL Warehouses"],
    "tutorials/genie-code-customer-segmentation": ["Genie Code"],
    "tutorials/governance/access-data-on-external-location": ["Unity Catalog"],
    "tutorials/governance/data-lineage-with-unity-catalog": ["Unity Catalog"],
    "tutorials/governance/system-tables": ["Unity Catalog"],
    "tutorials/governance/table-acl-and-dynamic-views-with-uc": ["Unity Catalog"],
    "tutorials/governance/upgrade-table-to-unity-catalog": ["Unity Catalog"],
    "tutorials/lakehouse-platform/c360-platform-reduce-churn": ["Databricks Data Intelligence Platform"],
    "tutorials/lakehouse-platform/cdc-pipeline-with-delta-live-table": ["Lakeflow"],
    "tutorials/lakehouse-platform/dbdemos-fsi-smart-claims": ["Databricks Data Intelligence Platform"],
    "tutorials/lakehouse-platform/dbdemos-hls-patient-readmission-health": ["Databricks Data Intelligence Platform"],
    "tutorials/lakehouse-platform/iot-and-predictive-maintenance": ["Databricks Data Intelligence Platform"],
    "tutorials/lakehouse-platform/lakeflow-declarative-pipeline": ["Lakeflow"],
    "tutorials/lakehouse-platform/lakehouse-credit-decisioning": ["Databricks Data Intelligence Platform"],
    "tutorials/lakehouse-platform/orchestrate-and-run-your-dbt-jobs": ["Lakeflow", "dbt & External Engines"],
    "tutorials/lakehouse-platform/retail-banking-fraud-detection": ["Databricks Data Intelligence Platform"],
    "tutorials/lakehouse-platform/spark-streaming-advanced": ["Streaming", "Apache Spark"],
}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode("utf-8", "replace")


def live_urls():
    xml = fetch(SITEMAP)
    urls = re.findall(r"https://www\.databricks\.com/resources/demos/[^<\s]+", xml)
    return sorted({u for u in urls if "/tours/" in u or "/tutorials/" in u})


def page_title(u):
    try:
        h = fetch(u)
        m = re.search(r"<title[^>]*>(.*?)</title>", h, re.S)
        t = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
        return u, re.sub(r"\s*\|\s*Databricks\s*$", "", t)
    except Exception:
        return u, ""


def kind_of(u):
    return "tour" if "/tours/" in u else "tutorial"


def path_of(u):
    return u.split("/resources/demos/", 1)[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--titles", help="cache file {url: {t}} to avoid refetching titles")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    urls = live_urls()
    if not urls:
        raise SystemExit("no demo URLs from sitemap — layout changed")

    # titles: from cache when given, else fetch live in parallel.
    titles = {}
    if args.titles and os.path.exists(args.titles):
        cache = json.load(open(args.titles))
        titles = {u: (cache.get(u, {}) or {}).get("t", "") for u in urls}
    missing = [u for u in urls if not titles.get(u)]
    if missing:
        with cf.ThreadPoolExecutor(max_workers=16) as ex:
            for u, t in ex.map(page_title, missing):
                titles[u] = t

    live_paths = {path_of(u) for u in urls}
    stale = sorted(set(MAP) - live_paths)
    unmapped = sorted(p for p in live_paths if p not in MAP)

    # build tile -> [ {t,u,kind} ], tours first then tutorials, then by title
    per_tile = {}
    for u in urls:
        p = path_of(u)
        for tile in MAP.get(p, []):
            per_tile.setdefault(tile, []).append(
                {"t": titles.get(u) or p.rsplit("/", 1)[-1].replace("-", " ").title(),
                 "u": u, "kind": kind_of(u)})
    for tile, rows in per_tile.items():
        rows.sort(key=lambda r: (r["kind"] != "tour", r["t"].lower()))

    links = json.load(open(LINKS, encoding="utf-8"))
    known = set(links)
    missing_tiles = sorted(t for t in per_tile if t not in known)

    sys.stderr.write(
        f"live demo URLs: {len(urls)} | mapped tiles: {len(per_tile)} | "
        f"tours+tutorials placed: {sum(len(v) for v in per_tile.values())}\n")
    if stale:
        sys.stderr.write("STALE MAP paths (no longer in sitemap):\n  " + "\n  ".join(stale) + "\n")
    if unmapped:
        sys.stderr.write("UNMAPPED live paths (add to MAP or they are dropped):\n  " + "\n  ".join(unmapped) + "\n")
    if missing_tiles:
        sys.stderr.write("MAP tiles absent from links.json:\n  " + "\n  ".join(missing_tiles) + "\n")

    if args.check:
        return

    for tile in known:
        rows = per_tile.get(tile)
        if rows:
            links[tile]["demos"] = rows
        elif "demos" in links[tile]:
            del links[tile]["demos"]

    open(LINKS, "w", encoding="utf-8").write(json.dumps(links, ensure_ascii=False))
    sys.stderr.write(f"wrote {LINKS}\n")


if __name__ == "__main__":
    main()
