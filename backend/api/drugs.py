from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from models.schemas import DrugInteraction, SeverityLevel
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from data.drug_interactions_database import (
    check_drug_interaction, 
    check_drug_list_interactions, 
    get_drug_summary,
    drug_interaction_db
)

router = APIRouter(prefix="/drugs", tags=["Drug Information"])

@router.post("/interactions", response_model=List[DrugInteraction])
async def check_drug_interactions(medications: List[str]):
    """
    Check for drug-drug interactions in a medication list
    Returns interactions sorted by severity (most severe first)
    """
    if not medications or len(medications) < 2:
        return []
    
    try:
        interactions_data = check_drug_list_interactions(medications)
        
        # Convert to DrugInteraction model format
        interactions = []
        for interaction_data in interactions_data:
            interaction = DrugInteraction(
                drug1=interaction_data["drug1"],
                drug2=interaction_data["drug2"],
                severity=interaction_data["severity"],
                description=interaction_data["description"],
                mechanism=interaction_data.get("mechanism"),
                management=interaction_data["management"],
                sources=interaction_data.get("sources", [])
            )
            interactions.append(interaction)
        
        return interactions
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error checking drug interactions: {str(e)}"
        )

@router.get("/interactions/{drug_name}")
async def get_drug_interaction_profile(drug_name: str):
    """
    Get comprehensive interaction profile for a specific drug
    """
    try:
        summary = get_drug_summary(drug_name)
        
        if summary["total_interactions"] == 0:
            return {
                "drug": drug_name,
                "message": "No known interactions found in database",
                "total_interactions": 0
            }
        
        return summary
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving drug profile: {str(e)}"
        )

@router.post("/check-pair")
async def check_drug_pair(drug1: str, drug2: str):
    """
    Check interaction between two specific drugs
    """
    try:
        interaction_data = check_drug_interaction(drug1, drug2)
        
        if not interaction_data:
            return {
                "drug1": drug1,
                "drug2": drug2,
                "interaction_found": False,
                "message": "No interaction found between these drugs"
            }
        
        return {
            "drug1": drug1,
            "drug2": drug2,
            "interaction_found": True,
            "severity": interaction_data["severity"],
            "description": interaction_data["description"],
            "mechanism": interaction_data.get("mechanism"),
            "management": interaction_data["management"],
            "onset": interaction_data.get("onset"),
            "documentation": interaction_data.get("documentation"),
            "sources": interaction_data.get("sources", [])
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error checking drug pair: {str(e)}"
        )

@router.get("/search")
async def search_drugs(
    query: str = Query(..., description="Drug name to search"),
    exact_match: bool = Query(False, description="Require exact match")
):
    """
    Search for drugs in the database
    """
    try:
        # Get all available drugs from the database
        all_drugs = set()
        
        # Extract drugs from interaction pairs
        for (drug1, drug2) in drug_interaction_db.interactions.keys():
            all_drugs.add(drug1)
            all_drugs.add(drug2)
        
        # Add aliases
        for standard_name, aliases in drug_interaction_db.drug_aliases.items():
            all_drugs.add(standard_name)
            all_drugs.extend(aliases)
        
        query_lower = query.lower()
        
        if exact_match:
            matches = [drug for drug in all_drugs if drug.lower() == query_lower]
        else:
            matches = [drug for drug in all_drugs if query_lower in drug.lower()]
        
        # Limit results and sort
        matches = sorted(list(set(matches)))[:20]
        
        return {
            "query": query,
            "exact_match": exact_match,
            "matches": matches,
            "total_found": len(matches)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching drugs: {str(e)}"
        )

