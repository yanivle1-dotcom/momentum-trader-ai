# 📱 Social Media Sentiment Analyzer for Stock Trading

Automatically collects and analyzes stock mentions from multiple social media platforms to identify trending stocks before price movements.

## ✨ Features

- 📱 **Multi-Platform Data Collection** - Reddit, StockTwits, Twitter/X
- 🎯 **Sentiment Analysis** - Bullish/Bearish/Neutral classification
- 📊 **Trending Score** - Identifies viral stocks gaining attention
- 🤖 **Automated Daily Scans** - Monitor watchlist automatically
- 💾 **JSON Export** - Easy integration with trading systems
- 📈 **Top Posts Tracking** - See what's driving the sentiment

## 🔍 Platforms Covered

### Reddit
- r/wallstreetbets (WSB)
- r/stocks
- r/investing
- r/StockMarket
- r/pennystocks
- r/options

### StockTwits
- Dedicated stock trading social network
- Built-in bullish/bearish sentiment labels
- Real trader opinions

### Twitter/X
- Stock ticker mentions ($TSLA, etc.)
- Hashtag tracking (#stocks)
- Engagement metrics (likes, retweets)

## 🛠️ Installation

### 1. Install Python dependencies
```bash
pip3 install requests python-dotenv
```

### 2. Setup API Keys

#### Reddit API
1. Go to: https://www.reddit.com/prefs/apps
2. Click "create another app"
3. Select "script"
4. Fill in:
   - name: `StockAnalyzer`
   - redirect uri: `http://localhost:8080`
5. Copy Client ID and Secret

#### Twitter API
1. Go to: https://developer.twitter.com/en/portal/dashboard
2. Create a project and app
3. Generate Bearer Token
4. Copy the token

#### StockTwits
- No API key needed! Public API available

### 3. Configure environment variables
```bash
cd /Users/yanivlevi/momentum-trader-ai
cp .env.example .env
nano .env  # Add your API keys
```

Add to `.env`:
```
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_secret_here
TWITTER_BEARER_TOKEN=your_token_here
```

## 🚀 Usage

### Analyze single stock
```bash
python3 social_sentiment_analyzer.py TSLA
```

### Daily watchlist scan
```bash
python3 daily_sentiment_scan.py
```

### Example output:
```
======================================================================
📊 SOCIAL SENTIMENT ANALYSIS: $TSLA
======================================================================

📱 REDDIT:
   Mentions: 45
   Sentiment: 0.38

💬 STOCKTWITS:
   Mentions: 89
   Bullish: 67, Bearish: 22 (score: 0.51)

🐦 TWITTER:
   Mentions: 128
   Sentiment: 0.22

======================================================================
📊 SENTIMENT SUMMARY
======================================================================
Symbol: $TSLA
Total Mentions: 262
Overall Sentiment: BULLISH
Sentiment Score: 0.37 (-1 to +1)
Trending Score: 262
```

## 📊 Understanding the Scores

### Sentiment Score (-1 to +1)
- **0.7 - 1.0**: Extreme euphoria 🚀 (be cautious - possible bubble)
- **0.3 - 0.7**: Strong bullish 📈 (good signal)
- **-0.3 - 0.3**: Neutral 😐 (no clear signal)
- **-0.7 - -0.3**: Strong bearish 📉 (consider shorting)
- **-1.0 - -0.7**: Panic 💀 (possible buying opportunity)

### Trending Score
- **500+**: Viral stock - massive attention
- **200-500**: Very popular
- **100-200**: Popular
- **50-100**: Moderate attention
- **< 50**: Low mentions

## 📈 Trading Strategies

### 1. WSB Effect (Momentum Trading)
```
If:
- Reddit mentions > 100 per day
- Sentiment Score > 0.5
- Sudden spike in mentions

Then: Buy at open, sell after 2-3 days
```

### 2. Contrarian Strategy
```
If:
- Sentiment Score < -0.6 (very negative)
- Stock price hasn't dropped much
- Reason is not fundamental

Then: Buy - likely overreaction
```

### 3. Confirmation Strategy
```
If:
- Your technical analysis says BUY
- Sentiment is also positive (> 0.3)

Then: Strong confirmation for trade
```

## 🔗 Integration with Trading System

### Python Integration
```python
from social_sentiment_analyzer import SocialSentimentAnalyzer

analyzer = SocialSentimentAnalyzer()
results = analyzer.get_comprehensive_sentiment('TSLA')

# Trading decision
if results['trending_score'] > 100 and results['sentiment_score'] > 0.3:
    print(f"🚨 STRONG BUY SIGNAL for {results['symbol']}")
elif results['trending_score'] > 100 and results['sentiment_score'] < -0.3:
    print(f"⚠️  STRONG SELL SIGNAL for {results['symbol']}")
```

### JSON Output
```python
import json

with open('sentiment_TSLA_20251203_123456.json', 'r') as f:
    data = json.load(f)

sentiment = data['sentiment_score']
mentions = data['total_mentions']

# Use in your trading algorithm
if mentions > 50 and sentiment > 0.4:
    execute_buy_order(data['symbol'])
```

## 🤖 Automated Daily Scans

Edit [daily_sentiment_scan.py](daily_sentiment_scan.py) to customize your watchlist:

```python
WATCHLIST = [
    'TSLA', 'NVDA', 'AAPL', 'AMD', 'PLTR',
    'GME', 'AMC', 'MSFT', 'GOOGL', 'META'
]
```

Run automatically with cron:
```bash
crontab -e

# Add this line - runs daily at 8 AM
0 8 * * * cd /Users/yanivlevi/momentum-trader-ai && python3 daily_sentiment_scan.py
```

## 📝 Output Files

### Single Stock Analysis
```
sentiment_TSLA_20251203_123456.json
```
Contains:
- Symbol and timestamp
- Platform-specific data
- Overall sentiment score
- Top posts/tweets
- Trending score

### Daily Scan Results
```
daily_sentiment_20251203_123456.json
```
Contains:
- All scanned stocks
- Ranked by trending score
- Strong buy/sell signals
- Viral stocks

## ⚠️ Rate Limits

- **Reddit**: 60 requests/minute (without auth)
- **Twitter**: 450 requests per 15 minutes
- **StockTwits**: No documented limit

The system automatically waits 2-3 seconds between requests.

## 🔧 Advanced Features

### Custom Sentiment Keywords

Edit sentiment keywords in [social_sentiment_analyzer.py](social_sentiment_analyzer.py:225):

```python
bullish_words = [
    'buy', 'long', 'calls', 'moon', 'rocket', 'bullish',
    # Add your own keywords
]

bearish_words = [
    'sell', 'short', 'puts', 'crash', 'dump', 'bearish',
    # Add your own keywords
]
```

### Historical Data Collection

Run scanner every hour and build a database:
```bash
# Add to crontab
0 * * * * cd /Users/yanivlevi/momentum-trader-ai && python3 daily_sentiment_scan.py >> sentiment_history.log
```

## 💡 Future Enhancements

Planned features:
- ✅ Reddit integration
- ✅ StockTwits integration
- ✅ Twitter integration
- 🔲 Instagram hashtag scraping
- 🔲 TikTok video analysis
- 🔲 Discord channel monitoring
- 🔲 ML-based sentiment (vs keyword)
- 🔲 Image/meme analysis
- 🔲 Influencer tracking
- 🔲 Real-time alerts (SMS/Email)
- 🔲 Historical backtesting

## 📚 Learn More

Recommended reading:
- "The WSB Effect" - How Reddit affects stock prices
- "Social Sentiment Trading" - Academic research
- "Alternative Data in Trading" - Using social media data

## 🤝 Contributing

Found a bug? Have a feature request? Please check the GitHub issues.

## 📄 License

MIT License - Feel free to use and modify!

---

**Happy Trading! 📈💰**

Remember: Social sentiment is just ONE tool. Always combine with technical and fundamental analysis.
