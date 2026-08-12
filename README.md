# ratel-social

Ratel's social content pipeline, run entirely in Claude Code. Three orchestrated skills — draft a
post, plan a week, build a video — each with an independent reviewer in the loop, so nothing goes
to Notion or gets rendered without a second pass checking it against Ratel's actual rules.

Nothing here auto-publishes. Everything lands as a reviewable Notion draft or a local render — you
always hit publish yourself.

## What a run looks like

```
> /draft
What's the post about? Dynamic Ranking shipped last week — an agent picked the 5th-ranked
tool and it turned out right, so the catalog bumped it to #1 for next time.
When do you want to publish it? Thursday

  ✓ style-scout researched real hook patterns on LinkedIn, X, and Reddit — in parallel
  ✓ linkedin-drafter, x-drafter, reddit-drafter each wrote their platform's version
  ✓ independent-reviewer checked each one against the hard rules + a virality rubric
  ✓ x-drafter's first pass got NEEDS REVISION (an unconfirmed benchmark number) — revised, passed

✓ Created: "Dynamic Ranking — shipped, not yet measured" — Thu 2026-08-14
📅 Calendar reminder set

── LINKEDIN ── (APPROVED, round 1)
[full reviewed post]
── X ── (APPROVED, round 2)
[full reviewed post]
── REDDIT ── r/LocalLLaMA (APPROVED, round 1)
[full reviewed post]
```

## Quick start

1. Open this repo in Claude Code.
2. Connect **Notion** and **Google Calendar** under your Claude Code integrations — not in
   `.mcp.json`, those work through your account rather than a repo config.
3. Run `/draft` for a post, `/strategy` to plan a week first, or `/video` for a short explainer.

## The three skills

| Skill | Give it | Get back |
|---|---|---|
| **`/draft`** | A topic + publish date | LinkedIn, X, and Reddit drafts, each independently reviewed (up to 2 revision rounds), written to Notion, plus a calendar reminder |
| **`/strategy`** | A goal ("growth push," "3-week launch," "a normal week") + a date range | A day-by-day content calendar informed by real performance data and current trends, written as skeleton Notion rows — run `/draft` on each slot when you're ready to write copy |
| **`/video`** | A topic (and optionally a locked hook, a length, brand references) | A scripted, narrated, independently-reviewed HyperFrames render — script → build → voiceover → music/SFX → review, in that order, since each stage needs the last one's real output |

Every skill ends in something you review before it goes anywhere public. None of them post for you.

## How it's built

```
/draft                                    /video
  ├─ style-scout × 3 (parallel)              ├─ video-scriptwriter
  ├─ {linkedin,x,reddit}-drafter × 3          ├─ (main thread) → hyperframes skill builds it
  │    (parallel, each independent)           ├─ video-voiceover
  └─ independent-reviewer per platform        ├─ video-music-sfx
       revision loop, max 2 rounds,           └─ video-reviewer
       escalates to you if still stuck             revision loop, max 2 rounds, same as /draft

/strategy
  ├─ performance-reporter + trend-scout (parallel)
  ├─ existing Notion pipeline (so it never double-books a day)
  └─ campaign-planner → sequences the week, you approve before anything writes to Notion
```

`/draft`'s three platforms run independently — LinkedIn can be approved while Reddit is still on
its second revision round. `/video` runs strictly in order, since voiceover timing depends on the
composition that was actually built, not an assumed length.

## Repo structure

```
.claude/commands/     the three orchestrator skills (/draft, /strategy, /video)
.claude/agents/       12 specialist agents — drafters, reviewers, researchers, video pipeline
context/              hard rules, per-platform style bibles, product background, growth playbooks
tracker/              one script per platform, pulls real engagement numbers back into Notion
```

## Tracking performance

`tracker/` has one script per platform. LinkedIn works today with just a Notion key. X and Reddit
need their own API credentials first — see `.env.example` for exactly what and where to get it. A
Claude `/schedule` routine already runs daily for Reddit, since that one needs no credentials at
all.

## Want the full detail?

- **`CLAUDE.md`** — architecture, the Notion schema every write depends on, repo hygiene rules.
- **`context/hard-rules.md`** — the single source of truth every drafting and review agent reads
  first. Start here if something a draft produced looks wrong.
- **`context/role.md`** — what running this pipeline actually involves week to week.

## A note for whoever's reading this next

This repo was built during an internship and is written to be handed off, not just used. If
something in here is stale, wrong, or confusing, that's worth fixing directly rather than working
around it — `context/role.md` says the same thing. The pipeline is only as good as the rules it
reads, and those rules only stay good if whoever's running it keeps them honest.
