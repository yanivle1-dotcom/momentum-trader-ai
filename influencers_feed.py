#!/usr/bin/env python3
"""
📰 Stock Market Influencers News Feed
Collects recommendations and insights from top Israeli and global market influencers
"""

import os
import sys
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import time
import re

load_dotenv()

# API Keys
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

class InfluencersFeed:
    """Aggregates content from top Israeli and global stock market influencers"""

    def __init__(self):
        self.influencers = self._get_influencers_list()
        self.feed_items = []

    def _get_influencers_list(self):
        """
        List of top Israeli and global stock market influencers
        """
        return {
            # מובילי דעה ישראליים
            'israeli': [
                {
                    'name': 'מיכה סטוקס',
                    'name_en': 'Micha Stocks',
                    'twitter': 'MichaStocks',
                    'youtube': '@MichaStocks',
                    'description': 'מנתח טכני, מומחה למניות אמריקאיות',
                    'focus': 'technical_analysis',
                    'language': 'he'
                },
                {
                    'name': 'צביקה ברגמן',
                    'name_en': 'Zvika Bergman',
                    'twitter': 'ZvikaBergman',
                    'youtube': '@ZvikaBergman',
                    'description': 'כלכלן, מומחה למניות ישראל וארה"ב',
                    'focus': 'fundamental_analysis',
                    'language': 'he'
                },
                {
                    'name': 'רועי רז',
                    'name_en': 'Roi Raz',
                    'twitter': 'RoiRazInvest',
                    'description': 'מנתח שוקי הון, מומחה לאופציות',
                    'focus': 'options',
                    'language': 'he'
                },
                {
                    'name': 'גיא רולניק',
                    'name_en': 'Guy Rolnik',
                    'twitter': 'GuyRolnik',
                    'description': 'עיתונאי כלכלי, פרופסור לכלכלה',
                    'focus': 'economics',
                    'language': 'he'
                },
                {
                    'name': 'יניב פגוט',
                    'name_en': 'Yaniv Pagot',
                    'twitter': 'YanivPagot',
                    'description': 'אסטרטג השקעות, מנכ"ל פגוט',
                    'focus': 'strategy',
                    'language': 'he'
                },
            ],

            # Global influencers
            'global': [
                {
                    'name': 'Warren Buffett',
                    'twitter': 'WarrenBuffett',
                    'description': 'CEO of Berkshire Hathaway, value investor',
                    'focus': 'value_investing',
                    'language': 'en'
                },
                {
                    'name': 'Cathie Wood',
                    'twitter': 'CathieDWood',
                    'description': 'CEO of ARK Invest, innovation investor',
                    'focus': 'innovation',
                    'language': 'en'
                },
                {
                    'name': 'Jim Cramer',
                    'twitter': 'jimcramer',
                    'youtube': '@MadMoneyOnCNBC',
                    'description': 'Host of Mad Money, stock picker',
                    'focus': 'stock_picks',
                    'language': 'en'
                },
                {
                    'name': 'Bill Ackman',
                    'twitter': 'BillAckman',
                    'description': 'CEO of Pershing Square, activist investor',
                    'focus': 'activism',
                    'language': 'en'
                },
                {
                    'name': 'Michael Burry',
                    'twitter': 'michaeljburry',
                    'description': 'Founder of Scion Asset Management',
                    'focus': 'contrarian',
                    'language': 'en'
                },
                {
                    'name': 'Elon Musk',
                    'twitter': 'elonmusk',
                    'description': 'CEO Tesla, SpaceX - market moving tweets',
                    'focus': 'tech',
                    'language': 'en'
                },
                {
                    'name': 'Ray Dalio',
                    'twitter': 'RayDalio',
                    'description': 'Founder of Bridgewater Associates',
                    'focus': 'macro',
                    'language': 'en'
                },
                {
                    'name': 'Gary Gensler',
                    'twitter': 'GaryGensler',
                    'description': 'SEC Chairman - regulatory updates',
                    'focus': 'regulation',
                    'language': 'en'
                },
            ]
        }

    def get_twitter_posts(self, username, max_results=10):
        """
        Get recent tweets from an influencer
        """
        if not TWITTER_BEARER_TOKEN:
            print(f"⚠️  Twitter API token not found - skipping {username}")
            return []

        print(f"🐦 Fetching tweets from @{username}...")

        # First, get user ID
        user_url = f"https://api.twitter.com/2/users/by/username/{username}"
        headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}

        try:
            user_response = requests.get(user_url, headers=headers, timeout=10)
            if user_response.status_code != 200:
                print(f"   ❌ Could not find user @{username}")
                return []

            user_id = user_response.json()['data']['id']

            # Get user's tweets
            tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets"
            params = {
                'max_results': min(max_results, 10),
                'tweet.fields': 'created_at,public_metrics,entities',
                'exclude': 'retweets,replies'
            }

            tweets_response = requests.get(tweets_url, headers=headers, params=params, timeout=10)

            if tweets_response.status_code == 200:
                data = tweets_response.json()
                tweets = data.get('data', [])

                posts = []
                for tweet in tweets:
                    # Extract stock tickers
                    tickers = self._extract_tickers(tweet.get('text', ''))

                    posts.append({
                        'text': tweet.get('text', ''),
                        'created_at': tweet.get('created_at', ''),
                        'likes': tweet.get('public_metrics', {}).get('like_count', 0),
                        'retweets': tweet.get('public_metrics', {}).get('retweet_count', 0),
                        'tickers': tickers,
                        'url': f"https://twitter.com/{username}/status/{tweet.get('id')}"
                    })

                print(f"   ✅ Found {len(posts)} tweets")
                return posts

        except Exception as e:
            print(f"   ❌ Error fetching tweets: {e}")

        return []

    def _extract_tickers(self, text):
        """
        Extract stock tickers from text ($TSLA, $AAPL, etc.)
        """
        # Match $TICKER pattern
        tickers = re.findall(r'\$([A-Z]{1,5})\b', text)
        return list(set(tickers))  # Remove duplicates

    def _extract_recommendations(self, text):
        """
        Extract buy/sell recommendations from text
        """
        text_lower = text.lower()

        buy_keywords = [
            'buy', 'buying', 'long', 'bullish', 'calls',
            'קנייה', 'קונה', 'קנה', 'לונג', 'עולה'
        ]

        sell_keywords = [
            'sell', 'selling', 'short', 'bearish', 'puts',
            'מכירה', 'מוכר', 'מכור', 'שורט', 'יורד'
        ]

        hold_keywords = [
            'hold', 'holding', 'wait', 'neutral',
            'החזקה', 'מחזיק', 'המתן', 'נייטרלי'
        ]

        # Count keywords
        buy_count = sum(1 for word in buy_keywords if word in text_lower)
        sell_count = sum(1 for word in sell_keywords if word in text_lower)
        hold_count = sum(1 for word in hold_keywords if word in text_lower)

        if buy_count > sell_count and buy_count > hold_count:
            return 'BUY'
        elif sell_count > buy_count and sell_count > hold_count:
            return 'SELL'
        elif hold_count > 0:
            return 'HOLD'
        else:
            return 'NEUTRAL'

    def get_youtube_videos(self, channel_handle, max_results=5):
        """
        Get recent videos from YouTube channel
        """
        if not YOUTUBE_API_KEY:
            print(f"⚠️  YouTube API key not found - skipping {channel_handle}")
            return []

        print(f"📺 Fetching YouTube videos from {channel_handle}...")

        try:
            # Search for channel
            search_url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                'key': YOUTUBE_API_KEY,
                'part': 'snippet',
                'q': channel_handle,
                'type': 'video',
                'maxResults': max_results,
                'order': 'date'
            }

            response = requests.get(search_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])

                videos = []
                for item in items:
                    snippet = item.get('snippet', {})
                    videos.append({
                        'title': snippet.get('title', ''),
                        'description': snippet.get('description', ''),
                        'published_at': snippet.get('publishedAt', ''),
                        'thumbnail': snippet.get('thumbnails', {}).get('medium', {}).get('url', ''),
                        'video_id': item.get('id', {}).get('videoId', ''),
                        'url': f"https://www.youtube.com/watch?v={item.get('id', {}).get('videoId', '')}"
                    })

                print(f"   ✅ Found {len(videos)} videos")
                return videos

        except Exception as e:
            print(f"   ❌ Error fetching YouTube: {e}")

        return []

    def aggregate_feed(self, focus_israeli=True, focus_global=True, max_per_influencer=5):
        """
        Aggregate feed from all influencers
        """
        print()
        print("=" * 70)
        print("📰 INFLUENCERS NEWS FEED - AGGREGATING...")
        print("=" * 70)
        print()

        all_items = []

        # Israeli influencers
        if focus_israeli:
            print("🇮🇱 Israeli Influencers:")
            print("-" * 70)
            for influencer in self.influencers['israeli']:
                print(f"\n👤 {influencer['name']} ({influencer['description']})")

                items = []

                # Twitter
                if 'twitter' in influencer:
                    tweets = self.get_twitter_posts(influencer['twitter'], max_per_influencer)
                    for tweet in tweets:
                        items.append({
                            'influencer': influencer['name'],
                            'influencer_en': influencer.get('name_en', influencer['name']),
                            'source': 'twitter',
                            'content': tweet['text'],
                            'created_at': tweet['created_at'],
                            'engagement': tweet['likes'] + tweet['retweets'],
                            'tickers': tweet['tickers'],
                            'recommendation': self._extract_recommendations(tweet['text']),
                            'url': tweet['url'],
                            'language': influencer['language'],
                            'focus': influencer['focus']
                        })

                # YouTube
                if 'youtube' in influencer:
                    videos = self.get_youtube_videos(influencer['youtube'], max_per_influencer)
                    for video in videos:
                        items.append({
                            'influencer': influencer['name'],
                            'influencer_en': influencer.get('name_en', influencer['name']),
                            'source': 'youtube',
                            'title': video['title'],
                            'content': video['description'],
                            'created_at': video['published_at'],
                            'thumbnail': video['thumbnail'],
                            'url': video['url'],
                            'language': influencer['language'],
                            'focus': influencer['focus']
                        })

                all_items.extend(items)
                time.sleep(2)  # Rate limiting

        # Global influencers
        if focus_global:
            print("\n🌍 Global Influencers:")
            print("-" * 70)
            for influencer in self.influencers['global']:
                print(f"\n👤 {influencer['name']} ({influencer['description']})")

                items = []

                # Twitter
                if 'twitter' in influencer:
                    tweets = self.get_twitter_posts(influencer['twitter'], max_per_influencer)
                    for tweet in tweets:
                        items.append({
                            'influencer': influencer['name'],
                            'source': 'twitter',
                            'content': tweet['text'],
                            'created_at': tweet['created_at'],
                            'engagement': tweet['likes'] + tweet['retweets'],
                            'tickers': tweet['tickers'],
                            'recommendation': self._extract_recommendations(tweet['text']),
                            'url': tweet['url'],
                            'language': influencer['language'],
                            'focus': influencer['focus']
                        })

                all_items.extend(items)
                time.sleep(2)  # Rate limiting

        # Sort by date (newest first)
        all_items.sort(key=lambda x: x.get('created_at', ''), reverse=True)

        return all_items

    def print_feed(self, items, show_top=20):
        """
        Print formatted feed
        """
        print()
        print("=" * 70)
        print("📰 INFLUENCERS FEED - TOP INSIGHTS")
        print("=" * 70)
        print()

        # Filter items with stock tickers or recommendations
        actionable = [item for item in items if item.get('tickers') or item.get('recommendation') != 'NEUTRAL']

        if not actionable:
            print("😐 No actionable insights found")
            return

        print(f"📊 Showing {min(show_top, len(actionable))} most recent insights:\n")

        for i, item in enumerate(actionable[:show_top], 1):
            emoji_source = "🐦" if item['source'] == 'twitter' else "📺"
            emoji_rec = ""
            if item.get('recommendation') == 'BUY':
                emoji_rec = " 🟢"
            elif item.get('recommendation') == 'SELL':
                emoji_rec = " 🔴"
            elif item.get('recommendation') == 'HOLD':
                emoji_rec = " 🟡"

            print(f"{i}. {emoji_source} {item['influencer']}{emoji_rec}")

            if item.get('tickers'):
                print(f"   💰 Stocks: {', '.join(['$' + t for t in item['tickers']])}")

            if item.get('recommendation') and item['recommendation'] != 'NEUTRAL':
                print(f"   📊 Signal: {item['recommendation']}")

            content = item.get('content', item.get('title', ''))
            if len(content) > 150:
                content = content[:150] + "..."
            print(f"   📝 {content}")

            print(f"   🔗 {item['url']}")
            print()

        # Summary by ticker
        print("=" * 70)
        print("📈 SUMMARY BY TICKER")
        print("=" * 70)

        ticker_mentions = {}
        for item in actionable:
            for ticker in item.get('tickers', []):
                if ticker not in ticker_mentions:
                    ticker_mentions[ticker] = {
                        'mentions': 0,
                        'buy': 0,
                        'sell': 0,
                        'influencers': set()
                    }

                ticker_mentions[ticker]['mentions'] += 1
                ticker_mentions[ticker]['influencers'].add(item['influencer'])

                if item.get('recommendation') == 'BUY':
                    ticker_mentions[ticker]['buy'] += 1
                elif item.get('recommendation') == 'SELL':
                    ticker_mentions[ticker]['sell'] += 1

        # Sort by mentions
        sorted_tickers = sorted(ticker_mentions.items(), key=lambda x: x[1]['mentions'], reverse=True)

        if sorted_tickers:
            print()
            for ticker, data in sorted_tickers[:10]:
                signal = ""
                if data['buy'] > data['sell']:
                    signal = " 🟢 BULLISH"
                elif data['sell'] > data['buy']:
                    signal = " 🔴 BEARISH"

                print(f"${ticker}: {data['mentions']} mentions by {len(data['influencers'])} influencers{signal}")
                print(f"   Signals: {data['buy']} BUY, {data['sell']} SELL")
        else:
            print("\n😐 No ticker mentions found")

        print()
        print("=" * 70)


def main():
    """
    Main function - aggregate and display influencers feed
    """
    feed = InfluencersFeed()

    print("📰 Market Influencers News Feed Aggregator")
    print("Collecting insights from top Israeli and global market leaders...")

    # Aggregate feed
    items = feed.aggregate_feed(
        focus_israeli=True,
        focus_global=True,
        max_per_influencer=5
    )

    # Print feed
    feed.print_feed(items, show_top=20)

    # Save to JSON
    output_file = f"influencers_feed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'generated_at': datetime.now().isoformat(),
            'total_items': len(items),
            'items': items
        }, f, indent=2, ensure_ascii=False)

    print(f"💾 Feed saved to: {output_file}")


if __name__ == "__main__":
    main()
