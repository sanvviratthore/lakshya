import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv(Path('D:/lakshya/.env'))
print('GOOGLE_API_KEY set:', bool(os.getenv('GOOGLE_API_KEY')))

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(model.name)
