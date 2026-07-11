# app/stock_routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.stock_analyzer import full_stock_analysis, format_analysis_for_ai
from app.agent import get_ai_response
from app.database import get_profile
from app.yf_helper import get_info_cached, get_fast_info_cached

router = APIRouter()

# ── Pydantic request models ──────────────────────────────────────
class SessionRequest(BaseModel):
    session_id: str

class StockRequest(BaseModel):
    symbol:     str
    session_id: str

class LearnRequest(BaseModel):
    session_id: str
    topic:      str

class PortfolioAddRequest(BaseModel):
    session_id:    str
    asset_type:    str = "mutual_fund"
    asset_name:    str
    invested:      float
    current_value: float
    monthly_sip:   float = 0

class GoalAddRequest(BaseModel):
    session_id:    str
    title:         str
    target_amount: float
    deadline:      Optional[str] = ""

class GoalUpdateRequest(BaseModel):
    session_id:   str
    goal_id:      int
    saved_amount: float
# ────────────────────────────────────────────────────────────────
@router.post("/analyze-stock")
def analyze_stock(request: StockRequest):
    analysis = full_stock_analysis(request.symbol)
    if "error" in analysis:
        return {"error": analysis["error"]}

    formatted    = format_analysis_for_ai(analysis)
    user_profile = get_profile(request.session_id)
    ai_response  = get_ai_response(
        [{"role": "user", "content": formatted}],
        user_profile
    )
    return {
        "symbol":         analysis["symbol"],
        "company_name":   analysis["company_name"],
        "current_price":  analysis["indicators"]["current_price"],
        "pct_change":     analysis["indicators"]["pct_change"],
        "recommendation": analysis["recommendation"],
        "score":          analysis["score"],
        "targets":        analysis["targets"],
        "indicators":     analysis["indicators"],
        "ai_analysis":    ai_response,
        "analysis_time":  analysis["analysis_time"]
    }


@router.get("/quick-price/{symbol}")
def quick_price(symbol: str):
    from app.stock_analyzer import INDEX_MAP, NSE_SUFFIX
    sym = symbol.upper().strip()
    if sym in INDEX_MAP:
        sym = INDEX_MAP[sym]
    elif not sym.startswith("^") and not sym.endswith(".NS") \
         and not sym.endswith(".BO"):
        sym = sym + NSE_SUFFIX
    try:
        fi = get_fast_info_cached(sym)
        return {
            "symbol":        symbol.upper(),
            "company_name":  sym,
            "current_price": round(float(fi.last_price), 2)
                             if hasattr(fi, "last_price") else 0,
            "sector":        "Index"
        }
    except Exception as e:
        return {"error": str(e), "current_price": 0}


@router.post("/savings-analysis")
def savings_analysis(request: SessionRequest):
    from app.saving_calculator import (
        calculate_savings_plan, format_savings_for_ai
    )
    user_profile = get_profile(request.session_id)
    if not user_profile:
        return {"error": "Profile not found."}
    savings_data = calculate_savings_plan(user_profile)
    if "error" in savings_data:
        return {"error": savings_data["error"]}
    formatted   = format_savings_for_ai(savings_data, user_profile)
    ai_response = get_ai_response(
        [{"role": "user", "content": formatted}], user_profile)
    return {"savings_data": savings_data, "ai_analysis": ai_response}


@router.post("/tax-analysis")
def tax_analysis(request: SessionRequest):
    from app.tax_optimizer import calculate_tax_savings, format_tax_for_ai
    user_profile = get_profile(request.session_id)
    if not user_profile:
        return {"error": "Profile not found."}
    tax_data    = calculate_tax_savings(user_profile)
    formatted   = format_tax_for_ai(tax_data)
    ai_response = get_ai_response(
        [{"role": "user", "content": formatted}], user_profile)
    return {"tax_data": tax_data, "ai_analysis": ai_response}


@router.post("/investment-roadmap")
def investment_roadmap(request: SessionRequest):
    from app.investment_roadmap import generate_roadmap, format_roadmap_for_ai
    user_profile = get_profile(request.session_id)
    if not user_profile:
        return {"error": "Profile not found."}
    roadmap = generate_roadmap(user_profile)
    if "error" in roadmap:
        return {"error": roadmap["error"]}
    formatted   = format_roadmap_for_ai(roadmap)
    ai_response = get_ai_response(
        [{"role": "user", "content": formatted}], user_profile)
    return {"roadmap": roadmap, "ai_analysis": ai_response}


@router.post("/insurance-analysis")
def insurance_analysis(request: SessionRequest):
    from app.insurance_planner import (
        calculate_insurance_needs, format_insurance_for_ai
    )
    user_profile = get_profile(request.session_id)
    if not user_profile:
        return {"error": "Profile not found."}
    insurance_data = calculate_insurance_needs(user_profile)
    formatted      = format_insurance_for_ai(insurance_data)
    ai_response    = get_ai_response(
        [{"role": "user", "content": formatted}], user_profile)
    return {"insurance_data": insurance_data, "ai_analysis": ai_response}


