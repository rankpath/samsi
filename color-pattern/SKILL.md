---
name: color-pattern
description: Generate seamless, tileable SVG background patterns coloured from a palette — dots, stripes, terrazzo, waves, scallop, herringbone, chevron, triangles, arcs and more — as web backgrounds, brand textures, packaging, social templates, or digital products for sale. Use whenever the user asks for a pattern, texture, background, ลาย, ลายพื้นหลัง, seamless tile, repeating graphic, wallpaper, or wants a palette turned into usable graphics. Also use when a design needs a background that is not a flat colour or a photo. Covers tiling maths, how to recolour a tile into colourways, and exporting at sellable sizes.
---

# Color Pattern

Turn a palette into seamless tiles that repeat with no visible seam, in
colourways that stay on-brand.

**Use `scripts/patterns.py` — do not hand-write SVG pattern maths.** Tiling
errors are invisible in a single tile and obvious once repeated, and the script
already handles edge wrapping.

## Quick start

```bash
python3 scripts/patterns.py --list
python3 scripts/patterns.py \
  --palette "#F0EEE9,#1E3FCB,#EBB13C,#8B4A33" \
  --out ./out --title "Client pattern set"
```

The first colour is always the background; every colour after it is a motif
colour. Output is one `.svg` per pattern plus `index.html`, a contact sheet
showing each tile actually repeating.

Flags: `--only dots,waves,terrazzo` to pick patterns, `--seed 42` to reshuffle
the randomised ones (scatter, terrazzo, arcs), `--out` for the folder.

## The workflow

1. **Get the palette.** If the user has one, use it. If not, build one first —
   that is the **`colour-skill`**'s job, not this one — it builds the twelve-token
   system and proves contrast. Do not invent colours here. Feed the finished
   palette in as `--palette "surface,accent,…"`, surface first.
2. **Decide the pattern's job** before picking a style. See the table below.
3. **Generate a set, not a single tile.** Users pick from options; generating
   one and defending it wastes a round trip.
4. **Show the contact sheet, not the tiles.** A tile viewed alone tells you
   nothing about whether it repeats well.
5. **Cut to a shortlist of three**, with a sentence on where each one belongs.

## Choosing a pattern for the job

| The pattern must… | Use | Avoid |
|---|---|---|
| Sit behind body text | grid, dots, crosses at low contrast | terrazzo, stripes, checker |
| Fill a hero or section band | waves, scallop, arcs, chevron | grid (reads as a spreadsheet) |
| Read as premium or crafted | herringbone, scallop, arcs | checker, halftone-style dots |
| Read as playful | terrazzo, scatter, triangles, dots | grid, stripes |
| Work on packaging or print | stripes, herringbone, terrazzo | anything with hairlines under 1pt |
| Work as a tiny avatar or favicon | checker, triangles, chevron | scatter, terrazzo, grid |

## Contrast rules — the opposite of interface rules

A palette that passes WCAG makes a **bad** background pattern. The rule inverts:

- **Behind text: keep motif and background within ~1.3:1.** Tint the motif, or
  drop it to 8–15% opacity. If you can read the pattern, you cannot read the text.
- **As a feature: go to full strength**, but then nothing else sits on top of it.
- **Never put a pattern behind body copy in dark mode** unless the motif is
  within a few percent of the surface lightness — light-on-dark blooms.
- **Scale is contrast.** The same tile at 40px reads as texture and at 300px
  reads as graphic. Test at the size it will actually be used.

## Colourways

A pattern sells or ships as a set, not a single file. Standard set of four from
one palette:

1. **Full** — background plus every motif colour.
2. **Duotone** — background plus the accent only.
3. **Tonal** — background plus one motif colour at 15% opacity. This is the one
   that actually gets used behind text.
4. **Inverted** — darkest colour as background, lightest as motif.

Generate each by reordering the `--palette` argument rather than editing SVG.

## Export

SVG is the master. It scales without loss and the colours stay editable — keep
it as the working file.

For raster delivery, render the tile at the pixel size it will repeat at, not
larger. A tile exported at 2000px and displayed at 100px looks soft.

| Use | Tile export | Notes |
|---|---|---|
| Web background | 200–600px PNG, or the SVG itself | SVG is smaller for flat-colour patterns |
| Social template | 1080×1080 filled, not the bare tile | Build the repeat into the canvas |
| Print / packaging | SVG or 300dpi at final size | Confirm CMYK conversion of the accent |
| Sold as a product | SVG + PNG at 3000×3000 + a JPG preview | Include a colourway sheet in the listing |

Rendering to PNG: `cairosvg tile.svg -o tile.png --output-width 600`

## Rules that prevent the two common failures

**Seams.** A motif that crosses the tile edge must reappear on the opposite
edge. The script does this by drawing every motif nine times at offsets of
±W and ±H; the SVG viewBox clips the overflow. Any motif spacing must divide the
tile size exactly — 200 ÷ 40 works, 200 ÷ 14 does not. See
`references/tiling.md` for the full maths and the failure cases.

**Visible repeat.** Seamless is not the same as invisible. Random placement
leaves voids, and the eye locks onto a repeating void faster than onto a
repeating motif. Use a jittered grid instead of pure random, and never use a
one-directional size or colour ramp inside a tile — it always bands.

Always verify by rendering the tile repeated at least 2×2 and looking at it.
Do not ship a tile you have only seen once.

## Reference files

- `references/tiling.md` — seamless tiling maths, the nine-copy method, which
  spacings are legal, and how to debug a seam.
- `scripts/patterns.py` — the generator. Read `--list` output before promising a
  user a pattern style that does not exist yet; adding one is about 10 lines.
