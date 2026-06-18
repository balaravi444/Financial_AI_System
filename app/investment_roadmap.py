# app/investment_roadmap.py

MUTUAL_FUND_CATEGORIES = {
    "emergency": {
        "name":        "Liquid Mutual Fund",
        "examples":    "Parag Parikh Liquid Fund, HDFC Liquid Fund",
        "returns":     "6-7%",
        "risk":        "Very Low",
        "use":         "Emergency fund — withdraw anytime"
    },
    "large_cap": {
        "name":        "Large Cap / Index Fund",
        "examples":    "Nifty 50 Index Fund (Zerodha Coin / Groww)",
        "returns":     "10-12%",
        "risk":        "Low-Medium",
        "use":         "Core stable long-term wealth"
    },
    "mid_cap": {
        "name":        "Mid Cap Fund",
        "examples":    "Motilal Oswal Midcap Fund, Nippon Mid Cap",
        "returns":     "13-16%",
        "risk":        "Medium",
        "use":         "Higher growth, 5+ year horizon"
    },
    "small_cap": {
        "name":        "Small Cap Fund",
        "examples":    "Nippon Small Cap, Quant Small Cap",
        "returns":     "15-20%",
        "risk":        "High",
        "use":         "Aggressive growth, 7+ year horizon"
    },
    "elss": {
        "name":        "ELSS Tax Saving Fund",
        "examples":    "Parag Parikh ELSS, Mirae Asset ELSS",
        "returns":     "12-15%",
        "risk":        "Medium",
        "use":         "Tax saving under 80C + wealth creation"
    },
    "debt": {
        "name":        "Debt / Short Duration Fund",
        "examples":    "HDFC Short Duration, ICICI Prudential Debt",
        "returns":     "7-8%",
        "risk":        "Low",
        "use":         "Stable returns, better than FD post-tax"
    },
    "gold": {
        "name":        "Gold ETF / Sovereign Gold Bond",
        "examples":    "Nippon Gold ETF, SGB via bank",
        "returns":     "8-10%",
        "risk":        "Low-Medium",
        "use":         "Portfolio hedge, inflation protection"
    }
}


def get_risk_allocation(risk_tolerance: str, age: int) -> dict:
    # Age-based equity reduction rule: 100 - age = equity %
    base_equity = max(40, min(90, 100 - age))

    if risk_tolerance == "low":
        equity   = max(30, base_equity - 20)
        debt     = 50
        gold     = 10
        liquid   = 10
    elif risk_tolerance == "high":
        equity   = min(90, base_equity + 10)
        debt     = max(5, 100 - equity - 5)
        gold     = 5
        liquid   = 0
    else:  # medium
        equity   = base_equity
        debt     = max(10, 100 - equity - 10)
        gold     = 10
        liquid   = 0

    # Normalize to 100%
    total  = equity + debt + gold + liquid
    factor = 100 / total

    return {
        "equity": round(equity * factor),
        "debt":   round(debt * factor),
        "gold":   round(gold * factor),
        "liquid": round(liquid * factor)
    }


def split_equity(equity_amount: float, risk_tolerance: str, age: int) -> dict:
    if risk_tolerance == "low" or age > 50:
        return {
            "large_cap": round(equity_amount * 0.70),
            "mid_cap":   round(equity_amount * 0.20),
            "small_cap": round(equity_amount * 0.10),
            "elss":      0
        }
    elif risk_tolerance == "high" and age < 35:
        return {
            "large_cap": round(equity_amount * 0.40),
            "mid_cap":   round(equity_amount * 0.30),
            "small_cap": round(equity_amount * 0.20),
            "elss":      round(equity_amount * 0.10)
        }
    else:
        return {
            "large_cap": round(equity_amount * 0.50),
            "mid_cap":   round(equity_amount * 0.30),
            "small_cap": round(equity_amount * 0.10),
            "elss":      round(equity_amount * 0.10)
        }


def calculate_future_value(monthly_sip: float, years: int, annual_rate: float) -> float:
    r = annual_rate / 12 / 100
    n = years * 12
    if r == 0:
        return monthly_sip * n
    fv = monthly_sip * (((1 + r) ** n - 1) / r) * (1 + r)
    return round(fv, 2)


