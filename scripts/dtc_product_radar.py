#!/usr/bin/env python3
"""
DTC Cross-Border Product Intelligence CLI Tool
Author: cnproduct (贸启航 / Product Radar)
License: MIT

Zero-dependency Python CLI tool to load, score, and evaluate trending DTC e-commerce products
across 5 forecast time horizons (7d, 14d, 30d, 60d, 90d) and 8 data platforms.
"""

import sys
import json
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_PATH = BASE_DIR / "data" / "trending-dtc-radar.json"
PLATFORM_PATH = BASE_DIR / "data" / "platform-matrix.json"
SCORING_PATH = BASE_DIR / "data" / "dtc-scoring-model.json"

def load_json(filepath):
    if not filepath.exists():
        print(f"Error: Required file not found at {filepath}", file=sys.stderr)
        sys.exit(1)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def print_overview(data):
    meta = data.get("metadata", {})
    products = data.get("products", [])
    
    print("\n" + "=" * 85)
    print(f"  {meta.get('title', 'DTC Product Intelligence')} (v{meta.get('version', '1.0')})")
    print(f"  Total Tracked Products: {len(products)} Hero SKUs across 5 Forecast Horizons")
    print("=" * 85 + "\n")
    
    horizons = [
        ("7d", "Next 7 Days (Flash Viral / Dropship)"),
        ("14d", "Next 14 Days (Short-Term Social Viral)"),
        ("30d", "Next 30 Days (Monthly Mainstay / Air Restock)"),
        ("60d", "Next 60 Days (Quarterly Holiday Hero / Sea Freight)"),
        ("90d", "Next 90 Days (Next-Season Early Bird / Tooling & OEM)")
    ]
    
    for h_code, h_name in horizons:
        h_prods = [p for p in products if p.get("horizon") == h_code]
        avg_dvi = sum(p.get("dvi_score", 0) for p in h_prods) / len(h_prods) if h_prods else 0
        print(f"┌─ [{h_code.upper()}] {h_name} ({len(h_prods)} SKUs | Avg DVI: {avg_dvi:.1f})")
        for idx, p in enumerate(h_prods[:5], 1):
            fob = p.get("economics", {}).get("fob_usd", 0)
            msrp = p.get("economics", {}).get("dtc_retail_usd", 0)
            margin = p.get("economics", {}).get("margin_multiplier", "N/A")
            print(f"│  {idx}. {p.get('sku_name')[:48]:<48} | FOB: ${fob:>4.2f} -> MSRP: ${msrp:>5.2f} ({margin})")
        if len(h_prods) > 5:
            print(f"│  ... and {len(h_prods) - 5} more Top 10 items. Use '--horizon {h_code}' to view full list.")
        print("└" + "─" * 80 + "\n")

def print_horizon(data, horizon_code):
    products = [p for p in data.get("products", []) if p.get("horizon") == horizon_code.lower()]
    if not products:
        print(f"No products found for horizon '{horizon_code}'. Available: 7d, 14d, 30d, 60d, 90d.", file=sys.stderr)
        return
        
    label = products[0].get("horizon_label", horizon_code)
    print("\n" + "=" * 90)
    print(f"  TOP 10 WINNING PRODUCTS: {label.upper()}")
    print("=" * 90)
    print(f"{'Rank':<5} {'SKU ID':<12} {'Category':<22} {'FOB':<8} {'MSRP':<8} {'Margin':<8} {'DVI':<6} {'Product Name'}")
    print("-" * 90)
    
    for idx, p in enumerate(products, 1):
        eco = p.get("economics", {})
        fob = f"${eco.get('fob_usd', 0):.2f}"
        msrp = f"${eco.get('dtc_retail_usd', 0):.2f}"
        margin = eco.get('margin_multiplier', 'N/A')
        dvi = f"{p.get('dvi_score', 0):.1f}"
        cat = p.get("category", "")[:20]
        name = p.get("sku_name", "")[:35]
        print(f"#{idx:<4} {p.get('id'):<12} {cat:<22} {fob:<8} {msrp:<8} {margin:<8} {dvi:<6} {name}")
        print(f"      中文名: {p.get('chinese_name')}")
        print(f"      3秒勾子: {p.get('ad_creative_hook')[:75]}...")
        print()

