"""
Shared Notion read/write module for Ratel's content trackers.
Used by linkedin_tracker.py, import_csv.py, and (once built) x_tracker.py / reddit_tracker.py.

Every platform tracker follows the same shape: find Posted pages, pull a source URL out of the
page body, fetch platform stats, PATCH the same metric properties back onto the page. This module
holds the Notion half so each platform tracker only has to implement the platform-API half.
"""

import os
from datetime import date
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = "379f341af2a380e49a2fe0a6282d4c23"
NOTION_API_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


def headers() -> dict:
    return {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def require_api_key() -> None:
    if not NOTION_API_KEY:
        raise SystemExit("ERROR: NOTION_API_KEY not set. Add it to .env")


def fetch_posted_posts() -> list[dict]:
    """Fetch all pages with Status = 'Posted', with name + publishing date + page id."""
    body = {
        "filter": {"property": "Status", "status": {"equals": "Posted"}},
        "page_size": 100,
    }
    r = requests.post(
        f"{NOTION_API_URL}/databases/{NOTION_DATABASE_ID}/query",
        headers=headers(),
        json=body,
        timeout=15,
    )
    r.raise_for_status()
    posts = []
    for page in r.json()["results"]:
        titles = page["properties"].get("Name", {}).get("title", [])
        name = titles[0]["plain_text"] if titles else "Untitled"
        pub_date = (page["properties"].get("Publishing date", {}).get("date") or {})
        pub_date_str = pub_date.get("start", "")[:10] if pub_date else ""
        accounts = [
            opt.get("name", "")
            for opt in page["properties"].get("Account", {}).get("multi_select", [])
        ]
        posts.append({
            "page_id": page["id"],
            "name": name,
            "pub_date": pub_date_str,
            "accounts": accounts,
        })
    return posts


def fetch_page_text(page_id: str) -> str:
    """Concatenate all rich-text from all blocks in a page."""
    lines: list[str] = []
    url: Optional[str] = f"{NOTION_API_URL}/blocks/{page_id}/children"
    while url:
        r = requests.get(url, headers=headers(), timeout=15)
        r.raise_for_status()
        data = r.json()
        for block in data["results"]:
            btype = block.get("type", "")
            rich = block.get(btype, {}).get("rich_text", [])
            lines.extend(seg.get("plain_text", "") for seg in rich)
        cursor = data.get("next_cursor")
        url = (f"{NOTION_API_URL}/blocks/{page_id}/children?start_cursor={cursor}"
               if cursor else None)
    return "\n".join(lines)


def update_metrics(page_id: str, stats: dict) -> None:
    """
    Write engagement numbers back to Notion.
    `stats` keys: reactions, comments, shares, impressions, engagement_rate (as a percent, e.g.
    4.38 not 0.0438 — this function does the percent-to-decimal conversion Notion expects).
    """
    properties = {
        "Reactions": {"number": int(stats.get("reactions", 0))},
        "Comments": {"number": int(stats.get("comments", 0))},
        "Shares": {"number": int(stats.get("shares", 0))},
        "Impressions": {"number": int(stats.get("impressions", 0))},
        "Engagement Rate": {"number": round(stats.get("engagement_rate", 0.0) / 100, 6)},
        "Last Updated": {"date": {"start": date.today().isoformat()}},
    }
    r = requests.patch(
        f"{NOTION_API_URL}/pages/{page_id}",
        headers=headers(),
        json={"properties": properties},
        timeout=15,
    )
    r.raise_for_status()
