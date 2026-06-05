#!/usr/bin/env python3
"""ViralTube Affiliate Link Tracker"""
import json
import os
from datetime import datetime

AFFILIATE_PRODUCTS = {
    # Finance
    "mint": {"name": "Mint App", "link": "YOUR_AFFILIATE_LINK", "type": "budget"},
    "ynab": {"name": "YNAB", "link": "YOUR_AFFILIATE_LINK", "type": "budget"},
    "wealthfront": {"name": "Wealthfront", "link": "YOUR_AFFILIATE_LINK", "type": "investing"},
    "betterment": {"name": "Betterment", "link": "YOUR_AFFILIATE_LINK", "type": "investing"},
    "acorns": {"name": "Acorns", "link": "YOUR_AFFILIATE_LINK", "type": "investing"},
    "robinhood": {"name": "Robinhood", "link": "YOUR_AFFILIATE_LINK", "type": "trading"},
    "webull": {"name": "Webull", "link": "YOUR_AFFILIATE_LINK", "type": "trading"},
    
    # Books
    "compound effect": {"name": "The Compound Effect", "link": "YOUR_AFFILIATE_LINK", "type": "book"},
    "rich dad poor dad": {"name": "Rich Dad Poor Dad", "link": "YOUR_AFFILIATE_LINK", "type": "book"},
    " psychology of money": {"name": "The Psychology of Money", "link": "YOUR_AFFILIATE_LINK", "type": "book"},
    
    # Tools
    "canva": {"name": "Canva Pro", "link": "YOUR_AFFILIATE_LINK", "type": "design"},
    "notion": {"name": "Notion", "link": "YOUR_AFFILIATE_LINK", "type": "productivity"},
    
    # Crypto
    "ledger": {"name": "Ledger Wallet", "link": "YOUR_AFFILIATE_LINK", "type": "crypto"},
    "coinbase": {"name": "Coinbase", "link": "YOUR_AFFILIATE_LINK", "type": "crypto"},
    
    # Courses
    "masterclass": {"name": "MasterClass", "link": "YOUR_AFFILIATE_LINK", "type": "course"},
    "skillshare": {"name": "Skillshare", "link": "YOUR_AFFILIATE_LINK", "type": "course"},
}

def extract_affiliates(text):
    """Extract mentioned products and find matching affiliates"""
    found = []
    text_lower = text.lower()
    
    for key, product in AFFILIATE_PRODUCTS.items():
        if key in text_lower:
            found.append({
                "product": product["name"],
                "link": product["link"],
                "type": product["type"],
                "mentioned_in": "script"
            })
    
    return found

def save_affiliate_report(affiliates, topic, output_dir=None):
    """Save affiliate report"""
    if not output_dir:
        output_dir = os.path.expanduser("~/Videos/viraltube")
    
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    safe_topic = topic.lower().replace(' ', '-')[:30]
    filename = f"{output_dir}/affiliates-{safe_topic}-{timestamp}.json"
    
    report = {
        "topic": topic,
        "generated": datetime.now().isoformat(),
        "affiliates": affiliates,
        "total_mentions": len(affiliates)
    }
    
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"📋 Affiliate report saved: {filename}")
    return filename

def main():
    import sys
    
    # Get affiliate section text
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = input("Paste AFFILIATE_SECTION text: ")
    
    topic = sys.argv[2] if len(sys.argv) > 2 else "Unknown"
    
    affiliates = extract_affiliates(text)
    
    if affiliates:
        print(f"\n🔗 Found {len(affiliates)} affiliate mentions:\n")
        for i, a in enumerate(affiliates, 1):
            print(f"{i}. {a['product']} ({a['type']})")
            print(f"   Link: {a['link']}")
            print()
    else:
        print("No known affiliate products found.")
        print("\nAdd your links to AFFILIATE_PRODUCTS in this script.")
    
    save_affiliate_report(affiliates, topic)

if __name__ == "__main__":
    main()
