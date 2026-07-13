# Flavio's Role — Content & Documentation Lead for Ratel

> Last updated: 2026-06-17. Aligned with Giacomo (CEO) and Rob (CTO).
> Four core activity streams, two paused pending resource availability.

---

## Mission

Drive Ratel's visibility, discoverability, and credibility through strategic content (social media + written), fresh community-driven narratives, and world-class GitHub documentation that converts visitors into engaged design partners.

---

## The Four Core Activities

### 1. Content Curation & Cascading (Ongoing Weekly)

**What it is:** Weekly content pipeline from external creative partner (Luce) → founder approval → social publication.

**Your role:**
- **X (Twitter):** Review Luce's weekly batch (Thursdays EOD CET) independently. Brainstorm 1–2 additional content ideas if the draft set misses an obvious angle.
- **LinkedIn:** Cascade strong X themes to LinkedIn where it makes business sense. Create supporting visual/written assets for planned events (hiring announcements, sponsored talks, product milestones).
- **Collaboration:** Draft the X→LinkedIn cascade plan, align with Giacomo before week publishes, flag any upcoming events on the verge.

**Cadence:** Async review by Sunday, feedback to Luce by Monday for queue.

**KPIs tracked:** Reply volume, follower delta, DM open rates, warm contact flags.

---

### 2. New Social Strategies (Strategic Direction)

**What it is:** Fresh, trend-responsive, personality-driven content that goes beyond the official roadmap.

**Objectives:**
1. Ride emerging trends in AI/tool-calling space (timely, not weeks-late hot takes)
2. Bring authentic community voice to Ratel (less institutional marketing speak, more "here's what we learned")

**Your role:**
- Develop an overall **strategic direction** — what narratives, cadences, content types will make Ratel recognizable in 2–3 weeks.
- Own the strategy unilaterally, then validate with Giacomo.
- Once signed off: **weekly planning** (topics, calendar) + **daily pings** for real-time trending moments.
- Channels: X + LinkedIn equally.

**Collaboration:** This is new territory for Ratel. Giacomo wants to see what you bring to the table that the internal team doesn't. Review phase is a conversation, not a checklist.

**Expected outcome:** Ratel perceived as a knowledgeable, personality-driven voice in the AI-engineering space. Not just announcements.

---

### 3. GitHub Documentation Overhaul (One-off + Ongoing)

**What it is:** Make every repo's landing page + README so good that visitors immediately understand Ratel and want to contribute/integrate.

**Two phases:**

#### Phase 1: One-Off Assessment & Redesign (8–10 weeks)
1. **Audit current state** — review all Ratel repos (ratel, ratel-mcp, ratel-bench, SDKs) for documentation quality, structure, missing assets.
2. **Benchmark:** Research what makes great READMEs in similar projects (check dev-team Slack thread for examples people already flagged).
3. **Propose changes** — structure improvements, wording refinements, visual assets (screenshots, demos, gifs, architecture diagrams).
4. **Alignment:** Block time with Giacomo + Rob to review and sign off.
5. **Implement:** Roll out changes across all repos.

#### Phase 2: Ongoing Maintenance (Continuous)
- **Trigger:** Every time a feature ships.
- **Your responsibility:** Docs reflect the code as it exists today — accurate structure, up-to-date examples, current feature flags.
- **Collaboration:** Stay in close contact with the dev team. When they ship, they tell you what changed. You update docs and ask clarifying questions if needed. (Once ramped, devs will also proactively send you PRs with docs updates.)

**Collaboration Model:** Proactive + lightweight. Weekly sync with Giacomo to confirm no doc gaps on recent ships. Async updates to repos.

**Success metric:** Visitor lands in repo → understands what Ratel is in <30 seconds → finds a clear next step (install, try demo, open issue).

---

### 4. Internal Automations

**Status:** Paused. Re-evaluate in 2–3 weeks.

**Objective** (when resumed): Consolidate all internal automations currently scattered across multiple locations into a single private GitHub repo.

---

## Weekly Touchpoints

| Day | Activity | Participants | Format |
|---|---|---|---|
| **Thursday EOD CET** | X post batch arrives from Luce | Flavio | Async review |
| **Sunday EOD CET** | Feedback to Luce + Giacomo review | Flavio, Giacomo | Slack/async |
| **Weekly (TBD)** | Social strategy check-in | Flavio, Giacomo | Slack or 15min sync |
| **Ongoing (as shipped)** | Docs update after feature ship | Flavio, Rob, Dev team | Async + Slack |

---

## Constraints & Guardrails

### X / LinkedIn Content (from Ratel X Strategy Doc)

**Hard gates (non-negotiable):**
- No token-reduction percentages until Robi publishes the official benchmark page.
- No links in posts — only in first reply.
- No outrage, no dunks (post-Grok algorithm penalty).
- Link to repos only on explicit "we shipped vX" release announcements.
- No claims about Mastra/LangGraph/LangChain adapters unless confirmed by founders.

**Tone:**
- Jack (CEO handle `@Giac_nicoli`): Business framing, customer ROI, vs-competitor takes, mission. Reference voice: `@pupposandro` (Lucebox).
- Rob (CTO handle `@rstagi_`): Mechanism + internals, postmortems, honest technical depth. Reference voice: `@davideciffa` (Lucebox).
- Brand handle (`@Ratel_AI`): Low-touch credential, reposts founders only.

**Format reference:** `@EXM7777` (Machina) — teaching-thread playbooks over single-insight tweets: lowercase "how to [outcome]" or contrarian pattern-break hooks, numbered thread structure, concrete numbers/timeframes in the hook. Governs *how* X posts are built (hook shape, thread structure); Jack/Rob references above still govern *who's* speaking and *what* they say. Full rules in `context/x-style.md`.

**Target creators** (turn on notifications):
`@hrishioa`, `@nutlope`, `@goodside`, `@marktenenholtz`, `@hyhieu226`, `@_xjdr`, `@ivanfioravanti`, `@ash_twtz`, `@Surendar__05`, `@vivek_naskar`, `@i_amanchadha`, `@jovandotse`, `@DegenApeDev`, `@manishkumar_dev`, `@EXM7777`.

---

## Tools & Resources

### Social Strategy Reference
- **X Playbook for Ratel:** Internal doc with persona, voice, plays 1–4, weekly cadence, KPIs
- **Week N posts draft:** Slack thread from Luce (Thursdays EOD CET)
- **Ratel overview doc:** `ratel-overview.md` (this repo)

### Documentation Resources
- **Current repos:**
  - `ratel-ai/ratel` — core library
  - `ratel-ai/ratel-mcp` — MCP gateway
  - `ratel-ai/ratel-bench` — benchmark harness
  - SDKs: TypeScript, Python (and more coming)
- **Dev team:** Slack channel for shipped features and design discussions

---

## Success Metrics

| Activity | Measure | Target | Cadence |
|---|---|---|---|
| **X curation** | Posts shipped on time | 100% by Sunday EOD | Weekly |
| **LinkedIn cascade** | Aligned posts + event assets | 80% coverage of key drops | Weekly |
| **Social strategy** | Follower growth per handle | +100 by week 8 | Weekly |
| **GitHub docs** | Assessment complete | All repos audited + plan drafted | 4 weeks |
| **Docs maintenance** | Update latency | <48h after feature ship | Per ship |

---

## Communication Protocol

- **Async-first:** Slack for updates, feedback, flags
- **Sync when needed:** 15–30min calls with Giacomo/Rob for alignment gates
- **Escalations:** Block time immediately if a decision blocks forward progress
