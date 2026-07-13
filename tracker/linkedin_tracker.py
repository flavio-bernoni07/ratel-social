#!/usr/bin/env python3
"""
LinkedIn Performance Tracker for Ratel
Fetches LinkedIn post metrics and writes them to the Notion database.

Setup:
  1. NOTION_API_KEY  — get from notion.com/my-integrations
  2. LINKEDIN_API_TOKEN — LinkedIn Developer App bearer token (optional)
  3. LINKEDIN_ORG_ID — numeric org ID from your LinkedIn company page URL (optional)
  4. In each Notion post page, add a line like:
       LinkedIn URL: https://linkedin.com/feed/update/urn:li:activity:7XXXXXXXXX/

Run manually:
  python tracker/linkedin_tracker.py

See tracker/import_csv.py for a no-API-token alternative using LinkedIn's CSV export.
"""

import os
import re
import sys
from datetime import datetime
from typing import Optional

import requests

import notion_client

LINKEDIN_API_TOKEN = os.getenv("LINKEDIN_API_TOKEN")
LINKEDIN_ORG_ID = os.getenv("LINKEDIN_ORG_ID")  # e.g. "110589471"
LINKEDIN_API_URL = "https://api.linkedin.com/rest"


def extract_linkedin_url(text: str) -> Optional[str]:
    """
    Find a LinkedIn post URL in page text.
    The Notion post page should have a line like:
      LinkedIn URL: https://linkedin.com/feed/update/urn:li:activity:7XXXXXXXXX/
    """
    pattern = r'https?://(?:www\.)?linkedin\.com/(?:feed/update|posts)/[^\s\]>]+'
    match = re.search(pattern, text)
    return match.group(0).rstrip("/,)") if match else None


def extract_urn(url: str) -> Optional[str]:
    """Pull the full urn:li:... from a LinkedIn URL."""
    match = re.search(r'(urn:li:(?:activity|ugcPost|share):\d+)', url)
    return match.group(1) if match else None


def _li_headers() -> dict:
    return {
        "Authorization": f"Bearer {LINKEDIN_API_TOKEN}",
        "LinkedIn-Version": "202406",
        "X-Restli-Protocol-Version": "2.0.0",
    }


def fetch_post_stats(post_urn: str) -> Optional[dict]:
    """
    Try two LinkedIn API approaches in order:
      1. Organization share statistics (company page posts) — needs r_organization_social
      2. Posts API (personal or org) — needs r_member_social or r_organization_social
    Returns a dict with reactions, comments, shares, impressions, engagement_rate (as a percent).
    """
    if not LINKEDIN_API_TOKEN:
        return None

    if LINKEDIN_ORG_ID:
        try:
            r = requests.get(
                f"{LINKEDIN_API_URL}/organizationalEntityShareStatistics",
                headers=_li_headers(),
                params={
                    "q": "organizationalEntity",
                    "organizationalEntity": f"urn:li:organization:{LINKEDIN_ORG_ID}",
                    "ugcPosts[0]": post_urn,
                },
                timeout=10,
            )
            if r.status_code == 200:
                elements = r.json().get("elements", [])
                if elements:
                    s = elements[0].get("totalShareStatistics", {})
                    reactions = s.get("likeCount", 0)
                    comments = s.get("commentCount", 0)
                    shares = s.get("shareCount", 0)
                    impressions = s.get("impressionCount", 0)
                    eng = ((reactions + comments + shares) / impressions * 100) if impressions else 0.0
                    return dict(reactions=reactions, comments=comments,
                                shares=shares, impressions=impressions, engagement_rate=eng)
        except Exception:
            pass

    try:
        encoded = requests.utils.quote(post_urn, safe="")
        r = requests.get(
            f"{LINKEDIN_API_URL}/posts/{encoded}",
            headers=_li_headers(),
            timeout=10,
        )
        if r.status_code == 200:
            data = r.json()
            reactions = data.get("likesSummary", {}).get("totalLikes", 0)
            comments = data.get("commentsSummary", {}).get("totalFirstLevelComments", 0)
            shares = data.get("resharesSummary", {}).get("totalReShares", 0)
            impressions = data.get("impressionCount", 0)
            eng = ((reactions + comments + shares) / impressions * 100) if impressions else 0.0
            return dict(reactions=reactions, comments=comments,
                        shares=shares, impressions=impressions, engagement_rate=eng)
    except Exception:
        pass

    return None


def run() -> None:
    print(f"LinkedIn Tracker  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 54)

    notion_client.require_api_key()

    if not LINKEDIN_API_TOKEN:
        print("WARNING: LINKEDIN_API_TOKEN not set — API calls will be skipped.")
        print("  Alternative: use tracker/import_csv.py with LinkedIn's analytics export.\n")

    print("Fetching Posted posts from Notion...")
    posts = notion_client.fetch_posted_posts()
    if not posts:
        print("No posts with Status = 'Posted' found.")
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

        li_url = extract_linkedin_url(text)
        if not li_url:
            print("    ! No LinkedIn URL in page. Add: LinkedIn URL: https://linkedin.com/...")
            skipped += 1
            continue

        post_urn = extract_urn(li_url)
        if not post_urn:
            print(f"    ! Could not parse URN from: {li_url}")
            skipped += 1
            continue

        stats = fetch_post_stats(post_urn)
        if not stats:
            print("    ! Could not fetch metrics. Check token + scopes (r_organization_social).")
            skipped += 1
            continue

        try:
            notion_client.update_metrics(page_id, stats)
            r, c, s, i = stats["reactions"], stats["comments"], stats["shares"], stats["impressions"]
            print(f"    ✓ {r} reactions · {c} comments · {s} shares · {i} impressions "
                  f"· {stats['engagement_rate']:.2f}%")
            updated += 1
        except Exception as e:
            print(f"    ✗ Notion write failed: {e}")
            skipped += 1

    print(f"\n{'=' * 54}")
    print(f"Done: {updated} updated, {skipped} skipped.")


if __name__ == "__main__":
    run()
