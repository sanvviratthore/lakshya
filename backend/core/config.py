import os
from dotenv import load_dotenv

# Load variables from the .env file in your root folder
load_dotenv()

class Config:
    # --- AI Keys ---
    # Swapped OpenAI for Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    LLAMA_CLOUD_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
    
    # --- Financial Constants (Standard Indian Market Rates) ---
    INFLATION_RATE = 0.06          # 6% Average Inflation
    EQUITY_EXPECTED_RETURN = 0.12  # 12% Nifty 50 Average
    DEBT_EXPECTED_RETURN = 0.07    # 7% FD/Debt Average
    
    # --- Advanced FIRE Parameters ---
    # Adding these makes your 'fire_planner.py' even more realistic
    STEP_UP_PERCENT = 0.05         # Assuming 5% annual increase in SIP
    CAPITAL_GAINS_TAX = 0.125      # Updated LTCG Tax (12.5% as per 2024/25 rules)
    
    # --- UI/UX Constants ---
    SPATIAL_SCALE_FACTOR = 0.0001
    APP_NAME = "Lakshya AI"
    VERSION = "1.0.0"

    @classmethod
    def validate_keys(cls):
        """Check if essential keys are missing at startup"""
        if not cls.GEMINI_API_KEY:
            print("⚠️ WARNING: GEMINI_API_KEY is missing in .env file!")