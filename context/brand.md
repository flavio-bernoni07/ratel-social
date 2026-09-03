# Ratel Brand Guide

Sourced directly from `docs/ratel-getting-started.html` (canonical color tokens + the live logo
SVG), `context/style-bible.md`, and real video projects under `videos/`. Nothing here is invented —
everything traces back to one of those sources. If a value in this file and the live site/repo ever
disagree, the live source wins and this file needs updating (see "Keeping this file current" below).

## Logo

**Correction (2026-08-14):** an earlier version of this file claimed the mark was a single inline
SVG with a literal path (`viewBox="0 0 552 256"`) living in a local `docs/ratel-getting-started.html`.
Neither claim held up: that file doesn't exist in this repo, and live-checking `docs.ratel.sh`
showed the real implementation is a **PNG silhouette used as a CSS mask**, not an SVG path. Verified
directly against the live site's HTML/CSS on 2026-08-14 — this section reflects what's actually
there, not the earlier draft.

- Asset: `ratel-badger.png` (served from `docs.ratel.sh/ratel-badger.png`, 2205x1021 PNG,
  transparent badger silhouette). A local copy for video use should be pulled fresh from that URL
  and cached under the project's asset folder, not redrawn.
- Applied via `mask-image` (CSS `-webkit-mask-image` / `mask-image`, `mask-repeat: no-repeat,
  mask-position: center, mask-size: contain`), with the fill color set by `background-color` on the
  masked element — **not** a raster/rasterized image shown directly.
- Fill color: `#023a2e` (`--forest`) in light mode, `#eee3ce` (`--cream`) in dark mode. Video work is
  dark-mode-only, so use `--cream` fill.
- Icon renders at 17x37px in the docs nav (small, inline with the wordmark text). No confirmed
  large-scale (e.g. ~300px) video logo-sting treatment exists yet in a live source — if a past video
  composition under `videos/` already has one, treat that as the precedent; otherwise this is a new
  treatment, not a documented repeat.
- **Never redraw or approximate the mark by hand-authoring path data.** Use the real
  `ratel-badger.png` asset (mask technique above) or an existing video composition's already-built
  treatment. Do not invent SVG path coordinates — that was the actual mistake in the earlier version
  of this file.

## Color Palette

Full token set, single source of truth (`docs/ratel-getting-started.html` `:root`):

| Token | Hex | Role |
|---|---|---|
| `--base` | `#001c16` | Primary background, deep forest-black |
| `--base-deep` | `#00130f` | Darkest background layer (code blocks, deep panels) |
| `--forest` | `#023a2e` | Secondary dark green surface |
| `--cream` | `#eee3ce` | Primary text-on-dark, logo fill, headlines |
| `--coral` | `#ed5126` | Primary accent — CTAs, hooks, highlighted words, eyebrows |
| `--coral-deep` | `#c4431f` | Coral hover/pressed state |
| `--green` | `#239452` | Secondary accent, success/positive signals |
| `--teal` | `#7ba0a0` | Tertiary accent, muted labels (e.g. "Getting started" eyebrow) |
| `--ink` | `#111113` | Text on light/cream buttons |
| `--paper` | `#fafafa` | Off-white, body text on dark, button backgrounds |
| `--warm-muted` | `#9e9788` | Muted secondary text, card subtext |
| `--glass-bg` | `rgba(0,15,12,0.72)` | Frosted glass card background |
| `--glass-border` | `rgba(238,227,206,0.22)` | Frosted glass card border |

Notes on how it's actually used:
- The site is dark-mode-only. There's no light theme variant defined anywhere.
- Coral is the single accent used for emphasis — never green or teal for CTAs, those stay
  supporting.
- The hero background isn't a flat color, it's a live WebGL gradient (`FlowGradient`, ported 1:1
  from ratel.sh) that blends four colors: a coral-orange, a deep forest green, a burnt coral, and a
  near-black green. If you need to describe "the Ratel background" to a designer: it's a
  slow-moving, seeded noise-warped blend of coral and forest-green, not a static gradient.
