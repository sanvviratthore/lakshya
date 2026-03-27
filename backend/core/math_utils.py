import pandas as pd
import numpy as np
from pyxirr import xirr
from datetime import datetime

class FinancialEngine:
    @staticmethod
    def calculate_xirr(transactions):
        """
        Calculates the true annualized return.
        Formula: $$ \sum_{i=1}^{N} \frac{P_i}{(1 + r)^{\frac{d_i - d_1}{365}}} = 0 $$
        """
        if not transactions:
            return 0.0
            
        # Ensure dates are datetime objects and amounts are floats
        dates = [pd.to_datetime(t['date']) for t in transactions]
        amounts = [float(t['amount']) for t in transactions]
        
        try:
            result = xirr(dates, amounts)
            # Handle cases where XIRR might return None or an error
            return result if result is not None else 0.0
        except Exception:
            return 0.0

    @staticmethod
    def calculate_hhi_diversification(holdings):
        """
        HHI (Herfindahl-Hirschman Index) measures concentration.
        Lower HHI = Better Diversified.
        """
        if not holdings:
            return 0
            
        # weights should be percentages (e.g., 10 for 10%)
        weights = [float(h.get('weight', 0)) for h in holdings]
        total_weight = sum(weights)
        
        if total_weight == 0: return 0
        
        # Normalize weights so they sum to 1
        normalized_weights = [w / total_weight for w in weights]
        hhi = sum([w**2 for w in normalized_weights])
        
        # Finance logic: HHI < 0.15 is 'Diversified', > 0.25 is 'Concentrated'
        # We convert this to a 0-100 Score for the UI
        score = max(0, min(100, 100 - (hhi * 400))) 
        return round(score, 2)

    @staticmethod
    def calculate_overlap(fund_a_stocks, fund_b_stocks):
        """
        Quantifies 'Clone' risk between two funds.
        """
        common_stocks = set(fund_a_stocks.keys()) & set(fund_b_stocks.keys())
        overlap = sum(min(fund_a_stocks[s], fund_b_stocks[s]) for s in common_stocks)
        return round(overlap, 2)

    @staticmethod
    def fire_projection(current_nw, monthly_sip, annual_return, inflation, years):
        """
        A deterministic path for comparison against the Monte Carlo simulation.
        Uses the Inflation-Adjusted (Real) Return.
        """
        path = []
        # Real Rate of Return formula: ((1 + nominal) / (1 + inflation)) - 1
        real_return = ((1 + annual_return) / (1 + inflation)) - 1
        
        # Year zero (Today)
        path.append({"year": 2026, "value": round(current_nw, 2)})
        
        for year in range(1, years + 1):
            # Compound Interest Formula for Lumpsum + SIP
            future_val = (current_nw * (1 + real_return)**year) + \
                         (monthly_sip * 12 * (((1 + real_return)**year - 1) / real_return))
            path.append({"year": 2026 + year, "value": round(future_val, 2)})
            
        return path