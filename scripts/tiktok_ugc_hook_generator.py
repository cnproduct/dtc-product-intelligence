#!/usr/bin/env python3
"""
TikTok Ads UGC Storyboard & High-Converting Hook Generator
---------------------------------------------------------
Inspired by open-source projects:
  - tarxn/tiktok-ads-scraper (ad longevity & demographic intelligence)
  - amekala/ads-mcp & AdsMCP/tiktok-ads-mcp-server (TikTok Ads API specs)
  - lofe-w/tiktok-creative-center-scraper-public (Creative Center trends)

Generates 4 high-converting 3-second visual hooks, full 30s UGC storyboards,
and TikTok ad copy with hashtag clusters for any DTC winning product.

Usage:
  python3 scripts/tiktok_ugc_hook_generator.py --product "Ultrasonic Jewelry Cleaner" --pain "dirty cloudy rings" --price "$34.99"
  python3 scripts/tiktok_ugc_hook_generator.py --sku DTC-7D-01
"""

import sys
import json
import argparse
import urllib.parse
from pathlib import Path

def generate_tiktok_campaign(product_name: str, pain_point: str = "daily fatigue", target_audience: str = "young adults", price: str = "$39.99"):
    encoded_kw = urllib.parse.quote(product_name)
    creative_center_url = f"https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en?keyword={encoded_kw}"

    hooks = [
        {
            "angle": "Pattern Interrupt / Skeptic Challenge",
            "hook_text": f"I genuinely thought this TikTok viral {product_name} was a total gimmick until I tried it...",
            "visual_action": f"Creator holding {product_name} close to camera with skeptical squint, then cutting directly to dramatic before-and-after demonstration.",
            "audio_vibe": "Suspenseful build-up cutting to upbeat trending beat drop."
        },
        {
            "angle": "Negative Warning / Cost Savings",
            "hook_text": f"Stop scrolling! If you're still wasting hundreds of dollars on {pain_point}, watch this right now.",
            "visual_action": f"Hand slapping red stop sign or throwing old expensive products into trash, revealing {product_name}.",
            "audio_vibe": "Urgent voiceover with high-tempo background tick."
        },
        {
            "angle": "Oddly Satisfying ASMR Reveal",
            "hook_text": f"This is hands down the most oddly satisfying thing you'll see on your FYP today.",
            "visual_action": f"Macro close-up, crisp unboxing, tactile click or instant foaming/cleaning action with loud ASMR sound effects.",
            "audio_vibe": "Zero background music, pure crisp high-definition ASMR sound effects."
        },
        {
            "angle": "The 'TikTok Made Me Buy It' Relatability",
            "hook_text": f"Ranking random things TikTok convinced me to buy: 10 out of 10, no regrets.",
            "visual_action": f"Selfie-cam walk-and-talk in cozy living room/bedroom showing daily lifestyle integration.",
            "audio_vibe": "Casual conversational lo-fi indie background music."
        }
    ]

    storyboard = [
        {
            "timestamp": "0:00 - 0:03",
            "section": "The Hook (First 3 Seconds)",
            "visual": f"Fast-paced clip of {product_name} solving {pain_point}. High contrast, bold on-screen text caption.",
            "speech": hooks[0]["hook_text"],
            "on_screen_text": f"STOP SCROLLING ⚠️ ({product_name})"
        },
        {
            "timestamp": "0:04 - 0:10",
            "section": "The Pain Point & Agitation",
            "visual": f"Creator reenacting common frustration with {pain_point}. Shows failed traditional alternatives.",
            "speech": f"I used to struggle with {pain_point} every single week, and none of the expensive alternatives actually worked.",
            "on_screen_text": f"The problem with regular solutions..."
        },
        {
            "timestamp": "0:11 - 0:18",
            "section": "The 'Aha!' Mechanism & Demonstration",
            "visual": f"Side-by-side split screen showing {product_name} working in real time. Macro detail on key features.",
            "speech": f"Then I found this {product_name}. It uses smart design to fix it in under 60 seconds with zero effort.",
            "on_screen_text": "Watch this happen in real time 👇"
        },
        {
            "timestamp": "0:19 - 0:25",
            "section": "Social Proof & Scarcity",
            "visual": f"Screen recording of 5-star customer reviews, viral unboxing montage, and 'Almost Sold Out' badge.",
            "speech": f"It has over 4.9 stars and keeps selling out on TikTok Shop. Plus they have a 30-day money back guarantee.",
            "on_screen_text": "⭐ 4.9/5 Stars | 12,000+ Happy Customers"
        },
        {
            "timestamp": "0:26 - 0:30",
            "section": "Call to Action (CTA)",
            "visual": f"Finger pointing down to the bright orange shopping bag / CTA button with flash discount badge.",
            "speech": f"Click the link below right now to grab yours for just {price} while current batch is in stock!",
            "on_screen_text": f"Shop Now 👉 Only {price} + Free Shipping"
        }
    ]

    ad_copies = [
        f"TikTok made me buy it and it's actually worth the hype! 🤯 Get 50% OFF today only.",
        f"Say goodbye to {pain_point} forever! 🚀 Over 10,000+ sold this month. Tap Shop Now!",
        f"Best purchase of 2026 hands down 🔥 30-day trial + Free Express Delivery."
    ]

    hashtags = [
        "#tiktokmademebuyit",
        "#amazonfinds",
        "#viralproduct",
        "#lifehacks",
        f"#{product_name.lower().replace(' ', '')}",
        "#musthaves"
    ]

    return {
        "product_name": product_name,
        "pain_point": pain_point,
        "target_audience": target_audience,
        "price_point": price,
        "tiktok_creative_center_url": creative_center_url,
        "hooks": hooks,
        "storyboard_30s": storyboard,
        "recommended_ad_copies": ad_copies,
        "hashtag_cluster": hashtags,
        "recommended_cta_button": "Shop Now"
    }

