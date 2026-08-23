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
#
# Optional keys:
# mono  drop chroma to zero and let LIGHTNESS carry what hue used to. Nine grey
#       fills that are only a shade apart read as one, so the groups are pushed
#       apart along the ladder instead, which is also what makes this the one
#       palette that survives a monochrome printer or a photocopier.
# over  per-theme overrides of the slot recipe, for the palettes whose whole
#       point is a denser fill than the default pale wash.
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
    # --- added for a global audience: mono for print and for the places that
    # want no colour at all, then a range from restrained to deliberately loud
    dict(key="mono",   label="Mono",     sub="print safe",  rot=0,    sat=0.00,
         mono=True, plat=("#2b2b2b", "#d8d8d8")),
    dict(key="solid",  label="Solid",    sub="filled",      rot=0,    sat=1.30,
         plat=("#c4321c", "#f0644a"),
         over={"light": dict(bg=(0.52, 0.88), bd=(0.50, 0.62)),
               "dark":  dict(bg=(0.40, 0.19), bd=(0.34, 0.40))}),
    dict(key="pop",    label="Pop",      sub="playful",     rot=92,   sat=1.62,
         plat=("#0f8f6a", "#2fd6a4"),
         over={"light": dict(bg=(0.78, 0.93)), "dark": dict(bg=(0.46, 0.15))}),
    dict(key="neon",   label="Neon",     sub="maximum",     rot=196,  sat=2.00,
         plat=("#7a11c8", "#c661ff"),
         over={"light": dict(line=(0.92, 0.42), bg=(0.95, 0.94)),
               "dark":  dict(line=(1.00, 0.66), bg=(0.62, 0.13), ink=(0.95, 0.80))}),
    dict(key="earth",  label="Earth",    sub="warm neutral", rot=24,  sat=0.78,
         plat=("#8a4a24", "#cf8a58"),
         over={"light": dict(bg=(0.46, 0.94)), "dark": dict(bg=(0.30, 0.13))}),
    dict(key="jewel",  label="Jewel",    sub="deep",        rot=-14,  sat=1.45,
         plat=("#8c1036", "#e0446f"),
         over={"light": dict(line=(0.70, 0.32), bg=(0.56, 0.91), bd=(0.54, 0.70)),
               "dark":  dict(line=(0.72, 0.58), bg=(0.50, 0.14), bd=(0.42, 0.34))}),
    dict(key="nordic", label="Nordic",   sub="cool calm",   rot=-62,  sat=0.52,
         plat=("#28566e", "#7fb2cc")),
    dict(key="berry",  label="Berry",    sub="cool warm",   rot=118,  sat=1.18,
         plat=("#8e2060", "#e05a9c")),
]
# The band of the lightness ladder the greyscale fills are spread across, palest
# first. A symmetric step around the recipe was the obvious way to do this and it
# does not work: the recipe fill already sits near the top of the ladder, so half
# the groups ran past white, clamped, and came back the same grey. The range is
# therefore stated outright, and sized so that even the two closest fills stay
# apart by more than MONO_MIN once luminance is worked out rather than lightness.
MONO_BG = {"light": (0.985, 0.852), "dark": (0.175, 0.062)}
MONO_MIN = 1.035
# A 2px outline is a far smaller target than a filled tile, so it needs a wider
# step to read as a different zone. This bar is set just under the tightest step
# the outline ladder actually produces, which is the pair the 3:1 page solve
# still clamps at the pale end.
MONO_LINE_MIN = 1.12
# The outlines need a band of their own, and not the fills'. Every line is
# solved for 3:1 against the page, and when the fill ladder is handed to the
# line slot most of the ladder is on the wrong side of that bar: the solve drags
# each one back to the edge of passing, so all nine zones end up the same grey
# and the outline stops saying which zone you are looking at. These two ends are
# picked to clear 3:1 already, so the solve has nothing to correct and the
# spread survives it.
MONO_LINE = {"light": (0.58, 0.20), "dark": (0.47, 0.97)}


