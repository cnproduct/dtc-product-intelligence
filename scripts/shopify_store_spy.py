#!/usr/bin/env python3
"""
Shopify Competitor & Best Seller Spy Engine
-------------------------------------------
Inspired by open-source scrapers (lagenar/shopify-scraper, samoculus/Shopify-Scraper).
Extracts public product data, best sellers, pricing distribution, and launch velocity
directly from any Shopify-powered DTC store without API tokens.

Usage:
  python3 scripts/shopify_store_spy.py --url https://gymshark.com --limit 20
  python3 scripts/shopify_store_spy.py --url https://colourpop.com --json
"""

import sys
import json
import argparse
import urllib.request
import urllib.parse
from datetime import datetime, timezone

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
}

def clean_url(url: str) -> str:
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    parsed = urllib.parse.urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"

def fetch_shopify_json(base_url: str, endpoint: str):
    full_url = f"{base_url}{endpoint}"
    req = urllib.request.Request(full_url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("products", [])
    except Exception as e:
        return None
    return None

def analyze_store(store_url: str, limit: int = 20):
    base_url = clean_url(store_url)
    
    # 1. Fetch best-selling products
    bestsellers = fetch_shopify_json(base_url, f"/collections/all/products.json?sort_by=best-selling&limit={limit}")
    
    # 2. Fetch recent products
    recent_products = fetch_shopify_json(base_url, f"/products.json?limit={limit}")
    
    if not bestsellers and not recent_products:
        return {
            "success": False,
            "error": f"Unable to fetch products from {base_url}. The store may not be Shopify or has blocked /products.json.",
            "store_url": base_url
        }

    products_list = bestsellers or recent_products or []
    
    items = []
    prices = []
    tags_count = {}
    
    for rank, p in enumerate(products_list[:limit], 1):
        variants = p.get("variants", [])
        p_prices = []
        for v in variants:
            try:
                p_prices.append(float(v.get("price", 0)))
            except (ValueError, TypeError):
                pass
        
        min_p = min(p_prices) if p_prices else 0.0
        max_p = max(p_prices) if p_prices else 0.0
        if min_p > 0:
            prices.append(min_p)
            
        tags = p.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]
        for t in tags:
            tags_count[t] = tags_count.get(t, 0) + 1
            
        images = p.get("images", [])
        img_url = images[0].get("src") if images else None
        
        items.append({
            "rank": rank,
            "title": p.get("title"),
            "handle": p.get("handle"),
            "url": f"{base_url}/products/{p.get('handle')}",
            "product_type": p.get("product_type"),
            "vendor": p.get("vendor"),
            "published_at": p.get("published_at"),
            "price_min": min_p,
            "price_max": max_p,
            "variants_count": len(variants),
            "image": img_url,
            "tags": tags[:5]
        })
        
    avg_price = round(sum(prices) / len(prices), 2) if prices else 0.0
    sorted_prices = sorted(prices)
    median_price = sorted_prices[len(sorted_prices)//2] if sorted_prices else 0.0
    top_tags = sorted(tags_count.items(), key=lambda x: x[1], reverse=True)[:8]

    return {
        "success": True,
        "store_url": base_url,
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "total_analyzed": len(items),
        "is_bestseller_sorted": bool(bestsellers),
        "pricing_summary": {
            "min": min(prices) if prices else 0,
            "max": max(prices) if prices else 0,
            "average": avg_price,
            "median": median_price
        },
        "top_tags": [t[0] for t in top_tags],
        "products": items
    }

def print_summary(res: dict):
    if not res.get("success"):
        print(f"❌ Error: {res.get('error')}")
        return

    print("\n" + "="*80)
    print(f"🛒 DTC SHOPIFY SPY REPORT: {res['store_url']}")
    print(f"📅 Scraped At: {res['scraped_at']}")
    print(f"🔥 Mode: {'Best-Selling Sorted' if res['is_bestseller_sorted'] else 'Recent Products'}")
    print(f"💰 Price Range: ${res['pricing_summary']['min']:.2f} - ${res['pricing_summary']['max']:.2f} (Avg: ${res['pricing_summary']['average']:.2f}, Median: ${res['pricing_summary']['median']:.2f})")
    print(f"🏷️  Hot Tags: {', '.join(res['top_tags'])}")
    print("="*80)
    print(f"{'#':<3} | {'Product Name':<42} | {'Price':<12} | {'Type':<18}")
    print("-" * 80)
    for p in res["products"]:
        p_str = f"${p['price_min']:.2f}" if p['price_min'] == p['price_max'] else f"${p['price_min']:.2f}-${p['price_max']:.2f}"
        title = (p['title'][:39] + '...') if len(p['title']) > 42 else p['title']
        ptype = (p['product_type'][:15] + '...') if p['product_type'] and len(p['product_type']) > 18 else (p['product_type'] or "N/A")
        print(f"{p['rank']:<3} | {title:<42} | {p_str:<12} | {ptype:<18}")
    print("="*80 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shopify Store Spy Tool")
    parser.add_argument("--url", required=True, help="Target Shopify store domain (e.g. https://colourpop.com)")
    parser.add_argument("--limit", type=int, default=20, help="Number of products to extract (default: 20)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON format")
    args = parser.parse_args()

    result = analyze_store(args.url, limit=args.limit)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_summary(result)
