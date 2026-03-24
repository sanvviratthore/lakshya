import pandas as pd

class PortfolioXRay:
    def __init__(self, holdings_data):
        """
        holdings_data: List of dicts 
        [{'fund': 'HDFC Top 100', 'stocks': {'RELIANCE': 9.2, 'HDFC': 8.1...}, 'type': 'Regular'}]
        """
        self.holdings = holdings_data

    def calculate_overlap_matrix(self):
        """
        Compares every fund against every other fund to find 'Clones'.
        """
        overlap_results = []
        fund_names = [h['fund'] for h in self.holdings]
        
        for i in range(len(self.holdings)):
            for j in range(i + 1, len(self.holdings)):
                fund_a = self.holdings[i]
                fund_b = self.holdings[j]
                
                common_stocks = set(fund_a['stocks'].keys()) & set(fund_b['stocks'].keys())
                overlap_pct = sum(min(fund_a['stocks'][s], fund_b['stocks'][s]) for s in common_stocks)
                
                if overlap_pct > 30: # 30% is a common threshold for 'Too Similar'
                    overlap_results.append({
                        "pair": f"{fund_a['fund']} & {fund_b['fund']}",
                        "overlap": round(overlap_pct, 2),
                        "verdict": "High Overlap - Consider Consolidating"
                    })
        return overlap_results

    def detect_regular_to_direct_savings(self):
        """
        Calculates how much money is 'leaking' due to Regular Plan commissions.
        """
        savings_leak = 0
        for fund in self.holdings:
            if fund.get('type') == 'Regular':
                # Avg difference in India between Regular and Direct is ~1%
                leak = fund.get('current_value', 0) * 0.01 
                savings_leak += leak
        
        return {
            "annual_leak": round(savings_leak, 2),
            "10_year_loss": round(savings_leak * 15.93, 2) # Includes 10% compounded growth
        }