#!/usr/bin/env python3
"""Emit INDUSTRIES entries from tools/industries/batch*.py into app/index.html."""
import importlib.util
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = ROOT / "app" / "index.html"
BATCH_DIR = ROOT / "tools" / "industries"

BEGIN = "  airlines: {"
END = "\n};\n\n/* Which industry is showing."


def js_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def js_arr(items) -> str:
    return "[" + ", ".join(js_str(x) for x in items) + "]"


def js_flow(f: dict) -> str:
    return "{ types:%s, vol:%s, interval:%s }" % (
        js_arr(f.get("types", [])), js_str(f.get("vol", "")), js_str(f.get("interval", "")))


def js_data_out(do: dict) -> str:
    lanes = []
    if do.get("batch"):
        lanes.append("batch:" + js_flow(do["batch"]))
    if do.get("stream"):
        lanes.append("stream:" + js_flow(do["stream"]))
    return "{ " + ", ".join(lanes) + " }"


def emit_tile(tile: dict, indent: str, ppl: bool = False) -> str:
    parts = [f'n:{js_str(tile["n"])}']
    if not ppl and tile.get("ic"):
        parts.append(f'ic:{js_str(tile["ic"])}')
    if tile.get("s"):
        parts.append(f's:{js_str(tile["s"])}')
    if tile.get("mark"):
        parts.append(f'mark:{js_str(tile["mark"])}')
    if tile.get("long"):
        parts.append(f'long:{js_str(tile["long"])}')
    if tile.get("cite"):
        cites = ", ".join(js_str(c) for c in tile["cite"])
        parts.append(f'cite:[{cites}]')
    if tile.get("cat"):
        parts.append(f'cat:{js_str(tile["cat"])}')
    if tile.get("what"):
        parts.append(f'what:{js_str(tile["what"])}')
    if tile.get("users"):
        parts.append(f'users:{js_str(tile["users"])}')
    if tile.get("dataOut"):
        parts.append(f'dataOut:{js_data_out(tile["dataOut"])}')
    if tile.get("feeds"):
        parts.append(f'feeds:{js_arr(tile["feeds"])}')
    if tile.get("kpis"):
        parts.append(f'kpis:{js_arr(tile["kpis"])}')
    if tile.get("teams"):
        parts.append(f'teams:{js_arr(tile["teams"])}')
    if tile.get("questions"):
        parts.append(f'questions:{js_arr(tile["questions"])}')
    if tile.get("uses"):
        uses = ", ".join(f'[{js_str(u[0])}, {js_str(u[1])}]' for u in tile["uses"])
        parts.append(f'uses:[{uses}]')
    if tile.get("caps"):
        caps = ", ".join(js_str(c) for c in tile["caps"])
        parts.append(f'caps:[{caps}]')
    if tile.get("rel"):
        rel = ", ".join(js_str(r) for r in tile["rel"])
        parts.append(f'rel:[{rel}]')
    if tile.get("sub"):
        sub = ", ".join(
            "{ n:%s, cares:%s }" % (js_str(p["n"]), js_str(p["cares"]))
            for p in tile["sub"]
        )
        parts.append(f'sub:[{sub}]')
    if tile.get("ucs"):
        ucs = ", ".join(js_str(u) for u in tile["ucs"])
        parts.append(f'ucs:[{ucs}]')
    inner = ", ".join(parts)
    return f"{indent}{{ {inner} }}"


def emit_group(g: dict, indent: str, rail_id: str = "") -> str:
    ppl = rail_id == "ppl"
    head = f'{{ box:{js_str(g["box"])}, ic:{js_str(g["ic"])}'
    if g.get("from"):
        head += f', from:{js_str(g["from"])}'
    if g.get("tail"):
        head += ", tail:true"
    tiles = g.get("tiles", [])
    tile_js = ",\n".join(emit_tile(t, indent + "    ", ppl=ppl) for t in tiles)
    return f"{indent}{head}, tiles:[\n{tile_js}\n{indent}] }}"


def emit_rails(rails: dict) -> str:
    lines = ["    rails:{"]
    for rid in ("src", "ing", "ppl", "cons"):
        groups = rails[rid]
        lines.append(f"      {rid}:[")
        for gi, g in enumerate(groups):
            lines.append(emit_group(g, "        ", rid) + ("," if gi < len(groups) - 1 else ""))
        lines.append("      ],")
    lines[-1] = lines[-1].rstrip(",")
    lines.append("    },")
    return "\n".join(lines)


