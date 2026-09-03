# LinkedIn Style Bible

Read `context/hard-rules.md` first — everything there applies on top of this.

## Voice

Direct, honest, specific. Like a knowledgeable peer, not a marketer. Earned over claimed.

Focus on the problem and the outcome. Do NOT name internal mechanisms: no "BM25", no "vector
search", no algorithm names. Describe what happens for the user, not how Ratel does it internally.

**Giacomo's patterns (closest style match):**
- Leads with the problem or mechanism, never the company name
- Metaphors that stick: "context rots", "context window as tax", "smart librarian"
- Short punchy statements + one explanatory line
- Takes positions, no hedging ("might", "could", "perhaps")
- Slightly irreverent, self-aware about being a startup

## Line breaks — non-negotiable, overrides "paragraph" language below

Flavio has said this explicitly, repeatedly, in caps: every distinct beat/thought gets its
own line, separated by a line break (or a blank line between short beats). Never write a
"paragraph" as 2-3 sentences run together on one line — that reads as a wall of text
("chucky") and gets rejected regardless of how good the content is.

Wherever this file or any other doc says "3-5 short paragraphs" or "one sentence," treat
that as "3-5 short beats, each on its own line, one idea per line." A single line can still
run a little long if it's one continuous thought, but never stack two sentences on one line.

**Bad (rejected every time):**
```
Testing whether tool filtering would even help usually means building the thing that would
prove it. A place to store the catalog. A service to run search over it. Something to keep
alive while you test. That upfront cost is why plenty of teams never test the idea at all.
```

**Good:**
```
We burned through a Claude Max plan in under a day.
Not on reasoning. Not on output. On setup.
Before it did anything useful, it read every tool we had registered.
All of them. Every single time.
```

## Hard structural gate — check mechanically before returning any draft

Not judgment calls. Count them:

1. **No paragraph block longer than 2 sentences, ever.** One is the default. Three is a rejection.
2. **Total word count ≤ 80.** Count the words. Report the number in the draft output.
3. **No line longer than ~20 words.** If a line needs a comma-spliced second clause, it's two lines.
4. **Cut every hedge and every meta-clause.** "and it's worth explaining plainly why it's true",
   "the fix isn't X, it's Y, the same way...", "First... Second..." — connective tissue is padding.
   Delete it and let the line breaks do the joining.
5. **Fragments are allowed and encouraged.** "2 things go wrong at scale." then two bullet lines.
   Not "Two things go wrong at scale. First, the agent runs out of attention: with enough options
   in front of it, it starts confusing similar-sounding tools."
6. **Digits, not words.** "80 tools" not "eighty tools". "2 things" not "Two things".
7. **Bullet lines (`- `) are fine on LinkedIn** for a 2-3 item list. Often better than prose beats.
8. **Trailing off with `…` beats finishing the thought** when the reader can complete it themselves.

### Worked before/after — Flavio's own rewrite, 2026-08-18

This is the calibration. Left is what the pipeline produced (rejected). Right is what he shipped.

**REJECTED (~190 words, 5 paragraph blocks):**
```
Most AI agents don't fail because the model is bad. They fail because they don't have the right
context to work with.

That idea is circulating widely among people building production agents right now, and it's worth
explaining plainly why it's true.

Every time an agent responds, it first reads a description of every tool it's allowed to use. If
it has eighty tools, it reads eighty descriptions before it reads your actual question.

Two things go wrong at scale. First, the agent runs out of attention: with enough options in front
of it, it starts confusing similar-sounding tools. Second, it spends so much of its working memory
on tool descriptions that there's less room left to actually reason about the task.

The fix isn't a smarter model. It's showing the agent fewer, more relevant options for the specific
thing it's doing right now, the same way a good search engine doesn't hand you every page on the
internet.
```

**SHIPPED (~105 words, every beat on its own line):**
```
AI agents fail because they don't have the right context to work with.

That idea is circulating widely among people building production agents right now.

Every time an agent responds, it first reads a description of every tool and skill it's allowed to
use. If it has 80, it reads 80…

2 things go wrong at scale.

- it starts confusing similar tools.

- it spends its working memory on descriptions leaving less room left to reason about the task.

It's showing the agent more relevant options for the task.

The same way a good search engine doesn't hand you every page on the internet.
```

