# 🚀 Momentum Trader AI - Complete Trading Intelligence System

מערכת מסחר חכמה המשלבת ניתוח סנטימנט מרשתות חברתיות, המלצות ממובילי דעת קהל, וכלי מסחר מתקדמים.

## ✨ מה במערכת?

### 1. 📱 Social Sentiment Analyzer
ניתוח סנטימנט של מניות מרשתות חברתיות:
- **Reddit** - r/wallstreetbets, r/stocks, r/investing
- **StockTwits** - פלטפורמה ייעודית למניות
- **Twitter/X** - ציוצים עם $TSLA, $NVDA וכו'

```bash
python3 social_sentiment_analyzer.py TSLA
python3 daily_sentiment_scan.py
```

📖 [מדריך מלא: SOCIAL_SENTIMENT_GUIDE.md](SOCIAL_SENTIMENT_GUIDE.md)

---

### 2. 📰 Influencers News Feed
מעקב אחרי המלצות ממובילי דעת קהל:

**🇮🇱 ישראלים:**
- מיכה סטוקס, צביקה ברגמן, רועי רז
- גיי רולניק, יניב פגוט

**🌍 עולמיים:**
- Warren Buffett, Cathie Wood, Jim Cramer
- Bill Ackman, Michael Burry, Elon Musk
- Ray Dalio, Gary Gensler

```bash
python3 influencers_feed.py
```

📖 [מדריך מלא: INFLUENCERS_GUIDE.md](INFLUENCERS_GUIDE.md)

---

### 3. 🎯 Combined Signals
שילוב של כל מקורות המידע:
- סנטימנט רשתות חברתיות
- המלצות מובילי דעה
- ציון ביטחון (Confidence Score)
- סיגנלים: STRONG BUY, BUY, HOLD, SELL, STRONG SELL

```bash
python3 combined_signals.py
```

---

## 🔑 Setup - התקנה מהירה

### 1. Clone הפרויקט
```bash
git clone git@github.com:yanivle1-dotcom/momentum-trader-ai.git
cd momentum-trader-ai
```

### 2. התקן Dependencies
```bash
pip3 install requests python-dotenv
```

### 3. הגדר API Keys

העתק את `.env.example` ל-`.env`:
```bash
cp .env.example .env
nano .env
```

הוסף את המפתחות שלך:
```
# חובה - לסנטימנט ומובילים
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_secret
TWITTER_BEARER_TOKEN=your_twitter_token

# אופציונלי - לסרטונים של מובילים
YOUTUBE_API_KEY=your_youtube_key
```

### 4. הרץ!
```bash
# סנטימנט למניה בודדת
python3 social_sentiment_analyzer.py NVDA

# סריקת watchlist מלאה
python3 daily_sentiment_scan.py

# פיד מובילי דעה
python3 influencers_feed.py

# שילוב הכל - סיגנלים משולבים
python3 combined_signals.py
```

---

## 📊 פלט לדוגמה

### Social Sentiment:
```
📊 SOCIAL SENTIMENT ANALYSIS: $TSLA
Total Mentions: 262
Overall Sentiment: BULLISH
Sentiment Score: 0.37 (-1 to +1)

📱 REDDIT: 45 mentions, sentiment: 0.38
💬 STOCKTWITS: 89 messages (67 bullish, 22 bearish)
🐦 TWITTER: 128 tweets, sentiment: 0.22
```

### Influencers Feed:
```
📰 INFLUENCERS FEED - TOP INSIGHTS

1. 🐦 מיכה סטוקס 🟢
   💰 Stocks: $NVDA
   📊 Signal: BUY

2. 🐦 Cathie Wood 🟢
   💰 Stocks: $COIN
   📊 Signal: BUY

📈 SUMMARY BY TICKER
$NVDA: 5 mentions by 3 influencers 🟢 BULLISH
```

### Combined Signals:
```
🚀 STRONG BUY SIGNALS:

💰 $NVDA
   Signal: STRONG BUY (Confidence: 85%)
   Sentiment: 0.45 | Mentions: 234
   Reasoning:
      • 🟢 Strong positive social sentiment
      • 🔥 Viral stock: 234 mentions
      • 👥 3 influencers recommend BUY
```

