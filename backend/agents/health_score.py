class MoneyHealthScore:
    def __init__(self, portfolio_metrics, profile_data):
        # portfolio_metrics: data from their actual investments (XIRR, etc.)
        # profile_data: data from their user profile (Insurance, Expenses, etc.)
        self.metrics = portfolio_metrics
        self.profile = profile_data

    def get_comprehensive_score(self):
        # 1. Emergency Fund (Target: 6 months of expenses)
        monthly_exp = self.profile.get('monthly_expenses', 1)
        if monthly_exp <= 0: monthly_exp = 1 # Avoid division by zero
        
        ef_score = min(100, (self.profile.get('liquid_cash', 0) / (monthly_exp * 6)) * 100)

        # 2. Insurance (Binary check: Term + Health)
        ins_score = (50 if self.profile.get('has_term_insurance') else 0) + \
                    (50 if self.profile.get('has_health_insurance') else 0)

        # 3. Diversification
        div_score = self.metrics.get('diversification_score', 50)

        # 4. Tax Efficiency (Using ELSS/80C)
        tax_score = 100 if self.profile.get('uses_elss') or self.profile.get('uses_80c') else 50

        # 5. Return vs Benchmark (Using XIRR)
        xirr = self.metrics.get('xirr', 0)
        ret_score = 100 if xirr >= 0.12 else 70 if xirr >= 0.08 else 40

        # 6. Low Cost (Direct vs Regular Mutual Funds)
        cost_score = 100 if self.metrics.get('percent_direct', 0) > 80 else 50

        scores = {
            "Emergency Fund": round(ef_score, 2),
            "Insurance": ins_score,
            "Diversification": div_score,
            "Tax Efficiency": tax_score,
            "Return vs Benchmark": ret_score,
            "Low Cost": cost_score
        }

        final = sum(scores.values()) / len(scores)
        
        return {
            "final_overall_score": round(final, 2),
            "breakdown": scores,
            "status": "Healthy" if final > 75 else "Needs Attention" if final > 50 else "Critical",
            "color_code": "#2ecc71" if final > 75 else "#f1c40f" if final > 50 else "#e74c3c"
        }