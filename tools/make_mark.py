#!/usr/bin/env python3
"""Writes the zhware mark: the wordmark, the favicon, its rasters, and the
page's font subset, all from Hanken Grotesk.

    pip install fonttools brotli          # in a throwaway venv
    python3 tools/make_mark.py PATH/TO/HankenGrotesk[wght].ttf

The font is the variable one from google/fonts (ofl/hankengrotesk). It is not
committed; the outputs are:

    logo.svg                    zh (700) ware (400, lighter) . (700, brass)
    favicon.svg                 zh. on nothing; ink follows the tab's theme
    icon.svg                    zh. on a paper tile, for the rasters
    favicon.ico, apple-touch-icon.png
    assets/fonts/hanken-grotesk.woff2   Latin subset, wght 400-700

Letters are outlines, so no SVG here needs the font. Rasters go through
wordgarner/tools/make_icons.py, which reads rect, circle and path only.
"""

import importlib.util
import sys
from pathlib import Path

from fontTools import subset
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = Path(__file__).resolve().parent.parent
INK, INK_DARK, BRASS, PAPER = "#1e2126", "#ece9e2", "#b8862b", "#f3f1ec"
TRACKING = -0.045  # em, as the design sheet's .wm-a
WARE_OPACITY = 0.62


def instance(src: Path, weight: int) -> TTFont:
    return instancer.instantiateVariableFont(TTFont(src), {"wght": weight})


def run(font: TTFont, text: str, x: float) -> tuple[list[str], float]:
    """Path data for [text] set from [x] on the baseline, y down; the new x."""
    upm = font["head"].unitsPerEm
    glyphs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
    paths = []
    for ch in text:
        name = cmap[ord(ch)]
        pen = SVGPathPen(glyphs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
        glyphs[name].draw(TransformPen(pen, (1, 0, 0, -1, x, 0)))
        paths.append(pen.getCommands())
        x += hmtx[name][0] + TRACKING * upm
    return paths, x


def bounds(font: TTFont, text: str, x: float = 0) -> tuple[float, float, float, float]:
    glyphs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font["hmtx"]
    box = None
    for ch in text:
        name = cmap[ord(ch)]
        pen = BoundsPen(glyphs)
        glyphs[name].draw(TransformPen(pen, (1, 0, 0, -1, x, 0)))
        if pen.bounds:
            b = pen.bounds
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
        x += hmtx[name][0] + TRACKING * font["head"].unitsPerEm
    return box


def write_logo(bold: TTFont, regular: TTFont) -> None:
    zh, x = run(bold, "zh", 0)
    ware, x2 = run(regular, "ware", x)
    dot, _ = run(bold, ".", x2)
    asc, desc = bold["hhea"].ascent, bold["hhea"].descent
    x_box = bounds(bold, "zh")
    end = bounds(bold, ".", x2)[2]
    top = -asc
    height = asc - desc
    left = x_box[0]
    (ROOT / "logo.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{left:.0f} {top} {end - left:.0f} {height}" '
        f'role="img" aria-label="zhware">\n'
        f'  <path fill="currentColor" d="{" ".join(zh)}"/>\n'
        f'  <path fill="currentColor" fill-opacity="{WARE_OPACITY}" d="{" ".join(ware)}"/>\n'
        f'  <path fill="{BRASS}" d="{" ".join(dot)}"/>\n'
        f"</svg>\n"
    )


def mark_paths(bold: TTFont, side: float, margin: float) -> tuple[str, str, float, float, float]:
    """zh. scaled into a [side] square: the letters, the dot, and the transform."""
    zh, x = run(bold, "zh", 0)
    dot, _ = run(bold, ".", x)
    b0 = bounds(bold, "zh")
    b1 = bounds(bold, ".", x)
    left, right = b0[0], b1[2]
    scale = (side - 2 * margin) / (right - left)
    ink_top, ink_bottom = b0[1], b0[3]
    dx = margin - left * scale
    dy = side / 2 - (ink_top + ink_bottom) / 2 * scale
    return " ".join(zh), " ".join(dot), scale, dx, dy


def write_icons(bold: TTFont) -> None:
    zh, dot, s, dx, dy = mark_paths(bold, 100, 9)
    g = f'transform="translate({dx:.2f} {dy:.2f}) scale({s:.5f})"'
    (ROOT / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">\n'
        f"  <style>.i{{fill:{INK}}}@media (prefers-color-scheme:dark){{.i{{fill:{INK_DARK}}}}}</style>\n"
        f'  <g {g}><path class="i" d="{zh}"/><path fill="{BRASS}" d="{dot}"/></g>\n'
        "</svg>\n"
    )
    zh, dot, s, dx, dy = mark_paths(bold, 100, 14)
    # make_icons.py has no transform support, so bake it into the numbers.
    def bake(d: str) -> str:
        out, nums, cmd = [], [], None
        for tok in d.replace("M", " M ").replace("L", " L ").replace("Q", " Q ").replace("C", " C ").replace("Z", " Z ").replace("H", " H ").replace("V", " V ").split():
            if tok.isalpha():
                out.append(tok)
                cmd = tok
                i = 0
            else:
                v = float(tok)
                if cmd == "H":
                    v = v * s + dx
                elif cmd == "V":
                    v = v * s + dy
                else:
                    v = v * s + (dx if i % 2 == 0 else dy)
                    i += 1
                out.append(f"{v:.2f}")
        return " ".join(out)
    (ROOT / "icon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">\n'
        f'  <rect width="100" height="100" rx="22" fill="{PAPER}"/>\n'
        f'  <path fill="{INK}" d="{bake(zh)}"/>\n'
        f'  <path fill="{BRASS}" d="{bake(dot)}"/>\n'
        "</svg>\n"
    )
    spec = importlib.util.spec_from_file_location("mi", ROOT / "wordgarner/tools/make_icons.py")
    mi = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mi)
    side, shapes = mi.parse_svg(ROOT / "icon.svg")
    tile = lambda n, **kw: mi._png(mi.render(shapes, side, n, **kw))  # noqa: E731
    (ROOT / "apple-touch-icon.png").write_bytes(tile(180, square=True))
    (ROOT / "favicon.ico").write_bytes(mi._ico([(n, tile(n)) for n in (16, 32, 48)]))


def write_font(src: Path) -> None:
    # Subset first: the subsetter trips on a partly instanced gvar.
    font = TTFont(src)
    opts = subset.Options()
    opts.layout_features = ["kern", "liga", "tnum"]
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=list(range(0x20, 0x7F)) + [0xA0, 0xA9, 0xB7, 0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2026, 0x2192])
    sub.subset(font)
    font = instancer.instantiateVariableFont(font, {"wght": (400, 700)})
    out = ROOT / "assets/fonts/hanken-grotesk.woff2"
    out.parent.mkdir(parents=True, exist_ok=True)
    font.flavor = "woff2"
    font.save(out)


def main(src: Path) -> None:
    bold, regular = instance(src, 700), instance(src, 400)
    write_logo(bold, regular)
    write_icons(bold)
    write_font(src)
    for p in ("logo.svg", "favicon.svg", "icon.svg", "favicon.ico", "apple-touch-icon.png", "assets/fonts/hanken-grotesk.woff2"):
        print(f"{(ROOT / p).stat().st_size:>7}  {p}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
