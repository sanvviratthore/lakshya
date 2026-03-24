import pandas as pd
import numpy as np
from pyxirr import xirr

class FinancialEngine:
    @staticmethod
    def calculate_xirr(transactions):
        """
        Calculates the true annualized return.
        Formula: $\sum_{i=1}^{N} \frac{P_i}{(1 + r)^{\frac{d_i - d_1}{365}}} = 0$
        'transactions' should be a list of dicts: [{'date': date, 'amount': -1000}, ...]
        """
        dates = [t['date'] for t in transactions]
        amounts = [t['amount'] for t in transactions]
        try:
            return xirr(dates, amounts)
        except Exception:
            return 0.0

    @staticmethod
    def calculate_hhi_diversification(weights):
        """
        Calculates diversification using HHI. 
        Higher HHI = High Concentration (Bad).
        Lower HHI = Well Diversified (Good).
        """
        # HHI is the sum of the squares of the weights
        hhi = sum([(w / 100)**2 for w in weights])
        
        # Normalize to a 0-100 'Health Score'
        # 0.15 is generally considered a diversified portfolio in finance
        score = max(0, 100 - (hhi * 500)) 
        return round(score, 2)

    @staticmethod
    def calculate_overlap(fund_a_holdings, fund_b_holdings):
        """
        Quantifies how much two funds are 'clones' of each other.
        fund_a_holdings: {'RELIANCE': 10.5, 'HDFC': 8.2, ...}
        """
        common_stocks = set(fund_a_holdings.keys()) & set(fund_b_holdings.keys())
        overlap = sum(min(fund_a_holdings[s], fund_b_holdings[s]) for s in common_stocks)
        return round(overlap, 2)

    @staticmethod
    def fire_projection(current_nw, monthly_sip, annual_return, inflation, years):
        """
        Basic deterministic projection for the FIRE Path.
        Returns a list of values for the 3D 'Spatial Path'.
        """
        path = []
        real_return = (1 + annual_return) / (1 + inflation) - 1
        for year in range(years + 1):
            future_val = current_nw * (1 + real_return)**year + \
                         monthly_sip * 12 * (((1 + real_return)**year - 1) / real_return)
            path.append({"year": 2024 + year, "value": round(future_val, 2)})
        return path