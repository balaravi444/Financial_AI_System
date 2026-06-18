# app/smart_tips_engine.py

from datetime import datetime
import random

DAILY_TIPS = [
    {
        "id":       "compound_power",
        "category": "investing",
        "tip":      "₹5,000/month SIP started at 25 becomes ₹3.5 crore at 60. The same SIP started at 35 becomes only ₹1.2 crore. Starting 10 years earlier = 3x more money.",
        "action":   "Start a SIP today, even ₹500/month. Every month you wait costs you lakhs.",
        "icon":     "📈"
    },
    {
        "id":       "emergency_fund",
        "category": "savings",
        "tip":      "Without an emergency fund, one medical crisis or job loss can wipe out years of savings and force you into debt.",
        "action":   "Open a liquid mutual fund account today. Transfer 10% of salary every month till you have 6 months expenses saved.",
        "icon":     "🛡️"
    },
    {
        "id":       "insurance_first",
        "category": "insurance",
        "tip":      "One hospitalisation without insurance costs ₹2-10 lakh. A ₹10 lakh health cover costs just ₹8,000-15,000/year at age 25.",
        "action":   "Compare health plans on Policybazaar this weekend. Takes 20 minutes. Could save your life savings.",
        "icon":     "🏥"
    },
    {
        "id":       "tax_saving",
        "category": "tax",
        "tip":      "Section 80C saves up to ₹46,800 tax per year (30% bracket). Most people don't use the full ₹1.5 lakh limit.",
        "action":   "Check if you've used your full 80C limit this year. ELSS mutual funds are the best 80C option.",
        "icon":     "💰"
    },
    {
        "id":       "sip_crash",
        "category": "investing",
        "tip":      "Market crashes are the best time to invest. When Nifty fell 35% in March 2020, those who kept their SIPs running doubled their money by 2021.",
        "action":   "Never stop SIP during a market crash. If anything, increase it by 50%.",
        "icon":     "📉"
    },
    {
        "id":       "food_delivery",
        "category": "savings",
        "tip":      "If you order food 15 times a month at ₹300/order = ₹4,500/month = ₹54,000/year. Invested as SIP for 10 years at 12% = ₹9.3 lakh.",
        "action":   "Cut food delivery to 8 times a month. Save ₹2,100/month and invest it.",
        "icon":     "🍕"
    },
    {
        "id":       "debt_first",
        "category": "debt",
        "tip":      "Credit card debt at 36-42% annual interest is the most expensive money in India. Paying it off is a guaranteed 36% return — better than any investment.",
        "action":   "If you have credit card dues, pay them fully before investing in anything else.",
        "icon":     "💳"
    },
    {
        "id":       "salary_hike",
        "category": "investing",
        "tip":      "When you get a salary hike, lifestyle inflation is the enemy. Most people spend 100% of their raise within months.",
        "action":   "Invest 50% of every salary hike. Keep only 50% for lifestyle improvement.",
        "icon":     "💼"
    },
    {
        "id":       "index_fund",
        "category": "investing",
        "tip":      "80% of professional mutual fund managers fail to beat the Nifty 50 index over 10 years. Yet index funds charge 10x less in fees.",
        "action":   "Put at least 50% of your equity SIP in a Nifty 50 index fund. Simple. Proven.",
        "icon":     "🎯"
    },
    {
        "id":       "term_insurance",
        "category": "insurance",
        "tip":      "₹1 crore term life insurance at age 28 costs ₹700/month. At age 38 it costs ₹1,400/month. Every year you wait doubles the cost.",
        "action":   "If someone depends on your income, buy term insurance this month.",
        "icon":     "👨‍👩‍👧"
    },
    {
        "id":       "gold_sgb",
        "category": "investing",
        "tip":      "Sovereign Gold Bonds give you gold's price appreciation PLUS 2.5% annual interest. Physical gold gives you neither the interest nor security.",
        "action":   "Never buy gold jewellery as investment. Use SGB or Gold ETF only.",
        "icon":     "🥇"
    },
    {
        "id":       "ltcg_harvest",
        "category": "tax",
        "tip":      "Equity gains up to ₹1.25 lakh/year are tax-free. If your gains exceed this, you're leaving free money on the table.",
        "action":   "Every March, sell equity funds with gains up to ₹1.25 lakh and immediately rebuy to reset cost basis.",
        "icon":     "🌾"
    },
    {
        "id":       "automate",
        "category": "savings",
        "tip":      "People who automate savings save 2-3x more than those who try to save what's left at month end. Willpower runs out. Automation doesn't.",
        "action":   "Set up auto-debit for SIP on salary day. Not the 5th. Not when you remember. Salary day.",
        "icon":     "⚙️"
    },
    {
        "id":       "ppf_power",
        "category": "tax",
        "tip":      "PPF at 7.1% tax-free is equivalent to a 10.1% FD for someone in 30% tax bracket. No FD in India gives 10%.",
        "action":   "Invest ₹1.5 lakh in PPF every April to maximise the compounding benefit for that financial year.",
        "icon":     "🏦"
    },
    {
        "id":       "review",
        "category": "investing",
        "tip":      "Most people check their portfolio during crashes and panic-sell. The best investors check it once a year.",
        "action":   "Set a calendar reminder for every January to review your portfolio. Do nothing rest of the year.",
        "icon":     "📅"
    }
]

