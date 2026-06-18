from pydantic import BaseModel

class UserProfile(BaseModel):
    session_id: str
    name: str
    age: int
    monthly_income: float
    monthly_expenses: float
    risk_tolerance: str = "medium"
    financial_goals: str = "not specified"
    existing_investments: str = "none"
    has_insurance: bool = False
    dependents: int = 0
    debts: str = "none"

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    session_id: str

class ProfileResponse(BaseModel):
    success: bool
    message: str