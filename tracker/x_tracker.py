#!/usr/bin/env python3
"""
X (Twitter) Performance Tracker for Ratel
Fetches X post metrics via API v2 and writes them to the Notion database.

Setup:
  1. NOTION_API_KEY — get from notion.com/my-integrations
  2. X_API_BEARER_TOKEN — an app-only bearer token from the X Developer Portal
     (developer.x.com). Needs a tier that includes tweet lookup with public_metrics — confirm
     your current plan covers this before relying on the daily run.
  3. In each Notion post page, add a line like:
       X URL: https://x.com/Ratel_AI/status/1234567890123456789

Run manually:
  python tracker/x_tracker.py

Known limitation: X's `public_metrics.impression_count` reflects the view count X shows publicly
on the platform. Whether this field is populated for app-only (bearer token) requests versus only
for the authenticated posting account has changed across X API revisions — verify against
developer.x.com's current docs if impressions come back as 0 for posts you know have views.
"""

import os
import re
import sys
from datetime import datetime
from typing import Optional

import requests

import notion_client

X_API_BEARER_TOKEN = os.getenv("X_API_BEARER_TOKEN")
X_API_URL = "https://api.twitter.com/2"


def extract_x_url(text: str) -> Optional[str]:
    """
    Find an X/Twitter post URL in page text.
    The Notion post page should have a line like:
      X URL: https://x.com/Ratel_AI/status/1234567890123456789
    """
    pattern = r'https?://(?:www\.)?(?:x\.com|twitter\.com)/\w+/status/(\d+)'
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_tweet_id(url: str) -> Optional[str]:
    match = re.search(r'/status/(\d+)', url)
    return match.group(1) if match else None


def fetch_post_stats(tweet_id: str) -> Optional[dict]:
    """Returns a dict with likes, replies, reposts, impressions, engagement_rate (as a percent)."""
    if not X_API_BEARER_TOKEN:
        return None

    try:
        r = requests.get(
            f"{X_API_URL}/tweets",
            headers={"Authorization": f"Bearer {X_API_BEARER_TOKEN}"},
            params={"ids": tweet_id, "tweet.fields": "public_metrics"},
            timeout=10,
        )
        if r.status_code != 200:
            return None
        data = r.json().get("data", [])
        if not data:
            return None
        m = data[0].get("public_metrics", {})
        likes = m.get("like_count", 0)
        replies = m.get("reply_count", 0)
        reposts = m.get("retweet_count", 0) + m.get("quote_count", 0)
        impressions = m.get("impression_count", 0)
        eng = ((likes + replies + reposts) / impressions * 100) if impressions else 0.0
        return dict(likes=likes, replies=replies, reposts=reposts,
                    impressions=impressions, engagement_rate=eng)
    except Exception:
        return None


def run() -> None:
    print(f"X Tracker  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 54)

    notion_client.require_api_key()

    if not X_API_BEARER_TOKEN:
        print("ERROR: X_API_BEARER_TOKEN not set. Add it to .env. Skipping this run.")
        sys.exit(0)  # exit 0, not 1 — this is an expected skip until credentials exist

    print("Fetching Posted posts from Notion...")
    posts = notion_client.fetch_posted_posts()
    posts = [p for p in posts if any(a.startswith("X ") for a in p["accounts"])]
    if not posts:
        print("No Posted posts tagged with an X account found.")
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

        x_url = extract_x_url(text)
        if not x_url:
            print("    ! No X URL in page. Add: X URL: https://x.com/handle/status/...")
            skipped += 1
            continue

        tweet_id = extract_tweet_id(x_url)
        if not tweet_id:
            print(f"    ! Could not parse tweet id from: {x_url}")
            skipped += 1
            continue

        stats = fetch_post_stats(tweet_id)
        if not stats:
            print("    ! Could not fetch metrics. Check X_API_BEARER_TOKEN and API tier.")
            skipped += 1
            continue

        try:
            notion_client.update_x_metrics(page_id, stats)
            print(f"    ✓ {stats['likes']} likes · {stats['replies']} replies "
                  f"· {stats['reposts']} reposts · {stats['impressions']} impressions "
                  f"· {stats['engagement_rate']:.2f}%")
            updated += 1
        except Exception as e:
            print(f"    ✗ Notion write failed: {e}")
            skipped += 1

    print(f"\n{'=' * 54}")
    print(f"Done: {updated} updated, {skipped} skipped.")


if __name__ == "__main__":
    run()
