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
src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, src_path)

from agents import OpenAIAgent, GeminiAgent, PerplexityAgent
from data import MarketDataFetcher, CurrencyConverter
from analysis import RossCameronAnalyzer
from backtesting import Backtester
from database import TradeDatabase
from alerts import AlertManager
from news import NewsAggregator
from calculator import PositionCalculator
from analysis.sector_research import SectorResearch
from analysis.comprehensive_analyzer import ComprehensiveAnalyzer
from analysis.quantitative_analysis import QuantitativeAnalyzer
from analysis.social_intelligence import SocialIntelligence

# Import enhanced agents and premium data
sys.path.insert(0, os.path.join(src_path, 'agents'))
sys.path.insert(0, os.path.join(src_path, 'data'))
from enhanced_perplexity_agent import EnhancedPerplexityAgent
from premium_data_sources import PremiumDataCollector

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
trade_db = TradeDatabase('../../trades.db')
alert_manager = AlertManager(check_interval=60)
news_aggregator = NewsAggregator()
position_calculator = None  # Will be initialized with account size
sector_research = SectorResearch()

# Initialize premium data collector
premium_data_collector = PremiumDataCollector()

# Initialize quantitative analyzer
quantitative_analyzer = QuantitativeAnalyzer(risk_free_rate=0.045)

# Initialize social intelligence module
social_intelligence = None
try:
    social_intelligence = SocialIntelligence()
    print("✅ Social Intelligence module initialized (sentiment + influencers)")
except Exception as e:
    print(f"⚠️  Social Intelligence module failed to initialize: {e}")

# Initialize agents
agents = {}

if os.getenv('OPENAI_API_KEY'):
    agents['chatgpt'] = OpenAIAgent(os.getenv('OPENAI_API_KEY'))

if os.getenv('GEMINI_API_KEY'):
    agents['gemini'] = GeminiAgent(os.getenv('GEMINI_API_KEY'))

if os.getenv('PERPLEXITY_API_KEY'):
    agents['perplexity'] = PerplexityAgent(os.getenv('PERPLEXITY_API_KEY'))

# Initialize enhanced Perplexity agent with real-time web search
enhanced_perplexity = None
if os.getenv('PERPLEXITY_API_KEY'):
    try:
        enhanced_perplexity = EnhancedPerplexityAgent(os.getenv('PERPLEXITY_API_KEY'))
        print("✅ Enhanced Perplexity agent initialized with real-time web search")
    except Exception as e:
        print(f"⚠️  Enhanced Perplexity agent failed to initialize: {e}")

# Initialize comprehensive analyzer with all AI agents, premium data, quantitative analysis, and Finnhub
comprehensive_analyzer = ComprehensiveAnalyzer(
    chatgpt_agent=agents.get('chatgpt'),
    gemini_agent=agents.get('gemini'),
    perplexity_agent=enhanced_perplexity,
    premium_data_collector=premium_data_collector,
    quantitative_analyzer=quantitative_analyzer,
    finnhub_api_key=os.getenv('FINNHUB_API_KEY')
)


# Load stock configuration
with open('../../config/stocks.json', 'r', encoding='utf-8') as f:
    config = json.load(f)


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', agents=list(agents.keys()))


@app.route('/features')
def features():
    """Features showcase page"""
    return render_template('features.html', agents=list(agents.keys()))


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


# ═══════════════════════════════════════════════════
#  NEW FEATURES - V2.0
# ═══════════════════════════════════════════════════

@app.route('/api/backtest', methods=['POST'])
def run_backtest():
    """Run backtest"""
    try:
        data = request.get_json()
        symbols = data.get('symbols', ['NVDA', 'TSLA'])
        backtester = Backtester(initial_capital=data.get('initial_capital', 10000))
        result = backtester.run_backtest(
            symbols=symbols,
            start_date=data['start_date'],
            end_date=data['end_date'],
            risk_per_trade=data.get('risk_per_trade', 2.0) / 100
        )
        return jsonify({'success': True, 'results': result.to_dict()})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/trades', methods=['GET'])
