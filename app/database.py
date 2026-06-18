# app/database.py
from app.db_manager import (
    save_profile    as db_save_profile,
    get_profile     as db_get_profile,
    save_message,
    get_conversation_history
)

def save_profile(session_id: str, profile_data: dict):
    db_save_profile(session_id, profile_data)

def get_profile(session_id: str) -> dict | None:
    return db_get_profile(session_id)

def profile_exists(session_id: str) -> bool:
    return get_profile(session_id) is not None

def format_profile_for_ai(profile: dict) -> str:
    income   = profile.get("monthly_income", 0)
    expenses = profile.get("monthly_expenses", 0)
    savings  = income - expenses
    return f"""
USER PROFILE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name     : {profile.get('name')}
Age      : {profile.get('age')}
Income   : ₹{income:,.0f}/month
Expenses : ₹{expenses:,.0f}/month
Savings  : ₹{savings:,.0f}/month ({round(savings/income*100) if income else 0}%)
Risk     : {profile.get('risk_tolerance','medium')}
Goals    : {profile.get('financial_goals','not specified')}
Invested : {profile.get('existing_investments','none')}
Insurance: {'Yes' if profile.get('has_insurance') else 'No'}
Dependents:{profile.get('dependents',0)}
Debts    : {profile.get('debts','none')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Always address by name. Never give generic advice.
""".strip()