def lit_of_lum(y):
    """The grey whose luminance is y. Inverse of the sRGB transfer curve.

    Stepping the eight fills evenly along LIGHTNESS looks like the obvious way
    to spread them and it is not: the curve is far steeper at the dark end, so
    equal lightness steps give wildly unequal contrast and the closest pair sat
    under the bar while the widest pair wasted room. Stepping evenly along
    luminance instead gives every neighbouring pair the same ratio, so the whole
    range is used and one number decides whether the palette passes.
    """
    y = max(0.0, min(1.0, y))
    return y * 12.92 if y <= 0.00304 else 1.055 * (y ** (1 / 2.4)) - 0.055

# base chroma and lightness per slot, before the palette's own multiplier
RECIPE = {
    "light": dict(line=(0.46, 0.39), bd=(0.44, 0.80), bg=(0.60, 0.96), ink=(0.44, 0.34)),
    "dark":  dict(line=(0.52, 0.62), bd=(0.26, 0.31), bg=(0.34, 0.11), ink=(0.60, 0.75)),
}
SLATE_SAT = {"light": 0.15, "dark": 0.13}


def build(pal, theme):
    """All five slots for all nine groups, as {token: hex}."""
    out = {}
    rec = dict(RECIPE[theme])
    rec.update(pal.get("over", {}).get(theme, {}))
    page, fill = PAGE_BG[theme], BAND_FILL[theme]
    order = list(HUES)
    for name, base_hue in HUES.items():
        hue = base_hue + pal["rot"]
        struct = name == STRUCTURAL
        k = SLATE_SAT[theme] / rec["line"][0] if struct else pal["sat"]
        # with no chroma the hue is meaningless, so the group's position on the
        # lightness ladder is the only thing left to tell it from its neighbours
        shift = 0.0
        mono_line_l = None
        if pal.get("mono") and not struct:
            spread = [n for n in order if n != STRUCTURAL]
            t = spread.index(name) / float(len(spread) - 1)

            def rung(band):
                a, b = band
                ya, yb = lum(hsl(0, 0, a)) + 0.05, lum(hsl(0, 0, b)) + 0.05
                return lit_of_lum(ya * (yb / ya) ** t - 0.05)

            shift = rung(MONO_BG[theme]) - rec["bg"][1]
            mono_line_l = rung(MONO_LINE[theme])

        def s(slot):
            return min(1.0, rec[slot][0] * k)

        hsat = min(1.0, 0.34 * (1 if struct else pal["sat"]))
        # clamped, because a shifted fill must stay a fill: run past white and
        # the tile loses its edge, run past the page and it stops being a tile
        def L(slot, lo=0.06, hi=0.985):
            return max(lo, min(hi, rec[slot][1] + shift))

        # head carries white text: always darken until white clears 4.5
        head = solve(hue, hsat, 0.39 + shift * 0.5, 4.5, "#ffffff", True, 0.22)
        # line is a graphical element against the page, 3:1 is the bar
        line = solve(hue, s("line"), mono_line_l if mono_line_l is not None else L("line"),
                     3.0, page, theme == "light", 0.22 if theme == "light" else 0.82)
        # ink is text on that group's own pale fill
        ink = solve(hue, s("ink"), L("ink"), 4.5, hsl(hue, s("bg"), L("bg")),
                    theme == "light", 0.18 if theme == "light" else 0.92)
        out["--g-%s-line" % name] = line
        out["--g-%s-head" % name] = head
        out["--g-%s-bd" % name]   = hsl(hue, s("bd"), L("bd"))
        out["--g-%s-bg" % name]   = hsl(hue, s("bg"), L("bg"))
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
            # A palette with no chroma cannot lean on that separation, so the
            # ladder has to do the work instead: two groups a hair apart in grey
            # are one group as far as the reader is concerned. Both the fill and
            # the outline are checked: the fill is the largest area of a group,
            # and the outline is the only thing marking a zone that has no fill
            # at all, which is how nine identical grey zone outlines shipped
            # while the fills alone were passing this gate.
            if pal.get("mono"):
                for slot, bar in (("bg", MONO_MIN), ("line", MONO_LINE_MIN)):
                    for a in HUES:
                        for b in HUES:
                            if a >= b or STRUCTURAL in (a, b):
                                continue
                            r = contrast(v["--g-%s-%s" % (a, slot)],
                                         v["--g-%s-%s" % (b, slot)])
                            if r < bar:
                                bad += 1
                                print("  FAIL %s: %s greys %s and %s only %.3f apart, bar %.3f"
                                      % (tag, slot, a, b, r, bar))
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
