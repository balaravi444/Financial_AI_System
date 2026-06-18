# app/tax_optimizer.py

TAX_SECTIONS = {
    "80C": {
        "limit": 150000,
        "name": "Section 80C",
        "instruments": [
            {"name": "ELSS Mutual Fund",        "limit": 150000, "returns": "12-15%", "lock_in": "3 years",  "recommended": True},
            {"name": "PPF",                      "limit": 150000, "returns": "7.1%",   "lock_in": "15 years", "recommended": True},
            {"name": "NPS Tier 2",               "limit": 150000, "returns": "10-12%", "lock_in": "Till 60",  "recommended": False},
            {"name": "Life Insurance Premium",   "limit": 150000, "returns": "4-6%",   "lock_in": "Varies",   "recommended": False},
            {"name": "Home Loan Principal",      "limit": 150000, "returns": "N/A",    "lock_in": "N/A",      "recommended": False},
            {"name": "Children School Fees",     "limit": 150000, "returns": "N/A",    "lock_in": "N/A",      "recommended": False},
            {"name": "5-Year Tax Saver FD",      "limit": 150000, "returns": "6.5-7%", "lock_in": "5 years",  "recommended": False},
            {"name": "Sukanya Samriddhi Yojana", "limit": 150000, "returns": "8.2%",   "lock_in": "21 years", "recommended": False},
        ]
    },
    "80D": {
        "limit": 75000,
        "name": "Section 80D",
        "instruments": [
            {"name": "Health Insurance (self + family)", "limit": 25000, "note": "Up to ₹25,000 for self/family under 60"},
            {"name": "Health Insurance (parents < 60)",  "limit": 25000, "note": "Additional ₹25,000 for parents under 60"},
            {"name": "Health Insurance (parents > 60)",  "limit": 50000, "note": "Additional ₹50,000 for senior citizen parents"},
        ]
    },
    "80CCD": {
        "limit": 50000,
        "name": "Section 80CCD(1B) — NPS",
        "instruments": [
            {"name": "NPS Additional Contribution", "limit": 50000, "returns": "10-12%", "note": "Over and above 80C limit"}
        ]
    },
    "24B": {
        "limit": 200000,
        "name": "Section 24(b) — Home Loan Interest",
        "instruments": [
            {"name": "Home Loan Interest", "limit": 200000, "note": "Up to ₹2 lakh on self-occupied property"}
        ]
    }
}

TAX_SLABS_NEW = [
    (300000,  0.00),
    (600000,  0.05),
    (900000,  0.10),
    (1200000, 0.15),
    (1500000, 0.20),
    (float('inf'), 0.30)
]

TAX_SLABS_OLD = [
    (250000,      0.00),
    (500000,      0.05),
    (1000000,     0.20),
    (float('inf'), 0.30)
]


def calculate_tax(income: float, slabs: list) -> float:
    tax = 0
    prev = 0
    for limit, rate in slabs:
        if income <= prev:
            break
        taxable = min(income, limit) - prev
        tax += taxable * rate
        prev = limit
    return round(tax, 2)