def print_tiktok_report(res: dict):
    print("\n" + "="*80)
    print(f"🎵 TIKTOK ADS HIGH-CONVERTING UGC BLUEPRINT: {res['product_name']}")
    print(f"🎯 Target Audience: {res['target_audience']} | Price Point: {res['price_point']}")
    print(f"🔗 Creative Center Spy: {res['tiktok_creative_center_url']}")
    print("="*80)

    print("\n⚡ [TOP 4 CONVERTING 3-SECOND HOOK ANGLES]")
    for i, h in enumerate(res["hooks"], 1):
        print(f"  {i}. 【{h['angle']}】")
        print(f"     🎙️ Audio Hook: \"{h['hook_text']}\"")
        print(f"     🎬 Visual Cue: {h['visual_action']}")
        print()

    print("⏱️ [FULL 30-SECOND UGC VIDEO STORYBOARD]")
    print("-" * 80)
    print(f"{'Time':<15} | {'Section':<22} | {'Speech & Visual'}")
    print("-" * 80)
    for s in res["storyboard_30s"]:
        speech_snippet = (s['speech'][:45] + '...') if len(s['speech']) > 48 else s['speech']
        print(f"{s['timestamp']:<15} | {s['section']:<22} | {speech_snippet}")
        print(f"{'':<15}   🎬 Visual: {s['visual']}")
        print(f"{'':<15}   🔤 Text:   {s['on_screen_text']}")
        print("-" * 80)

    print("\n📝 [TIKTOK IN-FEED AD COPIES]")
    for copy in res["recommended_ad_copies"]:
        print(f"  • \"{copy}\"")

    print("\n🏷️  [HASHTAG MATRIX]")
    print(f"  {' '.join(res['hashtag_cluster'])}")
    print("="*80 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TikTok Ads UGC Storyboard Generator")
    parser.add_argument("--product", help="Product name")
    parser.add_argument("--pain", default="everyday inconvenience", help="Core pain point")
    parser.add_argument("--audience", default="Gen Z & Millennials", help="Target audience")
    parser.add_argument("--price", default="$39.99", help="Price point")
    parser.add_argument("--sku", help="Lookup SKU from data/trending-dtc-radar.json")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    prod_name = args.product or "Ultrasonic Jewelry Cleaner"
    pain_pt = args.pain
    aud = args.audience
    price_pt = args.price

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
                        pain_pt = item.get("breakout_reason", "")
                        price_pt = f"${item.get('dtc_target_retail', 39.99):.2f}"
                        found = True
                        break
                if found:
                    break

    res = generate_tiktok_campaign(prod_name, pain_point=pain_pt, target_audience=aud, price=price_pt)
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print_tiktok_report(res)
