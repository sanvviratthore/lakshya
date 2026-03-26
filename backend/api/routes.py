from fastapi import APIRouter, UploadFile, File, HTTPException
from core.parser import StatementParser
from core.math_utils import FinancialEngine
from agents.portfolio_xray import PortfolioXRay
from agents.health_score import MoneyHealthScore
from agents.fire_planner import FIREPlanner
from core.auth_utils import create_access_token
from core.ai_engine import generate_financial_insights
import shutil, os

router = APIRouter()
parser, engine = StatementParser(), FinancialEngine()

@router.post("/auth/login")
async def login(data: dict):
    if email := data.get("email"):
        return {"access_token": create_access_token({"sub": email}), "token_type": "bearer", "user": "Nitu"}
    raise HTTPException(status_code=400, detail="Invalid email")

@router.post("/analyze-portfolio")
async def analyze_portfolio(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer: shutil.copyfileobj(file.file, buffer)
    try:
        raw_data = await parser.parse_statement(temp_path)
        xray = PortfolioXRay(raw_data['holdings'])
        return {"portfolio_value": raw_data['total_value'], "xirr": f"{round(engine.calculate_xirr(raw_data['transactions']) * 100, 2)}%", 
                "overlap_report": xray.calculate_overlap_matrix(), "annual_savings_potential": xray.detect_regular_to_direct_savings()['annual_leak'], 
                "holdings_count": len(raw_data['holdings'])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

@router.post("/get-health-score")
async def get_health_score(user_data: dict):
    return MoneyHealthScore(user_data['metrics'], user_data['profile']).get_comprehensive_score()

@router.post("/fire-analysis")
async def get_fire_analysis(data: dict):
    try:
        planner = FIREPlanner(float(data.get("current_savings", 0)), float(data.get("monthly_invest", 0)), float(data.get("target_corpus", 50000000)))
        projection = planner.run_monte_carlo()
        return {"status": "success", "chart_data": projection, "ai_summary": generate_financial_insights(projection)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))