class PortfolioXRay:
    def __init__(self, holdings_data):
        self.holdings = holdings_data

    def calculate_overlap_matrix(self):
        return [{"pair": f"{self.holdings[i]['fund']} & {self.holdings[j]['fund']}", 
                 "overlap": round(sum(min(self.holdings[i]['stocks'].get(s, 0), self.holdings[j]['stocks'].get(s, 0)) for s in set(self.holdings[i]['stocks'].keys()) & set(self.holdings[j]['stocks'].keys())), 2),
                 "verdict": "High Overlap - Consider Consolidating"} 
                for i in range(len(self.holdings)) for j in range(i + 1, len(self.holdings)) 
                if sum(min(self.holdings[i]['stocks'].get(s, 0), self.holdings[j]['stocks'].get(s, 0)) for s in set(self.holdings[i]['stocks'].keys()) & set(self.holdings[j]['stocks'].keys())) > 30]

    def detect_regular_to_direct_savings(self):
        leak = sum(f.get('current_value', 0) * 0.01 for f in self.holdings if f.get('type') == 'Regular')
        return {"annual_leak": round(leak, 2), "10_year_loss": round(leak * 15.93, 2)}