What changed, concretely: the hedged second clause of the hook cut entirely; "and it's worth
explaining plainly why it's true" deleted; "eighty" → "80"; the First/Second paragraph became two
bullet fragments; "the same way a good search engine..." promoted from a trailing subordinate clause
to its own standalone closing line. Nothing was added. Every edit was a deletion or a line break.

## Post anatomy

```
LINE 1 — THE HOOK (10-15 words max)
Tension, curiosity, or a punch that stops the scroll. No em dashes.

LINE 2 — THE EARN
One sentence. Makes clicking "see more" obvious.

[BLANK LINE]

LINES 3-6 — THE CORE
3-5 short beats, each on its own line (see "Line breaks" above — not paragraph blocks).
Concrete: specific numbers, outcomes, real moments.
No mechanism names. No token-reduction % until Rob's benchmark page is live.

LINE 7 — THE TAKEAWAY
One sentence. The single thing the reader walks away with.

LINE 8 — THE QUESTION (optional, only if genuine)
A real question: "Has anyone seen a different pattern here?" not "What do you think?"
```

## Hook formulas

From the Style Bible (fallback when Style Scout finds nothing live):
- **Counterintuitive:** "Most AI agents don't fail because of the model."
- **Specific moment:** "I spent 6 months thinking we had a model problem. We had a context problem."
- **Pattern break:** "Everyone is talking about [X]. Nobody is talking about [Y]."
- **Number punch:** "One change dropped our token cost by 82%. It wasn't the model." (only usable
  once the benchmark page is live — see hard-rules.md)

Broader mad-lib families, useful when the above don't fit the brief:
- **Curiosity:** "I was wrong about [common belief]." / "The real reason [outcome] happens isn't
  what you think." / "[Impressive result] — and it only took [surprisingly short time]."
- **Story:** "Last week, [unexpected thing] happened." / "I almost [big mistake/failure]." /
  "3 years ago, I [past state]. Today, [current state]."
- **Value:** "How to [desirable outcome] (without [common pain]):" / "[Number] [things] that
  [outcome]:" / "Stop [common mistake]. Do this instead:"
- **Contrarian:** "Unpopular opinion: [bold statement]" / "[Common advice] is wrong. Here's why:" /
  "I stopped [common practice] and [positive result]."

## Voice guardrails

- **No AI-slop rhythm.** Don't write in identical metronomic beats where every line is the same
  length with a period after every clause — that's the obvious LLM tell. Fix it by *varying line
  length* (a 4-word line next to a 14-word line), not by merging beats into paragraph blocks.
  **This guardrail previously said "let two or three related ideas share a paragraph" — that was
  wrong and it is what produced the block-paragraph draft rejected on 2026-08-18. Never merge
  beats into a paragraph. The line-break rule wins, always.**
- **No self-referential hooks.** Don't open by inventing a specific reader action or scenario you
  can't actually know ("You added a skill last week and..."). General second-person claims are
  fine ("Most agents don't fail because of the model"); a fabricated specific moment about the
  reader is not.
- **No yapping hooks.** Even when the post has a personal or physical-moment anchor, the hook
  itself stays terse. Save the color for the earn line and body, not the first sentence.
- **First-person posts stay first-person.** A founder-voiced or personal post speaks as one named
  person ("I shipped this last week"), not "we" — don't let a personal angle drift into corporate
  plural mid-post.

## Visuals

Real screenshot > data chart/table > diagram > text card > nothing. Never stock photos.

## Length

**~60-80 words target — confirmed 2026-08-16, supersedes the old 150-250 range.** A first
tightening pass to ~127-142 words was still judged too long. Structure: hook (own line), 1-2 tight
core beats (own line each), one closer/takeaway or question. Every beat still gets its own line per
the non-negotiable line-break rule below — short doesn't mean cramming ideas back onto one line,
it means cutting beats and words, not spacing. A story-driven milestone or a post that genuinely
needs a worked example can run longer, but treat that as the exception, not the default.
