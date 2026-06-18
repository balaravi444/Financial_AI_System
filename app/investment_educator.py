# app/investment_educator.py

INVESTMENT_LESSONS = {
    "stocks": {
        "id":    "stocks",
        "title": "Stocks — owning a piece of a company",
        "emoji": "📈",
        "layer1": {
            "what":    "A stock is a tiny piece of ownership in a company. When you buy 1 share of Reliance, you literally own a small part of Reliance Industries.",
            "analogy": "Think of a company as a pizza. A stock is one slice. If the pizza becomes more valuable, your slice is worth more too."
        },
        "layer2": {
            "how_it_makes_money": [
                "Price appreciation — company grows, stock price rises. You buy at ₹100, sell at ₹150 = ₹50 profit.",
                "Dividends — company shares profits with shareholders. Like interest, but variable.",
                "Bonus shares — company gives free extra shares to existing shareholders."
            ],
            "how_you_lose_money": [
                "Company performs badly — stock price falls.",
                "Market crash — even good stocks fall when overall market panics.",
                "Wrong timing — buying at peak, panic-selling at bottom."
            ]
        },
        "layer3": {
            "real_numbers": {
                "nifty50_10yr_return": "12-14% CAGR (last 20 years)",
                "best_year":           "Nifty gained 75% in 2009 (post-crash recovery)",
                "worst_year":          "Nifty fell 52% in 2008 (global financial crisis)",
                "min_investment":      "₹1 — you can buy fractional shares via some brokers",
                "tax":                 "STCG 20% (held < 1 year), LTCG 12.5% above ₹1.25 lakh/year"
            },
            "realistic_expectation": "Expect 12-14% annually over 10+ years. Expect -30% to -50% in bad years. Never invest money you need in 1-2 years."
        },
        "how_to_start":  "Open Zerodha or Groww account. Complete KYC with Aadhaar + PAN. Start with Nifty 50 index fund before picking individual stocks.",
        "beginner_tip":  "Don't try to pick winning stocks. 90% of professional fund managers can't beat the index. Start with index funds.",
        "risk_level":    "Medium-High",
        "time_horizon":  "5+ years minimum"
    },
    "mutual_funds": {
        "id":    "mutual_funds",
        "title": "Mutual Funds — investing made easy",
        "emoji": "🏦",
        "layer1": {
            "what":    "A mutual fund pools money from thousands of investors and a professional fund manager invests it across many stocks/bonds. You own units of the fund, not individual stocks.",
            "analogy": "Instead of buying one stock yourself, you join a group of 10,000 people and a professional shops for all of you together."
        },
        "layer2": {
            "how_it_makes_money": [
                "NAV (Net Asset Value) rises as underlying stocks/bonds grow.",
                "Dividends from underlying stocks get reinvested.",
                "SIP (Systematic Investment Plan) — invest fixed amount monthly, buy more units when price is low."
            ],
            "types": {
                "Large Cap":  "Top 100 companies. Safe, stable. 10-12% returns.",
                "Mid Cap":    "Companies ranked 101-250. More growth, more risk. 13-16% returns.",
                "Small Cap":  "Companies ranked 251+. High growth, high risk. 15-20% returns.",
                "Index Fund": "Copies Nifty 50. No fund manager needed. Lowest cost. 12-14% returns.",
                "ELSS":       "Tax saving fund. 3-year lock-in. 12-15% returns. 80C benefit.",
                "Debt Fund":  "Invests in bonds. Low risk. 7-8% returns. Better than FD post-tax.",
                "Liquid":     "Like a savings account but better. 6-7% returns. Withdraw anytime."
            }
        },
        "layer3": {
            "real_numbers": {
                "min_sip":        "₹100/month (some funds allow ₹500 minimum)",
                "expense_ratio":  "0.1-1.5% per year (index funds cheapest)",
                "index_vs_active": "Index funds beat 80% of active funds over 10 years",
                "tax_equity":     "LTCG 12.5% above ₹1.25 lakh/year (held 1+ year)",
                "tax_debt":       "Added to income, taxed at your slab rate"
            },
            "realistic_expectation": "Large cap: 10-12%, Mid cap: 13-16%, Small cap: 15-20%. Returns are NOT guaranteed. Past performance ≠ future returns."
        },
        "how_to_start":  "Download Groww or Zerodha Coin. Search 'Nifty 50 Index Fund'. Start SIP with ₹500/month. Increase by 10% every year.",
        "beginner_tip":  "Start with a Nifty 50 index fund. It's the single best investment for most Indians. Simple, low cost, proven.",
        "risk_level":    "Low to High (depends on type)",
        "time_horizon":  "3+ years (equity), 1+ year (debt)"
    },
    "fd": {
        "id":    "fd",
        "title": "Fixed Deposit — the safe choice",
        "emoji": "🏛️",
        "layer1": {
            "what":    "An FD is a loan you give to the bank at a fixed interest rate for a fixed period. The bank guarantees to return your money plus interest.",
            "analogy": "You lend ₹1 lakh to the bank for 1 year. They pay you ₹7,000 as rent for using your money."
        },
        "layer2": {
            "how_it_makes_money": [
                "Fixed interest rate agreed upfront — currently 6.5-8.5% per year.",
                "Interest compounds quarterly in most FDs.",
                "Senior citizens get 0.25-0.5% extra rate.",
                "Tax Saver FD (5-year lock-in) qualifies for 80C deduction."
            ],
            "risks": [
                "Inflation risk — if inflation is 6% and FD gives 6.5%, real gain is only 0.5%.",
                "Tax risk — FD interest is fully taxable as income.",
                "Penalty for early withdrawal — typically 0.5-1% penalty."
            ]
        },
        "layer3": {
            "real_numbers": {
                "current_rates":    "SBI 6.5-7%, HDFC 7-7.5%, Small Finance Banks up to 9%",
                "insurance_cover":  "DICGC insures up to ₹5 lakh per bank. Split across banks if more.",
                "post_tax_return":  "At 30% tax slab: 7% FD → 4.9% actual return",
                "vs_debt_fund":     "Debt mutual fund at 7% return — taxed at slab only on redemption (more efficient)"
            },
            "realistic_expectation": "FD gives guaranteed returns but tax eats heavily. Better for emergency fund and short-term goals (1-3 years). Not ideal for long-term wealth."
        },
        "how_to_start":  "Open FD directly from your bank app (HDFC, SBI, ICICI all support). Or use Stable Money / Groww FD for comparison.",
        "beginner_tip":  "Use FD for emergency fund backup and goals within 1-3 years. For 3+ years, debt mutual funds beat FD post-tax.",
        "risk_level":    "Very Low",
        "time_horizon":  "1 month to 10 years"
    },
    "ppf": {
        "id":    "ppf",
        "title": "PPF — the government's gift to taxpayers",
        "emoji": "🏦",
        "layer1": {
            "what":    "Public Provident Fund is a government savings scheme with 7.1% interest that is completely tax-free — no tax on investment, no tax on interest, no tax on withdrawal.",
            "analogy": "PPF is like an FD that the government gives special protection to. The 7.1% is tax-free, which means it beats most FDs after tax."
        },
        "layer2": {
            "how_it_makes_money": [
                "7.1% per year, compounded annually (government sets rate, changes rarely).",
                "EEE status — Exempt on investment (80C), Exempt on interest, Exempt on maturity.",
                "15-year lock-in with partial withdrawal from year 7."
            ],
            "best_for": [
                "Safe long-term savings with tax benefits.",
                "People in 20-30% tax bracket — the tax saving makes effective return 9-10%.",
                "Retirement fund component."
            ]
        },
        "layer3": {
            "real_numbers": {
                "annual_limit":    "₹1.5 lakh maximum per year",
                "lock_in":         "15 years (extendable in 5-year blocks)",
                "effective_return": "For 30% tax bracket: 7.1% tax-free ≈ 10.1% pre-tax FD equivalent",
                "loan_facility":   "Loan against PPF from year 3 to year 6 at 1% above PPF rate"
            },
            "realistic_expectation": "7.1% fully tax-free is excellent for a guaranteed instrument. Best used as the safe portion of a retirement portfolio."
        },
        "how_to_start":  "Open PPF account at any SBI branch or online via SBI YONO. Or HDFC/ICICI bank. Minimum ₹500/year. Maximum ₹1.5 lakh/year.",
        "beginner_tip":  "Invest ₹12,500/month (₹1.5 lakh/year) in PPF if you want completely safe, tax-free growth. Open today — the 15-year clock starts now.",
        "risk_level":    "Zero (government guaranteed)",
        "time_horizon":  "15 years minimum"
    },
    "gold": {
        "id":    "gold",
        "title": "Gold — the oldest wealth protector",
        "emoji": "🥇",
        "layer1": {
            "what":    "Gold is a precious metal that has stored value for 5,000 years. When rupee weakens or markets crash, gold usually holds or gains value.",
            "analogy": "Gold is insurance for your portfolio. When everything else is burning, gold usually survives."
        },
        "layer2": {
            "how_it_makes_money": [
                "Price appreciation — gold price rises over long term (8-10% annually in India).",
                "Rupee depreciation hedge — as rupee weakens vs dollar, gold price rises in India.",
                "Crisis hedge — gold rose 25% in 2020 when COVID crashed markets."
            ],
            "ways_to_invest": {
                "Physical Gold":       "Jewellery/coins — making charges (10-25%) are a major cost. Avoid for investment.",
                "Gold ETF":            "Buy gold like a stock via your demat account. No storage risk. Purest form.",
                "Sovereign Gold Bond": "Government bonds linked to gold price + 2.5% extra interest. Best option.",
                "Digital Gold":        "Groww/PhonePe sell digital gold. Easy but check storage charges."
            }
        },
        "layer3": {
            "real_numbers": {
                "10yr_return":    "Gold gave ~10% CAGR in India over last 20 years",
                "sgb_bonus":      "Sovereign Gold Bond gives gold returns + 2.5%/year interest",
                "ideal_allocation": "5-10% of total portfolio in gold",
                "tax_sgb":        "SGB held to maturity (8 years) — capital gains are tax-free"
            },
            "realistic_expectation": "Gold is not a wealth creator — it's a wealth protector. Keep 5-10% in gold. Don't overinvest. It underperforms equity over 20+ years."
        },
        "how_to_start":  "Buy Sovereign Gold Bond when RBI issues (check rbi.org.in). Or buy Nippon Gold ETF via Zerodha/Groww.",
        "beginner_tip":  "Skip physical gold jewellery for investment — you lose 15-25% in making charges. Use SGB or Gold ETF only.",
        "risk_level":    "Low-Medium",
        "time_horizon":  "3+ years"
    },
    "nps": {
        "id":    "nps",
        "title": "NPS — supercharge your retirement",
        "emoji": "🎯",
        "layer1": {
            "what":    "National Pension System is a government retirement scheme. You invest monthly and get a pension after 60. Extra ₹50,000 tax deduction beyond 80C.",
            "analogy": "NPS is a forced retirement savings scheme with a bonus tax saving of ₹50,000 every year."
        },
        "layer2": {
            "how_it_makes_money": [
                "Invests in equity + bonds mix based on your age (auto choice).",
                "Returns driven by market performance — historically 10-12%.",
                "Tax saving: 80CCD(1B) gives extra ₹50,000 deduction beyond 80C."
            ],
            "rules": [
                "Can withdraw 60% as lump sum at 60 — tax-free.",
                "40% must be used to buy annuity (monthly pension).",
                "Partial withdrawal allowed for specific purposes after 3 years."
            ]
        },
        "layer3": {
            "real_numbers": {
                "tax_benefit":     "At 30% bracket: ₹50,000 extra deduction saves ₹15,000 tax/year",
                "historical_return": "Tier 1 equity plan: 12-14% CAGR (last 10 years)",
                "min_contribution": "₹1,000/year minimum",
                "lock_in":         "Till age 60 (partial withdrawal allowed from year 3)"
            },
            "realistic_expectation": "NPS is best for the tax saving angle. The lock-in till 60 is restrictive but forces retirement discipline. Good complement to mutual funds."
        },
        "how_to_start":  "Open NPS at enps.nsdl.com or through your bank. PRAN number issued immediately. Start with ₹5,000/month.",
        "beginner_tip":  "Use NPS specifically for the extra ₹50,000 tax deduction. Invest ₹50,000/year = save ₹15,000 tax (30% bracket). That's 30% instant return.",
        "risk_level":    "Low-Medium",
        "time_horizon":  "Till retirement (age 60)"
    }
}


