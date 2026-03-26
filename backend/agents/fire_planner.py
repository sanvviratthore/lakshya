import numpy as np, pandas as pd

class FIREPlanner:
    def __init__(self, current_savings, monthly_invest, target_corpus):
        self.current, self.monthly, self.target = current_savings, monthly_invest, target_corpus

    def run_monte_carlo(self, years=25, iterations=1000, avg_return=0.12, std_dev=0.15):
        results = []
        for _ in range(iterations):
            path = [self.current]
            for _ in range(years):
                path.append(max(0, (path[-1] + self.monthly * 12) * (1 + np.random.normal(avg_return, std_dev))))
            results.append(path)
        df = pd.DataFrame(results).T
        return {"years": list(range(2026, 2026 + years + 1)), "median_path": df.median(axis=1).tolist(), 
                "safe_path": df.quantile(0.25, axis=1).tolist(), "dream_path": df.quantile(0.75, axis=1).tolist(),
                "success_probability": float((df.iloc[-1] >= self.target).mean() * 100)}