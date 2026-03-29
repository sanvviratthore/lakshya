import google.generativeai as genai
from core.config import Config

# Configure the Gemini Model
genai.configure(api_key=Config.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')

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

def generate_mentor_chat_reply(messages, profile_data=None):
    """
    Turn a short conversation history into a single Lakshya reply.
    Expects messages as a list of { role: 'user'|'assistant', content: str }.
    """
    if not isinstance(messages, list) or not messages:
        return "I am here whenever you need me. Ask me anything about SIPs, FIRE, tax, or insurance."

    conversation_lines = []
    for msg in messages:
        role = (msg.get('role') or '').strip().lower()
        content = (msg.get('content') or '').strip()
        if not content:
            continue
        if role == 'assistant':
            conversation_lines.append(f"Lakshya: {content}")
        else:
            conversation_lines.append(f"User: {content}")

    conversation = "\n".join(conversation_lines[-12:])
    profile_blurb = profile_data if profile_data else "General Investor"

    prompt = f"""
You are Lakshya AI, a premium financial strategist.
User Profile: {profile_blurb}

Conversation so far:
{conversation}

Reply as Lakshya in 3-5 concise sentences. Be direct, helpful, and avoid disclaimers.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lakshya AI is currently analyzing market patterns. (Error: {str(e)})"