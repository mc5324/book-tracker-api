
import os
import sys
import csv
import time
import argparse
from typing import Any, Dict, List, Optional

import requests
import pandas as pd
from dotenv import load_dotenv

API_URL = "https://www.googleapis.com/books/v1/volumes"

def normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """Safely flatten fields from Google Books item into a row dict."""
    volume = item.get("volumeInfo", {}) or {}
    sale = item.get("saleInfo", {}) or {}
    access = item.get("accessInfo", {}) or {}

    authors = volume.get("authors") or []
    categories = volume.get("categories") or []

    return {
        "id": item.get("id"),
        "title": volume.get("title"),
        "subtitle": volume.get("subtitle"),
        "authors": ", ".join(authors) if isinstance(authors, list) else authors,
        "publisher": volume.get("publisher"),
        "publishedDate": volume.get("publishedDate"),
        "description": volume.get("description"),
        "pageCount": volume.get("pageCount"),
        "categories": ", ".join(categories) if isinstance(categories, list) else categories,
        "averageRating": volume.get("averageRating"),
        "ratingsCount": volume.get("ratingsCount"),
        "language": volume.get("language"),
        "infoLink": volume.get("infoLink"),
        "previewLink": volume.get("previewLink"),
        "canonicalVolumeLink": volume.get("canonicalVolumeLink"),
        "isEbook": sale.get("isEbook"),
        "webReaderLink": access.get("webReaderLink"),
    }

def fetch_books(q: str, api_key: Optional[str], max_results: int = 20, page_size: int = 40, sleep_s: float = 0.1) -> List[Dict[str, Any]]:
    """Fetch up to max_results books, handling pagination via startIndex.
    Google Books allows maxResults up to 40 per request.
    """
    results: List[Dict[str, Any]] = []
    start = 0
    page_size = max(1, min(page_size, 40))

    while len(results) < max_results:
        remaining = max_results - len(results)
        this_page = min(page_size, remaining)

        params = {
            "q": q,
            "startIndex": start,
            "maxResults": this_page,
        }
        if api_key:
            params["key"] = api_key

        resp = requests.get(API_URL, params=params, timeout=30)
        if resp.status_code != 200:
            raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")

        data = resp.json()
        items = data.get("items") or []
        if not items:
            break

        for item in items:
            results.append(normalize_item(item))

        start += this_page
        time.sleep(sleep_s)  # be polite

    return results

def to_dataframe(rows: List[Dict[str, Any]]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    # keep a friendly column order
    cols = [
        "id", "title", "subtitle", "authors", "publisher", "publishedDate",
        "categories", "pageCount", "averageRating", "ratingsCount",
        "language", "infoLink", "previewLink", "canonicalVolumeLink",
        "isEbook", "webReaderLink", "description"
    ]
    return df.reindex(columns=cols)

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Search Google Books and save to CSV.")
    parser.add_argument("--q", required=True, help="Search query (e.g., 'atomic habits')")
    parser.add_argument("--max", type=int, default=20, help="Max results to fetch (default: 20)")
    parser.add_argument("--page-size", type=int, default=40, help="Page size per request (<=40)")
    parser.add_argument("--out", type=str, default="", help="Optional CSV output path (e.g., data/books.csv)")
    parser.add_argument("--no-desc", action="store_true", help="Drop long description column for compact CSV")
    args = parser.parse_args()

    api_key = os.getenv("GOOGLE_BOOKS_API_KEY", "").strip() or None

    try:
        rows = fetch_books(q=args.q, api_key=api_key, max_results=args.max, page_size=args.page_size)
    except Exception as e:
        print(f"[ERROR] Failed to fetch books: {e}", file=sys.stderr)
        sys.exit(1)

    if not rows:
        print("[INFO] No results found.")
        sys.exit(0)

    df = to_dataframe(rows)
    if args.no_desc and "description" in df.columns:
        df = df.drop(columns=["description"])

    if args.out:
        os.makedirs(os.path.dirname(args.out), exist_ok=True)
        df.to_csv(args.out, index=False, quoting=csv.QUOTE_MINIMAL)
        print(f"[OK] Wrote {len(df)} rows to {args.out}")
    else:
        # Show a compact preview
        with pd.option_context("display.max_rows", 10, "display.max_colwidth", 80):
            print(df.head(10))

if __name__ == "__main__":
    main()
