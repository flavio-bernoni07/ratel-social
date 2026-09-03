---
description: Runs /draft and then a visual (video or static image) back to back for the same release — an independently-reviewed LinkedIn/X/Reddit post set in Notion, plus either a scripted/voiced HyperFrames video or a single branded static visual.
---

You are the orchestrator for a combined post + visual run. This command does not reimplement
`/draft` or `/video` — it invokes each one, in full, via the Skill tool, and reports a combined
result. Each pipeline keeps its own input questions, its own review loop, and its own escalation
handling exactly as documented in `.claude/commands/draft.md` and `.claude/commands/video.md`. The
static-visual path (Step 2b) is this command's own responsibility — there's no separate `/visual`
skill, so it's run inline here, following `context/social-visuals.md`.

---

## Step 1 — Run `/draft`

Invoke the `draft` skill (via the Skill tool). Let it ask its own Step 0 question and run its full
flow unmodified: Style Scout ×3, drafters ×3, independent reviewer loops per platform, the Notion
row, and the calendar reminder. Do not pass it a pre-filled brief — it asks for its own.

Wait for `/draft` to finish (or escalate and get resolved) before moving to Step 2.

---

## Step 2 — Ask: video or static visual?

Before starting any visual work, ask exactly one question:

```
Want a video for this, or a single branded static image?
```

Wait for the reply. This is a real fork, not a formality — a video is a multi-minute pipeline
(script → build → voiceover → music/SFX → review → render), a static visual is a single HyperFrames
image project (minutes, no audio, no review loop beyond the technical `check` gate and an
`emil-design-eng` pass). Don't default to video just because that's what `/post` used to always do.

- **Video** → go to Step 2a.
- **Static visual** → go to Step 2b.

---

## Step 2a — Run `/video`

Invoke the `video` skill (via the Skill tool). Let it ask its own Step 0 question and run its full
sequential flow unmodified: script, HyperFrames build, voiceover, music/SFX, independent review
loop, and the render-approval gate.

This runs strictly after `/draft`, not in parallel — `/video`'s composition-build step needs direct
interactive access to the `hyperframes` skill from the main conversation, so there's no real
concurrency to gain by interleaving the two, and running them one at a time keeps each pipeline's
own escalation prompts unambiguous about which run they belong to.

If the post and the video are meant to share an angle, carry that context yourself when answering
`/video`'s Step 0 question on the user's behalf where it's genuinely the same answer (e.g. "anything
to avoid") — but still let `/video` ask its own question rather than skipping it, since video-specific
details (length, hook line, destination aspect ratio) have no equivalent in `/draft`.

Once done, go to Step 3.

---

## Step 2b — Craft a static visual

Follow `context/social-visuals.md` in full — it is the single source of truth for this path (brand
tokens via `context/brand.md`, the two-register design system, the landscape template, the
visual-device vocabulary, the hard content rules, and the recurring-bugs checklist). Summary of the
flow, in order:

1. Load `emil-design-eng` (via the Skill tool) before building, to inform the composition/layout
   choice — this is not optional, per the standing process preference for any visual-design work.
2. Pick the post's own "visual suggestion" note (from the `/draft` Notion row's content, Step 5 of
   `draft.md`) as the hook line + visual device if one exists; otherwise pick a device from
   `context/social-visuals.md`'s vocabulary that hasn't been used this week.
3. Scaffold a HyperFrames project under `videos/<slug>-visual/` (landscape resolution), build the
   left-text/right-visual composition using `context/brand.md`'s verified tokens/logo/fonts — never
   an invented or unverified logo path, color, or font name.
4. Run `npx hyperframes check --json` until it's clean (0 lint / 0 runtime / 0 layout errors, all
   contrast checks passing). Fix using `context/social-visuals.md`'s recurring-bugs checklist.
5. Run `npx hyperframes snapshot --frames 1` to get the deliverable PNG. Eyeball it — the check gate
   doesn't flag dead space or a weak visual hierarchy, only structural errors.
6. Load `emil-design-eng` again as a critique pass on the finished snapshot; apply what it surfaces.
7. Rename the exported PNG to the actual post title (colons replaced, since they're invalid in
   filenames) and place it in a flat delivery folder, not left inside the numbered project directory.

There's no automated revision-loop-then-escalate pattern here like `/draft`/`/video` have — this is
a single build-check-review-fix cycle done directly in the main conversation, since there's no
independent-reviewer-equivalent agent for static visuals. If something about the post's claims is
unclear or looks like it'd violate `context/hard-rules.md` once visualized, ask rather than guess.

Once done, go to Step 3.

---

## Step 3 — Combined confirmation

After `/draft` and whichever visual path ran (or one is intentionally dropped per its own escalation
flow), print one combined summary. For a video:

```
✓ Post: "[Post Title]" — YYYY-MM-DD — [Notion page link if available]
  LinkedIn: [verdict + rounds]   X: [verdict + rounds]   Reddit: [verdict + rounds] → r/[subreddit]

✓ Video: videos/<slug>/renders/<filename>.mp4 — [duration]s, [resolution]
  Review: [verdict + rounds]

── FLAGS ──
[any flags carried through from either pipeline]
```

For a static visual, swap the second block for:

```
✓ Visual: [delivery path]/[Post Title].png — 1600x900
  Check: [lint/runtime/layout/contrast — all clean, or note what was fixed]
```

If either pipeline stopped short (dropped after escalation, or the user declined to render/finish),
say so plainly instead of implying both completed.
