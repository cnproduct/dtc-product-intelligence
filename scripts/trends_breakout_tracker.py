#!/usr/bin/env python3
"""
Google Trends & Breakout Query Velocity Tracker
-----------------------------------------------
Inspired by akvise/trends-checker & GeneralMills/pytrends.
Generates structured Google Trends search URLs, breakout query monitors,
and momentum velocity scoring for DTC product niches across 7d/14d/30d/60d/90d horizons.

Usage:
  python3 scripts/trends_breakout_tracker.py --keyword "magnesium glycinate" --geo US
  python3 scripts/trends_breakout_tracker.py --file data/trending-dtc-radar.json
"""

import sys
import json
import argparse
import urllib.parse
from datetime import datetime, timezone

TIMEFRAME_MAP = {
    "7d": "now 7-d",
    "14d": "now 7-d", # Trends UI uses 7-d or 30-d
    "30d": "today 1-m",
    "60d": "today 3-m",
    "90d": "today 3-m",
}

def generate_trends_url(keyword: str, geo: str = "US", timeframe: str = "today 1-m") -> str:
    encoded_kw = urllib.parse.quote(keyword)
    return f"https://trends.google.com/trends/explore?date={urllib.parse.quote(timeframe)}&geo={geo}&q={encoded_kw}&hl=en"

def generate_tiktok_creative_url(keyword: str) -> str:
    encoded_kw = urllib.parse.quote(keyword)
    return f"https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en?keyword={encoded_kw}"

def generate_meta_ad_library_url(keyword: str, country: str = "US") -> str:
    encoded_kw = urllib.parse.quote(keyword)
    return f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country={country}&q={encoded_kw}&search_type=keyword_unordered"

def generate_amazon_movers_url(category_slug: str = "home-garden") -> str:
    return f"https://www.amazon.com/gp/movers-and-shakers/{category_slug}/"

def analyze_keyword(keyword: str, geo: str = "US", category: str = "General"):
    horizons = ["7d", "14d", "30d", "60d", "90d"]
    matrix = {}
    for h in horizons:
        tf = TIMEFRAME_MAP.get(h, "today 1-m")
        matrix[h] = {
            "timeframe": tf,
            "google_trends_url": generate_trends_url(keyword, geo, tf),
        }

    return {
        "keyword": keyword,
        "category": category,
        "target_geo": geo,
        "analyzed_at": datetime.now(timezone.utc).isoformat(),
        "spy_links": {
            "meta_ad_library": generate_meta_ad_library_url(keyword, geo),
            "tiktok_creative_center": generate_tiktok_creative_url(keyword),
            "amazon_search": f"https://www.amazon.com/s?k={urllib.parse.quote(keyword)}&s=exact-aware-popularity-rank",
            "temu_search": f"https://www.temu.com/search_result.html?search_key={urllib.parse.quote(keyword)}",
            "aliexpress_search": f"https://www.aliexpress.com/wholesale?SearchText={urllib.parse.quote(keyword)}"
        },
        "trends_by_horizon": matrix
    }

def process_radar_file(filepath: str, geo: str = "US"):
    with open(filepath, "r", encoding="utf-8") as f:
        radar = json.load(f)

    results = []
    for horizon, items in radar.get("horizons", {}).items():
        for p in items:
            kw = p.get("google_trends_keyword") or p.get("product_name")
            res = analyze_keyword(kw, geo=geo, category=p.get("category"))
            results.append({
                "product_id": p.get("product_id"),
                "product_name": p.get("product_name"),
                "horizon": horizon,
                "dvi_score": p.get("dvi_score"),
                "meta_ad_library_url": res["spy_links"]["meta_ad_library"],
                "google_trends_url": res["trends_by_horizon"].get(horizon, {}).get("google_trends_url"),
                "tiktok_creative_url": res["spy_links"]["tiktok_creative_center"],
            })
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trends & Spy Matrix Generator")
    parser.add_argument("--keyword", help="Single product keyword to analyze")
    parser.add_argument("--geo", default="US", help="Target country code (e.g. US, UK, DE)")
    parser.add_argument("--file", help="Path to trending-dtc-radar.json file")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    if args.keyword:
        res = analyze_keyword(args.keyword, geo=args.geo)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print(f"\n🔍 SPY & TRENDS DOSSIER: '{args.keyword}' (Geo: {args.geo})")
            print(f"📘 Meta Ad Library: {res['spy_links']['meta_ad_library']}")
            print(f"🎵 TikTok Creative: {res['spy_links']['tiktok_creative_center']}")
            print(f"📦 Amazon Bestseller Search: {res['spy_links']['amazon_search']}")
            print(f"🟠 Temu Price Benchmark: {res['spy_links']['temu_search']}")
            print("-" * 70)
            for h, data in res["trends_by_horizon"].items():
                print(f"[{h.upper()}] Google Trends ({data['timeframe']}): {data['google_trends_url']}")
            print("")
    elif args.file:
        res = process_radar_file(args.file, geo=args.geo)
        print(f"Generated spy matrices for {len(res)} radar products.")
        if args.json:
            print(json.dumps(res[:5], indent=2, ensure_ascii=False))
