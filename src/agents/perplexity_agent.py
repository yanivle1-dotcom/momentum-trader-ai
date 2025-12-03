"""
Perplexity AI Agent for market analysis
"""
from typing import Dict, Any
import json
import requests
from .base_agent import BaseAgent


class PerplexityAgent(BaseAgent):
    """Perplexity-based market analysis agent with real-time web search"""

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.api_url = "https://api.perplexity.ai/chat/completions"
        self.model = "llama-3.1-sonar-large-128k-online"

    def analyze_stock(self, stock_data: Dict[str, Any], catalyst_search: bool = True) -> Dict[str, Any]:
        """Analyze stock using Perplexity with real-time web search"""

        try:
            prompt = self.build_analysis_prompt(stock_data)

            # Perplexity API call
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "אתה מנתח שוק מומחה עם גישה לאינטרנט בזמן אמת. חפש חדשות עדכניות וספק מקורות. החזר JSON תקין."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 2000,
                "return_citations": True,
                "search_recency_filter": "day"  # חדשות מהיום האחרון
            }

            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()

            data = response.json()
            content = data['choices'][0]['message']['content']
            citations = data.get('citations', [])

            # Parse JSON from response
            text = content.strip()
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text:
                text = text.split('```')[1].split('```')[0].strip()

            result = json.loads(text)

            # Add citations from Perplexity
            if citations and 'catalyst_sources' in result:
                result['catalyst_sources'].extend(citations)

            # Add metadata
            result['agent'] = 'Perplexity'
            result['model'] = self.model
            result['timestamp'] = stock_data.get('timestamp')
            result['citations'] = citations

            if self.validate_response(result):
                return result
            else:
                return self._error_response("תשובה לא תקינה מ-Perplexity")

        except json.JSONDecodeError as e:
            return self._error_response(f"שגיאת JSON: {str(e)}")
        except Exception as e:
            return self._error_response(f"שגיאה ב-Perplexity: {str(e)}")

    def _error_response(self, error_msg: str) -> Dict[str, Any]:
        """Return error response structure"""
        return {
            'agent': 'Perplexity',
            'error': error_msg,
            'catalyst': 'לא זמין',
            'setup_type': None,
            'setup_valid': False,
            'analysis': f'שגיאה בניתוח: {error_msg}',
            'warnings': ['לא ניתן היה לבצע ניתוח']
        }
