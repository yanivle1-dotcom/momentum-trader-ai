// Main Application JavaScript

class MomentumTraderApp {
    constructor() {
        this.selectedAgent = 'chatgpt';
        this.currentStocks = [];
        this.usdIlsRate = 3.6;

        this.init();
    }

    init() {
        // Event listeners
        document.getElementById('scan-btn').addEventListener('click', () => this.scanStocks());
        document.getElementById('refresh-btn').addEventListener('click', () => this.scanStocks());
        document.getElementById('agent-select').addEventListener('change', (e) => {
            this.selectedAgent = e.target.value;
        });

        // Modal close
        document.querySelector('.close').addEventListener('click', () => {
            document.getElementById('analysis-modal').style.display = 'none';
        });

        // Close modal on outside click
        window.addEventListener('click', (e) => {
            const modal = document.getElementById('analysis-modal');
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });

        // Load exchange rate on start
        this.loadExchangeRate();

        // Auto-scan on load
        setTimeout(() => this.scanStocks(), 500);
    }

    async loadExchangeRate() {
        try {
            const response = await fetch('/api/exchange-rate');
            const data = await response.json();

            if (data.success) {
                this.usdIlsRate = data.rate_info.rate;
                document.getElementById('usd-ils-rate').textContent =
                    this.usdIlsRate.toFixed(2);
            }
        } catch (error) {
            console.error('Error loading exchange rate:', error);
        }
    }

    async scanStocks() {
        this.showLoading(true);

        try {
            const response = await fetch('/api/scan');
            const data = await response.json();

            if (data.success) {
                this.currentStocks = data.stocks;
                this.usdIlsRate = data.usd_ils_rate;
                this.renderStocks();
            } else {
                this.showError('שגיאה בסריקת מניות: ' + data.error);
            }
        } catch (error) {
            this.showError('שגיאה בחיבור לשרת: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    renderStocks() {
        const container = document.getElementById('results-container');
        container.innerHTML = '';

        if (this.currentStocks.length === 0) {
            container.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 40px; background: white; border-radius: 15px;">
                    <h2>😔 לא נמצאו מניות מומנטום</h2>
                    <p>נסה שוב מאוחר יותר או שנה את קריטריוני הסינון</p>
                </div>
            `;
            return;
        }

        this.currentStocks.forEach(stock => {
            const card = this.createStockCard(stock);
            container.appendChild(card);
        });
    }

    createStockCard(stock) {
        const card = document.createElement('div');
        card.className = 'stock-card';
        card.onclick = () => this.analyzeStock(stock.symbol);

        const priceChangeClass = stock.change_percent >= 0 ? 'positive' : 'negative';
        const priceChangeSign = stock.change_percent >= 0 ? '+' : '';

        // Display price in both currencies
        let priceDisplay = '';
        if (stock.market === 'US') {
            priceDisplay = `
                <div class="stock-price">
                    $${stock.current_price.toFixed(2)}
                    <span style="font-size: 0.6em; color: #666;">
                        (₪${stock.current_price_ils.toFixed(2)})
                    </span>
                </div>
            `;
        } else {
            priceDisplay = `
                <div class="stock-price">
                    ₪${stock.current_price.toFixed(2)}
                </div>
            `;
        }

        card.innerHTML = `
            <div class="stock-header">
                <div class="stock-symbol">${stock.symbol}</div>
                <div class="market-badge ${stock.market}">${stock.market}</div>
            </div>

            ${priceDisplay}

            <div class="price-change ${priceChangeClass}">
                ${priceChangeSign}${stock.change_percent.toFixed(2)}%
                (${priceChangeSign}${stock.change.toFixed(2)})
            </div>

            <div class="stock-metrics">
                <div class="metric">
                    <div class="metric-label">RVOL</div>
                    <div class="metric-value highlight">${stock.rvol.toFixed(2)}x</div>
                </div>
                <div class="metric">
                    <div class="metric-label">גאפ</div>
                    <div class="metric-value ${Math.abs(stock.gap_percent) > 5 ? 'highlight' : ''}">
                        ${stock.gap_percent.toFixed(2)}%
                    </div>
                </div>
                <div class="metric">
                    <div class="metric-label">נפח</div>
                    <div class="metric-value">${this.formatVolume(stock.volume)}</div>
                </div>
                <div class="metric">
                    <div class="metric-label">טווח יומי</div>
                    <div class="metric-value">${stock.day_range.toFixed(2)}</div>
                </div>
            </div>

            <div style="text-align: center; margin-top: 15px;">
                <small style="color: #666;">לחץ לניתוח מלא</small>
            </div>
        `;

        return card;
    }

    async analyzeStock(symbol) {
        this.showLoading(true);

        try {
            const response = await fetch(`/api/analyze/${symbol}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    agent: this.selectedAgent
                })
            });