def get_lesson(topic: str) -> dict | None:
    topic_map = {
        "stock":   "stocks",
        "stocks":  "stocks",
        "share":   "stocks",
        "equity":  "stocks",
        "mf":      "mutual_funds",
        "mutual":  "mutual_funds",
        "sip":     "mutual_funds",
        "fund":    "mutual_funds",
        "fd":      "fd",
        "fixed":   "fd",
        "deposit": "fd",
        "ppf":     "ppf",
        "gold":    "gold",
        "nps":     "nps",
        "pension": "nps"
    }

    key = None
    for k, v in topic_map.items():
        if k in topic.lower():
            key = v
            break

    if not key:
        return None
    return INVESTMENT_LESSONS.get(key)


def format_lesson_for_ai(lesson: dict, profile: dict) -> str:
    age    = profile.get("age", 30)
    income = profile.get("monthly_income", 0)
    risk   = profile.get("risk_tolerance", "medium")
    name   = profile.get("name", "User")

    l2 = lesson["layer2"]
    l3 = lesson["layer3"]

    money_points = "\n".join(
        f"- {m}" for m in l2.get("how_it_makes_money", [])
    )
    numbers = "\n".join(
        f"- {k}: {v}"
        for k, v in l3["real_numbers"].items()
    )

    return f"""
INVESTMENT EDUCATION REQUEST — {lesson['title']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Student profile: {name}, age {age}, income ₹{income:,.0f}/month, risk: {risk}

LAYER 1 — WHAT IT IS:
{lesson['layer1']['what']}
Analogy: {lesson['layer1']['analogy']}

LAYER 2 — HOW IT MAKES MONEY:
{money_points}

LAYER 3 — REAL NUMBERS:
{numbers}
Expected return: {l3['realistic_expectation']}

Risk level   : {lesson['risk_level']}
Time horizon : {lesson['time_horizon']}
How to start : {lesson['how_to_start']}
Beginner tip : {lesson['beginner_tip']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Teach {name} about {lesson['title']} using all 3 layers above.
Use simple language. Use the analogy. Give real rupee examples
based on their ₹{income:,.0f} income. Tell them exactly whether
THIS instrument suits their age ({age}) and risk tolerance ({risk}).
End with: should {name} invest in this? Yes/No/Maybe and exactly why.
""".strip()


