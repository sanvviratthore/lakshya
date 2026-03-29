from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from agents.portfolio_xray import PortfolioXRay
from agents.health_score import MoneyHealthScore
from agents.fire_planner import FIREPlanner
# Ensure these internal core modules exist or are updated as we discussed
from core.parser import StatementParser
from core.math_utils import FinancialEngine
from core.ai_engine import generate_financial_insights, generate_mentor_chat_reply
import shutil
import os

router = APIRouter()
parser = StatementParser()
engine = FinancialEngine()

@router.post("/auth/login")
async def login(data: dict = Body(...)):
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    # For hackathon simplicity, we'll return a static user object
    return {
        "access_token": "mock_token_for_nitu", 
        "user": {"name": "Nitu", "email": email},
        "status": "authenticated"
    }

@router.post("/analyze-portfolio")
async def analyze_portfolio(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    try:
        # Save uploaded file
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 1. Parse PDF
        raw_data = await parser.parse_statement(temp_path)
        
        # 2. Run X-Ray Agent
        xray = PortfolioXRay(raw_data['holdings'])
        overlap_data = xray.calculate_overlap_matrix()
        leak_data = xray.detect_regular_to_direct_savings()
        
        # 3. Calculate XIRR
        portfolio_xirr = engine.calculate_xirr(raw_data['transactions'])

        return {
            "portfolio_value": round(raw_data['total_value'], 2),
            "xirr": round(portfolio_xirr * 100, 2),
            "holdings_count": len(raw_data['holdings']),
            "overlap_report": overlap_data,
            "savings_potential": leak_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@router.post("/fire-analysis")
async def get_fire_analysis(data: dict = Body(...)):
    try:
        # 1. Run Math Agent (Monte Carlo)
        planner = FIREPlanner(
            current_savings=data.get("current_savings", 0),
            monthly_invest=data.get("monthly_invest", 0),
            target_corpus=data.get("target_corpus", 50000000)
        )
        projection = planner.run_monte_carlo()
        
        # 2. Get AI Insights (This uses your Gemini Key!)
        # Pass projection and any profile data so Gemini is "Context-Aware"
        ai_advice = generate_financial_insights(projection, data.get("profile", {}))
        
        return {
            "status": "success",
            "chart_data": projection,
            "ai_summary": ai_advice
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/comprehensive-health")
async def get_health_score(data: dict = Body(...)):
    # data expects {'metrics': {...}, 'profile': {...}}
    health_agent = MoneyHealthScore(data['metrics'], data['profile'])
    return health_agent.get_comprehensive_score()

@router.post("/mentor-chat")
async def mentor_chat(data: dict = Body(...)):
    messages = data.get("messages", [])
    profile = data.get("profile", None)
    if not isinstance(messages, list) or len(messages) == 0:
        raise HTTPException(status_code=400, detail="Messages are required")

    reply = generate_mentor_chat_reply(messages, profile)
    return {"reply": reply}