# 📈 Momentum Trader AI - Ross Cameron System

מערכת ניתוח מומנטום מתקדמת לפי שיטת **Ross Cameron / Warrior Trading** עם שילוב AI Agents (ChatGPT, Gemini, Perplexity).

## 🎯 מה המערכת עושה?

המערכת מספקת:
- ✅ **סריקה אוטומטית** של מניות מומנטום (ישראליות ואמריקאיות)
- ✅ **זיהוי סט-אפים** לפי Ross Cameron (Gap & Go, Red to Green, First Green Day, וכו')
- ✅ **ניתוח AI בזמן אמת** עם חיפוש חדשות וקטליסטים
- ✅ **המלצות כניסה/יציאה** מדויקות עם Risk:Reward
- ✅ **גרפים אינטראקטיביים** עם אינדיקטורים
- ✅ **תמיכה בשקלים** - המרה אוטומטית USD→ILS
- ✅ **ממשק בעברית** מלא

## 🚀 התקנה מהירה

### דרישות מקדימות

- Python 3.8 ומעלה
- מפתחות API (לפחות אחד):
  - OpenAI (ChatGPT)
  - Google Gemini
  - Perplexity AI

### שלב 1: הורדה והתקנה

```bash
cd momentum-trader-ai

# צור סביבה וירטואלית
python3 -m venv venv

# הפעל את הסביבה
# Mac/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# התקן תלויות
pip install -r requirements.txt
```

### שלב 2: הגדרת מפתחות API

העתק את קובץ הדוגמה:
```bash
cp .env.example .env
```

ערוך את הקובץ `.env` והוסף את המפתחות שלך:

```bash
# לפחות מפתח אחד נדרש!
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
PERPLEXITY_API_KEY=pplx-...

# אופציונלי - לשער מטבע מדויק יותר
EXCHANGE_RATE_API_KEY=...
```

#### איפה להשיג מפתחות API?

**OpenAI (ChatGPT):**
1. היכנס ל: https://platform.openai.com/api-keys
2. לחץ "Create new secret key"
3. העתק את המפתח

**Google Gemini:**
1. היכנס ל: https://makersuite.google.com/app/apikey
2. לחץ "Get API key"
3. העתק את המפתח

**Perplexity AI:**
1. היכנס ל: https://www.perplexity.ai/settings/api
2. צור API key חדש
3. העתק את המפתח

**Exchange Rate (אופציונלי):**
1. היכנס ל: https://www.exchangerate-api.com/
2. הירשם בחינם (1,500 בקשות/חודש)
3. העתק את המפתח

### שלב 3: הרצת המערכת

```bash
cd src/web
python app.py
```

פתח דפדפן וגש ל:
```
http://localhost:5000
```

## 📊 איך להשתמש במערכת?

### 1. סריקת מניות

לחץ על כפתור **"🔍 סרוק מניות"** - המערכת תסרוק אוטומטית מניות עם:
- RVOL ≥ 2.0x
- Gap ≥ 3%
- נפח מינימלי 100K

### 2. ניתוח מלא

לחץ על כרטיס מניה כדי לקבל:
- 🎯 **זיהוי סט-אפ** (Gap & Go, Red to Green, וכו')
- 📊 **נתוני שוק** עדכניים
- 🤖 **ניתוח AI** עם חדשות/קטליסטים
- 💰 **תוכנית מסחר** מלאה:
  - נקודת כניסה
  - סטופ לוס
  - 3 יעדים
  - Risk:Reward
- 📈 **גרף אינטראקטיבי** עם VWAP, EMA9, EMA20

### 3. בחירת AI Agent

השתמש בתפריט הנפתח כדי לבחור:
- **ChatGPT** - מהיר ומדויק
- **Gemini** - חזק בניתוח טקסטואלי
- **Perplexity** - מצוין לחיפוש חדשות בזמן אמת

## ⚙️ התאמה אישית

### הוספת/הסרת מניות

ערוך את הקובץ: `config/stocks.json`

```json
{
  "israeli_stocks": [
    "TEVA.TA",
    "NICE.TA",
    "המניות_שלך.TA"
  ],
  "us_stocks_popular_in_israel": [
    "NVDA",
    "TSLA",
    "המניות_שלך"
  ]
}
```

### שינוי קריטריוני סינון

ערוך את `momentum_criteria` באותו קובץ:

```json
{
  "momentum_criteria": {
    "min_rvol": 2.0,        // נפח יחסי מינימלי
    "min_gap_percent": 3.0, // גאפ מינימלי באחוזים
    "min_volume": 100000,   // נפח מינימלי
    "max_price": 500,       // מחיר מקסימלי
    "min_price": 1          // מחיר מינימלי
  }
}
```

## 🎓 הסבר על שיטת Ross Cameron

המערכת מזהה את הסט-אפים הבאים:

### 1. Gap & Go
- גאפ משמעותי (3%+)
- RVOL גבוה (2x+)
- מחיר מעל VWAP ו-EMA9
- פריצה עם נפח

### 2. Red to Green
- פתח באדום (גאפ שלילי)
- הופך לירוק במהלך היום
- נפח גבוה מאוד
- שובר מעל מחיר סגירה קודם

### 3. First Green Day
- 2+ ימים אדומים קודמים
- יום ירוק חזק (+2%+)
- עלייה בנפח
- פוטנציאל לטרנד חדש

### 4. Micro Pullback
- במגמת עלייה (EMA9 > EMA20)
- פולבק קל ל-EMA9
- מחיר מעל VWAP
- הזדמנות להצטרף למגמה

### 5. Bull Flag
- עלייה חדה (flagpole)
- קונסולידציה (5-15% pullback)
- נפח יורד בקונסולידציה
- פריצה חזרה למעלה

## 🏗️ מבנה הפרויקט

```
momentum-trader-ai/
├── src/
│   ├── agents/              # AI Agents
│   │   ├── base_agent.py
│   │   ├── openai_agent.py
│   │   ├── gemini_agent.py
│   │   └── perplexity_agent.py
│   ├── data/                # נתוני שוק
│   │   ├── market_data.py
│   │   └── currency_converter.py
│   ├── analysis/            # ניתוח טכני
│   │   └── ross_cameron_setups.py
│   └── web/                 # שרת ווב
│       └── app.py
├── templates/               # HTML
│   └── index.html
├── static/                  # CSS & JS
│   ├── css/style.css
│   └── js/app.js
├── config/                  # הגדרות
│   └── stocks.json
├── requirements.txt
├── .env                     # מפתחות API (אל תשתף!)
└── README.md
```

## 🐛 פתרון בעיות נפוצות

### שגיאה: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### שגיאה: "Agent not configured"
בדוק שהוספת מפתח API תקין בקובץ `.env`

### המערכת לא מוצאת מניות
- בדוק את הקריטריונים ב-`config/stocks.json`
- נסה בשעות מסחר (אחרי פתיחת השוק)
- הרחב את הסימבולים ברשימה

### גרף לא נטען
בדוק שיש חיבור לאינטרנט (Plotly נטען מ-CDN)

### שער מטבע לא מתעדכן
הוסף מפתח API ל-ExchangeRate-API בקובץ `.env`

## ⚠️ דיסקליימר חשוב

**המערכת הזו היא לחינוך בלבד!**

- ❌ זה **לא** ייעוץ השקעות אישי
- ❌ זה **לא** המלצה לקנות/למכור
- ❌ אין ערבות לרווח
- ✅ תמיד עשה מחקר עצמאי
- ✅ אל תסחר עם כסף שאתה לא יכול להפסיד
- ✅ השתמש ב-paper trading לתרגול

**המסחר במניות כרוך בסיכון גבוה ואפשרות להפסד מלא של ההון.**

## 🔒 אבטחה

- **אל תשתף** את קובץ ה-`.env` עם מפתחות ה-API
- הוסף `.env` ל-`.gitignore` אם אתה מעלה לגיטהאב
- שמור על המפתחות בסוד

## 📚 משאבים נוספים

- [Warrior Trading YouTube](https://www.youtube.com/c/WarriorTrading)
- [Ross Cameron Trading Strategies](https://www.warriortrading.com/trading-strategies/)
- [Day Trading Guide](https://www.warriortrading.com/day-trading/)

## 🤝 תרומה לפרויקט

רוצה לשפר? מוזמן!
1. Fork את הפרויקט
2. צור branch חדש
3. בצע שינויים
4. שלח Pull Request

## 📝 רישיון

MIT License - חופשי לשימוש אישי וחינוכי.

---

**נבנה עם ❤️ לקהילת הטריידרים הישראלית**

לשאלות או תמיכה: [צור Issue ב-GitHub]
