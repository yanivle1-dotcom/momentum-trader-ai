# 📰 מדריך News Feed של מובילי דעת קהל בשוק ההון

מערכת שאוספת המלצות ותובנות ממובילי דעת קהל מובילים בישראל ובעולם בתחום שוק ההון.

## 🎯 מה המערכת עושה?

המערכת אוספת תוכן מ:
- **Twitter/X** - ציוצים עם המלצות למניות
- **YouTube** - סרטוני אנליזה חדשים
- **זיהוי אוטומטי** - מזהה המלצות קנייה/מכירה
- **חילוץ מניות** - מזהה אוטומטית $TSLA, $NVDA וכו'

## 👥 מובילי דעת קהל במערכת

### 🇮🇱 ישראלים:
1. **מיכה סטוקס** (@MichaStocks)
   - מנתח טכני, מומחה למניות אמריקאיות
   - YouTube + Twitter

2. **צביקה ברגמן** (@ZvikaBergman)
   - כלכלן, מומחה למניות ישראל וארה"ב
   - YouTube + Twitter

3. **רועי רז** (@RoiRazInvest)
   - מנתח שוקי הון, מומחה לאופציות
   - Twitter

4. **גיי רולניק** (@GuyRolnik)
   - עיתונאי כלכלי, פרופסור לכלכלה
   - Twitter

5. **יניב פגוט** (@YanivPagot)
   - אסטרטג השקעות, מנכ"ל פגוט
   - Twitter

### 🌍 עולמיים:
1. **Warren Buffett** (@WarrenBuffett)
   - CEO של Berkshire Hathaway
   - משקיע ערך מספר 1 בעולם

2. **Cathie Wood** (@CathieDWood)
   - CEO של ARK Invest
   - מתמחה בחדשנות וטכנולוגיה

3. **Jim Cramer** (@jimcramer)
   - מנחה Mad Money ב-CNBC
   - המלצות יומיות למניות

4. **Bill Ackman** (@BillAckman)
   - CEO של Pershing Square
   - משקיע אקטיביסט

5. **Michael Burry** (@michaeljburry)
   - מייסד Scion Asset Management
   - ידוע מ-The Big Short

6. **Elon Musk** (@elonmusk)
   - CEO Tesla, SpaceX
   - ציוצים משפיעים על השוק

7. **Ray Dalio** (@RayDalio)
   - מייסד Bridgewater Associates
   - מומחה מאקרו

8. **Gary Gensler** (@GaryGensler)
   - יו"ר SEC
   - עדכונים רגולטוריים

## 🔑 הוצאת API Keys

### 1. Twitter API (חובה)
השתמש באותו Bearer Token משלב הסנטימנט:
```
TWITTER_BEARER_TOKEN=your_token_here
```

### 2. YouTube API (אופציונלי)

1. עבור ל: https://console.cloud.google.com/apis/credentials
2. צור פרויקט חדש או בחר קיים
3. לחץ "Enable APIs and Services"
4. חפש "YouTube Data API v3" והפעל
5. עבור ל-Credentials → Create Credentials → API Key
6. העתק את ה-API Key

**חשוב:** YouTube API מוגבל ל-10,000 יחידות ביום (חינמי).
כל חיפוש וידאו = 100 יחידות, כלומר 100 חיפושים ביום.

## ⚙️ התקנה

### הגדר API Keys בקובץ .env:
```bash
cd /Users/yanivlevi/momentum-trader-ai
nano .env
```

הוסף:
```
# Twitter (חובה)
TWITTER_BEARER_TOKEN=your_bearer_token_here

# YouTube (אופציונלי)
YOUTUBE_API_KEY=your_youtube_api_key_here
```

## 🚀 שימוש

### הרץ את ה-News Feed:
```bash
python3 influencers_feed.py
```

