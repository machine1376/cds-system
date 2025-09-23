# backend/main.py
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv
import logging
from api import clinical, drugs, knowledge, guidelines, knowledge_repository

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Clinical Decision Support API",
    description="AI-powered clinical decision support system for healthcare professionals",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security
security = HTTPBearer()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:8080", "http://127.0.0.1:3000", "http://127.0.0.1:3001", "http://127.0.0.1:3002", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(clinical.router)
app.include_router(drugs.router)
app.include_router(knowledge.router)
app.include_router(guidelines.router)
app.include_router(knowledge_repository.router)
# app.include_router(users.router)
# app.include_router(auth.router)
# app.include_router(assessments.router)
# app.include_router(training.router)
# app.include_router(admin.router)

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "Clinical Decision Support API",
        "version": "1.0.0",
        "timestamp": "2024-01-01T00:00:00Z"
    }

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Clinical Decision Support System API",
        "documentation": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )