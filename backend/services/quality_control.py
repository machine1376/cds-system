# backend/services/quality_control.py
import logging
from typing import List, Dict, Any
from services.rag_service import RAGService
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class MedicalQualityController:
    """Ensure quality and accuracy of medical knowledge"""
    
    def __init__(self):
        self.rag_service = RAGService()
        
        # Define quality criteria
        self.min_abstract_length = 100
        self.required_mesh_terms = 1
        self.excluded_keywords = [
            "case report",  # Exclude case reports for evidence-based medicine
            "letter to editor",
            "editorial",
            "commentary"
        ]
        
    def validate_medical_content(self, documents: List[Dict]) -> List[Dict]:
        """Validate medical content for quality and relevance"""
        validated_docs = []
        
        for doc in documents:
            if self._meets_quality_criteria(doc):
                validated_docs.append(doc)
            else:
                logger.warning(f"Document failed quality check: {doc.get('title', 'Unknown')}")
        
        logger.info(f"Quality validation: {len(validated_docs)}/{len(documents)} documents passed")
        return validated_docs
    
    def _meets_quality_criteria(self, doc: Dict) -> bool:
        """Check if document meets quality criteria"""
        content = doc.get('content', '')
        metadata = doc.get('metadata', {})
        
        # Check minimum length
        if len(content) < self.min_abstract_length:
            return False
        
        # Check for excluded keywords
        content_lower = content.lower()
        if any(keyword in content_lower for keyword in self.excluded_keywords):
            return False
        
        # Require MeSH terms for PubMed articles
        if metadata.get('document_type') == 'research_paper':
            mesh_terms = metadata.get('mesh_terms', [])
            if len(mesh_terms) < self.required_mesh_terms:
                return False
        
        # Check for medical relevance
        if not self._is_medically_relevant(content, metadata):
            return False
        
        return True
    
    def _is_medically_relevant(self, content: str, metadata: Dict) -> bool:
        """Check if content is medically relevant"""
        medical_keywords = [
            'patient', 'treatment', 'diagnosis', 'therapy', 'clinical',
            'medical', 'disease', 'syndrome', 'medicine', 'healthcare',
            'hospital', 'physician', 'nurse', 'drug', 'medication'
        ]
        
        content_lower = content.lower()
        relevance_score = sum(1 for keyword in medical_keywords if keyword in content_lower)
        
        return relevance_score >= 2  # Require at least 2 medical keywords

class KnowledgeBaseMonitor:
    """Monitor and maintain knowledge base quality"""
    
    def __init__(self):
        self.rag_service = RAGService()
        self.quality_controller = MedicalQualityController()
    
    def generate_quality_report(self) -> Dict[str, Any]:
        """Generate comprehensive quality report"""
        try:
            # Get index statistics
            index_stats = self.rag_service.get_index_stats()
            
            # Sample random documents for quality analysis
            sample_results = self.rag_service.retrieve_relevant_docs(
                "medical treatment", top_k=50
            )
            
            # Analyze document types and evidence levels
            doc_analysis = self._analyze_document_distribution(sample_results)
            
            report = {
                "timestamp": datetime.now().isoformat(),
                "index_statistics": index_stats,
                "document_analysis": doc_analysis,
                "quality_metrics": self._calculate_quality_metrics(sample_results),
                "recommendations": self._generate_recommendations(doc_analysis)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating quality report: {e}")
            return {"error": str(e)}
    
    def _analyze_document_distribution(self, documents: List[Dict]) -> Dict[str, Any]:
        """Analyze distribution of document types and characteristics"""
        doc_types = {}
        evidence_levels = {}
        specialties = {}
        publication_years = {}
        
        for doc in documents:
            metadata = doc.get('metadata', {})
            
            # Document type distribution
            doc_type = metadata.get('document_type', 'unknown')
            doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
            
            # Evidence level distribution
            evidence_level = metadata.get('evidence_level', 'unknown')
            evidence_levels[evidence_level] = evidence_levels.get(evidence_level, 0) + 1
            
            # Specialty distribution
            specialty = metadata.get('specialty', 'unknown')
            specialties[specialty] = specialties.get(specialty, 0) + 1
            
            # Publication year distribution
            year = metadata.get('publication_year', 'unknown')
            if year != 'unknown':
                try:
                    year = int(str(year)[:4])  # Extract year
                    year_range = f"{(year//5)*5}-{(year//5)*5+4}"  # Group by 5-year ranges
                    publication_years[year_range] = publication_years.get(year_range, 0) + 1
                except:
                    publication_years['unknown'] = publication_years.get('unknown', 0) + 1
        
        return {
            "document_types": doc_types,
            "evidence_levels": evidence_levels,
            "specialties": specialties,
            "publication_years": publication_years,
            "total_analyzed": len(documents)
        }
    
    def _calculate_quality_metrics(self, documents: List[Dict]) -> Dict[str, float]:
        """Calculate quality metrics for the knowledge base"""
        if not documents:
            return {}
        
        # Calculate average relevance score
        total_score = sum(doc.get('score', 0) for doc in documents)
        avg_relevance = total_score / len(documents)
        
        # Calculate evidence quality distribution
        evidence_weights = {'A': 3, 'B': 2, 'C': 1}
        evidence_scores = []
        
        for doc in documents:
            evidence_level = doc.get('metadata', {}).get('evidence_level', 'C')
            evidence_scores.append(evidence_weights.get(evidence_level, 1))
        
        avg_evidence_quality = sum(evidence_scores) / len(evidence_scores)
        
        # Calculate content completeness
        complete_docs = sum(1 for doc in documents if len(doc.get('content', '')) > 500)
        completeness_ratio = complete_docs / len(documents)
        
        return {
            "average_relevance_score": round(avg_relevance, 3),
            "average_evidence_quality": round(avg_evidence_quality, 2),
            "content_completeness_ratio": round(completeness_ratio, 2),
            "total_documents_analyzed": len(documents)
        }
    
    def _generate_recommendations(self, doc_analysis: Dict) -> List[str]:
        """Generate recommendations for improving knowledge base"""
        recommendations = []
        
        # Check evidence level distribution
        evidence_levels = doc_analysis.get('evidence_levels', {})
        total_docs = sum(evidence_levels.values())
        
        if total_docs > 0:
            level_a_ratio = evidence_levels.get('A', 0) / total_docs
            if level_a_ratio < 0.3:
                recommendations.append("Consider adding more high-quality evidence (Level A) sources")
        
        # Check specialty coverage
        specialties = doc_analysis.get('specialties', {})
        if len(specialties) < 5:
            recommendations.append("Expand coverage to include more medical specialties")
        
        # Check document type diversity
        doc_types = doc_analysis.get('document_types', {})
        if 'clinical_guideline' not in doc_types or doc_types.get('clinical_guideline', 0) < 10:
            recommendations.append("Add more clinical practice guidelines")
        
        # Check publication recency
        pub_years = doc_analysis.get('publication_years', {})
        recent_years = [k for k in pub_years.keys() if k.startswith('202')]
        if len(recent_years) < 2:
            recommendations.append("Include more recent publications (2020+)")
        
        if not recommendations:
            recommendations.append("Knowledge base appears well-balanced")
        
        return recommendations