---

## 🎯 אסטרטגיות מסחר

### Triple Confirmation (הכי חזק!)
```
✅ מובילים ממליצים BUY
✅ סנטימנט חיובי (> 0.3)
✅ אנליזה טכנית מסכימה

👉 Confidence 85%+ - סיגנל חזק מאוד
```

### Early Bird
```
✅ מובל משפיע מזכיר מניה
❌ עדיין אין buzz ברשתות

👉 כנס מוקדם לפני הקהל
```

### WSB Effect
```
✅ Reddit mentions > 100
✅ Sentiment > 0.5
✅ זינוק פתאומי באזכורים

👉 קנה בפתיחה, מכור אחרי 2-3 ימים
```

### Stop Loss חכם
```
❌ מובילים מדברים שלילי
❌ סנטימנט הופך
✅ אתה מחזיק

👉 צא מהפוזיציה
```

---

## 🤖 הרצה אוטומטית

### cron jobs - סריקה יומית אוטומטית:

```bash
crontab -e
```

הוסף:
```
# סנטימנט - כל יום ב-8:00
0 8 * * * cd /Users/yanivlevi/momentum-trader-ai && python3 daily_sentiment_scan.py

# מובילים - כל יום ב-7:30 (לפני השוק)
30 7 * * 1-5 cd /Users/yanivlevi/momentum-trader-ai && python3 influencers_feed.py

# סיגנלים משולבים - כל יום ב-20:00
0 20 * * * cd /Users/yanivlevi/momentum-trader-ai && python3 combined_signals.py
```

---

## 🔗 API Keys - איפה מוציאים?

### Reddit API (חינמי)
1. https://www.reddit.com/prefs/apps
2. Create app → script
3. העתק Client ID + Secret

### Twitter API (חינמי)
1. https://developer.twitter.com/en/portal/dashboard
2. Create project + app
3. Generate Bearer Token

### YouTube API (אופציונלי)
1. https://console.cloud.google.com/apis/credentials
2. Enable YouTube Data API v3
3. Create API Key
4. מוגבל ל-10,000 יחידות/יום (חינמי)

---

## 📁 מבנה הפרויקט

```
momentum-trader-ai/
├── social_sentiment_analyzer.py   # ניתוח סנטימנט רשתות
├── daily_sentiment_scan.py        # סריקת watchlist יומית
├── influencers_feed.py            # פיד מובילי דעה
├── combined_signals.py            # שילוב כל המקורות
│
├── SOCIAL_SENTIMENT_GUIDE.md      # מדריך סנטימנט (עברית)
├── SENTIMENT_README.md            # תיעוד סנטימנט (אנגלית)
├── INFLUENCERS_GUIDE.md           # מדריך מובילים (עברית)
│
├── .env.example                   # תבנית API keys
├── .env                           # המפתחות שלך (אל תעלה ל-Git!)
└── *.json                         # תוצאות סריקות
```

---

## 📚 מדריכים מפורטים

- **[SOCIAL_SENTIMENT_GUIDE.md](SOCIAL_SENTIMENT_GUIDE.md)** - מדריך מלא לניתוח סנטימנט (עברית)
- **[SENTIMENT_README.md](SENTIMENT_README.md)** - Social sentiment documentation (English)
- **[INFLUENCERS_GUIDE.md](INFLUENCERS_GUIDE.md)** - מדריך מובילי דעה (עברית)
- **[סיכום_סנטימנט.md](סיכום_סנטימנט.md)** - סיכום מהיר - סנטימנט
- **[סיכום_מובילי_דעה.md](סיכום_מובילי_דעה.md)** - סיכום מהיר - מובילים

---

## 🎓 דוגמאות שימוש

### דוגמה 1: בדיקה מהירה של מניה
```bash
python3 social_sentiment_analyzer.py TSLA
```

