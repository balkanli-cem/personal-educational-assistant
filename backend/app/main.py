from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from datetime import datetime

from .models.database import get_db
from .routers import auth, educational, user_profile, ai_educational

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Personalized Educational Assistant API",
    description="AI-powered educational platform with personalized learning experiences",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(educational.router, prefix="/api/educational", tags=["educational"])
app.include_router(user_profile.router, prefix="/api/profile", tags=["user-profile"])
app.include_router(ai_educational.router, prefix="/api/ai", tags=["ai-educational"])

@app.get("/")
async def root():
    return {"message": "Personalized Educational Assistant API", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy", 
        "service": "educational-assistant",
        "timestamp": datetime.utcnow().isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)