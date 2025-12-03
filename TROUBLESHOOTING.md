# 🔧 פתרון בעיות נפוצות

## תוכן עניינים מהיר
- [בעיות התקנה](#בעיות-התקנה)
- [בעיות הרצה](#בעיות-הרצה)
- [בעיות API](#בעיות-api)
- [בעיות נתונים](#בעיות-נתונים)
- [בעיות ממשק](#בעיות-ממשק)
- [בעיות ביצועים](#בעיות-ביצועים)

---

## 🔨 בעיות התקנה

### ❌ "python3: command not found"

**בעיה**: Python לא מותקן או לא בנתיב.

**פתרון Mac**:
```bash
# התקן Homebrew אם אין
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# התקן Python
brew install python3
```

**פתרון Windows**:
1. הורד מ: https://www.python.org/downloads/
2. **חשוב**: סמן "Add Python to PATH"
3. התקן

**בדיקה**:
```bash
python3 --version
# צריך להראות: Python 3.8.x ומעלה
```

---

### ❌ "pip: command not found"

**בעיה**: pip לא מותקן.

**פתרון**:
```bash
# Mac/Linux:
python3 -m ensurepip --upgrade

# אם זה לא עובד:
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

---

### ❌ "No module named 'flask'"

**בעיה**: חבילות לא מותקנות או סביבה וירטואלית לא פעילה.

**פתרון**:
```bash
# ודא שאתה בתיקיית הפרויקט:
cd /Users/yanivlevi/momentum-trader-ai

# הפעל את הסביבה הוירטואלית:
source venv/bin/activate  # Mac/Linux
# או
venv\Scripts\activate      # Windows

# התקן מחדש:
pip install -r requirements.txt

# בדיקה:
pip list | grep flask
```

---

### ❌ "Permission denied: setup.sh"

**בעיה**: הקובץ לא ניתן להרצה.

**פתרון**:
```bash
chmod +x setup.sh run.sh test_system.py
bash setup.sh
```

---

### ❌ התקנה תקועה / איטית

**בעיה**: בעיית רשת או מראה pip איטית.

**פתרון**:
```bash
# שדרג pip:
pip install --upgrade pip

# נסה עם timeout גבוה יותר:
pip install -r requirements.txt --timeout 100

# או עם מראה מהירה:
pip install -r requirements.txt -i https://pypi.org/simple
```

---

## 🚀 בעיות הרצה

### ❌ "Port 5000 already in use"

**בעיה**: יישום אחר משתמש בפורט 5000.

**פתרון 1** - שנה פורט:
```bash
# ערוך .env:
echo "FLASK_PORT=5001" >> .env

# הרץ מחדש:
bash run.sh
```

**פתרון 2** - סגור את התהליך הישן:
```bash
# Mac/Linux:
lsof -ti:5000 | xargs kill -9

# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

---

### ❌ "Address already in use"

**בעיה**: שרת Flask כבר רץ.

**פתרון**:
```bash
# סגור את השרת:
Ctrl+C (בטרמינל שבו הוא רץ)

# אם זה לא עוזר:
ps aux | grep flask
kill -9 <PID>
```

---

### ❌ ".env file not found"

**בעיה**: קובץ ההגדרות חסר.

**פתרון**:
```bash
# צור מהדוגמה:
cp .env.example .env

# ערוך והוסף מפתחות:
nano .env
```

---

### ❌ שרת מתחיל אבל דפדפן לא נפתח

**בעיה**: הדפדפן לא נפתח אוטומטית.

**פתרון**:
פתח ידנית:
```
http://localhost:5000
```

אם זה לא עובד, נסה:
```
http://127.0.0.1:5000
```

---

## 🔑 בעיות API

### ❌ "Agent not configured"

**בעיה**: מפתח API חסר או לא תקין.

**פתרון**:
```bash
# בדוק את .env:
cat .env

# ודא שיש לפחות מפתח אחד:
OPENAI_API_KEY=sk-...
# או
GEMINI_API_KEY=...
# או
PERPLEXITY_API_KEY=pplx-...

# בדוק שאין רווחים או מרכאות מיותרות!
```

**בדיקה**:
```bash
python test_system.py
```

---

### ❌ "Invalid API key"

**בעיה**: המפתח לא תקין או פג.

**פתרון**:

**OpenAI**:
1. לך ל: https://platform.openai.com/api-keys
2. צור מפתח חדש
3. העתק ל-`.env`

**Gemini**:
1. לך ל: https://makersuite.google.com/app/apikey
2. צור מפתח חדש
3. העתק ל-`.env`

**Perplexity**:
1. לך ל: https://www.perplexity.ai/settings/api
2. צור מפתח חדש
3. העתק ל-`.env`

---

### ❌ "Rate limit exceeded"

**בעיה**: עברת את מכסת ה-API.

**פתרון**:
1. **המתן**: מכסות מתאפסות לאחר זמן
2. **שדרג תוכנית**: אם אתה משתמש הרבה
3. **החלף Agent**: השתמש ב-agent אחר זמנית

**דוגמה**:
```javascript
// בדשבורד, החלף מ-ChatGPT ל-Gemini
```

---

### ❌ "Connection timeout"

**בעיה**: אין חיבור לאינטרנט או API down.

**פתרון**:
```bash
# בדוק חיבור:
ping google.com

# בדוק סטטוס APIs:
# OpenAI: https://status.openai.com/
# Google: https://status.cloud.google.com/
```

---

## 📊 בעיות נתונים

### ❌ "No data available"

**בעיה**: Yahoo Finance לא מחזיר נתונים למניה.

**סיבות אפשריות**:
1. סימבול שגוי
2. מניה לא נסחרת
3. שעות מחוץ למסחר

**פתרון**:
```bash
# בדוק סימבול:
# מניות ישראליות: TEVA.TA (עם .TA)
# מניות אמריקאיות: NVDA (בלי סיומת)

# בדוק שהמניה נסחרת:
# https://finance.yahoo.com/quote/NVDA
```

---

### ❌ "לא מוצא מניות בסריקה"

**בעיה**: אין מניות שעומדות בקריטריונים.

**סיבות**:
1. **לא שעות מסחר**: המניות לא בתנועה
2. **קריטריונים קשים**: RVOL/Gap גבוהים מדי
3. **יום שקט**: אין מומנטום היום

**פתרון**:
```json
// ערוך config/stocks.json:
{
  "momentum_criteria": {
    "min_rvol": 1.5,         // הורד מ-2.0
    "min_gap_percent": 2.0,  // הורד מ-3.0
    "min_volume": 50000      // הורד מ-100000
  }
}
```

**טיפ**: הרץ בין 9:30-11:00 EST (שעות הפריים).

---

### ❌ מחירים לא מתעדכנים

**בעיה**: נתונים ישנים.

**סיבות**:
1. Yahoo Finance delay (15 דקות חלק מהמניות)
2. שוק סגור
3. בעיית חיבור

**פתרון**:
```bash
# רענן דפדפן:
Ctrl+R (Cmd+R במק)

# או לחץ "רענן" בממשק

# בדוק שעות מסחר:
# NYSE: 9:30-16:00 EST
# TASE: 9:30-17:25 IST
```

---

### ❌ שער מטבע לא מדויק

**בעיה**: המרת USD→ILS לא מדויקת.

**פתרון**:
1. הוסף מפתח ExchangeRate-API ב-`.env`:
```bash
EXCHANGE_RATE_API_KEY=your_key_here
```

2. קבל מפתח חינם:
https://www.exchangerate-api.com/

---

## 🖥️ בעיות ממשק

### ❌ גרפים לא נטענים

**בעיה**: Plotly לא נטען.

**פתרון**:
```bash
# בדוק חיבור אינטרנט:
ping cdn.plot.ly

# נסה דפדפן אחר:
# Chrome / Firefox / Safari

# נקה Cache:
Ctrl+Shift+Delete → Clear Cache

# פתח Console (F12) וחפש שגיאות
```

---

### ❌ עיצוב שבור / CSS לא נטען

**בעיה**: קבצי CSS לא נמצאים.

**פתרון**:
```bash
# ודא שהקבצים קיימים:
ls static/css/style.css
ls static/js/app.js

# רענן עם Ctrl+Shift+R (hard reload)

# בדוק Console (F12) לשגיאות 404
```

---

### ❌ כפתורים לא עובדים

**בעיה**: JavaScript error.

**פתרון**:
```bash
# פתח Console (F12)
# חפש שגיאות אדומות

# נסה דפדפן אחר

# ודא ש-JavaScript מופעל בדפדפן
```

---

### ❌ טקסט בעברית הפוך

**בעיה**: RTL לא עובד.

**פתרון**:
קובץ HTML צריך לכלול:
```html
<html lang="he" dir="rtl">
```

אם זה לא עוזר:
```css
/* static/css/style.css */
body {
    direction: rtl;
    text-align: right;
}
```

---

## ⚡ בעיות ביצועים

### ❌ המערכת איטית

**סיבות אפשריות**:
1. חיבור אינטרנט איטי
2. הרבה מניות לסרוק
3. AI Agent איטי

**פתרון**:

**1. הקטן רשימת מניות**:
```json
// config/stocks.json
{
  "israeli_stocks": ["TEVA.TA", "NICE.TA"],
  "us_stocks": ["NVDA", "TSLA", "AAPL"]
}
```

**2. החלף ל-Agent מהיר**:
- ChatGPT: הכי מהיר
- Gemini: בינוני
- Perplexity: איטי יותר (אבל עם חיפוש)

**3. שדרג חיבור**:
```bash
# בדוק מהירות:
speedtest-cli
```

---

### ❌ שרת קורס / נתקע

**בעיה**: Flask crash.

**פתרון**:
```bash
# הסתכל על השגיאות בטרמינל

# הרץ מחדש:
Ctrl+C
bash run.sh

# אם זה קורה הרבה:
# בדוק logs ב-Console
# או הרץ:
python test_system.py
```

---

### ❌ זיכרון גבוה / CPU גבוה

**בעיה**: המערכת צורכת הרבה משאבים.

**פתרון**:
```bash
# בדוק צריכה:
# Mac:
top -o cpu

# Linux:
htop

# Windows:
Task Manager

# אם זה גבוה מדי:
# 1. הקטן מספר מניות
# 2. סגור טאבים אחרים
# 3. רסטארט למחשב
```

---

## 🛠️ כלים לדיאגנוסטיקה

### בדיקת מערכת מלאה

```bash
python test_system.py
```

זה יבדוק:
- ✅ חבילות Python
- ✅ מפתחות API
- ✅ מודולים
- ✅ חיבור לנתוני שוק
- ✅ המרת מטבע

---

### בדיקת API ידנית

```bash
# בדוק OpenAI:
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_KEY"

# בדוק Gemini:
curl "https://generativelanguage.googleapis.com/v1/models?key=YOUR_KEY"

# בדוק Perplexity:
curl https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer YOUR_KEY"
```

---

### בדיקת נתוני שוק

```python
# פתח Python console:
python3

# בדוק yfinance:
import yfinance as yf
ticker = yf.Ticker("NVDA")
print(ticker.info['currentPrice'])
```

---

## 📞 עזרה נוספת

### לא מצאת פתרון?

1. **חפש ב-FAQ**: [FAQ.md](FAQ.md)
2. **קרא דוקומנטציה**: [README.md](README.md)
3. **בדוק Issues**: GitHub Issues
4. **פתח Issue חדש** עם:
   - תיאור הבעיה
   - מה ניסית
   - הודעות שגיאה
   - Screenshots

---

### מידע שימושי לתמיכה

כשאתה מבקש עזרה, צרף:

```bash
# גרסת Python:
python3 --version

# גרסת pip:
pip --version

# רשימת חבילות:
pip list

# מערכת הפעלה:
uname -a  # Mac/Linux
systeminfo  # Windows

# הודעות שגיאה:
# העתק את כל השגיאה מהטרמינל
```

---

## 🎯 Checklist מהיר

כשיש בעיה, בדוק:

- [ ] Python 3.8+ מותקן?
- [ ] נמצא בתיקייה הנכונה?
- [ ] סביבה וירטואלית פעילה?
- [ ] חבילות מותקנות? (`pip list`)
- [ ] קובץ `.env` קיים?
- [ ] יש מפתח API תקין?
- [ ] חיבור אינטרנט פעיל?
- [ ] שעות מסחר?
- [ ] פורט 5000 פנוי?
- [ ] Console (F12) נקי משגיאות?

---

## 💡 עצות כלליות

### טיפ 1: רסטארט פותר 80% מהבעיות
```bash
# סגור הכל
# הפעל מחדש:
bash run.sh
```

### טיפ 2: קרא שגיאות בקפידה
רוב השגיאות מסבירות בדיוק מה הבעיה.

### טיפ 3: גוגל זה חבר
העתק את השגיאה ל-Google - בדרך כלל יש פתרון.

### טיפ 4: השתמש ב-Console
F12 בדפדפן → Console → תראה שגיאות JavaScript

### טיפ 5: נקה Cache
לפעמים דפדפן "זוכר" גרסה ישנה.

---

**עדיין תקוע?** → [FAQ.md](FAQ.md) או פתח Issue בגיטהאב!

---

*בנוי עם ❤️ וסבלנות רבה 🛠️*
