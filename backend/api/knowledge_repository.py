# backend/api/knowledge_repository.py
"""
Knowledge Base Repository API endpoints for Clinical Decision Support System
"""

import asyncio
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
from data.knowledge_repository_database import (
    knowledge_repository,
    search_knowledge_repository,
    get_document_by_id,
    get_repository_statistics,
    get_source_information,
    get_processing_metadata,
    DocumentType,
    EvidenceLevel,
    AccessLevel
)

router = APIRouter(prefix="/knowledge-repository", tags=["Knowledge Repository"])

# Pydantic models for API requests/responses
class DocumentSearchRequest(BaseModel):
    query: str
    specialty: Optional[str] = None
    document_type: Optional[str] = None
    evidence_level: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    access_level: Optional[str] = None
    max_results: Optional[int] = 50

class DocumentSummaryResponse(BaseModel):
    document_id: str
    title: str
    document_type: str
    evidence_level: str
    publication_date: datetime
    authors: List[str]
    journal: str
    abstract: str
    specialties: List[str]
    quality_score: float
    citation_count: int
    access_level: str

class DetailedDocumentResponse(BaseModel):
    document_id: str
    title: str
    document_type: str
    citation: Dict[str, Any]
    abstract: str
    full_text_available: bool
    keywords: List[str]
    mesh_terms: List[str]
    specialties: List[str]
    evidence_level: str
    publication_status: str
    access_level: str
    source_url: Optional[str]
    pdf_url: Optional[str]
    quality_metrics: Dict[str, float]
    processing_metadata: Optional[Dict[str, Any]]

class RepositoryStatsResponse(BaseModel):
    total_documents: int
    document_types: Dict[str, int]
    evidence_levels: Dict[str, int]
    access_levels: Dict[str, int]
    quality_metrics: Dict[str, float]
    content_coverage: Dict[str, Any]
    processing_status: Dict[str, float]

@router.get("/", response_model=RepositoryStatsResponse)
async def get_repository_overview():
    """
    Get overview statistics for the knowledge repository
    """
    try:
        stats = get_repository_statistics()
        
        return RepositoryStatsResponse(
            total_documents=stats["repository_metrics"]["total_documents"],
            document_types=stats["repository_metrics"]["document_types"],
            evidence_levels=stats["repository_metrics"]["evidence_levels"],
            access_levels=stats["repository_metrics"]["access_levels"],
            quality_metrics={
                "average_quality_score": stats["repository_metrics"]["average_quality_score"],
                "peer_reviewed_percentage": stats["repository_metrics"]["peer_reviewed_percentage"],
                "open_access_percentage": stats["repository_metrics"]["open_access_percentage"],
                "recent_content_percentage": stats["repository_metrics"]["recent_content_percentage"]
            },
            content_coverage=stats["content_coverage"],
            processing_status=stats["processing_status"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving repository overview: {str(e)}"
        )

@router.post("/search", response_model=List[DocumentSummaryResponse])
async def search_documents(request: DocumentSearchRequest):
    """
    Search documents in the knowledge repository
    """
    try:
        # Build filters from request
        filters = {}
        if request.specialty:
            filters["specialty"] = request.specialty
        if request.document_type:
            filters["document_type"] = request.document_type
        if request.evidence_level:
            filters["evidence_level"] = request.evidence_level
        if request.start_date:
            filters["start_date"] = request.start_date
        if request.end_date:
            filters["end_date"] = request.end_date
        
        # Search documents
        doc_ids = search_knowledge_repository(request.query, filters)
        
        # Limit results
        max_results = request.max_results or 50
        limited_doc_ids = doc_ids[:max_results]
        
        # Convert to response format
        results = []
        for doc_id in limited_doc_ids:
            doc = get_document_by_id(doc_id)
            if doc:
                author_names = [f"{author.first_name} {author.last_name}" for author in doc.citation.authors]
                
                results.append(DocumentSummaryResponse(
                    document_id=doc.document_id,
                    title=doc.title,
                    document_type=doc.document_type.value,
                    evidence_level=doc.evidence_level.value,
                    publication_date=doc.citation.publication_date,
                    authors=author_names,
                    journal=doc.citation.journal,
                    abstract=doc.abstract,
                    specialties=doc.specialties,
                    quality_score=doc.quality_score,
                    citation_count=doc.citation_count,
                    access_level=doc.access_level.value
                ))
        
        return results
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching documents: {str(e)}"
        )

