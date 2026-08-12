# The Content Operator's Role

> This repo was originally built during Flavio Bernoni's internship (content & documentation lead,
> summer 2026) and is written to hand off cleanly to whoever runs Ratel's social content next.
> Nothing here is Flavio-specific — swap in your own name, cadence, and Slack handles as you settle
> in, and update the Weekly Touchpoints table below to match reality.

## Mission

Drive Ratel's visibility, discoverability, and credibility through strategic content (social media
+ written), fresh community-driven narratives, and documentation good enough to convert visitors
into engaged users.

## The job, in practice

1. **Run the drafting pipeline.** `/draft` for one-off posts, `/strategy` for planning a week or
   campaign, `/video` for anything that needs motion. All three write to the same Notion database
   as reviewable drafts — nothing auto-publishes. You still hit publish yourself, on your own
   judgment, after reading the draft.
2. **React to what ships.** Every real feature ship is a content opportunity. The fastest way to
   find out what shipped: ask in the dev Slack channel, or check `#product` directly. Don't invent
   a feature story from a stale doc — `context/ratel-overview.md` says on every page that it needs
   re-verification for anything load-bearing.
3. **Bring a real point of view, not just announcements.** Ratel wants to be recognized as a
   knowledgeable, personality-driven voice in the AI-engineering space, not a company that only
   posts when it ships something. `/strategy`'s trend-scout exists for this — use it weekly, not
   just during launch weeks.
4. **Keep this repo itself in shape.** If a rule drifts, a context file goes stale, or an agent's
   instructions stop matching how the pipeline actually works, fix it here rather than working
   around it in your head. The next person inherits whatever state you leave this in.

## Weekly touchpoints (edit this to match your actual cadence)

| Day | Activity | Format |
|---|---|---|
| Weekly (pick a day) | Review last week's performance (`/strategy` pulls `performance-reporter`) | Async |
| Weekly (pick a day) | Plan the coming week or campaign (`/strategy`) | Async, review before approving |
| Ongoing, as shipped | Draft a post reacting to a real ship (`/draft`) | Within 48h of the ship, ideally |

## Constraints and guardrails

The actual rules live in `context/hard-rules.md` (cross-platform) and the per-platform style files
— this section is about judgment calls the rules don't cover.

- **Target creators worth having notifications on**, for staying current on what the AI-agent
  space is actually talking about: `@hrishioa`, `@nutlope`, `@goodside`, `@marktenenholtz`,
  `@hyhieu226`, `@_xjdr`, `@ivanfioravanti`, `@ash_twtz`, `@Surendar__05`, `@vivek_naskar`,
  `@i_amanchadha`, `@jovandotse`, `@DegenApeDev`, `@manishkumar_dev`, `@EXM7777`.
- **Voice reference, X format specifically:** `@EXM7777` (Machina) — governs *how* X posts are
  built (hook shape, thread structure). `context/x-style.md` has the full breakdown.
- **When something is ambiguous** — whether a claim is safe to make, whether a feature is really
  shipped, whether a number is confirmed — ask in Slack before drafting around the uncertainty. A
  flagged unknown in a draft's `## Flags` section is fine; a confidently-wrong claim isn't.

## Escalation

If a decision blocks forward progress (a founder needs to confirm something, a hard rule seems to
be in the way of something legitimate, a tool or credential is missing), say so plainly rather than
working around it silently. `/draft` and `/video` both surface unresolved issues in a `Flags`
section for exactly this reason — use it.