def inspect_sku(data, sku_id):
    products = data.get("products", [])
    matched = [p for p in products if p.get("id").lower() == sku_id.lower() or sku_id.lower() in p.get("sku_name", "").lower()]
    
    if not matched:
        print(f"No SKU found matching '{sku_id}'", file=sys.stderr)
        return
        
    for p in matched:
        print("\n" + "#" * 85)
        print(f"SKU ID: {p.get('id')} - {p.get('sku_name')}")
        print(f"中文品名: {p.get('chinese_name')}")
        print(f"Category : {p.get('category')} | Horizon: {p.get('horizon_label')}")
        print(f"DVI Score: {p.get('dvi_score')} / 100 ({p.get('tier')})")
        print("#" * 85)
        
        print("\n[1] Platform Cross-Convergence Signals:")
        for plat, sig in p.get("platform_signals", {}).items():
            print(f"  • {plat.replace('_', ' ').title():<16}: {sig}")
            
        print("\n[2] Unit Economics & DTC Margins:")
        eco = p.get("economics", {})
        print(f"  • Factory FOB Cost: ${eco.get('fob_usd', 0):.2f} USD")
        print(f"  • Target DTC MSRP : ${eco.get('dtc_retail_usd', 0):.2f} USD")
        print(f"  • Margin Multiple : {eco.get('margin_multiplier')} (Break-even ROAS: {eco.get('breakeven_roas')})")
        print(f"  • Winning Bundle  : {eco.get('recommended_bundle')}")
        
        print("\n[3] Logistics & Shipping Feasibility:")
        log = p.get("logistics", {})
        print(f"  • Unit Weight     : {log.get('weight_grams')} grams")
        print(f"  • Packaging Size  : {log.get('box_cm')} cm")
        print(f"  • Logistics Mode  : {log.get('shipping_mode')}")
        
        print("\n[4] TikTok / Meta Video Ad Hook (First 3 Seconds):")
        print(f"  🎬 \"{p.get('ad_creative_hook')}\"")
        
        print("\n[5] Target Audience & Positioning:")
        print(f"  🎯 {p.get('target_audience')}")
        print()

def print_category(data, category_query):
    products = data.get("products", [])
    matched = [p for p in products if category_query.lower() in p.get("category", "").lower()]
    
    if not matched:
        print(f"No products found matching category '{category_query}'.", file=sys.stderr)
        return
        
    print("\n" + "=" * 85)
    print(f"  PRODUCTS MATCHING CATEGORY: '{category_query}' ({len(matched)} SKUs)")
    print("=" * 85)
    for p in matched:
        eco = p.get("economics", {})
        print(f"• [{p.get('horizon').upper()}] {p.get('id')} - {p.get('sku_name')}")
        print(f"  中文: {p.get('chinese_name')} | FOB: ${eco.get('fob_usd'):.2f} -> MSRP: ${eco.get('dtc_retail_usd'):.2f} ({eco.get('margin_multiplier')}) | DVI: {p.get('dvi_score')}")
    print()

def export_brief(data, horizon_code=None):
    products = data.get("products", [])
    if horizon_code:
        products = [p for p in products if p.get("horizon") == horizon_code.lower()]
        title_suffix = f"({horizon_code.upper()} Forecast Window)"
    else:
        title_suffix = "(All 5 Horizons Full Radar)"
        
    output_lines = [
        f"# DTC E-Commerce Product Intelligence Brief {title_suffix}",
        f"> Generated on 2026-10-03 | cnproduct (贸启航 / Product Radar)\n",
        "| ID | Horizon | Category | Product Name | FOB ($) | MSRP ($) | Margin | DVI Score |",
        "|---|---|---|---|---|---|---|---|"
    ]
    
    for p in products:
        eco = p.get("economics", {})
        output_lines.append(
            f"| **{p.get('id')}** | {p.get('horizon').upper()} | {p.get('category')} | {p.get('sku_name')} | ${eco.get('fob_usd'):.2f} | ${eco.get('dtc_retail_usd'):.2f} | {eco.get('margin_multiplier')} | {p.get('dvi_score')} |"
        )
        
    brief_md = "\n".join(output_lines)
    output_path = BASE_DIR / "reports" / f"exported-brief-{horizon_code or 'all'}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(brief_md)
    print(f"\n✓ Successfully exported brief to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="DTC Cross-Border Product Intelligence CLI")
    parser.add_argument("--overview", action="store_true", help="Display overview across all 5 forecast horizons")
    parser.add_argument("--horizon", type=str, choices=["7d", "14d", "30d", "60d", "90d"], help="Display Top 10 products for a specific time horizon")
    parser.add_argument("--sku", type=str, help="Inspect detailed economics, video hook, and signals for a SKU ID")
    parser.add_argument("--category", type=str, help="Filter products by category name (e.g. Home, Beauty, Electronics, Apparel, Pet, Sports)")
    parser.add_argument("--export-brief", action="store_true", help="Export filtered selection to a markdown brief report")
    
    args = parser.parse_args()
    data = load_json(DATA_PATH)
    
    if args.sku:
        inspect_sku(data, args.sku)
    elif args.horizon:
        print_horizon(data, args.horizon)
        if args.export_brief:
            export_brief(data, args.horizon)
    elif args.category:
        print_category(data, args.category)
    elif args.export_brief:
        export_brief(data)
    else:
        print_overview(data)

if __name__ == "__main__":
    main()