@router.get("/severity-stats")
async def get_severity_statistics():
    """
    Get statistics about interaction severities in the database
    """
    try:
        severity_counts = {}
        total_interactions = len(drug_interaction_db.interactions)
        
        for interaction_data in drug_interaction_db.interactions.values():
            severity = interaction_data["severity"]
            severity_counts[severity.value] = severity_counts.get(severity.value, 0) + 1
        
        # Calculate percentages
        severity_percentages = {
            severity: round((count / total_interactions) * 100, 1)
            for severity, count in severity_counts.items()
        }
        
        return {
            "total_interactions": total_interactions,
            "severity_counts": severity_counts,
            "severity_percentages": severity_percentages,
            "severity_descriptions": {
                "contraindicated": "Avoid combination - serious risk",
                "major": "Significant interaction - close monitoring required",
                "moderate": "Moderate interaction - monitor for effects", 
                "minor": "Minor interaction - minimal clinical significance"
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting statistics: {str(e)}"
        )

@router.get("/clinical-alerts/{drug_name}")
async def get_clinical_alerts(drug_name: str):
    """
    Get clinical alerts and warnings for a specific drug
    """
    try:
        summary = get_drug_summary(drug_name)
        
        if summary["total_interactions"] == 0:
            return {
                "drug": drug_name,
                "alerts": [],
                "message": "No clinical alerts found"
            }
        
        alerts = []
        
        # Create alerts for contraindicated interactions
        contraindicated = summary["by_severity"].get(SeverityLevel.CONTRAINDICATED, [])
        for interaction in contraindicated:
            alerts.append({
                "level": "CRITICAL",
                "message": f"CONTRAINDICATED with {interaction['interacting_drug'].upper()}",
                "description": interaction["description"],
                "action_required": "Do not use together"
            })
        
        # Create alerts for major interactions
        major = summary["by_severity"].get(SeverityLevel.MAJOR, [])
        for interaction in major:
            alerts.append({
                "level": "WARNING",
                "message": f"MAJOR interaction with {interaction['interacting_drug']}",
                "description": interaction["description"],
                "action_required": "Close monitoring required"
            })
        
        return {
            "drug": drug_name,
            "total_alerts": len(alerts),
            "alerts": alerts,
            "summary": f"{len(contraindicated)} contraindicated, {len(major)} major interactions"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting clinical alerts: {str(e)}"
        )

@router.post("/patient-specific-check")
async def patient_specific_interaction_check(
    medications: List[str],
    patient_age: Optional[int] = None,
    kidney_function: Optional[str] = None,  # "normal", "mild", "moderate", "severe"
    liver_function: Optional[str] = None    # "normal", "mild", "moderate", "severe"
):
    """
    Check drug interactions with patient-specific considerations
    """
    try:
        # Get standard interactions
        interactions = check_drug_list_interactions(medications)
        
        # Enhance with patient-specific warnings
        enhanced_interactions = []
        
        for interaction_data in interactions:
            enhanced = {**interaction_data}
            
            # Add age-specific warnings
            if patient_age:
                if patient_age >= 65:
                    enhanced["geriatric_considerations"] = "Elderly patients may be at higher risk for adverse effects"
                elif patient_age < 18:
                    enhanced["pediatric_considerations"] = "Pediatric dosing and monitoring may differ"
            
            # Add organ function warnings
            if kidney_function and kidney_function != "normal":
                enhanced["renal_considerations"] = f"Use caution with {kidney_function} kidney function"
            
            if liver_function and liver_function != "normal":
                enhanced["hepatic_considerations"] = f"Use caution with {liver_function} liver function"
            
            enhanced_interactions.append(enhanced)
        
        return {
            "medications": medications,
            "patient_factors": {
                "age": patient_age,
                "kidney_function": kidney_function,
                "liver_function": liver_function
            },
            "interactions_found": len(enhanced_interactions),
            "interactions": enhanced_interactions
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in patient-specific check: {str(e)}"
        )

# Additional endpoint for testing the database
@router.get("/database-info")
async def get_database_info():
    """
    Get information about the drug interaction database
    """
    try:
        total_interactions = len(drug_interaction_db.interactions)
        unique_drugs = set()
        
        for (drug1, drug2) in drug_interaction_db.interactions.keys():
            unique_drugs.add(drug1)
            unique_drugs.add(drug2)
        
        total_aliases = sum(len(aliases) for aliases in drug_interaction_db.drug_aliases.values())
        
        return {
            "database_version": "1.0",
            "total_interactions": total_interactions,
            "unique_drugs": len(unique_drugs),
            "total_aliases": total_aliases
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting database info: {str(e)}"
        )