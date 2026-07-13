# ratel-social

Give it a date and a topic. Get back a LinkedIn post, an X post, and a Reddit post (subreddit
picked for you), each independently reviewed, saved as a draft in Notion. Nothing here
auto-publishes — you always hit publish yourself.

## Setup

1. Open this repo in Claude Code.
2. Connect **Notion** and **Google Calendar** under your Claude Code integrations (not in
   `.mcp.json` — those work through your account, not a repo config).
3. Run `/draft`.

## The two skills

- **`/draft`** — give a topic + publish date, get three reviewed drafts written to Notion plus a
  calendar reminder. This is the everyday command.
- **`/strategy`** — give a goal ("growth push," "3-week launch," "a normal week") and a date
  range, get a day-by-day content plan saved to Notion. Plans the week, doesn't write the posts —
  run `/draft` on each planned day when you're ready.

## Tracking performance

`tracker/` has one script per platform (LinkedIn, X, Reddit) that pulls real engagement numbers
into Notion. LinkedIn works today. X and Reddit need API credentials first — see `.env.example`.
A Claude `/schedule` routine already runs daily for Reddit, since that one needs no credentials.

## Want the details?

- `CLAUDE.md` — architecture, Notion schema, the rules every agent follows.
- `context/` — style bibles, hard rules, subreddit-picking logic, product background.
