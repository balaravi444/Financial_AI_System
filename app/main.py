# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.agent import get_ai_response
from app.models import UserProfile, ChatRequest, ChatResponse, ProfileResponse
from app.database import save_profile, get_profile
from app.stock_routes import router as stock_router
from app.db_manager import (
    init_db, save_message,
    get_conversation_history
)
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s"
)
logger = logging.getLogger("financeai")

# Init DB once here
init_db()

app = FastAPI(title="FinanceAI", version="4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(stock_router)


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/profile", response_model=ProfileResponse)
def save_user_profile(profile: UserProfile):
    save_profile(profile.session_id, profile.dict())
    logger.info(f"Profile saved: {profile.name}")
    return ProfileResponse(
        success=True,
        message=f"Profile saved for {profile.name}"
    )


@app.get("/profile/{session_id}")
def get_user_profile(session_id: str):
    profile = get_profile(session_id)
    if profile:
        return {"exists": True, "profile": profile}
    return {"exists": False, "profile": None}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Load history from DB — survives restarts
    history = get_conversation_history(request.session_id, limit=20)

    history.append({
        "role":    "user",
        "content": request.message
    })

    user_profile = get_profile(request.session_id)
    reply        = get_ai_response(history, user_profile)

    # Persist both messages
    save_message(request.session_id, "user",      request.message)
    save_message(request.session_id, "assistant", reply)

    logger.info(f"Chat — session {request.session_id[:8]}...")
    return ChatResponse(reply=reply, session_id=request.session_id)


@app.get("/health")
def health():
    return {"status": "FinanceAI running", "version": "4.0"}