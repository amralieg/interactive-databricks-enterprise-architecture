"""Shared blocks for industry authoring."""

AGENT_HARNESSES = {
    "box": "Agent Harnesses",
    "ic": "agents",
    "tiles": [
        {
            "n": "Omnigent OSS",
            "s": "Databricks, open source",
            "ic": "omni",
            "long": "Open-source meta-harness above existing agent frameworks, enabling agent composition, collaboration and centralised governance from one interface. A managed Beta is available.",
            "caps": ["Build", "Deploy", "Optimize", "Govern"],
            "rel": ["Agent Bricks", "Unity AI Gateway"],
        },
        {
            "n": "Claude Code",
            "s": "3rd-party harness",
            "ic": "code",
            "long": "Anthropic's coding harness working against the platform through MCP, with spend, routing and policy governed by Unity AI Gateway.",
        },
        {
            "n": "OpenAI Codex",
            "s": "3rd-party harness",
            "ic": "code",
            "long": "OpenAI's coding harness connected over MCP, governed at runtime by Unity AI Gateway rather than trusted by configuration.",
        },
        {
            "n": "Any MCP Harness",
            "s": "Cursor, IDEs, frameworks",
            "ic": "mcp",
            "long": "Cursor and other IDE agents, LangGraph and CrewAI frameworks, and any other harness that speaks MCP, admitted and scoped in the Unity AI Gateway registry.",
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


def ppl_rail(business_tiles, technical_tiles=None):
    return [
        {"box": "Business", "ic": "zbrief", "tiles": business_tiles[:5]},
        {"box": "Technical", "ic": "code", "tiles": technical_tiles or TECH_PPL},
    ]


def cons_rail(groups, genie_spaces=None, dashboards=None):
    """Consumers rail = the industry's own consumer groups, then Genie Agents
    (top 4), then AI/BI Dashboards (top 4), then the shared Agent Harnesses.

    inject_industries.swap_layout() then lifts the Genie Agents box up into the
    top band and drops the top band's Apps into the slot it vacated, so the
    rendered rail reads: groups, Apps, AI/BI Dashboards, Agent Harnesses."""
    out = list(groups)
    if genie_spaces:
        out.append({"box": "Genie Agents", "ic": "genie", "tiles": genie_spaces})
    if dashboards:
        out.append({"box": "AI/BI Dashboards", "ic": "aibi", "tiles": dashboards})
    return out + [AGENT_HARNESSES]


def fed_group(tile_name, long, cat=None, what=None, users=None, data_out=None):
    t = {"n": tile_name, "ic": "fed", "long": long}
    if cat:
        t["cat"] = cat
    if what:
        t["what"] = what
    if users:
        t["users"] = users
    if data_out:
        t["dataOut"] = data_out
    return {
        "box": "Federation Sources",
        "ic": "fed",
        "from": "fed",
        "tail": True,
        "tiles": [t],
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


def tile(n, ic, long, cite=None, s=None, cat=None, what=None, users=None, data_out=None):
    t = {"n": n, "ic": ic, "long": long}
    if cite:
        t["cite"] = cite if isinstance(cite, list) else [cite]
    if s:
        t["s"] = s
    if cat:
        t["cat"] = cat
    if what:
        t["what"] = what
    if users:
        t["users"] = users
    if data_out:
        t["dataOut"] = data_out
    return t


DATA_SHAPES = ("structured", "semi-structured", "unstructured")


def flow(types, vol, interval):
    """One lane of a source's output: the data shapes it emits, a typical volume
    and the cadence it arrives at. `types` is any of DATA_SHAPES."""
    bad = [x for x in types if x not in DATA_SHAPES]
    if bad:
        raise ValueError(f"flow: unknown data shape(s) {bad}; use {DATA_SHAPES}")
    return {"types": list(types), "vol": vol, "interval": interval}


def data_out(batch=None, stream=None):
    """What a source produces, split into a batch lane and/or a streaming lane.
    At least one lane must be present; each lane is a flow()."""
    d = {}
    if batch:
        d["batch"] = batch
    if stream:
        d["stream"] = stream
    if not d:
        raise ValueError("data_out: at least one of batch / stream is required")
    return d


def genie(n, long, feeds, teams, questions):
    """A Genie space in the Consumers rail: what it does, the data sources it is
    grounded on, the teams that live in it and the top questions it answers."""
    return {"n": n, "ic": "genie", "long": long,
            "feeds": feeds, "teams": teams, "questions": questions}


def dashboard(n, long, kpis, teams):
    """An AI/BI dashboard in the Consumers rail: what it shows, the metrics and
    KPIs it is built on and the teams that read it."""
    return {"n": n, "ic": "aibi", "long": long, "kpis": kpis, "teams": teams}


def biz(n, mark, long, uses, sub=None, ucs=None):
    t = {"n": n, "mark": mark, "long": long, "uses": uses}
    if sub:
        t["sub"] = [{"n": p[0], "cares": p[1]} for p in sub]
    if ucs:
        t["ucs"] = ucs
    return t


def app(n, s, ic, long):
    return {"n": n, "s": s, "ic": ic, "long": long}


def uc(n, s, ic, long, problem=None, who=None, how=None, comps=None, stories=None):
    t = {"n": n, "s": s, "ic": ic, "long": long}
    if problem:
        t["problem"] = problem
    if who:
        t["who"] = who
    if how:
        t["how"] = how
    if comps:
        t["comps"] = comps
    if stories:
        t["stories"] = [{"t": s[0], "u": s[1]} for s in stories]
    return t
