# 🔌 API Documentation

## Base URL
```
http://localhost:5000
```

---

## Endpoints

### 1. GET `/`
**Dashboard Page**

Returns the main HTML dashboard.

**Response:** HTML page

---

### 2. GET `/api/scan`
**Scan Stocks for Momentum**

Scans all configured stocks for momentum setups based on criteria.

**Query Parameters:** None

**Response:**
```json
{
  "success": true,
  "stocks": [
    {
      "symbol": "NVDA",
      "market": "US",
      "current_price": 450.25,
      "current_price_ils": 1620.90,
      "currency": "USD",
      "change": 12.50,
      "change_percent": 2.85,
      "volume": 45000000,
      "avg_volume": 20000000,
      "rvol": 2.25,
      "gap_percent": 3.5,
      "day_high": 452.00,
      "day_low": 445.00,
      "vwap": 448.50,
      "ema_9": 447.00,
      "ema_20": 440.00,
      "rsi": 65.5
    }
  ],
  "usd_ils_rate": 3.60,
  "timestamp": "2024-01-15T10:30:00+02:00"
}
```

---

### 3. POST `/api/analyze/<symbol>`
**Analyze Specific Stock**

Get detailed analysis including Ross Cameron setups and AI insights.

**Path Parameters:**
- `symbol` (string) - Stock ticker (e.g., "NVDA", "TEVA.TA")

**Body:**
```json
{
  "agent": "chatgpt"  // or "gemini" or "perplexity"
}
```

**Response:**
```json
{
  "success": true,
  "symbol": "NVDA",
  "market": "US",
  "stock_data": {
    "symbol": "NVDA",
    "current_price": 450.25,
    "current_price_ils": 1620.90,
    "currency": "USD",
    "change_percent": 2.85,
    "rvol": 2.25,
    "gap_percent": 3.5,
    "vwap": 448.50,
    "ema_9": 447.00,
    "ema_20": 440.00,
    "rsi": 65.5,
    "timestamp": "2024-01-15T10:30:00+02:00"
  },
  "setup_analysis": {
    "setup_type": "Gap & Go",
    "setup_valid": true,
    "criteria_met": [
      "גאפ משמעותי: 3.5%",
      "RVOL גבוה: 2.3x",
      "מחיר מעל VWAP",
      "מחיר מעל EMA9"
    ],
    "criteria_failed": [],
    "entry_point": 449.50,
    "stop_loss": 446.00,
    "targets": [454.00, 459.50, 468.00],
    "risk_reward": "1:2.7",
    "confidence": "high"
  },
  "ai_analysis": {
    "agent": "ChatGPT",
    "model": "gpt-4-turbo-preview",
    "catalyst": "חברת NVIDIA הכריזה על שבב AI חדש...",
    "catalyst_sources": [
      "https://...",
      "https://..."
    ],
    "setup_type": "Gap & Go",
    "setup_valid": true,
    "analysis": "ניתוח מפורט בעברית...",
    "why_now": "מומנטום חזק עם קטליסט ברור...",
    "risk_level": "בינוני",
    "warnings": [
      "שים לב לנפח בפריצה",
      "RSI גבוה - עקוב אחרי אינדיקציות לסיום המומנטום"
    ],
    "timestamp": "2024-01-15T10:30:00+02:00"
  },
  "usd_ils_rate": 3.60,
  "timestamp": "2024-01-15T10:30:00+02:00"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Stock data not available"
}
```

---

### 4. GET `/api/chart/<symbol>`
**Get Chart Data**

Returns OHLCV data with technical indicators for charting.

**Path Parameters:**
- `symbol` (string) - Stock ticker

**Query Parameters:**
- `period` (string, optional) - Data period. Default: "5d"
  - Options: "1d", "5d", "1mo", "3mo", "6mo", "1y"

**Example:**
```
GET /api/chart/NVDA?period=5d
```

**Response:**
```json
{
  "success": true,
  "symbol": "NVDA",
  "data": {
    "timestamps": ["2024-01-15 09:30", "2024-01-15 09:35", ...],
    "open": [445.00, 446.50, ...],
    "high": [447.00, 448.00, ...],
    "low": [444.50, 446.00, ...],
    "close": [446.50, 447.50, ...],
    "volume": [1000000, 950000, ...],
    "vwap": [446.00, 446.80, ...],
    "ema_9": [445.50, 446.20, ...],
    "ema_20": [440.00, 440.50, ...],
    "rsi": [62.5, 63.8, ...]
  }
}
```

