"""
Ross Cameron / Warrior Trading Setup Detection
"""
import pandas as pd
from typing import Dict, List, Optional, Tuple
from enum import Enum


class SetupType(Enum):
    """Ross Cameron setup types"""
    GAP_AND_GO = "Gap & Go"
    RED_TO_GREEN = "Red to Green"
    FIRST_GREEN_DAY = "First Green Day"
    MICRO_PULLBACK = "Micro Pullback"
    BULL_FLAG = "Bull Flag"
    NONE = "No Setup"


class RossCameronAnalyzer:
    """Detect Ross Cameron momentum setups"""

    def __init__(self):
        self.min_rvol = 2.0
        self.min_gap_percent = 3.0

    def analyze_setup(self, stock_data: Dict, historical_df: Optional[pd.DataFrame] = None) -> Dict:
        """
        Analyze stock for Ross Cameron setups

        Returns:
            Dictionary with setup analysis
        """

        if not stock_data.get('data_available'):
            return self._no_setup("נתונים לא זמינים")

        setup_results = {
            'setup_type': None,
            'setup_valid': False,
            'criteria_met': [],
            'criteria_failed': [],
            'entry_point': None,
            'stop_loss': None,
            'targets': [],
            'risk_reward': None,
            'confidence': 'low'
        }

        # Check each setup type
        gap_and_go = self._check_gap_and_go(stock_data)
        red_to_green = self._check_red_to_green(stock_data)
        first_green = self._check_first_green_day(stock_data, historical_df)
        micro_pullback = self._check_micro_pullback(stock_data, historical_df)
        bull_flag = self._check_bull_flag(stock_data, historical_df)

        # Pick best setup
        setups = [
            (gap_and_go, SetupType.GAP_AND_GO),
            (red_to_green, SetupType.RED_TO_GREEN),
            (first_green, SetupType.FIRST_GREEN_DAY),
            (micro_pullback, SetupType.MICRO_PULLBACK),
            (bull_flag, SetupType.BULL_FLAG)
        ]

        best_setup = None
        max_score = 0

        for setup_check, setup_type in setups:
            if setup_check['valid'] and setup_check['score'] > max_score:
                max_score = setup_check['score']
                best_setup = (setup_check, setup_type)

        if best_setup:
            setup_check, setup_type = best_setup
            setup_results.update({
                'setup_type': setup_type.value,
                'setup_valid': True,
                'criteria_met': setup_check['criteria_met'],
                'criteria_failed': setup_check['criteria_failed'],
                'entry_point': setup_check['entry'],
                'stop_loss': setup_check['stop'],
                'targets': setup_check['targets'],
                'risk_reward': setup_check['risk_reward'],
                'confidence': setup_check['confidence']
            })

        return setup_results

    def _check_gap_and_go(self, data: Dict) -> Dict:
        """Check for Gap & Go setup"""

        score = 0
        criteria_met = []
        criteria_failed = []

        # Must have significant gap
        gap = data.get('gap_percent', 0)
        if abs(gap) >= self.min_gap_percent:
            criteria_met.append(f"גאפ משמעותי: {gap:.1f}%")
            score += 3
        else:
            criteria_failed.append(f"גאפ לא מספיק: {gap:.1f}%")

        # High relative volume
        rvol = data.get('rvol', 0)
        if rvol >= self.min_rvol:
            criteria_met.append(f"RVOL גבוה: {rvol:.1f}x")
            score += 2
        else:
            criteria_failed.append(f"RVOL נמוך: {rvol:.1f}x")

        # Price above VWAP
        price = data.get('current_price', 0)
        vwap = data.get('vwap', 0)
        if price > vwap:
            criteria_met.append("מחיר מעל VWAP")
            score += 1
        else:
            criteria_failed.append("מחיר מתחת VWAP")

        # Price above EMA9
        ema9 = data.get('ema_9', 0)
        if price > ema9:
            criteria_met.append("מחיר מעל EMA9")
            score += 1

        valid = score >= 5

        # Calculate entry, stop, targets
        entry = round(max(vwap, ema9) * 1.01, 2)  # 1% above VWAP/EMA9
        stop = round(min(vwap, ema9) * 0.99, 2)   # 1% below
        risk = entry - stop

        targets = [
            round(entry + risk * 1.5, 2),  # 1.5R
            round(entry + risk * 2.5, 2),  # 2.5R
            round(entry + risk * 4, 2)     # 4R
        ]

        confidence = 'high' if score >= 6 else 'medium' if score >= 5 else 'low'

        return {
            'valid': valid,
            'score': score,
            'criteria_met': criteria_met,
            'criteria_failed': criteria_failed,
            'entry': entry,
            'stop': stop,
            'targets': targets,
            'risk_reward': f"1:{(targets[1]-entry)/risk:.1f}",
            'confidence': confidence
        }

    def _check_red_to_green(self, data: Dict) -> Dict:
        """Check for Red to Green Move setup"""

        score = 0
        criteria_met = []
        criteria_failed = []

        # Started red (negative gap or down day)
        gap = data.get('gap_percent', 0)
        change = data.get('change_percent', 0)

        started_red = gap < 0 or change < 0
        if started_red:
            criteria_met.append("התחיל באדום")
            score += 2

        # Now turning green
        if change > 0:
            criteria_met.append("הופך לירוק")
            score += 3
        else:
            criteria_failed.append("עדיין לא ירוק")

        # High volume
        rvol = data.get('rvol', 0)
        if rvol >= 2.5:
            criteria_met.append(f"נפח גבוה: {rvol:.1f}x")
            score += 2
        else:
            criteria_failed.append("נפח לא מספיק")

        # Breaking VWAP
        price = data.get('current_price', 0)
        vwap = data.get('vwap', 0)
        prev_close = data.get('previous_close', 0)

        if price > prev_close:
            criteria_met.append("מעל מחיר סגירה קודם")
            score += 2

        valid = score >= 6

        entry = round(prev_close * 1.005, 2)  # 0.5% above previous close
        stop = round(data.get('day_low', price * 0.98), 2)
        risk = entry - stop

        targets = [
            round(entry + risk * 2, 2),
            round(entry + risk * 3, 2),
            round(entry + risk * 5, 2)
        ]

        confidence = 'high' if score >= 7 else 'medium' if score >= 6 else 'low'

        return {
            'valid': valid,
            'score': score,
            'criteria_met': criteria_met,
            'criteria_failed': criteria_failed,
            'entry': entry,
            'stop': stop,
            'targets': targets,
            'risk_reward': f"1:{(targets[1]-entry)/risk:.1f}",
            'confidence': confidence
        }

    def _check_first_green_day(self, data: Dict, historical_df: Optional[pd.DataFrame]) -> Dict:
        """Check for First Green Day setup"""

        score = 0
        criteria_met = []
        criteria_failed = []

        # Need historical data to confirm previous red days
        if historical_df is None or historical_df.empty:
            return {
                'valid': False,
                'score': 0,
                'criteria_met': [],
                'criteria_failed': ['נדרש מידע היסטורי'],
                'entry': 0,
                'stop': 0,
                'targets': [],
                'risk_reward': '0:0',
                'confidence': 'low'
            }

        # Check if previous days were red
        try:
            daily_changes = historical_df['Close'].pct_change()
            recent_red = (daily_changes[-3:-1] < 0).sum()

            if recent_red >= 2:
                criteria_met.append("2+ ימים אדומים קודמים")
                score += 3
        except:
            pass

        # Today turning green
        change = data.get('change_percent', 0)
        if change > 2:
            criteria_met.append(f"יום ירוק: +{change:.1f}%")
            score += 3
        else:
            criteria_failed.append("לא מספיק ירוק")

        # Volume surge
        rvol = data.get('rvol', 0)
        if rvol >= 2.0:
            criteria_met.append(f"עלייה בנפח: {rvol:.1f}x")
            score += 2

        valid = score >= 6

        price = data.get('current_price', 0)
        entry = round(price * 1.02, 2)
        stop = round(data.get('day_low', price * 0.96), 2)
        risk = entry - stop

        targets = [
            round(entry + risk * 2, 2),
            round(entry + risk * 3, 2),
            round(entry + risk * 5, 2)
        ]

        confidence = 'medium' if score >= 6 else 'low'

        return {
            'valid': valid,
            'score': score,
            'criteria_met': criteria_met,
            'criteria_failed': criteria_failed,
            'entry': entry,
            'stop': stop,
            'targets': targets,
            'risk_reward': f"1:{(targets[1]-entry)/risk:.1f}" if risk > 0 else "0:0",
            'confidence': confidence
        }

    def _check_micro_pullback(self, data: Dict, historical_df: Optional[pd.DataFrame]) -> Dict:
        """Check for Micro Pullback setup"""

        score = 0
        criteria_met = []
        criteria_failed = []

        # Price near EMA9
        price = data.get('current_price', 0)
        ema9 = data.get('ema_9', 0)

        if ema9 > 0:
            distance_from_ema = abs(price - ema9) / ema9
            if distance_from_ema < 0.02:  # Within 2%
                criteria_met.append("קרוב ל-EMA9")
                score += 2

        # Above VWAP
        vwap = data.get('vwap', 0)
        if price > vwap:
            criteria_met.append("מעל VWAP")
            score += 2
        else:
            criteria_failed.append("מתחת VWAP")

        # Strong uptrend
        ema9 = data.get('ema_9', 0)
        ema20 = data.get('ema_20', 0)
        if ema9 > ema20:
            criteria_met.append("EMA9 > EMA20 (אפטרנד)")
            score += 2

        # Good volume
        rvol = data.get('rvol', 0)
        if rvol >= 1.5:
            criteria_met.append(f"נפח טוב: {rvol:.1f}x")
            score += 1

        valid = score >= 5

        entry = round(max(ema9, vwap) * 1.005, 2)
        stop = round(ema9 * 0.98, 2)
        risk = entry - stop

        targets = [
            round(entry + risk * 2, 2),
            round(entry + risk * 3, 2),
            round(entry + risk * 4, 2)
        ]

        confidence = 'high' if score >= 6 else 'medium' if score >= 5 else 'low'

        return {
            'valid': valid,
            'score': score,
            'criteria_met': criteria_met,
            'criteria_failed': criteria_failed,
            'entry': entry,
            'stop': stop,
            'targets': targets,
            'risk_reward': f"1:{(targets[1]-entry)/risk:.1f}" if risk > 0 else "0:0",
            'confidence': confidence
        }

    def _check_bull_flag(self, data: Dict, historical_df: Optional[pd.DataFrame]) -> Dict:
        """Check for Bull Flag setup"""

        score = 0
        criteria_met = []
        criteria_failed = []

        # Need historical data for pattern
        if historical_df is None or historical_df.empty:
            return {
                'valid': False,
                'score': 0,
                'criteria_met': [],
                'criteria_failed': ['נדרש מידע היסטורי'],
                'entry': 0,
                'stop': 0,
                'targets': [],
                'risk_reward': '0:0',
                'confidence': 'low'
            }

        # Check for consolidation after strong move
        try:
            recent_high = historical_df['High'].max()
            current_price = data.get('current_price', 0)

            # Pullback from high
            pullback = (recent_high - current_price) / recent_high
            if 0.05 < pullback < 0.15:  # 5-15% pullback
                criteria_met.append(f"פולבק מהשיא: {pullback*100:.1f}%")
                score += 3
        except:
            pass

        # Volume contraction during consolidation
        rvol = data.get('rvol', 0)
        if 0.5 < rvol < 1.5:
            criteria_met.append("נפח בקונסולידציה")
            score += 2

        # Near support (EMA9 or VWAP)
        price = data.get('current_price', 0)
        ema9 = data.get('ema_9', 0)
        vwap = data.get('vwap', 0)

        support = max(ema9, vwap)
        if abs(price - support) / support < 0.03:
            criteria_met.append("קרוב לתמיכה")
            score += 2

        valid = score >= 5

        entry = round(data.get('day_high', price * 1.01) * 1.005, 2)
        stop = round(support * 0.98, 2)
        risk = entry - stop

        # Bull flag targets are ambitious
        targets = [
            round(entry + risk * 3, 2),
            round(entry + risk * 5, 2),
            round(entry + risk * 8, 2)
        ]

        confidence = 'medium' if score >= 5 else 'low'

        return {
            'valid': valid,
            'score': score,
            'criteria_met': criteria_met,
            'criteria_failed': criteria_failed,
            'entry': entry,
            'stop': stop,
            'targets': targets,
            'risk_reward': f"1:{(targets[1]-entry)/risk:.1f}" if risk > 0 else "0:0",
            'confidence': confidence
        }

    def _no_setup(self, reason: str) -> Dict:
        """Return no setup found"""
        return {
            'setup_type': SetupType.NONE.value,
            'setup_valid': False,
            'criteria_met': [],
            'criteria_failed': [reason],
            'entry_point': None,
            'stop_loss': None,
            'targets': [],
            'risk_reward': None,
            'confidence': 'none'
        }
