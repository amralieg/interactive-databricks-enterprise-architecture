"""
arch-explorer MCP server — exposes the shared reference-architecture templates
(the same 63 industry YAMLs the web app reads) as MCP tools, so an agent can
list, fetch, and search Databricks Data Intelligence Platform reference
architectures without the browser app.

Data source is the sibling app/ directory, read straight from disk:
  ../architectures/manifest.json   — [{id, label, built}]
  ../architectures/<id>.yaml       — one industry's full reference architecture
  ../resources/*.json              — accelerators / connectors / links / references

Because it reads those files directly, new industry templates dropped into
architectures/ appear through these tools with no code change — the same
shared-template property the web app relies on.

Run:      python server.py           (stdio transport)
Register: claude mcp add arch-explorer -- python /abs/path/to/app/mcp/server.py
"""
from __future__ import annotations

import json
import os
from functools import lru_cache

import yaml

# The class was FastMCP in mcp 1.x and was renamed MCPServer in 2.x; the
# .tool() decorator and .run() (stdio by default) are identical on both.
try:
    from mcp.server.fastmcp import FastMCP as _Server
except ModuleNotFoundError:  # mcp >= 2.0
    from mcp.server.mcpserver import MCPServer as _Server

HERE = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(HERE)                       # .../app
ARCH_DIR = os.path.join(APP_DIR, "architectures")
RES_DIR = os.path.join(APP_DIR, "resources")
MANIFEST = os.path.join(ARCH_DIR, "manifest.json")

RESOURCE_KINDS = ("accelerators", "connectors", "links", "references")

mcp = _Server("arch-explorer")


# --------------------------------------------------------------------------
# Loading helpers (cached — the templates are static for a process lifetime)
# --------------------------------------------------------------------------
@lru_cache(maxsize=1)
def _manifest() -> list[dict]:
    with open(MANIFEST, encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=128)
def _load_arch(industry_id: str) -> dict:
    """Parse one industry's YAML. Raises FileNotFoundError if the id is unknown."""
    path = os.path.join(ARCH_DIR, industry_id + ".yaml")
    # Guard against path traversal via a crafted id.
    if os.path.dirname(os.path.abspath(path)) != os.path.abspath(ARCH_DIR):
        raise FileNotFoundError(industry_id)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _valid_ids() -> set[str]:
    return {row["id"] for row in _manifest()}


# --------------------------------------------------------------------------
# Tools
# --------------------------------------------------------------------------
@mcp.tool()
def list_industries() -> list[dict]:
    """List every reference architecture available, one per industry.

    Returns a list of {id, name, description}. Use the `id` with
    get_architecture to fetch the full architecture for that industry.
    """
    out = []
    for row in _manifest():
        iid = row["id"]
        try:
            arch = _load_arch(iid)
            name = arch.get("name") or row.get("label") or iid
            desc = arch.get("description", "")
        except (FileNotFoundError, yaml.YAMLError):
            name, desc = row.get("label") or iid, ""
        out.append({"id": iid, "name": name, "description": desc})
    return out


@mcp.tool()
def get_architecture(industry_id: str) -> dict:
    """Return the full reference architecture for one industry as structured JSON.

    `industry_id` is an id from list_industries (e.g. "banking"). The result
    includes the industry name/description plus its sources, cloud integrations,
    data pipelines (medallion), consumers, and agent use cases.
    """
    if industry_id not in _valid_ids():
        raise ValueError(
            f"Unknown industry_id {industry_id!r}. "
            f"Call list_industries for valid ids."
        )
    arch = _load_arch(industry_id)
    return {"id": industry_id, **arch}


@mcp.tool()
def search_architectures(query: str) -> list[dict]:
    """Find industries whose architecture mentions `query` (case-insensitive).

    Matches the industry name/description and the name/summary of any component
    tile. Returns [{id, name, matches}] where `matches` lists where it hit
    (e.g. "description", or a component name), so you can pick the right
    industry to fetch in full with get_architecture.
    """
    q = (query or "").strip().lower()
    if not q:
        return []
    results = []
    for row in _manifest():
        iid = row["id"]
        try:
            arch = _load_arch(iid)
        except (FileNotFoundError, yaml.YAMLError):
            continue
        matches: list[str] = []
        name = arch.get("name") or iid
        if q in name.lower():
            matches.append("name")
        if q in (arch.get("description") or "").lower():
            matches.append("description")
        # Walk the source/pipeline/consumer sections for tile name/summary hits.
        for section in ("sources", "cloud_integrations", "pipelines", "consumers", "agent_usecases"):
            for group in arch.get(section) or []:
                for tile in (group.get("tiles") or []) if isinstance(group, dict) else []:
                    tname = tile.get("name", "")
                    if q in tname.lower() or q in (tile.get("summary") or "").lower():
                        if tname and tname not in matches:
                            matches.append(tname)
        if matches:
            results.append({"id": iid, "name": name, "matches": matches[:8]})
    return results


@mcp.tool()
def list_resources(kind: str) -> dict:
    """Return one of the shared resource maps that back the architectures.

    `kind` is one of: accelerators, connectors, links, references. These map
    product/connector keys to solution accelerators, Lakeflow Connect
    connectors, doc links, and citation references used across all industries.
    """
    if kind not in RESOURCE_KINDS:
        raise ValueError(f"kind must be one of {', '.join(RESOURCE_KINDS)}")
    path = os.path.join(RES_DIR, kind + ".json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    mcp.run()
