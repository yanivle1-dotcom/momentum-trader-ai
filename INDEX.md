# 📖 מדריך לקבצי הפרויקט

## 🚀 קבצים ראשונים - התחל כאן!

| קובץ | תיאור | למי זה |
|------|--------|---------|
| [QUICKSTART.md](QUICKSTART.md) | התחלה תוך 5 דקות | כולם! |
| [README.md](README.md) | מדריך מלא למערכת | מתחילים |
| [FAQ.md](FAQ.md) | שאלות נפוצות | תשובות מהירות |

---

## 📚 תיעוד למידה

| קובץ | תיאור | תוכן |
|------|--------|------|
| [ROSS_CAMERON_GUIDE.md](ROSS_CAMERON_GUIDE.md) | מדריך מקיף לשיטת Ross Cameron | 5 סט-אפים, ניהול סיכון, טיפים |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | סיכום מלא של הפרויקט | ארכיטקטורה, תכונות, סטטיסטיקות |
| [ARCHITECTURE.md](ARCHITECTURE.md) | תיעוד טכני מפורט | Data flow, שכבות, דיאגרמות |

---

## 🔧 תיעוד טכני

| קובץ | תיאור | למי זה |
|------|--------|---------|
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | תיעוד API מלא | מפתחים |
| [requirements.txt](requirements.txt) | רשימת תלויות Python | התקנה |
| [.env.example](.env.example) | דוגמת קובץ הגדרות | הגדרה ראשונית |

---

## 🏃 קבצי הרצה

| קובץ | פקודה | מה זה עושה |
|------|-------|-------------|
| [setup.sh](setup.sh) | `bash setup.sh` | התקנה אוטומטית |
| [run.sh](run.sh) | `bash run.sh` | הפעלת המערכת |
| [test_system.py](test_system.py) | `python test_system.py` | בדיקת הרכיבים |

---

## ⚙️ קבצי תצורה

| קובץ/תיקייה | מה שם | מתי לערוך |
|-------------|--------|-----------|
| `.env` | מפתחות API | **פעם אחת בהתחלה** |
| `config/stocks.json` | רשימת מניות וקריטריונים | כשרוצה לשנות מניות |
| `.gitignore` | מניעת העלאה של קבצים רגישים | אל תשנה! |

---

## 🐍 קוד Python - Backend

### src/agents/ - AI Agents
| קובץ | מה בתוכו |
|------|----------|
| `base_agent.py` | Base class לכל ה-agents |
| `openai_agent.py` | ChatGPT integration |
| `gemini_agent.py` | Google Gemini integration |
| `perplexity_agent.py` | Perplexity AI integration |
| `__init__.py` | Package initialization |

### src/data/ - נתוני שוק
| קובץ | מה בתוכו |
|------|----------|
| `market_data.py` | משיכת מחירים, אינדיקטורים, סריקה |
| `currency_converter.py` | המרת USD→ILS |
| `__init__.py` | Package initialization |

### src/analysis/ - ניתוח טכני
| קובץ | מה בתוכו |
|------|----------|
| `ross_cameron_setups.py` | זיהוי 5 סט-אפים של Ross |
| `__init__.py` | Package initialization |

### src/web/ - שרת ווב
| קובץ | מה בתוכו |
|------|----------|
| `app.py` | Flask server + 6 API endpoints |
| `__init__.py` | Package initialization |

---

## 🌐 קוד Frontend

### templates/
| קובץ | מה בתוכו |
|------|----------|
| `index.html` | דשבורד ראשי בעברית |

### static/css/
| קובץ | מה בתוכו |
|------|----------|
| `style.css` | כל העיצוב של הדשבורד |

### static/js/
| קובץ | מה בתוכו |
|------|----------|
| `app.js` | לוגיקה, AJAX, גרפים (Plotly) |

---

## 📂 מבנה מלא