def emit_top_tile(t: dict) -> str:
    parts = [
        f'n:{js_str(t["n"])}',
        f's:{js_str(t["s"])}',
        f'ic:{js_str(t["ic"])}',
        f'long:{js_str(t["long"])}',
    ]
    if t.get("problem"):
        parts.append(f'problem:{js_str(t["problem"])}')
    if t.get("who"):
        parts.append(f'who:{js_str(t["who"])}')
    if t.get("how"):
        parts.append(f'how:{js_str(t["how"])}')
    if t.get("comps"):
        comps = ", ".join(js_str(c) for c in t["comps"])
        parts.append(f'comps:[{comps}]')
    if t.get("stories"):
        st = ", ".join(
            "{ t:%s, u:%s }" % (js_str(s["t"]), js_str(s["u"])) for s in t["stories"]
        )
        parts.append(f'stories:[{st}]')
    return "{ " + ", ".join(parts) + " }"


def emit_top(top: list) -> str:
    lines = ["    top:["]
    for si, sec in enumerate(top):
        lines.append(
            f'      {{ title:{js_str(sec["title"])}, ic:{js_str(sec["ic"])}, '
            f'span:{sec["span"]}, cols:{sec["cols"]}, tiles:['
        )
        for ti, t in enumerate(sec["tiles"]):
            comma = "," if ti < len(sec["tiles"]) - 1 else ""
            lines.append("        " + emit_top_tile(t) + comma)
        lines.append("      ]}," if si == 0 else "      ]}")
    lines.append("    ],")
    return "\n".join(lines)


def emit_sources(sources: dict) -> str:
    lines = ["    sources:{"]
    keys = list(sources.keys())
    for i, k in enumerate(keys):
        v = sources[k]
        comma = "," if i < len(keys) - 1 else ""
        lines.append(
            f'      {js_str(k)}:{{ t:{js_str(v["t"])}, u:{js_str(v["u"])} }}{comma}'
        )
    lines.append("    },")
    return "\n".join(lines)


def emit_industry(iid: str, ind: dict) -> str:
    lines = [
        f"  {iid}: {{",
        f'    label:{js_str(ind["label"])},',
        f'    blurb:{js_str(ind["blurb"])},',
        "    medallion:{",
    ]
    for stage in ("Bronze", "Silver", "Gold"):
        m = ind["medallion"][stage]
        lines.append(
            f'      {stage}:{{ s:{js_str(m["s"])}, long:{js_str(m["long"])} }},'
        )
    lines.append("    },")
    lines.append(emit_rails(ind["rails"]))
    lines.append(emit_top(ind["top"]))
    lines.append(emit_sources(ind["sources"]).rstrip(","))
    lines.append("  },")
    return "\n".join(lines)


def load_batches():
    merged = {}
    for path in sorted(BATCH_DIR.glob("batch*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for name in dir(mod):
            if name.startswith("INDUSTRIES_BATCH"):
                merged.update(getattr(mod, name))
    return merged


def main():
    text = APP.read_text(encoding="utf-8")
    m_begin = text.find(BEGIN)
    m_end = text.find(END)
    if m_begin < 0 or m_end < 0:
        sys.exit("Could not find INDUSTRIES block markers in app/index.html")

    # airlines is the hand-authored reference and the only entry preserved
    # verbatim. Everything between its closing brace and the object's closing
    # `};` is regenerated from the batch files on every run, so re-injecting is
    # idempotent instead of appending the batches again (which previously
    # tripled the industry list and ballooned index.html to 21k lines).
    a_close = text.find("\n  },\n", m_begin)
    if a_close < 0 or a_close >= m_end:
        sys.exit("Could not find end of the airlines reference block")
    airlines_block = text[m_begin : a_close + len("\n  },")]

    extra = load_batches()
    if not extra:
        print("No batch modules found yet.", file=sys.stderr)
        return 1

    emitted = "\n".join(emit_industry(iid, ind) for iid, ind in sorted(extra.items()))
    new_text = text[:m_begin] + airlines_block + "\n" + emitted + text[m_end:]
    APP.write_text(new_text, encoding="utf-8")
    print(f"Injected {len(extra)} industries into {APP}")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
