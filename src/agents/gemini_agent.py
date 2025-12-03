"""
Google Gemini Agent for market analysis
"""
from typing import Dict, Any
import json
import google.generativeai as genai
from .base_agent import BaseAgent


class GeminiAgent(BaseAgent):
    """Gemini-based market analysis agent"""

    def __init__(self, api_key: str):
        super().__init__(api_key)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def analyze_stock(self, stock_data: Dict[str, Any], catalyst_search: bool = True) -> Dict[str, Any]:
        """Analyze stock using Gemini with web search"""

        try:
            prompt = self.build_analysis_prompt(stock_data)

            # Add instruction for JSON output
            prompt += "\n\nחשוב: החזר רק JSON תקין, ללא טקסט נוסף."

            response = self.model.generate_content(prompt)

            # Parse JSON from response
            text = response.text.strip()

            # Try to extract JSON if wrapped in markdown
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text:
                text = text.split('```')[1].split('```')[0].strip()

            result = json.loads(text)

            # Add metadata
            result['agent'] = 'Gemini'
            result['model'] = 'gemini-pro'
            result['timestamp'] = stock_data.get('timestamp')

            if self.validate_response(result):
                return result
            else:
                return self._error_response("תשובה לא תקינה מ-Gemini")

        except json.JSONDecodeError as e:
            return self._error_response(f"שגיאת JSON: {str(e)}")
        except Exception as e:
            return self._error_response(f"שגיאה ב-Gemini: {str(e)}")

    def _error_response(self, error_msg: str) -> Dict[str, Any]:
        """Return error response structure"""
        return {
            'agent': 'Gemini',
            'error': error_msg,
            'catalyst': 'לא זמין',
            'setup_type': None,
            'setup_valid': False,
            'analysis': f'שגיאה בניתוח: {error_msg}',
            'warnings': ['לא ניתן היה לבצע ניתוח']
        }
