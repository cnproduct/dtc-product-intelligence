#!/usr/bin/env python3
"""
Google Ads Responsive Search Ads (RSA) & PMax Campaign Builder
--------------------------------------------------------------
Inspired by open-source agent skills:
  - itallstartedwithaidea/agent-skills (Google Ads 12-skill suite)
  - amekala/ads-mcp (Google Ads API v23 MCP server)
  - alphaparkinc/genpark-ad-copy-generator-skill (RSA character validator)

Generates character-compliant Google Ads RSA & Performance Max (PMax) campaigns:
  • 15 RSA Headlines (<= 30 characters each)
  • 4 RSA Descriptions (<= 90 characters each)
  • 2 URL Display Paths (<= 15 characters each)
  • 3 Match-Type Keyword Clusters (Exact, Phrase, Broad)
  • High-Intent Negative Keyword Seed List
  • Performance Max (PMax) Long Headline (<= 90 chars) & Business Name (<= 25 chars)

Usage:
  python3 scripts/google_ads_builder.py --product "Red Light Therapy Face Mask" --brand "LumaGlow"
  python3 scripts/google_ads_builder.py --sku DTC-7D-01
"""

import sys
import json
import argparse
from pathlib import Path

MAX_HEADLINE_LEN = 30
MAX_DESC_LEN = 90
MAX_PATH_LEN = 15
MAX_PMAX_LONG_HL = 90
MAX_BIZ_NAME = 25

def truncate(text: str, max_len: int) -> str:
    text = text.strip()
    return text[:max_len] if len(text) > max_len else text

def build_google_ads(product_name: str, brand: str = "Store", price: str = "$39.99", discount: str = "20% OFF"):
    brand_clean = truncate(brand, MAX_BIZ_NAME)
    
    # 15 RSA Headlines (<= 30 chars each) categorized by intent
    raw_headlines = [
        # 1-3: Brand & Exact Name
        f"{brand_clean}: {product_name}",
        f"Official {product_name}",
        f"Buy {product_name} Online",
        # 4-6: Benefits & Transformation
        f"Fast Visible Results at Home",
        f"Clinical-Grade Home Therapy",
        f"Dermatologist Recommended",
        # 7-9: Offers & Urgency
        f"{discount} - Today Only",
        f"Free 2-Day Express Shipping",
        f"Starting at {price} - Shop Now",
        # 10-12: Trust & Risk Reversal
        f"30-Day Money-Back Guarantee",
        f"Rated 4.9/5 by 12,000+ Buyers",
        f"1-Year Official Warranty",
        # 13-15: Call to Action
        f"Shop Official Online Store",
        f"Order Now & Save {discount}",
        f"Limited Stock - Buy Today"
    ]
    
    headlines = []
    for hl in raw_headlines:
        clean_hl = truncate(hl, MAX_HEADLINE_LEN)
        headlines.append({
            "text": clean_hl,
            "length": len(clean_hl),
            "max": MAX_HEADLINE_LEN,
            "valid": len(clean_hl) <= MAX_HEADLINE_LEN
        })

    # 4 RSA Descriptions (<= 90 chars each)
    raw_descriptions = [
        f"Experience clinical-grade {product_name.lower()} at home. Fast visible results. Order now!",
        f"Rated 4.9/5 by 10,000+ happy buyers. Enjoy {discount} plus free 2-day express delivery.",
        f"Tired of expensive salon treatments? Get dermatologist-approved results for only {price}.",
        f"Risk-free shopping with 30-day money-back guarantee & 1-year warranty. Limited stock left!"
    ]

    descriptions = []
    for desc in raw_descriptions:
        clean_desc = truncate(desc, MAX_DESC_LEN)
        descriptions.append({
            "text": clean_desc,
            "length": len(clean_desc),
            "max": MAX_DESC_LEN,
            "valid": len(clean_desc) <= MAX_DESC_LEN
        })

    # Display paths (<= 15 chars)
    slug_parts = product_name.lower().replace(" ", "-").split("-")
    p1 = truncate(slug_parts[0] if slug_parts else "shop", MAX_PATH_LEN)
    p2 = truncate(slug_parts[1] if len(slug_parts) > 1 else "special", MAX_PATH_LEN)

    # Keywords
    base_kw = product_name.lower()
    exact_kw = [f"[{base_kw}]", f"[{brand.lower()} {base_kw}]", f"[buy {base_kw}]"]
    phrase_kw = [f'"{base_kw}"', f'"best {base_kw}"', f'"{base_kw} reviews"', f'"{base_kw} for sale"']
    broad_kw = [f"{base_kw}", f"home {base_kw} devices", f"affordable {base_kw}"]

    # Negative Keywords
    negatives = [
        "free", "diy", "how to make", "wholesale alibaba", "jobs", "salary", 
        "patent", "pdf manual", "wikipedia", "used ebay", "reddit review", "craigslist"
    ]

    # Performance Max (PMax) Assets
    pmax_long_hl = truncate(f"Shop Top-Rated {product_name} - {discount} & Free 2-Day Shipping", MAX_PMAX_LONG_HL)

    return {
        "platform": "Google Ads Search (RSA) & Performance Max (PMax)",
        "product_name": product_name,
        "brand_name": brand_clean,
        "final_url": f"https://{brand.lower().replace(' ', '')}.com/products/{product_name.lower().replace(' ', '-')}",
        "display_paths": [p1, p2],
        "rsa_headlines_15": headlines,
        "rsa_descriptions_4": descriptions,
        "pmax_assets": {
            "business_name": brand_clean,
            "short_headline": headlines[0]["text"],
            "long_headline": {
                "text": pmax_long_hl,
                "length": len(pmax_long_hl),
                "max": MAX_PMAX_LONG_HL
            },
            "description": descriptions[0]["text"],
            "call_to_action": "Shop Now"
        },
        "target_keywords": {
            "exact_match": exact_kw,
            "phrase_match": phrase_kw,
            "broad_match": broad_kw
        },
        "negative_keywords_seed": negatives
    }

