from datetime import datetime


def calculate_insurance_needs(profile: dict) -> dict:
    name = profile.get("name", "User")
    age = profile.get("age", 30)
    income = profile.get("monthly_income", 0)
    expenses = profile.get("monthly_expenses", 0)
    dependents = profile.get("dependents", 0)
    has_insurance = profile.get("has_insurance", False)
    debts = profile.get("debts", "none")

    annual_income = income * 12
    simple_term_cover = max(int(annual_income * 15), 1000000)
    if dependents >= 3:
        simple_term_cover = max(simple_term_cover, int(annual_income * 18))

    health_cover = 1000000 if age < 40 else 1500000
    health_premium = 12000 if age < 40 else 18000
    term_monthly_premium = round(simple_term_cover / 1000000 * 1200)
    critical_illness_cover = 1000000
    critical_illness_premium = 2400 if age < 40 else 3600

    recommendations = []
    urgency_flags = []
    needs_critical = False

    if not has_insurance:
        needs_critical = True
        urgency_flags.append({
            "flag": "No health or term insurance detected",
            "action": "Buy a minimum ₹10-15 lakh health cover and a term plan equal to 15x annual income."
        })
        recommendations.append(
            "Buy health insurance with at least ₹10 lakh coverage and term life insurance with cover equal to 15x your annual income."
        )
    else:
        recommendations.append(
            "Review your health and term insurance every year. Keep coverage aligned with salary hikes and family changes."
        )

    if debts.lower() not in ["none", "no", ""]:
        urgency_flags.append({
            "flag": "You have active debts or EMIs",
            "action": "High-interest debt increases financial risk. Maintain insurance while you clear the debt."
        })

    if dependents > 0:
        urgency_flags.append({
            "flag": "Your dependents rely on your income",
            "action": "Keep term cover high and review beneficiary details."
        })

    if age >= 45 and not has_insurance:
        urgency_flags.append({
            "flag": "Insurance premiums rise with age",
            "action": "Buy cover now before rates go higher."
        })

    total_monthly_cost = round(health_premium + term_monthly_premium + critical_illness_premium)

    return {
        "name": name,
        "age": age,
        "has_insurance": has_insurance,
        "dependents": dependents,
        "annual_income": annual_income,
        "monthly_expenses": expenses,
        "health_insurance": {
            "cover": health_cover,
            "monthly_premium": health_premium,
            "note": "Recommended health cover for your age."
        },
        "term_insurance": {
            "cover_display": f"₹{simple_term_cover:,}",
            "monthly_premium": term_monthly_premium,
            "note": "Term insurance to protect your family if you are the primary earner."
        },
        "critical_illness": {
            "cover": critical_illness_cover,
            "annual_premium": critical_illness_premium * 12,
            "monthly_premium": critical_illness_premium,
            "note": "Critical illness cover protects against large hospital bills."
        },
        "total_monthly_cost": total_monthly_cost,
        "needs_critical": needs_critical,
        "urgency_flags": urgency_flags,
        "recommendations": recommendations,
        "created_at": datetime.now().isoformat()
    }


def format_insurance_for_ai(insurance_data: dict) -> str:
    health = insurance_data["health_insurance"]
    term = insurance_data["term_insurance"]
    critical = insurance_data["critical_illness"]
    flags = "\n".join(
        f"- {f['flag']}: {f['action']}" for f in insurance_data["urgency_flags"]
    )
    recs = "\n".join(f"- {r}" for r in insurance_data["recommendations"])

    return f"""
INSURANCE NEEDS SUMMARY for {insurance_data['name']}:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Age: {insurance_data['age']}
Dependents: {insurance_data['dependents']}
Monthly Expenses: ₹{insurance_data['monthly_expenses']:,.0f}
Annual Income: ₹{insurance_data['annual_income']:,.0f}
Has insurance: {'Yes' if insurance_data['has_insurance'] else 'No'}

HEALTH INSURANCE:
- Recommended cover: ₹{health['cover']:,}
- Estimated premium: ₹{health['monthly_premium']:,}/month

TERM INSURANCE:
- Recommended cover: {term['cover_display']}
- Estimated premium: ₹{term['monthly_premium']:,}/month

CRITICAL ILLNESS COVER:
- Cover: ₹{critical['cover']:,}
- Estimated premium: ₹{critical['monthly_premium']:,}/month

HOURLY RISK REVIEW:
{flags if flags else '- No urgent flags detected'}

RECOMMENDATIONS:
{recs}

Based on this insurance assessment, provide:
1. A clear explanation of what insurance {insurance_data['name']} needs now.
2. Why health + term + critical illness cover matter for their age and dependents.
3. Exact next steps: what to buy first, the coverage target, and the monthly budget.
4. A gentle but firm warning if they currently have no insurance.
5. A short closing line: this is educational information, not professional advice.
""".strip()
