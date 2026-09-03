# X Style Bible

Read `context/hard-rules.md` first — everything there applies on top of this. Note that X is the
one platform where mechanism names (BM25, vector search, MCP) are allowed, framed as steps.

## Hard limit: 280 characters per post — non-negotiable

A single X post (including every tweet in a numbered thread) is capped at **280 characters total**
for a standard account — letters, spaces, punctuation, and emoji all count; a URL always counts as
exactly 23 characters regardless of its real length. This is a platform-enforced hard limit, not a
style preference: past it, the post cannot be published (X Premium raises it to 25,000, but Ratel's
accounts are standard, so write to 280).

**"3-6 short lines" (Format 1, below) describes line count, not a license to ignore the character
budget.** Six short-feeling lines can easily run 400-500+ characters if each line is a full
sentence — that's over the limit even though it "looks like" a short raw post. Before finalizing
any X draft, count the actual character length of the full post (blank lines between paragraphs
count too) and cut until it's under 280. This was missed for two consecutive drafts on 2026-08-15
(435 and 523 characters, both approved through full review before anyone counted characters) —
every drafter and reviewer must check this explicitly, not just judge by "feels short."

**Beyond the hard limit, the user wants X copy shorter and punchier than the drafts have been
trending — short sentences, not long ones, even well within the 280-character budget.** Don't use
all 280 characters just because you can; a tight 120-character post beats a stretched 270-character
one.

**Working target: 150-220 characters.** 280 is the wall you cannot hit, not the goal. Aiming at 280
is how drafts keep sailing past it. Aim at ~180 and you have margin.

**Count it mechanically, don't eyeball it.** Flavio has flagged over-length X drafts more than once
("you always, and I mean always, go over it"), including after the 280 rule was already written
down here — so the rule existing is not enough, the count has to actually be performed and printed.
Paste the final text into a character counter or run
`python3 -c "import sys;print(len(sys.stdin.read().rstrip()))"` and report the number. A draft that
does not carry an actual counted number is not finished.

Reference voice: **@EXM7777 (Machina)** — ~120K followers. Runs **two distinct formats**, not one.
Pick per content, don't default to threads for everything.

## Format 1 — Short raw post (default)

Default for hot takes, warnings, observations, urgency. No numbering, no "1/". 3-6 short lines,
each its own paragraph, blank line between each — reads like verse, not prose. **The whole post,
blank lines included, must be under 280 characters — count it, don't estimate.**

- Opens on an imperative command or a blunt claim: "invest in X, go in debt if you have to" /
  "most agents don't fail because of the model."
- Includes one line with a specific personal/concrete number: "i'm stacking 5 subs" / "we cut
  inference cost by [X]" (only if the benchmark page is live).
- Closes on urgency or a gut-punch, not a tidy summary: "Fable 5 already disappeared" — implies
  things move fast, act now. Not "here's your takeaway."
- Plain spoken language, contractions, "+" instead of "and" is fine. Occasional profanity in
  Machina's own voice — **do not copy the profanity itself into Ratel copy**, keep the punch and
  directness instead.
- This is the default for Ratel content that makes a claim or observation rather than teaching a
  multi-step process. Most Ratel posts should use this format.

## Format 2 — Numbered teaching thread

Only for genuine multi-step tutorials. Numbered (1/ 2/ 3/ ...), 5-15 tweets for Ratel content
(Machina runs 20-50 — his threads teach a full framework, Ratel's should stay tighter). Use only
when the content is actually a sequence of steps someone would follow in order, not a single
observation padded out to look like a thread. **Every individual numbered tweet is its own post
and must independently stay under the 280-character limit** — the numbering prefix ("3/ ") counts
toward that tweet's own 280, not a separate budget.

Shape: hook → one line on why it matters → numbered steps → a named reusable framework, if there
is one → close on the single most important takeaway.

## Hook rules (both formats)

- All lowercase. No title case, minimal punctuation, no em dashes.
- Two dominant shapes:
  1. **"how to [outcome]"** — optionally with a parenthetical qualifier ending in a colon: "how to
     make money with n8n", "how to build ai agents (from the best to ever do it):"
  2. **Pattern-break / contrarian**: "[widely-held assumption] isn't [real reason]" — "the fastest
     way to profit from AI isn't innovation or disruption"
- Name a concrete number or timeframe in the hook when it's true: "3 ways", "in 30 days",
  "0 to 10k".

## Voice assignment

- Roberto's voice for technical posts (mechanism + internals, honest depth).
- Giacomo's voice for business posts (ROI, mission, vs-competitor framing).
- `@Ratel_AI` (brand handle) is low-touch — reposts founders, rarely originates.