---

### 5. GET `/api/agents`
**Get Available AI Agents**

Returns list of configured AI agents.

**Response:**
```json
{
  "success": true,
  "agents": [
    {
      "name": "chatgpt",
      "display_name": "ChatGPT",
      "available": true
    },
    {
      "name": "gemini",
      "display_name": "Gemini",
      "available": true
    },
    {
      "name": "perplexity",
      "display_name": "Perplexity",
      "available": true
    }
  ]
}
```

---

### 6. GET `/api/exchange-rate`
**Get Current Exchange Rate**

Returns current USD/ILS exchange rate.

**Response:**
```json
{
  "success": true,
  "rate_info": {
    "rate": 3.60,
    "source": "ExchangeRate-API",
    "timestamp": "2024-01-15T10:30:00+02:00",
    "from": "USD",
    "to": "ILS"
  }
}
```

---

## Error Responses

All endpoints may return error responses in this format:

```json
{
  "success": false,
  "error": "Error message here"
}
```

**HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found (stock/resource not found)
- `500` - Internal Server Error

---

## Rate Limits

**Market Data (Yahoo Finance):**
- No strict limit, but avoid excessive requests
- Recommended: Max 1 request per second per symbol

**AI Agents:**
- Depends on your API key tier
- OpenAI: Varies by plan
- Gemini: 60 requests/minute (free tier)
- Perplexity: Varies by plan

---

## Using the API Programmatically

### Python Example

```python
import requests

# Scan for momentum stocks
response = requests.get('http://localhost:5000/api/scan')
data = response.json()

if data['success']:
    for stock in data['stocks']:
        print(f"{stock['symbol']}: {stock['change_percent']:.2f}%")

# Analyze a specific stock
response = requests.post(
    'http://localhost:5000/api/analyze/NVDA',
    json={'agent': 'chatgpt'}
)
analysis = response.json()

if analysis['success']:
    setup = analysis['setup_analysis']
    print(f"Setup: {setup['setup_type']}")
    print(f"Entry: ${setup['entry_point']}")
    print(f"Stop: ${setup['stop_loss']}")
    print(f"Targets: {setup['targets']}")
```

### JavaScript Example

```javascript
// Scan for stocks
fetch('http://localhost:5000/api/scan')
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      data.stocks.forEach(stock => {
        console.log(`${stock.symbol}: ${stock.change_percent.toFixed(2)}%`);
      });
    }
  });

// Analyze stock
fetch('http://localhost:5000/api/analyze/NVDA', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ agent: 'chatgpt' })
})
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      console.log('Setup:', data.setup_analysis.setup_type);
      console.log('Entry:', data.setup_analysis.entry_point);
    }
  });
```

### cURL Example

```bash
# Scan stocks
curl http://localhost:5000/api/scan

# Analyze stock
curl -X POST http://localhost:5000/api/analyze/NVDA \
  -H "Content-Type: application/json" \
  -d '{"agent": "chatgpt"}'

# Get chart data
curl "http://localhost:5000/api/chart/NVDA?period=5d"
```

---

## Configuration

Stock lists and criteria can be configured in:
```
config/stocks.json
```

Example:
```json
{
  "israeli_stocks": ["TEVA.TA", "NICE.TA"],
  "us_stocks_popular_in_israel": ["NVDA", "TSLA"],
  "momentum_criteria": {
    "min_rvol": 2.0,
    "min_gap_percent": 3.0,
    "min_volume": 100000
  }
}
```

---

## Notes

- All timestamps are in ISO 8601 format with Israel timezone
- Prices are rounded to 2 decimal places
- Volume is in number of shares
- RVOL is relative to 20-day average
- RSI is 14-period
- EMAs are 9 and 20 periods on 5-minute candles

---

## Support

For issues or questions:
- Check [README.md](README.md) for setup instructions
- See [ROSS_CAMERON_GUIDE.md](ROSS_CAMERON_GUIDE.md) for trading methodology
- Open an issue on GitHub
