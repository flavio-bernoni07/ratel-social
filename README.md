# ratel-social

Ratel's multi-platform social content pipeline, powered by Claude Code. Give it a date and a
topic, get back an independently-reviewed LinkedIn post, X post, and Reddit post (subreddit picked
for you), all written to Notion as a draft. Nothing here auto-publishes.

This repo replaces `ratel-linkedin`. The core gap it fixes: the old repo built a virality-review
agent that was never actually wired into the drafting flow — drafts went straight to Notion
unreviewed. Here, every platform's draft goes through an independent reviewer with a bounded
revision loop before it lands.

---

## What's inside

```
.claude/
  commands/
    draft.md               ← the orchestrator: date + topic → 3 reviewed drafts → Notion + calendar
    strategy.md              ← campaign planner: goal + date range → day-by-day calendar → skeleton Notion rows
    weekly-strategy.md      ← dormant weekly planner (performance + trends → plan)
  agents/
    style-scout.md          ← hook/subreddit research, called once per platform
    linkedin-drafter.md
    x-drafter.md
    reddit-drafter.md       ← also picks the subreddit
    independent-reviewer.md ← the piece that was missing before — actually wired in
    campaign-planner.md      ← sequencing logic for /strategy, does not draft copy
    trend-scout.md          ← used by /strategy and dormant weekly-strategy
    performance-reporter.md ← used by /strategy and dormant weekly-strategy
  settings.json

context/
  hard-rules.md             ← single source of truth for cross-platform rules — read this first
  linkedin-style.md
  x-style.md
  reddit-style.md           ← subreddit-picking rubric + candidate shortlist
  campaign-planning.md       ← narrative-arc + cadence rules for /strategy
  accounts.md                ← Notion Account/Person field rules (Account is multi_select, not text)
  ratel-overview.md          ← company + product reference
  flavio-role.md             ← Flavio's role, guardrails, weekly cadence

tracker/
  notion_client.py           ← shared Notion read/write module
  linkedin_tracker.py        ← API-based LinkedIn metric sync
  import_csv.py              ← CSV-based LinkedIn metric sync (no token needed)
  x_tracker.py                ← stub, not built (see docstring for what's needed)
  reddit_tracker.py           ← stub, not built (see docstring for what's needed)
  requirements.txt

.github/workflows/
  tracker.yml                 ← GitHub Actions: runs the LinkedIn tracker daily at 14:00 UTC

CLAUDE.md
.env.example
.mcp.json
```

---

## Quick start

### 1. Clone and open

```bash
cd ratel-social
claude
```

### 2. Connect MCP servers

Notion and Google Calendar access come through your Claude Code account connectors, not a
repo-level `.mcp.json` entry — make sure both are connected in your Claude Code integrations.
`.mcp.json` here only declares `ratel-mcp` (update the config path to your local Ratel config).

### 3. Draft a post

```
/draft
```

Answer the one question it asks (topic + publish date). The orchestrator handles everything else:
research, drafting, independent review with up to 2 automatic revision rounds per platform, and
the Notion + Calendar write.

### 4. Plan a campaign or a week

```
/strategy
```

Give it a goal ("growth push for the SDK", "3-week launch campaign", "a normal content week") and
a date range. It gathers performance data + trends + the existing pipeline, spawns
`campaign-planner` to sequence a day-by-day calendar (type, platform, topic brief, and why that
order works), and once you approve it, writes skeleton Notion rows (`Status: Not started`) so they
show up on the Content Calendar immediately. It never drafts copy itself — run `/draft` on any
planned day when you're ready to actually write it.

### 5. Older dormant planner

```
/weekly-strategy
```

A simpler performance+trends → text plan, superseded by `/strategy` for anything that needs actual
Notion rows. Kept because `trend-scout`/`performance-reporter` are shared by both.

---

## Notion database

Same database this repo's predecessor used — no migration needed.

**Posts database**: `379f341a-f2a3-80b5-9485-000b2eb7e9cc`
**Content Calendar**: a view on the same database, keyed off `Publishing date`. There is no
separate "Weekly Plan" table to hand-edit — setting `Publishing date` is what makes a row appear
on the calendar.

