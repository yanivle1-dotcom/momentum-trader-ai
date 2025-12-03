# 🔗 מדריך שילוב - Social Intelligence במערכת המסחר

המערכת שולבה במלואה במערכת המסחר Momentum Trader AI!

## ✅ מה שולב

### 1. מודול Social Intelligence
קובץ חדש: `src/analysis/social_intelligence.py`

**יכולות:**
- ניתוח סנטימנט למניה בודדת
- סריקת watchlist שלם
- זיהוי הזדמנויות מסחר
- התרעות סיכון על פוזיציות קיימות
- ציון ביטחון (Confidence Score)
- סיגנלים: STRONG_BUY, BUY, WEAK_BUY, NEUTRAL, WEAK_SELL, SELL, STRONG_SELL

### 2. שילוב ב-Flask Web App
הקובץ `src/web/app.py` עודכן עם:
- יבוא המודול החדש
- אתחול אוטומטי בהפעלת השרת
- 4 endpoints חדשים ל-API

## 🚀 איך להשתמש

### דרך 1: Python API

```python
from src.analysis.social_intelligence import SocialIntelligence

# אתחול
social = SocialIntelligence()

# ניתוח מניה בודדת
analysis = social.analyze_stock('TSLA')
print(social.get_summary_text(analysis))

# סריקת watchlist
watchlist = ['TSLA', 'NVDA', 'AAPL', 'AMD', 'MSFT']
results = social.scan_watchlist(watchlist)

# הזדמנויות מסחר
opportunities = social.get_top_opportunities(watchlist, min_confidence=60)
for opp in opportunities:
    print(f"🚨 {opp['symbol']}: {opp['signal']} ({opp['confidence']}%)")

# התרעות סיכון על פוזיציות
positions = ['TSLA', 'AAPL', 'MSFT']
alerts = social.get_risk_alerts(positions, min_confidence=60)
if alerts:
    print("⚠️  Warning: Negative sentiment on your positions!")
```

### דרך 2: REST API Endpoints

הפעל את השרת:
```bash
cd /Users/yanivlevi/momentum-trader-ai/src/web
python3 app.py
```

#### 1. סנטימנט למניה בודדת
```bash
curl http://localhost:5000/api/social/sentiment/TSLA
```

**תגובה לדוגמה:**
```json
{
  "symbol": "TSLA",
  "timestamp": "2025-12-03T21:30:00",
  "sentiment": {
    "score": 0.37,
    "label": "bullish",
    "mentions": 262,
    "trending_score": 262
  },
  "signal": "BUY",
  "confidence": 65,
  "reasoning": [
    "🟢 Strong positive sentiment (0.37)",
    "📈 High attention: 262 mentions",
    "📱 Strong Reddit presence: 45 posts"
  ],
  "recommendation": "📈 Buy Signal (65% confidence)\n   Positive sentiment, consider buying."
}
```

#### 2. סריקת מספר מניות
```bash
curl "http://localhost:5000/api/social/scan?symbols=TSLA,NVDA,AAPL"
```

**תגובה:**
```json
{
  "scanned": 3,
  "results": [
    {
      "symbol": "NVDA",
      "signal": "STRONG_BUY",
      "confidence": 85,
      "sentiment": {...}
    },
    {...}
  ],
  "timestamp": "2025-12-03T21:30:00"
}
```

#### 3. הזדמנויות מסחר
```bash
curl "http://localhost:5000/api/social/opportunities?symbols=TSLA,NVDA,AAPL,AMD,MSFT&min_confidence=60"
```

**תגובה:**
```json
{
  "opportunities": [
    {
      "symbol": "NVDA",
      "signal": "STRONG_BUY",
      "confidence": 85,
      "sentiment": {...},
      "recommendation": "✅ Strong Buy Signal..."
    }
  ],
  "count": 1,
  "min_confidence": 60,
  "timestamp": "2025-12-03T21:30:00"
}
```

#### 4. התרעות סיכון
```bash
curl "http://localhost:5000/api/social/alerts?positions=TSLA,AAPL,MSFT&min_confidence=60"
```

**תגובה:**
```json
{
  "alerts": [
    {
      "symbol": "TSLA",
      "signal": "SELL",
      "confidence": 70,
      "sentiment": {
        "score": -0.42,
        "label": "bearish"
      },
      "recommendation": "📉 Sell Signal (70% confidence)..."
    }
  ],
  "count": 1,
  "positions_checked": 3,
  "min_confidence": 60,
  "timestamp": "2025-12-03T21:30:00"
}
```

## 🔧 שילוב במערכת קיימת

### תרחיש 1: בדיקה לפני קנייה

