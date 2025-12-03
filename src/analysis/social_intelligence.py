"""
Social Intelligence Module
Integrates social sentiment and influencer recommendations into trading system
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

# Add parent directory to path to import our modules
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parent_dir)

from social_sentiment_analyzer import SocialSentimentAnalyzer
from influencers_feed import InfluencersFeed


class SocialIntelligence:
    """
    Combines social sentiment and influencer recommendations
    Provides trading signals based on social media intelligence
    """

    def __init__(self):
        self.sentiment_analyzer = SocialSentimentAnalyzer()
        self.influencers_feed = InfluencersFeed()
        self.cache = {}  # Cache recent analyses

    def analyze_stock(self, symbol: str, use_cache: bool = True) -> Dict:
        """
        Complete social intelligence analysis for a stock

        Args:
            symbol: Stock ticker symbol
            use_cache: Use cached data if available (within 1 hour)

        Returns:
            Dictionary with analysis results
        """
        # Check cache
        if use_cache and symbol in self.cache:
            cache_age = (datetime.now() - self.cache[symbol]['timestamp']).seconds
            if cache_age < 3600:  # 1 hour
                return self.cache[symbol]['data']

        print(f"🔍 Analyzing social intelligence for ${symbol}...")

        # Get social sentiment
        sentiment_data = self.sentiment_analyzer.get_comprehensive_sentiment(symbol)

        # Calculate social signal
        signal, confidence, reasoning = self._calculate_signal(
            sentiment_data,
            None  # Influencer data would go here if we had it cached
        )

        result = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'sentiment': {
                'score': sentiment_data['sentiment_score'],
                'label': sentiment_data['overall_sentiment'],
                'mentions': sentiment_data['total_mentions'],
                'trending_score': sentiment_data['trending_score'],
                'platforms': sentiment_data['platforms']
            },
            'signal': signal,
            'confidence': confidence,
            'reasoning': reasoning,
            'recommendation': self._get_recommendation(signal, confidence)
        }

        # Cache result
        self.cache[symbol] = {
            'timestamp': datetime.now(),
            'data': result
        }

        return result

    def _calculate_signal(self, sentiment_data: Dict, influencer_data: Optional[Dict]) -> tuple:
        """
        Calculate trading signal based on social intelligence

        Returns:
            (signal, confidence, reasoning) tuple
        """
        signal = 'NEUTRAL'
        confidence = 0
        reasoning = []

        sentiment_score = sentiment_data['sentiment_score']
        mentions = sentiment_data['total_mentions']

        # Sentiment analysis
        if sentiment_score > 0.5:
            reasoning.append(f"🟢 Very strong positive sentiment ({sentiment_score:.2f})")
            confidence += 35
        elif sentiment_score > 0.3:
            reasoning.append(f"🟢 Strong positive sentiment ({sentiment_score:.2f})")
            confidence += 25
        elif sentiment_score > 0.15:
            reasoning.append(f"🟡 Moderate positive sentiment ({sentiment_score:.2f})")
            confidence += 15
        elif sentiment_score < -0.5:
            reasoning.append(f"🔴 Very strong negative sentiment ({sentiment_score:.2f})")
            confidence += 35
        elif sentiment_score < -0.3:
            reasoning.append(f"🔴 Strong negative sentiment ({sentiment_score:.2f})")
            confidence += 25
        elif sentiment_score < -0.15:
            reasoning.append(f"🟡 Moderate negative sentiment ({sentiment_score:.2f})")
            confidence += 15

        # Volume analysis
        if mentions > 500:
            reasoning.append(f"🔥 Viral: {mentions} mentions")
            confidence += 30
        elif mentions > 200:
            reasoning.append(f"📈 Very high attention: {mentions} mentions")
            confidence += 20
        elif mentions > 100:
            reasoning.append(f"📈 High attention: {mentions} mentions")
            confidence += 15
        elif mentions > 50:
            reasoning.append(f"👀 Moderate attention: {mentions} mentions")
            confidence += 10
        elif mentions > 20:
            reasoning.append(f"👀 Some attention: {mentions} mentions")
            confidence += 5
        else:
            reasoning.append(f"😐 Low attention: {mentions} mentions")

        # Platform breakdown
        platforms = sentiment_data.get('platforms', {})
        if 'reddit' in platforms and platforms['reddit'].get('mentions', 0) > 50:
            reasoning.append(f"📱 Strong Reddit presence: {platforms['reddit']['mentions']} posts")
            confidence += 5

        if 'stocktwits' in platforms and platforms['stocktwits'].get('total_messages', 0) > 30:
            bullish = platforms['stocktwits'].get('bullish_count', 0)
            bearish = platforms['stocktwits'].get('bearish_count', 0)
            if bullish > bearish * 2:
                reasoning.append(f"💬 StockTwits very bullish: {bullish} vs {bearish}")
                confidence += 5

        # Determine signal
        if sentiment_score > 0.4 and mentions > 100:
            signal = 'STRONG_BUY'
        elif sentiment_score > 0.3 and mentions > 50:
            signal = 'BUY'
        elif sentiment_score > 0.15:
            signal = 'WEAK_BUY'
        elif sentiment_score < -0.4 and mentions > 100:
            signal = 'STRONG_SELL'
        elif sentiment_score < -0.3 and mentions > 50:
            signal = 'SELL'
        elif sentiment_score < -0.15:
            signal = 'WEAK_SELL'
        else:
            signal = 'NEUTRAL'

        # Cap confidence
        confidence = min(confidence, 95)

        return signal, confidence, reasoning

    def _get_recommendation(self, signal: str, confidence: int) -> str:
        """
        Get human-readable recommendation
        """
        recommendations = {
            'STRONG_BUY': f"✅ Strong Buy Signal ({confidence}% confidence)\n   Consider entering position. High social momentum.",
            'BUY': f"📈 Buy Signal ({confidence}% confidence)\n   Positive sentiment, consider buying.",
            'WEAK_BUY': f"🟢 Weak Buy Signal ({confidence}% confidence)\n   Slightly positive, wait for confirmation.",
            'NEUTRAL': f"😐 Neutral ({confidence}% confidence)\n   No clear social signal. Wait for better setup.",
            'WEAK_SELL': f"🟡 Weak Sell Signal ({confidence}% confidence)\n   Slightly negative, monitor closely.",
            'SELL': f"📉 Sell Signal ({confidence}% confidence)\n   Negative sentiment, consider exiting.",
            'STRONG_SELL': f"❌ Strong Sell Signal ({confidence}% confidence)\n   Very negative sentiment. Avoid or short."
        }
        return recommendations.get(signal, "No recommendation")

    def scan_watchlist(self, watchlist: List[str]) -> List[Dict]:
        """
        Scan multiple stocks and return sorted by signal strength

        Args:
            watchlist: List of stock symbols

        Returns:
            List of analysis results sorted by confidence
        """
        print(f"\n🔍 Scanning {len(watchlist)} stocks...")

        results = []
        for symbol in watchlist:
            try:
                analysis = self.analyze_stock(symbol)
                results.append(analysis)
            except Exception as e:
                print(f"   ❌ Error analyzing {symbol}: {e}")

        # Sort by confidence (highest first)
        results.sort(key=lambda x: x['confidence'], reverse=True)

        return results

    def get_top_opportunities(self, watchlist: List[str], min_confidence: int = 60) -> List[Dict]:
        """
        Get top trading opportunities from watchlist

        Args:
            watchlist: List of stock symbols
            min_confidence: Minimum confidence threshold

        Returns:
            List of opportunities (STRONG_BUY or BUY signals)
        """
        results = self.scan_watchlist(watchlist)

        opportunities = [
            r for r in results
            if r['signal'] in ['STRONG_BUY', 'BUY'] and r['confidence'] >= min_confidence
        ]

        return opportunities

    def get_risk_alerts(self, positions: List[str], min_confidence: int = 60) -> List[Dict]:
        """
        Check current positions for negative social sentiment

        Args:
            positions: List of stock symbols you currently hold
            min_confidence: Minimum confidence for alert

        Returns:
            List of positions with negative sentiment
        """
        results = self.scan_watchlist(positions)

        alerts = [
            r for r in results
            if r['signal'] in ['STRONG_SELL', 'SELL', 'WEAK_SELL'] and r['confidence'] >= min_confidence
        ]

        return alerts

    def get_summary_text(self, analysis: Dict) -> str:
        """
        Get formatted text summary of analysis

        Args:
            analysis: Analysis result dictionary

        Returns:
            Formatted text summary
        """
        lines = [
            f"📊 Social Intelligence: ${analysis['symbol']}",
            f"{'='*60}",
            f"",
            f"Signal: {analysis['signal']} ({analysis['confidence']}% confidence)",
            f"",
            f"Sentiment Score: {analysis['sentiment']['score']:.2f} ({analysis['sentiment']['label'].upper()})",
            f"Total Mentions: {analysis['sentiment']['mentions']}",
            f"Trending Score: {analysis['sentiment']['trending_score']}",
            f"",
            f"Reasoning:",
        ]

        for reason in analysis['reasoning']:
            lines.append(f"  • {reason}")

        lines.append(f"")
        lines.append(f"Recommendation:")
        lines.append(f"{analysis['recommendation']}")
        lines.append(f"")
        lines.append(f"{'='*60}")

        return "\n".join(lines)


def main():
    """
    Test the social intelligence module
    """
    print("🧠 Social Intelligence Module - Test")
    print("="*70)

    social_intel = SocialIntelligence()

    # Test single stock
    print("\n1. Single Stock Analysis:")
    analysis = social_intel.analyze_stock('TSLA')
    print(social_intel.get_summary_text(analysis))

    # Test watchlist scan
    print("\n2. Watchlist Scan:")
    watchlist = ['NVDA', 'AAPL', 'AMD', 'MSFT', 'GOOGL']
    results = social_intel.scan_watchlist(watchlist)

    print(f"\n📊 Top 3 Signals:")
    for i, result in enumerate(results[:3], 1):
        print(f"\n{i}. ${result['symbol']}: {result['signal']} ({result['confidence']}%)")
        print(f"   Sentiment: {result['sentiment']['score']:.2f} | Mentions: {result['sentiment']['mentions']}")

    # Test opportunities
    print("\n3. Trading Opportunities:")
    opportunities = social_intel.get_top_opportunities(watchlist, min_confidence=50)

    if opportunities:
        print(f"\n✅ Found {len(opportunities)} opportunities:")
        for opp in opportunities:
            print(f"   • ${opp['symbol']}: {opp['signal']} ({opp['confidence']}% confidence)")
    else:
        print("\n😐 No strong opportunities found")


if __name__ == "__main__":
    main()