def calculate_tax_savings(profile: dict) -> dict:
    annual_income = profile.get("monthly_income", 0) * 12
    age           = profile.get("age", 30)
    name          = profile.get("name", "User")
    has_insurance = profile.get("has_insurance", False)
    debts         = profile.get("debts", "none")

    # Tax without any deductions
    tax_without_deductions = calculate_tax(annual_income, TAX_SLABS_OLD)

    # Determine tax bracket
    if annual_income <= 300000:
        bracket = "No tax (below ₹3 lakh)"
        bracket_rate = 0
    elif annual_income <= 600000:
        bracket = "5% tax bracket"
        bracket_rate = 5
    elif annual_income <= 900000:
        bracket = "10% tax bracket"
        bracket_rate = 10
    elif annual_income <= 1200000:
        bracket = "15% tax bracket"
        bracket_rate = 15
    elif annual_income <= 1500000:
        bracket = "20% tax bracket"
        bracket_rate = 20
    else:
        bracket = "30% tax bracket"
        bracket_rate = 30

    # Recommended deductions based on profile
    recommendations = []
    total_potential_savings = 0

    # 80C recommendation
    elss_recommended = min(150000, max(0, annual_income * 0.15))
    tax_saved_80c    = round(elss_recommended * (bracket_rate / 100), 2)
    total_potential_savings += tax_saved_80c

    recommendations.append({
        "section":     "Section 80C",
        "instrument":  "ELSS Mutual Fund (best option)",
        "invest":      elss_recommended,
        "tax_saved":   tax_saved_80c,
        "limit":       150000,
        "why":         "Shortest lock-in (3 years), highest returns (12-15%), tax-free gains up to ₹1 lakh/year"
    })

    # 80D recommendation
    if not has_insurance:
        health_premium  = 15000 if age < 40 else 25000
        tax_saved_80d   = round(health_premium * (bracket_rate / 100), 2)
        total_potential_savings += tax_saved_80d

        recommendations.append({
            "section":    "Section 80D",
            "instrument": "Health Insurance",
            "invest":     health_premium,
            "tax_saved":  tax_saved_80d,
            "limit":      25000,
            "why":        f"You have NO health insurance — this is urgent. Estimated premium ₹{health_premium:,}/year at age {age}"
        })

    # NPS 80CCD recommendation (only if income > 5 lakh)
    if annual_income > 500000:
        nps_amount    = min(50000, annual_income * 0.05)
        tax_saved_nps = round(nps_amount * (bracket_rate / 100), 2)
        total_potential_savings += tax_saved_nps

        recommendations.append({
            "section":    "Section 80CCD(1B)",
            "instrument": "NPS Additional Contribution",
            "invest":     nps_amount,
            "tax_saved":  tax_saved_nps,
            "limit":      50000,
            "why":        "Extra ₹50,000 deduction over 80C. Good for retirement + tax saving combo"
        })

    # LTCG harvesting tip
    ltcg_tip = None
    if annual_income > 500000:
        ltcg_tip = {
            "title": "LTCG Tax Harvesting",
            "tip":   "Sell equity mutual funds/stocks with gains up to ₹1,00,000 every March and immediately rebuy. Gains up to ₹1 lakh/year are tax-free. This resets your cost basis and saves 10% tax on future gains."
        }

    # Tax after deductions
    total_deductions    = sum(r["invest"] for r in recommendations)
    taxable_after       = max(0, annual_income - total_deductions - 50000)  # 50k standard deduction
    tax_after           = calculate_tax(taxable_after, TAX_SLABS_OLD)
    actual_tax_saved    = round(tax_without_deductions - tax_after, 2)

    return {
        "name":                   name,
        "annual_income":          annual_income,
        "tax_bracket":            bracket,
        "bracket_rate":           bracket_rate,
        "tax_without_deductions": tax_without_deductions,
        "tax_after_deductions":   tax_after,
        "total_tax_saved":        actual_tax_saved,
        "total_to_invest":        total_deductions,
        "recommendations":        recommendations,
        "ltcg_tip":               ltcg_tip,
        "sections":               TAX_SECTIONS
    }


def format_tax_for_ai(tax_data: dict) -> str:
    recs = ""
    for r in tax_data["recommendations"]:
        recs += f"""
- {r['section']} via {r['instrument']}
  Invest: ₹{r['invest']:,.0f} | Tax Saved: ₹{r['tax_saved']:,.0f}
  Why: {r['why']}
"""

    return f"""
TAX OPTIMIZATION ANALYSIS for {tax_data['name']}:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Annual Income        : ₹{tax_data['annual_income']:,.0f}
Tax Bracket          : {tax_data['tax_bracket']}
Tax Without Planning : ₹{tax_data['tax_without_deductions']:,.0f}
Tax After Planning   : ₹{tax_data['tax_after_deductions']:,.0f}
Total Tax Saved      : ₹{tax_data['total_tax_saved']:,.0f}

RECOMMENDED DEDUCTIONS:
{recs}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Based on this tax analysis, explain to {tax_data['name']}:
1. How much tax they are currently paying
2. Exactly how much they can save with each section
3. Which instrument to pick first and why
4. Step by step how to actually invest (which app, how to start)
5. LTCG harvesting tip if applicable
Use simple language. Give exact rupee amounts.
""".strip()