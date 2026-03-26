import os
from llama_parse import LlamaParse
from dotenv import load_dotenv

load_dotenv()

class StatementParser:
    def __init__(self):
        self.parser = LlamaParse(api_key=os.getenv("LLAMA_CLOUD_API_KEY"), result_type="markdown", verbose=True, language="en")

    async def parse_statement(self, file_path):
        docs = await self.parser.aload_data(file_path)
        return self._extract_with_llm("\n\n".join([doc.text for doc in docs]))

    def _extract_with_llm(self, text):
        return {"status": "success", "data": "Structured JSON would go here"}