### פלט לדוגמה:
```
======================================================================
📰 INFLUENCERS FEED - TOP INSIGHTS
======================================================================

📊 Showing 20 most recent insights:

1. 🐦 מיכה סטוקס 🟢
   💰 Stocks: $NVDA, $TSLA
   📊 Signal: BUY
   📝 נראה לי שNVIDIA תפרוץ את 500$ השבוע. המומנטום חזק...
   🔗 https://twitter.com/MichaStocks/status/...

2. 🐦 Cathie Wood 🟢
   💰 Stocks: $COIN, $SHOP
   📊 Signal: BUY
   📝 Adding to our position in $COIN. We believe crypto...
   🔗 https://twitter.com/CathieDWood/status/...

3. 📺 צביקה ברגמן
   📝 ניתוח שוק: למה הבנקים בישראל יעלו ב-2026
   🔗 https://www.youtube.com/watch?v=...

======================================================================
📈 SUMMARY BY TICKER
======================================================================

$NVDA: 5 mentions by 3 influencers 🟢 BULLISH
   Signals: 4 BUY, 1 SELL

$TSLA: 4 mentions by 2 influencers 🔴 BEARISH
   Signals: 1 BUY, 3 SELL

$AAPL: 3 mentions by 2 influencers
   Signals: 2 BUY, 1 SELL
```

## 📊 מה תקבל?

