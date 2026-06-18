# app/smart_savings_engine.py

from datetime import datetime

SPENDING_LEAKS = [
    {
        "category":    "Food delivery",
        "apps":        ["swiggy", "zomato", "blinkit", "dunzo"],
        "avg_monthly": 4500,
        "tip":         "Cook 4 days, order 3 days. Saves ₹2,500–4,000/month.",
        "saving":      3000
    },
    {
        "category":    "OTT subscriptions",
        "apps":        ["netflix", "hotstar", "prime", "sonyliv", "zee5", "mxplayer"],
        "avg_monthly": 1200,
        "tip":         "Keep 1–2 platforms. Share family plans. Saves ₹600–1,500/month.",
        "saving":      800
    },
    {
        "category":    "Impulse online shopping",
        "apps":        ["amazon", "flipkart", "meesho", "myntra", "ajio", "nykaa"],
        "avg_monthly": 3500,
        "tip":         "Wait 24 hours before buying anything above ₹500. Saves ₹1,500–3,000/month.",
        "saving":      2000
    },
    {
        "category":    "Cab rides",
        "apps":        ["ola", "uber", "rapido"],
        "avg_monthly": 2500,
        "tip":         "Use metro/bus for regular commute. Saves ₹1,000–2,500/month.",
        "saving":      1500
    },
    {
        "category":    "Coffee and snacks",
        "apps":        ["starbucks", "cafe coffee day", "chaayos"],
        "avg_monthly": 2000,
        "tip":         "Make coffee at home 5 days. Treat yourself 2 days. Saves ₹1,000/month.",
        "saving":      1000
    },
    {
        "category":    "Gym memberships",
        "apps":        ["gym", "cult.fit", "cultfit"],
        "avg_monthly": 1500,
        "tip":         "If going less than 3x/week, switch to home workout + YouTube. Saves ₹800–1,500/month.",
        "saving":      1000
    },
    {
        "category":    "Unnecessary data / phone plans",
        "apps":        ["airtel", "jio", "vi", "bsnl"],
        "avg_monthly": 500,
        "tip":         "Compare plans yearly. Jio/BSNL often have better rates. Saves ₹200–500/month.",
        "saving":      300
    }
]

MONTH_END_WARNING = {
    "trigger_day":   22,
    "message":       "Last week of month alert — most people overspend in the last 7 days. Track every expense carefully this week.",
    "tip":           "Set a ₹500/day limit for the remaining days of the month."
}

SAVING_HABITS = [
    {
        "habit":       "Pay yourself first",
        "description": "Transfer your savings amount on salary day — before spending anything.",
        "impact":      "HIGH",
        "how":         "Set up auto-transfer to a separate savings account on the 1st of every month."
    },
    {
        "habit":       "24-hour rule",
        "description": "Wait 24 hours before any purchase above ₹500.",
        "impact":      "HIGH",
        "how":         "Add to cart, close the app, come back tomorrow. 70% of the time you won't buy it."
    },
    {
        "habit":       "No-spend weekdays",
        "description": "Pick 2–3 weekdays per week where you spend ₹0 outside essentials.",
        "impact":      "MEDIUM",
        "how":         "Pack lunch, make coffee at home, avoid malls on those days."
    },
    {
        "habit":       "Weekly money review",
        "description": "Every Sunday, review what you spent that week.",
        "impact":      "HIGH",
        "how":         "Check your UPI app or bank statement. Takes 10 minutes. Prevents next week's mistakes."
    },
    {
        "habit":       "Cash envelope for wants",
        "description": "Withdraw your 'wants' budget in cash each month.",
        "impact":      "MEDIUM",
        "how":         "When the envelope is empty, wants spending stops for the month."
    }
]


