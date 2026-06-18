# app/health_score.py
from app.db_manager import get_snapshots

def calculate_health_score(profile: dict) -> dict:
    income    = profile.get("monthly_income", 0)
    expenses  = profile.get("monthly_expenses", 0)
    savings   = income - expenses
    age       = profile.get("age", 30)
    insurance = profile.get("has_insurance", False)
    debts     = profile.get("debts", "none")
    investments = profile.get("existing_investments", "none")
    goals     = profile.get("financial_goals", "not specified")

    score      = 0
    breakdown  = []
    max_scores = {}

    # 1. Savings Rate (25 points)
    if income > 0:
        rate = savings / income * 100
        if rate >= 30:
            pts = 25
        elif rate >= 20:
            pts = 20
        elif rate >= 10:
            pts = 12
        elif rate > 0:
            pts = 5
        else:
            pts = 0
        score += pts
        breakdown.append({
            "category": "Savings Rate",
            "score":    pts,
            "max":      25,
            "status":   f"{round(rate, 1)}% of income saved",
            "tip":      "Target 20%+ to score full points"
        })

    # 2. Insurance (20 points)
    if insurance:
        pts = 20
        msg = "Insurance in place"
    else:
        pts = 0
        msg = "No insurance — critical gap"
    score += pts
    breakdown.append({
        "category": "Insurance Coverage",
        "score":    pts,
        "max":      20,
        "status":   msg,
        "tip":      "Get health + term insurance for full points"
    })

    # 3. Debt Status (20 points)
    has_debt = debts.lower() not in ["none", "no", ""]
    if not has_debt:
        pts = 20
        msg = "Debt free"
    else:
        pts = 8
        msg = f"Has debt: {debts}"
    score += pts
    breakdown.append({
        "category": "Debt Status",
        "score":    pts,
        "max":      20,
        "status":   msg,
        "tip":      "Clear all high-interest debt for full points"
    })

    # 4. Investment Habit (20 points)
    is_investing = investments.lower() not in ["none", "no", ""]
    if is_investing:
        pts = 20
        msg = f"Investing: {investments}"
    elif savings > 2000:
        pts = 10
        msg = "Has savings but not investing"
    else:
        pts = 0
        msg = "Not investing yet"
    score += pts
    breakdown.append({
        "category": "Investment Habit",
        "score":    pts,
        "max":      20,
        "status":   msg,
        "tip":      "Start SIP to score full points"
    })

    # 5. Age vs Financial Progress (15 points)
    if age < 25:
        pts = 15
        msg = "Early start — time advantage"
    elif age < 35:
        pts = 12 if is_investing else 8
        msg = "Prime saving years"
    elif age < 45:
        pts = 10 if is_investing else 5
        msg = "Mid-career — accelerate savings"
    else:
        pts = 8 if is_investing else 3
        msg = "Focus on retirement planning"
    score += pts
    breakdown.append({
        "category": "Financial Progress",
        "score":    pts,
        "max":      15,
        "status":   msg,
        "tip":      "Consistent investing over time improves this"
    })

    # Grade
    if score >= 85:
        grade = "A+"
        label = "Excellent"
        color = "green"
    elif score >= 70:
        grade = "A"
        label = "Very Good"
        color = "green"
    elif score >= 55:
        grade = "B"
        label = "Good"
        color = "blue"
    elif score >= 40:
        grade = "C"
        label = "Average"
        color = "amber"
    elif score >= 25:
        grade = "D"
        label = "Needs Work"
        color = "red"
    else:
        grade = "F"
        label = "Critical"
        color = "red"

    # Top priority action
    lowest  = min(breakdown, key=lambda x: x["score"] / x["max"])
    next_action = f"Focus on: {lowest['category']} — {lowest['tip']}"

    return {
        "score":       score,
        "max":         100,
        "grade":       grade,
        "label":       label,
        "color":       color,
        "breakdown":   breakdown,
        "next_action": next_action,
        "name":        profile.get("name", "User")
    }