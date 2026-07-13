# Claude Code — Project Context

This is Ratel's private multi-platform social content workspace. You help draft, review, and
manage LinkedIn, X, and Reddit posts for Ratel through one orchestrated pipeline.

## The skill

`/draft` — Give a date and a topic. The orchestrator runs Style Scout research, spawns a
specialized drafter per platform (LinkedIn, X, Reddit), runs each draft through an Independent
Reviewer with up to 2 automatic revision rounds, then writes the approved result to Notion plus a
calendar reminder. Nothing auto-publishes — every output is a reviewable Notion draft.

`/weekly-strategy` — Dormant weekly planner. `trend-scout` and `performance-reporter` exist and
work; this command just isn't part of the `/draft` loop yet.

## Architecture

```
Orchestrator (.claude/commands/draft.md)
  ├─ style-scout          × 3 in parallel (platform param: linkedin / x / reddit)
  ├─ linkedin-drafter      × 1, then independent-reviewer, revision loop (max 2 rounds)
  ├─ x-drafter             × 1, then independent-reviewer, revision loop (max 2 rounds)
  └─ reddit-drafter        × 1 (also picks the subreddit), then independent-reviewer, revision loop
```

The three platform loops run independently — one platform being SATISFIED doesn't wait on
another. If a platform is still NEEDS REVISION after round 2, the orchestrator stops looping and
asks the user how to proceed rather than looping forever or silently accepting a bad draft.

## Key context files (read before drafting or reviewing anything)

- `context/hard-rules.md` — single source of truth for cross-platform rules. Read this first.
- `context/linkedin-style.md`, `context/x-style.md`, `context/reddit-style.md` — per-platform
  voice, structure, hook formulas. `reddit-style.md` also holds the subreddit-picking rubric and
  candidate shortlist.
- `context/accounts.md` — Notion `Account`/`Person` field rules. `Account` is multi_select with a
  fixed option set, not free text.
- `context/ratel-overview.md` — what Ratel builds, what's shipped vs not, benchmark numbers,
  install commands. Load before drafting any post.
- `context/flavio-role.md` — Flavio's role, weekly cadence, persona/voice assignments.

## Notion database

Posts database (same one `ratel-linkedin` used, no migration needed):
`379f341a-f2a3-80b5-9485-000b2eb7e9cc`

There is no separate "Weekly Plan" table to hand-edit. Setting the `Publishing date` property is
what makes a row appear on the Content Calendar view. Do not try to parse or edit a manual
weekly-plan block — it doesn't exist anymore (confirmed live 2026-07-13).

**Never change the `Account` multi_select's option set** without explicit sign-off — it's a shared
database Luce and Giacomo also use. If a post needs an account tag that doesn't exist yet (e.g. a
non-Jack Reddit persona), surface that to the user instead of adding the option yourself.

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
