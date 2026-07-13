# Hard Rules — Single Source of Truth

Every drafting and review agent in this repo reads this file. If a rule here conflicts with
anything else (a Style Bible, a memory, a habit), this file wins.

## Rules that apply to every platform (LinkedIn, X, Reddit)

- **No em dashes (—). Ever.** Not in hooks, not in body, not in takeaways. Use a period, a colon,
  or a line break instead. This is the paramount rule — it overrides every other style preference.
  A double-hyphen (`--`) used as an em-dash substitute is still a violation in spirit.
- **No benchmark or token-reduction percentages** until Rob confirms the benchmark page is live.
  If a draft would naturally include one, flag it in commentary outside the draft, never embed a
  bracketed note inside the draft copy itself.
- **No repo-shipped claims** ("we shipped vX") without founder confirmation.
- **No Mastra / LangGraph / LangChain adapter claims** without founder confirmation.
- **No manipulative CTAs**: "Comment X for the guide", "tag someone who needs this", "share if you
  agree", "like if you agree".
- **Banned phrases**: "I'm excited to announce", "Thrilled to share", "Game changer", "leverage",
  "synergy".
- **No outrage, no dunks.**
- Never present a number, result, or anecdote borrowed from someone else's product as Ratel's own.

## Rules that differ by platform

| Rule | LinkedIn | X | Reddit |
|---|---|---|---|
| Mechanism names (BM25, vector search, MCP internals) | **Not allowed** in body — describe outcomes only | **Allowed**, framed as steps rather than jargon-drops | **Allowed** — Reddit's technical audience expects real depth |
| Links in body | **Not allowed** — first reply only | **Not allowed** — final reply only | **Allowed** — Reddit posts are expected to link out |
| Length | 150-250 words (up to 400 for milestones) | Short post: 3-6 lines. Thread: 5-15 tweets, only for genuine step sequences | 150-400 words |
| Hashtags / emoji | Max 3 hashtags, max 2 emoji | Not used | Not used — off-genre for Reddit |
| Tone | Direct, honest, specific, earned over claimed | Terser, imperative, closes on urgency not summary | Data-first, community tone, "here's what we found" not "we're excited to share" |

## Why this file exists

The old repo (`ratel-linkedin`) had these rules duplicated across `CLAUDE.md`, `post-notion.md`,
and `virality-reviewer.md`, and they drifted (e.g. `post-notion.md` said X allows mechanism names
in a section `CLAUDE.md`'s top-level hard rules didn't mention). Every agent in this repo reads
this one file instead of re-deriving rules from a command prompt.