            const data = await response.json();

            if (data.success) {
                this.showAnalysisModal(data);
                this.loadChart(symbol);
            } else {
                this.showError('שגיאה בניתוח: ' + data.error);
            }
        } catch (error) {
            this.showError('שגיאה: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    showAnalysisModal(data) {
        const modal = document.getElementById('analysis-modal');
        const modalBody = document.getElementById('modal-body');

        const stock = data.stock_data;
        const setup = data.setup_analysis;
        const ai = data.ai_analysis;

        // Build price display
        let priceDisplay = '';
        if (stock.currency === 'USD') {
            priceDisplay = `$${stock.current_price.toFixed(2)} (₪${stock.current_price_ils.toFixed(2)})`;
        } else {
            priceDisplay = `₪${stock.current_price.toFixed(2)}`;
        }

        // Build criteria lists
        let criteriaMetHtml = '';
        if (setup.criteria_met && setup.criteria_met.length > 0) {
            criteriaMetHtml = '<ul class="criteria-list">' +
                setup.criteria_met.map(c => `<li class="met">✓ ${c}</li>`).join('') +
                '</ul>';
        }

        let criteriaFailedHtml = '';
        if (setup.criteria_failed && setup.criteria_failed.length > 0) {
            criteriaFailedHtml = '<ul class="criteria-list">' +
                setup.criteria_failed.map(c => `<li class="failed">✗ ${c}</li>`).join('') +
                '</ul>';
        }

        // Build trade plan
        let tradePlanHtml = '';
        if (setup.setup_valid && setup.entry_point) {
            tradePlanHtml = `
                <div class="trade-plan">
                    <h3>תוכנית מסחר</h3>
                    <div class="plan-item">
                        <div class="plan-label">🎯 נקודת כניסה:</div>
                        <div class="plan-value">$${setup.entry_point.toFixed(2)}</div>
                    </div>
                    <div class="plan-item">
                        <div class="plan-label">🛑 סטופ לוס:</div>
                        <div class="plan-value">$${setup.stop_loss.toFixed(2)}</div>
                    </div>
                    <div class="plan-item">
                        <div class="plan-label">🎁 יעדים:</div>
                        <div class="plan-value">
                            ${setup.targets.map((t, i) => `יעד ${i+1}: $${t.toFixed(2)}`).join(' | ')}
                        </div>
                    </div>
                    <div class="plan-item">
                        <div class="plan-label">📊 R:R:</div>
                        <div class="plan-value">${setup.risk_reward}</div>
                    </div>
                    <div class="plan-item">
                        <div class="plan-label">💪 רמת ביטחון:</div>
                        <div class="plan-value">${this.translateConfidence(setup.confidence)}</div>
                    </div>
                </div>
            `;
        }

        // AI Analysis
        let aiAnalysisHtml = '';
        if (ai && ai.analysis) {
            aiAnalysisHtml = `
                <div class="analysis-section">
                    <h2>🤖 ניתוח ${ai.agent}</h2>
                    <div class="ai-analysis">${ai.analysis}</div>

                    ${ai.catalyst ? `
                        <h3>📰 קטליסט</h3>
                        <p>${ai.catalyst}</p>
                    ` : ''}

                    ${ai.catalyst_sources && ai.catalyst_sources.length > 0 ? `
                        <h3>📌 מקורות</h3>
                        <ul>
                            ${ai.catalyst_sources.map(s => `<li>${s}</li>`).join('')}
                        </ul>
                    ` : ''}

                    ${ai.warnings && ai.warnings.length > 0 ? `
                        <h3>⚠️ אזהרות</h3>
                        <ul class="criteria-list">
                            ${ai.warnings.map(w => `<li class="failed">${w}</li>`).join('')}
                        </ul>
                    ` : ''}
                </div>
            `;
        }

        modalBody.innerHTML = `
            <h1 style="color: #667eea; margin-bottom: 20px;">
                ${data.symbol}
                <span style="font-size: 0.6em; color: #666;">(${data.market})</span>
            </h1>

            <div class="analysis-section">
                <h2>📊 נתוני מניה</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 15px;">
                    <div class="metric">
                        <div class="metric-label">מחיר נוכחי</div>
                        <div class="metric-value">${priceDisplay}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">שינוי יומי</div>
                        <div class="metric-value ${stock.change_percent >= 0 ? 'positive' : 'negative'}">
                            ${stock.change_percent >= 0 ? '+' : ''}${stock.change_percent.toFixed(2)}%
                        </div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">RVOL</div>
                        <div class="metric-value highlight">${stock.rvol.toFixed(2)}x</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">גאפ</div>
                        <div class="metric-value">${stock.gap_percent.toFixed(2)}%</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">VWAP</div>
                        <div class="metric-value">$${stock.vwap.toFixed(2)}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">RSI</div>
                        <div class="metric-value">${stock.rsi.toFixed(2)}</div>
                    </div>
                </div>
            </div>

            <div class="analysis-section">
                <h2>🎯 סט-אפ לפי Ross Cameron</h2>
                <div style="margin: 15px 0;">
                    <span class="setup-badge ${setup.setup_valid ? 'valid' : 'invalid'}">
                        ${setup.setup_type || 'אין סט-אפ'}
                    </span>
                </div>

                ${setup.setup_valid ? '<h3>✅ קריטריונים שהתקיימו</h3>' : ''}
                ${criteriaMetHtml}

                ${setup.criteria_failed.length > 0 ? '<h3>❌ קריטריונים שלא התקיימו</h3>' : ''}
                ${criteriaFailedHtml}

                ${tradePlanHtml}
            </div>

            ${aiAnalysisHtml}

            <div class="analysis-section">
                <h2>📈 גרף</h2>
                <div id="chart-container" class="chart-container">
                    <p style="text-align: center; padding: 40px;">טוען גרף...</p>
                </div>
            </div>

            <div style="background: #fff3cd; padding: 15px; border-radius: 8px; margin-top: 20px; border: 2px solid #ffc107;">
                <strong>⚠️ דיסקליימר:</strong> זהו ניתוח חינוכי כללי לפי עקרונות מומנטום של רוס קמרון.
                אין לראות בכך ייעוץ השקעות אישי. קבל החלטות בהתאם לשיקול דעתך ובאחריותך.
            </div>
        `;

        modal.style.display = 'flex';
    }

    async loadChart(symbol) {
        try {
            const response = await fetch(`/api/chart/${symbol}?period=5d`);
            const data = await response.json();

            if (data.success) {
                this.renderChart(data.data);
            }
        } catch (error) {
            console.error('Error loading chart:', error);
        }
    }

    renderChart(chartData) {
        const container = document.getElementById('chart-container');

        // Candlestick trace
        const candlestick = {
            x: chartData.timestamps,
            open: chartData.open,
            high: chartData.high,
            low: chartData.low,
            close: chartData.close,
            type: 'candlestick',
            name: 'Price',
            yaxis: 'y'
        };

        // VWAP
        const vwap = {
            x: chartData.timestamps,
            y: chartData.vwap,
            type: 'scatter',
            mode: 'lines',
            name: 'VWAP',
            line: { color: 'orange', width: 2 },
            yaxis: 'y'
        };

        // EMA 9
        const ema9 = {
            x: chartData.timestamps,
            y: chartData.ema_9,
            type: 'scatter',
            mode: 'lines',
            name: 'EMA 9',
            line: { color: 'blue', width: 2 },
            yaxis: 'y'
        };

        // EMA 20
        const ema20 = {
            x: chartData.timestamps,
            y: chartData.ema_20,
            type: 'scatter',
            mode: 'lines',
            name: 'EMA 20',
            line: { color: 'red', width: 2 },
            yaxis: 'y'
        };

        // Volume
        const volume = {
            x: chartData.timestamps,
            y: chartData.volume,
            type: 'bar',
            name: 'Volume',
            yaxis: 'y2',
            marker: { color: 'rgba(102, 126, 234, 0.3)' }
        };

        const layout = {
            title: '',
            xaxis: { rangeslider: { visible: false } },
            yaxis: { title: 'Price', side: 'right' },
            yaxis2: {
                title: 'Volume',
                overlaying: 'y',
                side: 'left',
                showgrid: false
            },
            height: 500,
            margin: { r: 60, l: 60 }
        };

        Plotly.newPlot(container, [candlestick, vwap, ema9, ema20, volume], layout);
    }

    translateConfidence(confidence) {
        const translations = {
            'high': 'גבוהה 🔥',
            'medium': 'בינונית ⚡',
            'low': 'נמוכה ⚠️',
            'none': 'אין'
        };
        return translations[confidence] || confidence;
    }

    formatVolume(volume) {
        if (volume >= 1000000) {
            return (volume / 1000000).toFixed(1) + 'M';
        } else if (volume >= 1000) {
            return (volume / 1000).toFixed(1) + 'K';
        }
        return volume.toString();
    }

    showLoading(show) {
        document.getElementById('loading').style.display = show ? 'block' : 'none';
    }

    showError(message) {
        const container = document.getElementById('results-container');
        container.innerHTML = `
            <div style="grid-column: 1 / -1; background: #f8d7da; color: #721c24; padding: 20px; border-radius: 10px; text-align: center;">
                <h3>❌ שגיאה</h3>
                <p>${message}</p>
            </div>
        `;
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new MomentumTraderApp();
});