def detect_spending_leaks(profile: dict) -> dict:
    income   = profile.get("monthly_income", 0)
    expenses = profile.get("monthly_expenses", 0)
    name     = profile.get("name", "User")

    if income == 0:
        return {"error": "Income data missing"}

    spending_ratio = expenses / income if income > 0 else 1
    total_leak_potential = sum(l["saving"] for l in SPENDING_LEAKS)

    # Based on spending ratio — flag more leaks if spending too high
    high_spender   = spending_ratio > 0.75
    medium_spender = spending_ratio > 0.55

    priority_leaks = []
    if high_spender:
        priority_leaks = SPENDING_LEAKS[:5]
    elif medium_spender:
        priority_leaks = SPENDING_LEAKS[:3]
    else:
        priority_leaks = SPENDING_LEAKS[:2]

    priority_saving = sum(l["saving"] for l in priority_leaks)

    # Month end check
    today     = datetime.now()
    month_end = today.day >= MONTH_END_WARNING["trigger_day"]

    # Annual impact
    annual_saving  = priority_saving * 12
    sip_10yr_value = round(priority_saving * (((1.01) ** 120 - 1) / 0.01) * 1.01)

    return {
        "name":               name,
        "income":             income,
        "expenses":           expenses,
        "spending_ratio":     round(spending_ratio * 100, 1),
        "is_high_spender":    high_spender,
        "leaks":              priority_leaks,
        "total_leak_saving":  priority_saving,
        "annual_saving":      annual_saving,
        "sip_10yr_value":     sip_10yr_value,
        "month_end_warning":  MONTH_END_WARNING if month_end else None,
        "all_leaks":          SPENDING_LEAKS,
        "saving_habits":      SAVING_HABITS
    }


def generate_monthly_tracker(profile: dict) -> dict:
    income   = profile.get("monthly_income", 0)
    expenses = profile.get("monthly_expenses", 0)
    savings  = income - expenses

    today = datetime.now()
    day   = today.day

    # Daily budget
    days_in_month      = 30
    daily_budget       = round(expenses / days_in_month, 0)
    days_remaining     = max(1, days_in_month - day)
    estimated_month_spend = expenses

    # Weekly breakdown target
    week1 = round(expenses * 0.25)
    week2 = round(expenses * 0.25)
    week3 = round(expenses * 0.25)
    week4 = round(expenses * 0.25)

    # Milestones
    milestones = []
    if savings >= 5000:
        milestones.append({
            "milestone": "Starter Saver",
            "achieved":  True,
            "desc":      f"Saving ₹{savings:,.0f}/month"
        })
    if savings >= income * 0.2:
        milestones.append({
            "milestone": "20% Club",
            "achieved":  True,
            "desc":      "Saving 20%+ of income"
        })
    if savings >= income * 0.3:
        milestones.append({
            "milestone": "Power Saver",
            "achieved":  True,
            "desc":      "Saving 30%+ — top 10% of Indians"
        })

    return {
        "income":         income,
        "expenses":       expenses,
        "savings":        savings,
        "daily_budget":   daily_budget,
        "day_of_month":   day,
        "days_remaining": days_remaining,
        "weekly_targets": {
            "week1": week1,
            "week2": week2,
            "week3": week3,
            "week4": week4
        },
        "milestones":     milestones
    }


def format_savings_engine_for_ai(leak_data: dict, tracker: dict) -> str:
    leaks_text = ""
    for l in leak_data["leaks"]:
        leaks_text += f"\n- {l['category']}: avg ₹{l['avg_monthly']:,}/month — save ₹{l['saving']:,}/month"
        leaks_text += f"\n  Tip: {l['tip']}"

    habits_text = "\n".join(
        f"- {h['habit']} ({h['impact']} impact): {h['description']}"
        for h in leak_data["saving_habits"][:3]
    )

    month_end = ""
    if leak_data.get("month_end_warning"):
        month_end = f"\n⚠️ MONTH-END ALERT: {leak_data['month_end_warning']['message']}"

    return f"""
SMART SAVINGS ENGINE ANALYSIS for {leak_data['name']}:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Monthly Income  : ₹{leak_data['income']:,.0f}
Monthly Expenses: ₹{leak_data['expenses']:,.0f}
Spending Ratio  : {leak_data['spending_ratio']}% of income
{month_end}

TOP SPENDING LEAKS DETECTED:
{leaks_text}

TOTAL POTENTIAL MONTHLY SAVING : ₹{leak_data['total_leak_saving']:,}
ANNUAL SAVING IF FIXED          : ₹{leak_data['annual_saving']:,}
IF INVESTED AS SIP FOR 10 YEARS : ₹{leak_data['sip_10yr_value']:,}

DAILY BUDGET TARGET: ₹{tracker['daily_budget']:,.0f}/day
TODAY IS DAY {tracker['day_of_month']} — {tracker['days_remaining']} days remaining this month

TOP SAVING HABITS TO BUILD:
{habits_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Based on this analysis, give {leak_data['name']} a powerful, 
motivating savings improvement plan. Be specific with rupee amounts.
Show them the real cost of each leak over 10 years.
Give them 3 immediate actions they can take today.
Tell them exactly what ₹{leak_data['total_leak_saving']:,}/month becomes
if invested as SIP for 10, 20 years.
Make it feel urgent but achievable.
""".strip()