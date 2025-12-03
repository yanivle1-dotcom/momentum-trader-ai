# 🚀 התחלה מהירה - 5 דקות

## צעד 1: התקנה (2 דקות)

```bash
cd momentum-trader-ai
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

## צעד 2: הגדר API Keys (2 דקות)

```bash
cp .env.example .env
nano .env  # או פתח בעורך טקסט
```

הוסף **לפחות** מפתח אחד:

```bash
OPENAI_API_KEY=sk-proj-xxxxx...
# או
GEMINI_API_KEY=xxxxx...
# או
PERPLEXITY_API_KEY=pplx-xxxxx...
```

### איפה להשיג?

**OpenAI:** https://platform.openai.com/api-keys
**Gemini:** https://makersuite.google.com/app/apikey
**Perplexity:** https://www.perplexity.ai/settings/api

## צעד 3: הפעל! (1 דקה)

```bash
cd src/web
python app.py
```

פתח דפדפן: **http://localhost:5000**

## זהו! 🎉

- לחץ **"סרוק מניות"**
- בחר מניה לניתוח מלא
- קבל סט-אפים והמלצות

---

**צריך עזרה?** קרא את [README.md](README.md) המלא
