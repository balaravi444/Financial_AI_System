# app/savings_calculator.py

def calculate_savings_plan(profile: dict) -> dict:
    income   = profile.get("monthly_income", 0)
    expenses = profile.get("monthly_expenses", 0)
    debts    = profile.get("debts", "none")
    age      = profile.get("age", 30)
    name     = profile.get("name", "User")

    if income == 0:
        return {"error": "Income data missing"}

    # 50-30-20 rule targets
    needs_target   = round(income * 0.50, 2)
    wants_target   = round(income * 0.30, 2)
    savings_target = round(income * 0.20, 2)

    # Actual savings
    actual_savings = round(income - expenses, 2)
    savings_rate   = round((actual_savings / income) * 100, 2)

    # Emergency fund
    emergency_target  = round(expenses * 6, 2)
    emergency_monthly = round(emergency_target / 12, 2)

    # Savings health score (out of 10)
    if savings_rate >= 30:
        health_score = 10
        health_label = "Excellent"
    elif savings_rate >= 20:
        health_score = 8
        health_label = "Good"
    elif savings_rate >= 10:
        health_score = 5
        health_label = "Average"
    elif savings_rate > 0:
        health_score = 3
        health_label = "Needs Work"
    else:
        health_score = 1
        health_label = "Critical"

    # Gap analysis
    savings_gap = round(savings_target - actual_savings, 2)

    # Recommendations
    recommendations = []

    if actual_savings <= 0:
        recommendations.append(
            f"You are spending more than you earn. "
            f"Cut ₹{abs(actual_savings):,.0f} from monthly expenses immediately."
        )
    elif savings_rate < 20:
        recommendations.append(
            f"You are saving ₹{actual_savings:,.0f}/month ({savings_rate}%). "
            f"Target is ₹{savings_target:,.0f} (20%). "
            f"Try to save ₹{savings_gap:,.0f} more each month."
        )
    else:
        recommendations.append(
            f"Great job! You are saving ₹{actual_savings:,.0f}/month ({savings_rate}%). "
            f"Keep it up and start investing the surplus."
        )

    if debts.lower() not in ["none", "no", ""]:
        recommendations.append(
            f"You have active debts/EMIs ({debts}). "
            f"Pay off high-interest debt before investing."
        )

    recommendations.append(
        f"Build an emergency fund of ₹{emergency_target:,.0f} "
        f"(6 months of expenses). "
        f"Save ₹{emergency_monthly:,.0f}/month for 12 months to reach this."
    )

    if age < 30:
        recommendations.append(
            "You are young — even ₹1,000/month in SIP now will "
            "grow to ₹35+ lakhs by retirement at 12% CAGR."
        )

    # Common spending leaks to check
    spending_leaks = [
        {"item": "Food delivery (Swiggy/Zomato)", "estimate": "₹3,000–9,000/month",
         "tip": "Cook 4 days a week, order 3 days — saves ₹3,000+"},
        {"item": "Unused OTT subscriptions",       "estimate": "₹500–2,000/month",
         "tip": "Keep only 1–2 platforms, share family plans"},
        {"item": "Impulse online shopping",         "estimate": "₹2,000–5,000/month",
         "tip": "Wait 24 hours before buying anything above ₹500"},
        {"item": "Coffee/tea outside daily",        "estimate": "₹1,500–3,000/month",
         "tip": "Make coffee at home 5 days, treat yourself 2 days"},
        {"item": "Cab rides (Ola/Uber)",            "estimate": "₹2,000–4,000/month",
         "tip": "Use metro/bus for regular routes, cab only when needed"},
    ]

    return {
        "name":              name,
        "income":            income,
        "expenses":          expenses,
        "actual_savings":    actual_savings,
        "savings_rate":      savings_rate,
        "health_score":      health_score,
        "health_label":      health_label,
        "breakdown": {
            "needs_target":   needs_target,
            "wants_target":   wants_target,
            "savings_target": savings_target,
        },
        "emergency_fund": {
            "target":          emergency_target,
            "monthly_needed":  emergency_monthly,
        },
        "savings_gap":       savings_gap,
        "recommendations":   recommendations,
        "spending_leaks":    spending_leaks,
    }


def format_savings_for_ai(savings_data: dict, profile: dict) -> str:
    s = savings_data
    b = s["breakdown"]
    e = s["emergency_fund"]

    return f"""
USER SAVINGS ANALYSIS for {s['name']}:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Monthly Income  : ₹{s['income']:,.0f}
Monthly Expenses: ₹{s['expenses']:,.0f}
Actual Savings  : ₹{s['actual_savings']:,.0f} ({s['savings_rate']}%)
Savings Health  : {s['health_label']} ({s['health_score']}/10)

50-30-20 TARGETS vs ACTUAL:
- Needs  (50%): Target ₹{b['needs_target']:,.0f}
- Wants  (30%): Target ₹{b['wants_target']:,.0f}
- Savings(20%): Target ₹{b['savings_target']:,.0f} | Actual ₹{s['actual_savings']:,.0f}

EMERGENCY FUND:
- Target : ₹{e['target']:,.0f} (6 months expenses)
- Monthly: Save ₹{e['monthly_needed']:,.0f}/month for 12 months

KEY RECOMMENDATIONS:
{chr(10).join(f'- {r}' for r in s['recommendations'])}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Based on this savings analysis, give {s['name']} a detailed, 
personalised savings improvement plan. Be specific with rupee amounts.
Include: what to cut, where to save more, and exact next steps.
Add encouragement based on their age and situation.
""".strip()