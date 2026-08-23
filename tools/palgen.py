"""Generate the palette CSS for index.html.

Every coloured shape in the diagram takes all five of its slots from one of nine
hue groups. A palette is therefore a recipe applied across those nine hues, not a
hand-picked set of swatches, which is what makes a new palette cheap and what
keeps contrast honest: the recipe is solved per hue rather than eyeballed.

Slots, and the only thing each may be used for:
  line  saturated accent: zone outlines, notches, tile edges
  head  a heading bar carrying WHITE text
  bd    a soft border for a band or tile on its own fill
  bg    the pale fill itself
  ink   text and icons ON that fill

`head` is solved per hue for >=4.5 against white, and `line` for >=3.0 against
the page background, because both vary with hue at fixed lightness: a yellow and
a blue at the same L are nowhere near the same contrast.

Run:  python3 tools/palgen.py --check      report contrast for every slot
      python3 tools/palgen.py --emit       print the CSS block to paste
"""
import argparse, colorsys

# --- the nine hues, degrees on the wheel -------------------------------------
HUES = {
    "green":  142, "teal":   184, "blue":   219, "slate":  214,
    "violet": 266, "plum":   318, "rose":   349, "coral":   11, "amber":  38,
}
# slate is the structural group: it must not compete with the eight that carry
# meaning, so it is held at low chroma in every palette
STRUCTURAL = "slate"

PAGE_BG   = {"light": "#f4f6f8", "dark": "#0c1015"}
BAND_FILL = {"light": "#ffffff", "dark": "#161b22"}


def hex_of(r, g, b):
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))


