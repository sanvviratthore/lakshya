import os
import json
import google.generativeai as genai
try:
    from llama_parse import LlamaParse
except RuntimeError:
    LlamaParse = None
except ImportError:
    LlamaParse = None
from core.config import Config
from dotenv import load_dotenv

load_dotenv()

class StatementParser:
    def __init__(self):
        # LlamaParse handles the heavy lifting of PDF-to-Markdown
        if LlamaParse is not None:
            self.parser = LlamaParse(
                api_key=Config.LLAMA_CLOUD_KEY, 
                result_type="markdown", 
                verbose=True, 
                language="en"
            )
        else:
            self.parser = None
            print("WARNING: LlamaParse could not be loaded. PDF parsing will fail.")
        # Gemini handles the "Thinking" to structure the data
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')

    async def parse_statement(self, file_path):
        """Processes the PDF and returns structured portfolio data."""
        try:
            # 1. Convert PDF to Markdown using Llama Cloud
            docs = await self.parser.aload_data(file_path)
            full_text = "\n\n".join([doc.text for doc in docs])
            
            # 2. Extract structured data using Gemini
            return self._extract_with_gemini(full_text)
        except Exception as e:
            print(f"Parsing Error: {str(e)}")
            raise Exception("Could not parse the investment statement.")

    def _extract_with_gemini(self, text):
        """Uses Gemini to turn raw text into the JSON format the Agents need."""
        prompt = f"""
        Extract investment data from this financial statement. Return ONLY a JSON object.
        JSON Structure:
        {{
            "total_value": float,
            "holdings": [
                {{
                    "fund": "Name of Mutual Fund",
                    "type": "Direct" or "Regular",
                    "current_value": float,
                    "stocks": {{"STOCK_NAME": weight_percentage, ...}}
                }}
            ],
            "transactions": [
                {{"date": "YYYY-MM-DD", "amount": float}}
            ]
        }}
        
        If stock weights aren't visible, estimate top 3 holdings based on fund name.
        Text to parse:
        {text[:8000]} 
        """
        
        response = self.model.generate_content(prompt)
        
        # Clean the response to ensure it's pure JSON
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)