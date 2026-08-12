# Ratel — Company & Product Overview

> Last updated: 2026-08-12. Source: github.com/ratel-ai/ratel + github.com/ratel-ai/ratel-mcp READMEs, ADR 0012, roadmap.md, plus a live #product Slack scan (live-checked, not internal Notion).
> Tags used throughout: [exists] = ships today; [net-new] = planned, not built; [deferred] = real but later.
> Note: the top-level ratel-ai/ratel README changed substantially since 2026-06-17 — it now leads with the skills suite (`npx skills add ratel-ai/skills --all`) rather than the SDK as the primary "fastest way to integrate." If drafting install-flow copy, re-check the live README rather than assuming this doc's Install Commands section below is still the lead framing.
> Every fact below with a specific date attached was true on that date — re-verify anything load-bearing (a benchmark number, a "not built yet" claim, a shipped-feature name) against Slack or the live repo before it goes in a post, don't just trust this file's age.

---

## What Ratel Is

Ratel is a **context-engineering platform for AI agents**. Its job is to decide what information ends up in an AI's working memory (called the "context window") on each turn — specifically, which tools and skills the AI is allowed to see and use.

The core problem: AI agents with large tool catalogs (50, 100, 200+ tools) suffer because the AI reads every tool description on every single message. This burns tokens (= money), confuses the AI, and slows everything down. Ratel fixes this by acting like a smart librarian: instead of showing the AI all 200 tools, it retrieves only the 3–5 most relevant ones for the current task.

---

## The Three Repos — Three Parts of One Story

| Repo | Role | Plain English |
|---|---|---|
| `ratel-ai/ratel` | The Library | The engine developers embed in their own AI apps |
| `ratel-ai/ratel-mcp` | The Showcase | A ready-made product built on the library, for Claude Code / Cursor users |
| `ratel-ai/ratel-bench` | The Proof | Benchmark tests proving the claims are real |

---

## Business Model: Open-Core (Modeled on Supabase)

- The foundation (Core Lib, SDKs, Core Server) is **free and open-source**
- A managed **Cloud tier** on top is the paid product
- Unique twist vs Supabase: the SDK can run **fully in-process** (no server at all), in addition to calling a server
- Money comes from companies that don't want to self-host — they pay Ratel to run it for them with extra smart features

---

## The Full Stack — Five Layers

### Layer 1: Core Lib `[exists]`

The engine. Written in Rust (fast, safe). Pure and stateless — it does no saving, no internet calls, no database. You hand it your tool definitions at startup; it builds an in-memory search index; when your app stops, everything disappears.

**Contains:**
- **Tool Catalog** — the list of tools, each with name/description/schemas/search index/embeddings
- **Skill Catalog** `[exists]` — same but for skills (multi-step recipes). Skills do NOT flow through MCP itself (the host reads `SKILL.md` files directly); Ratel sources them from a Ratel-managed folder (`~/.ratel/skills/`) and surfaces them via `search_capabilities`'s `skills` bucket + `get_skill_content` (see ADR 0012). A dedicated suite lives at `ratel-ai/skills` (`npx skills add ratel-ai/skills --all`).
- **BM25 lexical search** — keyword text search, genuinely zero infrastructure, the default method
- **Semantic + hybrid retrieval** `[exists as of ADR-0011]` — opt-in `SearchMethod`: `Bm25` (default), `Semantic`, or `Hybrid` (BM25 + dense fused via Reciprocal Rank Fusion). The dense arm runs a local in-process embedding model (`BAAI/bge-small-en-v1.5`, pure-Rust Candle) — no vector DB, no external embedding API, no service to deploy. Corrected 2026-07-09: this doc previously said semantic/vector search was `[net-new]`/not built; verified against the live repo, it has shipped.
- **Usage analytics event model** — defines the shape of logs; does not store them
- **Model-routing event** — fires a "this skill prefers this model" signal; does not act on it

**The rule:** the lib does no I/O, no persistence, no external model calls. Everything it needs is fed to it at startup. This is what makes it run with zero infrastructure.

---

### Layer 2: SDKs `[exists]`

Wrappers that make the Core Lib usable in specific programming languages.

