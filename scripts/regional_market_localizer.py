#!/usr/bin/env python3
"""
Regional Market & Local Platform Intelligence Adapter
------------------------------------------------------
Adapts DTC products and ad copy to 5 major localized e-commerce platforms,
regional languages, payment methods, and cultural conversion triggers.

Supported Regional Ecosystems:
  1. LATAM (Latin America): Mercado Libre (MELI) | Spanish (ES-MX) & Portuguese (PT-BR) | PIX & Mercado Pago
  2. MENA (Middle East / GCC): Noon.com & Snapchat Ads | Arabic (AR) | COD & Tabby/Tamara BNPL
  3. SEA (Southeast Asia): Shopee, Lazada & Line Ads | Thai (TH), Vietnamese (VI), Indonesian (ID) | Gratis Ongkir & COD
  4. EUROPE (Local Titans): Allegro (Poland), Otto & Kaufland (DACH) | Polish (PL) & German (DE) | Allegro Smart & CE/TÜV
  5. EAST ASIA: Rakuten (Japan) & Coupang (Korea) | Japanese (JA) & Korean (KO) | Rakuten Points & Rocket Delivery

Usage:
  python3 scripts/regional_market_localizer.py --sku DTC-7D-01 --region all
  python3 scripts/regional_market_localizer.py --product "Ultrasonic Cleaner" --region mena
"""

import sys
import json
import argparse
from pathlib import Path

REGIONAL_PROFILES = {
    "latam": {
        "region_name": "Latin America (Mexico, Brazil, Colombia)",
        "flagship_platforms": ["Mercado Libre (MELI)", "Amazon.com.mx", "Shopee Brasil"],
        "primary_ad_channels": ["Facebook/Instagram Ads", "Mercado Ads", "TikTok Ads LatAm"],
        "languages": ["Spanish (ES-MX)", "Portuguese (PT-BR)"],
        "critical_conversion_triggers": [
            "PIX: Instant payment with extra 5% discount (Crucial in Brazil)",
            "Mercado Pago: Hasta 12 cuotas sin interés (Installments without card)",
            "Envío FULL: Entrega al día siguiente garantizada (Next-day delivery badge)",
            "Garantía de compra protegida por 30 días"
        ],
        "compliance_notes": "NOM certification for electronics in Mexico; Anatel for wireless devices in Brazil."
    },
    "mena": {
        "region_name": "Middle East & GCC (Saudi Arabia, UAE, Kuwait, Qatar)",
        "flagship_platforms": ["Noon.com", "Amazon.sa / Amazon.ae", "Trendyol"],
        "primary_ad_channels": ["Snapchat Ads (Dominant in KSA)", "TikTok Ads", "Instagram Ads"],
        "languages": ["Arabic (العربية - AR)", "English"],
        "critical_conversion_triggers": [
            "الدفع عند الاستلام (Cash on Delivery - COD with zero friction)",
            "تابي وتمارا (Tabby & Tamara: Split into 4 interest-free payments)",
            "توصيل سريع مجاني خلال 24-48 ساعة (Express 24-48h Delivery)",
            "ضمان استبدال فوري لمدة سنتين (2-Year Replacement Warranty)"
        ],
        "compliance_notes": "SASO / Saber registration in Saudi Arabia; ECAS in UAE; Halal sensitivity on cosmetics."
    },
    "sea": {
        "region_name": "Southeast Asia (Indonesia, Thailand, Vietnam, Philippines, Malaysia)",
        "flagship_platforms": ["Shopee", "Lazada", "TikTok Shop SEA", "Tokopedia"],
        "primary_ad_channels": ["TikTok Shop Spark Ads", "Facebook Ads", "Line Ads (Thailand/Taiwan)", "Zalo (Vietnam)"],
        "languages": ["Bahasa Indonesia (ID)", "Thai (TH)", "Vietnamese (VI)"],
        "critical_conversion_triggers": [
            "Gratis Ongkir / Free Shipping Vouchers (Voucher Gratis Ongkir Xtra)",
            "COD (Bayar di Tempat / Cash on Delivery)",
            "Mega Campaign Bundles (8.8, 9.9, 11.11 Double-Digit Sales vouchers)",
            "Tahan Lama & Anti Air (Emphasis on durability under humid tropical weather)"
        ],
        "compliance_notes": "BPOM for food/cosmetics in Indonesia; TISI in Thailand; FDA Philippines."
    },
    "europe_local": {
        "region_name": "Europe Local Strongholds (Poland, Germany, France, Benelux)",
        "flagship_platforms": ["Allegro (Poland & CEE)", "Otto & Kaufland (Germany)", "Bol.com (Netherlands/Belgium)", "Cdiscount (France)"],
        "primary_ad_channels": ["Google Ads PMax", "Allegro Ads", "Meta Ads", "Pinterest Ads"],
        "languages": ["Polish (PL)", "German (DE)", "French (FR)", "Dutch (NL)"],
        "critical_conversion_triggers": [
            "Allegro Smart! (Free courier & parcel locker delivery in Poland)",
            "TÜV Rheinland / GS Geprüfte Sicherheit & CE Mark (Non-negotiable trust in Germany)",
            "Kauf auf Rechnung (Invoice purchase via Klarna / Ratepay)",
            "Indice de Réparabilité & Triman logo (Mandatory eco-repair score in France)"
        ],
        "compliance_notes": "LUCID EPR in Germany; Triman sorting in France; CE / WEEE / RoHS compliance."
    },
    "east_asia": {
        "region_name": "East Asia (Japan & South Korea)",
        "flagship_platforms": ["Rakuten Ichiba (Japan)", "Yahoo! Shopping", "Coupang (Korea)", "Naver Smartstore"],
        "primary_ad_channels": ["Line Ads (Japan)", "Kakao Ads & KakaoTalk Channel (Korea)", "Google Search Japan"],
        "languages": ["Japanese (日本語 - JA)", "Korean (한국어 - KO)"],
        "critical_conversion_triggers": [
            "Rakuten Super Points Multiplier (楽天ポイント5倍・お買い物マラソン)",
            "Coupang Wow Rocket Delivery (로켓배송 - 새벽도착 Next-morning dawn delivery)",
            "0.1mm Precision Manufacturing Guarantee (微米级严谨做工与1年国内质保)",
            "Japanese Polite Business Keigo Copy (安心・安全の国内サポート体制)"
        ],
        "compliance_notes": "PSE certification for electrical appliances in Japan; KC certification in South Korea."
    }
}

