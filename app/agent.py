# app/agent.py
import os
from groq import Groq
from dotenv import load_dotenv
from app.fraud_shield import scan_for_fraud, get_fraud_warning_prompt

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_SYSTEM_PROMPT = """You are FinanceAI, an expert Indian financial advisor 
and stock market analyst. You follow all SEBI and NSE rules. You explain 
everything clearly in simple English — how stocks work, mutual funds, FDs, 
insurance, savings tips, tax saving, and investment planning.

You always:
- Address the user by their first name
- Give step-by-step reasoning before any recommendation  
- Tailor advice to the user's exact income, age, and goals
- Flag urgent gaps (no insurance, high debt, no emergency fund)
- End every response with: ⚠️ This is educational information, not SEBI-registered investment advice.

You never give generic advice when you know the user's profile."""


def build_smart_context(profile: dict) -> str:
    if not profile:
        return ""

    income   = profile.get("monthly_income", 0)
    expenses = profile.get("monthly_expenses", 0)
    savings  = income - expenses
    age      = profile.get("age", 30)
    name     = profile.get("name", "User")

    flags = []

    if not profile.get("has_insurance"):
        flags.append("🚨 NO INSURANCE — proactively suggest term + health insurance if relevant")

    if savings < income * 0.1:
        flags.append("🚨 LOW SAVINGS RATE (under 10%) — suggest cutting expenses first")
    elif savings < income * 0.2:
        flags.append("⚠️ SAVINGS RATE BELOW 20% — gently encourage increasing savings")

    if profile.get("debts", "none").lower() not in ["none", "no", ""]:
        flags.append("⚠️ HAS ACTIVE DEBT/EMI — suggest clearing high-interest debt before investing")

    if profile.get("existing_investments", "none").lower() in ["none", "no", ""]:
        flags.append("📌 NO INVESTMENTS YET — start with basics: emergency fund, then SIP")

    if age < 25:
        flags.append("👤 YOUNG INVESTOR — explain basics clearly, focus on habits not complexity")
    elif age > 50:
        flags.append("👤 NEAR RETIREMENT — focus on capital preservation and stable income")

    emergency_fund_target = expenses * 6
    flags.append(f"📊 Emergency fund target: ₹{emergency_fund_target:,.0f} (6 months expenses)")

    flag_text = "\n".join(f"- {f}" for f in flags)

    return f"""
LIVE USER PROFILE — use this to personalise every single response:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name            : {name}
Age             : {age} years old
Monthly Income  : ₹{income:,.0f}
Monthly Expenses: ₹{expenses:,.0f}
Monthly Savings : ₹{savings:,.0f} ({round(savings/income*100) if income else 0}% of income)
Risk Tolerance  : {profile.get("risk_tolerance", "medium")}
Goals           : {profile.get("financial_goals", "not specified")}
Investments     : {profile.get("existing_investments", "none")}
Insurance       : {"Yes" if profile.get("has_insurance") else "No"}
Dependents      : {profile.get("dependents", 0)}
Debts/EMIs      : {profile.get("debts", "none")}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SMART FLAGS (act on these automatically):
{flag_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Always address this user as {name}. Never give generic advice.
""".strip()


def get_ai_response(
    conversation_history: list,
    user_profile: dict | None = None
) -> str:

    # Get the last user message for fraud scanning
    last_user_message = ""
    for msg in reversed(conversation_history):
        if msg.get("role") == "user":
            last_user_message = msg.get("content", "")
            break

    # Scan for fraud patterns
    fraud_result = scan_for_fraud(last_user_message)

    system_prompt = BASE_SYSTEM_PROMPT

    if user_profile:
        context = build_smart_context(user_profile)
        system_prompt = f"{BASE_SYSTEM_PROMPT}\n\n{context}"

    # If fraud detected — inject fraud warning into the conversation
    if fraud_result["fraud_detected"]:
        fraud_prompt = get_fraud_warning_prompt(fraud_result, last_user_message)
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history[:-1])
        messages.append({"role": "user", "content": fraud_prompt})
    else:
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(conversation_history)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1500,
        temperature=0.4
    )

    reply = response.choices[0].message.content

    # If fraud detected — prepend the formatted warning card
    if fraud_result["fraud_detected"]:
        from app.fraud_shield import format_fraud_response
        warning_card = format_fraud_response(fraud_result)
        reply = warning_card + "\n\n" + reply

    return reply