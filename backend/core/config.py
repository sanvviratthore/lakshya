import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_KEY = os.getenv("OPENAI_API_KEY")
    LLAMA_CLOUD_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
    INFLATION_RATE = 0.06
    EQUITY_EXPECTED_RETURN = 0.12
    DEBT_EXPECTED_RETURN = 0.07
    SPATIAL_SCALE_FACTOR = 0.0001