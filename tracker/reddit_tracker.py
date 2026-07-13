#!/usr/bin/env python3
"""
Reddit Performance Tracker for Ratel
Fetches Reddit post metrics via the Reddit API (app-only OAuth2) and writes them to Notion.

Setup:
  1. NOTION_API_KEY — get from notion.com/my-integrations
  2. Register a Reddit "script" app at reddit.com/prefs/apps to get REDDIT_CLIENT_ID and
     REDDIT_CLIENT_SECRET. REDDIT_USER_AGENT should be a descriptive string
     (e.g. "ratel-social-tracker/1.0 by u/yourusername") — Reddit aggressively rate-limits or
     blocks generic/missing user agents.
  3. In each Notion post page, add a line like:
       Reddit URL: https://www.reddit.com/r/LocalLLaMA/comments/1abcxyz/some_title/

Run manually:
  python tracker/reddit_tracker.py

Known limitation: Reddit has no "impressions" concept, so there is no Engagement Rate field for
Reddit in Notion — only Upvotes, Comments, and Upvote Ratio are tracked. Reddit also fuzzes vote
counts for anti-manipulation purposes, so exact numbers are approximate by design on Reddit's end,
not a bug in this script.
"""

import os
import re
import sys
from datetime import datetime
from typing import Optional

import requests

import notion_client

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "ratel-social-tracker/1.0")


def extract_reddit_url(text: str) -> Optional[str]:
    """
    Find a Reddit post URL in page text.
    The Notion post page should have a line like:
      Reddit URL: https://www.reddit.com/r/LocalLLaMA/comments/1abcxyz/some_title/
    """
    pattern = r'https?://(?:www\.)?reddit\.com/r/\w+/comments/(\w+)/[^\s\]>]*'
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_post_id(url: str) -> Optional[str]:
    match = re.search(r'/comments/(\w+)/', url)
    return match.group(1) if match else None


def _get_access_token() -> Optional[str]:
    if not (REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET):
        return None
    try:
        r = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET),
            data={"grant_type": "client_credentials"},
            headers={"User-Agent": REDDIT_USER_AGENT},
            timeout=10,
        )
        if r.status_code != 200:
            return None
        return r.json().get("access_token")
    except Exception:
        return None


def fetch_post_stats(post_id: str, token: str) -> Optional[dict]:
    """Returns a dict with upvotes, comments, upvote_ratio (as a percent)."""
    try:
        r = requests.get(
            "https://oauth.reddit.com/by_id/" + f"t3_{post_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "User-Agent": REDDIT_USER_AGENT,
            },
            timeout=10,
        )
        if r.status_code != 200:
            return None
        children = r.json().get("data", {}).get("children", [])
        if not children:
            return None
        d = children[0].get("data", {})
        return dict(
            upvotes=d.get("ups", 0),
            comments=d.get("num_comments", 0),
            upvote_ratio=d.get("upvote_ratio", 0.0) * 100,
        )
    except Exception:
        return None


def run() -> None:
    print(f"Reddit Tracker  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 54)

    notion_client.require_api_key()

    token = _get_access_token()
    if not token:
        print("ERROR: Could not get a Reddit access token. Check REDDIT_CLIENT_ID / "
              "REDDIT_CLIENT_SECRET in .env. Skipping this run.")
        sys.exit(0)  # exit 0, not 1 — this is an expected skip until credentials exist

    print("Fetching Posted posts from Notion...")
    posts = notion_client.fetch_posted_posts()
    posts = [p for p in posts if "Reddit Jack" in p["accounts"]]
    if not posts:
        print("No Posted posts tagged with a Reddit account found.")
        return
    print(f"Found {len(posts)} post(s).\n")

    updated, skipped = 0, 0

    for post in posts:
        name, page_id = post["name"], post["page_id"]
        print(f"  {name}")

        try:
            text = notion_client.fetch_page_text(page_id)
        except Exception as e:
            print(f"    ! Could not read page: {e}")
            skipped += 1
            continue

        reddit_url = extract_reddit_url(text)
        if not reddit_url:
            print("    ! No Reddit URL in page. Add: Reddit URL: https://www.reddit.com/r/.../comments/...")
            skipped += 1
            continue

        post_id = extract_post_id(reddit_url)
        if not post_id:
            print(f"    ! Could not parse post id from: {reddit_url}")
            skipped += 1
            continue

        stats = fetch_post_stats(post_id, token)
        if not stats:
            print("    ! Could not fetch metrics.")
            skipped += 1
            continue

        try:
            notion_client.update_reddit_metrics(page_id, stats)
            print(f"    ✓ {stats['upvotes']} upvotes · {stats['comments']} comments "
                  f"· {stats['upvote_ratio']:.0f}% upvote ratio")
            updated += 1
        except Exception as e:
            print(f"    ✗ Notion write failed: {e}")
            skipped += 1

    print(f"\n{'=' * 54}")
    print(f"Done: {updated} updated, {skipped} skipped.")


if __name__ == "__main__":
    run()