### דוגמה 2: סריקת watchlist
ערוך את `daily_sentiment_scan.py` (שורה 13):
```python
WATCHLIST = ['TSLA', 'NVDA', 'AAPL', 'AMD', 'MSFT']
```
הרץ:
```bash
python3 daily_sentiment_scan.py
```

### דוגמה 3: שילוב Python
```python
from social_sentiment_analyzer import SocialSentimentAnalyzer

analyzer = SocialSentimentAnalyzer()
results = analyzer.get_comprehensive_sentiment('NVDA')

if results['sentiment_score'] > 0.4 and results['total_mentions'] > 100:
    print("🚨 STRONG BUY SIGNAL!")
```

### דוגמה 4: סיגנלים משולבים
```python
from combined_signals import CombinedSignals

analyzer = CombinedSignals()
results = analyzer.scan_watchlist(['TSLA', 'NVDA', 'AAPL'])

# סנן רק STRONG BUY
strong_buys = [r for r in results if r['combined_signal'] == 'STRONG BUY']
for stock in strong_buys:
    print(f"🚨 {stock['symbol']}: {stock['confidence']}% confidence")
```

---

## ⚠️ הגבלות וטיפים

### Rate Limits:
- **Reddit**: 60 requests/minute
- **Twitter**: 450 requests/15 minutes
- **YouTube**: 10,000 units/day (100 searches)

### טיפים:
1. ✅ **התחל עם Reddit + Twitter** - YouTube אופציונלי
2. ✅ **הרץ פעמיים ביום** - בוקר וערב
3. ✅ **שלב עם טכני** - אל תסמוך רק על סנטימנט
4. ✅ **בנה היסטוריה** - רוץ שבוע לפני מסחר
5. ✅ **עקוב אחרי דיוק** - תעד מי צודק

### אזהרות:
- ❌ **אל תסמוך רק על מובילים** - גם Buffett טועה
- ❌ **אל תזרום עיוור** - Jim Cramer ~47% דיוק
- ❌ **אל תשכח Stop Loss** - זה לא 100%
- ❌ **אל תתעלם מ-fundamentals** - סנטימנט ≠ ערך

---

## 💡 רעיונות לשיפורים עתידיים

- ✅ Reddit, StockTwits, Twitter integration
- ✅ Influencers tracking (Israeli + Global)
- ✅ Combined signals system
- 🔲 Instagram hashtag scraping
- 🔲 TikTok video analysis
- 🔲 Discord channels monitoring
- 🔲 Telegram groups tracking
- 🔲 ML-based sentiment (vs keywords)
- 🔲 Real-time alerts (SMS/WhatsApp)
- 🔲 Accuracy tracking dashboard
- 🔲 Historical backtesting
- 🔲 Portfolio simulation

---

## 🤝 Contributing

מצאת bug? יש רעיון לפיצ'ר? רוצה להוסיף מובל דעה?
פתח issue ב-GitHub!

---

## 📄 License

MIT License - Feel free to use and modify!

---

## 🙏 Credits

Built with:
- Python 3.9+
- Twitter API v2
- Reddit API
- YouTube Data API v3
- StockTwits API

---

## 📞 Support

אם יש בעיות:
1. בדוק את ה-API keys ב-`.env`
2. וודא חיבור לאינטרנט
3. בדוק את המדריכים המפורטים
4. הרץ עם מניה פופולרית (TSLA, NVDA)

---

## 🎯 Quick Start Checklist

- [ ] Clone הפרויקט
- [ ] `pip3 install requests python-dotenv`
- [ ] הוצא Reddit API keys
- [ ] הוצא Twitter Bearer Token
- [ ] העתק `.env.example` ל-`.env`
- [ ] הוסף את המפתחות ל-`.env`
- [ ] הרץ: `python3 social_sentiment_analyzer.py TSLA`
- [ ] הרץ: `python3 influencers_feed.py`
- [ ] הרץ: `python3 combined_signals.py`
- [ ] הגדר cron jobs לאוטומציה

---

**בהצלחה במסחר! 🚀📈💰**

זכור: Information + Analysis + Discipline = Success

> "The stock market is a device for transferring money from the impatient to the patient."
> - Warren Buffett
