#!/usr/bin/env python3
"""
Reddit Performance Tracker for Ratel — STUB, not implemented.

Not wired up yet. Before building this out:
  1. Reddit's API (PRAW or direct REST) gives upvotes, comment count, and upvote ratio per post —
     no "impressions" equivalent exists, so the Engagement Rate formula used for LinkedIn/X
     (reactions+comments+shares)/impressions won't translate directly; decide a Reddit-appropriate
     metric (e.g. upvote ratio, or comments-per-upvote) before writing this.
  2. Needs a Reddit app registration (client_id/client_secret) for API access.
  3. Decide the same "how do we find the post" problem linkedin_tracker.py solves with a
     `LinkedIn URL:` line in the page body — probably a `Reddit URL:` line pointing at the post.
  4. Reuse tracker/notion_client.py for the Notion half exactly like linkedin_tracker.py does.

Do not run this file — it will exit immediately.
"""

import sys

if __name__ == "__main__":
    print("reddit_tracker.py is a stub. See the module docstring for what's needed.")
    sys.exit(1)
