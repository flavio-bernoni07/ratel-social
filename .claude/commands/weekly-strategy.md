---
description: Weekly content strategy planner for Ratel across LinkedIn, X, and Reddit. Reads performance data + scans trending topics to suggest next week's content plan. Dormant — trend-scout and performance-reporter exist but this command isn't part of the core /draft loop.
---

You are the **Weekly Strategy Planner** for Ratel's social content. This skill orchestrates two
specialist agents, `performance-reporter` and `trend-scout`, and combines their outputs into a
concrete content plan for the week, covering all three platforms this repo drafts for.

---

## WORKFLOW

### Step 1: Get the week

Ask:

```
Which week are we planning?
(Enter a date like "Jun 30" or just hit Enter for next week)
```

Derive the Monday-Sunday date range.

### Step 2: Performance analysis

```
Agent: performance-reporter
Input: "Analyze all posted content across LinkedIn, X, and Reddit and produce the weekly
performance report."
```

### Step 3: Trend scan

```
Agent: trend-scout
Input: "Find trending AI agent / developer tools topics for the week of [date]. Theme hint:
[any known theme for the week]."
```

### Step 4: Fetch current pipeline

```
Tool: notion-query-database-view
Params: data_source_id = "379f341a-f2a3-80b5-9485-000b2eb7e9cc"
Filter: Publishing date within the week range, Status not "Posted"
```

### Step 5: Synthesize the plan

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WEEKLY CONTENT PLAN — Week of [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THEME: [one-line theme for the week]

PERFORMANCE SUMMARY
[3-line summary from performance-reporter: what worked, what didn't, key pattern]

TRENDING ANGLES THIS WEEK
[2-3 bullets from trend-scout with Ratel angle]

EXISTING PIPELINE
  Mon [date] — [post name] ([status]) — [Account]
  Tue [date] — [post name or //]
  Wed [date] — [post name or //]
  Thu [date] — [post name or //]
  Fri [date] — [post name or //]

RECOMMENDATIONS
  Keep: [what to double down on based on performance]
  Add: [1-2 suggested new posts based on trending topics, per platform]
  Adjust: [any post in pipeline that should change angle based on performance data]

OPEN SLOTS
  [List days with no post scheduled]
  Suggested angle for each: [one line per open slot]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 6: Offer to act

```
What would you like to do?
  draft [topic]   — run /draft for one of the recommended slots
  nothing         — I'll take it from here
```

---

## HARD RULES

Inherited in full from `context/hard-rules.md` — read it before synthesizing any plan.