| SDK | Language | Install | Bridge technology |
|---|---|---|---|
| `@ratel-ai/sdk` | TypeScript / JavaScript | `pnpm add @ratel-ai/sdk` | NAPI-RS |
| `ratel-ai` | Python | `pip install ratel-ai` | PyO3 |
| More | Coming later | — | — |

The Rust Core Lib is pre-compiled and bundled inside the package. Developers don't need to install Rust.

**Two interchangeable backends (same API, different execution):**
- **Embed mode** (today): Core Lib runs inside your app. Zero infrastructure.
- **Server mode** `[net-new]`: SDK calls the Core Server over the network. For scale.

**Key objects the SDKs expose:**
- `ToolRegistry` — search-only index (metadata, no execution)
- `ToolCatalog` — search + execution (the full thing)
- `search_capabilities` — the gateway tool you give the AI to find tools
- `invoke_tool` — the gateway tool you give the AI to run a tool it found
- `registerMcpServer` — pulls an existing MCP server's tools into the catalog
- Opt-in telemetry (off by default)

**The "no infra" asterisk:** BM25 text search = truly zero infra. Semantic/vector search requires an embedding provider (e.g. OpenAI embeddings API). Not zero infra.

---

### Layer 3: Core Server `[net-new — not built]`

Everything the Core Lib deliberately omits: IO, database, external model calls, cross-session state. Self-hostable, open-source. Supabase-style.

**Adds on top of Core Lib:**
- **API Controller** — HTTP interface the SDK calls in server mode
- **Model-providers adapter** — generates embeddings (calls OpenAI, Voyage, local models, etc.)
- **Chat Management** — stores full conversation histories in PostgreSQL
- **Usage Analytics** — aggregates log events into summaries
- **PostgreSQL persistence** — real database; state survives restarts
- **Continuous Improvement (basic)** — uses usage data + any configured AI model to suggest better tool/skill descriptions

**Why not built yet:** Core Lib + SDKs already deliver the core value. Server adds scale and persistence, needed once the foundation is validated.

---

### Layer 4: Coding Harness Plugins `[mostly net-new]`

Plugins that integrate Ratel directly into the coding tools developers use daily: Claude Code, Codex (OpenAI), OpenCode (open-source alternative).

**Contains:**
- **CLI** `[exists]` — the `ratel` terminal command. Today's only shipped piece of this layer.
  - `ratel inspect` — read telemetry logs from AI sessions
  - `ratel mcp import` — interactive wizard that scans Claude Code's MCP setup and moves servers behind Ratel
  - `ratel serve` / `ratel mcp serve` — run the Ratel gateway locally
  - `ratel backup` — save config before making changes
- **Local Daemon** `[net-new]` — a background process running on your machine with UI, backend, local persistence, cloud client
- **Plugin system** `[net-new]` — adapters for each specific harness (Claude Code, Codex, OpenCode)
- **Model Routing consumer** `[net-new]` — receives model-preference signals from the Core Lib and executes model switches inside the harness

**Note:** The daemon intentionally overlaps the Core Server. It's an experiment layer expected to converge into the Core Server over time, not a permanent second server.

---

### Layer 5: Cloud `[net-new — not built at all]`

The paid, managed, closed-source tier. Ratel runs the Core Server for you, with smarter extra features.

**Contains:**
- **Managed Server** — hosted Core Server, no ops work for the customer
- **Advanced Analytics** — deeper usage pattern analysis beyond the OSS aggregation
- **Continuous Improvement (advanced)** — same loop as basic, but using fine-tuned AI models trained specifically for this task. The closed part is the trained model weights, not the mechanism.
- **Advanced Model Routing** `[open — not yet designed]` — smarter routing decisions computed in the Cloud
- **Skill/Workflow Suggestion** — proposes BRAND NEW skills from observed usage patterns. Cloud-only because it needs an extra AI model call to extract intent from chat history.

---

### Benchmark `[exists — separate repo]`

Lives at `ratel-ai/ratel-bench`. Not a product tier — the validation/honesty bar. Every shippable capability must beat a real baseline here before it counts as done.

