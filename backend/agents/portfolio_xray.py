class PortfolioXRay:
    def __init__(self, holdings_data):
        # holdings_data is a list of dicts: [{'fund': 'HDFC Top 100', 'stocks': {'RELIANCE': 10, ...}, 'type': 'Regular', 'current_value': 500000}, ...]
        self.holdings = holdings_data

    def calculate_overlap_matrix(self):
        overlaps = []
        n = len(self.holdings)
        
        for i in range(n):
            for j in range(i + 1, n):
                fund_a = self.holdings[i]
                fund_b = self.holdings[j]
                
                # Find common stocks between the two funds
                common_stocks = set(fund_a['stocks'].keys()) & set(fund_b['stocks'].keys())
                
                # Calculate the weighted overlap percentage
                overlap_pct = sum(min(fund_a['stocks'].get(s, 0), fund_b['stocks'].get(s, 0)) for s in common_stocks)
                
                if overlap_pct > 20:  # Lowered threshold to 20% to catch more issues
                    overlaps.append({
                        "pair": f"{fund_a['fund']} & {fund_b['fund']}",
                        "overlap": round(overlap_pct, 2),
                        "verdict": "Critical Overlap" if overlap_pct > 40 else "High Overlap",
                        "suggestion": "You are paying two sets of fees for the same stocks. Consider consolidating."
                    })
        return overlaps

    def detect_regular_to_direct_savings(self):
        """
        Calculates how much is lost to 'Regular' fund commissions (approx 1% extra per year).
        15.93 is the factor for 10 years of compounding at 12% vs 11%.
        """
        annual_leak = sum(f.get('current_value', 0) * 0.01 for f in self.holdings if f.get('type', '').lower() == 'regular')
        
        return {
            "annual_leak": round(annual_leak, 2),
            "ten_year_opportunity_cost": round(annual_leak * 15.93, 2),
            "status": "Action Required" if annual_leak > 0 else "Optimized",
            "message": f"Switching to Direct plans could save you ₹{round(annual_leak, 2)} every year."
        }