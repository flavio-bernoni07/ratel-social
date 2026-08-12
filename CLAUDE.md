# Claude Code — Project Context

This is Ratel's private multi-platform social content workspace. You help draft, review, and
manage LinkedIn, X, and Reddit posts, plus short product/explainer videos, for Ratel through
orchestrated pipelines.

## The skills

`/draft` — Give a date and a topic. The orchestrator runs Style Scout research, spawns a
specialized drafter per platform (LinkedIn, X, Reddit), runs each draft through an Independent
Reviewer with up to 2 automatic revision rounds, then writes the approved result to Notion plus a
calendar reminder. Nothing auto-publishes — every output is a reviewable Notion draft.

`/strategy` — Give a goal and a date range. Spawns `performance-reporter` + `trend-scout` +
`campaign-planner` to sequence a day-by-day content calendar (type, platform, topic brief), then
writes skeleton Notion rows (`Status: Not started`) once approved. Does not draft copy — that's
still `/draft`, run per slot once you're ready.

`/video` — Give a topic and get a scripted, voiced, independently-reviewed HyperFrames video.
Unlike `/draft`, this pipeline is **sequential**, not parallel: script → build the composition
(hands off to the `hyperframes` skill directly) → voiceover → music/SFX → independent review, with
the same revision-loop-then-escalate pattern as `/draft`. See Architecture below.

`/weekly-strategy` — Older, simpler performance+trends → text plan. Superseded by `/strategy` for
anything that needs actual Notion rows, kept because it shares `trend-scout`/`performance-reporter`.

## Architecture

```
/draft (.claude/commands/draft.md)
  ├─ style-scout          × 3 in parallel (platform param: linkedin / x / reddit)
  ├─ linkedin-drafter      × 1, then independent-reviewer, revision loop (max 2 rounds)
  ├─ x-drafter             × 1, then independent-reviewer, revision loop (max 2 rounds)
  └─ reddit-drafter        × 1 (also picks the subreddit), then independent-reviewer, revision loop

/video (.claude/commands/video.md)
  ├─ video-scriptwriter    × 1  →  writes the script + the HyperFrames brief
  ├─ (main thread) hands the brief to the `hyperframes` skill directly to build the composition
  ├─ video-voiceover       × 1  →  generates narration, reconciles real duration against the script
  ├─ video-music-sfx       × 1  →  adds a bed/SFX only if it earns its place, defaults to skipping
  └─ video-reviewer        × 1, then revision loop (max 2 rounds) — technical check + beat-by-beat
     visual inspection + honesty/rule compliance, all three required for SATISFIED
```

The three `/draft` platform loops run independently — one platform being SATISFIED doesn't wait on
another. `/video`'s stages run strictly in order — each one's input is the previous one's real
output (a script needs to exist before HyperFrames can build from it; voiceover needs the built
composition's actual beat timing; music needs voiceover's final duration).

If a loop is still NEEDS REVISION after round 2 (either pipeline), the orchestrator stops looping
and asks the user how to proceed rather than looping forever or silently accepting a bad result.

## Key context files (read before drafting or reviewing anything)

- `context/hard-rules.md` — single source of truth for cross-platform rules, including the
  unmeasured-claims rule that applies to video the same as posts. Read this first.
- `context/linkedin-style.md`, `context/x-style.md`, `context/reddit-style.md` — per-platform
  voice, structure, hook formulas. `reddit-style.md` also holds the subreddit-picking rubric and
  candidate shortlist. `linkedin-style.md` also has voice guardrails (no AI-slop paragraph
  stacking, no self-referential hooks).
- `context/accounts.md` — Notion `Account`/`Person` field rules. `Account` is multi_select with a
  fixed option set, not free text.
- `context/ratel-overview.md` — what Ratel builds, what's shipped vs not, benchmark numbers,
  install commands. Load before drafting any post or video. Every claim in it needs re-verification
  against Slack or the live repo before it lands in a post — the file says so on every page.
- `context/role.md` — the content operator's role, weekly cadence, escalation norms. Written for
  handoff — not tied to any one person's name.
