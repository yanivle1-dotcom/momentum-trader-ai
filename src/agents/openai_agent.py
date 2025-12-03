"""
OpenAI (ChatGPT) Agent for market analysis
"""
from typing import Dict, Any
import json
import openai
from .base_agent import BaseAgent


class OpenAIAgent(BaseAgent):
    """ChatGPT-based market analysis agent"""

    def __init__(self, api_key: str):
        super().__init__(api_key)
        openai.api_key = api_key
        self.model = "gpt-4-turbo-preview"

    def analyze_stock(self, stock_data: Dict[str, Any], catalyst_search: bool = True) -> Dict[str, Any]:
        """Analyze stock using ChatGPT with web search"""

        try:
            prompt = self.build_analysis_prompt(stock_data)

            # Use GPT-4 with function calling to ensure structured output
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "אתה מנתח שוק מומחה. השתמש בידע עדכני מהאינטרנט. החזר תמיד JSON תקין."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)

            # Add metadata
            result['agent'] = 'ChatGPT'
            result['model'] = self.model
            result['timestamp'] = stock_data.get('timestamp')

            if self.validate_response(result):
                return result
            else:
                return self._error_response("תשובה לא תקינה מ-ChatGPT")

        except Exception as e:
            return self._error_response(f"שגיאה ב-ChatGPT: {str(e)}")

    def _error_response(self, error_msg: str) -> Dict[str, Any]:
        """Return error response structure"""
        return {
            'agent': 'ChatGPT',
            'error': error_msg,
            'catalyst': 'לא זמין',
            'setup_type': None,
            'setup_valid': False,
            'analysis': f'שגיאה בניתוח: {error_msg}',
            'warnings': ['לא ניתן היה לבצע ניתוח']
        }
