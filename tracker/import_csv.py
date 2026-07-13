#!/usr/bin/env python3
"""
LinkedIn Analytics CSV Importer for Ratel
Reads LinkedIn's analytics export and writes metrics to Notion — no API token needed.

How to export from LinkedIn:
  1. Go to your LinkedIn Company Page
  2. Click Analytics → Posts (in the left sidebar)
  3. Click Export (top right corner)
  4. Save the CSV
  5. Run: python tracker/import_csv.py path/to/export.csv

Matching logic (in order):
  1. LinkedIn URL stored in Notion page body (most reliable)
  2. Publishing date from Notion database property (fallback — works if one post per day)
"""

import csv
import sys
from datetime import datetime
from typing import Optional

import notion_client
from linkedin_tracker import extract_linkedin_url, extract_urn

# LinkedIn analytics CSV column names (LinkedIn may vary these slightly)
COL_URL = ["Post link", "Post URL", "URL", "Content URL", "Permalink"]
COL_DATE = ["Created date", "Published date", "Date published", "Date", "Published at"]
COL_REACTIONS = ["Reactions", "Likes", "Like count"]
COL_COMMENTS = ["Comments", "Comment count"]
COL_SHARES = ["Reposts", "Shares", "Reshares"]
COL_IMPRESSIONS = ["Impressions", "Impression count"]
COL_ENGAGEMENT = ["Engagement rate (%)", "Engagement rate", "Engagement Rate (%)"]


def find_col(row: dict, candidates: list[str]) -> Optional[str]:
    for c in candidates:
        if c in row:
            return row[c]
    return None


def parse_date(val: Optional[str]) -> str:
    if not val:
        return ""
    val = val.strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%B %d, %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(val, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return val[:10]


def parse_pct(val: Optional[str]) -> float:
    """Returns a percent (4.38), not a fraction — matches notion_client.update_metrics."""
    if not val:
        return 0.0
    cleaned = val.strip().rstrip("%").replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def load_csv(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def run(csv_path: str) -> None:
    print("LinkedIn CSV Importer")
    print("=" * 54)

    notion_client.require_api_key()

    try:
        rows = load_csv(csv_path)
    except FileNotFoundError:
        print(f"ERROR: File not found: {csv_path}")
        sys.exit(1)

    if not rows:
        print("ERROR: CSV is empty.")
        sys.exit(1)

    print(f"CSV loaded: {len(rows)} rows")
    print(f"Columns: {list(rows[0].keys())}\n")

    csv_by_urn: dict[str, dict] = {}
    csv_by_date: dict[str, dict] = {}

    for row in rows:
        url_val = find_col(row, COL_URL) or ""
        date_val = parse_date(find_col(row, COL_DATE))
        reactions = int(float(find_col(row, COL_REACTIONS) or 0))
        comments = int(float(find_col(row, COL_COMMENTS) or 0))
        shares = int(float(find_col(row, COL_SHARES) or 0))
        impressions = int(float(find_col(row, COL_IMPRESSIONS) or 0))
        eng_raw = find_col(row, COL_ENGAGEMENT)
        if eng_raw:
            eng = parse_pct(eng_raw)
        elif impressions:
            eng = (reactions + comments + shares) / impressions * 100
        else:
            eng = 0.0

        stats = dict(reactions=reactions, comments=comments,
                     shares=shares, impressions=impressions, engagement_rate=eng)

        urn = extract_urn(url_val)
        if urn:
            csv_by_urn[urn] = stats
        if date_val:
            if date_val in csv_by_date:
                csv_by_date[date_val] = None  # multiple posts on same date → ambiguous
            else:
                csv_by_date[date_val] = stats

    print(f"CSV: {len(csv_by_urn)} posts matched by URN, "
          f"{sum(1 for v in csv_by_date.values() if v)} unambiguous dates.\n")

    print("Fetching Posted posts from Notion...")
    posts = notion_client.fetch_posted_posts()
    print(f"Found {len(posts)} posted Notion page(s).\n")

    updated, skipped = 0, 0

    for post in posts:
        name, page_id, pub_date = post["name"], post["page_id"], post["pub_date"]
        print(f"  {name}  [{pub_date}]")

        stats: Optional[dict] = None
        match_method = ""

        try:
            text = notion_client.fetch_page_text(page_id)
            li_url = extract_linkedin_url(text)
        except Exception as e:
            print(f"    ! Could not read page: {e}")
            skipped += 1
            continue

        if li_url:
            urn = extract_urn(li_url)
            if urn and urn in csv_by_urn:
                stats = csv_by_urn[urn]
                match_method = "URL"
            elif urn:
                print(f"    ! URL found in page but URN {urn} not in CSV.")

        if not stats and pub_date:
            day_stats = csv_by_date.get(pub_date)
            if day_stats is not None:
                stats = day_stats
                match_method = f"date ({pub_date})"
            elif pub_date in csv_by_date:
                print(f"    ! Multiple posts on {pub_date} in CSV — can't match by date. "
                      "Add a LinkedIn URL to the Notion page.")

        if not stats:
            if not li_url:
                print("    ! No LinkedIn URL in page and no date match.")
                print("      Add a line: LinkedIn URL: https://linkedin.com/feed/update/urn:li:activity:XXXXXXXX/")
            skipped += 1
            continue

        try:
            notion_client.update_linkedin_metrics(page_id, stats)
            r, c, s, i = stats["reactions"], stats["comments"], stats["shares"], stats["impressions"]
            print(f"    ✓ [{match_method}] {r} reactions · {c} comments · {s} shares "
                  f"· {i} impressions · {stats['engagement_rate']:.2f}%")
            updated += 1
        except Exception as e:
            print(f"    ✗ Notion write failed: {e}")
            skipped += 1

    print(f"\n{'=' * 54}")
    print(f"Done: {updated} updated, {skipped} skipped.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tracker/import_csv.py path/to/linkedin-export.csv")
        print("\nHow to export:")
        print("  LinkedIn Company Page → Analytics → Posts → Export (top right)")
        sys.exit(1)
    run(sys.argv[1])
