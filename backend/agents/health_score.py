class MoneyHealthScore:
    def __init__(self, portfolio_metrics, profile_data):
        self.metrics = portfolio_metrics # XIRR, Diversification, etc.
        self.profile = profile_data # Age, Emergency Fund status

    def get_comprehensive_score(self):
        """
        Weights 6 key dimensions of Indian Personal Finance.
        """
        scores = {
            "Emergency Fund": self._score_emergency_fund(),
            "Insurance": self._score_insurance(),
            "Diversification": self.metrics.get('diversification_score', 50),
            "Tax Efficiency": self._score_tax(),
            "Return vs Benchmark": self._score_performance(),
            "Low Cost (Direct vs Reg)": self._score_costs()
        }
        
        # Calculate Weighted Average
        final_score = sum(scores.values()) / len(scores)
        
        return {
            "final_overall_score": round(final_score, 2),
            "breakdown": scores,
            "color_code": "Green" if final_score > 75 else "Yellow" if final_score > 50 else "Red"
        }

    def _score_emergency_fund(self):
        # Ideal: 6 months of expenses
        ratio = self.profile.get('liquid_cash', 0) / (self.profile.get('monthly_expenses', 1) * 6)
        return min(100, ratio * 100)

    def _score_insurance(self):
        # Simple check: Do they have Term and Health insurance?
        score = 0
        if self.profile.get('has_term_insurance'): score += 50
        if self.profile.get('has_health_insurance'): score += 50
        return score

    def _score_performance(self):
        # Performance relative to Nifty 50 (Assume 12% benchmark)
        xirr = self.metrics.get('xirr', 0)
        if xirr >= 0.12: return 100
        if xirr >= 0.08: return 70
        return 40

    def _score_tax(self):
        # Are they using 80C (ELSS)?
        return 100 if self.profile.get('uses_elss') else 50
    
    def _score_costs(self):
        # Regular funds = 50, Direct funds = 100
        return 100 if self.metrics.get('percent_direct') > 80 else 50