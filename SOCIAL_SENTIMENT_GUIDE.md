# 📱 מדריך מערכת ניתוח סנטימנט מרשתות חברתיות

מערכת שאוספת ומנתחת אזכורים של מניות מרשתות חברתיות כדי לזהות טרנדים לפני תנועות מחיר.

## 🎯 מה המערכת עושה?

המערכת אוספת מידע מהרשתות הבאות:
- **Reddit** - r/wallstreetbets, r/stocks, r/investing, r/StockMarket, r/pennystocks, r/options
- **StockTwits** - פלטפורמה ייעודית למניות עם סנטימנט משולב
- **Twitter/X** - ציוצים עם הזכרות של מניות
- **Instagram** - (בפיתוח) האשטאגים של מניות
- **TikTok** - (בפיתוח) סרטונים על מניות

## 📊 איך זה עובד?

1. **איסוף נתונים** - חיפוש באתרים עבור סימול המניה ($TSLA, $NVDA, וכו')
2. **ניתוח סנטימנט** - קביעה אם כל אזכור הוא חיובי/שלילי/ניטרלי
3. **חישוב ציון** - משוקלל לפי פלטפורמה, מספר אזכורים, ו-engagement
4. **שמירת תוצאות** - JSON עם כל הנתונים לשילוב במערכת המסחר

## 🔑 הוצאת API Keys

### 1. Reddit API
1. עבור ל: https://www.reddit.com/prefs/apps
2. לחץ "create another app" בתחתית הדף
3. בחר "script"
4. מלא:
   - name: `StockAnalyzer`
   - description: `Stock sentiment analyzer`
   - redirect uri: `http://localhost:8080`
5. לחץ "create app"
6. העתק:
   - **Client ID**: המחרוזת מתחת ל"personal use script"
   - **Client Secret**: המחרוזת ליד "secret"

### 2. Twitter/X API
1. עבור ל: https://developer.twitter.com/en/portal/dashboard
2. צור פרויקט חדש
3. צור App חדש
4. עבור ל-Keys and Tokens
5. צור Bearer Token
6. העתק את ה-Bearer Token

### 3. StockTwits
- **לא נדרש API key!** הAPI פתוח לציבור
- אם יש בעיות עם Cloudflare, אפשר להוסיף User-Agent מתקדם

## ⚙️ התקנה

### 1. התקן חבילות Python
```bash
pip3 install requests python-dotenv
```

### 2. הגדר API Keys בקובץ .env
```bash
cd /Users/yanivlevi/momentum-trader-ai
nano .env
```

הוסף את השורות הבאות:
```
# Reddit API
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here

# Twitter API
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here
```

## 🚀 שימוש

### הרצה בודדת למניה אחת:
```bash
cd /Users/yanivlevi/momentum-trader-ai
python3 social_sentiment_analyzer.py TSLA
```

### דוגמאות למניות פופולריות:
```bash
python3 social_sentiment_analyzer.py NVDA
python3 social_sentiment_analyzer.py AAPL
python3 social_sentiment_analyzer.py GME
python3 social_sentiment_analyzer.py AMC
```

## 📈 פלט התוכנית

התוכנית מציגה:
```
======================================================================
📊 SOCIAL SENTIMENT ANALYSIS: $TSLA
======================================================================

📱 REDDIT:
   Mentions: 45
   Sentiment: 0.38

💬 STOCKTWITS:
   Bullish: 67, Bearish: 23 (score: 0.44)

🐦 TWITTER:
   Mentions: 128
   Sentiment: 0.22

======================================================================
📊 SENTIMENT SUMMARY
======================================================================
Symbol: $TSLA
Total Mentions: 173
Overall Sentiment: BULLISH
Sentiment Score: 0.35 (-1 to +1)
Trending Score: 173
```

הקובץ JSON נשמר אוטומטית:
```
sentiment_TSLA_20251203_203456.json
```

## 🔗 שילוב עם מערכת המסחר

### דוגמה לשימוש בקוד Python:

```python
from social_sentiment_analyzer import SocialSentimentAnalyzer

# צור אנליזר
analyzer = SocialSentimentAnalyzer()

# קבל סנטימנט למניה
results = analyzer.get_comprehensive_sentiment('TSLA')

# בדוק אם כדאי לסחור
if results['trending_score'] > 100 and results['sentiment_score'] > 0.3:
    print(f"🚨 STRONG BUY SIGNAL for {results['symbol']}")
    print(f"   Trending: {results['trending_score']} mentions")
    print(f"   Sentiment: {results['sentiment_score']}")

elif results['trending_score'] > 100 and results['sentiment_score'] < -0.3:
    print(f"⚠️  STRONG SELL SIGNAL for {results['symbol']}")
```

### אינטגרציה אוטומטית:
```python
import json

# קרא תוצאות מקובץ
with open('sentiment_TSLA_20251203_203456.json', 'r') as f:
    data = json.load(f)

# שלב עם אסטרטגיית המסחר
sentiment_score = data['sentiment_score']
total_mentions = data['total_mentions']

# החלטת סחר
if total_mentions > 50:  # מספיק אזכורים
    if sentiment_score > 0.4:
        action = "BUY"
    elif sentiment_score < -0.4:
        action = "SELL"
    else:
        action = "HOLD"
```

## 🎯 אסטרטגיות מסחר לפי סנטימנט

### 1. טרנדים ויראליים (WSB Effect)
```
אם:
- Reddit mentions > 100 (ביום)
- Sentiment Score > 0.5
- זינוק פתאומי באזכורים

אז: קנה בפתיחה, מכור אחרי 2-3 ימים
```

### 2. סנטימנט הפוך (Contrarian)
```
אם:
- Sentiment Score < -0.6 (שלילי מאוד)
- המניה לא ממש נפלה במחיר
- הסיבה לא פונדמנטלית

אז: קנה - ייתכן overreaction
```

### 3. אימות אסטרטגיה
```
אם:
- האנליזה הטכנית שלך אומרת BUY
- גם הסנטימנט חיובי (> 0.3)

אז: אישור חזק לסחר
```

## 📊 הבנת הציונים

### Sentiment Score (-1 to +1):
- **0.7 - 1.0**: אופוריה מוחלטת 🚀 (זהיר - ייתכן bubble)
- **0.3 - 0.7**: חיובי חזק 📈 (אות טוב)
- **-0.3 - 0.3**: ניטרלי 😐 (אין אות ברור)
- **-0.7 - -0.3**: שלילי חזק 📉 (שקול SHORT או המתן)
- **-1.0 - -0.7**: פאניקה 💀 (ייתכן הזדמנות קנייה)

### Trending Score:
- **500+**: מניה ויראלית - תשומת לב עצומה
- **200-500**: מאוד פופולרית
- **100-200**: פופולרית
- **50-100**: תשומת לב בינונית
- **< 50**: מעט אזכורים

## 🤖 הרצה אוטומטית

### סקריפט לסריקה יומית של מניות:

צור קובץ: `daily_sentiment_scan.py`

```python
#!/usr/bin/env python3
from social_sentiment_analyzer import SocialSentimentAnalyzer
import json
from datetime import datetime

# רשימת מניות לסריקה
WATCHLIST = ['TSLA', 'NVDA', 'AAPL', 'AMD', 'PLTR', 'GME', 'AMC', 'MSFT']

analyzer = SocialSentimentAnalyzer()
hot_stocks = []

print("🔍 Starting daily sentiment scan...")

for symbol in WATCHLIST:
    print(f"\n📊 Analyzing {symbol}...")
    results = analyzer.get_comprehensive_sentiment(symbol)

    # שמור מניות עם סנטימנט חזק
    if results['total_mentions'] > 50:
        hot_stocks.append({
            'symbol': symbol,
            'sentiment': results['sentiment_score'],
            'mentions': results['total_mentions'],
            'trending': results['trending_score']
        })

# מיין לפי trending score
hot_stocks.sort(key=lambda x: x['trending'], reverse=True)

# הצג תוצאות
print("\n" + "="*70)
print("🔥 HOT STOCKS TODAY")
print("="*70)

for stock in hot_stocks[:5]:  # Top 5
    print(f"📈 {stock['symbol']}: {stock['mentions']} mentions, sentiment: {stock['sentiment']:.2f}")

# שמור לקובץ
output = {
    'date': datetime.now().isoformat(),
    'hot_stocks': hot_stocks
}

with open('daily_sentiment.json', 'w') as f:
    json.dump(output, f, indent=2)
```

הרץ אוטומטית כל יום:
```bash
chmod +x daily_sentiment_scan.py
crontab -e

# הוסף שורה זו - הרצה כל יום ב-8 בבוקר
0 8 * * * cd /Users/yanivlevi/momentum-trader-ai && python3 daily_sentiment_scan.py
```

## ⚠️ הגבלות וטיפים

### Rate Limiting:
- **Reddit**: 60 בקשות לדקה (ללא אימות)
- **Twitter**: 450 בקשות ל-15 דקות
- **StockTwits**: אין הגבלה מדווחת

המערכת מוסיפה המתנה של 2 שניות בין בקשות.

### טיפים לשיפור דיוק:
1. **צור היסטוריה** - אסוף נתונים למשך שבוע לפני סחר
2. **השווה לממוצע** - מניה עם 100 אזכורים זה הרבה ל-GME, מעט ל-TSLA
3. **בדוק פתאומיות** - זינוק פתאומי חשוב מספר מוחלט
4. **שים לב לתזמון** - סנטימנט בשעות המסחר יותר חשוב

## 🔧 Troubleshooting

### בעיה: Reddit לא מחזיר תוצאות
**פתרון**:
- וודא שה-API keys נכונים
- נסה לחפש בדפדפן קודם: https://www.reddit.com/r/wallstreetbets/search?q=TSLA

### בעיה: Twitter API error 403
**פתרון**:
- וודא שיש לך Bearer Token מ-Twitter Developer Portal
- בדוק שהפרויקט שלך מאושר לגישה ל-API v2

### בעיה: StockTwits לא עובד (Cloudflare)
**פתרון**:
- זה נורמלי - StockTwits יש הגנת Cloudflare
- ניתן לדלג עליו - Reddit + Twitter מספיקים
- או להשתמש ב-browser automation (Selenium)

## 📝 קבצים במערכת

```
momentum-trader-ai/
├── social_sentiment_analyzer.py    # המנוע הראשי
├── SOCIAL_SENTIMENT_GUIDE.md       # המדריך הזה
├── .env                             # API keys (אל תעלה ל-GitHub!)
├── .env.example                     # תבנית ל-API keys
└── sentiment_*.json                 # תוצאות הסריקות
```

## 🎓 לימוד נוסף

מאמרים מומלצים:
- "The WSB Effect" - איך Reddit משפיע על מחירי מניות
- "Social Sentiment Trading" - מחקרים אקדמיים על מסחר לפי סנטימנט
- "Alternative Data in Trading" - שימוש בנתוני רשתות חברתיות

## 💡 רעיונות לשיפורים עתידיים

1. **ML Sentiment Analysis** - במקום keywords, השתמש במודל AI
2. **Image Analysis** - נתח תמונות ומימים (bullish/bearish)
3. **Influencer Tracking** - עקוב אחרי traders מפורסמים
4. **Discord Integration** - צ'אנלים של מסחר
5. **Real-time Alerts** - התרעות SMS/Email על זינוקים
6. **Backtesting** - בדוק איך הסנטימנט חזה תנועות בעבר

---

**בהצלחה במסחר! 📈💰**

זכור: סנטימנט הוא רק כלי אחד. תמיד שלב עם אנליזה טכנית ופונדמנטלית.