- A subtle grain texture (`docs/grain.png`, tiled at 120px, 6% opacity) sits over everything — this
  is why nothing on the site looks flat/vector-clean, it always has a slight film-grain texture.

**Hard rule for anyone touching brand color:** every hex used anywhere (site, video, deck) must
trace back to this table or its documented rgba derivatives. Video review (the `video-brand-reviewer`
agent) hard-fails any color found via `grep -oE '#[0-9a-fA-F]{6}'` that isn't on this list.

## Typography

**Correction (2026-08-14):** an earlier version of this file named "Acid Grotesk" and "Geist Pixel
Square" as the display/label faces, with local `.woff2` files under `docs/fonts/`. Neither exists —
that directory isn't in this repo, and live-checking `docs.ratel.sh`'s actual CSS bundle
(`@font-face` declarations, verified 2026-08-14) shows only two font families in use, both from
Vercel's real, publicly embeddable Geist family:

1. **Geist** (`font-family: Geist, Geist Fallback`) — the sans/display face. Used via
   `var(--font-sans)` across the docs site: headlines, body, UI chrome. Widely embeddable (it's the
   standard Vercel/Next.js default font, available via `next/font/google` or a direct `.woff2`
   embed), so safe to use in a rendered video without an unbundled-font risk.
2. **Geist Mono** (`font-family: Geist Mono, Geist Mono Fallback`) — used via `var(--font-mono)`:
   code blocks, `<kbd>`/`<samp>`/`<pre>`, and by extension the natural choice for the pill-shaped
   tool badges (`search_capabilities`, `invoke_tool`) this project's other context files describe.

No separate "pixel" or small-caps utility face was found live — if a past video composition under
`videos/` already established one for uppercase labels/eyebrows, treat that as precedent; otherwise
default small-label treatment to Geist at a smaller size/tighter tracking rather than inventing a
third typeface.

Confirmed accent color in the live CSS: text selection uses `#ed51263d` (`--coral` at ~24% alpha),
consistent with coral being the one accent used for emphasis.

## UI / Visual Language (site)

- Glassmorphism cards: every content block is a `.glass` panel — `rgba(0,15,12,0.72)` background,
  1px `rgba(238,227,206,0.22)` border, `border-radius: 26px`, `backdrop-filter: blur(20px)`. This
  rounded, frosted-glass-on-dark look is the dominant UI signature — used for literally every card
  type on the page (why-box, gateway-box, path-card, test-card, star-cta).
- Buttons: solid cream pill (`--cream` bg, `--ink` text) for primary actions, outlined glass pill
  for secondary.
- Code blocks get their own darker nested treatment: `--base-deep` background, macOS-style
  traffic-light dots, syntax highlighting in a muted purple/blue/green palette (`#c792ea` keywords,
  `#82aaff` functions, `#c3e88d` strings, `#4ade80` highlights).
- Rounded corners everywhere, nothing is sharp: 26px on cards, 10-16px on buttons/code
  blocks/pills.

## Video Style

Built in HyperFrames, one project per video under `videos/<slug>/`.

**House style — locked (2026-08-24).** The canonical reference is
`videos/cloud-day1-launch-video/index.html`, rendered as
`~/Desktop/Progetti/Ratel/Materials/AI-Videos/Video-Cloud.mp4`. Every video matches it on five
points, and a composition missing any of them gets fixed before review, not after:

1. **Handheld camera rig.** `#drift` (slow wander, `scale: 1.035`, ~3.4s segments at ±7px / ±5px /
   ±0.06deg) nested around `#shake` (micro-jitter, ~0.34s segments at ±2.6px / ±2.0px / ±0.05deg),
   both GSAP-driven off a fixed-seed LCG so the path is identical on every render. No CSS transform
   on either wrapper. The over-scale on `#drift` is what keeps the frame covered as the rig moves.
2. **Flash cuts.** One frame (1/30s) of `#e5e5e7` at `z-index: 50`, placed outside the camera rig,
   with the scene swap hard-set underneath. Never a crossfade. The closing logo lock is the one
   exception and dissolves. Each flash carries `camera-flash-whoosh-transition-hit.mp3` started
   0.20s early so the transient lands on the white frame.
