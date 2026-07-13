# Reddit Style + Subreddit Selection

Read `context/hard-rules.md` first. Reddit is the one platform where links are allowed in the body
and mechanism names are expected, not restricted.

## Voice

Data-first, community tone. "Here's what we found," never "We're excited to share." No LinkedIn
anatomy (no hook-line/earn-line structure) — just a clear, honest technical explanation that would
survive being posted by someone with zero marketing background.

- **Title**: factual, descriptive, never marketing. "We measured X and found Y" style, not "Ratel
  is amazing".
- **Body**: genuine technical depth, 150-400 words, links allowed inline.
- Luce posts to Reddit on her own account, not a corporate one — this repo drafts, it never posts.

## Subreddit-picking rubric

Score every candidate subreddit against these five criteria before picking one. Weight roughly in
this order:

1. **Topic/audience fit** — does the sub's core identity match the topic? (r/LocalLLaMA for
   local-model angles, r/MachineLearning for research/benchmark framing, r/AI_Agents for tooling,
   r/programming/r/ExperiencedDevs for general dev-practice, r/SideProject/r/buildinpublic/
   r/microsaas for founder-journey/launch content.)
2. **Self-promo tolerance** — check the sub's current rules/sidebar before committing. Does it ban
   company links outright, require flair, or restrict self-promo to a weekly thread?
3. **Size/activity** — subscriber count + recent post frequency. Too small = no reach, too
   large/generic = buried or stricter mod rules.
4. **Competitor saturation** — has this exact pitch or mechanism been posted repeatedly in this
   sub recently? (Check Style Scout's sampled top posts.)
5. **Content-format fit** — does the sub reward genuine data-first text posts, or is it link-only /
   hostile to first-time company accounts?

A pick only survives if it clears all five, not just the top-scoring one on fit alone. A sub with
perfect topic fit but a hard "no self-promotion" rule is a fail — pick the next-best candidate.

## Candidate shortlist

This is real prior research (from the predecessor repo's `docs/launch-weeks.md` Reddit Strategy
section, carried over here — that file itself isn't part of this repo), not an invented list.
Re-vet live before every use — subreddit rules change.

- **Tier A** — build-in-public / founder journey: r/microsaas, r/SideProject, r/buildinpublic.
  Explicitly **not** r/indiehackers (prior exclusion — keep it).
- **Tier B** — framework-specific, genuine engagement only, high self-promo sensitivity: r/crewAI,
  r/AutoGenAI, r/LangGraph, r/llamaindex. Skip these for anything that reads as launch/promo.
- **Tier C** — standing technical plan: r/LocalLLaMA, r/MachineLearning, r/selfhosted, r/Python,
  r/AI_Agents, r/ExperiencedDevs.
- **Worth live-vetting each time, not pre-cleared**: r/opensource, r/programming.

## Method

Pull the top posts from the last year in each target sub, use them as a style template, and write
in that sub's actual format rather than a generic "Reddit voice." A post that reads like it was
written for a different sub is one of the fastest ways to get removed or downvoted.
