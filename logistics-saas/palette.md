# Logistics SaaS — colour system

Built with `colour-skill`. Category: B2B SaaS, operations tooling.
Audience: dispatch and ops staff, on screen most of a working day.
Primary action: create a booking; secondary: resolve an exception.

## Why this direction

Cool grey (`#F5F6F8`) is the default for logistics dashboards and is exactly why
they all look alike. The surface here is a warm-leaning neutral, which reads
current without costing any legibility. The accent is Luminous Blue — the 2027
Colour of the Year — doing the job navy usually does, with more energy.

The real domain problem is not the accent. It is that **logistics needs a status
scale, not a success/error pair.** Five states have to be told apart instantly
in a dense table: queued, in transit, delivered, delayed, exception. That is the
part most palettes get wrong.

## Tokens — light

| Token | Hex | Role | Contrast |
|---|---|---|---|
| surface | `#F7F6F3` | App canvas | — |
| raised | `#FFFFFF` | Cards, table, panels | — |
| sunken | `#EDEBE6` | Inputs, table header, hover rows | — |
| border | `#DBD7CF` | Hairlines and dividers only | 1.3:1 |
| border-strong | `#8E897C` | Input and secondary button outlines | 3.2:1 |
| ink | `#12151C` | Body text | 16.9:1 |
| ink-muted | `#4E5364` | Labels, captions, secondary | 7.1:1 |
| ink-inverse | `#FFFFFF` | Text on accent | 8.0:1 |
| accent | `#1E3FCB` | CTA, links, active nav, focus ring | 7.4:1 |
| accent-hover | `#152FA0` | Button hover | — |
| accent-quiet | `#E3E7F8` | Selected rows, active nav background | accent on it 6.5:1 |

## Tokens — dark

| Token | Hex | Contrast on surface |
|---|---|---|
| surface | `#12151C` | — |
| raised | `#1A1F29` | — |
| sunken | `#0C0F14` | — |
| border | `#2B323E` | 1.4:1 |
| border-strong | `#5C6676` | 3.2:1 |
| ink | `#E7E9EE` | 15.0:1 |
| ink-muted | `#9AA3B2` | 7.2:1 |
| ink-inverse | `#12151C` | on accent 6.0:1 |
| accent | `#6E8CFF` | 6.0:1 |
| accent-hover | `#8AA2FF` | — |
| accent-quiet | `#1B2440` | accent on it 5.0:1 |

Dark mode is rebuilt, not inverted. The accent is lifted roughly 20% in
lightness because the light-mode cobalt disappears against a dark surface.

## Status scale

| State | Light | Dark | Light bg | Dark bg | Marker |
|---|---|---|---|---|---|
| Queued | `#5B6478` | `#9AA3B2` | `#E9EAEE` | `#222836` | `·` |
| In transit | `#0E6E8C` | `#4FB8D8` | `#DEEEF4` | `#13303B` | `→` |
| Delivered | `#116B45` | `#4FBD8A` | `#DDEEE6` | `#133026` | `✓` |
| Delayed | `#8A5B06` | `#E0A63B` | `#F6EBD5` | `#332612` | `!` |
| Exception | `#A8241D` | `#F0837A` | `#F7E0DE` | `#361D1C` | `×` |

All five clear 5.3:1 on both surfaces in both modes.

**Every status chip carries a glyph as well as a colour.** Around one in twelve
men has a red-green deficiency, and delayed-versus-exception is precisely the
pair that collapses. The glyph is not decoration — it is the actual signal for
those users, and the colour is the accelerator for everyone else.

## Usage rules

- **accent**: the New booking button, links, active nav, focus rings. Nothing
  else. If a status ever borrows the accent, in-transit stops meaning anything.
- **border** is for dividers. Anything a user has to aim at — inputs, secondary
  buttons — uses **border-strong**, which clears 3:1.
- **sunken** for table headers, input fields, and row hover. Never for a card.
- Status colours appear only in chips, alert dots, and the status-mix bar. They
  never colour body text or a background a user reads against.
