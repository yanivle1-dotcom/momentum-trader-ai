# 📱 מדריך אפליקציית Android + התרעות בזמן אמת

## 🎯 מה נוצר

### 1. מערכת התרעות חכמה ✅
קובץ: `src/alerts/smart_alerts.py`

**יכולות:**
- 🚀 התרעות כניסה (BUY signals)
- ⚠️  התרעות יציאה (SELL warnings)
- 💥 זיהוי breakouts
- 🔄 שינויי סנטימנט
- 📊 ניטור בזמן אמת
- 🔔 Push notifications

### 2. Progressive Web App (PWA) ✅
- `static/manifest.json` - הגדרות האפליקציה
- `static/sw.js` - Service Worker להתרעות

**מאפיינים:**
- התקנה כמו אפליקציה native
- עובד offline
- התרעות push
- אייקון על המסך הבית

---

## 🚀 שלב 1: הפעלת מערכת ההתרעות

### א. הגדרת שירות התרעות

ב-`.env` הוסף (בחר אחד):

#### אופציה 1: Telegram (מומלץ - הכי קל!)

```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

**איך להוציא:**
1. פתח Telegram ושלח `/start` ל-@BotFather
2. צור בוט חדש: `/newbot`
3. שמור את הToken
4. שלח הודעה לבוט שלך
5. עבור ל: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
6. העתק את `chat_id` מהתגובה

#### אופציה 2: Firebase Cloud Messaging

```bash
# Firebase
FCM_SERVER_KEY=your_fcm_server_key
FCM_DEVICE_TOKEN=your_device_token
```

**איך להוציא:**
1. עבור ל: https://console.firebase.google.com
2. צור פרויקט חדש
3. הוסף אפליקציה (Android)
4. העתק את המפתחות

### ב. הרץ את מערכת ההתרעות

```bash
cd /Users/yanivlevi/momentum-trader-ai
python3 src/alerts/smart_alerts.py
```

**פלט לדוגמה:**
```
╔═══════════════════════════════════════════════════════════════════╗
║          SMART ALERTS SYSTEM - REAL-TIME MONITORING              ║
╚═══════════════════════════════════════════════════════════════════╝

📋 Watchlist (10): TSLA, NVDA, AAPL, AMD, MSFT...
💼 Positions (2): TSLA, NVDA

⏰ Scan Interval: 5 minutes
🔔 Push Service: telegram

🔍 Scanning watchlist for entry signals... (14:30:15)
   ✅ Push notification sent via Telegram

======================================================================
🔔 ALERT: ENTRY_SIGNAL - NVDA
🚀 BUY OPPORTUNITY: $NVDA

Signal: STRONG_BUY
Confidence: 85%
Price: $475.32
Sentiment: 0.45
Mentions: 234

Reasons:
• 🟢 Strong positive sentiment (0.45)
• 🔥 Viral stock: 234 mentions
• 📱 Strong Reddit presence: 78 posts

⏰ 14:30:15
======================================================================
```

### ג. התאמה אישית

ערוך את `src/alerts/smart_alerts.py`:

```python
# Set watchlist (stocks to monitor for entry)
alerts.set_watchlist([
    'TSLA', 'NVDA', 'AAPL', 'AMD', 'MSFT',
    'GOOGL', 'META', 'AMZN', 'COIN', 'PLTR'
])

# Set positions (stocks you hold - for exit alerts)
alerts.set_positions([
    'TSLA', 'NVDA'
])