```
momentum-trader-ai/
│
├── 📄 קבצי תיעוד (קרא אותי!)
│   ├── INDEX.md (הקובץ הזה)
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── FAQ.md
│   ├── ROSS_CAMERON_GUIDE.md
│   ├── PROJECT_SUMMARY.md
│   ├── ARCHITECTURE.md
│   └── API_DOCUMENTATION.md
│
├── ⚙️ קבצי הגדרה
│   ├── requirements.txt
│   ├── .env.example
│   ├── .env (תיצור בעצמך)
│   └── .gitignore
│
├── 🏃 סקריפטים
│   ├── setup.sh
│   ├── run.sh
│   └── test_system.py
│
├── 🔧 config/
│   └── stocks.json
│
├── 🐍 src/
│   ├── __init__.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py
│   │   ├── openai_agent.py
│   │   ├── gemini_agent.py
│   │   └── perplexity_agent.py
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── market_data.py
│   │   └── currency_converter.py
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── ross_cameron_setups.py
│   │
│   └── web/
│       ├── __init__.py
│       └── app.py
│
├── 🌐 templates/
│   └── index.html
│
└── 📁 static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

---

## 🎯 מתי לקרוא מה?

### 📌 אני רוצה להתחיל מהר!
→ [QUICKSTART.md](QUICKSTART.md)

### 📌 אני רוצה להבין את המערכת
→ [README.md](README.md)

### 📌 יש לי שאלה ספציפית
→ [FAQ.md](FAQ.md)

### 📌 אני רוצה ללמוד את שיטת Ross Cameron
→ [ROSS_CAMERON_GUIDE.md](ROSS_CAMERON_GUIDE.md)

### 📌 אני רוצה להבין איך זה עובד טכנית
→ [ARCHITECTURE.md](ARCHITECTURE.md)

### 📌 אני רוצה להשתמש ב-API
→ [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

### 📌 אני רוצה לראות סיכום של הכל
→ [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

### 📌 יש לי בעיה טכנית
→ [FAQ.md](FAQ.md) → פתרון בעיות

### 📌 אני רוצה לשנות משהו בקוד
1. [ARCHITECTURE.md](ARCHITECTURE.md) - הבן את המבנה
2. קרא את הקוד הרלוונטי (רשום למעלה)
3. בצע שינויים
4. הרץ `python test_system.py`

---

## 🔍 חיפוש מהיר

### אני מחפש...

**...איך להתקין**
→ [QUICKSTART.md](QUICKSTART.md) או [README.md](README.md)

**...מה זה Gap & Go**
→ [ROSS_CAMERON_GUIDE.md](ROSS_CAMERON_GUIDE.md)

**...איך לשנות מניות**
→ [FAQ.md](FAQ.md) או ערוך `config/stocks.json`

**...איך לקבל API key**
→ [QUICKSTART.md](QUICKSTART.md) - יש קישורים

**...למה אין מניות בסריקה**
→ [FAQ.md](FAQ.md) - שאלות נפוצות

**...איך הנתונים זורמים במערכת**
→ [ARCHITECTURE.md](ARCHITECTURE.md) - Data Flow

**...מה זה RVOL / VWAP / R:R**
→ [FAQ.md](FAQ.md) או [ROSS_CAMERON_GUIDE.md](ROSS_CAMERON_GUIDE.md)

**...איך לשנות את העיצוב**
→ ערוך `static/css/style.css`

**...איך להוסיף סט-אפ חדש**
→ ערוך `src/analysis/ross_cameron_setups.py`

**...איך לתרום לפרויקט**
→ [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - תרומה

---

## 📊 רמות קושי

### 🟢 מתחיל (ללא ידע בתכנות)
קרא בסדר הזה:
1. [QUICKSTART.md](QUICKSTART.md)
2. [FAQ.md](FAQ.md)
3. [ROSS_CAMERON_GUIDE.md](ROSS_CAMERON_GUIDE.md)
4. התחל להשתמש!

### 🟡 בינוני (יודע Python בסיסי)
קרא בסדר הזה:
1. [README.md](README.md)
2. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
3. [ARCHITECTURE.md](ARCHITECTURE.md)
4. התחל לשנות ולהתאים!

### 🔴 מתקדם (מפתח מנוסה)
קרא בסדר הזה:
1. [ARCHITECTURE.md](ARCHITECTURE.md)
2. [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
3. קפוץ ישר לקוד!
4. תרום לפרויקט 😊

---

## 🗺️ מפת מסלול

```
START HERE
    │
    ├─→ רוצה להתחיל מהר?
    │   └─→ QUICKSTART.md → run!
    │
    ├─→ רוצה להבין לעומק?
    │   └─→ README.md → ROSS_CAMERON_GUIDE.md
    │
    ├─→ יש בעיה?
    │   └─→ FAQ.md → פתרון
    │
    ├─→ מפתח?
    │   └─→ ARCHITECTURE.md → API_DOCUMENTATION.md
    │
    └─→ רוצה סיכום?
        └─→ PROJECT_SUMMARY.md
```

---

## 💡 טיפים לניווט

### טיפ 1: השתמש ב-Ctrl+F (Cmd+F)
כל הקבצים ארוכים - חפש מילת מפתח!

### טיפ 2: התחל מה-FAQ
רוב השאלות כבר נענו שם.

### טיפ 3: ה-README הוא המקור המרכזי
כשלא בטוח - חזור ל-README.

### טיפ 4: הקוד מתועד
יש הערות בקוד - קרא אותן!

### טיפ 5: יש דוגמאות
כמעט בכל קובץ יש דוגמאות שימוש.

---

## 📞 עזרה נוספת

לא מצאת מה שחיפשת?

1. ✅ חפש ב-[FAQ.md](FAQ.md)
2. ✅ חפש בקובץ הרלוונטי (Ctrl+F)
3. ✅ בדוק Issues בגיטהאב
4. ✅ פתח Issue חדש

---

## 🎓 מסלול למידה מומלץ

### שבוע 1: התקנה והבנה
- [ ] קרא QUICKSTART.md
- [ ] התקן את המערכת
- [ ] הרץ את test_system.py
- [ ] הפעל את המערכת
- [ ] נסה לסרוק מניות

### שבוע 2: למידת השיטה
- [ ] קרא ROSS_CAMERON_GUIDE.md במלואו
- [ ] צפה בסרטונים של Warrior Trading
- [ ] נתח 10 מניות במערכת
- [ ] רשום את התובנות

### שבוע 3: התאמה אישית
- [ ] שנה רשימת מניות
- [ ] התנסה עם AI agents שונים
- [ ] קרא FAQ.md
- [ ] נסה קריטריונים שונים

### שבוע 4: התעמקות
- [ ] קרא ARCHITECTURE.md
- [ ] הבן את מבנה הקוד
- [ ] נסה לשנות משהו קטן
- [ ] תרגל Paper Trading

---

## 🏆 מטרות ציון דרך

- ✅ התקנה הצליחה
- ✅ הבנת הסט-אפים
- ✅ סריקה ראשונה עבדה
- ✅ ניתוח ראשון עבד
- ✅ הבנת Risk:Reward
- ✅ שינוי הגדרות ראשון
- ✅ הוספת מניה ראשונה
- ✅ שבוע של Paper Trading
- ✅ 50 טריידים מדומים
- 🎯 **מוכן ל-Live Trading!**

---

**בהצלחה! 🚀**

*אם הקובץ הזה עזר לך, שתף אותו!*

---

נבנה עם ❤️ לקהילה 🇮🇱
