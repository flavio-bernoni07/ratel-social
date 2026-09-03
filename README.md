# ratel-social

Ratel's social content pipeline, run entirely in Claude Code. Four skills — draft a post, plan a
week, build a video, do a post and its visual together — each with an independent reviewer in the
loop, so nothing reaches Notion or gets rendered without a second pass checking it against Ratel's
actual rules.

**Nothing here auto-publishes.** Everything lands as a reviewable Notion draft or a local render.
You always hit publish yourself.

---

## Install

```bash
git clone https://github.com/flavio-bernoni07/ratel-social.git
cd ratel-social
./install.sh
```

That checks and installs everything scriptable, then prints the few manual steps. Re-run it any
time — it is idempotent. Use `./install.sh --check` to look without changing anything.

Then open the repo in Claude Code and run `/draft`.

---

## What you need

| Tool | What it does here | Install |
|---|---|---|
| **Node 18+** | runs HyperFrames | `brew install node` |
| **ffmpeg** | probes and mixes every render's audio | `brew install ffmpeg` |
| **Python 3.11+** | the Notion metrics tracker | `brew install python` |
| **HyperFrames** | builds and renders every video and static visual | `npx hyperframes skills update` |
| **Voicebox** | narration — free, local, no API key | [voicebox.sh](https://voicebox.sh) → open once, download a TTS model |
| **Notion** | where every draft lands | connect in Claude Code's integrations panel |
| **Google Calendar** | publish reminders | connect in Claude Code's integrations panel |
| **HeyGen** *(optional)* | alternative TTS + music library | `npx hyperframes auth login` |

Two things `install.sh` cannot do for you:

1. **Connect Notion and Google Calendar** in Claude Code's integrations panel. These authenticate
   through your account, not through `.mcp.json`.
2. **Open Voicebox once** and download a TTS model. Pick **Qwen CustomVoice** — it ships nine preset
   speakers, so you do not need to record or clone a voice to start. It also takes a plain-language
   delivery instruction ("quick, certain, unimpressed by its own news"), which matters more for how
   human narration sounds than which voice you pick.

The design skills need no install — they are vendored in `.agents/skills/` and symlinked into
`.claude/skills/`, so they ship with the clone.

---

## The four skills

| Skill | Give it | Get back |
|---|---|---|
| **`/draft`** | A topic + publish date | LinkedIn, X and Reddit drafts, each independently reviewed (max 2 revision rounds), written to Notion, plus a calendar reminder |
| **`/post`** | A topic + publish date | Everything `/draft` does, **then asks video or static image** and produces that too — the whole release in one run |
| **`/video`** | A topic (optionally a locked hook, a length, brand references) | A scripted, narrated, independently-reviewed HyperFrames render |
| **`/strategy`** | A goal + a date range | A day-by-day content calendar from real performance data and current trends, as skeleton Notion rows — run `/draft` per slot when you write copy |

### What a run looks like

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
```

---

## Visuals

`/post` and `/video` both produce visuals, and the choice between them is a real fork:

- **Video** — a multi-stage pipeline: script → build → voiceover → music/SFX → independent review →
  render. Minutes of work per stage, because each one needs the previous stage's real output.
- **Static image** — one 1600x900 HyperFrames project rendered as a single frame. No audio, no
  revision loop beyond the technical check and a design pass. See `context/social-visuals.md`.

### The video house style is locked

Every video matches `videos/cloud-day1-launch-video/index.html` — rendered as `Video-Cloud.mp4` —
on five points, documented in full in **`context/brand.md` § Video Style**:

1. **Handheld camera rig** — a slow `#drift` wander nested around a `#shake` micro-jitter, both GSAP
   driven off a fixed-seed generator so the path is identical on every render.
2. **Flash cuts** — one frame of `#e5e5e7` above the rig, scene hard-swapped underneath. Never a
   crossfade. Each flash carries its whoosh transient, started 0.20s early so it lands on the white.
3. **The background gradient stack** — two radial washes over a deep green linear base. Never a flat
   near-black fill.
4. **Burned-in subtitles, always**, plus a new music track per video at -13.7 LUFS.
5. **The real "Ratel, live now" end card**, dissolved rather than flash-cut — the one exception to
   rule 2.

A composition missing any of these gets fixed before review, not after.

**Design skills load before the first composition is written**, never as a polish pass:
`apple-design` → `emil-design-eng` → `animate` → `animation-vocabulary`, then `review-animations` on
the finished build. Motion and typography are far more expensive to retrofit than to decide up front.

---

## How it's built

```
/draft                                    /video
  ├─ style-scout × 3 (parallel)              ├─ video-scriptwriter
  ├─ {linkedin,x,reddit}-drafter × 3         ├─ (main thread) → hyperframes skill builds it
  │    (parallel, each independent)          ├─ video-voiceover
  └─ independent-reviewer per platform       ├─ video-music-sfx
       revision loop, max 2 rounds,          └─ video-reviewer
       escalates to you if still stuck            revision loop, max 2 rounds, same as /draft

/post                                     /strategy
  ├─ /draft in full                          ├─ performance-reporter + trend-scout (parallel)
  ├─ asks: video or static image?            ├─ existing Notion pipeline (never double-books a day)
  └─ /video, or the inline static path       └─ campaign-planner → you approve before Notion writes
```

`/draft`'s three platforms run independently — LinkedIn can be approved while Reddit is still on its
second revision round. `/video` runs strictly in order, since voiceover timing depends on the
composition that was actually built, not an assumed length.

If a loop is still `NEEDS REVISION` after round 2, the orchestrator stops and asks you, rather than
looping forever or quietly shipping something weak.

---

## Repo structure

```
install.sh            one-command setup, idempotent
.claude/commands/     the four orchestrator skills
.claude/agents/       12 specialist agents — drafters, reviewers, researchers, video pipeline
.claude/skills/       symlinks into .agents/skills
.agents/skills/       vendored design + editor skills (pinned in skills-lock.json)
context/              hard rules, per-platform style bibles, brand, product background
tracker/              one script per platform, pulls engagement numbers back into Notion
videos/               HyperFrames projects (gitignored — renders do not belong in git)
```

---

## The rules that matter most

Four are non-negotiable and every agent reads them first, in `context/hard-rules.md`:

- No em dashes in post copy, ever
- No benchmark percentages until the benchmark page is live
- No mechanism names (BM25, vector search) on LinkedIn — allowed on X and Reddit
- No links in post body on LinkedIn/X — allowed on Reddit

**Every claim gets re-verified** against Slack or the live repo before it lands in a post.
`context/ratel-overview.md` says so on every page, and it means it.

---

## Tracking performance

`tracker/` has one script per platform. LinkedIn works today with just a Notion key. X and Reddit
need their own API credentials — see `.env.example` for what and where. Metric properties in Notion
are per-platform, since one row can carry a post on all three at once, so use the matching update
function in `tracker/notion_client.py`.

---

## Going deeper

- **`CLAUDE.md`** — architecture, the fixed Notion page schema every write depends on, repo hygiene.
- **`context/hard-rules.md`** — start here if a draft produced something that looks wrong.
- **`context/brand.md`** — logo technique, colour tokens, the real font stack, video style.
- **`context/role.md`** — what running this week to week actually involves.

---

## A note for whoever reads this next

This repo is written to be handed off, not just used. If something here is stale, wrong or
confusing, fix it directly rather than working around it — `context/role.md` says the same. The
pipeline is only as good as the rules it reads, and those rules only stay good if whoever runs it
keeps them honest.