@router.post("/spending-leaks")
def spending_leaks(request: SessionRequest):
    from app.smart_savings_engine import (
        detect_spending_leaks, generate_monthly_tracker,
        format_savings_engine_for_ai
    )
    user_profile = get_profile(request.session_id)
    if not user_profile:
        return {"error": "Profile not found."}
    leak_data   = detect_spending_leaks(user_profile)
    tracker     = generate_monthly_tracker(user_profile)
    formatted   = format_savings_engine_for_ai(leak_data, tracker)
    ai_response = get_ai_response(
        [{"role": "user", "content": formatted}], user_profile)
    return {"leak_data": leak_data, "tracker": tracker,
            "ai_analysis": ai_response}


@router.post("/learn")
def learn_topic(request: LearnRequest):
    from app.investment_educator import (
        get_lesson, format_lesson_for_ai,
        get_learning_path, INVESTMENT_LESSONS
    )
    user_profile = get_profile(request.session_id)
    if not user_profile:
        return {"error": "Profile not found."}
    lesson = get_lesson(request.topic)
    if not lesson:
        return {
            "error":         f"Topic '{request.topic}' not found.",
            "available":     list(INVESTMENT_LESSONS.keys()),
            "learning_path": get_learning_path(user_profile)
        }
    formatted   = format_lesson_for_ai(lesson, user_profile)
    ai_response = get_ai_response(
        [{"role": "user", "content": formatted}], user_profile)
    return {"lesson": lesson, "ai_analysis": ai_response,
            "learning_path": get_learning_path(user_profile)}


@router.post("/daily-tips")
def daily_tips(request: SessionRequest):
    from app.smart_tips_engine import (
        get_daily_tip, get_contextual_alerts, format_tips_for_ai
    )
    user_profile = get_profile(request.session_id)
    if not user_profile:
        return {"error": "Profile not found."}
    daily_tip   = get_daily_tip(user_profile)
    alerts      = get_contextual_alerts(user_profile)
    formatted   = format_tips_for_ai(daily_tip, alerts, user_profile)
    ai_response = get_ai_response(
        [{"role": "user", "content": formatted}], user_profile)
    return {"daily_tip": daily_tip, "alerts": alerts,
            "ai_analysis": ai_response}


@router.post("/health-score")
def health_score(request: SessionRequest):
    from app.health_score import calculate_health_score
    from app.db_manager   import save_snapshot
    user_profile = get_profile(request.session_id)
    if not user_profile:
        return {"error": "Profile not found."}
    score_data = calculate_health_score(user_profile)
    save_snapshot(request.session_id, user_profile, score_data["score"])
    ai_response = get_ai_response(
        conversation_history=[{"role": "user", "content": f"""
Financial health score for {score_data['name']}: {score_data['score']}/100
Grade: {score_data['grade']} — {score_data['label']}
Next action: {score_data['next_action']}
Give a brief motivating analysis. Tell them exactly what to fix first.
        """}],
        user_profile=user_profile
    )
    return {"score_data": score_data, "ai_analysis": ai_response}


@router.get("/health-history/{session_id}")
def health_history(session_id: str):
    from app.db_manager import get_snapshots
    return {"snapshots": get_snapshots(session_id, months=6)}


@router.post("/portfolio/add")
def portfolio_add(request: PortfolioAddRequest):
    from app.db_manager import add_portfolio_item, get_portfolio_summary
    if not get_profile(request.session_id):
        return {"error": "Profile not found."}
    add_portfolio_item(
        request.session_id, request.asset_type,
        request.asset_name, request.invested,
        request.current_value, request.monthly_sip
    )
    return {"success": True,
            "portfolio": get_portfolio_summary(request.session_id)}


@router.get("/portfolio/{session_id}")
def portfolio_get(session_id: str):
    from app.db_manager import get_portfolio_summary
    if not get_profile(session_id):
        return {"error": "Profile not found."}
    return {"portfolio": get_portfolio_summary(session_id)}


@router.post("/goals/add")
def goal_add(request: GoalAddRequest):
    from app.db_manager import add_goal, get_goals
    if not get_profile(request.session_id):
        return {"error": "Profile not found."}
    goal_id = add_goal(
        request.session_id, request.title,
        request.target_amount, request.deadline or ""
    )
    return {"success": True, "goal_id": goal_id,
            "goals": get_goals(request.session_id)}


@router.post("/goals/update")
def goal_update(request: GoalUpdateRequest):
    from app.db_manager import update_goal, get_goals
    update_goal(request.goal_id, request.saved_amount)
    return {"success": True,
            "goals": get_goals(request.session_id)}


@router.get("/goals/{session_id}")
def goals_get(session_id: str):
    from app.db_manager import get_goals
    return {"goals": get_goals(session_id)}


@router.get("/search-stocks/{query}")
def search_stocks(query: str):
    from app.stock_analyzer import NSE_SUFFIX, BSE_SUFFIX
    results = []
    for suffix in [NSE_SUFFIX, BSE_SUFFIX]:
        try:
            info = get_info_cached(query.upper() + suffix)
            if info.get("longName"):
                results.append({
                    "symbol":   query.upper(),
                    "name":     info.get("longName", query),
                    "exchange": "NSE" if suffix == NSE_SUFFIX else "BSE",
                    "sector":   info.get("sector", "")
                })
        except Exception:
            continue
    return {"results": results, "query": query}