def print_google_ads_report(res: dict):
    print("\n" + "="*80)
    print(f"🎯 GOOGLE ADS RESPONSIVE SEARCH (RSA) & PMAX SPEC: {res['product_name']}")
    print(f"🏢 Brand: {res['brand_name']} | Final URL: {res['final_url']}")
    print(f"🔗 Display URL Path: /{res['display_paths'][0]}/{res['display_paths'][1]}")
    print("="*80)

    print("\n📌 [15 RSA HEADLINES (Max 30 Chars)]")
    for i, h in enumerate(res["rsa_headlines_15"], 1):
        status = "✅" if h["valid"] else "❌"
        print(f"  {i:<2}. {status} ({h['length']}/30 chars): \"{h['text']}\"")

    print("\n📝 [4 RSA DESCRIPTIONS (Max 90 Chars)]")
    for i, d in enumerate(res["rsa_descriptions_4"], 1):
        status = "✅" if d["valid"] else "❌"
        print(f"  {i}. {status} ({d['length']}/90 chars): \"{d['text']}\"")

    print("\n⭐ [PERFORMANCE MAX (PMAX) ASSETS]")
    pmax = res["pmax_assets"]
    print(f"  • Business Name  ({len(pmax['business_name'])}/25 chars): \"{pmax['business_name']}\"")
    print(f"  • Short Headline ({len(pmax['short_headline'])}/30 chars): \"{pmax['short_headline']}\"")
    print(f"  • Long Headline  ({pmax['long_headline']['length']}/90 chars): \"{pmax['long_headline']['text']}\"")
    print(f"  • CTA Button:    {pmax['call_to_action']}")

    print("\n🔑 [KEYWORD INTENT MATRIX]")
    print(f"  • Exact Match  ([kw]):  {', '.join(res['target_keywords']['exact_match'])}")
    print(f"  • Phrase Match (\"kw\"):  {', '.join(res['target_keywords']['phrase_match'])}")
    print(f"  • Broad Match:          {', '.join(res['target_keywords']['broad_match'])}")

    print("\n⛔ [NEGATIVE KEYWORDS SEED LIST (Save Wasted Budget)]")
    print(f"  {', '.join(res['negative_keywords_seed'])}")
    print("="*80 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Ads Campaign Builder")
    parser.add_argument("--product", help="Product name")
    parser.add_argument("--brand", default="LumaStore", help="Brand name")
    parser.add_argument("--price", default="$39.99", help="Retail price")
    parser.add_argument("--discount", default="20% OFF", help="Discount tag")
    parser.add_argument("--sku", help="Lookup SKU from data/trending-dtc-radar.json")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    prod_name = args.product or "Collapsible Foot Spa Bucket"
    brand_name = args.brand
    price_val = args.price
    discount_val = args.discount

    if args.sku:
        radar_path = Path(__file__).resolve().parent.parent / "data" / "trending-dtc-radar.json"
        if radar_path.exists():
            with open(radar_path, "r", encoding="utf-8") as f:
                radar = json.load(f)
            found = False
            for horizon, items in radar.get("horizons", {}).items():
                for item in items:
                    if item.get("product_id") == args.sku:
                        prod_name = item.get("product_name")
                        price_val = f"${item.get('dtc_target_retail', 39.99):.2f}"
                        discount_val = "Special Promo"
                        found = True
                        break
                if found:
                    break

    res = build_google_ads(prod_name, brand=brand_name, price=price_val, discount=discount_val)
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print_google_ads_report(res)
