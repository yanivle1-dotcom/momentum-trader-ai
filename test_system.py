#!/usr/bin/env python3
"""
Test script to verify system components
"""
import os
import sys
from dotenv import load_dotenv

print("🧪 Testing Momentum Trader AI Components...\n")

# Load environment
load_dotenv()

# Test 1: Check Python packages
print("1️⃣ Testing Python packages...")
try:
    import flask
    import yfinance
    import pandas
    import pandas_ta
    print("   ✅ All required packages installed\n")
except ImportError as e:
    print(f"   ❌ Missing package: {e}\n")
    print("   Run: pip install -r requirements.txt\n")
    sys.exit(1)

# Test 2: Check API keys
print("2️⃣ Checking API keys...")
has_key = False

if os.getenv('OPENAI_API_KEY'):
    print("   ✅ OpenAI API key found")
    has_key = True

if os.getenv('GEMINI_API_KEY'):
    print("   ✅ Gemini API key found")
    has_key = True

if os.getenv('PERPLEXITY_API_KEY'):
    print("   ✅ Perplexity API key found")
    has_key = True

if not has_key:
    print("   ⚠️  No API keys found!")
    print("   Add at least one API key to .env file\n")
else:
    print()

# Test 3: Check modules
print("3️⃣ Testing custom modules...")
sys.path.append('src')

try:
    from agents import OpenAIAgent, GeminiAgent, PerplexityAgent
    print("   ✅ AI agents module OK")
except ImportError as e:
    print(f"   ❌ Agents module error: {e}")

try:
    from data import MarketDataFetcher, CurrencyConverter
    print("   ✅ Data module OK")
except ImportError as e:
    print(f"   ❌ Data module error: {e}")

try:
    from analysis import RossCameronAnalyzer
    print("   ✅ Analysis module OK")
except ImportError as e:
    print(f"   ❌ Analysis module error: {e}")

print()

# Test 4: Test market data
print("4️⃣ Testing market data fetch...")
try:
    from data import MarketDataFetcher
    fetcher = MarketDataFetcher()
    data = fetcher.get_current_data('AAPL')

    if data.get('data_available'):
        print(f"   ✅ Successfully fetched AAPL data")
        print(f"      Price: ${data['current_price']}")
        print(f"      Change: {data['change_percent']:.2f}%")
    else:
        print(f"   ⚠️  Data fetch returned no data")
except Exception as e:
    print(f"   ❌ Market data error: {e}")

print()

# Test 5: Test currency converter
print("5️⃣ Testing currency converter...")
try:
    from data import CurrencyConverter
    converter = CurrencyConverter()
    rate = converter.get_usd_to_ils_rate()
    print(f"   ✅ USD/ILS rate: {rate:.2f}")
    print(f"      $100 = ₪{converter.usd_to_ils(100):.2f}")
except Exception as e:
    print(f"   ❌ Currency converter error: {e}")

print()

# Summary
print("╔═══════════════════════════════════════════════╗")
print("║            System Check Complete              ║")
print("╚═══════════════════════════════════════════════╝")
print()

if has_key:
    print("✅ System is ready!")
    print()
    print("To start the application:")
    print("   cd src/web && python app.py")
    print()
    print("Then open: http://localhost:5000")
else:
    print("⚠️  Add API keys to .env before running")
    print()
    print("Get API keys from:")
    print("   OpenAI: https://platform.openai.com/api-keys")
    print("   Gemini: https://makersuite.google.com/app/apikey")
    print("   Perplexity: https://www.perplexity.ai/settings/api")

print()