def rgb_of(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def hsl(hue, sat, lit):
    r, g, b = colorsys.hls_to_rgb((hue % 360) / 360.0, lit, sat)
    return hex_of(r, g, b)


def lum(c):
    def f(v):
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (f(v) for v in rgb_of(c))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    x, y = lum(a), lum(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


def solve(hue, sat, lit, want, against, darker, limit):
    """Take the recipe's lightness, and move only as far as contrast demands.

    Starting from the far end and returning the first passing value is what
    produced a palette much darker than intended: for most hues the recipe
    already passes, so the search must begin there and stay put. `darker` is the
    direction that gains contrast, which is toward black on a light surface and
    toward white on a dark one.
    """
    if contrast(hsl(hue, sat, lit), against) >= want:
        return hsl(hue, sat, lit)
    steps = 240
    for i in range(1, steps + 1):
        l = lit + (limit - lit) * (i / steps)
        c = hsl(hue, sat, l)
        if contrast(c, against) >= want:
            return c
    return hsl(hue, sat, limit)


# --- palettes ----------------------------------------------------------------
# rot   hue rotation applied to all nine groups
# sat   chroma multiplier for the eight meaning-carrying groups
# plat  the platform head accent, which used to be hardcoded to the brand red
#       and was therefore the one shape a palette could not touch
PALETTES = [
    dict(key="",       label="Spectrum", sub="default",     rot=0,    sat=1.00,
         plat=("#ff3621", "#ff5c47")),
    dict(key="muted",  label="Muted",    sub="low chroma",  rot=0,    sat=0.62,
         plat=("#a8443a", "#d2776b")),
    dict(key="vivid",  label="Vivid",    sub="projector",   rot=0,    sat=1.55,
         plat=("#ff1f08", "#ff7259")),
    dict(key="ocean",  label="Ocean",    sub="analogous",   rot=-38,  sat=1.00,
         plat=("#0f6f8c", "#3aa9c9")),
    dict(key="sunset", label="Sunset",   sub="warm shift",  rot=150,  sat=1.10,
         plat=("#b0341f", "#e8735a")),
]

# base chroma and lightness per slot, before the palette's own multiplier
RECIPE = {
    "light": dict(line=(0.46, 0.39), bd=(0.44, 0.80), bg=(0.60, 0.96), ink=(0.44, 0.34)),
    "dark":  dict(line=(0.52, 0.62), bd=(0.26, 0.31), bg=(0.34, 0.11), ink=(0.60, 0.75)),
}
SLATE_SAT = {"light": 0.15, "dark": 0.13}


def build(pal, theme):
    """All five slots for all nine groups, as {token: hex}."""
    out, rec = {}, RECIPE[theme]
    page, fill = PAGE_BG[theme], BAND_FILL[theme]
    for name, base_hue in HUES.items():
        hue = base_hue + pal["rot"]
        struct = name == STRUCTURAL
        k = SLATE_SAT[theme] / rec["line"][0] if struct else pal["sat"]

        def s(slot):
            return min(1.0, rec[slot][0] * k)

        hsat = min(1.0, 0.34 * (1 if struct else pal["sat"]))
        # head carries white text: always darken until white clears 4.5
        head = solve(hue, hsat, 0.39, 4.5, "#ffffff", True, 0.22)
        # line is a graphical element against the page, 3:1 is the bar
        line = solve(hue, s("line"), rec["line"][1], 3.0, page,
                     theme == "light", 0.22 if theme == "light" else 0.82)
        # ink is text on that group's own pale fill
        ink = solve(hue, s("ink"), rec["ink"][1], 4.5, hsl(hue, s("bg"), rec["bg"][1]),
                    theme == "light", 0.18 if theme == "light" else 0.92)
        out["--g-%s-line" % name] = line
        out["--g-%s-head" % name] = head
        out["--g-%s-bd" % name]   = hsl(hue, s("bd"), rec["bd"][1])
        out["--g-%s-bg" % name]   = hsl(hue, s("bg"), rec["bg"][1])
        out["--g-%s-ink" % name]  = ink
    out["--plat-accent"] = pal["plat"][0 if theme == "light" else 1]
    return out


def check():
    worst_text, worst_line, bad = (99, ""), (99, ""), 0
    for pal in PALETTES:
        for theme in ("light", "dark"):
            v = build(pal, theme)
            tag = "%s/%s" % (pal["label"], theme)
            for name in HUES:
                head = v["--g-%s-head" % name]
                ink  = v["--g-%s-ink" % name]
                bg   = v["--g-%s-bg" % name]
                line = v["--g-%s-line" % name]
                for label, c, ref, bar in (
                        ("white on head", "#ffffff", head, 4.5),
                        ("ink on bg",     ink,       bg,   4.5),
                        ("line on page",  line,      PAGE_BG[theme], 3.0)):
                    r = contrast(c, ref)
                    if label == "line on page":
                        if r < worst_line[0]:
                            worst_line = (r, "%s %s" % (tag, name))
                    elif r < worst_text[0]:
                        worst_text = (r, "%s %s %s" % (tag, name, label))
                    if r < bar:
                        bad += 1
                        print("  FAIL %-22s %-8s %-14s %.2f < %.1f" % (tag, name, label, r, bar))
            # the eight meaning groups must stay visually apart from each other
            for a in HUES:
                for b in HUES:
                    if a >= b or STRUCTURAL in (a, b):
                        continue
                    d = abs(((HUES[a] - HUES[b] + 180) % 360) - 180)
                    if d < 19:
                        bad += 1
                        print("  FAIL %s: %s and %s only %d deg apart" % (tag, a, b, d))
    print("worst text contrast : %.2f  (%s)  bar 4.5" % worst_text)
    print("worst line contrast : %.2f  (%s)  bar 3.0" % worst_line)
    print("failures            : %d" % bad)
    return bad


def emit():
    for pal in PALETTES:
        for theme in ("light", "dark"):
            if not pal["key"]:
                sel = ":root" if theme == "light" else "body.theme-dark"
            else:
                sel = "body.pal-%s%s" % (pal["key"], "" if theme == "light" else ".theme-dark")
            print("  %s {" % sel)
            v = build(pal, theme)
            for name in HUES:
                print("  " + " ".join(
                    "%s:%s;" % ("--g-%s-%s" % (name, s), v["--g-%s-%s" % (name, s)])
                    for s in ("line", "head", "bd", "bg", "ink")))
            print("  --plat-accent:%s;" % v["--plat-accent"])
            print("  }")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    p.add_argument("--emit", action="store_true")
    a = p.parse_args()
    if a.emit:
        emit()
    else:
        raise SystemExit(1 if check() else 0)
