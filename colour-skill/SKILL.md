---
name: colour-skill
description: Build a complete, on-trend, accessibility-checked colour system for any website, landing page, app UI, brand refresh, or client deck — grounded in the 2026–2027 colour forecast (Pantone Cloud Dancer, WGSN x Coloro Luminous Blue) and in per-industry web conventions. Use this skill whenever the user mentions colour, color, palette, hex codes, brand colours, "what colour should I use", theming, dark mode, design tokens, CSS variables, a rebrand, a moodboard, or asks you to design or restyle any website, landing page, dashboard, deck, or social template — even if they don't say the word "palette". Also use it when reviewing an existing design for contrast, accessibility, or brand consistency.
---

# Colour Skill

Turn a vague brief ("make it look modern", "something calm for a clinic") into a
named, documented colour system with real hex values, WCAG contrast evidence, and
usage rules a developer or Canva designer can follow without asking follow-ups.

## The 60-second version

1. **Pin the brief**: category, audience, region, light/dark, what must convert.
2. **Pick the neutral first, accent second.** The neutral is 80–90% of the pixels
   and decides whether the site feels 2021 or 2027. Never start with the accent.
3. **Build exactly 12 tokens** (see Token set below). Not 40. Not 5.
4. **Prove contrast** before shipping. Every text/background pair gets a ratio.
5. **Ship in three formats**: a token table, a CSS `:root` block, and a
   plain-language usage rule per token.

Never hand back a loose list of pretty hex codes. That is a moodboard, not a system.

## Step 1 — Pin the brief

Ask only what you can't infer. Minimum you need:

| Input | Why it matters |
|---|---|
| Website category | Decides the palette family — see `references/category-palettes.md` |
| Audience age / market | Older or medical audiences need higher contrast and fewer hues |
| Region | Colour meaning is not universal — see Regional notes below |
| Light, dark, or both | Dark mode is not "invert the hex", it needs its own ramp |
| Primary conversion action | The accent exists to serve this and nothing else |
| Existing brand assets | Logo colour is a constraint, not a suggestion |

If the user has a logo or existing site, sample from it and work around it rather
than proposing a replacement, unless they asked for a rebrand.

## Step 2 — Choose the direction

Read `references/trend-2027.md` for the forecast detail and the exact
approximate hex values. The short version of where colour is heading:

- **Neutrals carry the design now.** Pantone's 2026 Colour of the Year is
  Cloud Dancer, a soft white. Pure `#FFFFFF` reads as cheap and clinical;
  warm or mineral off-whites (`#F0EEE9`, `#F8F5F1`) read as considered.
- **One saturated accent, used rarely.** WGSN x Coloro's 2027 Colour of the Year
  is Luminous Blue, a cobalt that deliberately bridges "natural" and "digital".
- **Earth tones stay, but as neutrals, not as the whole palette.** Clay, russet,
  and mineral beige are the supporting cast for 2027, not the star.
- **Dark mode becomes designed, not inverted.** Deep Green is being positioned as
  the new black — a dark surface with a hue in it.

Pick **one dominant direction plus one accent direction**. Two dominant
directions is how palettes fall apart.

## Step 3 — The token set

Always produce exactly these twelve. Name them by role, never by colour
("accent", not "blue") so the system survives a rebrand.

```
surface          the main canvas
surface-raised   cards, panels, sidebars
surface-sunken   input fields, code blocks, wells
border           hairlines and dividers
ink              body text
ink-muted        captions, labels, secondary text
ink-inverse      text sitting on accent or on dark surfaces
accent           the single brand colour — CTAs, links, active states
accent-hover     one step darker or lighter, for interaction feedback
accent-quiet     8–12% tint of accent, for selected rows and badges
positive         success, confirmation, in-stock
critical         errors, destructive actions, expiry
```

Rules that go with them:

- The accent appears on **less than 10% of any screen**. If it's everywhere,
  nothing is emphasised.
