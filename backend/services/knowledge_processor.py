
import os
import hashlib
import logging
import json
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import PyPDF2
from docx import Document as DocxDocument
from bs4 import BeautifulSoup
import re
from services.rag_service import RAGService, Document

logger = logging.getLogger(__name__)

@dataclass
class MedicalArticle:
    """Data class for medical articles from PubMed"""
    pmid: str
    title: str
    abstract: str
    journal: str
    authors: List[str]
    publication_date: str
    doi: str = ""
    article_type: str = ""
    mesh_terms: List[str] = None
    keywords: List[str] = None
    url: str = ""
    
    def __post_init__(self):
        if self.mesh_terms is None:
            self.mesh_terms = []
        if self.keywords is None:
            self.keywords = []

class KnowledgeProcessor:
    def __init__(self):
        self.rag_service = RAGService()
        self.chunk_size = 1000  # characters
        self.chunk_overlap = 200  # characters
    
    def process_text_file(self, file_path: str, metadata: Dict[str, Any] = None) -> List[Document]:
        """Process a text file and return Document objects"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            base_metadata = {
                "source_file": os.path.basename(file_path),
                "file_type": "text",
                **(metadata or {})
            }
            
            return self._chunk_text(content, base_metadata)
            
        except Exception as e:
            logger.error(f"Error processing text file {file_path}: {e}")
            return []
    
    def process_pdf_file(self, file_path: str, metadata: Dict[str, Any] = None) -> List[Document]:
        """Process a PDF file and return Document objects"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                content = ""
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    content += f"\n--- Page {page_num + 1} ---\n{page_text}"
            
            base_metadata = {
                "source_file": os.path.basename(file_path),
                "file_type": "pdf",
                "total_pages": len(pdf_reader.pages),
                **(metadata or {})
            }
            
            return self._chunk_text(content, base_metadata)
            
        except Exception as e:
            logger.error(f"Error processing PDF file {file_path}: {e}")
            return []
    
    def process_medical_guideline(self, content: str, guideline_info: Dict[str, Any]) -> List[Document]:
        """Process medical guideline content with specific metadata"""
        metadata = {
            "document_type": "clinical_guideline",
            "specialty": guideline_info.get("specialty", "general"),
            "organization": guideline_info.get("organization", "unknown"),
            "year": guideline_info.get("year"),
            "evidence_level": guideline_info.get("evidence_level", "unknown"),
            "guideline_title": guideline_info.get("title", "")
        }
        
        return self._chunk_text(content, metadata)
    
    def process_research_paper(self, content: str, paper_info: Dict[str, Any]) -> List[Document]:
        """Process research paper with specific metadata"""
        metadata = {
            "document_type": "research_paper",
            "journal": paper_info.get("journal", ""),
            "authors": paper_info.get("authors", []),
            "publication_year": paper_info.get("year"),
            "doi": paper_info.get("doi", ""),
            "study_type": paper_info.get("study_type", ""),
            "paper_title": paper_info.get("title", "")
        }
        
        return self._chunk_text(content, metadata)
    
    def _chunk_text(self, text: str, base_metadata: Dict[str, Any]) -> List[Document]:
        """Split text into chunks with overlap"""
        # Clean the text
        text = self._clean_text(text)
        
        chunks = []
        start = 0
        chunk_num = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings within the last 200 characters
                search_start = max(start + self.chunk_size - 200, start)
                sentence_end = self._find_sentence_boundary(text, search_start, end)
                if sentence_end != -1:
                    end = sentence_end
            
            chunk_text = text[start:end].strip()
            
            if len(chunk_text) > 50:  # Only create chunks with meaningful content
                # Create unique ID for this chunk
                chunk_id = self._generate_chunk_id(chunk_text, base_metadata, chunk_num)
                
                chunk_metadata = {
                    **base_metadata,
                    "chunk_number": chunk_num,
                    "chunk_start": start,
                    "chunk_end": end,
                    "chunk_size": len(chunk_text)
                }
                
                document = Document(
                    content=chunk_text,
                    metadata=chunk_metadata,
                    doc_id=chunk_id
                )
                
                chunks.append(document)
                chunk_num += 1
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            if start >= len(text):
                break
        
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """Clean text by removing extra whitespace and formatting"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove page headers/footers patterns
        text = re.sub(r'--- Page \d+ ---', '', text)
        # Remove multiple newlines
        text = re.sub(r'\n+', '\n', text)
        return text.strip()
    
    def _find_sentence_boundary(self, text: str, start: int, end: int) -> int:
        """Find a good sentence boundary for chunking"""
        # Look for sentence endings (., !, ?) followed by space and capital letter
        sentence_pattern = r'[.!?]\s+[A-Z]'
        
        search_text = text[start:end]
        matches = list(re.finditer(sentence_pattern, search_text))
        
        if matches:
            # Take the last sentence boundary found
            last_match = matches[-1]
            return start + last_match.start() + 1
        
        return -1
    
    def _generate_chunk_id(self, content: str, metadata: Dict[str, Any], chunk_num: int) -> str:
        """Generate unique ID for a chunk"""
        # Create hash from content and metadata
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        source = metadata.get("source_file", "unknown")
        return f"{source}_{chunk_num}_{content_hash}"
    
    def load_sample_medical_data(self) -> bool:
        """Load sample medical knowledge for testing"""
        try:
            sample_guidelines = [
                {
                    "content": """
                    Acute Coronary Syndrome Management Guidelines:
                    
                    Initial Assessment:
                    - Obtain 12-lead ECG within 10 minutes of presentation
                    - Check troponin levels immediately and repeat in 3-6 hours
                    - Assess for STEMI vs NSTEMI vs unstable angina
                    
                    STEMI Management:
                    - Primary PCI within 90 minutes if available
                    - Fibrinolytic therapy if PCI not available within 120 minutes
                    - Dual antiplatelet therapy (aspirin + P2Y12 inhibitor)
                    - Anticoagulation with heparin or bivalirudin
                    
                    Risk Stratification:
                    - Use TIMI or GRACE risk scores
                    - High-risk patients require early invasive strategy
                    - Consider stress testing for low-risk patients
                    """,
                    "metadata": {
                        "specialty": "cardiology",
                        "organization": "AHA/ACC",
                        "year": 2023,
                        "evidence_level": "A",
                        "title": "Acute Coronary Syndrome Guidelines"
                    }
                },
                {
                    "content": """
                    Diabetes Management - Type 2:
                    
                    Initial Therapy:
                    - Metformin as first-line unless contraindicated
                    - Target HbA1c < 7% for most adults
                    - Lifestyle modifications: diet and exercise
                    
                    Second-line Options:
                    - SGLT2 inhibitors for patients with heart failure or CKD
                    - GLP-1 agonists for weight loss and cardiovascular benefits
                    - Sulfonylureas if cost is a concern
                    
                    Monitoring:
                    - HbA1c every 3-6 months
                    - Annual eye and foot exams
                    - Monitor kidney function
                    """,
                    "metadata": {
                        "specialty": "endocrinology",
                        "organization": "ADA",
                        "year": 2023,
                        "evidence_level": "A",
                        "title": "Type 2 Diabetes Management"
                    }
                },
                {
                    "content": """
                    Hypertension Management Guidelines:
                    
                    Blood Pressure Targets:
                    - General population: < 130/80 mmHg
                    - Elderly (≥65): < 130/80 mmHg if tolerated
                    - Diabetes/CKD: < 130/80 mmHg
                    
                    First-line Medications:
                    - ACE inhibitors or ARBs
                    - Thiazide or thiazide-like diuretics
                    - Calcium channel blockers
                    
                    Lifestyle Modifications:
                    - DASH diet
                    - Sodium restriction (<2.3g/day)
                    - Regular aerobic exercise
                    - Weight management
                    - Limit alcohol consumption
                    """,
                    "metadata": {
                        "specialty": "cardiology",
                        "organization": "AHA/ACC",
                        "year": 2023,
                        "evidence_level": "A",
                        "title": "Hypertension Management Guidelines"
                    }
                }
            ]
            
            documents = []
            for guideline in sample_guidelines:
                docs = self.process_medical_guideline(
                    guideline["content"], 
                    guideline["metadata"]
                )
                documents.extend(docs)
            
            # Add documents to RAG service
            success = self.rag_service.add_documents(documents)
            
            if success:
                logger.info(f"Successfully loaded {len(documents)} sample medical documents")
                return True
            else:
                logger.error("Failed to load sample medical documents")
                return False
                
        except Exception as e:
            logger.error(f"Error loading sample medical data: {e}")
            return False

    # Add these methods to the existing KnowledgeProcessor class

def process_pubmed_articles(self, articles: List[MedicalArticle]) -> List[Document]:
    """Process PubMed articles into documents"""
    documents = []
    
    for article in articles:
        # Combine title and abstract for full content
        content = f"Title: {article.title}\n\nAbstract: {article.abstract}"
        
        # Add MeSH terms and keywords to content for better searchability
        if article.mesh_terms:
            content += f"\n\nMeSH Terms: {', '.join(article.mesh_terms)}"
        
        if article.keywords:
            content += f"\n\nKeywords: {', '.join(article.keywords)}"
        
        metadata = {
            "document_type": "research_paper",
            "pmid": article.pmid,
            "title": article.title,
            "journal": article.journal,
            "authors": article.authors,
            "publication_year": article.publication_date,
            "doi": article.doi,
            "article_type": article.article_type,
            "mesh_terms": article.mesh_terms,
            "keywords": article.keywords,
            "url": article.url,
            "evidence_level": self._determine_evidence_level(article.article_type),
            "specialty": self._determine_specialty(article.mesh_terms)
        }
        
        # Create chunks from the content
        chunks = self._chunk_text(content, metadata)
        documents.extend(chunks)
    
    return documents

def process_clinical_guidelines(self, guidelines: List[Dict[str, Any]]) -> List[Document]:
    """Process clinical guidelines into documents"""
    documents = []
    
    for guideline in guidelines:
        # This would normally fetch the full guideline text
        # For demo, we'll use the available information
        content = f"Clinical Guideline: {guideline['title']}\n\n"
        content += f"Organization: {guideline['organization']}\n"
        content += f"Publication Year: {guideline['year']}\n"
        content += f"Specialty: {guideline['specialty']}\n"
        
        if 'topics' in guideline:
            content += f"Key Topics: {', '.join(guideline['topics'])}\n\n"
        
        # In a real implementation, you would fetch the full guideline content here
        content += "Full guideline content would be processed here..."
        
        metadata = {
            "document_type": "clinical_guideline",
            "title": guideline['title'],
            "organization": guideline['organization'],
            "publication_year": guideline['year'],
            "specialty": guideline['specialty'],
            "evidence_level": guideline.get('evidence_level', 'A'),
            "url": guideline.get('url', ''),
            "topics": guideline.get('topics', [])
        }
        
        chunks = self._chunk_text(content, metadata)
        documents.extend(chunks)
    
    return documents

def _determine_evidence_level(self, article_type: str) -> str:
    """Determine evidence level based on article type"""
    high_evidence_types = [
        "Meta-Analysis",
        "Systematic Review", 
        "Practice Guideline",
        "Randomized Controlled Trial"
    ]
    
    moderate_evidence_types = [
        "Clinical Trial",
        "Controlled Clinical Trial",
        "Multicenter Study"
    ]
    
    if any(etype in article_type for etype in high_evidence_types):
        return "A"
    elif any(etype in article_type for etype in moderate_evidence_types):
        return "B"
    else:
        return "C"

def _determine_specialty(self, mesh_terms: List[str]) -> str:
    """Determine medical specialty from MeSH terms"""
    specialty_keywords = {
        "cardiology": ["heart", "cardiac", "cardiovascular", "coronary", "myocardial"],
        "endocrinology": ["diabetes", "insulin", "thyroid", "hormone", "endocrine"],
        "infectious_disease": ["infection", "antibiotic", "bacteria", "virus", "sepsis"],
        "pulmonology": ["lung", "respiratory", "pneumonia", "asthma", "COPD"],
        "emergency_medicine": ["emergency", "trauma", "resuscitation", "acute"],
        "neurology": ["brain", "neurologic", "stroke", "seizure", "nervous system"]
    }
    
    mesh_text = " ".join(mesh_terms).lower()
    
    for specialty, keywords in specialty_keywords.items():
        if any(keyword in mesh_text for keyword in keywords):
            return specialty
    
    return "general_medicine"

def load_expanded_medical_knowledge(self, specialties: List[str] = None) -> bool:
    """Load expanded medical knowledge from multiple sources"""
    try:
        if specialties is None:
            specialties = ["cardiology", "endocrinology", "emergency_medicine", "infectious_disease"]
        
        logger.info(f"Expanding medical knowledge for specialties: {specialties}")
        
        # Initialize knowledge expander
        from services.literature_collector import MedicalKnowledgeExpander
        expander = MedicalKnowledgeExpander()
        
        # Collect articles and guidelines
        articles, guidelines = expander.expand_knowledge_base(specialties, articles_per_specialty=50)
        
        all_documents = []
        
        # Process PubMed articles
        if articles:
            logger.info(f"Processing {len(articles)} research articles...")
            article_docs = self.process_pubmed_articles(articles)
            all_documents.extend(article_docs)
        
        # Process clinical guidelines
        if guidelines:
            logger.info(f"Processing {len(guidelines)} clinical guidelines...")
            guideline_docs = self.process_clinical_guidelines(guidelines)
            all_documents.extend(guideline_docs)
        
        # Add to RAG service
        if all_documents:
            success = self.rag_service.add_documents(all_documents)
            
            if success:
                logger.info(f"Successfully loaded {len(all_documents)} documents from {len(articles)} articles and {len(guidelines)} guidelines")
                
                # Save metadata for tracking
                self._save_knowledge_metadata(articles, guidelines)
                
                return True
            else:
                logger.error("Failed to add documents to RAG service")
                return False
        else:
            logger.warning("No documents were processed")
            return False
            
    except Exception as e:
        logger.error(f"Error loading expanded medical knowledge: {e}")
        return False

def _save_knowledge_metadata(self, articles: List, guidelines: List[Dict]):
    """Save metadata about loaded knowledge for tracking"""
    try:
        metadata = {
            "last_updated": datetime.now().isoformat(),
            "total_articles": len(articles),
            "total_guidelines": len(guidelines),
            "articles_by_specialty": {},
            "guidelines_by_specialty": {},
            "sources": {
                "pubmed_articles": len(articles),
                "clinical_guidelines": len(guidelines)
            }
        }
        
        # Count by specialty
        for article in articles:
            specialty = getattr(article, 'specialty', 'unknown')
            metadata["articles_by_specialty"][specialty] = metadata["articles_by_specialty"].get(specialty, 0) + 1
        
        for guideline in guidelines:
            specialty = guideline.get('specialty', 'unknown')
            metadata["guidelines_by_specialty"][specialty] = metadata["guidelines_by_specialty"].get(specialty, 0) + 1
        
        # Save to file
        os.makedirs('data/metadata', exist_ok=True)
        with open('data/metadata/knowledge_base_info.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info("Knowledge base metadata saved")
        
    except Exception as e:
        logger.warning(f"Could not save knowledge metadata: {e}")