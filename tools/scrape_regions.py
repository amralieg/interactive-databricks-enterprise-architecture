#!/usr/bin/env python3
"""Scrape Databricks regional availability into app/resources/regions.json.

Databricks does NOT publish a single product x region matrix. It publishes two
things per cloud, both server-rendered HTML tables:

  * "Databricks clouds and regions"  -> the flat list of supported regions.
  * "Features with limited regional availability" -> the ONLY features that are
    NOT available in every supported region, one column per feature.

Everything absent from the second page is available in every supported region of
that cloud (the page states this itself: "If a feature is supported in all
regions, it is not included"). So the runtime materialises a full matrix from:

    region in regionsFor(product) iff
        product maps to a limited-availability feature column -> that cell's value
        otherwise                                             -> every supported region

This scraper emits the raw scraped truth (supported regions + the limited-feature
tables) plus the curated product->feature-column ALIAS so the runtime resolver has
one authoritative file to read. Re-run whenever the docs change; a companion gate
(regiongate.py) fails the build on drift.

Usage:  python3 tools/scrape_regions.py   [--check]
"""
import argparse, datetime, json, os, re, sys, urllib.request
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "app", "resources", "regions.json")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125 Safari/537.36")

# Doc pages per cloud. supported = the region list; feature = the limited table.
SOURCES = {
    "aws": {
        "supported": "https://docs.databricks.com/aws/en/resources/supported-regions",
        "feature":   "https://docs.databricks.com/aws/en/resources/feature-region-support",
    },
    "azure": {
        "supported": "https://learn.microsoft.com/en-us/azure/databricks/resources/supported-regions",
        "feature":   "https://learn.microsoft.com/en-us/azure/databricks/resources/feature-region-support",
    },
    "gcp": {
        "supported": "https://docs.databricks.com/gcp/en/resources/supported-regions",
        "feature":   "https://docs.databricks.com/gcp/en/resources/feature-region-support",
    },
}

# Curated product -> primary limited-availability feature column. The value is a
# case-insensitive substring matched against the scraped column labels of the
# active cloud. A product NOT listed here is treated as available in every
# supported region (the docs' own default). A product listed here but whose
# column is absent on a given cloud also falls back to all-supported for that
# cloud. One column per product keeps the truth defensible (no invented AND/OR).
ALIAS = {
    "AI Search": "AI Search",
    "Apps": "Databricks Apps",
    "Lakehouse//RT": "Lakehouse Real-Time",
    "Lakeflow Connect": "Managed connectors in Lakeflow Connect",
    "Zerobus": "Zerobus Ingest",
    "Lakebase": "Lakebase Autoscaling",
    "Model Serving": "Custom Model Serving capability (CPU serving)",
    "Unity Gateway": "Unity Gateway",
    "AI Functions": "Other AI functions",
    "Knowledge Assistant": "Knowledge Assistant",
}

CHECK = "✓"


class TableParser(HTMLParser):
    """Collect every <table> as a list of rows, each row a list of cell texts.
    Tolerant of the unclosed <td><p> markup docs.databricks.com emits and of the
    standard fully-closed markup learn.microsoft.com emits."""

    def __init__(self):
        super().__init__()
        self.tables, self._rows, self._cells, self._buf = [], None, None, []
        self._in_table = 0
        self._in_cell = False

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self._in_table += 1
            self._rows = []
        elif tag == "tr" and self._in_table:
            self._flush_row()
            self._cells = []
        elif tag in ("td", "th") and self._in_table:
            # a new cell starts: close the previous one, then begin capturing.
            # Text between <tr> and the first cell (whitespace on fully-closed
            # markup) is ignored because _in_cell is still False there.
            self._flush_cell()
            self._buf = []
            self._in_cell = True

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._in_table:
            self._flush_cell()
        elif tag == "table" and self._in_table:
            self._flush_row()
            if self._rows:
                self.tables.append(self._rows)
            self._rows, self._in_table = None, self._in_table - 1

    def handle_data(self, data):
        if self._in_cell:
            self._buf.append(data)

    def _flush_cell(self):
        if self._cells is not None and self._in_cell:
            self._cells.append("".join(self._buf).strip())
        self._buf = []
        self._in_cell = False

    def _flush_row(self):
        self._flush_cell()
        if self._cells:
            self._rows.append(self._cells)
        self._cells = None


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode("utf-8", "replace")