CONTEXTUAL_ALERTS = {
    "no_insurance": {
        "priority": "CRITICAL",
        "alert":    "You have NO insurance. One medical emergency can wipe out your entire savings.",
        "action":   "Get health insurance this week. Minimum ₹5 lakh cover.",
        "icon":     "🚨"
    },
    "no_emergency_fund": {
        "priority": "HIGH",
        "alert":    "Without an emergency fund, you are one job loss away from financial crisis.",
        "action":   "Start a liquid fund SIP. Save 3 months expenses first, then 6 months.",
        "icon":     "⚠️"
    },
    "no_investments": {
        "priority": "HIGH",
        "alert":    "Every month without investing is compounding working against you, not for you.",
        "action":   "Start a ₹500 SIP today. Platform: Groww or Zerodha Coin.",
        "icon":     "⚠️"
    },
    "high_debt": {
        "priority": "HIGH",
        "alert":    "Your debt is costing you more in interest than any investment can make.",
        "action":   "Pay off all high-interest debt before investing.",
        "icon":     "⚠️"
    },
    "low_savings": {
        "priority": "MEDIUM",
        "alert":    "You are saving less than 10% of income. Financial security requires at least 20%.",
        "action":   "Find 3 expenses to cut this month. Even ₹1,000 more saved changes your future.",
        "icon":     "🔔"
    },
    "young_investor": {
        "priority": "INFO",
        "alert":    "You are young — time is your biggest asset. Every year of early investing is worth more than 2 years of late investing.",
        "action":   "Start SIP immediately. Even ₹500/month. Increase 10% every year.",
        "icon":     "💡"
    },
    "month_end": {
        "priority": "MEDIUM",
        "alert":    "It's the last week of the month. Most people overspend now. Track every expense carefully.",
        "action":   "Set a daily spending limit of ₹500 for the remaining days.",
        "icon":     "📅"
    }
}

MARKET_TIPS = {
    "market_down": {
        "condition": "When Nifty is 10%+ below recent high",
        "tip":       "Market is down — this is NOT the time to panic. It IS the time to increase SIP.",
        "action":    "If Nifty falls 15%+, consider doing a lump sum top-up in your index fund.",
        "icon":      "📉"
    },
    "market_up": {
        "condition": "When Nifty hits all-time high",
        "tip":       "Market at all-time high. Don't make large lump sum investments. Continue SIP only.",
        "action":    "Rebalance portfolio if equity allocation has grown beyond your target %.",
        "icon":      "📈"
    },
    "tax_season": {
        "condition": "January-March",
        "tip":       "Tax saving season. Last chance to invest in 80C instruments for this financial year.",
        "action":    "Check your 80C usage. Invest in ELSS or PPF before 31st March.",
        "icon":      "📋"
    },
    "new_fy": {
        "condition": "April — new financial year",
        "tip":       "New financial year started. Best time to invest in PPF (full year compounding), review SIP amounts, and update financial goals.",
        "action":    "Increase SIP by 10% today. It takes 2 minutes.",
        "icon":      "🎯"
    }
}


