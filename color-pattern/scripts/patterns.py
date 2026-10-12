#!/usr/bin/env python3
"""
Seamless SVG pattern tiles from a palette.

Every motif is emitted nine times (dx, dy in -W, 0, +W / -H, 0, +H) so anything
crossing a tile edge reappears on the opposite edge. The SVG root clips to the
viewBox, so the visible result is one tile that repeats with no seam.

  python3 patterns.py --palette "#F0EEE9,#1E3FCB,#EBB13C" --out ./out
  python3 patterns.py --list
"""
import argparse, math, os, random

W = H = 200  # tile size in user units; scale on export, not here


# ---------------------------------------------------------------- helpers
def wrap(body):
    """Nine translated copies so motifs wrap across every edge."""
    out = []
    for dx in (-W, 0, W):
        for dy in (-H, 0, H):
            out.append(f'<g transform="translate({dx},{dy})">{body}</g>')
    return "".join(out)


def svg(body, bg):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}">'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>{body}</svg>')


def pick(pal, i):
    """Motif colours are everything after the background."""
    motif = pal[1:] or pal
    return motif[i % len(motif)]


# ---------------------------------------------------------------- patterns
def p_dots(pal, seed):
    n, r = 4, 9
    step = W / n
    b = "".join(
        f'<circle cx="{c*step+step/2:.2f}" cy="{r_*step+step/2:.2f}" r="{r}" '
        f'fill="{pick(pal,(c+r_))}"/>'
        for r_ in range(n) for c in range(n))
    return svg(wrap(b), pal[0])


def p_scatter(pal, seed):
    """Jittered grid, not pure random. Random placement leaves voids, and a
    void is what makes the repeat visible to the eye."""
    rng = random.Random(seed)
    n = 6
    step = W / n
    parts = []
    for r in range(n):
        for c in range(n):
            x = c * step + rng.uniform(.15, .85) * step
            y = r * step + rng.uniform(.15, .85) * step
            parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" '
                         f'r="{rng.uniform(4,9):.2f}" fill="{pick(pal,r+c)}" '
                         f'opacity="{rng.uniform(.65,1):.2f}"/>')
    return svg(wrap("".join(parts)), pal[0])


def p_stripes(pal, seed):
    """Slope-1 lines spaced by a divisor of W. W == H, so a shift of one tile
    in either axis maps the line set onto itself."""
    step = 40                      # must divide W
    nrep = W // step               # colour cycle must match the geometry cycle
    parts = []
    for i in range(-5, 11):
        c = i * step
        parts.append(f'<path d="M {-H} {-H+c} L {2*W} {2*W+c}" stroke="{pick(pal,i % nrep)}" '
                     f'stroke-width="13" fill="none"/>')
    return svg("".join(parts), pal[0])


def p_grid(pal, seed):
    c = pick(pal, 0)
    b = "".join(f'<line x1="{i*40}" y1="0" x2="{i*40}" y2="{H}" stroke="{c}" stroke-width="2"/>'
                f'<line x1="0" y1="{i*40}" x2="{W}" y2="{i*40}" stroke="{c}" stroke-width="2"/>'
                for i in range(6))
    return svg(wrap(b), pal[0])


def p_checker(pal, seed):
    s = W / 4
    b = "".join(
        f'<rect x="{c*s}" y="{r*s}" width="{s}" height="{s}" fill="{pick(pal,0)}"/>'
        for r in range(4) for c in range(4) if (r + c) % 2 == 0)
    return svg(b, pal[0])


def p_terrazzo(pal, seed):
    rng = random.Random(seed)
    n = 7
    step = W / n
    parts = []
    for r in range(n):
        for c in range(n):
            x = c * step + rng.uniform(.1, .9) * step
            y = r * step + rng.uniform(.1, .9) * step
            sides = rng.randint(3, 6)
            rad = rng.uniform(4, 9)
            pts = []
            for k in range(sides):
                a = 2 * math.pi * k / sides + rng.uniform(-.3, .3)
                rr = rad * rng.uniform(.6, 1.3)
                pts.append(f"{x+rr*math.cos(a):.1f},{y+rr*math.sin(a):.1f}")
            parts.append(f'<polygon points="{" ".join(pts)}" fill="{pick(pal,r+c)}" '
                         f'opacity="{rng.uniform(.65,1):.2f}"/>')
    return svg(wrap("".join(parts)), pal[0])


def p_waves(pal, seed):
    rows = 5
    step = H / rows
    parts = []
    for r in range(rows):
        y = r * step
        d = f"M 0 {y:.1f}"
        for x in range(0, W + 1, 10):
            d += f" L {x} {y + math.sin(x / W * 2 * math.pi * 2) * 9:.2f}"
        parts.append(f'<path d="{d}" fill="none" stroke="{pick(pal,r % rows)}" '
                     f'stroke-width="3" stroke-linecap="round"/>')
    return svg(wrap("".join(parts)), pal[0])


def p_scallop(pal, seed):
    r = 25                         # 2r * 4 == W
    step = H / 4                   # even row count keeps the half-drop aligned
    parts = []
    for row in range(5):
        y = row * step
        off = 0 if row % 2 == 0 else r
        for col in range(-1, 5):
            x = col * r * 2 + off
            parts.append(f'<path d="M {x} {y} a {r} {r} 0 0 0 {2*r} 0" fill="none" '
                         f'stroke="{pick(pal,row)}" stroke-width="3"/>')
    return svg(wrap("".join(parts)), pal[0])


