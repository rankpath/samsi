# Thai and bilingual (TH/EN) websites

Read this whenever the site has any Thai content. Thai is not English with
different glyphs — it breaks four assumptions baked into most Latin-first design
systems, and a palette that passes in English can fail in Thai.

## 1. Why colour choices change

Thai glyphs stack. Vowels and tone marks sit above and below the baseline, so a
line of Thai text has more ink and more vertical complexity than Latin at the
same size. Consequences for the palette:

- **Muted text needs more contrast in Thai.** A `#5B6072` on `#F0EEE9` that reads
  fine in English gets fuzzy in Thai at 14px. For Thai body copy target **5.5:1
  minimum** rather than 4.5:1, or raise the size.
- **Thin weights collapse.** Thai at weight 300 loses its tone marks on low-DPI
  screens. Body text should be 400 minimum, and small labels 500.
- **Low-chroma text on tinted surfaces is riskier.** Keep accent-coloured body
  text out of Thai layouts entirely; accent belongs on buttons and links only.
- **Dark mode hurts Thai more.** Light-on-dark blooms and the tone marks merge
  into the ascender. On dark surfaces, avoid weights above 600 for Thai and give
  it slightly more line-height than the English version.

## 2. Typeface selection

Two families of Thai type, and the choice signals a lot:

| Style | Reads as | Use for | Google Fonts |
|---|---|---|---|
| Looped (มีหัว) | Official, trustworthy, readable | Government, medical, legal, education, anything for readers over 40 | Sarabun, Noto Sans Thai, IBM Plex Sans Thai Looped |
| Loopless (ไม่มีหัว) | Modern, designed, urban | Tech, fashion, F&B, creative, youth | Anuphan, IBM Plex Sans Thai, LINE Seed Sans TH |
| Display | Loud, promotional | Headlines only, never body | Kanit, Prompt, Chakra Petch, Bai Jamjuree |

Rules:
- **Never set Thai body copy in Kanit or Prompt.** They are display faces. This is
  the single most common mistake on Thai commercial sites.
- Match optical weight across scripts. Latin 600 usually needs Thai 600, but some
  Thai faces run heavy — check side by side rather than trusting the number.
- If the client is a hospital or clinic, default to **Sarabun or Noto Sans Thai**.
  Looped type carries institutional credibility that loopless does not.

## 3. Layout rules

- **Line-height**: Thai needs `1.75–1.9`. Latin at `1.5` looks generous; the same
  value clips Thai tone marks against the line above.
- **Letter-spacing must be `0` or `normal`.** Tracking splits Thai character
  clusters and makes words unreadable. Any `letter-spacing` you set for Latin
  headings has to be reset under `:lang(th)`.
- **No `text-transform: uppercase`.** Thai has no case; the rule does nothing to
  Thai and creates an inconsistent bilingual system.
- **Don't justify text.** Thai has no spaces between words, so browsers break
  lines at cluster boundaries. Justified Thai produces huge random gaps.
- **Thai runs 15–25% longer** than the same English copy. Buttons, nav items, and
  card headings need to flex, not be fixed-width. Design the Thai version first
  if you can — fitting English into a Thai-sized box always works, the reverse
  rarely does.
- **Bump Thai up 1–1.5px.** Thai at 16px reads smaller than Latin at 16px.

## 4. Building the two versions

Prefer **separate URLs** (`/th/` and `/en/`) over a JavaScript toggle if search
traffic matters. Google needs a crawlable URL per language, and Thai-language
search is where most local demand sits. A toggle is fine for a prototype or an
app-like product page.

Either way:

- Set `lang="th"` or `lang="en"` on `<html>` — it changes font fallback and line
  breaking, not just semantics.
- Add `hreflang` pairs for both versions plus `x-default`.
- Keep the **language switcher in the header, always visible**, labelled in the
  target language (`English` / `ไทย`), never as a flag. Flags mean countries,
  not languages.
- Translate the whole page or none of it. Half-translated pages read as
  abandoned and cost more trust than an English-only page would.
- Numbers, prices, and dates: Thai sites use Arabic numerals and the Gregorian
  calendar for commerce. Thai numerals and the Buddhist era belong in official
  and legal contexts — match what the client's competitors do.

## 5. CSS pattern

```css
:root { --leading-latin: 1.55; --leading-thai: 1.8; }

body { font-family: 'Inter Tight', sans-serif; line-height: var(--leading-latin); }

:lang(th), html[lang="th"] body {
  font-family: 'IBM Plex Sans Thai', 'Noto Sans Thai', sans-serif;
  line-height: var(--leading-thai);
  letter-spacing: 0;              /* mandatory reset */
  font-size: 1.06em;              /* optical size match */
}
html[lang="th"] h1,
html[lang="th"] h2 {
  font-family: 'Anuphan', sans-serif;
  letter-spacing: 0;              /* kills the Latin display tracking */
  line-height: 1.25;              /* tight Latin leading clips tone marks */
}
html[lang="th"] .label { text-transform: none; }
```

Always load the Thai family — do not rely on the system fallback. Thai system
fonts differ so much between iOS, Android and Windows that an unloaded fallback
changes the entire feel of the page.
