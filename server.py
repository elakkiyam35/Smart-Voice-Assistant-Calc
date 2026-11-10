"""
FastAPI Server for Smart Voice Assistant Calculator Using Artificial Intelligence.
Provides RESTful APIs for Voice/Text calculations, OCR processing,
Multi-turn conversational dialog, User Authentication, History, and Settings.
"""

import os
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, Request, HTTPException, status, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.math_engine import MathEngine
from core.conversational import ConversationManager
from core.ocr_engine import OCREngine
from core.database import (
    init_db,
    register_user,
    login_user,
    reset_password,
    save_history,
    get_history,
    delete_history_item,
    clear_all_history,
    get_user_settings,
    save_user_settings
)

# Initialize core services
math_engine = MathEngine(angle_mode='deg')
conversation_manager = ConversationManager(math_engine)
ocr_engine = OCREngine(math_engine)

app = FastAPI(
    title="Smart Voice Assistant Calculator API",
    description="Intelligent AI-powered Voice Assistant Calculator backend with SymPy, multi-turn follow-ups, OCR, and history.",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static directories exist
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# -------------------------------------------------------------
# Pydantic Request Models
# -------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    user_id: Optional[int] = None
    angle_mode: Optional[str] = "deg"


class CalculateRequest(BaseModel):
    expression: str
    user_id: Optional[int] = None
    angle_mode: Optional[str] = "deg"


class OCRRequest(BaseModel):
    image_base64: Optional[str] = None
    ocr_text: Optional[str] = None
    user_id: Optional[int] = None


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username_or_email: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: str
    new_password: str


class SettingsRequest(BaseModel):
    user_id: Optional[int] = None
    theme: Optional[str] = "dark"
    voice_enabled: Optional[bool] = True
    speech_rate: Optional[float] = 1.0
    speech_pitch: Optional[float] = 1.0
    voice_name: Optional[str] = ""
    angle_mode: Optional[str] = "deg"


# -------------------------------------------------------------
# Frontend Root Route
# -------------------------------------------------------------

@app.get("/")
async def serve_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Smart Voice Assistant Calculator API is running. index.html not yet installed."}


# -------------------------------------------------------------
# Conversation & Calculation Endpoints
# -------------------------------------------------------------

@app.post("/api/chat")
async def handle_chat(req: ChatRequest):
    """
    Main conversational endpoint: handles voice transcripts and text queries,
    maintains multi-turn context, follow-ups, and logs to calculation history.
    """
    if req.angle_mode:
        math_engine.set_angle_mode(req.angle_mode)

    res = conversation_manager.process_message(req.message, session_id=req.session_id or "default")

    # Save to history if calculation was performed successfully
    if res.get('status') == 'success' and res.get('raw_answer') is not None:
        save_history(
            user_id=req.user_id,
            query=req.message,
            expression=res['visual_output'].get('expression', req.message),
            operation_name=res['visual_output'].get('operation_name', 'Calculation'),
            answer=str(res['raw_answer']),
            steps=res['visual_output'].get('steps', []),
            status='success'
        )

    return res


@app.post("/api/calculate")
async def direct_calculate(req: CalculateRequest):
    """
    Direct calculation endpoint for keypad / direct text queries.
    """
    if req.angle_mode:
        math_engine.set_angle_mode(req.angle_mode)

    res = math_engine.calculate(req.expression)

    if res.get('status') == 'success' and res.get('raw_answer') is not None:
        save_history(
            user_id=req.user_id,
            query=req.expression,
            expression=res['visual_output'].get('expression', req.expression),
            operation_name=res['visual_output'].get('operation_name', 'Calculation'),
            answer=str(res['raw_answer']),
            steps=res['visual_output'].get('steps', []),
            status='success'
        )

    return res


@app.post("/api/ocr")
async def process_ocr(
    image: Optional[UploadFile] = File(None),
    image_base64: Optional[str] = Form(None),
    ocr_text: Optional[str] = Form(None),
    user_id: Optional[int] = Form(None)
):
    """
    OCR endpoint: Accepts image file upload, Base64 image, or client-side OCR text.
    Extracts mathematical expression, solves it, and returns full 3-format output.
    """
    img_bytes = None
    if image:
        img_bytes = await image.read()

    res = ocr_engine.extract_and_solve(
        image_bytes=img_bytes,
        base64_data=image_base64,
        client_ocr_text=ocr_text
    )

    if res.get('status') == 'success' and res.get('raw_answer') is not None:
        save_history(
            user_id=user_id,
            query=f"[Image OCR] {res.get('detected_text')}",
            expression=res['visual_output'].get('expression', res.get('detected_text', 'Image Equation')),
            operation_name=res['visual_output'].get('operation_name', 'Image OCR'),
            answer=str(res['raw_answer']),
            steps=res['visual_output'].get('steps', []),
            status='success'
        )

    return res


# -------------------------------------------------------------
# User Authentication Endpoints
# -------------------------------------------------------------

@app.post("/api/auth/register")
async def register(req: RegisterRequest):
    success, msg, user_data = register_user(req.username, req.email, req.password)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg, "user": user_data}


@app.post("/api/auth/login")
async def login(req: LoginRequest):
    success, msg, user_data = login_user(req.username_or_email, req.password)
    if not success:
        raise HTTPException(status_code=401, detail=msg)
    return {"message": msg, "user": user_data}


@app.post("/api/auth/forgot-password")
async def forgot_password(req: ForgotPasswordRequest):
    success, msg = reset_password(req.email, req.new_password)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"message": msg}


# -------------------------------------------------------------
# Calculation History Endpoints
# -------------------------------------------------------------

@app.get("/api/history")
async def fetch_history(user_id: Optional[int] = None, filter_type: Optional[str] = None):
    records = get_history(user_id=user_id, limit=100, filter_type=filter_type)
    return {"history": records}


@app.delete("/api/history/{item_id}")
async def delete_item(item_id: int, user_id: Optional[int] = None):
    deleted = delete_history_item(user_id=user_id, item_id=item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="History record not found.")
    return {"message": "Calculation deleted from history."}


@app.delete("/api/history")
async def clear_history(user_id: Optional[int] = None):
    clear_all_history(user_id=user_id)
    return {"message": "All calculation history cleared successfully."}


# -------------------------------------------------------------
# Settings Endpoints
# -------------------------------------------------------------

@app.get("/api/settings")
async def fetch_settings(user_id: Optional[int] = None):
    settings_data = get_user_settings(user_id)
    return {"settings": settings_data}


@app.post("/api/settings")
async def update_settings(req: SettingsRequest):
    data = req.dict(exclude_unset=True)
    user_id = data.pop('user_id', None)
    save_user_settings(user_id, data)
    if req.angle_mode:
        math_engine.set_angle_mode(req.angle_mode)
    return {"message": "Settings updated successfully."}


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": "Smart Voice Assistant Calculator Using Artificial Intelligence",
        "version": "2.0.0"
    }