**Three eval modes:**
1. **MetaTool retrieval-only** — does the right tool come back? Free, deterministic, fast.
2. **ToolRet retrieval-only** — tests against a public 43k-tool corpus other researchers also use, for external comparability.
3. **MetaTool tasks + LLM-as-judge** — full end-to-end: AI agent runs real tasks, a separate AI grades quality. Measures accuracy, token usage, dollar cost.

**Published numbers (headline):**
- Local AI model: accuracy 8% → 77% with Ratel
- Open-source cloud model: +12 percentage points accuracy, −85% input tokens
- Claude Sonnet (frontier): −82% input tokens, −68% cost

---

## Key Concepts (Plain English)

### Retrieval
Fetching the relevant things from a large pile. When the AI is about to respond, Ratel searches the full tool catalog and pulls out only the relevant subset for this specific task. Like a librarian who gives you 5 books instead of all 50,000.

### BM25
The search algorithm Ratel uses for retrieval. Keyword-based text matching — the same family as early Google Search. No math embeddings needed. Fast, deterministic (same input always gives same output), genuinely zero infrastructure.

### Semantic / Vector Search `[net-new]`
A smarter search that understands meaning, not just keywords. Converts text into mathematical coordinates (embeddings) and finds tools that are "near" the query in that space. Requires an external embedding provider — NOT zero infrastructure.

### Replace vs Suggest Mode
- **Replace (default):** AI's tool list for this turn IS the top search results. Nothing else visible.
- **Suggest (opt-in):** All tools stay visible; Ratel adds hints about which are most relevant.

### Skills
Multi-step recipes (playbooks) that live alongside tools in the same catalog, found the same way. A tool is one action (send email). A skill is a full workflow (onboard new employee: create email → add to Slack → send welcome → assign laptop). When a skill surfaces in search results, the tools it uses are automatically surfaced alongside it.

### Model Routing
Skills can declare a model preference: "this task needs Claude Opus" or "this is simple, use Haiku." The Core Lib fires this as a signal (a "routing event"). The harness, server, or Cloud receives it and switches the active AI model. The hint is always overridable. Routing = picking the right model for the right task, not picking the right agent.

### Library (Lib)
A package of code you include inside your own project. It doesn't run standalone — your app calls it when needed. Like a cookbook you keep on your shelf: it doesn't cook for you, but when you need a recipe, you open it. Ratel's Core Lib is a Rust library you embed in your app.

### Harness
The coding tool/environment that wraps an AI agent for developer use. Claude Code, Codex, OpenCode are all "coding harnesses" — they're the shell developers use daily that has AI built in. A "harness plugin" is an integration that makes Ratel work inside that shell automatically.

### Daemon
A program that runs silently in the background on your machine all the time, like Dropbox syncing files without you thinking about it. Ratel's planned daemon would coordinate catalog search, show a UI panel, and hold local state — all running quietly while you work.

### In-Process / Embedded Mode
The Core Lib runs inside your app's own memory. No separate server, no network call, no database. Everything happens in the same process. When your app stops, nothing persists. Zero infrastructure.

### Context Window
An AI model's working memory for one conversation turn. Everything the model reads before generating a response. Ratel's entire job is managing what goes into this window — specifically, keeping it free of irrelevant tool clutter.

### MCP (Model Context Protocol)
A standard communication protocol (like HTTP for the web) for how AI hosts (Claude Code, Cursor, ChatGPT) talk to tool servers. Ratel works on both sides: as a client (ingesting tools from upstream MCP servers) and as a server (exposing a filtered catalog to AI hosts).

### Open-Core
Business model where the foundation is free/open-source and a managed cloud version is the paid product. Supabase is the canonical example. Ratel follows this model.

### PostgreSQL
The most widely-used professional relational database. Used in the Core Server tier for durable storage of chats, logs, and catalog state.

### Embeddings
The process of converting text into mathematical coordinates. Used for semantic (meaning-based) search. Not required for BM25 text search. Requires an external provider (e.g. OpenAI Embeddings API) or a local model.

---

## Recent Ships (verify still current before quoting)

### Dynamic Ranking `[exists, shipped 2026-07-27]`
Also called "Adaptive Ranking" in some internal Slack messages — Dynamic Ranking is the name
confirmed in the founder meeting transcript, use that one. The catalog learns from what actually
gets picked: if an agent selects a lower-ranked tool or skill and it turns out to be the right one,
that item's rank rises for similar future queries. Queries are clustered, and items that keep
performing well within a cluster keep climbing.

