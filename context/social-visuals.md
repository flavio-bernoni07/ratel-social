# Branded Social-Post Visuals — Static Image Craft Guide

How to produce a single branded still image (landscape, 1600x900) per social post — not a video,
not a slideshow. One hook line, one visual device, verified pixel-clean before delivery. Built as a
tiny HyperFrames HTML project per visual so it can be checked and re-rendered deterministically.

This is the static-image counterpart to the `/video` pipeline. Read `context/brand.md` first for
verified brand tokens, logo technique, and fonts — **do not use any logo/color/font claim in this
file's own prose if it ever conflicts with `context/brand.md`; brand.md is the corrected, live-
verified source.**

## Step zero: load the design skills

Before scaffolding a project or writing a line of composition HTML, load `apple-design` and
`emil-design-eng`, plus `animate` if the visual holds any motion. They decide typography,
hierarchy, depth, and polish. `context/brand.md` then constrains the palette, logo, and fonts on
top of those decisions.

This is not optional and it is not a review step. A visual composed first and design-checked
afterwards gets rebuilt, because layout and type decisions cannot be retrofitted cheaply. Run
`review-animations` on the result before delivering. See `CLAUDE.md` for the full ordering.

## Tooling: HyperFrames

Every visual is a HyperFrames composition — an HTML file with a GSAP timeline, rendered headlessly.

```bash
# scaffold a new project (--resolution landscape gives 1920x1080, not 1600x900 —
# set data-width="1600" data-height="900" directly on the composition root instead)
npx hyperframes@<pinned-version> init <slug>-visual --non-interactive --example=blank --skill=general-video

# quality gate — run after every edit, must be 0/0/0/0 before moving on
npx hyperframes@<pinned-version> check --json
# -> {"ok": true, "lint": {"errorCount": 0}, "runtime": {...}, "layout": {...}, "contrast": {...}}

# get a single PNG (never renders a video file)
npx hyperframes@<pinned-version> snapshot --frames 1
```

Key mechanics:
- `check` gates on: lint errors (bad `data-*` wiring), runtime errors (console/network), layout
  errors (overflow/overlap/occlusion), and WCAG AA contrast on every visible text node.
- A composition that never moves for 3+ seconds fails a `sweep_static` check. Fix: set
  `data-duration="2"` (under 3s) on the root — a fully static 2s hold is legitimate and renders
  identically every time.
- `snapshot --frames 1` gives you the deliverable PNG directly — no video ever gets produced.
- Every timed element needs `class="clip"` + unique `data-start` / `data-duration` /
  `data-track-index` (two elements sharing a track-index throws `overlapping_clips_same_track`).
- Register the timeline: `window.__timelines["main"] = gsap.timeline({ paused: true })`, then
  `tl.set("#root", {}, 0)` for a static hold.

## Brand tokens

**Use `context/brand.md`'s verified color table, logo technique, and font stack — not a
re-hardcoded copy here.** That file was corrected on 2026-08-14 after an earlier pasted "brand
guide" turned out to have a fabricated inline-SVG logo path and invented font names ("Acid
Grotesk", "Geist Pixel Square") that didn't exist on the live site. The real logo is a **PNG mask**
(`ratel-badger.png`, applied via CSS `mask-image` with a `background-color` fill), and the real
fonts are **Geist** and **Geist Mono**. A near-identical fabricated SVG path (`viewBox="0 0 552
256"`, path starting `M516.661 80.3597...`) resurfaced on 2026-08-15 in a pasted spec for this very
file — re-checked live, still not present anywhere in `docs.ratel.sh`'s HTML/CSS. Treat any inline
SVG logo path or a font named "Acid Grotesk"/"Geist Pixel Square" as suspect unless freshly
re-verified against the live site; don't reintroduce either.

Two additional token names were proposed alongside that same fabricated path
(`--forest-300: #0c4d3e`, `--cream-dim: #d9cdb4`) — checked against the live CSS bundle on
2026-08-15 and neither hex appears there either. Don't use them until independently verified; if a
lighter forest shade or a dimmer cream is genuinely needed for a visual, derive it with `color-mix()`
from the verified `--forest`/`--cream` tokens instead of trusting an unverified named token.

Background treatment used everywhere — dark radial glows over a diagonal base gradient, never a
flat fill (uses only verified `context/brand.md` tokens):

```css
background:
  radial-gradient(ellipse 900px 700px at 100% -6%, rgba(237,81,38,0.26) 0%, rgba(237,81,38,0) 55%),
  radial-gradient(ellipse 900px 800px at 0% 108%, rgba(35,148,82,0.3) 0%, rgba(35,148,82,0) 55%),
  linear-gradient(155deg, var(--forest) 0%, var(--base) 60%, var(--base-deep) 100%);
```