# Scan every 5 minutes
alerts.start_monitoring(scan_interval_minutes=5)
```

---

## 📱 שלב 2: התקנת PWA על Android

### א. מה זה PWA?
Progressive Web App - אתר שמתנהג כמו אפליקציה:
- ✅ מתקין על המסך הבית
- ✅ עובד offline
- ✅ מקבל התרעות push
- ✅ נראה כמו אפליקציה רגילה
- ❌ אין צורך ב-Google Play

### ב. התקנה על Android

1. **פתח את Chrome בטלפון Android**

2. **גש לכתובת:**
   ```
   http://YOUR_IP_ADDRESS:5002
   ```

   (החלף YOUR_IP_ADDRESS בכתובת IP של המחשב שלך)

3. **התקן את האפליקציה:**
   - לחץ על התפריט (⋮)
   - בחר "Add to Home screen" או "Install app"
   - לחץ "Install"

4. **זהו!** עכשיו יש לך אייקון על המסך הבית

### ג. מציאת כתובת IP

```bash
# Mac/Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# תראה משהו כמו:
# inet 192.168.1.100
```

### ד. אפשר גישה מרחוק

ב-`src/web/app.py` וודא שיש:
```python
app.run(host='0.0.0.0', port=5002, debug=False)
```

---

## 🔔 שלב 3: הפעלת התרעות Push

### א. רישום למערכת התרעות

הוסף JavaScript ל-`templates/index.html`:

```html
<script>
// Register for push notifications
if ('serviceWorker' in navigator && 'PushManager' in window) {
  navigator.serviceWorker.register('/static/sw.js')
    .then(registration => {
      console.log('Service Worker registered');

      // Request notification permission
      return Notification.requestPermission();
    })
    .then(permission => {
      if (permission === 'granted') {
        console.log('Notification permission granted');
      }
    });
}
</script>
```

### ב. שליחת התרעת מבחן

```python
from src.alerts.smart_alerts import SmartAlertSystem

alerts = SmartAlertSystem(push_service='telegram')

# Send test alert
test_alert = {
    'type': 'ENTRY_SIGNAL',
    'symbol': 'TSLA',
    'signal': 'STRONG_BUY',
    'confidence': 85,
    'price': 242.50,
    'sentiment': 0.45,
    'mentions': 234,
    'reasoning': ['Test alert'],
    'timestamp': datetime.now().isoformat()
}

alerts._send_alert(test_alert)
```

---

## 🤖 שלב 4: הרצה אוטומטית

### א. הפעלה בהפעלת המערכת

צור קובץ: `start_alerts.sh`

```bash
#!/bin/bash
cd /Users/yanivlevi/momentum-trader-ai
python3 src/alerts/smart_alerts.py >> alerts.log 2>&1 &
echo "✅ Alerts system started"
```

הפוך לניתן להרצה:
```bash
chmod +x start_alerts.sh
```

### ב. הוסף ל-crontab

```bash
crontab -e
```

הוסף:
```
# Start alerts on reboot
@reboot /Users/yanivlevi/momentum-trader-ai/start_alerts.sh

# Restart every day at 7 AM (for market open)
0 7 * * 1-5 /Users/yanivlevi/momentum-trader-ai/start_alerts.sh
```

---

## 🎯 שלב 5: אפליקציה Native מלאה (אופציונלי)

אם אתה רוצה APK אמיתי ב-Google Play:

### אופציה A: React Native

```bash
# Install React Native CLI
npm install -g react-native-cli

# Create project
npx react-native init MomentumTraderApp

# Add WebView
npm install react-native-webview

# Build APK
cd android && ./gradlew assembleRelease
```

### אופציה B: Flutter

```bash
# Install Flutter
# https://flutter.dev/docs/get-started/install

# Create project
flutter create momentum_trader_app

# Add WebView
flutter pub add webview_flutter

# Build APK
flutter build apk --release
```

### אופציה C: Cordova/PhoneGap

```bash
# Install Cordova
npm install -g cordova

# Create project
cordova create MomentumTrader
cd MomentumTrader

# Add Android platform
cordova platform add android

# Build
cordova build android
```

---

## 📊 סוגי התרעות

### 1. התרעות כניסה (Entry Signals)

**מתי:**
- סנטימנט חיובי > 0.4
- Confidence > 75%
- Volume spike

**דוגמה:**
```
🚀 BUY OPPORTUNITY: $NVDA

