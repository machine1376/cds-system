# backend/main_prod.py - Production version with static file serving
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(clinical.router)
app.include_router(drugs.router)
app.include_router(knowledge.router)
app.include_router(guidelines.router)
app.include_router(knowledge_repository.router)

# Mount static files (React frontend)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

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
        "main_prod:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