def get_contextual_alerts(profile: dict) -> list:
    alerts    = []
    income    = profile.get("monthly_income", 0)
    expenses  = profile.get("monthly_expenses", 0)
    savings   = income - expenses
    age       = profile.get("age", 30)
    insurance = profile.get("has_insurance", False)
    debts     = profile.get("debts", "none")
    investments = profile.get("existing_investments", "none")

    if not insurance:
        alerts.append(CONTEXTUAL_ALERTS["no_insurance"])

    if income > 0 and savings < income * 0.1:
        alerts.append(CONTEXTUAL_ALERTS["low_savings"])

    if investments.lower() in ["none", "no", ""]:
        alerts.append(CONTEXTUAL_ALERTS["no_investments"])

    if debts.lower() not in ["none", "no", ""]:
        alerts.append(CONTEXTUAL_ALERTS["high_debt"])

    if age < 27:
        alerts.append(CONTEXTUAL_ALERTS["young_investor"])

    today = datetime.now()
    if today.day >= 22:
        alerts.append(CONTEXTUAL_ALERTS["month_end"])

    month = today.month
    if month in [1, 2, 3]:
        alerts.append({
            "priority": "HIGH",
            "alert":    f"Tax saving deadline is 31st March — only {4 - month} month(s) left!",
            "action":   "Check your 80C usage now. Invest in ELSS or PPF before deadline.",
            "icon":     "📋"
        })

    if month == 4:
        alerts.append({
            "priority": "INFO",
            "alert":    "New financial year — perfect time to review and increase your SIPs.",
            "action":   "Increase each SIP by 10% today. It compounds massively over time.",
            "icon":     "🎯"
        })

    return alerts


def get_daily_tip(profile: dict) -> dict:
    today    = datetime.now()
    day_seed = today.day + today.month

    # Pick tip based on profile priorities
    income    = profile.get("monthly_income", 0)
    insurance = profile.get("has_insurance", False)
    debts     = profile.get("debts", "none")
    investments = profile.get("existing_investments", "none")

    # Priority tips based on situation
    if not insurance:
        for tip in DAILY_TIPS:
            if tip["id"] == "insurance_first":
                return tip

    if debts.lower() not in ["none", "no", ""]:
        for tip in DAILY_TIPS:
            if tip["id"] == "debt_first":
                return tip

    if investments.lower() in ["none", "no", ""]:
        for tip in DAILY_TIPS:
            if tip["id"] == "compound_power":
                return tip

    # Otherwise rotate through tips
    index = day_seed % len(DAILY_TIPS)
    return DAILY_TIPS[index]


def format_tips_for_ai(
    daily_tip: dict,
    alerts: list,
    profile: dict
) -> str:
    name   = profile.get("name", "User")
    income = profile.get("monthly_income", 0)
    age    = profile.get("age", 30)

    alert_text = ""
    for a in alerts[:3]:
        alert_text += f"\n{a['icon']} [{a['priority']}] {a['alert']}\n   Action: {a['action']}"

    return f"""
SMART TIPS ENGINE for {name}:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TODAY'S TIP ({daily_tip['icon']} {daily_tip['category'].upper()}):
{daily_tip['tip']}
Action: {daily_tip['action']}

PERSONALISED ALERTS FOR {name.upper()}:
{alert_text if alert_text else "No critical alerts — you're on track!"}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Based on these tips and alerts for {name} (age {age}, income ₹{income:,.0f}/month):
1. Expand on today's tip with a real example using their income
2. Address the most critical alert first with specific action steps
3. Give one powerful financial insight they probably don't know
4. End with one sentence of genuine motivation
Keep it concise, punchy, and actionable. No fluff.
""".strip()