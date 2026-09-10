# arch-explorer MCP server

Exposes the shared Databricks reference-architecture templates — the same 63
industry YAMLs the web app reads — as MCP tools, so an agent (Claude Code,
Claude Desktop, or any MCP client) can list, fetch, and search them without the
browser app.

It reads `../architectures/*.yaml` and `../resources/*.json` directly, so new
industry templates dropped into `architectures/` show up through these tools
with no code change.

## Tools

| Tool | Args | Returns |
|------|------|---------|
| `list_industries` | — | `[{id, name, description}]` for all 63 industries |
| `get_architecture` | `industry_id` | the full architecture for one industry (sources, cloud integrations, pipelines/medallion, consumers, agent use cases) |
| `search_architectures` | `query` | `[{id, name, matches}]` — industries whose name/description/components mention the query |
| `list_resources` | `kind` | one of the shared maps: `accelerators`, `connectors`, `links`, `references` |

## Run it

```bash
pip install -r requirements.txt
python server.py          # stdio transport
```

## Register with Claude Code

One-liner:

```bash
claude mcp add arch-explorer -- python /absolute/path/to/app/mcp/server.py
```

Or add to a project `.mcp.json`:

```json
{
  "mcpServers": {
    "arch-explorer": {
      "command": "python",
      "args": ["/absolute/path/to/app/mcp/server.py"]
    }
  }
}
```

Tools then appear as `mcp__arch-explorer__list_industries`, etc. Use a
virtualenv's Python (e.g. the path from `which python` after installing the
requirements) if `python` on PATH lacks the deps.

## Notes

- `mcp[cli]` 2.x renamed `FastMCP` to `MCPServer`; `server.py` imports whichever
  is present, so it runs on both 1.x and 2.x.
- Retrieval only — it serves the reference templates as-is. Generating a
  tailored architecture from a free-text description (the web app's two-phase
  LLM flow) is not included here.