def get_learning_path(profile: dict) -> list:
    age  = profile.get("age", 30)
    risk = profile.get("risk_tolerance", "medium")

    if age < 28:
        return [
            {"order": 1, "topic": "mutual_funds", "reason": "Best starting point for young investors"},
            {"order": 2, "topic": "ppf",          "reason": "Safe foundation + tax saving"},
            {"order": 3, "topic": "stocks",        "reason": "Learn after mutual fund basics"},
            {"order": 4, "topic": "fd",            "reason": "For emergency fund"},
            {"order": 5, "topic": "gold",          "reason": "Portfolio protection"},
            {"order": 6, "topic": "nps",           "reason": "Start retirement planning early"}
        ]
    elif risk == "low":
        return [
            {"order": 1, "topic": "fd",            "reason": "Safe, guaranteed returns"},
            {"order": 2, "topic": "ppf",           "reason": "Best safe tax-free option"},
            {"order": 3, "topic": "mutual_funds",  "reason": "Start with debt funds"},
            {"order": 4, "topic": "gold",          "reason": "Portfolio hedge"},
            {"order": 5, "topic": "nps",           "reason": "Retirement planning"},
            {"order": 6, "topic": "stocks",        "reason": "Only 10% allocation"}
        ]
    else:
        return [
            {"order": 1, "topic": "mutual_funds",  "reason": "Core of your portfolio"},
            {"order": 2, "topic": "stocks",        "reason": "Higher returns with more research"},
            {"order": 3, "topic": "ppf",           "reason": "Safe tax-free component"},
            {"order": 4, "topic": "nps",           "reason": "Extra ₹50k tax saving"},
            {"order": 5, "topic": "gold",          "reason": "5-10% hedge"},
            {"order": 6, "topic": "fd",            "reason": "Emergency fund only"}
        ]