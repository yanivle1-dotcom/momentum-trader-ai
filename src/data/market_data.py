"""
Market data fetching and processing
"""
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pytz


class MarketDataFetcher:
    """Fetch and process market data"""

    def __init__(self):
        self.israel_tz = pytz.timezone('Asia/Jerusalem')
        self.us_tz = pytz.timezone('America/New_York')

    def get_stock_data(self, symbol: str, period: str = "5d") -> Optional[pd.DataFrame]:
        """
        Fetch stock data from Yahoo Finance

        Args:
            symbol: Stock ticker symbol
            period: Data period (1d, 5d, 1mo, etc.)

        Returns:
            DataFrame with OHLCV data or None
        """
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval="5m")

            if df.empty:
                return None

            return df

        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators"""

        if df is None or df.empty:
            return df

        # EMA
        df['EMA_9'] = ta.ema(df['Close'], length=9)
        df['EMA_20'] = ta.ema(df['Close'], length=20)

        # VWAP
        df['VWAP'] = ta.vwap(df['High'], df['Low'], df['Close'], df['Volume'])

        # RSI
        df['RSI'] = ta.rsi(df['Close'], length=14)

        # Volume SMA
        df['Volume_SMA'] = df['Volume'].rolling(window=20).mean()

        return df

    def get_current_data(self, symbol: str) -> Dict:
        """
        Get current stock data with indicators

        Returns:
            Dictionary with current stock data
        """
        try:
            ticker = yf.Ticker(symbol)

            # Get current price
            info = ticker.info
            current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)

            # Get historical data for calculations
            df = self.get_stock_data(symbol, period="5d")

            if df is None or df.empty:
                return self._error_data(symbol, "No data available")

            # Calculate indicators
            df = self.calculate_indicators(df)

            # Get latest values
            latest = df.iloc[-1]
            previous_close = info.get('previousClose', latest['Close'])

            # Calculate metrics
            change = current_price - previous_close
            change_percent = (change / previous_close * 100) if previous_close else 0

            # Calculate RVOL (current volume vs 20-day average)
            current_volume = latest['Volume']
            avg_volume = df['Volume'].mean()
            rvol = current_volume / avg_volume if avg_volume > 0 else 0

            # Calculate gap
            premarket_high = info.get('preMarketPrice')
            if premarket_high:
                gap_percent = ((premarket_high - previous_close) / previous_close * 100)
            else:
                gap_percent = ((latest['Open'] - previous_close) / previous_close * 100)

            # Price action analysis
            day_high = latest['High']
            day_low = latest['Low']
            day_range = day_high - day_low

            # Get premarket data
            premarket_volume = info.get('preMarketVolume', 0)

            return {
                'symbol': symbol,
                'current_price': round(current_price, 2),
                'previous_close': round(previous_close, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'volume': int(current_volume),
                'avg_volume': int(avg_volume),
                'rvol': round(rvol, 2),
                'gap_percent': round(gap_percent, 2),
                'day_high': round(day_high, 2),
                'day_low': round(day_low, 2),
                'day_range': round(day_range, 2),
                'premarket_volume': int(premarket_volume),
                'vwap': round(latest['VWAP'], 2) if not pd.isna(latest['VWAP']) else 0,
                'ema_9': round(latest['EMA_9'], 2) if not pd.isna(latest['EMA_9']) else 0,
                'ema_20': round(latest['EMA_20'], 2) if not pd.isna(latest['EMA_20']) else 0,
                'rsi': round(latest['RSI'], 2) if not pd.isna(latest['RSI']) else 0,
                'market_cap': info.get('marketCap', 0),
                'float_shares': info.get('floatShares', 0),
                'timestamp': datetime.now(self.israel_tz).isoformat(),
                'data_available': True
            }

        except Exception as e:
            print(f"Error getting current data for {symbol}: {e}")
            return self._error_data(symbol, str(e))

    def _error_data(self, symbol: str, error: str) -> Dict:
        """Return error data structure"""
        return {
            'symbol': symbol,
            'error': error,
            'data_available': False,
            'current_price': 0,
            'timestamp': datetime.now(self.israel_tz).isoformat()
        }

    def scan_for_momentum(self, symbols: List[str], criteria: Dict) -> List[Dict]:
        """
        Scan multiple stocks for momentum setups

        Args:
            symbols: List of stock symbols
            criteria: Dictionary with screening criteria

        Returns:
            List of stocks that pass the criteria
        """
        results = []

        min_rvol = criteria.get('min_rvol', 2.0)
        min_gap = criteria.get('min_gap_percent', 3.0)
        min_volume = criteria.get('min_volume', 100000)

        for symbol in symbols:
            data = self.get_current_data(symbol)

            if not data.get('data_available'):
                continue

            # Check criteria
            passes = True

            if data['rvol'] < min_rvol:
                passes = False

            if abs(data['gap_percent']) < min_gap:
                passes = False

            if data['volume'] < min_volume:
                passes = False

            if passes:
                results.append(data)

        # Sort by RVOL (highest first)
        results.sort(key=lambda x: x.get('rvol', 0), reverse=True)

        return results
