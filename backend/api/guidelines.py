
"""
Clinical Guidelines API endpoints for the Clinical Decision Support System
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from data.clinical_guidelines_database import (
    get_guideline_by_id,
    search_clinical_guidelines,
    get_guidelines_for_specialty,
    get_guidelines_for_scenario,
    get_guidelines_database_stats,
    clinical_guidelines_db,
    ClinicalGuideline
)

router = APIRouter(prefix="/guidelines", tags=["Clinical Guidelines"])

# Pydantic models for API responses
class GuidelineResponse(BaseModel):
    id: str
    title: str
    organization: str
    specialty: str
    publication_year: int
    evidence_level: str
    last_updated: str
    summary: str
    url: Optional[str] = None
    doi: Optional[str] = None

class DetailedGuidelineResponse(GuidelineResponse):
    content: str
    key_recommendations: List[Dict[str, Any]]
    contraindications: List[str]
    monitoring_requirements: List[str]
    patient_populations: List[str]
    clinical_scenarios: List[str]
    references: List[str]

class GuidelineSearchRequest(BaseModel):
    query: str
    specialty: Optional[str] = None
    organization: Optional[str] = None
    min_year: Optional[int] = None
    max_results: Optional[int] = 20

def convert_guideline_to_response(guideline: ClinicalGuideline, detailed: bool = False):
    """Convert ClinicalGuideline to API response format"""
    base_response = GuidelineResponse(
        id=guideline.id,
        title=guideline.title,
        organization=guideline.organization,
        specialty=guideline.specialty,
        publication_year=guideline.publication_year,
        evidence_level=guideline.evidence_level,
        last_updated=guideline.last_updated,
        summary=guideline.summary,
        url=guideline.url,
        doi=guideline.doi
    )
    
    if detailed:
        return DetailedGuidelineResponse(
            **base_response.dict(),
            content=guideline.content,
            key_recommendations=guideline.key_recommendations,
            contraindications=guideline.contraindications,
            monitoring_requirements=guideline.monitoring_requirements,
            patient_populations=guideline.patient_populations,
            clinical_scenarios=guideline.clinical_scenarios,
            references=guideline.references
        )
    
    return base_response

@router.get("/", response_model=List[GuidelineResponse])
async def get_all_guidelines(
    specialty: Optional[str] = Query(None, description="Filter by medical specialty"),
    organization: Optional[str] = Query(None, description="Filter by organization"),
    min_year: Optional[int] = Query(None, description="Minimum publication year"),
    limit: int = Query(50, description="Maximum number of results")
):
    """
    Get all clinical guidelines with optional filtering
    """
    try:
        all_guidelines = list(clinical_guidelines_db.guidelines.values())
        
        # Apply filters
        filtered_guidelines = []
        for guideline in all_guidelines:
            if specialty and guideline.specialty != specialty:
                continue
            if organization and organization.lower() not in guideline.organization.lower():
                continue
            if min_year and guideline.publication_year < min_year:
                continue
            filtered_guidelines.append(guideline)
        
        # Sort by publication year (newest first) and limit results
        filtered_guidelines.sort(key=lambda g: g.publication_year, reverse=True)
        limited_guidelines = filtered_guidelines[:limit]
        
        return [convert_guideline_to_response(g) for g in limited_guidelines]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving guidelines: {str(e)}"
        )

@router.get("/{guideline_id}", response_model=DetailedGuidelineResponse)
async def get_guideline(guideline_id: str):
    """
    Get detailed information for a specific guideline
    """
    try:
        guideline = get_guideline_by_id(guideline_id)
        
        if not guideline:
            raise HTTPException(
                status_code=404,
                detail=f"Guideline with ID '{guideline_id}' not found"
            )
        
        return convert_guideline_to_response(guideline, detailed=True)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving guideline: {str(e)}"
        )

@router.post("/search", response_model=List[GuidelineResponse])
async def search_guidelines(request: GuidelineSearchRequest):
    """
    Search clinical guidelines using text query and filters
    """
    try:
        results = search_clinical_guidelines(
            query=request.query,
            specialty=request.specialty,
            organization=request.organization,
            min_year=request.min_year
        )
        
        # Limit results
        max_results = request.max_results or 20
        limited_results = results[:max_results]
        
        return [convert_guideline_to_response(g) for g in limited_results]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching guidelines: {str(e)}"
        )

@router.get("/specialty/{specialty}", response_model=List[GuidelineResponse])
async def get_guidelines_by_specialty(specialty: str):
    """
    Get all guidelines for a specific medical specialty
    """
    try:
        guidelines = get_guidelines_for_specialty(specialty)
        
        if not guidelines:
            raise HTTPException(
                status_code=404,
                detail=f"No guidelines found for specialty '{specialty}'"
            )
        
        return [convert_guideline_to_response(g) for g in guidelines]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving guidelines for specialty: {str(e)}"
        )

@router.get("/scenario/{scenario}", response_model=List[GuidelineResponse])
async def get_guidelines_by_scenario(scenario: str):
    """
    Get guidelines relevant to a specific clinical scenario
    """
    try:
        guidelines = get_guidelines_for_scenario(scenario)
        
        return [convert_guideline_to_response(g) for g in guidelines]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving guidelines for scenario: {str(e)}"
        )

@router.get("/stats/database")
async def get_database_statistics():
    """
    Get comprehensive statistics about the guidelines database
    """
    try:
        stats = get_guidelines_database_stats()
        
        # Add additional metadata
        enhanced_stats = {
            **stats,
            "available_specialties": list(stats["specialties"].keys()),
            "available_organizations": list(stats["organizations"].keys()),
            "coverage_summary": {
                "most_covered_specialty": max(stats["specialties"].items(), key=lambda x: x[1])[0],
                "newest_guideline_year": stats["latest_year"],
                "oldest_guideline_year": stats["oldest_year"],
                "year_range": stats["latest_year"] - stats["oldest_year"] if stats["latest_year"] and stats["oldest_year"] else 0
            }
        }
        
        return enhanced_stats
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving database statistics: {str(e)}"
        )

@router.get("/recommendations/{guideline_id}")
async def get_guideline_recommendations(guideline_id: str):
    """
    Get key recommendations from a specific guideline
    """
    try:
        guideline = get_guideline_by_id(guideline_id)
        
        if not guideline:
            raise HTTPException(
                status_code=404,
                detail=f"Guideline with ID '{guideline_id}' not found"
            )
        
        return {
            "guideline_id": guideline_id,
            "guideline_title": guideline.title,
            "organization": guideline.organization,
            "publication_year": guideline.publication_year,
            "evidence_level": guideline.evidence_level,
            "key_recommendations": guideline.key_recommendations,
            "total_recommendations": len(guideline.key_recommendations)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving recommendations: {str(e)}"
        )

@router.get("/clinical-alerts/{specialty}")
async def get_specialty_clinical_alerts(specialty: str):
    """
    Get important clinical alerts and contraindications for a specialty
    """
    try:
        guidelines = get_guidelines_for_specialty(specialty)
        
        if not guidelines:
            raise HTTPException(
                status_code=404,
                detail=f"No guidelines found for specialty '{specialty}'"
            )
        
        alerts = []
        contraindications = []
        monitoring_requirements = []
        
        for guideline in guidelines:
            # Collect contraindications
            for contraindication in guideline.contraindications:
                contraindications.append({
                    "contraindication": contraindication,
                    "source_guideline": guideline.title,
                    "organization": guideline.organization
                })
            
            # Collect monitoring requirements
            for monitoring in guideline.monitoring_requirements:
                monitoring_requirements.append({
                    "monitoring": monitoring,
                    "source_guideline": guideline.title,
                    "organization": guideline.organization
                })
            
            # Create alerts for Class I recommendations
            for rec in guideline.key_recommendations:
                if rec.get("class") == "I" or rec.get("class") == "Strong":
                    alerts.append({
                        "alert_type": "STRONG_RECOMMENDATION",
                        "recommendation": rec["recommendation"],
                        "evidence_level": rec.get("level_of_evidence", "Unknown"),
                        "source_guideline": guideline.title
                    })
        
        return {
            "specialty": specialty,
            "total_guidelines": len(guidelines),
            "clinical_alerts": alerts[:10],  # Limit to top 10
            "contraindications": contraindications[:10],
            "monitoring_requirements": monitoring_requirements[:10],
            "summary": f"Found {len(alerts)} strong recommendations, {len(contraindications)} contraindications, {len(monitoring_requirements)} monitoring requirements"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving clinical alerts: {str(e)}"
        )

@router.post("/compare")
async def compare_guidelines(guideline_ids: List[str]):
    """
    Compare recommendations across multiple guidelines
    """
    try:
        if len(guideline_ids) < 2:
            raise HTTPException(
                status_code=400,
                detail="At least 2 guideline IDs required for comparison"
            )
        
        if len(guideline_ids) > 5:
            raise HTTPException(
                status_code=400,
                detail="Maximum 5 guidelines can be compared at once"
            )
        
        guidelines = []
        for gid in guideline_ids:
            guideline = get_guideline_by_id(gid)
            if not guideline:
                raise HTTPException(
                    status_code=404,
                    detail=f"Guideline with ID '{gid}' not found"
                )
            guidelines.append(guideline)
        
        comparison = {
            "compared_guidelines": [
                {
                    "id": g.id,
                    "title": g.title,
                    "organization": g.organization,
                    "year": g.publication_year,
                    "evidence_level": g.evidence_level
                } for g in guidelines
            ],
            "recommendation_comparison": [],
            "contraindication_overlap": [],
            "monitoring_overlap": []
        }
        
        # Compare key recommendations
        for i, guideline in enumerate(guidelines):
            for rec in guideline.key_recommendations:
                comparison["recommendation_comparison"].append({
                    "guideline_index": i,
                    "guideline_title": guideline.title,
                    "recommendation": rec["recommendation"],
                    "class": rec.get("class", "Unknown"),
                    "evidence_level": rec.get("level_of_evidence", "Unknown")
                })
        
        # Find overlapping contraindications
        all_contraindications = []
        for guideline in guidelines:
            all_contraindications.extend(guideline.contraindications)
        
        contraindication_counts = {}
        for contraindication in all_contraindications:
            contraindication_counts[contraindication] = contraindication_counts.get(contraindication, 0) + 1
        
        for contraindication, count in contraindication_counts.items():
            if count > 1:
                comparison["contraindication_overlap"].append({
                    "contraindication": contraindication,
                    "appears_in_guidelines": count,
                    "consistency": "High" if count == len(guidelines) else "Moderate"
                })
        
        return comparison
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error comparing guidelines: {str(e)}"
        )

# Update main.py to include guidelines router
"""
Add to backend/main.py:

