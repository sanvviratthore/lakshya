import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY", "YOUR_ACTUAL_KEY_HERE"))
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_financial_insights(projection_results):
    prob = projection_results['success_probability']
    median_end = projection_results['median_path'][-1]
    prompt = f"As Lakshya AI: Success Probability: {prob:.1f}%, Corpus: ₹{median_end:,.0f}. Provide: (1) Verdict (Safe/Risky/Dream), (2) 1 Tactical Move, (3) Encouragement. Be concise."
    try:
        return model.generate_content(prompt).text
    except Exception as e:
        return f"AI Analysis momentarily offline. (Error: {str(e)})"