- KPI deltas use delivered/exception, but always with a `+` or `−` sign in front.
- Focus ring: 2px solid accent, 1px offset. Never remove it — ops staff run this
  tool on a keyboard.

## CSS

```css
:root{
  --surface:#F7F6F3; --raised:#FFFFFF; --sunken:#EDEBE6;
  --border:#DBD7CF; --border-strong:#8E897C;
  --ink:#12151C; --ink-muted:#4E5364; --ink-inverse:#FFFFFF;
  --accent:#1E3FCB; --accent-hover:#152FA0; --accent-quiet:#E3E7F8;
  --queued:#5B6478; --transit:#0E6E8C; --delivered:#116B45;
  --delayed:#8A5B06; --exception:#A8241D;
  --queued-bg:#E9EAEE; --transit-bg:#DEEEF4; --delivered-bg:#DDEEE6;
  --delayed-bg:#F6EBD5; --exception-bg:#F7E0DE;
}
[data-theme="dark"]{
  --surface:#12151C; --raised:#1A1F29; --sunken:#0C0F14;
  --border:#2B323E; --border-strong:#5C6676;
  --ink:#E7E9EE; --ink-muted:#9AA3B2; --ink-inverse:#12151C;
  --accent:#6E8CFF; --accent-hover:#8AA2FF; --accent-quiet:#1B2440;
  --queued:#9AA3B2; --transit:#4FB8D8; --delivered:#4FBD8A;
  --delayed:#E0A63B; --exception:#F0837A;
  --queued-bg:#222836; --transit-bg:#13303B; --delivered-bg:#133026;
  --delayed-bg:#332612; --exception-bg:#361D1C;
}
```

## Thai interfaces

Thai glyphs carry tone marks above and below the baseline, so muted text that
reads cleanly in Latin at 7:1 goes fuzzy in Thai at 12–13px. The Thai build
overrides these tokens; everything else stays identical.

| Token | EN light | TH light | EN dark | TH dark |
|---|---|---|---|---|
| ink-muted | `#4E5364` | `#3F4454` | `#9AA3B2` | `#B3BBC8` |
| queued | `#5B6478` | `#4E576B` | `#9AA3B2` | `#B3BBC8` |
| transit | `#0E6E8C` | `#0B5F7A` | `#4FB8D8` | `#6FC7E2` |
| delivered | `#116B45` | `#0E5C3B` | `#4FBD8A` | `#6BCB9E` |
| delayed | `#8A5B06` | `#754D05` | `#E0A63B` | `#E8B558` |
| exception | `#A8241D` | `#93201A` | `#F0837A` | `#F59B93` |

Muted text goes from 7.1:1 to 9.0:1, and every status chip clears 7:1.

```css
html[lang="th"]{
  --ink-muted:#3F4454;
  --queued:#4E576B; --transit:#0B5F7A; --delivered:#0E5C3B;
  --delayed:#754D05; --exception:#93201A;
  --lead:1.7; --row-pad:14px; --fs:15.5px;
}
html[lang="th"][data-theme="dark"]{
  --ink-muted:#B3BBC8;
  --queued:#B3BBC8; --transit:#6FC7E2; --delivered:#6BCB9E;
  --delayed:#E8B558; --exception:#F59B93;
}
html[lang="th"] body{
  font-family:'IBM Plex Sans Thai', sans-serif;
  letter-spacing:0;                      /* mandatory — tracking splits Thai clusters */
}
html[lang="th"] h1{letter-spacing:0;}    /* reset the Latin display tracking */
html[lang="th"] .num{font-family:'Inter Tight', sans-serif;}
```

Beyond colour: base size goes 14.5 → 15.5px, line-height 1.5 → 1.7, and table
row padding 11 → 14px. Rows get taller and that is correct — do not claw the
space back by shrinking the type. Reference numbers, lane codes, dates and KPI
figures stay in the Latin face via `.num`, because Thai numerals are not used in
operational tooling and the Latin face has better tabular alignment.