def localize_product(product_name: str, brand: str = "Store", price_usd: float = 39.99, region_filter: str = "all"):
    results = {}
    regions_to_process = REGIONAL_PROFILES.keys() if region_filter == "all" else [region_filter.lower()]

    for reg_key in regions_to_process:
        if reg_key not in REGIONAL_PROFILES:
            continue
        profile = REGIONAL_PROFILES[reg_key]
        
        # Local currency approximations
        price_map = {
            "latam": f"${price_usd * 18:.0f} MXN / R$ {price_usd * 5.5:.2f} BRL",
            "mena": f"{price_usd * 3.75:.0f} SAR / {price_usd * 3.67:.0f} AED",
            "sea": f"Rp {price_usd * 16000:,.0f} IDR / ฿{price_usd * 36:.0f} THB",
            "europe_local": f"€{price_usd * 0.92:.2f} EUR / {price_usd * 4.1:.0f} PLN",
            "east_asia": f"¥{price_usd * 155:,.0f} JPY / ₩{price_usd * 1350:,.0f} KRW"
        }

        # Localized ad copy hooks
        hooks = {
            "latam": [
                f"¡Oferta exclusiva para México y Brasil! {product_name} con envío FULL gratis.",
                f"Paga con PIX y obtén 5% de descuento adicional. ¡Meses sin intereses disponibles!"
            ],
            "mena": [
                f"العرض الأقوى في السعودية والإمارات! {product_name} الأصلي مع الدفع عند الاستلام.",
                f"قسّم مشترياتك على 4 دفعات مريحة وبدون أي فوائد مع تابي وتمارا. اطلب الآن!"
            ],
            "sea": [
                f"🔥 PROMO TERBESAR! {product_name} ready stock dengan Voucher Gratis Ongkir Xtra + Bisa COD.",
                f"Flash Sale 8.8! Beli sekarang dan dapatkan diskon 50% hanya di Shopee/TikTok Shop."
            ],
            "europe_local": [
                f"Top-Angebot in Deutschland: {product_name} mit CE/TÜV Prüfung und Rechnungskauf.",
                f"Kup teraz na Allegro ze Smart! Darmowa dostawa do Paczkomatu w 24h."
            ],
            "east_asia": [
                f"【日本国内発送・1年保証】大人気 {product_name} が楽天ポイント5倍キャンペーン中！",
                f"쿠팡 로켓배송 오늘 주문 내일 아침 도착! {product_name} 특가 세일 진행 중."
            ]
        }

        results[reg_key] = {
            "profile": profile,
            "estimated_local_pricing": price_map.get(reg_key, f"${price_usd:.2f} USD"),
            "localized_ad_hooks": hooks.get(reg_key, []),
            "conversion_triggers": profile["critical_conversion_triggers"]
        }

    return {
        "product_name": product_name,
        "brand": brand,
        "usd_price": price_usd,
        "regions": results
    }

def print_localization_report(res: dict):
    print("\n" + "="*80)
    print(f"🌍 MULTI-REGION & LOCAL PLATFORM DOSSIER: {res['product_name']}")
    print(f"💰 Baseline USD: ${res['usd_price']:.2f}")
    print("="*80)

    for reg_key, data in res["regions"].items():
        prof = data["profile"]
        print(f"\n🗺️  【{prof['region_name'].upper()}】")
        print(f"  🏢 Flagship Platforms:  {', '.join(prof['flagship_platforms'])}")
        print(f"  📢 Core Ad Channels:    {', '.join(prof['primary_ad_channels'])}")
        print(f"  💵 Localized Pricing:   {data['estimated_local_pricing']}")
        print(f"  🗣️  Languages:           {', '.join(prof['languages'])}")
        print(f"  📋 Compliance / Certs:  {prof['compliance_notes']}")
        print("  🔑 Essential Local Conversion Triggers:")
        for t in data["conversion_triggers"]:
            print(f"     • {t}")
        print("  ✍️  Localized Native Ad Hooks:")
        for h in data["localized_ad_hooks"]:
            print(f"     💬 \"{h}\"")
        print("-" * 80)
    print("="*80 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Regional Market & Local Platform Intelligence Adapter")
    parser.add_argument("--product", help="Product name")
    parser.add_argument("--brand", default="Store", help="Brand name")
    parser.add_argument("--price", type=float, default=39.99, help="USD price")
    parser.add_argument("--region", default="all", choices=["all", "latam", "mena", "sea", "europe_local", "east_asia"], help="Target region")
    parser.add_argument("--sku", help="Lookup SKU from data/trending-dtc-radar.json")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    prod_name = args.product or "Ultrasonic Cleaner"
    brand_name = args.brand
    price_val = args.price

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
                        price_val = item.get("dtc_target_retail", 39.99)
                        found = True
                        break
                if found:
                    break

    res = localize_product(prod_name, brand=brand_name, price_usd=price_val, region_filter=args.region)
    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print_localization_report(res)