from api import clinical, drugs, knowledge, guidelines

app.include_router(guidelines.router)
"""

# Integration with Clinical AI Service
"""
backend/services/clinical_ai_enhanced.py
Enhanced Clinical AI Service that uses guidelines database
"""

from typing import List, Dict, Any
from services.clinical_ai import ClinicalAIService
from data.clinical_guidelines_database import search_clinical_guidelines, get_guidelines_for_scenario

class EnhancedClinicalAIService(ClinicalAIService):
    """Enhanced Clinical AI Service with guidelines integration"""
    
    def __init__(self):
        super().__init__()
        
    def _build_medical_context(self, docs: List[Dict], query, include_guidelines: bool = True) -> str:
        """Enhanced context building with clinical guidelines"""
        context_parts = []
        
        # Add patient context if available
        if query.patient_context:
            patient_info = []
            if query.patient_context.age:
                patient_info.append(f"Age: {query.patient_context.age}")
            if query.patient_context.gender:
                patient_info.append(f"Gender: {query.patient_context.gender}")
            if query.patient_context.medical_conditions:
                patient_info.append(f"Conditions: {', '.join(query.patient_context.medical_conditions)}")
            if query.patient_context.current_medications:
                patient_info.append(f"Medications: {', '.join(query.patient_context.current_medications)}")
            
            if patient_info:
                context_parts.append(f"PATIENT CONTEXT: {'; '.join(patient_info)}")
        
        # Add relevant medical literature from RAG
        if docs:
            context_parts.append("RELEVANT MEDICAL LITERATURE:")
            for i, doc in enumerate(docs, 1):
                source_info = doc['metadata'].get('source_file', 'Unknown source')
                evidence_level = doc['metadata'].get('evidence_level', 'Unknown')
                context_parts.append(
                    f"\n{i}. Source: {source_info} (Evidence Level: {evidence_level})\n"
                    f"   Content: {doc['content']}\n"
                    f"   Relevance Score: {doc['score']:.3f}"
                )
        
        # Add relevant clinical guidelines
        if include_guidelines:
            relevant_guidelines = search_clinical_guidelines(query.query, max_results=3)
            
            if relevant_guidelines:
                context_parts.append("RELEVANT CLINICAL GUIDELINES:")
                for i, guideline in enumerate(relevant_guidelines, 1):
                    context_parts.append(
                        f"\n{i}. {guideline.title} ({guideline.organization}, {guideline.publication_year})\n"
                        f"   Evidence Level: {guideline.evidence_level}\n"
                        f"   Summary: {guideline.summary[:300]}...\n"
                        f"   Key Recommendations: {len(guideline.key_recommendations)} recommendations available"
                    )
        
        return "\n\n".join(context_parts)
    
    def get_scenario_specific_guidelines(self, clinical_scenario: str) -> List[Dict[str, Any]]:
        """Get guidelines specific to a clinical scenario"""
        guidelines = get_guidelines_for_scenario(clinical_scenario)
        
        return [
            {
                "title": g.title,
                "organization": g.organization,
                "year": g.publication_year,
                "evidence_level": g.evidence_level,
                "key_recommendations": g.key_recommendations[:3],  # Top 3 recommendations
                "contraindications": g.contraindications,
                "monitoring": g.monitoring_requirements
            }
            for g in guidelines[:2]  # Limit to top 2 guidelines
        ]

# Test the guidelines integration
if __name__ == "__main__":
    print("Testing Clinical Guidelines API Integration...")
    
    # Test search
    search_results = search_clinical_guidelines("diabetes management")
    print(f"Found {len(search_results)} diabetes guidelines")
    
    # Test specialty filter
    cardiology_guidelines = get_guidelines_for_specialty("cardiology")
    print(f"Found {len(cardiology_guidelines)} cardiology guidelines")
    
    # Test scenario matching
    chest_pain_guidelines = get_guidelines_for_scenario("chest pain")
    print(f"Found {len(chest_pain_guidelines)} guidelines for chest pain")
    
    # Test database stats
    stats = get_guidelines_database_stats()
    print(f"Database contains {stats['total_guidelines']} guidelines covering {len(stats['specialties'])} specialties")