def tables_of(html):
    p = TableParser()
    p.feed(html)
    return p.tables


def clean_code(s):
    """Region codes carry footnote markers on the Azure docs (southcentralus*,
    uksouth†) that differ between the supported-regions and feature-region tables,
    so the same region reads as two different codes and a feature cell orphans off
    the region list. Strip every trailing non-alphanumeric so both tables agree."""
    return re.sub(r"[^a-z0-9]+$", "", (s or "").strip())


def is_region_row(cell):
    return bool(re.fullmatch(r"[a-z]{2}(-[a-z]+)?-[a-z0-9-]*\d", cell.strip())) \
        or bool(re.fullmatch(r"[a-z]+[a-z0-9]*", cell.strip())) and "-" not in cell


def parse_supported(html):
    """The region list: the table whose header is Region | Location and whose
    rows are region-code | location, with no extra feature columns."""
    out = {}
    for rows in tables_of(html):
        if not rows:
            continue
        head = [c.lower() for c in rows[0]]
        if len(head) == 2 and head[0].startswith("region") and "location" in head[1]:
            for r in rows[1:]:
                if len(r) >= 2 and r[0]:
                    out[clean_code(r[0])] = r[1].strip()
    return out


def parse_features(html):
    """Every limited-availability table: header Region|Location|<feat>|<feat>...
    Returns {feature_label: {region_code: bool}}. Later duplicate tables (the doc
    renders each twice) simply overwrite with identical data."""
    feats = {}
    for rows in tables_of(html):
        if len(rows) < 2:
            continue
        head = rows[0]
        low = [c.lower() for c in head]
        if not (low[0].startswith("region") and len(head) >= 3 and "location" in low[1]):
            continue
        cols = head[2:]
        for r in rows[1:]:
            if len(r) < 2 or not r[0]:
                continue
            code = clean_code(r[0])
            vals = r[2:]
            for i, label in enumerate(cols):
                lab = re.sub(r"\s+", " ", label).strip()
                if not lab:
                    continue
                has = i < len(vals) and CHECK in vals[i]
                feats.setdefault(lab, {})[code] = bool(has)
    return feats


def build():
    clouds = {}
    for cloud, urls in SOURCES.items():
        sup_html = fetch(urls["supported"])
        feat_html = fetch(urls["feature"])
        supported = parse_supported(sup_html)
        features = parse_features(feat_html)
        clouds[cloud] = {
            "regions": [{"code": k, "loc": v} for k, v in supported.items()],
            "features": features,
        }
        sys.stderr.write(
            f"{cloud}: {len(supported)} regions, {len(features)} limited features\n")
    return {
        "generated": datetime.date.today().isoformat(),
        "sources": SOURCES,
        "alias": ALIAS,
        "clouds": clouds,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="scrape and diff against the committed file; exit 1 on drift")
    args = ap.parse_args()
    data = build()

    # every cloud must have yielded regions and at least one limited feature, or
    # the doc layout moved and a silent empty file would poison the runtime.
    for cloud, c in data["clouds"].items():
        if not c["regions"]:
            raise SystemExit(f"{cloud}: 0 regions scraped — doc layout changed")
        if not c["features"]:
            raise SystemExit(f"{cloud}: 0 limited features scraped — doc layout changed")

    new = json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True)
    if args.check:
        old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        # compare on everything but the generated date
        def strip_date(s):
            return re.sub(r'"generated":\s*"[^"]*"', '"generated":""', s)
        if strip_date(old) != strip_date(new):
            sys.stderr.write("regions.json is stale — re-run tools/scrape_regions.py\n")
            sys.exit(1)
        sys.stderr.write("regions.json up to date\n")
        return
    open(OUT, "w", encoding="utf-8").write(new)
    sys.stderr.write(f"wrote {OUT}\n")


if __name__ == "__main__":
    main()
