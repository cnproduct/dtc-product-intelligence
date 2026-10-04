#!/usr/bin/env python3
"""
ChatGPT Ads & SearchGPT Conversational Campaign Builder
------------------------------------------------------
Inspired by open-source projects:
  - fseixas/chatgpt-ads-builder (Claude/Agent ChatGPT Ads Skill)
  - alphaparkinc/genpark-ad-copy-generator-skill (Character validator)
  - AI-Marketing-Hub/chatgpt-ads (OpenAI Advertiser guidelines)

Builds character-compliant ads for OpenAI / ChatGPT Ads format:
  • Headline: <= 35 characters
  • Description: <= 67 characters
  • Conversational Context Hints: 3-5 natural query prompts that trigger the ad
  • 1024x1024 thumbnail generation prompt

Usage:
  python3 scripts/chatgpt_ad_builder.py --product "Red Light Therapy Face Mask" --brand "LumaGlow" --offer "20% OFF"
  python3 scripts/chatgpt_ad_builder.py --sku DTC-7D-01
"""

import sys
import json
import argparse
from pathlib import Path

MAX_HEADLINE_LEN = 35
MAX_DESCRIPTION_LEN = 67

def validate_length(text: str, max_len: int, label: str):
    length = len(text)
    is_valid = length <= max_len
    return {
        "text": text,
        "length": length,
        "max_length": max_len,
        "is_valid": is_valid,
        "status": "PASS" if is_valid else f"FAIL (exceeded by {length - max_len} chars)"
    }

def build_chatgpt_ad(product_name: str, brand: str = "Store", benefit: str = "", offer: str = "Free Shipping"):
    # Generate 2 tailored copy variants that strictly fit 35 / 67 char limits
    # Variant A: Benefit & Solution focused
    h1 = f"{brand}: {product_name}"[:MAX_HEADLINE_LEN]
    d1 = f"Clinical-grade {benefit or 'results at home'}. {offer}. Order today!"
    if len(d1) > MAX_DESCRIPTION_LEN:
        d1 = f"Top-rated {product_name[:20]}. {offer}. Shop official store!"[:MAX_DESCRIPTION_LEN]

    # Variant B: Social Proof / Offer focused
    h2 = f"Try {product_name}"[:MAX_HEADLINE_LEN]
    d2 = f"Over 10,000+ happy buyers. {offer} with 30-day money-back guarantee."
    if len(d2) > MAX_DESCRIPTION_LEN:
        d2 = f"Rated 4.9/5 by 10,000+ customers. {offer} today only!"[:MAX_DESCRIPTION_LEN]

    # Conversational Context Hints (Natural user prompts that should trigger this sponsored recommendation)
    context_hints = [
        f"User asking for the best {product_name.lower()} recommendation for daily use",
        f"User comparing top alternatives to high-end {product_name.lower()} brands",
        f"User looking for reliable solutions with fast shipping and {offer.lower()}",
        f"User researching affordable home wellness and personal care gadgets"
    ]

    # 1024x1024 icon/thumbnail visual prompt
    image_prompt = (
        f"A clean, minimalist 1024x1024 commercial product photo of {product_name}, "
        "studio lighting on modern pastel background, high resolution, no text overlay, centered product aesthetic."
    )

    val_h1 = validate_length(h1, MAX_HEADLINE_LEN, "Variant A Headline")
    val_d1 = validate_length(d1, MAX_DESCRIPTION_LEN, "Variant A Description")
    val_h2 = validate_length(h2, MAX_HEADLINE_LEN, "Variant B Headline")
    val_d2 = validate_length(d2, MAX_DESCRIPTION_LEN, "Variant B Description")

    return {
        "platform": "ChatGPT Ads / OpenAI Sponsored Recommendations",
        "product_name": product_name,
        "brand": brand,
        "campaign_constraints": {
            "headline_char_limit": MAX_HEADLINE_LEN,
            "description_char_limit": MAX_DESCRIPTION_LEN,
            "all_passed": all([val_h1["is_valid"], val_d1["is_valid"], val_h2["is_valid"], val_d2["is_valid"]])
        },
        "ad_variants": [
            {
                "variant_id": "A_benefit_focused",
                "headline": val_h1,
                "description": val_d1,
                "display_url": f"https://{brand.lower().replace(' ', '')}.com/{product_name.lower().replace(' ', '-')}"
            },
            {
                "variant_id": "B_social_proof",
                "headline": val_h2,
                "description": val_d2,
                "display_url": f"https://{brand.lower().replace(' ', '')}.com/special-offer"
            }
        ],
        "conversational_context_hints": context_hints,
        "thumbnail_image_prompt": image_prompt
    }

def print_ad_report(res: dict):
    print("\n" + "="*80)
    print(f"🤖 CHATGPT ADS / SEARCHGPT CAMPAIGN SPEC: {res['product_name']}")
    print(f"🏢 Brand: {res['brand']} | Compliance: {'✅ ALL PASSED' if res['campaign_constraints']['all_passed'] else '❌ OVER LIMIT'}")
    print("="*80)
    
    print("\n📝 [AD CREATIVE VARIANTS (Enforcing 35/67 Character Limits)]")
    for v in res["ad_variants"]:
        print(f"  • {v['variant_id'].upper()}:")
        h = v["headline"]
        d = v["description"]
        print(f"    Headline    ({h['length']}/{h['max_length']} chars) [{h['status']}]: \"{h['text']}\"")
        print(f"    Description ({d['length']}/{d['max_length']} chars) [{d['status']}]: \"{d['text']}\"")
        print(f"    Display URL: {v['display_url']}")
        print()

    print("💬 [CONVERSATIONAL SEARCH CONTEXT HINTS (Natural Prompt Triggers)]")
    for i, hint in enumerate(res["conversational_context_hints"], 1):
        print(f"  {i}. \"{hint}\"")

    print("\n🎨 [THUMBNAIL IMAGE PROMPT (1024x1024)]")
    print(f"  Prompt: {res['thumbnail_image_prompt']}")
    print("="*80 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ChatGPT Ads Campaign Builder")
    parser.add_argument("--product", help="Product name")
    parser.add_argument("--brand", default="LumaStore", help="Brand name")
    parser.add_argument("--benefit", default="visible skin rejuvenation", help="Core user benefit")
    parser.add_argument("--offer", default="20% OFF + Free 3-Day Shipping", help="Promotional offer")
    parser.add_argument("--sku", help="Lookup SKU from data/trending-dtc-radar.json")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    prod_name = args.product or "Collapsible Foot Spa Bucket"
    brand_name = args.brand
    benefit_text = args.benefit
    offer_text = args.offer

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
                        benefit_text = item.get("breakout_reason", "")[:30]
                        found = True
                        break
                if found:
                    break

    res = build_chatgpt_ad(prod_name, brand=brand_name, benefit=benefit_text, offer=offer_text)
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print_ad_report(res)