def p_crosses(pal, seed):
    n, a, t = 4, 11, 3.5
    step = W / n
    parts = []
    for r in range(n):
        for c in range(n):
            x, y = c * step + step / 2, r * step + step / 2
            col = pick(pal, r + c)
            parts.append(f'<rect x="{x-a:.1f}" y="{y-t/2:.1f}" width="{2*a}" height="{t}" fill="{col}"/>'
                         f'<rect x="{x-t/2:.1f}" y="{y-a:.1f}" width="{t}" height="{2*a}" fill="{col}"/>')
    return svg(wrap("".join(parts)), pal[0])


def p_triangles(pal, seed):
    s = W / 4
    parts = []
    for r in range(4):
        for c in range(4):
            x, y = c * s, r * s
            up = (r + c) % 2 == 0
            pts = (f"{x},{y+s} {x+s/2},{y} {x+s},{y+s}" if up
                   else f"{x},{y} {x+s},{y} {x+s/2},{y+s}")
            parts.append(f'<polygon points="{pts}" fill="{pick(pal,r+c)}"/>')
    return svg("".join(parts), pal[0])


def p_arcs(pal, seed):
    rng = random.Random(seed)
    s = W / 4
    parts = []
    for r in range(4):
        for c in range(4):
            x, y = c * s, r * s
            rot = rng.choice([0, 90, 180, 270])
            parts.append(
                f'<g transform="rotate({rot} {x+s/2} {y+s/2})">'
                f'<path d="M {x} {y+s} A {s} {s} 0 0 1 {x+s} {y}" fill="none" '
                f'stroke="{pick(pal,r+c)}" stroke-width="7"/></g>')
    return svg(wrap("".join(parts)), pal[0])


def p_herringbone(pal, seed):
    bw, bh = 50, 20             # 4 cols, 10 rows — both whole numbers
    parts = []
    for r in range(-1, 11):
        for c in range(-1, 5):
            x = c * bw + (r % 2) * bw / 2   # row count is even, so the offset wraps
            y = r * bh
            rot = 45 if (r + c) % 2 == 0 else -45
            parts.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" '
                         f'fill="{pick(pal,r+c)}" transform="rotate({rot} {x+bw/2} {y+bh/2})"/>')
    return svg(wrap("".join(parts)), pal[0])


def p_chevron(pal, seed):
    rows, cols = 5, 4
    sh, sw = H / rows, W / cols
    parts = []
    for r in range(rows):
        for c in range(cols):
            x, y = c * sw, r * sh
            parts.append(f'<path d="M {x} {y+sh*.75} L {x+sw/2} {y+sh*.25} '
                         f'L {x+sw} {y+sh*.75}" fill="none" stroke="{pick(pal,r)}" '
                         f'stroke-width="7" stroke-linecap="square"/>')
    return svg(wrap("".join(parts)), pal[0])


PATTERNS = {
    "dots": p_dots, "scatter": p_scatter, "stripes": p_stripes, "grid": p_grid,
    "checker": p_checker, "terrazzo": p_terrazzo, "waves": p_waves,
    "scallop": p_scallop, "crosses": p_crosses, "triangles": p_triangles,
    "arcs": p_arcs, "herringbone": p_herringbone, "chevron": p_chevron,
}


# ---------------------------------------------------------------- contact sheet
def sheet(names, pal, outdir, title):
    cards = "".join(
        f'<figure><div class="tile" style="background-image:url({n}.svg)"></div>'
        f'<figcaption>{n}</figcaption></figure>' for n in names)
    chips = "".join(f'<span style="background:{c}"></span>' for c in pal)
    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
body{{margin:0;background:#F0EEE9;color:#14161C;font:16px/1.55 system-ui,sans-serif;padding:28px;}}
h1{{font-size:22px;margin:0 0 6px;letter-spacing:-.02em;}}
p{{margin:0 0 6px;color:#4E5364;font-size:14px;}}
.chips{{display:flex;gap:6px;margin:14px 0 26px;}}
.chips span{{width:34px;height:34px;border-radius:3px;border:1px solid rgba(0,0,0,.14);}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:18px;}}
figure{{margin:0;}}
.tile{{height:190px;border:1px solid #D6D2C8;border-radius:3px;background-size:100px 100px;background-repeat:repeat;}}
figcaption{{font-size:13px;color:#4E5364;margin-top:7px;}}
</style></head><body>
<h1>{title}</h1><p>Each swatch is one 200×200 tile repeating at 100px. Seams should be invisible.</p>
<div class="chips">{chips}</div><div class="grid">{cards}</div></body></html>"""
    open(os.path.join(outdir, "index.html"), "w", encoding="utf-8").write(html)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--palette", default="#F0EEE9,#1E3FCB,#EBB13C,#8B4A33",
                    help="comma-separated hex; the first one is the background")
    ap.add_argument("--out", default="./out")
    ap.add_argument("--only", default="", help="comma-separated pattern names")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--title", default="Pattern set")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    if a.list:
        print("\n".join(PATTERNS))
        return

    pal = [c.strip() for c in a.palette.split(",") if c.strip()]
    names = [n.strip() for n in a.only.split(",") if n.strip()] or list(PATTERNS)
    os.makedirs(a.out, exist_ok=True)
    for n in names:
        open(os.path.join(a.out, n + ".svg"), "w", encoding="utf-8").write(
            PATTERNS[n](pal, a.seed))
    sheet(names, pal, a.out, a.title)
    print(f"{len(names)} tiles + contact sheet written to {a.out}")


if __name__ == "__main__":
    main()