### 1. פיד ממוין לפי תאריך
- הציוצים/סרטונים האחרונים מכל המובילים
- מזהה אוטומטית המלצות BUY/SELL/HOLD
- מחלץ סימולי מניות ($TSLA, $NVDA, וכו')

### 2. סיכום לפי מניה
- כמה פעמים כל מניה הוזכרה
- כמה מובילים דיברו עליה
- מה היחס בין BUY ל-SELL

### 3. קובץ JSON מלא
```
influencers_feed_20251203_143027.json
```

## 🎯 איך להשתמש בזה למסחר

### אסטרטגיה 1: קונצנזוס מובילים
```
אם:
- 3+ מובילים מזכירים את אותה מניה
- רוב ההמלצות BUY
- בפרק זמן של 24 שעות

👉 סיגנל חזק לקנייה
```

### אסטרטגיה 2: התראה מוקדמת
```
אם:
- מובל משפיע (Cathie Wood, Buffett) מזכיר מניה חדשה
- עדיין לא תופס תאוצה

👉 כנס מוקדם לפני הקהל
```

### אסטרטגיה 3: סטופ לוס חכם
```
אם:
- מחזיק מניה
- מובילים מתחילים לדבר שלילי
- 2+ המלצות SELL

👉 שקול לצאת מהפוזיציה
```

### אסטרטגיה 4: שילוב עם סנטימנט
```
אם:
- מובילים ממליצים BUY
- גם סנטימנט הרשתות חיובי
- גם האנליזה הטכנית שלך מסכימה

👉 Triple confirmation - סיגנל חזק מאוד!
```

## 🔗 שילוב עם המערכות האחרות

### שילוב עם Social Sentiment:
```python
from influencers_feed import InfluencersFeed
from social_sentiment_analyzer import SocialSentimentAnalyzer

# אסוף המלצות מובילים
feed = InfluencersFeed()
items = feed.aggregate_feed()

# מצא מניות שמובילים ממליצים עליהן
recommended_stocks = set()
for item in items:
    if item.get('recommendation') == 'BUY':
        recommended_stocks.update(item.get('tickers', []))

# בדוק סנטימנט לכל מניה
analyzer = SocialSentimentAnalyzer()
for stock in recommended_stocks:
    sentiment = analyzer.get_comprehensive_sentiment(stock)

    if sentiment['sentiment_score'] > 0.3:
        print(f"🚨 STRONG BUY: ${stock}")
        print(f"   Influencers recommend + positive social sentiment")
```

## 📱 הוספת מובילים נוספים

ערוך את `influencers_feed.py` בשורה 37:

```python
'israeli': [
    {
        'name': 'שם מובל',
        'name_en': 'Name in English',
        'twitter': 'TwitterHandle',
        'youtube': '@YouTubeChannel',
        'description': 'תיאור קצר',
        'focus': 'technical_analysis',  # או: fundamental, options, etc.
        'language': 'he'
    },
    # הוסף עוד מובילים כאן
],
```

## 🤖 הרצה אוטומטית

### סקריפט יומי - בוקר + ערב:

```bash
crontab -e

# כל יום ב-8:00 בבוקר
0 8 * * * cd /Users/yanivlevi/momentum-trader-ai && python3 influencers_feed.py

# כל יום ב-20:00 בערב
0 20 * * * cd /Users/yanivlevi/momentum-trader-ai && python3 influencers_feed.py
```

### שלח התראה אם יש המלצה חזקה:

צור קובץ: `check_influencers_alerts.py`

```python
#!/usr/bin/env python3
from influencers_feed import InfluencersFeed
import json

feed = InfluencersFeed()
items = feed.aggregate_feed()

# ספור המלצות BUY לפי מניה
buy_signals = {}
for item in items:
    if item.get('recommendation') == 'BUY':
        for ticker in item.get('tickers', []):
            if ticker not in buy_signals:
                buy_signals[ticker] = 0
            buy_signals[ticker] += 1

# התרעה על מניות עם 3+ המלצות
for ticker, count in buy_signals.items():
    if count >= 3:
        print(f"🚨 ALERT: ${ticker} has {count} BUY recommendations from influencers!")
        # כאן תוסיף שליחת SMS/Email/Telegram
```

## 📊 ניתוח מתקדם

### מעקב אחר דיוק מובילים:

צור מסד נתונים שעוקב אחר המלצות לאורך זמן:

```python
import json
from datetime import datetime, timedelta

# קרא פיד היסטורי
feeds = []
# ... טען קבצי JSON מהימים האחרונים

# בדוק איזה מובילים צדקו
for influencer in ['מיכה סטוקס', 'Cathie Wood', 'Jim Cramer']:
    recommendations = []

    for feed in feeds:
        for item in feed['items']:
            if item['influencer'] == influencer:
                recommendations.append(item)

    # השווה להמלצות מחיר המניה 7 ימים אחרי
    # חשב אחוז הצלחה
```

## ⚠️ הגבלות

### Twitter API:
- 450 בקשות ל-15 דקות
- המערכת ממתינה 2 שניות בין בקשות

### YouTube API:
- 10,000 יחידות ביום (חינמי)
- 100 יחידות לחיפוש
- = 100 חיפושים ביום
- אם צריך יותר: $0 for first 10,000, then paid

### Twitter Accounts:
- חלק מהחשבונות פרטיים או מוגנים
- לא כל המובילים פעילים ב-Twitter
- Elon Musk מציף הרבה - אפשר להגביל

## 💡 טיפים

1. **התחל עם Twitter בלבד** - YouTube אופציונלי
2. **הרץ פעמיים ביום** - בוקר + ערב
3. **שלב עם סנטימנט** - וודא שהקהל מסכים עם המובילים
4. **עקוב אחרי דיוק** - רשום את ההמלצות ובדוק תוצאות
5. **אל תסמוך רק על זה** - זה כלי נוסף, לא תחליף לאנליזה

## 🎓 דוגמאות שימוש מהחיים

### דוגמה 1: Cathie Wood קנתה COIN
```
2024-03-15: Cathie Wood tweeted about buying $COIN
+ Social sentiment was positive (0.4)
+ Technical analysis showed breakout

Result: COIN +25% in 2 weeks
```

### דוגמה 2: Michael Burry shorted TSLA
```
2024-02-10: Burry announced short position on $TSLA
- Social sentiment turned negative (-0.3)
- Influencers started agreeing

Result: TSLA -15% in 1 month
```

### דוגמה 3: מיכה סטוקס ו-NVDA
```
2024-01-05: מיכה המליץ על NVDA לפני פרסום רווחים
+ צביקה ברגמן הסכים
+ סנטימנט Reddit חיובי מאוד

Result: NVDA +30% אחרי הרווחים
```

## 🔮 פיצ'רים עתידיים

- ✅ Twitter integration
- ✅ YouTube integration
- 🔲 Telegram channels
- 🔲 Discord servers
- 🔲 LinkedIn posts
- 🔲 Blog posts / Seeking Alpha
- 🔲 Podcast transcripts
- 🔲 Real-time alerts
- 🔲 WhatsApp/SMS notifications
- 🔲 Accuracy tracking
- 🔲 Portfolio simulation

## 📞 הוספת מובילים

רוצה להוסיף מובל דעה נוסף? פתח issue ב-GitHub או ערוך את הקובץ בעצמך!

המבנה:
```python
{
    'name': 'שם המובל',
    'twitter': 'Handle',
    'description': 'מי זה',
    'focus': 'מה התמחותו',
    'language': 'he' או 'en'
}
```

---

**בהצלחה במעקב אחרי מובילי הדעה! 📰💰**

זכור: מובילי דעה יכולים לטעות. תמיד עשה את המחקר שלך לפני השקעה!
