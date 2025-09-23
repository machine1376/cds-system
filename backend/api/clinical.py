# backend/api/clinical.py
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List
import uuid
import time
from datetime import datetime

from models.schemas import (
    ClinicalQuery, ClinicalResponse, ClinicalRecommendation, 
    DrugInteraction, Source, EvidenceLevel, SeverityLevel
)

router = APIRouter(prefix="/clinical", tags=["Clinical Decision Support"])

# Mock data for testing - replace with actual AI service
def mock_clinical_service(query: ClinicalQuery) -> ClinicalResponse:
    """Temporary mock service - replace with actual AI implementation"""
    start_time = time.time()
    
    # Mock recommendation
    recommendation = ClinicalRecommendation(
        recommendation="Based on the clinical presentation, consider acute coronary syndrome. Obtain ECG, cardiac enzymes, and chest X-ray immediately.",
        confidence_score=0.85,
        evidence_level=EvidenceLevel.A,
        reasoning="Patient presents with classic symptoms of chest pain with radiation, which requires immediate cardiac evaluation to rule out MI.",
        considerations=[
            "Consider patient's cardiac risk factors",
            "Evaluate for other causes of chest pain",
            "Monitor vital signs closely"
        ],
        contraindications=[
            "Avoid sublingual nitroglycerin if systolic BP < 90 mmHg"
        ],
        monitoring=[
            "Continuous cardiac monitoring",
            "Serial troponin levels",
            "Blood pressure monitoring"
        ],
        sources=[
            Source(
                title="2020 AHA/ACC Guidelines for CAD",
                type="guideline",
                evidence_level=EvidenceLevel.A
            )
        ]
    )
    
    # Mock drug interaction if medications present
    drug_interactions = []
    if query.patient_context and query.patient_context.current_medications:
        if len(query.patient_context.current_medications) >= 2:
            drug_interactions = [
                DrugInteraction(
                    drug1=query.patient_context.current_medications[0],
                    drug2=query.patient_context.current_medications[1],
                    severity=SeverityLevel.MODERATE,
                    description="Potential interaction requiring monitoring",
                    management="Monitor for increased effects. Consider dose adjustment.",
                    sources=["DrugBank Database"]
                )
            ]
    
    processing_time = (time.time() - start_time) * 1000
    
    return ClinicalResponse(
        query_id=str(uuid.uuid4()),
        recommendations=[recommendation],
        drug_interactions=drug_interactions,
        differential_diagnoses=["Acute coronary syndrome", "Pulmonary embolism", "Aortic dissection"],
        red_flags=["Severe chest pain", "Hemodynamic instability"],
        next_steps=["Immediate ECG", "Troponin levels", "Cardiology consultation"],
        processing_time_ms=processing_time
    )

@router.post("/query", response_model=ClinicalResponse)
async def process_clinical_query(
    query: ClinicalQuery,
    background_tasks: BackgroundTasks
):
    """
    Process a clinical query and return evidence-based recommendations
    """
    try:
        # Validate query
        if not query.query.strip():
            raise HTTPException(
                status_code=400,
                detail="Query cannot be empty"
            )
        
        # Process the query (using mock service for now)
        response = mock_clinical_service(query)
        
        # Log query for analytics (background task)
        background_tasks.add_task(log_clinical_query, query, response)
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing clinical query: {str(e)}"
        )

@router.get("/specialties")
async def get_supported_specialties():
    """Get list of supported medical specialties"""
    return {
        "specialties": [
            "Internal Medicine",
            "Emergency Medicine",
            "Cardiology",
            "Pulmonology",
            "Infectious Disease",
            "Endocrinology",
            "Neurology",
            "Psychiatry",
            "General Surgery"
        ]
    }

@router.get("/query-types")
async def get_query_types():
    """Get supported query types"""
    return {
        "query_types": [
            {
                "type": "diagnosis",
                "description": "Diagnostic support and differential diagnosis"
            },
            {
                "type": "treatment",
                "description": "Treatment recommendations and protocols"
            },
            {
                "type": "drug_interaction",
                "description": "Drug interaction checking"
            },
            {
                "type": "dosing",
                "description": "Medication dosing guidance"
            },
            {
                "type": "monitoring",
                "description": "Patient monitoring recommendations"
            }
        ]
    }

def log_clinical_query(query: ClinicalQuery, response: ClinicalResponse):
    """Background task to log queries for analytics"""
    # This would typically save to database
    print(f"Logged query {response.query_id} at {datetime.now()}")