def generate_roadmap(profile: dict) -> dict:
    income        = profile.get("monthly_income", 0)
    expenses      = profile.get("monthly_expenses", 0)
    age           = profile.get("age", 30)
    name          = profile.get("name", "User")
    risk          = profile.get("risk_tolerance", "medium")
    goals         = profile.get("financial_goals", "retirement")
    has_insurance = profile.get("has_insurance", False)
    debts         = profile.get("debts", "none")
    investments   = profile.get("existing_investments", "none")

    available_to_invest = income - expenses

    if available_to_invest <= 0:
        return {
            "error": "Monthly expenses exceed income. Fix budget first before investing."
        }

    # Phase priorities
    phases = []
    remaining = available_to_invest

    # Phase 0 — Insurance (if missing)
    if not has_insurance:
        insurance_cost = 1000 if age < 30 else 2000
        phases.append({
            "phase":       0,
            "title":       "🚨 Urgent — Get Insurance First",
            "description": "Before investing a single rupee, get health + term insurance.",
            "action":      f"Set aside ₹{insurance_cost:,}/month for insurance premiums",
            "amount":      insurance_cost,
            "priority":    "CRITICAL"
        })
        remaining -= insurance_cost

    # Phase 1 — Emergency Fund
    emergency_target  = expenses * 6
    emergency_monthly = round(min(remaining * 0.3, emergency_target / 12), 0)
    phases.append({
        "phase":       1,
        "title":       "Emergency Fund",
        "description": f"Build ₹{emergency_target:,.0f} (6 months expenses) in a liquid fund.",
        "action":      f"SIP ₹{emergency_monthly:,.0f}/month in Liquid Mutual Fund for 12 months",
        "amount":      emergency_monthly,
        "fund":        MUTUAL_FUND_CATEGORIES["emergency"],
        "target":      emergency_target,
        "months":      12,
        "priority":    "HIGH"
    })
    remaining -= emergency_monthly

    # Phase 2 — Debt clearance
    if debts.lower() not in ["none", "no", ""]:
        debt_payment = round(remaining * 0.4, 0)
        phases.append({
            "phase":       2,
            "title":       "Clear High-Interest Debt",
            "description": f"You have: {debts}. Pay this off aggressively before investing.",
            "action":      f"Put ₹{debt_payment:,.0f}/month extra toward debt repayment",
            "amount":      debt_payment,
            "priority":    "HIGH"
        })
        remaining -= debt_payment

    # Phase 3 — Core Investment Plan
    if remaining > 500:
        allocation   = get_risk_allocation(risk, age)
        equity_amt   = round(remaining * allocation["equity"] / 100)
        debt_amt     = round(remaining * allocation["debt"]   / 100)
        gold_amt     = round(remaining * allocation["gold"]   / 100)
        equity_split = split_equity(equity_amt, risk, age)

        sip_plan = []

        if equity_split["large_cap"] > 0:
            sip_plan.append({
                "fund":    MUTUAL_FUND_CATEGORIES["large_cap"]["name"],
                "examples": MUTUAL_FUND_CATEGORIES["large_cap"]["examples"],
                "amount":  equity_split["large_cap"],
                "returns": MUTUAL_FUND_CATEGORIES["large_cap"]["returns"],
                "risk":    MUTUAL_FUND_CATEGORIES["large_cap"]["risk"]
            })

        if equity_split["mid_cap"] > 0:
            sip_plan.append({
                "fund":    MUTUAL_FUND_CATEGORIES["mid_cap"]["name"],
                "examples": MUTUAL_FUND_CATEGORIES["mid_cap"]["examples"],
                "amount":  equity_split["mid_cap"],
                "returns": MUTUAL_FUND_CATEGORIES["mid_cap"]["returns"],
                "risk":    MUTUAL_FUND_CATEGORIES["mid_cap"]["risk"]
            })

        if equity_split["small_cap"] > 0 and risk != "low":
            sip_plan.append({
                "fund":    MUTUAL_FUND_CATEGORIES["small_cap"]["name"],
                "examples": MUTUAL_FUND_CATEGORIES["small_cap"]["examples"],
                "amount":  equity_split["small_cap"],
                "returns": MUTUAL_FUND_CATEGORIES["small_cap"]["returns"],
                "risk":    MUTUAL_FUND_CATEGORIES["small_cap"]["risk"]
            })

        if equity_split["elss"] > 0:
            sip_plan.append({
                "fund":    MUTUAL_FUND_CATEGORIES["elss"]["name"],
                "examples": MUTUAL_FUND_CATEGORIES["elss"]["examples"],
                "amount":  equity_split["elss"],
                "returns": MUTUAL_FUND_CATEGORIES["elss"]["returns"],
                "risk":    MUTUAL_FUND_CATEGORIES["elss"]["risk"]
            })

        if debt_amt > 0:
            sip_plan.append({
                "fund":    MUTUAL_FUND_CATEGORIES["debt"]["name"],
                "examples": MUTUAL_FUND_CATEGORIES["debt"]["examples"],
                "amount":  debt_amt,
                "returns": MUTUAL_FUND_CATEGORIES["debt"]["returns"],
                "risk":    MUTUAL_FUND_CATEGORIES["debt"]["risk"]
            })

        if gold_amt > 0:
            sip_plan.append({
                "fund":    MUTUAL_FUND_CATEGORIES["gold"]["name"],
                "examples": MUTUAL_FUND_CATEGORIES["gold"]["examples"],
                "amount":  gold_amt,
                "returns": MUTUAL_FUND_CATEGORIES["gold"]["returns"],
                "risk":    MUTUAL_FUND_CATEGORIES["gold"]["risk"]
            })

        # Future value projections
        years_to_retire = max(1, 60 - age)
        avg_return      = 12 if risk == "high" else (10 if risk == "medium" else 8)
        future_value_10 = calculate_future_value(remaining, 10, avg_return)
        future_value_20 = calculate_future_value(remaining, 20, avg_return)
        future_value_retire = calculate_future_value(remaining, years_to_retire, avg_return)

        phases.append({
            "phase":       3,
            "title":       "Core Investment SIP Plan",
            "description": f"Invest ₹{remaining:,.0f}/month across diversified funds",
            "amount":      remaining,
            "allocation":  allocation,
            "sip_plan":    sip_plan,
            "projections": {
                "monthly_sip":      remaining,
                "10_years":         future_value_10,
                "20_years":         future_value_20,
                "at_retirement":    future_value_retire,
                "years_to_retire":  years_to_retire,
                "assumed_return":   avg_return
            },
            "priority": "MEDIUM"
        })

    # Review triggers
    review_triggers = [
        "When Nifty falls 20%+ from peak — increase SIP by 1.5x",
        "When you get a salary hike — add 50% of increment to SIP",
        "Every January — rebalance portfolio to original allocation",
        "When you have dependents — review insurance cover",
        "Every 3 years — review fund performance vs benchmark"
    ]

    return {
        "name":             name,
        "age":              age,
        "income":           income,
        "expenses":         expenses,
        "available":        available_to_invest,
        "risk_tolerance":   risk,
        "goals":            goals,
        "phases":           phases,
        "review_triggers":  review_triggers,
        "how_to_start":     [
            "Download Groww or Zerodha Coin app",
            "Complete KYC with Aadhaar + PAN (takes 10 minutes)",
            "Link your bank account",
            "Start SIP with the amounts above on the 1st of every month",
            "Never stop SIP during market crashes — that's when it works best"
        ]
    }


