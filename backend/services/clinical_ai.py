# backend/services/clinical_ai.py
import os
import openai
import logging
from typing import List, Dict, Any, Optional
from services.rag_service import RAGService
from models.schemas import (
    ClinicalQuery, ClinicalResponse, ClinicalRecommendation,
    EvidenceLevel, Source
)
import uuid
import time

logger = logging.getLogger(__name__)

class ClinicalAIService:
    def __init__(self):
        self.openai_client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.rag_service = RAGService()
        self.model = "gpt-4-turbo-preview"
        
    def process_clinical_query(self, query: ClinicalQuery) -> ClinicalResponse:
        """Process a clinical query using RAG and GPT-4"""
        start_time = time.time()
        
        try:
            # Retrieve relevant medical knowledge
            relevant_docs = self.rag_service.retrieve_relevant_docs(
                query.query, 
                top_k=5
            )
            
            # Build context from retrieved documents
            context = self._build_medical_context(relevant_docs, query)
            
            # Generate clinical recommendation using GPT-4
            recommendations = self._generate_recommendations(query, context)
            
            # Check for drug interactions if medications are present
            drug_interactions = []
            if query.patient_context and query.patient_context.current_medications:
                # This would integrate with drug interaction service
                pass
            
            processing_time = (time.time() - start_time) * 1000
            
            return ClinicalResponse(
                query_id=str(uuid.uuid4()),
                recommendations=recommendations,
                drug_interactions=drug_interactions,
                processing_time_ms=processing_time
            )
            
        except Exception as e:
            logger.error(f"Error processing clinical query: {e}")
            raise
    
    def _build_medical_context(self, docs: List[Dict], query: ClinicalQuery) -> str:
        """Build medical context from retrieved documents"""
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
        
        # Add relevant medical literature
        if docs:
            context_parts.append("RELEVANT MEDICAL KNOWLEDGE:")
            for i, doc in enumerate(docs, 1):
                source_info = doc['metadata'].get('source_file', 'Unknown source')
                evidence_level = doc['metadata'].get('evidence_level', 'Unknown')
                context_parts.append(
                    f"\n{i}. Source: {source_info} (Evidence Level: {evidence_level})\n"
                    f"   Content: {doc['content']}\n"
                    f"   Relevance Score: {doc['score']:.3f}"
                )
        
        return "\n\n".join(context_parts)
    
    def _generate_recommendations(self, query: ClinicalQuery, context: str) -> List[ClinicalRecommendation]:
        """Generate clinical recommendations using GPT-4"""
        system_prompt = self._get_clinical_system_prompt()
        
        user_message = f"""
        MEDICAL CONTEXT:
        {context}
        
        CLINICAL QUERY: {query.query}
        
        Please provide evidence-based clinical recommendations in the specified JSON format.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            # Parse the response and create recommendation objects
            recommendations = self._parse_gpt_response(response.choices[0].message.content)
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            # Return fallback recommendation
            return [self._create_fallback_recommendation()]
    
    def _get_clinical_system_prompt(self) -> str:
        """Get the system prompt for clinical decision support"""
        return """
        You are an expert clinical decision support AI assistant. Your role is to provide evidence-based medical recommendations to healthcare professionals.

        IMPORTANT GUIDELINES:
        1. Always prioritize patient safety
        2. Provide evidence-based recommendations with clear reasoning
        3. Include appropriate confidence scores (0.0-1.0)
        4. Mention relevant contraindications and monitoring requirements
        5. Recommend physician consultation for complex cases
        6. Never provide recommendations outside your confidence level

        RESPONSE FORMAT:
        For each recommendation, provide:
        - Primary recommendation (clear, actionable)
        - Clinical reasoning (why this recommendation)
        - Confidence score (0.0-1.0)
        - Evidence level (A, B, or C)
        - Key considerations (important factors)
        - Contraindications (if any)
        - Monitoring requirements (if applicable)

        EVIDENCE LEVELS:
        - A: High-quality evidence (RCTs, meta-analyses, guidelines)
        - B: Moderate-quality evidence (cohort studies, case-control)
        - C: Low-quality evidence (case series, expert opinion)

        Always be conservative and recommend consulting with appropriate specialists when indicated.
        """
    
    def _parse_gpt_response(self, response_text: str) -> List[ClinicalRecommendation]:
        """Parse GPT-4 response into structured recommendations"""
        # This is a simplified parser - you might want to use JSON mode or more sophisticated parsing
        try:
            # For now, create a single recommendation from the response
            recommendation = ClinicalRecommendation(
                recommendation=response_text[:500],  # Truncate for now
                confidence_score=0.8,  # Default confidence
                evidence_level=EvidenceLevel.B,
                reasoning="Based on available medical literature and clinical guidelines.",
                considerations=[
                    "Consider patient-specific factors",
                    "Monitor for adverse effects",
                    "Follow up appropriately"
                ],
                contraindications=[],
                monitoring=[],
                sources=[
                    Source(
                        title="Clinical Guidelines",
                        type="guideline",
                        evidence_level=EvidenceLevel.A
                    )
                ]
            )
            
            return [recommendation]
            
        except Exception as e:
            logger.error(f"Error parsing GPT response: {e}")
            return [self._create_fallback_recommendation()]
    
    def _create_fallback_recommendation(self) -> ClinicalRecommendation:
        """Create a fallback recommendation when AI processing fails"""
        return ClinicalRecommendation(
            recommendation="Unable to process query. Please consult with appropriate medical professional for clinical guidance.",
            confidence_score=0.0,
            evidence_level=EvidenceLevel.C,
            reasoning="System error occurred during processing.",
            considerations=["Seek professional medical consultation"],
            contraindications=[],
            monitoring=[],
            sources=[]
        )