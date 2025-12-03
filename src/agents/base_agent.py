"""
Base Agent class for AI market analysis
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import json


class BaseAgent(ABC):
    """Base class for all AI agents"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.name = self.__class__.__name__

    @abstractmethod
    def analyze_stock(self, stock_data: Dict[str, Any], catalyst_search: bool = True) -> Dict[str, Any]:
        """
        Analyze stock data and return insights

        Args:
            stock_data: Dictionary containing stock information
            catalyst_search: Whether to search for news catalysts

        Returns:
            Dictionary with analysis results
        """
        pass

    def build_analysis_prompt(self, stock_data: Dict[str, Any]) -> str:
        """Build the analysis prompt for the AI"""

        symbol = stock_data.get('symbol', 'N/A')
        price = stock_data.get('current_price', 0)
        change_pct = stock_data.get('change_percent', 0)
        volume = stock_data.get('volume', 0)
        rvol = stock_data.get('rvol', 0)
        gap = stock_data.get('gap_percent', 0)

        prompt = f"""
אתה מנתח שוק מומחה לפי שיטת Ross Cameron / Warrior Trading.

נתוני המניה:
- סימול: {symbol}
- מחיר נוכחי: ${price:.2f}
- שינוי יומי: {change_pct:.2f}%
- גאפ: {gap:.2f}%
- נפח: {volume:,.0f}
- RVOL: {rvol:.2f}x

משימתך:
1. חפש חדשות/קטליסטים אקטואליים (מה-48 שעות האחרונות) על {symbol}
2. אמת את המידע מלפחות 2 מקורות
3. קבע האם יש סט-אפ מומנטום לפי Ross Cameron:
   - Gap & Go
   - Red to Green
   - First Green Day
   - Micro Pullback
   - Bull Flag

4. ספק ניתוח מפורט:
   - מהו הקטליסט (עם קישורים ותאריכים)
   - איזה סט-אפ קיים
   - נקודת כניסה מדויקת
   - סטופ לוס
   - יעדים (עם R:R)
   - למה כדאי/לא כדאי

5. תשובה בעברית, עם דיסקליימר שזה לא ייעוץ השקעות.

פורמט תשובה ב-JSON:
{{
    "catalyst": "תיאור הקטליסט + קישורים",
    "catalyst_sources": ["מקור 1", "מקור 2"],
    "setup_type": "סוג הסט-אפ או null",
    "setup_valid": true/false,
    "entry_price": מחיר כניסה או null,
    "stop_loss": מחיר סטופ או null,
    "targets": [יעד1, יעד2, יעד3],
    "risk_reward": "1:2",
    "analysis": "ניתוח מפורט בעברית",
    "why_now": "למה עכשיו / למה לא",
    "risk_level": "נמוך/בינוני/גבוה",
    "warnings": ["אזהרה 1", "אזהרה 2"]
}}
"""
        return prompt

    def validate_response(self, response: Dict[str, Any]) -> bool:
        """Validate that response contains required fields"""
        required_fields = ['catalyst', 'setup_type', 'analysis']
        return all(field in response for field in required_fields)