def format_roadmap_for_ai(roadmap: dict) -> str:
    phases_text = ""
    for p in roadmap["phases"]:
        phases_text += f"\nPhase {p['phase']}: {p['title']} — ₹{p['amount']:,.0f}/month\n"
        phases_text += f"  {p['description']}\n"
        if "sip_plan" in p:
            for s in p["sip_plan"]:
                phases_text += f"  - {s['fund']}: ₹{s['amount']:,.0f}/month ({s['returns']} expected)\n"
        if "projections" in p:
            proj = p["projections"]
            phases_text += f"  Projected wealth:\n"
            phases_text += f"  - In 10 years : ₹{proj['10_years']:,.0f}\n"
            phases_text += f"  - In 20 years : ₹{proj['20_years']:,.0f}\n"
            phases_text += f"  - At retirement: ₹{proj['at_retirement']:,.0f}\n"

    return f"""
PERSONALISED INVESTMENT ROADMAP for {roadmap['name']}:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Age             : {roadmap['age']}
Monthly Income  : ₹{roadmap['income']:,.0f}
Monthly Expenses: ₹{roadmap['expenses']:,.0f}
Available to Invest: ₹{roadmap['available']:,.0f}
Risk Tolerance  : {roadmap['risk_tolerance']}
Goals           : {roadmap['goals']}

INVESTMENT PHASES:
{phases_text}

HOW TO START:
{chr(10).join(f"- {s}" for s in roadmap['how_to_start'])}

WHEN TO REVIEW:
{chr(10).join(f"- {r}" for r in roadmap['review_triggers'])}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Based on this roadmap, give {roadmap['name']} a motivating, 
detailed explanation of their investment plan. 
Explain WHY each fund was chosen for their specific situation.
Tell them exactly what to do in the first 7 days.
Be encouraging — make investing feel achievable, not scary.
""".strip()