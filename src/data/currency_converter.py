"""
Currency conversion to ILS
"""
import requests
from datetime import datetime
from typing import Optional


class CurrencyConverter:
    """Convert USD to ILS"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.exchangerate-api.com/v4/latest/USD"
        self._cache = {}
        self._cache_time = None

    def get_usd_to_ils_rate(self) -> float:
        """
        Get current USD to ILS exchange rate

        Returns:
            Exchange rate or default 3.6 if unavailable
        """
        # Use cache if less than 1 hour old
        if self._cache_time and (datetime.now() - self._cache_time).seconds < 3600:
            return self._cache.get('USD_ILS', 3.6)

        try:
            # Try free API first
            response = requests.get(self.base_url, timeout=5)
            data = response.json()

            if 'rates' in data and 'ILS' in data['rates']:
                rate = data['rates']['ILS']
                self._cache['USD_ILS'] = rate
                self._cache_time = datetime.now()
                return rate

        except Exception as e:
            print(f"Error fetching exchange rate: {e}")

        # Try Bank of Israel as backup
        try:
            boi_url = "https://www.boi.org.il/currency.xml"
            response = requests.get(boi_url, timeout=5)

            # Parse XML (simplified - in production use xml.etree)
            # For now, return cached or default
            pass

        except:
            pass

        # Return cached or default
        return self._cache.get('USD_ILS', 3.6)

    def usd_to_ils(self, amount_usd: float) -> float:
        """Convert USD amount to ILS"""
        rate = self.get_usd_to_ils_rate()
        return round(amount_usd * rate, 2)

    def get_rate_info(self) -> dict:
        """Get rate with source information"""
        rate = self.get_usd_to_ils_rate()
        return {
            'rate': rate,
            'source': 'ExchangeRate-API',
            'timestamp': datetime.now().isoformat(),
            'from': 'USD',
            'to': 'ILS'
        }
