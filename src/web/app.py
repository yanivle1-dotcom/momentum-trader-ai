"""
Flask web application for Momentum Trader AI
"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
from datetime import datetime

# Import our modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import OpenAIAgent, GeminiAgent, PerplexityAgent
from data import MarketDataFetcher, CurrencyConverter
from analysis import RossCameronAnalyzer

# Load environment variables
load_dotenv()

app = Flask(__name__,
            template_folder='../../templates',
            static_folder='../../static')
CORS(app)

# Initialize components
market_data = MarketDataFetcher()
currency_converter = CurrencyConverter()
setup_analyzer = RossCameronAnalyzer()

# Initialize agents
agents = {}

if os.getenv('OPENAI_API_KEY'):
    agents['chatgpt'] = OpenAIAgent(os.getenv('OPENAI_API_KEY'))

if os.getenv('GEMINI_API_KEY'):
    agents['gemini'] = GeminiAgent(os.getenv('GEMINI_API_KEY'))

if os.getenv('PERPLEXITY_API_KEY'):
    agents['perplexity'] = PerplexityAgent(os.getenv('PERPLEXITY_API_KEY'))


# Load stock configuration
with open('../../config/stocks.json', 'r', encoding='utf-8') as f:
    config = json.load(f)


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', agents=list(agents.keys()))


@app.route('/api/scan', methods=['GET'])
def scan_stocks():
    """Scan stocks for momentum setups"""

    try:
        # Get all symbols
        israeli = config.get('israeli_stocks', [])
        us = config.get('us_stocks_popular_in_israel', [])
        all_symbols = israeli + us

        # Get momentum criteria
        criteria = config.get('momentum_criteria', {})

        # Scan for momentum
        results = market_data.scan_for_momentum(all_symbols, criteria)

        # Add currency conversion for US stocks
        usd_ils_rate = currency_converter.get_usd_to_ils_rate()

        for stock in results:
            symbol = stock['symbol']

            # Add market info
            stock['market'] = 'IL' if symbol.endswith('.TA') else 'US'

            # Convert to ILS if US stock
            if stock['market'] == 'US':
                stock['current_price_ils'] = round(stock['current_price'] * usd_ils_rate, 2)
                stock['currency'] = 'USD'
            else:
                stock['current_price_ils'] = stock['current_price']
                stock['currency'] = 'ILS'

        return jsonify({
            'success': True,
            'stocks': results,
            'usd_ils_rate': usd_ils_rate,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/analyze/<symbol>', methods=['POST'])
def analyze_stock(symbol):
    """Analyze a specific stock"""

    try:
        data = request.get_json() or {}
        agent_name = data.get('agent', 'chatgpt')

        # Validate agent
        if agent_name not in agents:
            return jsonify({
                'success': False,
                'error': f'Agent {agent_name} not configured'
            }), 400

        # Get stock data
        stock_data = market_data.get_current_data(symbol)

        if not stock_data.get('data_available'):
            return jsonify({
                'success': False,
                'error': 'Stock data not available'
            }), 404

        # Get historical data for setup analysis
        historical_df = market_data.get_stock_data(symbol, period="5d")

        # Analyze setup
        setup_analysis = setup_analyzer.analyze_setup(stock_data, historical_df)

        # Get AI analysis
        agent = agents[agent_name]
        ai_analysis = agent.analyze_stock(stock_data, catalyst_search=True)

        # Currency conversion
        usd_ils_rate = currency_converter.get_usd_to_ils_rate()
        market = 'IL' if symbol.endswith('.TA') else 'US'

        if market == 'US':
            stock_data['current_price_ils'] = round(stock_data['current_price'] * usd_ils_rate, 2)
            stock_data['currency'] = 'USD'
        else:
            stock_data['current_price_ils'] = stock_data['current_price']
            stock_data['currency'] = 'ILS'

        # Combine results
        result = {
            'success': True,
            'symbol': symbol,
            'market': market,
            'stock_data': stock_data,
            'setup_analysis': setup_analysis,
            'ai_analysis': ai_analysis,
            'usd_ils_rate': usd_ils_rate,
            'timestamp': datetime.now().isoformat()
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/chart/<symbol>', methods=['GET'])
def get_chart_data(symbol):
    """Get chart data for a stock"""

    try:
        period = request.args.get('period', '5d')

        df = market_data.get_stock_data(symbol, period=period)

        if df is None or df.empty:
            return jsonify({
                'success': False,
                'error': 'No data available'
            }), 404

        # Calculate indicators
        df = market_data.calculate_indicators(df)

        # Convert to JSON-friendly format
        chart_data = {
            'timestamps': df.index.strftime('%Y-%m-%d %H:%M').tolist(),
            'open': df['Open'].tolist(),
            'high': df['High'].tolist(),
            'low': df['Low'].tolist(),
            'close': df['Close'].tolist(),
            'volume': df['Volume'].tolist(),
            'vwap': df['VWAP'].tolist(),
            'ema_9': df['EMA_9'].tolist(),
            'ema_20': df['EMA_20'].tolist(),
            'rsi': df['RSI'].tolist()
        }

        return jsonify({
            'success': True,
            'symbol': symbol,
            'data': chart_data
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/agents', methods=['GET'])
def get_available_agents():
    """Get list of available AI agents"""

    agent_info = []

    for name, agent in agents.items():
        agent_info.append({
            'name': name,
            'display_name': name.capitalize(),
            'available': True
        })

    return jsonify({
        'success': True,
        'agents': agent_info
    })


@app.route('/api/exchange-rate', methods=['GET'])
def get_exchange_rate():
    """Get current USD/ILS exchange rate"""

    rate_info = currency_converter.get_rate_info()

    return jsonify({
        'success': True,
        'rate_info': rate_info
    })


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'

    print(f"""
    ╔═══════════════════════════════════════════════╗
    ║   Momentum Trader AI - Ross Cameron System   ║
    ╚═══════════════════════════════════════════════╝

    🚀 Server starting on http://localhost:{port}

    Available AI Agents: {', '.join(agents.keys())}

    📊 Dashboard: http://localhost:{port}
    """)

    app.run(host='0.0.0.0', port=port, debug=debug)
