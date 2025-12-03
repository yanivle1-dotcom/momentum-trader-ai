#!/usr/bin/env python3
"""
📊 Daily Social Sentiment Scanner
Scans watchlist of stocks and identifies hot ones based on social media buzz
"""

from social_sentiment_analyzer import SocialSentimentAnalyzer
import json
from datetime import datetime
import time

# רשימת מניות לסריקה - ערוך לפי צרכים
WATCHLIST = [
    'TSLA',  # Tesla
    'NVDA',  # Nvidia
    'AAPL',  # Apple
    'AMD',   # AMD
    'PLTR',  # Palantir
    'GME',   # GameStop
    'AMC',   # AMC Entertainment
    'MSFT',  # Microsoft
    'GOOGL', # Google
    'META',  # Meta/Facebook
    'AMZN',  # Amazon
    'NFLX',  # Netflix
]

def main():
    analyzer = SocialSentimentAnalyzer()
    hot_stocks = []

    print("=" * 70)
    print("🔍 DAILY SENTIMENT SCAN STARTING")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Scanning {len(WATCHLIST)} stocks...")
    print("=" * 70)
    print()

    for i, symbol in enumerate(WATCHLIST, 1):
        try:
            print(f"[{i}/{len(WATCHLIST)}] Analyzing {symbol}...")
            results = analyzer.get_comprehensive_sentiment(symbol)

            # שמור רק מניות עם מספר משמעותי של אזכורים
            if results['total_mentions'] >= 10:  # סף מינימלי
                hot_stocks.append({
                    'symbol': symbol,
                    'sentiment': results['sentiment_score'],
                    'sentiment_label': results['overall_sentiment'],
                    'mentions': results['total_mentions'],
                    'trending': results['trending_score'],
                    'platforms': {
                        'reddit': results['platforms'].get('reddit', {}).get('mentions', 0),
                        'stocktwits': results['platforms'].get('stocktwits', {}).get('total_messages', 0),
                        'twitter': results['platforms'].get('twitter', {}).get('mentions', 0),
                    }
                })

            # המתן בין בקשות (rate limiting)
            if i < len(WATCHLIST):
                time.sleep(3)

        except Exception as e:
            print(f"❌ Error analyzing {symbol}: {e}")
            continue

    # מיין לפי trending score
    hot_stocks.sort(key=lambda x: x['trending'], reverse=True)

    # הצג תוצאות
    print()
    print("=" * 70)
    print("🔥 HOT STOCKS - TOP MENTIONS")
    print("=" * 70)

    if not hot_stocks:
        print("⚠️  No stocks with significant mentions found")
    else:
        for i, stock in enumerate(hot_stocks[:10], 1):  # Top 10
            emoji = "🚀" if stock['sentiment'] > 0.3 else "📉" if stock['sentiment'] < -0.3 else "😐"
            print(f"{i:2}. {emoji} ${stock['symbol']:6} | {stock['mentions']:4} mentions | "
                  f"Sentiment: {stock['sentiment']:+.2f} ({stock['sentiment_label'].upper()})")
            print(f"      Reddit: {stock['platforms']['reddit']} | "
                  f"StockTwits: {stock['platforms']['stocktwits']} | "
                  f"Twitter: {stock['platforms']['twitter']}")

        # הצג סיגנלים חזקים
        print()
        print("=" * 70)
        print("🎯 STRONG SIGNALS")
        print("=" * 70)

        strong_buy = [s for s in hot_stocks if s['sentiment'] > 0.4 and s['mentions'] > 50]
        strong_sell = [s for s in hot_stocks if s['sentiment'] < -0.4 and s['mentions'] > 50]
        viral = [s for s in hot_stocks if s['mentions'] > 200]

        if strong_buy:
            print("\n📈 STRONG BUY SIGNALS:")
            for stock in strong_buy[:5]:
                print(f"   🟢 ${stock['symbol']}: {stock['mentions']} mentions, "
                      f"sentiment {stock['sentiment']:+.2f}")

        if strong_sell:
            print("\n📉 STRONG SELL SIGNALS:")
            for stock in strong_sell[:5]:
                print(f"   🔴 ${stock['symbol']}: {stock['mentions']} mentions, "
                      f"sentiment {stock['sentiment']:+.2f}")

        if viral:
            print("\n🚨 VIRAL STOCKS (HIGH VOLUME):")
            for stock in viral:
                print(f"   ⚡ ${stock['symbol']}: {stock['mentions']} mentions!")

        if not any([strong_buy, strong_sell, viral]):
            print("   😐 No strong signals today")

    # שמור לקובץ JSON
    output = {
        'date': datetime.now().isoformat(),
        'total_scanned': len(WATCHLIST),
        'stocks_with_mentions': len(hot_stocks),
        'hot_stocks': hot_stocks
    }

    output_file = f"daily_sentiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print()
    print("=" * 70)
    print(f"💾 Results saved to: {output_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()
