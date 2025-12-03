#!/usr/bin/env python3
"""
📱 Social Media Sentiment Analyzer for Stocks
Collects and analyzes stock mentions from social media platforms
"""

import os
import sys
import requests
import json
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from dotenv import load_dotenv
import time

load_dotenv()

# API Keys (add these to your .env)
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
STOCKTWITS_TOKEN = os.getenv("STOCKTWITS_TOKEN")

class SocialSentimentAnalyzer:
    """Analyzes stock sentiment from multiple social media platforms"""

    def __init__(self):
        self.reddit_token = None
        self.sentiment_scores = {}

    def authenticate_reddit(self):
        """Get Reddit API access token"""
        if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
            print("⚠️  Reddit credentials not found in .env")
            return False

        auth = requests.auth.HTTPBasicAuth(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
        data = {
            'grant_type': 'password',
            'username': 'your_reddit_username',  # Optional: add to .env
            'password': 'your_reddit_password'   # Optional: add to .env
        }
        headers = {'User-Agent': 'StockAnalyzer/1.0'}

        try:
            response = requests.post('https://www.reddit.com/api/v1/access_token',
                                   auth=auth, data=data, headers=headers)
            if response.status_code == 200:
                self.reddit_token = response.json()['access_token']
                return True
        except Exception as e:
            print(f"Reddit auth failed: {e}")
        return False

    def get_reddit_mentions(self, stock_symbol, limit=100):
        """
        Get stock mentions from Reddit (r/wallstreetbets, r/stocks, etc.)
        Returns: list of posts with sentiment data
        """
        print(f"📱 Searching Reddit for ${stock_symbol}...")

        subreddits = [
            'wallstreetbets',
            'stocks',
            'investing',
            'StockMarket',
            'pennystocks',
            'options'
        ]

        mentions = []
        headers = {'User-Agent': 'StockAnalyzer/1.0'}

        for subreddit in subreddits:
            try:
                # Search subreddit for stock symbol
                url = f'https://www.reddit.com/r/{subreddit}/search.json'
                params = {
                    'q': f'${stock_symbol} OR {stock_symbol}',
                    'restrict_sr': 'on',
                    'sort': 'new',
                    'limit': limit,
                    't': 'week'  # Last week
                }

                response = requests.get(url, headers=headers, params=params)

                if response.status_code == 200:
                    data = response.json()
                    posts = data.get('data', {}).get('children', [])

                    for post in posts:
                        post_data = post['data']
                        mentions.append({
                            'platform': 'reddit',
                            'subreddit': subreddit,
                            'title': post_data.get('title', ''),
                            'text': post_data.get('selftext', ''),
                            'score': post_data.get('score', 0),
                            'comments': post_data.get('num_comments', 0),
                            'url': f"https://reddit.com{post_data.get('permalink', '')}",
                            'created': datetime.fromtimestamp(post_data.get('created_utc', 0))
                        })

                time.sleep(2)  # Rate limiting

            except Exception as e:
                print(f"Error fetching from r/{subreddit}: {e}")

        print(f"✅ Found {len(mentions)} Reddit mentions")
        return mentions

    def get_stocktwits_sentiment(self, stock_symbol):
        """
        Get sentiment from StockTwits (Twitter-like platform for stocks)
        """
        print(f"💬 Checking StockTwits for ${stock_symbol}...")

        url = f'https://api.stocktwits.com/api/2/streams/symbol/{stock_symbol}.json'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                messages = data.get('messages', [])

                sentiments = []
                mentions = []

                for msg in messages:
                    sentiment = msg.get('entities', {}).get('sentiment', {})
                    if sentiment:
                        sentiments.append(sentiment.get('basic', 'neutral'))

                    mentions.append({
                        'platform': 'stocktwits',
                        'text': msg.get('body', ''),
                        'user': msg.get('user', {}).get('username', ''),
                        'created': msg.get('created_at', ''),
                        'sentiment': sentiment.get('basic', 'neutral') if sentiment else 'neutral'
                    })

                # Calculate sentiment score
                sentiment_counts = Counter(sentiments)
                bullish = sentiment_counts.get('bullish', 0)
                bearish = sentiment_counts.get('bearish', 0)
                total = len(sentiments) if sentiments else 1

                sentiment_score = (bullish - bearish) / total if total > 0 else 0

                print(f"✅ StockTwits: {len(mentions)} messages")
                print(f"   📊 Sentiment: {bullish} bullish, {bearish} bearish (score: {sentiment_score:.2f})")

                return {
                    'mentions': mentions,
                    'sentiment_score': sentiment_score,
                    'bullish_count': bullish,
                    'bearish_count': bearish,
                    'total_messages': len(mentions)
                }

        except Exception as e:
            print(f"Error fetching StockTwits: {e}")

        return None

    def get_twitter_mentions(self, stock_symbol, max_results=100):
        """
        Get stock mentions from Twitter/X
        Requires Twitter API v2 access
        """
        if not TWITTER_BEARER_TOKEN:
            print("⚠️  Twitter Bearer Token not found")
            return []

        print(f"🐦 Searching Twitter for ${stock_symbol}...")

        url = "https://api.twitter.com/2/tweets/search/recent"
        headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}

        # Search for stock mentions
        query = f"(${stock_symbol} OR #{stock_symbol}) -is:retweet lang:en"
        params = {
            'query': query,
            'max_results': min(max_results, 100),
            'tweet.fields': 'created_at,public_metrics,entities',
        }

        try:
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                tweets = data.get('data', [])

                mentions = []
                for tweet in tweets:
                    mentions.append({
                        'platform': 'twitter',
                        'text': tweet.get('text', ''),
                        'created': tweet.get('created_at', ''),
                        'likes': tweet.get('public_metrics', {}).get('like_count', 0),
                        'retweets': tweet.get('public_metrics', {}).get('retweet_count', 0),
                        'replies': tweet.get('public_metrics', {}).get('reply_count', 0)
                    })

                print(f"✅ Found {len(mentions)} Twitter mentions")
                return mentions
            else:
                print(f"Twitter API error: {response.status_code}")

        except Exception as e:
            print(f"Error fetching Twitter: {e}")

        return []

    def analyze_sentiment(self, text):
        """
        Simple sentiment analysis based on keywords
        Returns: 'bullish', 'bearish', or 'neutral'
        """
        text_lower = text.lower()

        bullish_words = [
            'buy', 'long', 'calls', 'moon', 'rocket', 'bullish', 'pump',
            'breakout', 'rally', 'surge', 'gap up', 'squeeze', 'tendies',
            'yolo', 'diamond hands', 'hold', 'hodl', 'to the moon'
        ]

        bearish_words = [
            'sell', 'short', 'puts', 'crash', 'dump', 'bearish', 'drop',
            'tank', 'fail', 'overvalued', 'bubble', 'red', 'loss', 'bag holder'
        ]

        bullish_count = sum(1 for word in bullish_words if word in text_lower)
        bearish_count = sum(1 for word in bearish_words if word in text_lower)

        if bullish_count > bearish_count:
            return 'bullish'
        elif bearish_count > bullish_count:
            return 'bearish'
        else:
            return 'neutral'

    def get_comprehensive_sentiment(self, stock_symbol):
        """
        Get comprehensive sentiment analysis from all platforms
        """
        print()
        print("=" * 70)
        print(f"📊 SOCIAL SENTIMENT ANALYSIS: ${stock_symbol}")
        print("=" * 70)
        print()

        results = {
            'symbol': stock_symbol,
            'timestamp': datetime.now().isoformat(),
            'platforms': {},
            'overall_sentiment': 'neutral',
            'sentiment_score': 0,
            'total_mentions': 0,
            'trending_score': 0
        }

        # Reddit
        reddit_mentions = self.get_reddit_mentions(stock_symbol)
        if reddit_mentions:
            reddit_sentiments = [self.analyze_sentiment(m['title'] + ' ' + m['text'])
                               for m in reddit_mentions]
            reddit_score = sum(1 if s == 'bullish' else -1 if s == 'bearish' else 0
                             for s in reddit_sentiments)

            results['platforms']['reddit'] = {
                'mentions': len(reddit_mentions),
                'sentiment_score': reddit_score / len(reddit_mentions) if reddit_mentions else 0,
                'top_posts': sorted(reddit_mentions, key=lambda x: x['score'], reverse=True)[:5]
            }

        # StockTwits
        stocktwits_data = self.get_stocktwits_sentiment(stock_symbol)
        if stocktwits_data:
            results['platforms']['stocktwits'] = stocktwits_data

        # Twitter
        twitter_mentions = self.get_twitter_mentions(stock_symbol)
        if twitter_mentions:
            twitter_sentiments = [self.analyze_sentiment(m['text']) for m in twitter_mentions]
            twitter_score = sum(1 if s == 'bullish' else -1 if s == 'bearish' else 0
                              for s in twitter_sentiments)

            results['platforms']['twitter'] = {
                'mentions': len(twitter_mentions),
                'sentiment_score': twitter_score / len(twitter_mentions) if twitter_mentions else 0,
                'top_tweets': sorted(twitter_mentions, key=lambda x: x['likes'], reverse=True)[:5]
            }

        # Calculate overall metrics
        total_mentions = sum(p.get('mentions', 0) for p in results['platforms'].values())
        results['total_mentions'] = total_mentions

        # Weighted sentiment score
        sentiment_scores = []
        if 'reddit' in results['platforms']:
            sentiment_scores.append(results['platforms']['reddit']['sentiment_score'])
        if 'stocktwits' in results['platforms']:
            sentiment_scores.append(results['platforms']['stocktwits']['sentiment_score'])
        if 'twitter' in results['platforms']:
            sentiment_scores.append(results['platforms']['twitter']['sentiment_score'])

        if sentiment_scores:
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
            results['sentiment_score'] = avg_sentiment

            if avg_sentiment > 0.3:
                results['overall_sentiment'] = 'bullish'
            elif avg_sentiment < -0.3:
                results['overall_sentiment'] = 'bearish'
            else:
                results['overall_sentiment'] = 'neutral'

        # Trending score (mentions + engagement)
        results['trending_score'] = total_mentions

        return results

    def print_summary(self, results):
        """Print formatted summary of sentiment analysis"""
        print()
        print("=" * 70)
        print("📊 SENTIMENT SUMMARY")
        print("=" * 70)
        print(f"Symbol: ${results['symbol']}")
        print(f"Total Mentions: {results['total_mentions']}")
        print(f"Overall Sentiment: {results['overall_sentiment'].upper()}")
        print(f"Sentiment Score: {results['sentiment_score']:.2f} (-1 to +1)")
        print(f"Trending Score: {results['trending_score']}")
        print()

        for platform, data in results['platforms'].items():
            print(f"📱 {platform.upper()}:")
            print(f"   Mentions: {data.get('mentions', 0)}")
            print(f"   Sentiment: {data.get('sentiment_score', 0):.2f}")

            if platform == 'reddit' and 'top_posts' in data:
                print(f"   Top Post: {data['top_posts'][0]['title'][:60]}...")
            elif platform == 'stocktwits':
                print(f"   Bullish: {data.get('bullish_count', 0)}, Bearish: {data.get('bearish_count', 0)}")
            print()

        print("=" * 70)


def main():
    """Demo: Analyze social sentiment for a stock"""

    if len(sys.argv) < 2:
        print("Usage: python3 social_sentiment_analyzer.py SYMBOL")
        print("Example: python3 social_sentiment_analyzer.py TSLA")
        sys.exit(1)

    symbol = sys.argv[1].upper()

    analyzer = SocialSentimentAnalyzer()
    results = analyzer.get_comprehensive_sentiment(symbol)
    analyzer.print_summary(results)

    # Save results
    output_file = f"sentiment_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"💾 Results saved to: {output_file}")


if __name__ == "__main__":
    main()