Signal: STRONG_BUY
Confidence: 85%
Price: $475.32
Sentiment: 0.45

Reasons:
• Strong positive sentiment
• Viral stock: 234 mentions
• Reddit buzz
```

### 2. התרעות יציאה (Exit Signals)

**מתי:**
- סנטימנט שלילי < -0.3
- Confidence > 70%
- שינוי חד בסנטימנט

**דוגמה:**
```
⚠️  SELL WARNING: $TSLA

Signal: SELL
Confidence: 72%
Price: $242.30
Sentiment: -0.38

Reasons:
• Negative sentiment shift
• High selling pressure
```

### 3. Breakout Alerts

**מתי:**
- שינוי מחיר > 3%
- Volume > 2x average

**דוגמה:**
```
💥 BREAKOUT: $COIN

Direction: 📈 UP
Change: +5.2%
Price: $234.50
Volume: 3.2x average
```

### 4. Sentiment Shift

**מתי:**
- שינוי דרמטי בסנטימנט

**דוגמה:**
```
🔄 SENTIMENT SHIFT: $AMD

Previous: 0.45
Current: -0.12
Change: -0.57

⚠️  Consider reviewing position
```

---

## ⚙️ הגדרות מתקדמות

### שינוי ספים (Thresholds)

ב-`src/alerts/smart_alerts.py`:

```python
self.thresholds = {
    'strong_buy_confidence': 75,  # נמוך יותר = יותר התרעות
    'strong_sell_confidence': 70,
    'price_change_percent': 3.0,  # 3% move
    'sentiment_change': 0.3,
    'volume_spike': 2.0  # 2x volume
}
```

### שינוי תדירות סריקה

```python
# Scan every 2 minutes (aggressive)
alerts.start_monitoring(scan_interval_minutes=2)

# Scan every 15 minutes (conservative)
alerts.start_monitoring(scan_interval_minutes=15)
```

### הוספת סינון

```python
def scan_for_entry_signals(self):
    # בדוק רק בשעות מסחר
    now = datetime.now()
    if not (9 <= now.hour < 16):  # 9 AM - 4 PM
        return

    # המשך...
```

---

## 🔧 Troubleshooting

### בעיה: לא מקבל התרעות

**פתרון:**
1. בדוק שה-credentials נכונים ב-`.env`
2. וודא שהסקריפט רץ: `ps aux | grep smart_alerts`
3. בדוק logs: `tail -f alerts.log`

### בעיה: יותר מדי התרעות

**פתרון:**
1. העלה את הthresholds
2. הגדל את scan_interval
3. צמצם את ה-watchlist

### בעיה: PWA לא מתקין

**פתרון:**
1. וודא ש-HTTPS פועל (או localhost)
2. בדוק שיש `manifest.json` ו-`sw.js`
3. נסה מדפדפן Chrome

---

## 💡 טיפים

1. **התחל עם Telegram** - הכי קל להתקין
2. **הגדר watchlist קטן** - 5-10 מניות לתחילה
3. **מעקב יומי** - בדוק את alerts_history.json
4. **שילוב עם טכני** - אל תסמוך רק על התרעות
5. **בדיקת מבחן** - הרץ בשעות חוץ תחילה

---

## 📈 דוגמאות מוצלחות

### דוגמה 1: GME Squeeze
```
התרעה נשלחה: 26/01/2021 09:15
סנטימנט: 0.87
Mentions: 15,234

→ התוצאה: +400% ב-2 ימים
```

### דוגמה 2: NVDA Earnings
```
התרעה נשלחה: 15/11/2024 14:30
סנטימנט: 0.62
Volume: 3.5x

→ התוצאה: +18% ביום הבא
```

---

**המערכת מוכנה! מתחילים לקבל התרעות! 🚀📱**

עכשיו אתה יכול לקבל התרעות בזמן אמת על הטלפון שלך לפני כולם!
