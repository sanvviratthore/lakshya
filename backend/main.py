import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router
from core.config import Config

app = FastAPI(
    title="Lakshya AI Backend",
    description="AI-Powered Financial Strategy Engine",
    version="1.0.0"
)

# --- CORS Settings ---
# This is CRITICAL. Without this, your frontend (8080) 
# won't be allowed to talk to your backend (8000).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For hackathon, allow all. For production, specify http://localhost:8080
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include Routes ---
# This pulls in all the logic from your routes.py
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Lakshya AI Systems Online",
        "status": "Ready",
        "engine": "Gemini-1.5-Flash"
    }

if __name__ == "__main__":
    # Validate keys before starting
    Config.validate_keys()
    
    # Run the server
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)