**Status as of 2026-08-12: live and on by default, but no measured accuracy lift yet** — no
concrete metrics, not trialed with specific clients in a controlled way. It's an indirect accuracy
mechanism (compensates for inconsistent phrasing), not a direct one. Cost implications haven't been
addressed either. Per the hard rule on unmeasured claims (`context/hard-rules.md`), describe the
mechanism and intent only — never imply a proven or measured outcome until this status changes.

### Docs "Ask AI" `[exists, shipped 2026-08-06]`
An AI chat button on docs.ratel.sh (bottom-right corner of every page) that answers questions about
Ratel's documentation. Built by Fausto. Minor feature, not typically its own post, but useful
context if a post touches the docs experience.

## What Is Built Today vs Not Built

| Component | Status |
|---|---|
| Core Lib — BM25 tool search | **EXISTS** |
| TypeScript SDK | **EXISTS** |
| Python SDK | **EXISTS** |
| CLI (`ratel` command, basic) | **EXISTS** |
| MCP server / gateway | **EXISTS** (in `ratel-mcp` repo) |
| Benchmark harness + results | **EXISTS** (in `ratel-bench` repo) |
| Skill Catalog | **EXISTS** (gateway-level, via `ratel-mcp` + `ratel-ai/skills` suite) |
| Semantic / hybrid retrieval | **EXISTS** (ADR-0011, opt-in, local in-process embedding model, no vector DB) |
| Core Server (entire tier) | not built |
| SDK server mode | not built (waits for Core Server) |
| Harness plugins (daemon, UI) | not built |
| Model routing consumer | not built |
| Cloud (all of it) | not built |
| Advanced model routing | not even fully designed |

---

## Roadmap Horizons

| Version | Focus |
|---|---|
| v0.1.x (now) | Tool search + Skills + Telemetry + Semantic search + LLM-driven suggestions |
| v0.2.x | Chat management (long-running agent memory) |
| v0.3.x | Memories (facts that persist across sessions) |
| v0.4.x | Context Graph — tools, skills, memories, history in one unified substrate |
| Cloud (parallel) | Managed server + Advanced analytics + Continuous improvement + Skill suggestion |

---

## The "Context Graph" — End Goal

One unified system where tools, skills, memories, and conversation history all live in the same searchable catalog. Every AI turn, the system retrieves exactly what that specific moment needs from all four content types. Same retrieval engine for everything. Layered on top: a continuous improvement loop that watches what gets used and makes the catalog smarter over time.

---

## Three Repos Quick Reference

```
ratel-ai/ratel       → library (embed in your own app)
ratel-ai/ratel-mcp   → MCP gateway product (for Claude Code / Cursor users)
ratel-ai/ratel-bench → benchmark proof (performance numbers)
```

## Install Commands (Only These Exist Today)

```bash
# TypeScript
pnpm add @ratel-ai/sdk

# Python
pip install ratel-ai
pip install 'ratel-ai[mcp]'   # + MCP support

# CLI
pnpm add -g @ratel-ai/cli

# MCP server (for Claude Code / Cursor) — tool retrieval
npx -y @ratel-ai/mcp-server --help
ratel-mcp mcp import              # migrate existing MCP servers into the gateway

# Skills gateway — skill retrieval (separate command, not part of `mcp import`)
ratel-mcp skill activate          # moves ~/.claude/skills -> ~/.ratel/skills so
                                   # the gateway can serve them via search_capabilities
                                   # + get_skill_content (reversible: `skill deactivate`)

# Onboarding skills suite (meta — teaches the agent to set up Ratel itself)
npx skills add ratel-ai/skills --all

# Rust
cargo add ratel-ai-core
```

**Two setup steps today, not one.** `mcp import` (tools) and `skill activate` (skills) are
separate top-level CLI verbs with no combined wizard — running one does not trigger the
other. Don't imply a single "drop Ratel in front of everything" command in copy; it's two.
(Roadmap note, not for external claims yet: a unified single command for the MCP + skills
gateway setup is expected eventually — flag to Flavio before publicly promising it.)