def get_trades():
    """Get trades"""
    trades = trade_db.get_all_trades(limit=int(request.args.get('limit', 100)))
    return jsonify({'success': True, 'trades': trades})


@app.route('/api/trades', methods=['POST'])
def add_trade():
    """Add trade"""
    data = request.get_json()
    trade_id = trade_db.add_trade(**data)
    return jsonify({'success': True, 'trade_id': trade_id})


@app.route('/api/trades/<int:trade_id>/close', methods=['PUT'])
def close_trade(trade_id):
    """Close trade"""
    data = request.get_json()
    trade_db.close_trade(trade_id, **data)
    return jsonify({'success': True})


@app.route('/api/trades/stats', methods=['GET'])
def get_trade_stats():
    """Get stats"""
    stats = trade_db.get_trade_stats()
    return jsonify({'success': True, 'stats': stats})


@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get alerts"""
    alerts = alert_manager.export_alerts()
    return jsonify({'success': True, 'alerts': alerts})


@app.route('/api/alerts', methods=['POST'])
def create_alert():
    """Create alert"""
    data = request.get_json()
    alert = alert_manager.add_alert(**data)
    if not alert_manager.running:
        alert_manager.start_monitoring()
    return jsonify({'success': True, 'alert_id': alert.id, 'alert': {'id': alert.id, 'message': alert.message}})


@app.route('/api/alerts/<int:alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    """Delete alert"""
    try:
        alert_manager.remove_alert(alert_id)
        return jsonify({'success': True, 'message': 'Alert deleted'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/news/<symbol>', methods=['GET'])
def get_stock_news(symbol):
    """Get news"""
    articles = news_aggregator.get_stock_news(symbol, hours=int(request.args.get('hours', 24)))
    sentiment = news_aggregator.analyze_sentiment(articles)
    return jsonify({'success': True, 'articles': news_aggregator.export_news(articles), 'sentiment': sentiment})


@app.route('/api/news/market', methods=['GET'])
def get_market_news():
    """Get market news"""
    articles = news_aggregator.get_market_news(hours=24, limit=20)
    return jsonify({'success': True, 'articles': news_aggregator.export_news(articles)})


@app.route('/api/news/trending', methods=['GET'])
def get_trending():
    """Get trending stocks"""
    hours = int(request.args.get('hours', 24))
    limit = int(request.args.get('limit', 10))
    trending = news_aggregator.get_trending_symbols(hours=hours, limit=limit)
    return jsonify({'success': True, 'trending': trending})


@app.route('/api/calculator/position', methods=['POST'])
def calculate_position():
    """Calculate position"""
    try:
        data = request.get_json()
        calc = PositionCalculator(float(data.get('account_size', 10000)))
        position = calc.calculate_position(
            entry_price=float(data['entry_price']),
            stop_loss=float(data['stop_loss']),
            targets=[float(t) for t in data['targets']],
            risk_percent=float(data.get('risk_percent', 2.0))
        )
        return jsonify({
            'success': True,
            'shares': position.shares,
            'total_cost': position.total_cost,
            'risk_amount': position.risk_amount,
            'risk_percent': position.risk_percent,
            'targets': position.targets,
            'potential_profit': position.potential_profit,
            'risk_reward_ratios': position.risk_reward_ratios
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ========== NEW: Market Research API ==========

@app.route('/market-research')
def market_research_page():
    """Market research UI page"""
    return render_template('market_research.html')


@app.route('/api/research/analyze/<symbol>', methods=['GET'])
def analyze_stock_research(symbol):
    """Analyze a stock and provide entry/exit recommendations"""
    try:
        symbol = symbol.upper()
        analysis = sector_research.analyze_entry_exit(symbol)

        if 'error' in analysis:
            return jsonify({'error': analysis['error']}), 400

        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/research/sectors', methods=['GET'])
def get_sectors_overview():
    """Get overview of top stocks across all sectors"""
    try:
        overview = sector_research.get_all_sectors_overview()
        return jsonify(overview)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/research/sector/<sector>', methods=['GET'])
def get_sector_stocks(sector):
    """Get top stocks in a specific sector"""
    try:
        top_n = int(request.args.get('top', 5))
        stocks = sector_research.get_sector_top_stocks(sector, top_n=top_n)

        if not stocks:
            return jsonify({'error': f'Sector {sector} not found'}), 404

        return jsonify({'sector': sector, 'stocks': stocks})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ========== NEW: Comprehensive Investment Dashboard ==========

@app.route('/investment-dashboard')
def investment_dashboard():
    """Investment dashboard UI page"""
    return render_template('investment_dashboard.html')


@app.route('/api/investment/analyze/<symbol>', methods=['GET'])
def comprehensive_stock_analysis(symbol):
    """
    Get comprehensive analysis for long-term investing or day trading
    """
    try:
        symbol = symbol.upper()
        analysis_type = request.args.get('type', 'long-term')  # 'long-term' or 'day-trading'

        if analysis_type not in ['long-term', 'day-trading']:
            return jsonify({'error': 'Invalid analysis type. Use long-term or day-trading'}), 400

        # Run comprehensive analysis
        analysis = comprehensive_analyzer.get_comprehensive_analysis(symbol, analysis_type)

        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/quant/monte-carlo/<symbol>', methods=['GET'])
def monte_carlo_analysis(symbol):
    """Monte Carlo simulation for price prediction"""
    try:
        symbol = symbol.upper()
        days = int(request.args.get('days', 252))  # Default: 1 year
        simulations = int(request.args.get('simulations', 10000))

        result = quantitative_analyzer.monte_carlo_simulation(symbol, days, simulations)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/quant/risk-metrics/<symbol>', methods=['GET'])
def risk_metrics_analysis(symbol):
    """Calculate comprehensive risk metrics"""
    try:
        symbol = symbol.upper()
        period = request.args.get('period', '1y')

        result = quantitative_analyzer.calculate_risk_metrics(symbol, period)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/quant/portfolio-optimize', methods=['POST'])
def portfolio_optimization():
    """Portfolio optimization"""
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])

        if not symbols or len(symbols) < 2:
            return jsonify({'error': 'Need at least 2 symbols'}), 400

        result = quantitative_analyzer.optimize_portfolio(symbols)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/quant/correlation', methods=['POST'])
def correlation_analysis():
    """Calculate correlation matrix"""
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])

        if not symbols or len(symbols) < 2:
            return jsonify({'error': 'Need at least 2 symbols'}), 400

        result = quantitative_analyzer.calculate_correlation_matrix(symbols)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/quant/options/<symbol>', methods=['GET'])
def options_pricing(symbol):
    """Black-Scholes options pricing"""
    try:
        symbol = symbol.upper()
        strike = float(request.args.get('strike', 0))
        days = int(request.args.get('days', 30))
        option_type = request.args.get('type', 'call')

        if strike == 0:
            return jsonify({'error': 'Strike price required'}), 400

        result = quantitative_analyzer.black_scholes_options(symbol, strike, days, option_type)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# SOCIAL INTELLIGENCE ENDPOINTS
# ============================================================================

@app.route('/api/social/sentiment/<symbol>', methods=['GET'])
def get_social_sentiment(symbol):
    """
    Get social sentiment analysis for a stock
    Example: GET /api/social/sentiment/TSLA
    """
    if not social_intelligence:
        return jsonify({
            'error': 'Social Intelligence module not available',
            'message': 'Check API keys for Reddit/Twitter'
        }), 503

    try:
        symbol = symbol.upper()
        analysis = social_intelligence.analyze_stock(symbol)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/social/scan', methods=['GET'])
def scan_social_sentiment():
    """
    Scan multiple stocks for social sentiment
    Example: GET /api/social/scan?symbols=TSLA,NVDA,AAPL
    """
    if not social_intelligence:
        return jsonify({'error': 'Social Intelligence module not available'}), 503

    try:
        symbols_param = request.args.get('symbols', '')
        if not symbols_param:
            return jsonify({'error': 'symbols parameter required'}), 400

        symbols = [s.strip().upper() for s in symbols_param.split(',')]
        results = social_intelligence.scan_watchlist(symbols)

        return jsonify({
            'scanned': len(symbols),
            'results': results,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/social/opportunities', methods=['GET'])
def get_social_opportunities():
    """
    Get top trading opportunities based on social sentiment
    Example: GET /api/social/opportunities?symbols=TSLA,NVDA,AAPL&min_confidence=60
    """
    if not social_intelligence:
        return jsonify({'error': 'Social Intelligence module not available'}), 503

    try:
        symbols_param = request.args.get('symbols', '')
        min_confidence = int(request.args.get('min_confidence', 60))

        if not symbols_param:
            return jsonify({'error': 'symbols parameter required'}), 400

        symbols = [s.strip().upper() for s in symbols_param.split(',')]
        opportunities = social_intelligence.get_top_opportunities(symbols, min_confidence)

        return jsonify({
            'opportunities': opportunities,
            'count': len(opportunities),
            'min_confidence': min_confidence,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/social/alerts', methods=['GET'])
def get_social_alerts():
    """
    Get risk alerts for current positions based on negative social sentiment
    Example: GET /api/social/alerts?positions=TSLA,AAPL&min_confidence=60
    """
    if not social_intelligence:
        return jsonify({'error': 'Social Intelligence module not available'}), 503

    try:
        positions_param = request.args.get('positions', '')
        min_confidence = int(request.args.get('min_confidence', 60))

        if not positions_param:
            return jsonify({'error': 'positions parameter required'}), 400

        positions = [s.strip().upper() for s in positions_param.split(',')]
        alerts = social_intelligence.get_risk_alerts(positions, min_confidence)

        return jsonify({
            'alerts': alerts,
            'count': len(alerts),
            'positions_checked': len(positions),
            'min_confidence': min_confidence,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'

    print(f"""
    ╔═══════════════════════════════════════════════╗
    ║         Momentum Trader AI - V3.0            ║
    ║    Professional Investment Analysis System    ║
    ╚═══════════════════════════════════════════════╝

    🚀 Server: http://localhost:{port}

    🎯 MAIN DASHBOARD: http://localhost:{port}/investment-dashboard
       • השקעות ארוכות טווח + מסחר יומי
       • ניתוח AI מ-ChatGPT ו-Gemini
       • חדשות בזמן אמת + סנטימנט
       • גרפים אינטראקטיביים
       • כל המידע שמשקיע צריך!

    📊 Market Research: http://localhost:{port}/market-research
    ✨ Features Dashboard: http://localhost:{port}/features
    🏠 Ross Cameron Dashboard: http://localhost:{port}/

    🤖 AI Agents: {', '.join(agents.keys()) if agents else 'None configured'}

    ✨ NEW V3.0 FEATURES:
    • 🎯 השקעות ארוכות טווח vs מסחר יומי
    • 🤖 השוואת המלצות AI (ChatGPT + Gemini)
    • 📰 חדשות עם ניתוח סנטימנט
    • 💰 ניתוח פונדמנטלי מעמיק
    • 📊 ניתוח טכני עם גרפים
    • 🎯 נקודות כניסה/יציאה מדויקות
    • 💎 ציונים והמלצות מקצועיות

    📖 התחל ב: /investment-dashboard

    🆕 SOCIAL INTELLIGENCE ENDPOINTS:
    • GET /api/social/sentiment/<symbol> - Social sentiment for stock
    • GET /api/social/scan?symbols=TSLA,NVDA - Scan multiple stocks
    • GET /api/social/opportunities - Top trading opportunities
    • GET /api/social/alerts?positions=TSLA,AAPL - Risk alerts for positions
    """)

    app.run(host='0.0.0.0', port=port, debug=debug)