### Database schema (verified live 2026-07-13 — re-verify before assuming this hasn't drifted)

| Property | Type | Notes |
|---|---|---|
| Name | Title | Short descriptive title |
| Status | Status | Not started → First sketch → In progress → Last draft → Approved → Posted |
| Type | Select | Problem, Solution, Benchmarks, People, Product, Event, Launch Week |
| Overview | Text | One-liner description of the post |
| Publishing date | Date | Target publish date — drives the Content Calendar view |
| Account | **Multi-select** | See `context/accounts.md` for the exact option set |
| Person | Person | Team members involved |
| LinkedIn Reactions / Comments / Shares / Impressions | Number | Auto-updated by `tracker/linkedin_tracker.py` |
| LinkedIn Engagement Rate | Number (%) | (reactions + comments + shares) / impressions |
| X Likes / Replies / Reposts / Impressions | Number | Auto-updated by `tracker/x_tracker.py` |
| X Engagement Rate | Number (%) | (likes + replies + reposts) / impressions |
| Reddit Upvotes / Comments | Number | Auto-updated by `tracker/reddit_tracker.py` |
| Reddit Upvote Ratio | Number (%) | Reddit's own upvote ratio, no impressions equivalent exists |
| Last Updated | Date | Last tracker sync date, shared across all three trackers |

`Account` is a multi_select with a fixed option set, not free text — this drifted from the old
repo's own docs once already. Always confirm live before writing to it. Metrics are per-platform
properties (added 2026-07-13, renamed from the old repo's single LinkedIn-only Reactions/Comments/
Shares/Impressions/Engagement Rate columns) because one row can carry a LinkedIn + X + Reddit post
at once, and a single shared column can't hold three platforms' numbers without conflating them.

---

## Performance tracking

All three trackers exist and share `tracker/notion_client.py` for the Notion half. LinkedIn is
proven (ported from the old repo). X and Reddit are written against the real APIs but untested
live — no credentials existed at build time. Both exit cleanly (code 0) rather than erroring if
their credentials aren't set, so a scheduled run with only LinkedIn configured won't fail the job.

### LinkedIn

**Option A — CSV export (no API token needed):**
```bash
cd ratel-social
pip install -r tracker/requirements.txt
cp .env.example .env  # fill in NOTION_API_KEY
python tracker/import_csv.py path/to/linkedin-export.csv
```

**Option B — API (needs LinkedIn Marketing Developer Platform approval):**
```bash
python tracker/linkedin_tracker.py
```
After publishing, add a line to the Notion page: `LinkedIn URL: https://linkedin.com/feed/update/urn:li:activity:7XXXXXXXXXXXXXXXXX/`

### X

Needs `X_API_BEARER_TOKEN` (developer.x.com — confirm your tier includes tweet `public_metrics`).
```bash
python tracker/x_tracker.py
```
After publishing, add a line to the Notion page: `X URL: https://x.com/handle/status/1234567890123456789`

### Reddit

Needs `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET` (reddit.com/prefs/apps, a "script" app) and a
descriptive `REDDIT_USER_AGENT`.
```bash
python tracker/reddit_tracker.py
```
After publishing, add a line to the Notion page: `Reddit URL: https://www.reddit.com/r/subreddit/comments/postid/title/`

### Automation

Two options, can coexist:
- **GitHub Actions** (`.github/workflows/tracker.yml`) — runs all three trackers daily at 14:00
  UTC. Needs the repo pushed to GitHub with the credentials above added as repo secrets.
- **Claude `/schedule` cloud routine** — doesn't need a GitHub remote. See the routine set up for
  this repo (created 2026-07-13) for details, or run `/schedule` to create/inspect it.

---

## Hard content rules

Full rules live in `context/hard-rules.md` — every drafting and review agent reads it before
producing anything. Summary: no em dashes ever, no benchmark percentages until Rob confirms the
page is live, no manipulative CTAs, no banned marketing phrases. Mechanism names and links are
allowed on X/Reddit but not LinkedIn — see the per-platform table in that file.
