import numpy as np
import pandas as pd

class FIREPlanner:
    def __init__(self, current_savings, monthly_invest, target_corpus):
        self.current_savings = current_savings
        self.monthly_invest = monthly_invest
        self.target_corpus = target_corpus

    def run_monte_carlo(self, years=25, iterations=1000, avg_return=0.12, std_dev=0.15):
        """
        Simulates 1000 market paths to find the probability of reaching FIRE.
        avg_return: 12% (Typical Indian Equity)
        std_dev: 15% (Market Volatility)
        """
        results = []
        
        for _ in range(iterations):
            path = [self.current_savings]
            for year in range(years):
                # Generate a random annual return based on normal distribution
                annual_market_return = np.random.normal(avg_return, std_dev)
                
                # Formula: (Balance + Annual SIP) * (1 + Market Return)
                new_balance = (path[-1] + (self.monthly_invest * 12)) * (1 + annual_market_return)
                path.append(max(0, new_balance))
            results.append(path)
        
        # Convert to DataFrame for percentile analysis
        df_results = pd.DataFrame(results).T
        
        # Calculate the 3D Path Data: Median, Optimistic (75th), and Pessimistic (25th)
        projection_data = {
            "years": list(range(2026, 2026 + years + 1)),
            "median_path": df_results.median(axis=1).tolist(),
            "safe_path": df_results.quantile(0.25, axis=1).tolist(),
            "dream_path": df_results.quantile(0.75, axis=1).tolist(),
            "success_probability": float((df_results.iloc[-1] >= self.target_corpus).mean() * 100)
        }
        
        return projection_data