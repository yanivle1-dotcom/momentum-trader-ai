"""
Smart Real-time Alerts System
Monitors stocks and sends push notifications for trading opportunities
"""

import os
import sys
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import schedule
import requests

# Add parent to path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parent_dir)

from src.analysis.social_intelligence import SocialIntelligence
from src.data.market_data import MarketDataFetcher
from dotenv import load_dotenv

load_dotenv()


class SmartAlertSystem:
    """
    Real-time monitoring and alert system
    Sends push notifications for:
    - Entry signals (buy opportunities)
    - Exit signals (sell warnings)
    - News-based price movements
    - Sentiment changes
    """

    def __init__(self, push_service='firebase'):
        self.social_intel = SocialIntelligence()
        self.market_data = MarketDataFetcher()
        self.push_service = push_service

        # Alert thresholds
        self.thresholds = {
            'strong_buy_confidence': 75,
            'strong_sell_confidence': 70,
            'price_change_percent': 3.0,  # Alert on 3%+ moves
            'sentiment_change': 0.3,  # Alert on big sentiment shifts
            'volume_spike': 2.0  # 2x average volume
        }

        # Track state
        self.watchlist = []
        self.positions = []
        self.last_alerts = {}  # Prevent duplicate alerts
        self.previous_state = {}  # Track previous values

    def set_watchlist(self, symbols: List[str]):
        """Set stocks to monitor for entry opportunities"""
        self.watchlist = [s.upper() for s in symbols]
        print(f"📋 Watchlist set: {', '.join(self.watchlist)}")

    def set_positions(self, symbols: List[str]):
        """Set stocks you currently hold (for exit alerts)"""
        self.positions = [s.upper() for s in symbols]
        print(f"💼 Positions set: {', '.join(self.positions)}")

    def scan_for_entry_signals(self):
        """
        Scan watchlist for BUY opportunities
        Send alert when:
        - Strong social sentiment + high confidence
        - Price breakout with volume
        - Major news catalyst
        """
        print(f"\n🔍 Scanning watchlist for entry signals... ({datetime.now().strftime('%H:%M:%S')})")

        for symbol in self.watchlist:
            try:
                # Get social intelligence
                social = self.social_intel.analyze_stock(symbol)

                # Get market data
                market = self.market_data.get_current_data(symbol)

                # Check for strong buy signal
                if (social['signal'] in ['STRONG_BUY', 'BUY'] and
                    social['confidence'] >= self.thresholds['strong_buy_confidence']):

                    alert = {
                        'type': 'ENTRY_SIGNAL',
                        'symbol': symbol,
                        'signal': social['signal'],
                        'confidence': social['confidence'],
                        'price': market.get('current_price', 0),
                        'sentiment': social['sentiment']['score'],
                        'mentions': social['sentiment']['mentions'],
                        'reasoning': social['reasoning'][:3],  # Top 3 reasons
                        'timestamp': datetime.now().isoformat()
                    }

                    self._send_alert(alert)

                # Check for price breakout
                if market.get('data_available'):
                    price_change = market.get('change_percent', 0)
                    volume_ratio = market.get('volume', 0) / market.get('avg_volume', 1) if market.get('avg_volume') else 0

                    if (abs(price_change) >= self.thresholds['price_change_percent'] and
                        volume_ratio >= self.thresholds['volume_spike']):

                        alert = {
                            'type': 'BREAKOUT',
                            'symbol': symbol,
                            'price': market['current_price'],
                            'change_percent': price_change,
                            'volume_ratio': volume_ratio,
                            'timestamp': datetime.now().isoformat()
                        }

                        self._send_alert(alert)

            except Exception as e:
                print(f"   ❌ Error scanning {symbol}: {e}")

    def scan_for_exit_signals(self):
        """
        Monitor positions for SELL warnings
        Send alert when:
        - Negative sentiment shift
        - Price drop with volume
        - Bad news
        """
        print(f"\n⚠️  Scanning positions for exit signals... ({datetime.now().strftime('%H:%M:%S')})")

        for symbol in self.positions:
            try:
                # Get social intelligence
                social = self.social_intel.analyze_stock(symbol)

                # Get market data
                market = self.market_data.get_current_data(symbol)

                # Check for sell signal
                if (social['signal'] in ['STRONG_SELL', 'SELL'] and
                    social['confidence'] >= self.thresholds['strong_sell_confidence']):

                    alert = {
                        'type': 'EXIT_SIGNAL',
                        'symbol': symbol,
                        'signal': social['signal'],
                        'confidence': social['confidence'],
                        'price': market.get('current_price', 0),
                        'sentiment': social['sentiment']['score'],
                        'reasoning': social['reasoning'][:3],
                        'timestamp': datetime.now().isoformat()
                    }

                    self._send_alert(alert)

                # Check for sentiment shift
                prev_sentiment = self.previous_state.get(f"{symbol}_sentiment", 0)
                current_sentiment = social['sentiment']['score']

                if prev_sentiment > 0.3 and current_sentiment < 0:
                    alert = {
                        'type': 'SENTIMENT_SHIFT',
                        'symbol': symbol,
                        'previous_sentiment': prev_sentiment,
                        'current_sentiment': current_sentiment,
                        'change': current_sentiment - prev_sentiment,
                        'timestamp': datetime.now().isoformat()
                    }

                    self._send_alert(alert)

                # Update state
                self.previous_state[f"{symbol}_sentiment"] = current_sentiment

            except Exception as e:
                print(f"   ❌ Error scanning {symbol}: {e}")

    def _send_alert(self, alert: Dict):
        """
        Send push notification

        Supports:
        - Firebase Cloud Messaging (FCM)
        - Telegram Bot
        - Email
        - SMS (Twilio)
        """
        # Prevent duplicate alerts (within 30 minutes)
        alert_key = f"{alert['symbol']}_{alert['type']}"
        last_alert_time = self.last_alerts.get(alert_key)

        if last_alert_time:
            time_diff = (datetime.now() - last_alert_time).seconds
            if time_diff < 1800:  # 30 minutes
                print(f"   ⏭️  Skipping duplicate alert for {alert['symbol']}")
                return

        # Format message
        message = self._format_alert_message(alert)

        print(f"\n{'='*70}")
        print(f"🔔 ALERT: {alert['type']} - {alert['symbol']}")
        print(message)
        print(f"{'='*70}\n")

        # Send via configured service
        if self.push_service == 'firebase':
            self._send_firebase(alert, message)
        elif self.push_service == 'telegram':
            self._send_telegram(alert, message)
        elif self.push_service == 'email':
            self._send_email(alert, message)

        # Update last alert time
        self.last_alerts[alert_key] = datetime.now()

        # Save to alerts history
        self._save_alert_to_history(alert)

    def _format_alert_message(self, alert: Dict) -> str:
        """Format alert message for notification"""

        if alert['type'] == 'ENTRY_SIGNAL':
            return f"""
🚀 BUY OPPORTUNITY: ${alert['symbol']}

Signal: {alert['signal']}
Confidence: {alert['confidence']}%
Price: ${alert['price']:.2f}
Sentiment: {alert['sentiment']:.2f}
Mentions: {alert['mentions']}

Reasons:
{chr(10).join(['• ' + r for r in alert['reasoning']])}

⏰ {datetime.now().strftime('%H:%M:%S')}
            """.strip()

        elif alert['type'] == 'EXIT_SIGNAL':
            return f"""
⚠️  SELL WARNING: ${alert['symbol']}

Signal: {alert['signal']}
Confidence: {alert['confidence']}%
Price: ${alert['price']:.2f}
Sentiment: {alert['sentiment']:.2f}

Reasons:
{chr(10).join(['• ' + r for r in alert['reasoning']])}

⏰ {datetime.now().strftime('%H:%M:%S')}
            """.strip()

        elif alert['type'] == 'BREAKOUT':
            direction = "📈 UP" if alert['change_percent'] > 0 else "📉 DOWN"
            return f"""
💥 BREAKOUT: ${alert['symbol']}

Direction: {direction}
Change: {alert['change_percent']:+.2f}%
Price: ${alert['price']:.2f}
Volume: {alert['volume_ratio']:.1f}x average

⏰ {datetime.now().strftime('%H:%M:%S')}
            """.strip()

        elif alert['type'] == 'SENTIMENT_SHIFT':
            return f"""
🔄 SENTIMENT SHIFT: ${alert['symbol']}

Previous: {alert['previous_sentiment']:.2f}
Current: {alert['current_sentiment']:.2f}
Change: {alert['change']:.2f}

⚠️  Consider reviewing your position

⏰ {datetime.now().strftime('%H:%M:%S')}
            """.strip()

        return str(alert)

    def _send_firebase(self, alert: Dict, message: str):
        """Send via Firebase Cloud Messaging"""
        fcm_token = os.getenv('FCM_DEVICE_TOKEN')
        fcm_server_key = os.getenv('FCM_SERVER_KEY')

        if not fcm_token or not fcm_server_key:
            print("   ⚠️  FCM credentials not configured")
            return

        url = 'https://fcm.googleapis.com/fcm/send'
        headers = {
            'Authorization': f'key={fcm_server_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            'to': fcm_token,
            'notification': {
                'title': f"{alert['type']}: {alert['symbol']}",
                'body': message,
                'sound': 'default',
                'priority': 'high'
            },
            'data': alert
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                print(f"   ✅ Push notification sent via Firebase")
            else:
                print(f"   ❌ Firebase error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Firebase send failed: {e}")

    def _send_telegram(self, alert: Dict, message: str):
        """Send via Telegram Bot"""
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')

        if not bot_token or not chat_id:
            print("   ⚠️  Telegram credentials not configured")
            return

        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print(f"   ✅ Telegram notification sent")
            else:
                print(f"   ❌ Telegram error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Telegram send failed: {e}")

    def _send_email(self, alert: Dict, message: str):
        """Send via Email (using SendGrid or SMTP)"""
        # TODO: Implement email sending
        print("   ⚠️  Email notifications not yet implemented")

    def _save_alert_to_history(self, alert: Dict):
        """Save alert to JSON file for history"""
        history_file = 'alerts_history.json'

        try:
            # Load existing history
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    history = json.load(f)
            else:
                history = []

            # Add new alert
            history.append(alert)

            # Keep only last 1000 alerts
            history = history[-1000:]

            # Save
            with open(history_file, 'w') as f:
                json.dump(history, f, indent=2, default=str)

        except Exception as e:
            print(f"   ⚠️  Failed to save alert history: {e}")

    def start_monitoring(self, scan_interval_minutes: int = 5):
        """
        Start continuous monitoring

        Args:
            scan_interval_minutes: How often to scan (default: 5 minutes)
        """
        print(f"""
╔═══════════════════════════════════════════════════════════════════╗
║          SMART ALERTS SYSTEM - REAL-TIME MONITORING              ║
╚═══════════════════════════════════════════════════════════════════╝

📋 Watchlist ({len(self.watchlist)}): {', '.join(self.watchlist)}
💼 Positions ({len(self.positions)}): {', '.join(self.positions)}

⏰ Scan Interval: {scan_interval_minutes} minutes
🔔 Push Service: {self.push_service}

Starting monitoring...
        """)

        # Schedule scans
        schedule.every(scan_interval_minutes).minutes.do(self.scan_for_entry_signals)
        schedule.every(scan_interval_minutes).minutes.do(self.scan_for_exit_signals)

        # Initial scan
        self.scan_for_entry_signals()
        self.scan_for_exit_signals()

        # Run forever
        try:
            while True:
                schedule.run_pending()
                time.sleep(10)
        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped")


def main():
    """
    Example usage
    """
    # Initialize
    alerts = SmartAlertSystem(push_service='telegram')  # or 'firebase'

    # Set watchlist (stocks to monitor for entry)
    alerts.set_watchlist([
        'TSLA', 'NVDA', 'AAPL', 'AMD', 'MSFT',
        'GOOGL', 'META', 'AMZN', 'COIN', 'PLTR'
    ])

    # Set positions (stocks you hold - for exit alerts)
    alerts.set_positions([
        'TSLA', 'NVDA'
    ])

    # Start monitoring (scan every 5 minutes)
    alerts.start_monitoring(scan_interval_minutes=5)


if __name__ == "__main__":
    main()
