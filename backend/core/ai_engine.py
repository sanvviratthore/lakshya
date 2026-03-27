import google.generativeai as genai
from core.config import Config

# Configure the Gemini Model
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_financial_insights(projection_data, profile_data=None):
    """
    This is the function routes.py is looking for.
    It takes the Monte Carlo results and turns them into a strategy.
    """
    # Extract some basic stats for the prompt
    prob = projection_data.get('success_probability', 'N/A')
    
    prompt = f"""
    You are Lakshya AI, a premium financial strategist.
    
    DATA POINTS:
    - FIRE Success Probability: {prob}%
    - User Profile: {profile_data if profile_data else 'General Investor'}
    
    TASK:
    Provide a concise, 3-sentence financial verdict. 
    1. Tell them if they are on track.
    2. Give one specific tip to improve their 'Wealth Velocity'.
    3. End with a bold, professional sign-off.
    
    Tone: Sophisticated, Direct, and High-End.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lakshya AI is currently analyzing market patterns. (Error: {str(e)})"