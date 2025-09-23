# backend/models/schemas.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class SeverityLevel(str, Enum):
    CONTRAINDICATED = "contraindicated"
    MAJOR = "major"
    MODERATE = "moderate"
    MINOR = "minor"

class EvidenceLevel(str, Enum):
    A = "A"  # High-quality evidence
    B = "B"  # Moderate-quality evidence
    C = "C"  # Low-quality evidence

class UserRole(str, Enum):
    PHYSICIAN = "physician"
    NURSE = "nurse"
    PHARMACIST = "pharmacist"
    PHYSICIAN_ASSISTANT = "physician_assistant"
    STUDENT = "student"

# Patient Context Model
class PatientContext(BaseModel):
    age: Optional[int] = Field(None, ge=0, le=150, description="Patient age in years")
    gender: Optional[str] = Field(None, description="Patient gender")
    weight_kg: Optional[float] = Field(None, ge=0, description="Weight in kilograms")
    height_cm: Optional[float] = Field(None, ge=0, description="Height in centimeters")
    allergies: Optional[List[str]] = Field(default=[], description="Known allergies")
    current_medications: Optional[List[str]] = Field(default=[], description="Current medications")
    medical_conditions: Optional[List[str]] = Field(default=[], description="Active medical conditions")
    lab_values: Optional[Dict[str, Any]] = Field(default={}, description="Recent lab values")

# Clinical Query Models
class ClinicalQuery(BaseModel):
    query: str = Field(..., min_length=10, max_length=1000, description="Clinical question or scenario")
    patient_context: Optional[PatientContext] = None
    query_type: Optional[str] = Field("general", description="Type of query: diagnosis, treatment, drug_interaction")
    urgency: Optional[str] = Field("routine", description="Urgency: routine, urgent, emergent")
    
    @validator('query')
    def query_must_be_meaningful(cls, v):
        if len(v.strip()) < 10:
            raise ValueError('Query must be at least 10 characters long')
        return v.strip()

# Response Models
class Source(BaseModel):
    title: str
    url: Optional[str] = None
    type: str = Field(..., description="Type of source: guideline, study, textbook")
    evidence_level: EvidenceLevel

class ClinicalRecommendation(BaseModel):
    recommendation: str = Field(..., description="Primary clinical recommendation")
    confidence_score: float = Field(..., ge=0, le=1, description="Confidence score 0-1")
    evidence_level: EvidenceLevel
    reasoning: str = Field(..., description="Clinical reasoning behind recommendation")
    considerations: List[str] = Field(default=[], description="Important clinical considerations")
    contraindications: List[str] = Field(default=[], description="Contraindications to consider")
    monitoring: List[str] = Field(default=[], description="Monitoring requirements")
    sources: List[Source] = Field(default=[], description="Evidence sources")

class DrugInteraction(BaseModel):
    drug1: str
    drug2: str
    severity: SeverityLevel
    description: str
    mechanism: Optional[str] = None
    management: str = Field(..., description="Clinical management recommendation")
    sources: List[str] = Field(default=[])

class ClinicalResponse(BaseModel):
    query_id: str
    recommendations: List[ClinicalRecommendation]
    drug_interactions: List[DrugInteraction] = Field(default=[])
    differential_diagnoses: List[str] = Field(default=[])
    red_flags: List[str] = Field(default=[], description="Critical warning signs")
    next_steps: List[str] = Field(default=[], description="Recommended next steps")
    timestamp: datetime = Field(default_factory=datetime.now)
    processing_time_ms: Optional[float] = None

# User and Authentication Models
class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$')
    role: UserRole
    full_name: str = Field(..., min_length=2, max_length=100)
    license_number: Optional[str] = None
    institution: Optional[str] = None

class UserCreate(User):
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

# Feedback and Quality Models
class FeedbackRating(BaseModel):
    query_id: str
    rating: int = Field(..., ge=1, le=5, description="Rating 1-5")
    feedback_text: Optional[str] = None
    was_helpful: bool
    used_recommendation: bool
    user_id: str

# Training and Assessment Models
class TrainingModule(BaseModel):
    module_id: str
    title: str
    description: str
    estimated_duration_minutes: int
    prerequisites: List[str] = Field(default=[])
    learning_objectives: List[str]

class AssessmentQuestion(BaseModel):
    question_id: str
    question_text: str
    options: List[str]
    correct_answer: int
    explanation: str
    difficulty_level: int = Field(ge=1, le=5)

class AssessmentResult(BaseModel):
    user_id: str
    module_id: str
    score: float = Field(ge=0, le=100)
    passed: bool
    time_taken_minutes: int
    incorrect_questions: List[str] = Field(default=[])