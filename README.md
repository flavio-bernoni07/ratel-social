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
    weekly-strategy.md      ← dormant weekly planner (performance + trends → plan)
  agents/
    style-scout.md          ← hook/subreddit research, called once per platform
    linkedin-drafter.md
    x-drafter.md
    reddit-drafter.md       ← also picks the subreddit
    independent-reviewer.md ← the piece that was missing before — actually wired in
    trend-scout.md          ← dormant, for weekly-strategy
    performance-reporter.md ← dormant, for weekly-strategy
  settings.json

context/
  hard-rules.md             ← single source of truth for cross-platform rules — read this first
  linkedin-style.md
  x-style.md
  reddit-style.md           ← subreddit-picking rubric + candidate shortlist
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

### 4. Plan the week (dormant, needs wiring into a cadence)

```
/weekly-strategy
```

Combines performance data from Notion + a trend scan into a content plan. `trend-scout` and
`performance-reporter` exist and work standalone; this command just isn't part of the `/draft`
loop.

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
| Reactions / Comments / Shares / Impressions | Number | Auto-updated by the tracker |
| Engagement Rate | Number (%) | (reactions + comments + shares) / impressions |
| Last Updated | Date | Last tracker sync date |

`Account` is a multi_select with a fixed option set, not free text — this drifted from the old
repo's own docs once already. Always confirm live before writing to it.

---

## Performance tracking

LinkedIn tracking is ported and works. X and Reddit tracking are stubs (see the docstrings in
`tracker/x_tracker.py` / `tracker/reddit_tracker.py` for what's blocking them).

### Option A: LinkedIn analytics CSV export (no API token needed)

```bash
cd ratel-social
pip install -r tracker/requirements.txt
cp .env.example .env  # fill in NOTION_API_KEY
python tracker/import_csv.py path/to/linkedin-export.csv
```

### Option B: LinkedIn API (automated, runs daily via GitHub Actions)

1. Create a LinkedIn Developer App, request Marketing Developer Platform access.
2. Add `NOTION_API_KEY`, `LINKEDIN_API_TOKEN`, `LINKEDIN_ORG_ID` as repo secrets
   (`Settings → Secrets → Actions`).
3. The tracker runs automatically every day at 14:00 UTC, or trigger manually from the Actions tab.

After publishing on LinkedIn, add a line to the Notion page:
```
LinkedIn URL: https://linkedin.com/feed/update/urn:li:activity:7XXXXXXXXXXXXXXXXX/
```

---

## Hard content rules

Full rules live in `context/hard-rules.md` — every drafting and review agent reads it before
producing anything. Summary: no em dashes ever, no benchmark percentages until Rob confirms the
page is live, no manipulative CTAs, no banned marketing phrases. Mechanism names and links are
allowed on X/Reddit but not LinkedIn — see the per-platform table in that file.
