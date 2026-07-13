#!/usr/bin/env python3
"""
X (Twitter) Performance Tracker for Ratel — STUB, not implemented.

Not wired up yet. Before building this out:
  1. X API v2 access requires a paid tier for post analytics (impressions, engagements) beyond
     basic public metrics (likes, reposts, replies) — confirm which tier Ratel has before assuming
     impressions/engagement-rate are obtainable at all.
  2. Decide the same "how do we find the post" problem linkedin_tracker.py solves with a
     `LinkedIn URL:` line in the page body — probably an `X URL:` line pointing at the tweet.
  3. Reuse tracker/notion_client.py for the Notion half (fetch_posted_posts, fetch_page_text,
     update_metrics) exactly like linkedin_tracker.py does — only the platform-API half needs
     writing here.

Do not run this file — it will exit immediately.
"""

import sys

if __name__ == "__main__":
    print("x_tracker.py is a stub. X API v2 access/tier needs confirming before this is built.")
    print("See the module docstring for what's needed.")
    sys.exit(1)
