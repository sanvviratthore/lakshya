import numpy as np
import pandas as pd

class FIREPlanner:
    def __init__(self, current_savings, monthly_invest, target_corpus):
        # Ensure these are floats to avoid calculation errors
        self.current = float(current_savings)
        self.monthly = float(monthly_invest)
        self.target = float(target_corpus)

    def run_monte_carlo(self, years=25, iterations=1000, avg_return=0.12, std_dev=0.15):
        results = []
        for _ in range(iterations):
            path = [self.current]
            for _ in range(years):
                # Simple and effective Monte Carlo step
                market_return = np.random.normal(avg_return, std_dev)
                next_val = (path[-1] + self.monthly * 12) * (1 + market_return)
                path.append(max(0, next_val))
            results.append(path)
        
        df = pd.DataFrame(results).T
        
        # We round to 2 decimal places so the Chart.js tooltips look clean
        return {
            "years": list(range(2026, 2026 + years + 1)),
            "median_path": [round(x, 2) for x in df.median(axis=1).tolist()],
            "safe_path": [round(x, 2) for x in df.quantile(0.25, axis=1).tolist()],
            "dream_path": [round(x, 2) for x in df.quantile(0.75, axis=1).tolist()],
            "success_probability": round(float((df.iloc[-1] >= self.target).mean() * 100), 2)
        }