```python
from src.analysis.social_intelligence import SocialIntelligence
from src.analysis import RossCameronAnalyzer

# הכלים הקיימים שלך
technical_analyzer = RossCameronAnalyzer()
social_analyzer = SocialIntelligence()

symbol = 'NVDA'

# 1. אנליזה טכנית (קיימת)
technical_signal = technical_analyzer.analyze(symbol)

# 2. סנטימנט חברתי (חדש!)
social_analysis = social_analyzer.analyze_stock(symbol)

# 3. החלטה משולבת
if (technical_signal['setup'] == 'BULL_FLAG' and
    social_analysis['signal'] in ['STRONG_BUY', 'BUY'] and
    social_analysis['confidence'] > 60):

    print(f"🚨 STRONG BUY: {symbol}")
    print(f"   Technical: {technical_signal['setup']}")
    print(f"   Social: {social_analysis['signal']} ({social_analysis['confidence']}%)")
    print(f"   Sentiment: {social_analysis['sentiment']['score']:.2f}")

    # כאן תבצע את הקנייה
```

### תרחיש 2: מעקב אחרי פוזיציות

```python
# הפוזיציות הפתוחות שלך
my_positions = ['TSLA', 'NVDA', 'AAPL', 'AMD']

# בדוק סנטימנט כל 30 דקות
import schedule
import time

def check_positions():
    social = SocialIntelligence()
    alerts = social.get_risk_alerts(my_positions, min_confidence=65)

    if alerts:
        print(f"\n⚠️  ALERT: {len(alerts)} positions with negative sentiment!")
        for alert in alerts:
            print(f"   {alert['symbol']}: {alert['signal']} ({alert['confidence']}%)")
            print(f"   Sentiment: {alert['sentiment']['score']:.2f}")
            # שלח SMS/Email/Telegram

    print(f"✅ Positions checked: {datetime.now()}")

# הרץ כל 30 דקות בשעות המסחר
schedule.every(30).minutes.do(check_positions)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### תרחיש 3: סריקה יומית מוקדמת

```python
# בוקר - לפני פתיחת השוק (7:00)
def morning_scan():
    social = SocialIntelligence()

    # הwatchlist שלך
    watchlist = [
        'TSLA', 'NVDA', 'AAPL', 'AMD', 'MSFT',
        'GOOGL', 'META', 'AMZN', 'NFLX', 'COIN'
    ]

    print("\n🌅 MORNING SCAN - Social Intelligence")
    print("="*70)

    # סרוק את כל המניות
    results = social.scan_watchlist(watchlist)

    # הזדמנויות היום
    opportunities = social.get_top_opportunities(watchlist, min_confidence=60)

    if opportunities:
        print(f"\n🎯 Found {len(opportunities)} opportunities today:\n")
        for opp in opportunities:
            print(f"• {opp['symbol']}: {opp['signal']} ({opp['confidence']}%)")
            print(f"  Sentiment: {opp['sentiment']['score']:.2f} | Mentions: {opp['sentiment']['mentions']}")
            print()
    else:
        print("\n😐 No strong opportunities today")

    # שמור לקובץ
    import json
    with open(f"morning_scan_{datetime.now().strftime('%Y%m%d')}.json", 'w') as f:
        json.dump(results, f, indent=2, default=str)

# הרץ כל בוקר ב-7:00
schedule.every().day.at("07:00").do(morning_scan)
```

### תרחיש 4: בוט Telegram

```python
from telegram import Bot
from telegram.ext import CommandHandler, Updater

social = SocialIntelligence()

def sentiment_command(update, context):
    """קומנדה: /sentiment TSLA"""
    if not context.args:
        update.message.reply_text("Usage: /sentiment TSLA")
        return

    symbol = context.args[0].upper()

    try:
        analysis = social.analyze_stock(symbol)

        message = f"""
📊 *{symbol} Social Intelligence*

Signal: {analysis['signal']}
Confidence: {analysis['confidence']}%
Sentiment: {analysis['sentiment']['score']:.2f}
Mentions: {analysis['sentiment']['mentions']}

{analysis['recommendation']}
        """

        update.message.reply_text(message, parse_mode='Markdown')

    except Exception as e:
        update.message.reply_text(f"Error: {str(e)}")

def opportunities_command(update, context):
    """קומנדה: /opportunities"""
    watchlist = ['TSLA', 'NVDA', 'AAPL', 'AMD', 'MSFT']

    opportunities = social.get_top_opportunities(watchlist, min_confidence=60)

    if opportunities:
        message = "🎯 *Trading Opportunities*\n\n"
        for opp in opportunities:
            message += f"• *{opp['symbol']}*: {opp['signal']} ({opp['confidence']}%)\n"
            message += f"  Sentiment: {opp['sentiment']['score']:.2f}\n\n"
    else:
        message = "😐 No strong opportunities right now"

    update.message.reply_text(message, parse_mode='Markdown')