- `context/growth-playbooks.md` — launch/community strategic frameworks (ORB channels, launch
  phases, content-repurposing atoms, community flywheel) for `campaign-planner` to draw on.

## Notion database

Posts database (same one `ratel-linkedin` used, no migration needed):
`379f341a-f2a3-80b5-9485-000b2eb7e9cc`

There is no separate "Weekly Plan" table to hand-edit. Setting the `Publishing date` property is
what makes a row appear on the Content Calendar view. Do not try to parse or edit a manual
weekly-plan block — it doesn't exist anymore (confirmed live 2026-07-13).

**Never change the `Account` multi_select's option set** without explicit sign-off — it's a shared
database Luce and Giacomo also use. If a post needs an account tag that doesn't exist yet (e.g. a
non-Jack Reddit persona), surface that to the user instead of adding the option yourself.

Metric properties are per-platform (`LinkedIn Reactions`/`Comments`/`Shares`/`Impressions`/
`Engagement Rate`, `X Likes`/`Replies`/`Reposts`/`Impressions`/`Engagement Rate`, `Reddit Upvotes`/
`Comments`/`Upvote Ratio`), added 2026-07-13 by renaming the old repo's single LinkedIn-only
columns and adding new ones for X/Reddit, since one row can carry a post on all three platforms at
once. `tracker/notion_client.py` has one update function per platform — use the matching one.

## What Ratel is (load before drafting any post or content)

Ratel is a **context-engineering platform for AI agents**. Three parts:

| Part | Repo | What it is |
|---|---|---|
| **Library / SDK** | `ratel-ai/ratel` | The core. Rust engine + TS SDK + Python SDK. Developers embed this in their agents to filter tools by relevance. This is the primary product. |
| **MCP Gateway** | `ratel-ai/ratel-mcp` | A ready-made product built on the SDK, for Claude Code / Cursor users. The showcase, not the full story. |
| **Benchmark** | `ratel-ai/ratel-bench` | Proof. Performance numbers that back every claim. |

**Primary audience: developers building AI agents.** Content should push toward the SDK
(`pnpm add @ratel-ai/sdk` / `pip install ratel-ai`), not just the MCP gateway install flow.

**Never describe Ratel as only "an MCP gateway."** That frames it as a Claude Code plugin, misses
the SDK-first story, and undersells the platform.

## Hard rules (non-negotiable — full detail in context/hard-rules.md)

- No em dashes in post copy, ever
- No benchmark percentages until Rob confirms the benchmark page is live
- No mechanism names (BM25, vector search) on LinkedIn — allowed on X and Reddit
- No links in post body on LinkedIn/X — allowed on Reddit

## Repo hygiene

This repo replaced `ratel-linkedin`, which had accumulated a stray nested git clone, multi-hundred
MB video files, and experimental docs unrelated to the content pipeline. Keep this repo to: the
drafting pipeline, its context files, and the tracker. Don't drop large media, unrelated tool
experiments, or other projects' source trees in here. If `find . -maxdepth 2 -name .git` ever
finds more than the repo's own `.git`, something got dropped in by accident, remove it.

`/video` produces real HyperFrames projects (rendered MP4s, generated audio, node dependencies)
under `videos/<slug>/` — this is deliberate and `.gitignore` already excludes `*.mp4`, `*.mov`, and
`/videos/` for exactly this reason. The pipeline that *builds* videos (the skill, the four agents)
lives in git; the videos themselves don't. Don't remove that gitignore rule to "fix" an untracked
directory — that's the intended state, not an accident.

## General working principles

- When enough information is available to complete the task, begin working instead of asking
  unnecessary questions. Ask for clarification only when a missing detail prevents meaningful
  progress.
- Do not revisit decisions that have already been made unless new evidence requires it.
- Keep solutions as simple as the task allows. Reuse existing work before creating new
  abstractions.
- Never claim work was completed unless it has been verified. Distinguish verified facts from
  assumptions, and report failures honestly instead of hiding them.
- Be concise. Explain important decisions briefly and avoid unnecessary narration.