- `positive` and `critical` are never the accent, even if the brand is green or red.
- Never carry meaning in hue alone — pair every status colour with an icon or label.
- Gradients are for atmosphere on large surfaces only, never behind body text.

## Step 4 — Prove contrast

Before presenting anything, compute and state the ratio for:
`ink` on `surface`, `ink-muted` on `surface`, `ink-inverse` on `accent`,
and `accent` on `surface`.

Targets: **4.5:1** for body text, **3:1** for text 24px+ or bold 19px+, and
**3:1** for button edges, icons, and focus rings against their background.

Contrast ratio = `(L1 + 0.05) / (L2 + 0.05)` where L is relative luminance.
If computing by hand is slow, write a five-line script — don't estimate.

If a trend colour fails, **keep the hue and change the lightness**, don't abandon
the direction. Luminous Blue at its true value fails as body text on white; it
passes comfortably as a button fill with white text.

## Step 5 — Deliver

Three blocks, in this order:

1. **Token table** — token, hex, role, contrast note.
2. **CSS** — a `:root` block, plus a `[data-theme="dark"]` block if dark mode
   was requested. Use the same token names in both.
3. **Usage rules** — one plain sentence per token, written for whoever is
   actually building it. If the client works in Canva rather than code, give the
   same values as a Brand Kit list with "use this for headings / backgrounds /
   buttons" phrasing instead of CSS.

Add a one-line rationale tying the palette to the brief. Not a paragraph of
colour-psychology filler — one line, e.g. "Mineral neutral base keeps a
treatment-heavy page calm; the cobalt is reserved entirely for booking CTAs."

## Regional notes

- **Any Thai content**: stop and read `references/thai-typography.md` before
  setting type or finalising muted-text values. Thai needs ~5.5:1 for body copy,
  `letter-spacing: 0`, and line-height around 1.8.
- **Thailand / SEA**: high-saturation palettes perform well in social and LINE
  creative but the same saturation on a landing page reduces perceived
  credibility for medical and financial services. Split the system: a calm web
  palette and a louder social palette that share the same accent.
- **Medical and clinic sites (Thailand)**: regulators respond badly to visuals
  that imply guaranteed outcomes. Avoid gold/"luxury" gradients and dramatic
  before/after colour grading that exaggerates results — the copy rules and the
  colour choices get read together.
- **Purple** reads as innovation in Western B2B, but as mourning in parts of
  Latin America and Southern Europe. **White** carries funeral associations in
  parts of East Asia — pair it with warmth if the market is Chinese or Korean.

## Common failure modes

| Symptom | Fix |
|---|---|
| "It looks AI-generated" | You used cream `#F4F1EA` + terracotta `#D97757` + a high-contrast serif. Change the neutral's temperature. |
| Palette looks muddy | Too many mid-tones. Force distance: very light surface, very dark ink, one saturated accent. |
| CTA doesn't stand out | The accent is being used decoratively elsewhere. Remove it from everything but actions. |
| Dark mode looks dirty | You inverted rather than rebuilt. Dark surfaces need a hue (not `#000`), and the accent usually needs lifting 10–15% in lightness. |
| Client keeps asking for changes | You showed colours without roles. Re-present as a token table with usage rules. |

## Related skill

Once the palette exists, **`color-pattern`** turns it into seamless tileable SVG
backgrounds and textures. Hand it the finished palette — background colour
first, motif colours after — rather than inventing new colours there.

## Reference files

- `references/trend-2027.md` — the 2026–2027 forecast, sources, approximate hex
  values, and how each trend colour behaves on screen. Read when choosing a
  direction or when the user asks "what's trending".
- `references/category-palettes.md` — ready palettes for 18 website categories
  with tokens and contrast notes. Read when the category is known.
- `references/thai-typography.md` — Thai type selection, line-height and
  letter-spacing rules, contrast adjustments for Thai text, and how to structure
  a TH/EN bilingual site. **Read this whenever any Thai content is involved** —
  a palette that passes in English can fail in Thai.