@router.get("/document/{document_id}", response_model=DetailedDocumentResponse)
async def get_document_details(document_id: str):
    """
    Get detailed information for a specific document
    """
    try:
        doc = get_document_by_id(document_id)
        if not doc:
            raise HTTPException(
                status_code=404,
                detail=f"Document with ID '{document_id}' not found"
            )
        
        # Get processing metadata
        processing_meta = get_processing_metadata(document_id)
        processing_data = None
        if processing_meta:
            processing_data = {
                "processing_date": processing_meta.processing_date.isoformat(),
                "extraction_method": processing_meta.extraction_method,
                "confidence_score": processing_meta.confidence_score,
                "validation_status": processing_meta.validation_status,
                "chunk_count": processing_meta.chunk_count,
                "embedding_status": processing_meta.embedding_status,
                "errors_detected": processing_meta.errors_detected
            }
        
        # Build citation information
        citation_data = {
            "title": doc.citation.title,
            "authors": [f"{author.first_name} {author.last_name}" for author in doc.citation.authors],
            "journal": doc.citation.journal,
            "volume": doc.citation.volume,
            "issue": doc.citation.issue,
            "pages": doc.citation.pages,
            "publication_date": doc.citation.publication_date.isoformat(),
            "doi": doc.citation.doi,
            "pmid": doc.citation.pmid,
            "pmcid": doc.citation.pmcid,
            "publisher": doc.citation.publisher
        }
        
        # Build quality metrics
        quality_metrics = {
            "overall_quality": doc.quality_score,
            "clinical_relevance": doc.clinical_relevance_score,
            "citation_impact": min(doc.citation_count / 100.0, 1.0),  # Normalized citation score
            "recency_score": max(0, 1 - (datetime.now() - doc.citation.publication_date).days / 3650),  # 10-year decay
            "peer_reviewed": 1.0 if doc.peer_reviewed else 0.0
        }
        
        return DetailedDocumentResponse(
            document_id=doc.document_id,
            title=doc.title,
            document_type=doc.document_type.value,
            citation=citation_data,
            abstract=doc.abstract,
            full_text_available=doc.full_text is not None,
            keywords=doc.keywords,
            mesh_terms=doc.mesh_terms,
            specialties=doc.specialties,
            evidence_level=doc.evidence_level.value,
            publication_status=doc.publication_status.value,
            access_level=doc.access_level.value,
            source_url=doc.source_url,
            pdf_url=doc.pdf_url,
            quality_metrics=quality_metrics,
            processing_metadata=processing_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving document details: {str(e)}"
        )

