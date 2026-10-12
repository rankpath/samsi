# Seamless tiling — the maths and the failure cases

## The nine-copy method

A tile is seamless when translating it by exactly one tile width or height maps
the artwork onto itself. The general way to guarantee that, without clever
per-pattern geometry, is to draw every motif nine times:

```
for dx in (-W, 0, +W):
    for dy in (-H, 0, +H):
        <g transform="translate(dx,dy)"> …motifs… </g>
```

An SVG root element clips to its viewBox, so the eight extra copies are invisible
except where they poke into the tile from outside — which is precisely the
content that must appear there for the edges to meet.

Cost is nine times the node count. For flat-colour patterns this is irrelevant.
For anything with hundreds of motifs, generate the tile and then flatten it.

## Which spacings are legal

If a motif repeats every `p` units, then `W` must be an exact multiple of `p`.
This is the single most common cause of a seam.

- `W = 200`, `p = 40` → 5 repeats. Legal.
- `W = 200`, `p = 14` → 14.28 repeats. **Seam.**
- `W = 200`, `p = 25` → 8 repeats. Legal.

For **half-drop** patterns (every other row offset by half a step, like scallop
or herringbone), the number of rows must additionally be **even**, or the offset
lands on the wrong phase at the seam.

For **45° diagonals**, do not rotate a set of vertical bars — a rotation about
the tile centre does not commute with the tile translation. Draw lines of slope
1 instead (`y = x + c`), spaced by a divisor of `W`, and require `W == H`. Then a
shift of one tile in either axis maps the line set onto itself.

## Colour cycles must match geometry cycles

Geometry can tile perfectly while colour does not. If the tile contains `n`
repeats of a motif and the palette has `m` motif colours, the colour index must
be periodic with `n`, not with `m`:

```python
# wrong — colour(i) != colour(i + n) unless m divides n
fill = motif[i % m]

# right
fill = motif[(i % n) % m]
```

Symptom: the shapes line up across the seam but the colours jump.

## Ramps always band

Any property that varies monotonically across the tile — dot size growing top to
bottom, opacity fading left to right, a colour gradient — cannot meet itself at
the seam. The tile is technically seamless only if the ramp wraps, and a wrapped
ramp reads as visible banding when repeated.

If you need a fade, apply it as a separate gradient layer over a uniform tile.
Do not build it into the tile.

## Debugging a seam

1. Render the tile to PNG at its natural size.
2. Paste it into a 2×2 grid.
3. Look at it. This catches more than any metric.

Automated checks are unreliable here: comparing the wrap edge against interior
pixel differences flags every pattern whose legitimate feature boundary happens
to fall on the tile edge — a checkerboard fails a naive seam test while being
perfectly seamless. Use the metric to shortlist, then use your eyes to decide.

If a seam is real, it is almost always one of:

| Symptom | Cause |
|---|---|
| Hard line at one edge only | A motif drawn at both `0` and `W`, doubling the stroke |
| Shapes cut in half at the edge | Missing the nine-copy wrap |
| Shapes align, colours jump | Colour cycle does not divide the geometry cycle |
| Regular grid of gaps in a random pattern | Pure random placement leaving voids |
| Bands across the repeat | A ramp built into the tile |