3. **Background.** The stage always carries this stack, never a flat near-black fill:

   ```css
   background:
     radial-gradient(ellipse 900px 700px at 100% -6%, rgba(237,81,38,0.22) 0%, rgba(237,81,38,0) 55%),
     radial-gradient(ellipse 900px 800px at 0% 108%, rgba(35,148,82,0.26) 0%, rgba(35,148,82,0) 55%),
     linear-gradient(155deg, #023a2e 0%, #001c16 60%, #00130f 100%);
   ```

4. **Music level.** BGM clip at `data-volume="0.2"`; the final render lands near **-13.7 LUFS**
   integrated. Mood is exciting and energetic, which overrides the "restrained, not a hype trailer"
   note below for launch and promo pieces.
5. **End voiceover is a real recording.** Every video closes on `~/Desktop/AUDIO REBE END.wav`, a
   person saying "Ratel, live now" (2.07s). Copy it into the project's `assets/audio/`. The closing
   line is never TTS.

**Look**
- Same token discipline as the site: colors and fonts always pulled from
  `docs/ratel-getting-started.html`, never approximated. (Reference clip's logo-sting background is
  `#002d1c`, a slightly different dark-green shade than the site's `--base` — an acceptable
  in-family variant, not a new color, but worth flagging to a designer as such.)
- Logo sting pattern: mark fades/scales in (`opacity 0→1, scale 0.85→1, back.out(1.6)` ease, 0.4s)
  over a soft radial glow (`#0c3b29` center fading to `#002d1c`), then a tagline drops in underneath
  (`translateY(16px)→0, power3.out`, 0.35s) in Geist Pixel Square, cream text.
- Motion must be literal, never decorative. Every beat has to visually match what's being said — a
  real pipeline diagram when talking pipeline, a real terminal search when talking search. Generic
  stock-feeling motion standing in for a concrete claim is a hard fail in review. Pull real product
  footage/screenshots already captured under `videos/` or the `ratel-assessment` catalog before
  inventing a new visual.

**Voice/pacing**
- Flat, matter-of-fact delivery — a diagnosis being read aloud, not a sales pitch. No upward lilt on
  closing lines.
- Target runtime: 12-15 seconds, ~30-45 words of VO at 140-150 wpm. Silent beats (real footage, the
  logo sting) are allowed to stay silent.
- Captions and VO must match verbatim wherever both appear in the same beat.
- Numbers under 20 are spoken as words in VO ("twelve"), but stay numerals on-screen in captions.
- All the LinkedIn/X hard rules apply verbatim to VO and captions: no em dashes, no benchmark
  percentages until Rob confirms the page is live, no mechanism names (BM25, vector search) spoken
  or shown, "tools and skills" always said together, no links on screen, no hype language ("game
  changer", "thrilled to share").

**QA gate:** every finished video gets reviewed by the `video-brand-reviewer` agent against exactly
this rubric (colors, literal motion, voice/pacing, content rules) before it ships, scored out of 10
per category, hard-fails on any rule violation.

## Voice (brief, for completeness)

Direct, honest, specific — like a knowledgeable peer, not a marketer. Never names internal
mechanisms in customer-facing copy (describes outcomes, not "BM25" or "vector search"). Takes
positions, no hedging. Paramount rule across every surface: no em dashes, ever.

## Where the real assets live

- `docs/ratel-getting-started.html` — canonical color tokens (`:root`) + the live logo SVG
- `docs/fonts/` — the three `.woff2` font files
- `docs/grain.png` — the site's grain texture overlay
- `videos/` — real rendered reference clips and compositions (logo stings, product footage)
- `context/style-bible.md` — the full written rulebook this guide summarizes

## Keeping this file current

This file is the canonical brand reference for drafting and video agents — load it before any
video build, and before any post that touches visual/brand description. When Flavio gives a brand
correction, addition, or clarification in conversation, fold it into this file (don't just apply it
inline to the one task at hand) so the next run starts from the corrected version.