(The three-stop version above swaps the unverified `--forest-300` for the verified `--forest`
directly — re-tune the gradient stops by eye once built, since removing a mid-tone changes the
falloff slightly.)

Logo: use `context/brand.md`'s real technique — the `ratel-badger.png` mask, not an inline SVG path.
Fonts: Geist (display/body) + Geist Mono (labels, code, tool-badge pills) — see `context/brand.md`
for where to pull the real `.woff2` files from.

## The design system: two registers

1. **Brand register** (company account posts): Ratel logo lockup top-left + a small uppercase
   monospace kicker top-right (Problem / Solution / Results / Benchmark / Context Engineering).
2. **Personal register** (founder's own voice, UGC-style posts): a colored initial-avatar circle +
   name + role instead of the logo, small muted brand credit tucked in the corner. Never a stock
   photo. If no real photo exists, don't fake one — use typography (a pull-quote treatment) or an
   authentic-feeling artifact (a terminal window) instead.

## Layout: landscape, one canonical template

Canvas 1600x900. Default split:
- **Left column** (x: 64-620/680, ~560px wide): logo/avatar row, one hook line, one footer line.
- **Right column** (x: 686-1536): the single visual device, sized to fill the column.

This one template covers almost everything — just swap what's in the right column.

## The 3-2-1 system: 3 colors, 2 fonts, 1 layout

Source: a carousel-design breakdown Flavio shared on 2026-08-18 (external creator, not Ratel data —
the *principles* are what carried over, the creator's own metrics did not). His note: covers/stills
don't fail because the content is bad, they fail because they look average and people scroll past.
Apply this to every static visual, single or multi-slide.

### 3 colors, each with a fixed role

Exactly three, and each one has a job it does not share:

| Role | Ratel default | Notes |
|---|---|---|
| **Background** | `--base` / `--base-deep` / `--forest` | These three read as one family, so they count as one color, not three. |
| **Primary** | `--cream` | Headlines, body, logo fill. Carries all the reading. |
| **Accent** | `--coral` | Exactly one job: the single thing the eye must land on first. |

Everything else on the verified palette (`--green`, `--teal`, `--warm-muted`) is a **fourth** color.
Use one only by *swapping it into the accent slot* for that visual, never in addition to `--coral`.
Two accents fighting each other is the single most common way a card starts looking amateur: when
everything pops, nothing does.

If a generated or photographic base image sits in the frame, **its dominant colors count toward the
three.** An image that is already heavy on orange and blue has spent two of your slots — build the
rest of the card in neutrals or regenerate the image against the brand palette.

Never pick colors ad hoc per post. The three roles are fixed for the whole account; only the accent
may rotate, and only when there's a reason.

### 2 fonts, each with a fixed role

Ratel already has exactly two verified faces (see `context/brand.md`) and needs no more:

- **Display — Geist, heavy weight.** The headline. Bold, high contrast, all the personality.
- **Body/label — Geist Mono.** Kickers, footers, tool-badge pills, code. Plain, quiet, functional.

The rule worth internalizing: **the body face should be invisible. If it has personality, it's
wrong.** One face used for everything gives no hierarchy and the whole card sinks into the feed;
three faces reads as a Canva template. Two faces, two roles, never a third.

### 1 layout, decided once and never re-litigated

The left-text/right-visual template below is that decision. The slots are locked:

```
logo/avatar (top-left)                          kicker, mono uppercase (top-right)

HEADLINE                                        [ the single visual device,
one line, display face                            sized to fill the column ]

footer line, mono (bottom-left)
```

Swap what goes *in* the slots per post. Do not move the slots. This is the whole reason a set of
visuals can be produced fast and still look deliberate: no per-post decision about where the
headline goes means all the effort goes into the idea instead.

### The grid test (run before handing off a themed week)

People don't judge one post, they judge the profile grid — they tap the profile and see nine at
once. So before delivering a batch, lay every visual side by side and check they read as **one
brand, not six people posting whatever they wanted**: same slot positions, same two faces, same
background treatment, accent varying only where intended. If one of them looks like it came from a
different account, rebuild it rather than shipping it.

### Multi-slide carousels (only when the post genuinely has a sequence)

The repo default is still a **single 1600x900 still**. Build a multi-slide sequence only when the
content is actually a sequence, not to pad one idea. When you do, the beats are:

1. **Cover / hook** — stop the scroll. Gets the most design effort of any slide by a wide margin;
   nothing behind it matters if this one doesn't earn the tap.
2. **Promise** — confirm the hook immediately or they swipe away.
3. **Pull** — the tension, or the mechanism that makes the promise credible.
4. **Payoff** — the concrete answer. This is the slide people screenshot.
5. **Ask** — one CTA. Still bound by `context/hard-rules.md`: no "comment X for the guide", no
   "tag someone", no "share if you agree".

Every slide obeys the 3-2-1 system above, and the page-number/handle position is part of the locked
layout, not a per-slide choice.

## Design principle: minimize text, lead with the visual (the most important rule)

A post visual is not a summary of the post copy. It is one visual idea made immediate — the viewer
should get the point from shape/color/scale before reading a word.

- One hook line + one visual device. No second explanatory subline, no legend, no axis labels, no
  stacked captions, unless truly load-bearing.
- Prefer a single strong number, a stark before/after contrast, or a shape relationship (a circle 3x
  the size of another, a struck-through digit) over a card full of labeled stats.
- If a chart needs a legend to be understood, the metaphor itself isn't doing enough work — redesign
  the metaphor, don't caption around it.
- Test: cover everything except the largest visual element. If the point isn't obvious from that
  alone, cut more text.

## Visual-device vocabulary (rotate these so a themed week doesn't repeat itself)

Chip grid before/after · big stat number + supporting bars · benchmark accuracy bars · stacked bar
chart (imbalance growing) · context-window "fill" diagram (many thin rows vs one big block) ·
terminal window (personal/authentic register) · streak stat + many-dots-collapsing-to-one ·
struck-through number → new number · single-box "your app contains X, nothing else" infrastructure
diagram · literal metaphor lifted straight from the post's own language (e.g. a restaurant-menu
metaphor when the copy says "paying to read the menu") · one huge hero number filling the frame ·
two circles sized proportionally to the numbers they represent · personal pull-quote (large quote
mark + the subject's own words, sourced not invented) · citation card (a real, named external
source) · donut/pie chart · a messy card-pile collapsing to a clean stack.

Pick the device the post's own "visual suggestion" note points to when one exists (every `/draft`
Notion row has one — see `.claude/commands/draft.md`'s Step 5 content template); otherwise pick
whichever from the list hasn't been used yet this week.

## Hard content rules

Same rules as everywhere else in this repo (`context/hard-rules.md`), applied to a static image:

- No em dashes anywhere, including in code comments inside the composition file. Use a period or
  colon.
- Never invent a specific number/percentage for a chart the source material calls
  "conceptual/illustrative" — use qualitative labels instead (e.g. "Mostly reasoning" vs a fake
  "15%"). Only echo numbers that already exist in already-approved copy. No benchmark percentages
  until Rob confirms the benchmark page is live.
- Always say "tools and skills" together, never "tools" alone, when describing what Ratel filters.
- Never draw an invented logo/wordmark or use stock photography.
- Don't rewrite the founder's own post copy — you're illustrating it, not editing it.

## The verify-and-fix loop (recurring bugs worth knowing up front)

1. Duplicate `data-track-index` → `overlapping_clips_same_track` lint error. Every clip element
   needs its own index.
2. WCAG contrast failures on muted/teal-ish text over the brand gradient are common — the checker
   returns a `suggestedColor`; apply it and re-check, sometimes needs two passes to actually clear
   4.5:1.
3. Deliberate text-over-image overlap (e.g. a strikethrough bar crossing a number): the escape-hatch
   attribute `data-layout-allow-occlusion` goes on the occluded text element itself, not on the
   element covering it — confirmed by testing both ways.
4. A flex-child meant to sit at the very bottom (e.g. a "buried" item after a long list) needs
   `margin-top: auto` — otherwise it just follows the last sibling with dead space below it,
   undercutting the caption that says it's "buried at the bottom."
5. Always resize the canvas / reposition the footer to hug the actual content — a fixed-height
   composition tends to leave a dead gap at the bottom; check the snapshot visually every time,
   don't trust the check gate alone (it doesn't flag "too much empty space," only structural
   errors).

## Naming and delivery

- Internal project folder keeps a slug name (`videos/<slug>-visual/` — same parent directory as
  `/video` output, still covered by this repo's `videos/` gitignore rule).
- The final exported PNG is named after the actual post title, not the slug (e.g. `Solution - Fewer
  Tools to Sort Through Beats a Smarter Model.png`, colons replaced since they're invalid in
  filenames).
- Drop every finished visual into one flat folder for easy hand-off — don't leave the user hunting
  through separate project directories or opening multiple Finder windows.

## The loop, end to end

Read the post → pick one hook line + one visual device from the vocabulary above → build in the
left-text/right-visual landscape template using `context/brand.md`'s verified tokens → run `check`
→ fix whatever it flags using the gotchas above → snapshot → eyeball it and tighten spacing → rename
to the post title → done.

Per this repo's standing process preference: run the `emil-design-eng` skill at both the start
(to inform the build) and the end (as a critique pass) of crafting any visual — see the memory
entry `feedback-video-visual-design-review`, which applies to static visuals exactly as it applies
to `/video`.