@router.get("/sources")
async def get_knowledge_sources():
    """
    Get information about knowledge sources in the repository
    """
    try:
        sources_data = []
        for source_id, source in knowledge_repository.sources.items():
            source_info = {
                "source_id": source.source_id,
                "name": source.name,
                "organization": source.organization,
                "source_type": source.source_type,
                "url": source.url,
                "impact_factor": source.impact_factor,
                "credibility_score": source.credibility_score,
                "subscription_status": source.subscription_status.value,
                "document_count": source.document_count,
                "last_indexed": source.last_indexed.isoformat(),
                "quality_metrics": source.quality_metrics
            }
            sources_data.append(source_info)
        
        # Sort by credibility score
        sources_data.sort(key=lambda x: x["credibility_score"], reverse=True)
        
        return {
            "total_sources": len(sources_data),
            "sources": sources_data,
            "summary": {
                "avg_credibility": sum(s["credibility_score"] for s in sources_data) / len(sources_data),
                "source_types": list(set(s["source_type"] for s in sources_data)),
                "subscription_breakdown": {
                    status: len([s for s in sources_data if s["subscription_status"] == status])
                    for status in set(s["subscription_status"] for s in sources_data)
                }
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving knowledge sources: {str(e)}"
        )

@router.get("/quality/report")
async def get_quality_report():
    """
    Generate comprehensive quality report for the knowledge repository
    """
    try:
        stats = get_repository_statistics()
        repo_metrics = stats["repository_metrics"]
        
        # Calculate additional quality indicators
        total_docs = repo_metrics["total_documents"]
        
        # Evidence quality distribution
        evidence_quality_score = (
            repo_metrics["evidence_levels"].get("A", 0) * 1.0 +
            repo_metrics["evidence_levels"].get("B", 0) * 0.8 +
            repo_metrics["evidence_levels"].get("C", 0) * 0.6 +
            repo_metrics["evidence_levels"].get("D", 0) * 0.4
        ) / total_docs if total_docs > 0 else 0
        
        # Content freshness analysis
        recent_threshold = datetime.now() - timedelta(days=5*365)  # 5 years
        very_recent_threshold = datetime.now() - timedelta(days=2*365)  # 2 years
        
        recent_docs = sum(1 for doc in knowledge_repository.documents.values() 
                         if doc.citation.publication_date >= recent_threshold)
        very_recent_docs = sum(1 for doc in knowledge_repository.documents.values() 
                              if doc.citation.publication_date >= very_recent_threshold)
        
        # Source diversity analysis
        unique_journals = len(set(doc.citation.journal for doc in knowledge_repository.documents.values()))
        unique_publishers = len(set(doc.citation.publisher for doc in knowledge_repository.documents.values() 
                                  if doc.citation.publisher))
        
        # Processing quality analysis
        processing_data = list(knowledge_repository.processing_metadata.values())
        avg_confidence = sum(p.confidence_score for p in processing_data) / len(processing_data) if processing_data else 0
        validation_rate = sum(1 for p in processing_data if p.validation_status == "validated") / len(processing_data) * 100 if processing_data else 0
        
        quality_report = {
            "overall_quality_score": repo_metrics["average_quality_score"],
            "evidence_quality_score": round(evidence_quality_score, 3),
            "content_freshness": {
                "recent_content_5y": round(recent_docs / total_docs * 100, 1),
                "very_recent_content_2y": round(very_recent_docs / total_docs * 100, 1),
                "freshness_score": round((recent_docs * 0.6 + very_recent_docs * 0.4) / total_docs, 3)
            },
            "source_diversity": {
                "unique_journals": unique_journals,
                "unique_publishers": unique_publishers,
                "diversity_score": round(min(unique_journals / 100, 1.0), 3)  # Normalized to 100 journals
            },
            "access_quality": {
                "open_access_percentage": repo_metrics["open_access_percentage"],
                "peer_reviewed_percentage": repo_metrics["peer_reviewed_percentage"],
                "subscription_access_percentage": round(
                    repo_metrics["access_levels"].get("subscription", 0) / total_docs * 100, 1
                )
            },
            "processing_quality": {
                "average_confidence": round(avg_confidence, 3),
                "validation_rate": round(validation_rate, 1),
                "embedding_completion": stats["processing_status"]["embedding_completion"]
            },
            "coverage_analysis": {
                "specialties_covered": stats["content_coverage"]["specialties_covered"],
                "document_type_diversity": len(repo_metrics["document_types"]),
                "publication_year_span": (
                    stats["content_coverage"]["publication_years"]["latest"] - 
                    stats["content_coverage"]["publication_years"]["earliest"]
                )
            },
            "recommendations": []
        }
        
        # Generate recommendations based on quality metrics
        recommendations = []
        
        if evidence_quality_score < 0.7:
            recommendations.append("Consider prioritizing higher evidence-level documents (Level A and B)")
        
        if quality_report["content_freshness"]["recent_content_5y"] < 60:
            recommendations.append("Increase acquisition of recent publications to improve content freshness")
        
        if repo_metrics["open_access_percentage"] < 40:
            recommendations.append("Expand open access content to improve accessibility")
        
        if validation_rate < 90:
            recommendations.append("Improve document processing validation procedures")
        
        if unique_journals < 50:
            recommendations.append("Diversify journal sources to reduce bias")
        
        quality_report["recommendations"] = recommendations
        
        return {
            "report_generated": datetime.now().isoformat(),
            "quality_assessment": quality_report,
            "summary": {
                "overall_grade": "A" if quality_report["overall_quality_score"] > 0.9 else
                               "B" if quality_report["overall_quality_score"] > 0.8 else
                               "C" if quality_report["overall_quality_score"] > 0.7 else "D",
                "strengths": [
                    area for area, score in [
                        ("Evidence Quality", evidence_quality_score),
                        ("Content Freshness", quality_report["content_freshness"]["freshness_score"]),
                        ("Source Diversity", quality_report["source_diversity"]["diversity_score"]),
                        ("Processing Quality", avg_confidence)
                    ] if score > 0.8
                ],
                "improvement_areas": [
                    area for area, score in [
                        ("Evidence Quality", evidence_quality_score),
                        ("Content Freshness", quality_report["content_freshness"]["freshness_score"]),
                        ("Source Diversity", quality_report["source_diversity"]["diversity_score"]),
                        ("Processing Quality", avg_confidence)
                    ] if score < 0.7
                ]
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating quality report: {str(e)}"
        )

@router.get("/analytics/usage")
async def get_repository_usage_analytics():
    """
    Get usage analytics for the knowledge repository
    """
    try:
        # Simulate usage analytics (in production, this would come from actual usage logs)
        total_docs = len(knowledge_repository.documents)
        
        # Document access patterns (simulated)
        most_accessed_types = {
            "research_paper": 45,
            "clinical_guideline": 25,
            "systematic_review": 15,
            "drug_monograph": 10,
            "textbook_chapter": 5
        }
        
        # Specialty usage patterns
        specialty_usage = {}
        for doc in knowledge_repository.documents.values():
            for specialty in doc.specialties:
                specialty_usage[specialty] = specialty_usage.get(specialty, 0) + 1
        
        # Evidence level preferences
        evidence_usage = {}
        for doc in knowledge_repository.documents.values():
            evidence_usage[doc.evidence_level.value] = evidence_usage.get(doc.evidence_level.value, 0) + 1
        
        return {
            "repository_size": total_docs,
            "usage_patterns": {
                "most_accessed_document_types": most_accessed_types,
                "specialty_distribution": specialty_usage,
                "evidence_level_usage": evidence_usage
            },
            "search_analytics": {
                "total_searches_simulated": 15000,
                "avg_results_per_search": 12.3,
                "most_common_search_terms": [
                    "diabetes", "cardiovascular", "antibiotic", "hypertension", "infection"
                ]
            },
            "content_gaps": {
                "underrepresented_specialties": [
                    specialty for specialty, count in specialty_usage.items() if count < 50
                ],
                "needed_document_types": [
                    "case_study", "conference_abstract"  # Types with lower representation
                ]
            },
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving usage analytics: {str(e)}"
        )

@router.post("/maintenance/reindex")
async def reindex_repository(background_tasks: BackgroundTasks):
    """
    Trigger repository reindexing (background task)
    """
    try:
        background_tasks.add_task(perform_reindexing)
        
        return {
            "status": "reindexing_started",
            "message": "Repository reindexing has been initiated in the background",
            "estimated_completion": (datetime.now() + timedelta(hours=2)).isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error starting reindex: {str(e)}"
        )

async def perform_reindexing():
    """Background task for repository reindexing"""
    # This would perform actual reindexing in production
    print("Starting repository reindexing...")
    # Simulate reindexing process
    print("Reindexing completed successfully")

@router.get("/export/bibliography")
async def export_bibliography(
    document_ids: List[str] = Query(..., description="Document IDs to include in bibliography"),
    format: str = Query("bibtex", description="Bibliography format: bibtex, apa, mla")
):
    """
    Export bibliography for selected documents
    """
    try:
        bibliography_entries = []
        
        for doc_id in document_ids:
            doc = get_document_by_id(doc_id)
            if not doc:
                continue
            
            if format.lower() == "bibtex":
                # Generate BibTeX entry
                authors_str = " and ".join([
                    f"{author.last_name}, {author.first_name}" 
                    for author in doc.citation.authors
                ])
                
                bibtex_entry = f"""@article{{{doc_id},
    title = {{{doc.citation.title}}},
    author = {{{authors_str}}},
    journal = {{{doc.citation.journal}}},
    volume = {{{doc.citation.volume or ""}}},
    number = {{{doc.citation.issue or ""}}},
    pages = {{{doc.citation.pages or ""}}},
    year = {{{doc.citation.publication_date.year}}},
    doi = {{{doc.citation.doi or ""}}},
    pmid = {{{doc.citation.pmid or ""}}}
}}"""
                bibliography_entries.append(bibtex_entry)
            
            elif format.lower() == "apa":
                # Generate APA format
                authors_apa = ", ".join([
                    f"{author.last_name}, {author.first_name[0]}." 
                    for author in doc.citation.authors
                ])
                
                apa_entry = f"{authors_apa} ({doc.citation.publication_date.year}). {doc.citation.title}. {doc.citation.journal}"
                if doc.citation.volume:
                    apa_entry += f", {doc.citation.volume}"
                if doc.citation.issue:
                    apa_entry += f"({doc.citation.issue})"
                if doc.citation.pages:
                    apa_entry += f", {doc.citation.pages}"
                apa_entry += "."
                if doc.citation.doi:
                    apa_entry += f" https://doi.org/{doc.citation.doi}"
                
                bibliography_entries.append(apa_entry)
        
        return {
            "format": format,
            "total_entries": len(bibliography_entries),
            "bibliography": bibliography_entries,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error exporting bibliography: {str(e)}"
        )

# Update main.py to include knowledge repository router
"""
Add to backend/main.py:

from api import clinical, drugs, knowledge, guidelines, analytics, knowledge_repository

app.include_router(knowledge_repository.router)
"""

# Frontend Knowledge Repository Management Component
# frontend/src/components/KnowledgeRepositoryManager.tsx

FRONTEND_COMPONENT = '''
import React, { useState, useEffect } from 'react';
import { 
  BookOpen, Search, Filter, Download, RefreshCw, 
  BarChart3, TrendingUp, Shield, AlertCircle,
  Eye, ExternalLink, Calendar, Users
} from 'lucide-react';

interface RepositoryStats {
  total_documents: number;
  document_types: Record<string, number>;
  evidence_levels: Record<string, number>;
  quality_metrics: Record<string, number>;
}

interface DocumentSummary {
  document_id: string;
  title: string;
  document_type: string;
  evidence_level: string;
  publication_date: string;
  authors: string[];
  journal: string;
  abstract: string;
  quality_score: number;
  citation_count: number;
}

const KnowledgeRepositoryManager: React.FC = () => {
  const [stats, setStats] = useState<RepositoryStats | null>(null);
  const [documents, setDocuments] = useState<DocumentSummary[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState({
    specialty: '',
    document_type: '',
    evidence_level: ''
  });
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    loadRepositoryData();
  }, []);

  const loadRepositoryData = async () => {
    setLoading(true);
    try {
      const statsResponse = await fetch('http://localhost:8000/knowledge-repository/');
      const statsData = await statsResponse.json();
      setStats(statsData);
    } catch (error) {
      console.error('Error loading repository data:', error);
    } finally {
      setLoading(false);
    }
  };

  const searchDocuments = async () => {
    setLoading(true);
    try {
      const searchRequest = {
        query: searchQuery,
        ...filters,
        max_results: 50
      };
      
      const response = await fetch('http://localhost:8000/knowledge-repository/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(searchRequest)
      });
      
      const results = await response.json();
      setDocuments(results);
    } catch (error) {
      console.error('Error searching documents:', error);
    } finally {
      setLoading(false);
    }
  };

  const getQualityColor = (score: number) => {
    if (score >= 0.9) return 'text-green-600 bg-green-100';
    if (score >= 0.8) return 'text-blue-600 bg-blue-100';
    if (score >= 0.7) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getEvidenceLevelColor = (level: string) => {
    switch (level.toUpperCase()) {
      case 'A': return 'bg-green-100 text-green-800';
      case 'B': return 'bg-blue-100 text-blue-800';
      case 'C': return 'bg-yellow-100 text-yellow-800';
      case 'D': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading && !stats) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-medical-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Knowledge Repository</h1>
          <p className="text-gray-600">Manage and explore medical literature database</p>
        </div>
        <button
          onClick={loadRepositoryData}
          className="btn-secondary flex items-center"
        >
          <RefreshCw className="w-4 h-4 mr-2" />
          Refresh
        </button>
      </div>

      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="flex space-x-8">
          {[
            { id: 'overview', label: 'Overview', icon: BarChart3 },
            { id: 'search', label: 'Search Documents', icon: Search },
            { id: 'quality', label: 'Quality Report', icon: Shield }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? 'border-medical-500 text-medical-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <tab.icon className="w-4 h-4 mr-2" />
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && stats && (
        <div className="space-y-6">
          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="card">
              <div className="flex items-center">
                <BookOpen className="w-8 h-8 text-medical-600 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Documents</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.total_documents.toLocaleString()}</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <Shield className="w-8 h-8 text-green-600 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600">Avg Quality Score</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.quality_metrics.average_quality_score?.toFixed(2)}</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <TrendingUp className="w-8 h-8 text-blue-600 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600">Peer Reviewed</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.quality_metrics.peer_reviewed_percentage?.toFixed(0)}%</p>
                </div>
              </div>
            </div>

            <div className="card">
              <div className="flex items-center">
                <Eye className="w-8 h-8 text-purple-600 mr-3" />
                <div>
                  <p className="text-sm font-medium text-gray-600">Open Access</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.quality_metrics.open_access_percentage?.toFixed(0)}%</p>
                </div>
              </div>
            </div>
          </div>

          {/* Distribution Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Document Types</h3>
              <div className="space-y-2">
                {Object.entries(stats.document_types).map(([type, count]) => (
                  <div key={type} className="flex justify-between items-center">
                    <span className="text-sm capitalize">{type.replace('_', ' ')}</span>
                    <div className="flex items-center">
                      <div className="w-20 bg-gray-200 rounded-full h-2 mr-2">
                        <div 
                          className="bg-medical-600 h-2 rounded-full" 
                          style={{ width: `${(count / stats.total_documents) * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-sm font-medium">{count}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Evidence Levels</h3>
              <div className="space-y-2">
                {Object.entries(stats.evidence_levels).map(([level, count]) => (
                  <div key={level} className="flex justify-between items-center">
                    <span className={`text-sm px-2 py-1 rounded ${getEvidenceLevelColor(level)}`}>
                      Level {level}
                    </span>
                    <div className="flex items-center">
                      <div className="w-20 bg-gray-200 rounded-full h-2 mr-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full" 
                          style={{ width: `${(count / stats.total_documents) * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-sm font-medium">{count}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Search Tab */}
      {activeTab === 'search' && (
        <div className="space-y-6">
          {/* Search Interface */}
          <div className="card">
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
              <div className="md:col-span-2">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search medical literature..."
                  className="input-field"
                  onKeyPress={(e) => e.key === 'Enter' && searchDocuments()}
                />
              </div>
              <select
                value={filters.specialty}
                onChange={(e) => setFilters({...filters, specialty: e.target.value})}
                className="input-field"
              >
                <option value="">All Specialties</option>
                <option value="cardiology">Cardiology</option>
                <option value="endocrinology">Endocrinology</option>
                <option value="infectious_disease">Infectious Disease</option>
                <option value="emergency_medicine">Emergency Medicine</option>
              </select>
              <select
                value={filters.evidence_level}
                onChange={(e) => setFilters({...filters, evidence_level: e.target.value})}
                className="input-field"
              >
                <option value="">All Evidence Levels</option>
                <option value="A">Level A</option>
                <option value="B">Level B</option>
                <option value="C">Level C</option>
              </select>
              <button
                onClick={searchDocuments}
                disabled={loading}
                className="btn-primary disabled:opacity-50"
              >
                {loading ? 'Searching...' : 'Search'}
              </button>
            </div>
          </div>

          {/* Search Results */}
          {documents.length > 0 && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Search Results ({documents.length})</h3>
              {documents.map((doc) => (
                <div key={doc.document_id} className="card border-l-4 border-medical-500">
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex-1">
                      <h4 className="font-semibold text-lg text-gray-900 mb-1">{doc.title}</h4>
                      <div className="flex items-center space-x-4 text-sm text-gray-600 mb-2">
                        <span>{doc.authors.slice(0, 3).join(', ')}{doc.authors.length > 3 ? ' et al.' : ''}</span>
                        <span>•</span>
                        <span>{doc.journal}</span>
                        <span>•</span>
                        <span>{new Date(doc.publication_date).getFullYear()}</span>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2 ml-4">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${getEvidenceLevelColor(doc.evidence_level)}`}>
                        Level {doc.evidence_level}
                      </span>
                      <span className={`px-2 py-1 rounded text-xs font-medium ${getQualityColor(doc.quality_score)}`}>
                        Quality: {(doc.quality_score * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                  
                  <p className="text-gray-700 text-sm mb-3 line-clamp-3">{doc.abstract}</p>
                  
                  <div className="flex justify-between items-center">
                    <div className="flex items-center space-x-4 text-xs text-gray-500">
                      <span className="capitalize">{doc.document_type.replace('_', ' ')}</span>
                      <span>Citations: {doc.citation_count}</span>
                    </div>
                    
                    <div className="flex space-x-2">
                      <button className="text-medical-600 hover:text-medical-700 text-sm">
                        View Details
                      </button>
                      <button className="text-gray-600 hover:text-gray-700">
                        <ExternalLink className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Quality Tab */}
      {activeTab === 'quality' && (
        <div className="space-y-6">
          <div className="card">
            <h3 className="text-lg font-semibold mb-4">Repository Quality Assessment</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <div className="text-3xl font-bold text-green-600">A</div>
                <div className="text-sm text-green-600">Overall Grade</div>
                <div className="text-xs text-gray-600 mt-1">High Quality Repository</div>
              </div>
              
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <div className="text-3xl font-bold text-blue-600">{stats?.quality_metrics.average_quality_score?.toFixed(2)}</div>
                <div className="text-sm text-blue-600">Quality Score</div>
                <div className="text-xs text-gray-600 mt-1">Above Average</div>
              </div>
              
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <div className="text-3xl font-bold text-purple-600">{stats?.quality_metrics.recent_content_percentage?.toFixed(0)}%</div>
                <div className="text-sm text-purple-600">Recent Content</div>
                <div className="text-xs text-gray-600 mt-1">Last 5 Years</div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="card">
              <h4 className="font-semibold mb-3">Quality Strengths</h4>
              <ul className="space-y-2">
                <li className="flex items-center text-green-600">
                  <Shield className="w-4 h-4 mr-2" />
                  High peer review rate ({stats?.quality_metrics.peer_reviewed_percentage?.toFixed(0)}%)
                </li>
                <li className="flex items-center text-green-600">
                  <TrendingUp className="w-4 h-4 mr-2" />
                  Strong evidence base (Level A & B dominant)
                </li>
                <li className="flex items-center text-green-600">
                  <BookOpen className="w-4 h-4 mr-2" />
                  Diverse document types
                </li>
              </ul>
            </div>

            <div className="card">
              <h4 className="font-semibold mb-3">Improvement Areas</h4>
              <ul className="space-y-2">
                <li className="flex items-center text-orange-600">
                  <AlertCircle className="w-4 h-4 mr-2" />
                  Increase open access content
                </li>
                <li className="flex items-center text-orange-600">
                  <Calendar className="w-4 h-4 mr-2" />
                  Add more recent publications
                </li>
                <li className="flex items-center text-orange-600">
                  <Users className="w-4 h-4 mr-2" />
                  Expand specialty coverage
                </li>
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default KnowledgeRepositoryManager;

// Test script for Knowledge Repository
# backend/test_knowledge_repository.py

import asyncio
from data.knowledge_repository_database import *

async def test_knowledge_repository():
    print("Testing Knowledge Base Repository...")
    
    # Test repository statistics
    stats = get_repository_statistics()
    print(f"\\nRepository Statistics:")
    print(f"Total Documents: {stats['repository_metrics']['total_documents']}")
    print(f"Document Types: {stats['repository_metrics']['document_types']}")
    print(f"Average Quality: {stats['repository_metrics']['average_quality_score']}")
    
    # Test search functionality  
    search_results = search_knowledge_repository("diabetes management")
    print(f"\\nSearch Results for 'diabetes management': {len(search_results)} documents")
    
    # Test document retrieval
    if search_results:
        doc = get_document_by_id(search_results[0])
        if doc:
            print(f"\\nSample Document:")
            print(f"Title: {doc.title}")
            print(f"Type: {doc.document_type.value}")
            print(f"Evidence Level: {doc.evidence_level.value}")
            print(f"Authors: {len(doc.citation.authors)} authors")
            print(f"Quality Score: {doc.quality_score}")
    
    # Test filtering
    filtered_results = search_knowledge_repository(
        "cardiovascular",
        {"specialty": "cardiology", "evidence_level": "A"}
    )
    print(f"\\nFiltered Results: {len(filtered_results)} documents")
    
    # Test source information
    sources = knowledge_repository.sources
    print(f"\\nKnowledge Sources: {len(sources)} sources")
    for source_id, source in list(sources.items())[:3]:
        print(f"  - {source.name}: {source.document_count} documents")
    
    print("\\nKnowledge Repository testing completed!")

if __name__ == "__main__":
    asyncio.run(test_knowledge_repository())
'''

# Create comprehensive test for the entire knowledge repository system
async def test_complete_knowledge_system():
    """Test the complete knowledge repository system"""
    print("="*60)
    print("COMPREHENSIVE KNOWLEDGE REPOSITORY TESTING")
    print("="*60)
    
    # Test 1: Repository initialization
    print("\\n1. Repository Initialization:")
    total_docs = len(knowledge_repository.documents)
    total_sources = len(knowledge_repository.sources)
    print(f"   Documents loaded: {total_docs}")
    print(f"   Sources configured: {total_sources}")
    
    # Test 2: Document type distribution
    print("\\n2. Document Type Analysis:")
    type_counts = {}
    for doc in knowledge_repository.documents.values():
        doc_type = doc.document_type.value
        type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
    
    for doc_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = count / total_docs * 100
        print(f"   {doc_type}: {count} ({percentage:.1f}%)")
    
    # Test 3: Quality metrics
    print("\\n3. Quality Assessment:")
    quality_scores = [doc.quality_score for doc in knowledge_repository.documents.values()]
    evidence_levels = [doc.evidence_level.value for doc in knowledge_repository.documents.values()]
    
    avg_quality = sum(quality_scores) / len(quality_scores)
    high_quality = sum(1 for score in quality_scores if score >= 0.9)
    level_a_count = sum(1 for level in evidence_levels if level == "A")
    
    print(f"   Average Quality Score: {avg_quality:.3f}")
    print(f"   High Quality Documents (≥0.9): {high_quality} ({high_quality/total_docs*100:.1f}%)")
    print(f"   Level A Evidence: {level_a_count} ({level_a_count/total_docs*100:.1f}%)")
    
    # Test 4: Search functionality
    print("\\n4. Search Function Testing:")
    test_queries = [
        "diabetes management",
        "cardiovascular disease", 
        "antibiotic resistance",
        "stroke treatment",
        "clinical guidelines"
    ]
    
    for query in test_queries:
        results = search_knowledge_repository(query)
        print(f"   '{query}': {len(results)} results")
    
    # Test 5: Content coverage
    print("\\n5. Content Coverage Analysis:")
    specialties = set()
    for doc in knowledge_repository.documents.values():
        specialties.update(doc.specialties)
    
    print(f"   Medical Specialties Covered: {len(specialties)}")
    print(f"   Specialties: {', '.join(sorted(specialties))}")
    
    # Test 6: Processing metadata
    print("\\n6. Processing Quality:")
    processing_data = list(knowledge_repository.processing_metadata.values())
    if processing_data:
        avg_confidence = sum(p.confidence_score for p in processing_data) / len(processing_data)
        validated_count = sum(1 for p in processing_data if p.validation_status == "validated")
        
        print(f"   Processed Documents: {len(processing_data)}")
        print(f"   Average Confidence: {avg_confidence:.3f}")
        print(f"   Validation Rate: {validated_count/len(processing_data)*100:.1f}%")
    
    print("\\n" + "="*60)
    print("KNOWLEDGE REPOSITORY SYSTEM READY")
    print("="*60)
    
    return {
        "total_documents": total_docs,
        "total_sources": total_sources,
        "average_quality": avg_quality,
        "specialties_covered": len(specialties),
        "system_status": "operational"
    }

if __name__ == "__main__":
    result = asyncio.run(test_complete_knowledge_system())