#!/usr/bin/env python3
"""
🎯 Combined Trading Signals
Combines influencer recommendations with social media sentiment for stronger signals
"""

from influencers_feed import InfluencersFeed
from social_sentiment_analyzer import SocialSentimentAnalyzer
from datetime import datetime
import json
import time

class CombinedSignals:
    """Combines multiple data sources for trading signals"""

    def __init__(self):
        self.influencers = InfluencersFeed()
        self.sentiment_analyzer = SocialSentimentAnalyzer()

    def analyze_stock(self, symbol):
        """
        Deep analysis of a single stock combining all sources
        """
        print()
        print("=" * 70)
        print(f"🎯 COMBINED ANALYSIS: ${symbol}")
        print("=" * 70)
        print()

        results = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'influencer_signal': None,
            'social_sentiment': None,
            'combined_signal': None,
            'confidence': 0,
            'reasoning': []
        }

        # 1. Get social sentiment
        print("📊 Step 1/2: Analyzing social media sentiment...")
        sentiment_data = self.sentiment_analyzer.get_comprehensive_sentiment(symbol)
        results['social_sentiment'] = sentiment_data

        # 2. Check if influencers mentioned this stock
        print()
        print("👥 Step 2/2: Checking influencer recommendations...")

        # For now, we'll use a simple check (you can extend this to call the feed)
        # In real implementation, you'd call aggregate_feed() and filter for this symbol

        results['influencer_signal'] = self._check_influencer_mentions(symbol)

        # 3. Combine signals
        results['combined_signal'], results['confidence'], results['reasoning'] = \
            self._calculate_combined_signal(results)

        return results

    def _check_influencer_mentions(self, symbol):
        """
        Check if influencers mentioned this stock recently
        Note: This is a placeholder. In production, you'd cache the feed
        """
        return {
            'mentioned': False,
            'buy_count': 0,
            'sell_count': 0,
            'influencers': []
        }

    def _calculate_combined_signal(self, results):
        """
        Calculate combined signal based on all data sources
        """
        signal = 'NEUTRAL'
        confidence = 0
        reasoning = []

        sentiment = results['social_sentiment']
        influencer = results['influencer_signal']

        # Social sentiment analysis
        if sentiment['sentiment_score'] > 0.4:
            reasoning.append(f"🟢 Strong positive social sentiment ({sentiment['sentiment_score']:.2f})")
            confidence += 30
        elif sentiment['sentiment_score'] > 0.2:
            reasoning.append(f"🟡 Moderate positive social sentiment ({sentiment['sentiment_score']:.2f})")
            confidence += 15
        elif sentiment['sentiment_score'] < -0.4:
            reasoning.append(f"🔴 Strong negative social sentiment ({sentiment['sentiment_score']:.2f})")
            confidence += 30
        elif sentiment['sentiment_score'] < -0.2:
            reasoning.append(f"🟡 Moderate negative social sentiment ({sentiment['sentiment_score']:.2f})")
            confidence += 15

        # Trending analysis
        if sentiment['total_mentions'] > 200:
            reasoning.append(f"🔥 Viral stock: {sentiment['total_mentions']} mentions")
            confidence += 25
        elif sentiment['total_mentions'] > 100:
            reasoning.append(f"📈 High attention: {sentiment['total_mentions']} mentions")
            confidence += 15
        elif sentiment['total_mentions'] > 50:
            reasoning.append(f"👀 Moderate attention: {sentiment['total_mentions']} mentions")
            confidence += 10
        else:
            reasoning.append(f"😐 Low attention: {sentiment['total_mentions']} mentions")

        # Influencer recommendations
        if influencer['mentioned']:
            if influencer['buy_count'] > influencer['sell_count']:
                reasoning.append(f"👥 {influencer['buy_count']} influencers recommend BUY")
                confidence += 20
            elif influencer['sell_count'] > influencer['buy_count']:
                reasoning.append(f"👥 {influencer['sell_count']} influencers recommend SELL")
                confidence += 20

        # Determine final signal
        if sentiment['sentiment_score'] > 0.3 and sentiment['total_mentions'] > 50:
            signal = 'STRONG BUY'
            confidence = min(confidence, 95)  # Cap at 95%
        elif sentiment['sentiment_score'] > 0.15:
            signal = 'BUY'
            confidence = min(confidence, 75)
        elif sentiment['sentiment_score'] < -0.3 and sentiment['total_mentions'] > 50:
            signal = 'STRONG SELL'
            confidence = min(confidence, 95)
        elif sentiment['sentiment_score'] < -0.15:
            signal = 'SELL'
            confidence = min(confidence, 75)
        else:
            signal = 'HOLD'
            confidence = min(confidence, 50)

        return signal, confidence, reasoning

    def scan_watchlist(self, watchlist):
        """
        Scan multiple stocks and rank by signal strength
        """
        print()
        print("=" * 70)
        print("🎯 COMBINED SIGNALS - WATCHLIST SCAN")
        print("=" * 70)
        print()

        results = []

        for i, symbol in enumerate(watchlist, 1):
            print(f"[{i}/{len(watchlist)}] Analyzing ${symbol}...")

            try:
                analysis = self.analyze_stock(symbol)
                results.append(analysis)

                # Rate limiting
                if i < len(watchlist):
                    time.sleep(3)

            except Exception as e:
                print(f"   ❌ Error analyzing {symbol}: {e}")
                continue

        # Sort by confidence
        results.sort(key=lambda x: x['confidence'], reverse=True)

        return results

    def print_report(self, results):
        """
        Print formatted analysis report
        """
        print()
        print("=" * 70)
        print("📊 COMBINED SIGNALS REPORT")
        print("=" * 70)
        print()

        # Categorize signals
        strong_buy = [r for r in results if r['combined_signal'] == 'STRONG BUY']
        buy = [r for r in results if r['combined_signal'] == 'BUY']
        strong_sell = [r for r in results if r['combined_signal'] == 'STRONG SELL']
        sell = [r for r in results if r['combined_signal'] == 'SELL']
        hold = [r for r in results if r['combined_signal'] == 'HOLD']

        # Print strong signals first
        if strong_buy:
            print("🚀 STRONG BUY SIGNALS:")
            print("-" * 70)
            for r in strong_buy:
                self._print_stock_summary(r)

        if buy:
            print()
            print("📈 BUY SIGNALS:")
            print("-" * 70)
            for r in buy:
                self._print_stock_summary(r)

        if strong_sell:
            print()
            print("💀 STRONG SELL SIGNALS:")
            print("-" * 70)
            for r in strong_sell:
                self._print_stock_summary(r)

        if sell:
            print()
            print("📉 SELL SIGNALS:")
            print("-" * 70)
            for r in sell:
                self._print_stock_summary(r)

        if hold:
            print()
            print("😐 HOLD / NEUTRAL:")
            print("-" * 70)
            for r in hold[:5]:  # Show only top 5 holds
                self._print_stock_summary(r)

        print()
        print("=" * 70)

    def _print_stock_summary(self, result):
        """
        Print summary for a single stock
        """
        sentiment = result['social_sentiment']

        print(f"\n💰 ${result['symbol']}")
        print(f"   Signal: {result['combined_signal']} (Confidence: {result['confidence']}%)")
        print(f"   Sentiment: {sentiment['sentiment_score']:.2f} | Mentions: {sentiment['total_mentions']}")

        print(f"   Reasoning:")
        for reason in result['reasoning']:
            print(f"      • {reason}")


def main():
    """
    Main function - analyze watchlist with combined signals
    """
    print("🎯 Combined Trading Signals")
    print("Analyzing stocks using social sentiment + influencer recommendations")
    print()

    # Watchlist to analyze
    WATCHLIST = [
        'TSLA',   # Tesla
        'NVDA',   # Nvidia
        'AAPL',   # Apple
        'AMD',    # AMD
        'MSFT',   # Microsoft
        'GOOGL',  # Google
        'META',   # Meta
        'AMZN',   # Amazon
    ]

    analyzer = CombinedSignals()

    # Scan watchlist
    results = analyzer.scan_watchlist(WATCHLIST)

    # Print report
    analyzer.print_report(results)

    # Save to JSON
    output_file = f"combined_signals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'generated_at': datetime.now().isoformat(),
            'watchlist': WATCHLIST,
            'results': results
        }, f, indent=2, ensure_ascii=False, default=str)

    print(f"💾 Results saved to: {output_file}")


if __name__ == "__main__":
    main()
