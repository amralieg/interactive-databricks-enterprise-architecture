"""Shared blocks for industry authoring."""

AGENT_HARNESSES = {
    "box": "Agent Harnesses",
    "ic": "agents",
    "tiles": [
        {
            "n": "Omnigent",
            "s": "Databricks, open source",
            "ic": "omni",
            "long": "Open-source meta-harness above existing agent frameworks, enabling agent composition, collaboration and centralised governance from one interface. A managed Beta is available.",
            "caps": ["Build", "Deploy", "Optimize", "Govern"],
            "rel": ["Agent Bricks", "Unity Gateway"],
        },
        {
            "n": "Claude Code",
            "s": "3rd-party harness",
            "ic": "code",
            "long": "Anthropic's coding harness working against the platform through MCP, with spend, routing and policy governed by Unity Gateway.",
        },
        {
            "n": "OpenAI Codex",
            "s": "3rd-party harness",
            "ic": "code",
            "long": "OpenAI's coding harness connected over MCP, governed at runtime by Unity Gateway rather than trusted by configuration.",
        },
        {
            "n": "Any MCP Harness",
            "s": "Cursor, IDEs, frameworks",
            "ic": "mcp",
            "long": "Cursor and other IDE agents, LangGraph and CrewAI frameworks, and any other harness that speaks MCP, admitted and scoped in the Unity Gateway registry.",
        },
    ],
}

TECH_PPL = [
    {
        "n": "Data Engineers",
        "mark": "Lakeflow",
        "long": "Land the operational, commercial and partner feeds; own the Bronze to Silver path and the pager when a pipeline breaks.",
        "uses": [
            ["Lakeflow Connect", "Managed connectors for ERP, SaaS and industry sources."],
            ["Lakeflow Designer", "Declarative pipelines with expectations on every critical feed."],
            ["Lakewatch", "Freshness on the tables business teams read every morning."],
        ],
    },
    {
        "n": "Data Scientists",
        "mark": "MLflow",
        "long": "Forecasting, risk, personalisation and optimisation models, and whether they still hold six months after deployment.",
        "uses": [
            ["Feature Store", "Features defined once and read identically in training and serving."],
            ["MLflow", "Every run tracked for audit and reproduction."],
            ["Model Serving", "Models scored in the operational and customer-facing path."],
        ],
    },
    {
        "n": "App Developers",
        "mark": "Apps",
        "long": "Ship the operational and customer applications the business works in, hosted next to governed data.",
        "uses": [
            ["Apps", "Operational screens with no separate web tier to run or secure."],
            ["Lakebase", "Serverless Postgres for workflow state and governed writes."],
            ["Agent Bricks", "Agents that draft decisions against governed tools."],
        ],
    },
]


def ing_rail(third_party_tiles):
    return [
        {"box": "Cloud ETL", "ic": "etl", "from": "ingest", "tiles": []},
        {"box": "3rd Party", "ic": "zplug", "tiles": third_party_tiles},
    ]


def ppl_rail(business_tiles):
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": TECH_PPL},
    ]


def cons_rail(groups):
    return groups + [AGENT_HARNESSES]


def fed_group(tile_name, long):
    return {
        "box": "Federation Sources",
        "ic": "fed",
        "from": "fed",
        "tail": True,
        "tiles": [{"n": tile_name, "ic": "fed", "long": long}],
    }


def top_band(apps, use_cases):
    return [
        {"title": "Apps", "ic": "apps", "span": 3, "cols": 2, "tiles": apps},
        {"title": "Use Cases", "ic": "ztarget", "span": 8, "cols": 5, "tiles": use_cases},
    ]


def medallion(bronze_s, bronze_long, silver_s, silver_long, gold_s, gold_long):
    return {
        "Bronze": {"s": bronze_s, "long": bronze_long},
        "Silver": {"s": silver_s, "long": silver_long},
        "Gold": {"s": gold_s, "long": gold_long},
    }


def tile(n, ic, long, cite=None, s=None):
    t = {"n": n, "ic": ic, "long": long}
    if cite:
        t["cite"] = cite if isinstance(cite, list) else [cite]
    if s:
        t["s"] = s
    return t


def biz(n, mark, long, uses):
    return {"n": n, "mark": mark, "long": long, "uses": uses}


def app(n, s, ic, long):
    return {"n": n, "s": s, "ic": ic, "long": long}


def uc(n, s, ic, long):
    return {"n": n, "s": s, "ic": ic, "long": long}
