import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    LLAMA_CLOUD_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
    OPENAI_KEY = os.getenv("OPENAI_API_KEY")
    
    # Financial Constants (India Specific)
    INFLATION_RATE = 0.06  # 6% Average
    EQUITY_EXPECTED_RETURN = 0.12
    DEBT_EXPECTED_RETURN = 0.07
    
    # Avataar.ai Config
    SPATIAL_SCALE_FACTOR = 0.0001 # To scale ₹ crores into 3D units