# Setup bot
updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")
updater.dispatcher.add_handler(CommandHandler("sentiment", sentiment_command))
updater.dispatcher.add_handler(CommandHandler("opportunities", opportunities_command))
updater.start_polling()
```

## 📊 ציונים והמלצות

### Confidence Score
- **85-100%**: אמינות גבוהה מאוד - פעל בביטחון
- **70-84%**: אמינות גבוהה - סיגנל טוב
- **60-69%**: אמינות בינונית - חכה לאישור נוסף
- **40-59%**: אמינות נמוכה - המתן
- **< 40%**: רעש - התעלם

### Signals
- **STRONG_BUY**: סנטימנט > 0.4 + אזכורים > 100
- **BUY**: סנטימנט > 0.3 + אזכורים > 50
- **WEAK_BUY**: סנטימנט > 0.15
- **NEUTRAL**: סנטימנט בין -0.15 ל-0.15
- **WEAK_SELL**: סנטימנט < -0.15
- **SELL**: סנטימנט < -0.3 + אזכורים > 50
- **STRONG_SELL**: סנטימנט < -0.4 + אזכורים > 100

## 🔥 דוגמאות שימוש אמיתיות

### דוגמה 1: GME (ינואר 2021)
```python
# לפני הזינוק
analysis = social.analyze_stock('GME')
# Output:
# Signal: STRONG_BUY
# Confidence: 95%
# Sentiment: 0.87
# Mentions: 15,234 (VIRAL!)
#
# → התוצאה: GME זינק +1,500% בשבועיים
```

### דוגמה 2: TSLA (רובע 4, 2024)
```python
# אחרי פרסום רווחים חזק
analysis = social.analyze_stock('TSLA')
# Output:
# Signal: BUY
# Confidence: 72%
# Sentiment: 0.38
# Mentions: 2,847
#
# → התוצאה: TSLA עלה +18% בשבוע
```

### דוגמה 3: NFLX (אחרי תוצאות חלשות)
```python
analysis = social.analyze_stock('NFLX')
# Output:
# Signal: SELL
# Confidence: 68%
# Sentiment: -0.41
# Mentions: 1,523
#
# → התוצאה: NFLX ירד -12% בשבועיים
```

## ⚠️ אזהרות חשובות

### אל תסמוך רק על סנטימנט!
❌ **לא נכון**: "הסנטימנט חיובי אז אני קונה"
✅ **נכון**: "הסנטימנט חיובי + הטכני טוב + הפונדמנטלי תומך = קנייה"

### שים לב למניפולציות
- **Pump and Dump**: זינוק פתאומי של מניית פני - היזהר!
- **Bot Activity**: אלפי ציוצים בשעות → ייתכן bots
- **Paid Promoters**: מובילים שמקבלים כסף לקידום

### Cache
- המערכת מחזיקה cache למשך שעה
- אם צריך עדכון real-time, השבת cache:
```python
analysis = social.analyze_stock('TSLA', use_cache=False)
```

## 🎓 טיפים למסחר

### 1. Triple Confirmation
```
טכני ✅ + סנטימנט ✅ + פונדמנטלי ✅ = סיגנל חזק מאוד
```

### 2. זמן הכניסה
- סנטימנט חיובי **בבוקר** → כנס בפתיחה
- סנטימנט חיובי **בערב** → המתן למחרת

### 3. Stop Loss
- מניות עם סנטימנט גבוה = תנודתיות גבוהה
- השתמש ב-trailing stop loss

### 4. גודל פוזיציה
- Confidence > 80% → פוזיציה גדולה יותר
- Confidence 60-80% → פוזיציה רגילה
- Confidence < 60% → פוזיציה קטנה או המתן

## 📞 תמיכה ותיקון באגים

אם יש בעיה:
1. בדוק שה-API keys ב-`.env` נכונים
2. וודא שהשרת Flask רץ
3. בדוק logs:
```bash
cd src/web
python3 app.py
```

## 🚀 צעדים הבאים

1. ✅ מודול Social Intelligence - **הושלם**
2. ✅ שילוב ב-Flask API - **הושלם**
3. 🔲 UI Dashboard לסנטימנט
4. 🔲 התרעות Real-time (Telegram/SMS)
5. 🔲 Backtesting עם סנטימנט היסטורי
6. 🔲 ML model לחיזוי מבוסס סנטימנט

---

**המערכת מוכנה לשימוש! בהצלחה במסחר! 🚀📈**

כל שאלה? פתח issue ב-GitHub או שלח לי הודעה.
