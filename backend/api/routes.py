from fastapi import APIRouter, UploadFile, File, HTTPException
from core.parser import StatementParser
from core.math_utils import FinancialEngine
from agents.portfolio_xray import PortfolioXRay
from agents.health_score import MoneyHealthScore
from agents.fire_planner import FIREPlanner
import shutil
import os

router = APIRouter()

# Initialize global tools
parser = StatementParser()
engine = FinancialEngine()

@router.post("/analyze-portfolio")
async def analyze_portfolio(file: UploadFile = File(...)):
    """
    Endpoint 1: The 'X-Ray'
    Upload CAMS PDF -> Get Overlap, XIRR, and Savings Leak.
    """
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 1. Parse using LlamaCloud
        raw_data = await parser.parse_statement(temp_path)
        
        # 2. Run X-Ray Agent
        xray = PortfolioXRay(raw_data['holdings'])
        overlap = xray.calculate_overlap_matrix()
        leak = xray.detect_regular_to_direct_savings()
        
        # 3. Calculate XIRR
        xirr = engine.calculate_xirr(raw_data['transactions'])

        return {
            "portfolio_value": raw_data['total_value'],
            "xirr": f"{round(xirr * 100, 2)}%",
            "overlap_report": overlap,
            "annual_savings_potential": leak['annual_leak'],
            "holdings_count": len(raw_data['holdings'])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

@router.post("/get-health-score")
async def get_health_score(user_data: dict):
    """
    Endpoint 2: The 'Health Meter'
    Takes portfolio metrics + user profile to give the 0-100 score.
    """
    # portfolio_metrics come from the /analyze-portfolio output
    health_agent = MoneyHealthScore(
        portfolio_metrics=user_data['metrics'],
        profile_data=user_data['profile']
    )
    return health_agent.get_comprehensive_score()

@router.post("/project-fire")
async def project_fire(params: dict):
    """
    Endpoint 3: The 'Spatial Path'
    Runs Monte Carlo simulation for the 3D visualization.
    """
    planner = FIREPlanner(
        current_savings=params['current_savings'],
        monthly_invest=params['monthly_sip'],
        target_corpus=params['target']
    )
    return planner.run_monte_carlo()