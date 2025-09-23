
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
import json
import os
from services.knowledge_processor import KnowledgeProcessor
from services.rag_service import RAGService

router = APIRouter(prefix="/knowledge", tags=["Knowledge Management"])

knowledge_processor = KnowledgeProcessor()
rag_service = RAGService()

@router.post("/expand")
async def expand_knowledge_base(
    specialties: List[str],
    background_tasks: BackgroundTasks
):
    """Expand the medical knowledge base for specified specialties"""
    try:
        # Run knowledge expansion in background
        background_tasks.add_task(
            knowledge_processor.load_expanded_medical_knowledge,
            specialties
        )
        
        return {
            "message": "Knowledge base expansion started",
            "specialties": specialties,
            "status": "processing"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error starting knowledge expansion: {str(e)}"
        )

@router.get("/stats")
async def get_knowledge_base_stats():
    """Get statistics about the current knowledge base"""
    try:
        # Get index stats from Pinecone
        index_stats = rag_service.get_index_stats()
        
        # Get metadata if available
        metadata_path = 'data/metadata/knowledge_base_info.json'
        metadata = {}
        
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
        
        return {
            "index_stats": index_stats,
            "knowledge_metadata": metadata,
            "status": "ready"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving knowledge base stats: {str(e)}"
        )

@router.get("/specialties")
async def get_available_specialties():
    """Get list of available medical specialties"""
    return {
        "available_specialties": [
            "cardiology",
            "endocrinology", 
            "emergency_medicine",
            "infectious_disease",
            "pulmonology",
            "neurology",
            "gastroenterology",
            "nephrology",
            "hematology",
            "oncology"
        ]
    }

@router.post("/search")
async def search_knowledge_base(
    query: str,
    specialty_filter: str = None,
    evidence_level_filter: str = None,
    top_k: int = 10
):
    """Search the medical knowledge base"""
    try:
        # Build filter dictionary
        filter_dict = {}
        
        if specialty_filter:
            filter_dict["specialty"] = specialty_filter
            
        if evidence_level_filter:
            filter_dict["evidence_level"] = evidence_level_filter
        
        # Search using RAG service
        results = rag_service.retrieve_relevant_docs(
            query=query,
            top_k=top_k,
            filter_dict=filter_dict if filter_dict else None
        )
        
        return {
            "query": query,
            "filters": filter_dict,
            "results": results,
            "total_found": len(results)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching knowledge base: {str(e)}"
        )

@router.delete("/clear")
async def clear_knowledge_base():
    """Clear the entire knowledge base (use with caution)"""
    try:
        # This would clear the Pinecone index
        # Implement only if needed for development
        return {
            "message": "Knowledge base clearing not implemented for safety",
            "recommendation": "Create a new index instead"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing knowledge base: {str(e)}"
        )