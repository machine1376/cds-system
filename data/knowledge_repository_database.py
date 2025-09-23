# backend/data/knowledge_repository_database.py
"""
Comprehensive mock Knowledge Base Repository for Clinical Decision Support System
Manages medical literature, documents, citations, and knowledge sources
"""

from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import json
import hashlib
import random

class DocumentType(Enum):
    RESEARCH_PAPER = "research_paper"
    CLINICAL_GUIDELINE = "clinical_guideline"
    TEXTBOOK_CHAPTER = "textbook_chapter"
    REVIEW_ARTICLE = "review_article"
    META_ANALYSIS = "meta_analysis"
    CASE_STUDY = "case_study"
    DRUG_MONOGRAPH = "drug_monograph"
    CLINICAL_TRIAL = "clinical_trial"
    SYSTEMATIC_REVIEW = "systematic_review"
    CONFERENCE_ABSTRACT = "conference_abstract"

class EvidenceLevel(Enum):
    LEVEL_A = "A"  # High-quality evidence
    LEVEL_B = "B"  # Moderate-quality evidence  
    LEVEL_C = "C"  # Low-quality evidence
    LEVEL_D = "D"  # Very low-quality evidence

class PublicationStatus(Enum):
    PUBLISHED = "published"
    IN_PRESS = "in_press"
    PREPRINT = "preprint"
    RETRACTED = "retracted"
    ARCHIVED = "archived"

class AccessLevel(Enum):
    OPEN_ACCESS = "open_access"
    SUBSCRIPTION = "subscription"
    INSTITUTIONAL = "institutional"
    FREE_ABSTRACT = "free_abstract"

@dataclass
class Author:
    first_name: str
    last_name: str
    middle_initial: Optional[str]
    affiliation: str
    orcid_id: Optional[str]
    email: Optional[str]
    is_corresponding: bool = False

@dataclass
class Citation:
    title: str
    authors: List[Author]
    journal: str
    volume: Optional[str]
    issue: Optional[str]
    pages: Optional[str]
    publication_date: datetime
    doi: Optional[str]
    pmid: Optional[str]
    pmcid: Optional[str]
    isbn: Optional[str]
    publisher: Optional[str]

@dataclass
class KnowledgeDocument:
    document_id: str
    title: str
    document_type: DocumentType
    citation: Citation
    abstract: str
    full_text: Optional[str]
    keywords: List[str]
    mesh_terms: List[str]
    specialties: List[str]
    evidence_level: EvidenceLevel
    publication_status: PublicationStatus
    access_level: AccessLevel
    source_url: Optional[str]
    pdf_url: Optional[str]
    added_date: datetime
    last_updated: datetime
    version: str
    word_count: int
    language: str
    clinical_relevance_score: float
    citation_count: int
    quality_score: float
    peer_reviewed: bool
    retraction_notice: Optional[str]

@dataclass
class KnowledgeSource:
    source_id: str
    name: str
    organization: str
    source_type: str  # "journal", "publisher", "database", "repository"
    url: str
    impact_factor: Optional[float]
    credibility_score: float
    subscription_status: AccessLevel
    last_indexed: datetime
    document_count: int
    quality_metrics: Dict[str, float]

@dataclass
class ProcessingMetadata:
    processing_id: str
    document_id: str
    processing_date: datetime
    extraction_method: str  # "ocr", "pdf_parser", "api", "manual"
    confidence_score: float
    errors_detected: List[str]
    validation_status: str  # "validated", "pending", "failed"
    chunk_count: int
    embedding_status: str  # "completed", "pending", "failed"
    indexing_status: str

class KnowledgeBaseRepository:
    """Comprehensive repository for managing medical knowledge documents"""
    
    def __init__(self):
        self.documents = self._generate_knowledge_documents()
        self.sources = self._generate_knowledge_sources()
        self.processing_metadata = self._generate_processing_metadata()
        self.search_index = self._build_search_index()
        self.citation_network = self._build_citation_network()
        self.quality_metrics = self._calculate_quality_metrics()
        
    def _generate_knowledge_documents(self) -> Dict[str, KnowledgeDocument]:
        """Generate comprehensive collection of medical knowledge documents"""
        documents = {}
        
        # High-impact medical journals and their typical content
        journal_templates = {
            "New England Journal of Medicine": {
                "impact_factor": 176.079,
                "specialties": ["internal_medicine", "cardiology", "oncology", "infectious_disease"],
                "document_types": [DocumentType.RESEARCH_PAPER, DocumentType.CLINICAL_TRIAL, DocumentType.REVIEW_ARTICLE]
            },
            "The Lancet": {
                "impact_factor": 168.273,
                "specialties": ["public_health", "neurology", "psychiatry", "global_health"],
                "document_types": [DocumentType.RESEARCH_PAPER, DocumentType.META_ANALYSIS, DocumentType.SYSTEMATIC_REVIEW]
            },
            "JAMA": {
                "impact_factor": 157.335,
                "specialties": ["internal_medicine", "surgery", "pediatrics", "psychiatry"],
                "document_types": [DocumentType.RESEARCH_PAPER, DocumentType.CLINICAL_TRIAL, DocumentType.REVIEW_ARTICLE]
            },
            "Nature Medicine": {
                "impact_factor": 87.241,
                "specialties": ["molecular_medicine", "genetics", "immunology", "oncology"],
                "document_types": [DocumentType.RESEARCH_PAPER, DocumentType.REVIEW_ARTICLE]
            },
            "Circulation": {
                "impact_factor": 39.918,
                "specialties": ["cardiology", "cardiovascular_surgery"],
                "document_types": [DocumentType.RESEARCH_PAPER, DocumentType.CLINICAL_TRIAL, DocumentType.CLINICAL_GUIDELINE]
            },
            "Diabetes Care": {
                "impact_factor": 19.112,
                "specialties": ["endocrinology", "internal_medicine"],
                "document_types": [DocumentType.RESEARCH_PAPER, DocumentType.CLINICAL_GUIDELINE, DocumentType.REVIEW_ARTICLE]
            },
            "Critical Care Medicine": {
                "impact_factor": 8.913,
                "specialties": ["critical_care", "emergency_medicine", "anesthesiology"],
                "document_types": [DocumentType.RESEARCH_PAPER, DocumentType.CLINICAL_TRIAL, DocumentType.CASE_STUDY]
            },
            "Antimicrobial Agents and Chemotherapy": {
                "impact_factor": 5.938,
                "specialties": ["infectious_disease", "pharmacology", "microbiology"],
                "document_types": [DocumentType.RESEARCH_PAPER, DocumentType.DRUG_MONOGRAPH, DocumentType.CLINICAL_TRIAL]
            }
        }
        
        # Generate documents for each journal
        doc_counter = 1
        for journal, journal_info in journal_templates.items():
            # Generate 50-100 documents per journal
            num_docs = random.randint(50, 100)
            
            for _ in range(num_docs):
                doc_id = f"doc_{doc_counter:06d}"
                
                # Select random specialty and document type
                specialty = random.choice(journal_info["specialties"])
                doc_type = random.choice(journal_info["document_types"])
                
                # Generate realistic title based on specialty
                title = self._generate_realistic_title(specialty, doc_type)
                
                # Generate authors (2-8 authors typical)
                authors = self._generate_authors(random.randint(2, 8))
                
                # Publication date (last 10 years, with bias toward recent)
                days_ago = int(random.expovariate(1/1000))  # Exponential distribution favoring recent
                days_ago = min(days_ago, 3650)  # Cap at 10 years
                pub_date = datetime.now() - timedelta(days=days_ago)
                
                # Generate citation
                citation = Citation(
                    title=title,
                    authors=authors,
                    journal=journal,
                    volume=str(random.randint(1, 400)),
                    issue=str(random.randint(1, 52)),
                    pages=f"{random.randint(1, 2000)}-{random.randint(2001, 2020)}",
                    publication_date=pub_date,
                    doi=f"10.{random.randint(1000, 9999)}/{random.randint(100000, 999999)}",
                    pmid=str(random.randint(10000000, 39999999)),
                    pmcid=f"PMC{random.randint(1000000, 9999999)}" if random.random() < 0.6 else None,
                    isbn=None,
                    publisher=journal.split()[0] if len(journal.split()) > 1 else journal
                )
                
                # Generate abstract
                abstract = self._generate_realistic_abstract(specialty, doc_type)
                
                # Generate keywords and MeSH terms
                keywords = self._generate_keywords(specialty, doc_type)
                mesh_terms = self._generate_mesh_terms(specialty, doc_type)
                
                # Determine evidence level based on document type
                evidence_level = self._assign_evidence_level(doc_type, journal_info["impact_factor"])
                
                # Generate quality metrics
                quality_score = self._calculate_quality_score(doc_type, journal_info["impact_factor"], pub_date)
                citation_count = self._estimate_citation_count(pub_date, journal_info["impact_factor"])
                
                # Generate full document
                document = KnowledgeDocument(
                    document_id=doc_id,
                    title=title,
                    document_type=doc_type,
                    citation=citation,
                    abstract=abstract,
                    full_text=self._generate_full_text_sample(abstract, specialty) if random.random() < 0.7 else None,
                    keywords=keywords,
                    mesh_terms=mesh_terms,
                    specialties=[specialty],
                    evidence_level=evidence_level,
                    publication_status=PublicationStatus.PUBLISHED,
                    access_level=self._determine_access_level(journal_info["impact_factor"]),
                    source_url=f"https://doi.org/{citation.doi}",
                    pdf_url=f"https://example.com/pdf/{doc_id}.pdf" if random.random() < 0.8 else None,
                    added_date=datetime.now() - timedelta(days=random.randint(1, 180)),
                    last_updated=datetime.now() - timedelta(days=random.randint(1, 30)),
                    version="1.0",
                    word_count=random.randint(2000, 8000),
                    language="en",
                    clinical_relevance_score=random.uniform(0.6, 1.0),
                    citation_count=citation_count,
                    quality_score=quality_score,
                    peer_reviewed=True,
                    retraction_notice=None
                )
                
                documents[doc_id] = document
                doc_counter += 1
        
        # Add some clinical guidelines from major organizations
        guidelines = self._generate_clinical_guidelines()
        documents.update(guidelines)
        
        # Add some textbook chapters and drug monographs
        textbooks = self._generate_textbook_chapters()
        documents.update(textbooks)
        
        drug_monographs = self._generate_drug_monographs()
        documents.update(drug_monographs)
        
        return documents
    
    def _generate_realistic_title(self, specialty: str, doc_type: DocumentType) -> str:
        """Generate realistic medical paper titles"""
        title_templates = {
            "cardiology": [
                "Efficacy of Novel {intervention} in Patients with {condition}",
                "Long-term Outcomes Following {procedure} for {condition}",
                "Risk Factors for {complication} in {population}",
                "Comparative Effectiveness of {treatment1} versus {treatment2}",
                "Predictors of {outcome} in Patients with {condition}"
            ],
            "endocrinology": [
                "Glycemic Control with {medication} in Type 2 Diabetes",
                "Thyroid Function and {outcome} in {population}",
                "Novel Therapeutic Approaches for {condition}",
                "Metabolic Effects of {intervention} in Diabetic Patients",
                "Long-term Safety of {medication} in {condition}"
            ],
            "infectious_disease": [
                "Antimicrobial Resistance Patterns in {organism}",
                "Treatment Outcomes for {infection} with {antibiotic}",
                "Epidemiology of {pathogen} in {setting}",
                "Novel Diagnostic Approaches for {infection}",
                "Prevention Strategies for Healthcare-Associated {infection}"
            ],
            "emergency_medicine": [
                "Early Recognition and Management of {condition}",
                "Diagnostic Accuracy of {test} in Emergency Department",
                "Outcomes Following {intervention} for {emergency_condition}",
                "Risk Stratification for {condition} in Emergency Setting",
                "Impact of {protocol} on {outcome} in Emergency Care"
            ],
            "neurology": [
                "Therapeutic Efficacy of {treatment} in {neurological_condition}",
                "Biomarkers for Early Detection of {neurodegenerative_disease}",
                "Cognitive Outcomes Following {intervention}",
                "Genetic Factors in {neurological_disorder}",
                "Neuroimaging Findings in {condition}"
            ]
        }
        
        # Specialty-specific terms
        terms = {
            "cardiology": {
                "intervention": ["PCI", "CABG", "cardiac rehabilitation", "beta-blocker therapy"],
                "condition": ["acute MI", "heart failure", "atrial fibrillation", "coronary artery disease"],
                "procedure": ["coronary angioplasty", "valve replacement", "cardiac catheterization"],
                "complication": ["in-stent restenosis", "cardiac death", "stroke"],
                "population": ["elderly patients", "diabetic patients", "post-MI patients"],
                "outcome": ["cardiovascular mortality", "major adverse cardiac events", "quality of life"],
                "treatment1": ["atorvastatin", "metoprolol", "lisinopril"],
                "treatment2": ["rosuvastatin", "carvedilol", "losartan"]
            },
            "endocrinology": {
                "medication": ["metformin", "insulin glargine", "semaglutide", "empagliflozin"],
                "condition": ["diabetic nephropathy", "thyroid cancer", "Cushing's syndrome"],
                "outcome": ["HbA1c reduction", "weight loss", "cardiovascular events"],
                "population": ["obese patients", "elderly diabetics", "pregnant women"],
                "intervention": ["continuous glucose monitoring", "bariatric surgery", "lifestyle modification"]
            },
            "infectious_disease": {
                "organism": ["MRSA", "Pseudomonas aeruginosa", "Candida auris"],
                "infection": ["ventilator-associated pneumonia", "catheter-related bloodstream infection", "C. difficile colitis"],
                "antibiotic": ["vancomycin", "meropenem", "ceftaroline"],
                "pathogen": ["carbapenem-resistant Enterobacteriaceae", "multidrug-resistant tuberculosis"],
                "setting": ["intensive care units", "long-term care facilities", "emergency departments"]
            }
        }
        
        if specialty in title_templates:
            template = random.choice(title_templates[specialty])
            specialty_terms = terms.get(specialty, {})
            
            # Replace placeholders with appropriate terms
            for placeholder, term_list in specialty_terms.items():
                if f"{{{placeholder}}}" in template:
                    template = template.replace(f"{{{placeholder}}}", random.choice(term_list))
            
            return template
        
        return f"Clinical Study on {specialty.replace('_', ' ').title()}"
    
    def _generate_authors(self, count: int) -> List[Author]:
        """Generate realistic author information"""
        first_names = [
            "Michael", "Sarah", "David", "Jennifer", "Robert", "Lisa", "James", "Mary",
            "John", "Patricia", "William", "Linda", "Richard", "Barbara", "Joseph", "Elizabeth",
            "Thomas", "Jessica", "Christopher", "Susan", "Charles", "Margaret", "Daniel", "Dorothy"
        ]
        
        last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
            "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White"
        ]
        
        institutions = [
            "Harvard Medical School", "Johns Hopkins University", "Mayo Clinic", "Stanford University",
            "University of California San Francisco", "Cleveland Clinic", "Mass General Brigham",
            "Memorial Sloan Kettering", "MD Anderson Cancer Center", "Emory University",
            "University of Pennsylvania", "Yale School of Medicine", "Duke University",
            "University of Michigan", "Northwestern University", "Mount Sinai Health System"
        ]
        
        authors = []
        for i in range(count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            
            author = Author(
                first_name=first_name,
                last_name=last_name,
                middle_initial=random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") if random.random() < 0.7 else None,
                affiliation=random.choice(institutions),
                orcid_id=f"0000-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}" if random.random() < 0.6 else None,
                email=f"{first_name.lower()}.{last_name.lower()}@example.edu" if random.random() < 0.3 else None,
                is_corresponding=(i == 0)  # First author is corresponding
            )
            authors.append(author)
        
        return authors
    
    def _generate_realistic_abstract(self, specialty: str, doc_type: DocumentType) -> str:
        """Generate realistic medical abstracts"""
        abstract_templates = {
            DocumentType.RESEARCH_PAPER: """
            BACKGROUND: {background_statement}
            
            METHODS: {study_design} involving {sample_size} patients with {condition}. {intervention_description} {outcome_measures}
            
            RESULTS: {primary_results} {secondary_results} {safety_results}
            
            CONCLUSIONS: {conclusion_statement} {clinical_implications}
            """,
            
            DocumentType.CLINICAL_TRIAL: """
            OBJECTIVE: To evaluate the {objective} in patients with {condition}.
            
            DESIGN: {trial_design} conducted at {num_centers} centers.
            
            PARTICIPANTS: {sample_size} patients with {inclusion_criteria}.
            
            INTERVENTION: {intervention_details}
            
            MAIN OUTCOME MEASURES: {primary_endpoint} and {secondary_endpoints}.
            
            RESULTS: {efficacy_results} {safety_results}
            
            CONCLUSIONS: {clinical_conclusion}
            """,
            
            DocumentType.SYSTEMATIC_REVIEW: """
            PURPOSE: To systematically review {review_topic}.
            
            DATA SOURCES: {databases_searched} through {search_date}.
            
            STUDY SELECTION: {inclusion_criteria} {exclusion_criteria}
            
            DATA EXTRACTION: {data_extraction_methods}
            
            RESULTS: {number_studies} studies involving {total_participants} participants. {main_findings}
            
            CONCLUSIONS: {synthesis_conclusion}
            """
        }
        
        # Get appropriate template
        template = abstract_templates.get(doc_type, abstract_templates[DocumentType.RESEARCH_PAPER])
        
        # Fill in placeholders with specialty-appropriate content
        abstract = self._fill_abstract_template(template, specialty, doc_type)
        
        return abstract.strip()
    
    def _fill_abstract_template(self, template: str, specialty: str, doc_type: DocumentType) -> str:
        """Fill abstract template with specialty-specific content"""
        # This would be a comprehensive function in production
        # For now, return a simplified version
        
        sample_abstracts = {
            "cardiology": """
            BACKGROUND: Cardiovascular disease remains the leading cause of mortality worldwide. Novel therapeutic approaches are needed to improve outcomes in high-risk patients.
            
            METHODS: Randomized controlled trial involving 1,247 patients with acute coronary syndrome. Patients received either standard care plus novel intervention or standard care alone. Primary endpoint was major adverse cardiovascular events at 12 months.
            
            RESULTS: The intervention group showed a 23% reduction in primary endpoint (HR 0.77, 95% CI 0.62-0.96, p=0.02). Secondary endpoints including cardiovascular mortality and repeat revascularization were also significantly improved.
            
            CONCLUSIONS: This novel intervention demonstrates significant clinical benefit in patients with acute coronary syndrome and should be considered for clinical implementation.
            """,
            
            "endocrinology": """
            BACKGROUND: Type 2 diabetes management continues to evolve with new therapeutic options. The long-term cardiovascular effects of newer glucose-lowering agents require further investigation.
            
            METHODS: Prospective cohort study of 2,156 adults with type 2 diabetes followed for 36 months. Primary outcome was composite cardiovascular events. Secondary outcomes included glycemic control and safety measures.
            
            RESULTS: Significant improvement in HbA1c (mean reduction 1.2%, p<0.001) with 19% reduction in cardiovascular events (HR 0.81, 95% CI 0.69-0.95). Hypoglycemia rates were low (3.2% vs 8.1% with standard therapy).
            
            CONCLUSIONS: This therapeutic approach provides superior glycemic control with cardiovascular benefits and acceptable safety profile in patients with type 2 diabetes.
            """
        }
        
        return sample_abstracts.get(specialty, template)
    
    def _generate_keywords(self, specialty: str, doc_type: DocumentType) -> List[str]:
        """Generate relevant keywords for medical documents"""
        specialty_keywords = {
            "cardiology": [
                "cardiovascular disease", "myocardial infarction", "heart failure", "coronary artery disease",
                "atrial fibrillation", "hypertension", "cardiac catheterization", "echocardiography",
                "electrocardiography", "cardiac rehabilitation", "percutaneous coronary intervention"
            ],
            "endocrinology": [
                "diabetes mellitus", "insulin resistance", "thyroid disorders", "metabolic syndrome",
                "glucose control", "HbA1c", "diabetic complications", "hormone therapy",
                "endocrine disorders", "obesity", "lipid metabolism"
            ],
            "infectious_disease": [
                "antimicrobial resistance", "antibiotic therapy", "bacterial infections", "viral infections",
                "healthcare-associated infections", "sepsis", "pneumonia", "bacteremia",
                "infection control", "epidemiology", "pathogen identification"
            ],
            "emergency_medicine": [
                "emergency department", "acute care", "triage", "trauma", "resuscitation",
                "critical care", "point-of-care testing", "emergency procedures", "rapid diagnosis",
                "emergency protocols", "acute management"
            ],
            "neurology": [
                "neurological disorders", "stroke", "seizures", "multiple sclerosis", "Parkinson's disease",
                "Alzheimer's disease", "neuroimaging", "neurodegenerative diseases", "epilepsy",
                "cognitive function", "neurological examination"
            ]
        }
        
        base_keywords = specialty_keywords.get(specialty, ["clinical medicine", "patient care", "treatment outcomes"])
        
        # Add document-type specific keywords
        type_keywords = {
            DocumentType.CLINICAL_TRIAL: ["randomized controlled trial", "clinical efficacy", "therapeutic intervention"],
            DocumentType.SYSTEMATIC_REVIEW: ["systematic review", "meta-analysis", "evidence synthesis"],
            DocumentType.CLINICAL_GUIDELINE: ["clinical guidelines", "best practices", "treatment recommendations"],
            DocumentType.META_ANALYSIS: ["meta-analysis", "statistical analysis", "pooled analysis"]
        }
        
        keywords = random.sample(base_keywords, min(5, len(base_keywords)))
        if doc_type in type_keywords:
            keywords.extend(random.sample(type_keywords[doc_type], 2))
        
        return keywords[:8]  # Limit to 8 keywords
    
    def _generate_mesh_terms(self, specialty: str, doc_type: DocumentType) -> List[str]:
        """Generate Medical Subject Headings (MeSH) terms"""
        mesh_terms_by_specialty = {
            "cardiology": [
                "Cardiovascular Diseases", "Heart Disease Risk Factors", "Myocardial Infarction",
                "Heart Failure", "Coronary Artery Disease", "Arrhythmias, Cardiac",
                "Hypertension", "Electrocardiography", "Echocardiography",
                "Cardiac Catheterization", "Angioplasty", "Coronary Vessels"
            ],
            "endocrinology": [
                "Diabetes Mellitus, Type 2", "Insulin Resistance", "Blood Glucose",
                "Hemoglobin A, Glycosylated", "Thyroid Diseases", "Metabolic Syndrome",
                "Diabetic Complications", "Endocrine System Diseases", "Hormones",
                "Glucose Metabolism Disorders", "Obesity"
            ],
            "infectious_disease": [
                "Bacterial Infections", "Anti-Bacterial Agents", "Drug Resistance, Microbial",
                "Cross Infection", "Sepsis", "Pneumonia", "Bacteremia",
                "Infection Control", "Epidemiologic Studies", "Communicable Diseases",
                "Antimicrobial Stewardship"
            ]
        }
        
        base_mesh = mesh_terms_by_specialty.get(specialty, ["Humans", "Treatment Outcome"])
        selected_mesh = random.sample(base_mesh, min(6, len(base_mesh)))
        
        # Add common MeSH terms
        common_mesh = ["Humans", "Adult", "Treatment Outcome", "Follow-Up Studies"]
        selected_mesh.extend(random.sample(common_mesh, 2))
        
        return list(set(selected_mesh))  # Remove duplicates
    
    def _assign_evidence_level(self, doc_type: DocumentType, impact_factor: float) -> EvidenceLevel:
        """Assign evidence level based on document type and journal quality"""
        if doc_type in [DocumentType.META_ANALYSIS, DocumentType.SYSTEMATIC_REVIEW]:
            return EvidenceLevel.LEVEL_A
        elif doc_type == DocumentType.CLINICAL_TRIAL and impact_factor > 20:
            return EvidenceLevel.LEVEL_A
        elif doc_type == DocumentType.CLINICAL_TRIAL:
            return EvidenceLevel.LEVEL_B
        elif doc_type == DocumentType.CLINICAL_GUIDELINE:
            return EvidenceLevel.LEVEL_A
        elif impact_factor > 50:
            return random.choice([EvidenceLevel.LEVEL_A, EvidenceLevel.LEVEL_B])
        elif impact_factor > 10:
            return random.choice([EvidenceLevel.LEVEL_B, EvidenceLevel.LEVEL_C])
        else:
            return random.choice([EvidenceLevel.LEVEL_C, EvidenceLevel.LEVEL_D])
    
    def _calculate_quality_score(self, doc_type: DocumentType, impact_factor: float, pub_date: datetime) -> float:
        """Calculate document quality score"""
        base_score = 0.5
        
        # Document type scoring
        type_scores = {
            DocumentType.META_ANALYSIS: 0.95,
            DocumentType.SYSTEMATIC_REVIEW: 0.90,
            DocumentType.CLINICAL_TRIAL: 0.85,
            DocumentType.CLINICAL_GUIDELINE: 0.88,
            DocumentType.RESEARCH_PAPER: 0.75,
            DocumentType.REVIEW_ARTICLE: 0.70,
            DocumentType.CASE_STUDY: 0.60
        }
        
        base_score = type_scores.get(doc_type, 0.65)
        
        # Impact factor bonus
        if impact_factor > 100:
            base_score += 0.05
        elif impact_factor > 50:
            base_score += 0.03
        elif impact_factor > 20:
            base_score += 0.02
        
        # Recency bonus (newer papers get slight boost)
        days_old = (datetime.now() - pub_date).days
        if days_old < 365:
            base_score += 0.02
        elif days_old < 1095:  # 3 years
            base_score += 0.01
        
        return min(base_score, 1.0)
    
    def _estimate_citation_count(self, pub_date: datetime, impact_factor: float) -> int:
        """Estimate citation count based on age and journal impact"""
        days_old = (datetime.now() - pub_date).days
        years_old = days_old / 365.25
        
        # Base citations per year based on impact factor
        citations_per_year = impact_factor / 10
        
        # Apply age factor (citations accumulate over time but with diminishing returns)
        total_citations = citations_per_year * years_old * random.uniform(0.5, 1.5)
        
        return max(0, int(total_citations))
    
    def _determine_access_level(self, impact_factor: float) -> AccessLevel:
        """Determine access level based on journal prestige"""
        if random.random() < 0.3:  # 30% open access
            return AccessLevel.OPEN_ACCESS
        elif impact_factor > 50:
            return AccessLevel.SUBSCRIPTION
        elif impact_factor > 10:
            return random.choice([AccessLevel.SUBSCRIPTION, AccessLevel.INSTITUTIONAL])
        else:
            return random.choice([AccessLevel.FREE_ABSTRACT, AccessLevel.INSTITUTIONAL])
    
    def _generate_full_text_sample(self, abstract: str, specialty: str) -> str:
        """Generate sample full text content"""
        introduction = f"""
        INTRODUCTION
        
        {specialty.replace('_', ' ').title()} represents a critical area of clinical medicine requiring evidence-based approaches to patient care. Recent advances in this field have led to improved understanding of disease mechanisms and therapeutic interventions.
        
        The current study addresses important clinical questions that have direct implications for patient outcomes and healthcare delivery.
        """
        
        methods = """
        METHODS
        
        Study Design and Participants
        This study was conducted in accordance with CONSORT guidelines and received institutional review board approval. Participants provided written informed consent.
        
        Statistical Analysis
        Statistical analyses were performed using appropriate methods with significance set at p<0.05. All analyses were performed using intention-to-treat principles.
        
        RESULTS
        
        Baseline Characteristics
        A total of participants were enrolled in the study. Baseline demographics were well-balanced between groups.
        
        Primary Outcomes
        The primary endpoint was met with statistically significant results favoring the intervention group.
        
        DISCUSSION
        
        These findings have important implications for clinical practice and contribute to the growing body of evidence in this field.
        """
        
        return f"{introduction}\n{abstract}\n{methods}"
    
    def _generate_clinical_guidelines(self) -> Dict[str, KnowledgeDocument]:
        """Generate clinical practice guidelines"""
        guidelines = {}
        doc_counter = 5000  # Start from 5000 to avoid conflicts
        
        guideline_data = [
            {
                "title": "2023 AHA/ACC/ACCP/ASPC/NLA/PCNA Guideline for the Management of Patients with Chronic Coronary Disease",
                "organization": "American Heart Association",
                "specialty": "cardiology",
                "year": 2023
            },
            {
                "title": "Standards of Care in Diabetes—2024",
                "organization": "American Diabetes Association", 
                "specialty": "endocrinology",
                "year": 2024
            },
            {
                "title": "Surviving Sepsis Campaign Guidelines 2021",
                "organization": "Society of Critical Care Medicine",
                "specialty": "emergency_medicine",
                "year": 2021
            },
            {
                "title": "IDSA Practice Guidelines for Healthcare-Associated Infections",
                "organization": "Infectious Diseases Society of America",
                "specialty": "infectious_disease", 
                "year": 2022
            }
        ]
        
        for guideline_info in guideline_data:
            doc_id = f"guideline_{doc_counter}"
            
            # Create author representing the organization
            authors = [Author(
                first_name="Clinical",
                last_name="Guidelines Committee",
                middle_initial=None,
                affiliation=guideline_info["organization"],
                orcid_id=None,
                email=None,
                is_corresponding=True
            )]
            
            citation = Citation(
                title=guideline_info["title"],
                authors=authors,
                journal=f"{guideline_info['organization']} Guidelines",
                volume=None,
                issue=None,
                pages=None,
                publication_date=datetime(guideline_info["year"], 1, 1),
                doi=f"10.1000/guideline.{doc_counter}",
                pmid=None,
                pmcid=None,
                isbn=None,
                publisher=guideline_info["organization"]
            )
            
            abstract = f"Comprehensive clinical practice guideline for {guideline_info['specialty']} developed by {guideline_info['organization']}. This evidence-based guideline provides recommendations for diagnosis, treatment, and management based on systematic review of current literature and expert consensus."
            
            document = KnowledgeDocument(
                document_id=doc_id,
                title=guideline_info["title"],
                document_type=DocumentType.CLINICAL_GUIDELINE,
                citation=citation,
                abstract=abstract,
                full_text=f"Complete clinical guideline content for {guideline_info['title']}...",
                keywords=self._generate_keywords(guideline_info["specialty"], DocumentType.CLINICAL_GUIDELINE),
                mesh_terms=self._generate_mesh_terms(guideline_info["specialty"], DocumentType.CLINICAL_GUIDELINE),
                specialties=[guideline_info["specialty"]],
                evidence_level=EvidenceLevel.LEVEL_A,
                publication_status=PublicationStatus.PUBLISHED,
                access_level=AccessLevel.OPEN_ACCESS,
                source_url=f"https://{guideline_info['organization'].lower().replace(' ', '')}.org/guidelines",
                pdf_url=f"https://guidelines.example.com/{doc_id}.pdf",
                added_date=datetime.now() - timedelta(days=30),
                last_updated=datetime.now() - timedelta(days=5),
                version="1.0",
                word_count=random.randint(15000, 50000),
                language="en",
                clinical_relevance_score=0.95,
                citation_count=random.randint(100, 500),
                quality_score=0.95,
                peer_reviewed=True,
                retraction_notice=None
            )
            
            guidelines[doc_id] = document
            doc_counter += 1
        
        return guidelines
    
    def _generate_textbook_chapters(self) -> Dict[str, KnowledgeDocument]:
        """Generate medical textbook chapters"""
        chapters = {}
        doc_counter = 6000
        
        textbooks = [
            {
                "title": "Harrison's Principles of Internal Medicine",
                "publisher": "McGraw-Hill Education",
                "chapters": [
                    "Approach to the Patient with Heart Disease",
                    "Diabetes Mellitus and Metabolic Syndrome",
                    "Infectious Disease Emergencies",
                    "Acute Coronary Syndromes"
                ]
            },
            {
                "title": "Goodman & Gilman's The Pharmacological Basis of Therapeutics",
                "publisher": "McGraw-Hill Education",
                "chapters": [
                    "Cardiovascular Pharmacology",
                    "Antimicrobial Agents",
                    "Endocrine Pharmacology",
                    "Neuropharmacology"
                ]
            }
        ]
        
        for textbook in textbooks:
            for chapter_title in textbook["chapters"]:
                doc_id = f"textbook_{doc_counter}"
                
                authors = [Author(
                    first_name="Expert",
                    last_name="Author",
                    middle_initial="M",
                    affiliation="Academic Medical Center",
                    orcid_id=None,
                    email=None,
                    is_corresponding=True
                )]
                
                citation = Citation(
                    title=f"{chapter_title} - {textbook['title']}",
                    authors=authors,
                    journal=textbook["title"],
                    volume=None,
                    issue=None,
                    pages="Chapter",
                    publication_date=datetime(2023, 1, 1),
                    doi=None,
                    pmid=None,
                    pmcid=None,
                    isbn=f"978-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1, 9)}",
                    publisher=textbook["publisher"]
                )
                
                # Determine specialty from chapter title
                specialty = "internal_medicine"
                if "heart" in chapter_title.lower() or "cardio" in chapter_title.lower():
                    specialty = "cardiology"
                elif "diabetes" in chapter_title.lower() or "endocrine" in chapter_title.lower():
                    specialty = "endocrinology"
                elif "infectious" in chapter_title.lower() or "antimicrobial" in chapter_title.lower():
                    specialty = "infectious_disease"
                
                document = KnowledgeDocument(
                    document_id=doc_id,
                    title=chapter_title,
                    document_type=DocumentType.TEXTBOOK_CHAPTER,
                    citation=citation,
                    abstract=f"Comprehensive textbook chapter covering {chapter_title.lower()} from the authoritative {textbook['title']}.",
                    full_text=f"Complete chapter content for {chapter_title}...",
                    keywords=self._generate_keywords(specialty, DocumentType.TEXTBOOK_CHAPTER),
                    mesh_terms=self._generate_mesh_terms(specialty, DocumentType.TEXTBOOK_CHAPTER),
                    specialties=[specialty],
                    evidence_level=EvidenceLevel.LEVEL_B,
                    publication_status=PublicationStatus.PUBLISHED,
                    access_level=AccessLevel.SUBSCRIPTION,
                    source_url=f"https://accessmedicine.mhmedical.com/content.aspx?bookid={doc_counter}",
                    pdf_url=None,
                    added_date=datetime.now() - timedelta(days=60),
                    last_updated=datetime.now() - timedelta(days=10),
                    version="1.0",
                    word_count=random.randint(8000, 25000),
                    language="en",
                    clinical_relevance_score=0.85,
                    citation_count=random.randint(50, 200),
                    quality_score=0.88,
                    peer_reviewed=True,
                    retraction_notice=None
                )
                
                chapters[doc_id] = document
                doc_counter += 1
        
        return chapters
    
    def _generate_drug_monographs(self) -> Dict[str, KnowledgeDocument]:
        """Generate drug monographs and pharmaceutical information"""
        monographs = {}
        doc_counter = 7000
        
        drugs = [
            {"name": "Atorvastatin", "class": "HMG-CoA Reductase Inhibitor", "specialty": "cardiology"},
            {"name": "Metformin", "class": "Biguanide", "specialty": "endocrinology"},
            {"name": "Vancomycin", "class": "Glycopeptide Antibiotic", "specialty": "infectious_disease"},
            {"name": "Lisinopril", "class": "ACE Inhibitor", "specialty": "cardiology"},
            {"name": "Insulin Glargine", "class": "Long-acting Insulin", "specialty": "endocrinology"},
            {"name": "Meropenem", "class": "Carbapenem Antibiotic", "specialty": "infectious_disease"}
        ]
        
        for drug in drugs:
            doc_id = f"drug_{doc_counter}"
            
            authors = [Author(
                first_name="Drug",
                last_name="Information Specialist",
                middle_initial=None,
                affiliation="Pharmaceutical Database",
                orcid_id=None,
                email=None,
                is_corresponding=True
            )]
            
            citation = Citation(
                title=f"{drug['name']} - Drug Monograph",
                authors=authors,
                journal="Clinical Pharmacology Database",
                volume=None,
                issue=None,
                pages=None,
                publication_date=datetime(2024, 1, 1),
                doi=f"10.1000/drug.{doc_counter}",
                pmid=None,
                pmcid=None,
                isbn=None,
                publisher="Clinical Drug Reference"
            )
            
            abstract = f"Comprehensive drug monograph for {drug['name']}, a {drug['class']} used in {drug['specialty']}. Includes pharmacology, indications, dosing, contraindications, adverse effects, and drug interactions."
            
            document = KnowledgeDocument(
                document_id=doc_id,
                title=f"{drug['name']} - Clinical Drug Information",
                document_type=DocumentType.DRUG_MONOGRAPH,
                citation=citation,
                abstract=abstract,
                full_text=f"Complete drug monograph for {drug['name']} including pharmacokinetics, pharmacodynamics, clinical uses, dosing guidelines, adverse effects, contraindications, and drug interactions.",
                keywords=[drug['name'].lower(), drug['class'].lower(), "pharmacology", "drug therapy", "clinical use"],
                mesh_terms=[drug['name'], "Drug Therapy", "Pharmacology", "Pharmaceutical Preparations"],
                specialties=[drug['specialty']],
                evidence_level=EvidenceLevel.LEVEL_A,
                publication_status=PublicationStatus.PUBLISHED,
                access_level=AccessLevel.SUBSCRIPTION,
                source_url=f"https://drugdatabase.example.com/{drug['name'].lower()}",
                pdf_url=f"https://drugdatabase.example.com/pdf/{doc_id}.pdf",
                added_date=datetime.now() - timedelta(days=15),
                last_updated=datetime.now() - timedelta(days=2),
                version="2.1",
                word_count=random.randint(5000, 12000),
                language="en",
                clinical_relevance_score=0.92,
                citation_count=random.randint(25, 100),
                quality_score=0.90,
                peer_reviewed=True,
                retraction_notice=None
            )
            
            monographs[doc_id] = document
            doc_counter += 1
        
        return monographs
    
    def _generate_knowledge_sources(self) -> Dict[str, KnowledgeSource]:
        """Generate knowledge source metadata"""
        sources = {}
        
        source_data = [
            {
                "name": "PubMed/MEDLINE",
                "organization": "National Library of Medicine",
                "type": "database",
                "url": "https://pubmed.ncbi.nlm.nih.gov",
                "impact_factor": None,
                "credibility": 0.98,
                "access": AccessLevel.OPEN_ACCESS,
                "doc_count": 35000000
            },
            {
                "name": "New England Journal of Medicine",
                "organization": "Massachusetts Medical Society",
                "type": "journal",
                "url": "https://nejm.org",
                "impact_factor": 176.079,
                "credibility": 0.96,
                "access": AccessLevel.SUBSCRIPTION,
                "doc_count": 15000
            },
            {
                "name": "The Lancet",
                "organization": "Elsevier",
                "type": "journal", 
                "url": "https://thelancet.com",
                "impact_factor": 168.273,
                "credibility": 0.95,
                "access": AccessLevel.SUBSCRIPTION,
                "doc_count": 12000
            },
            {
                "name": "Cochrane Library",
                "organization": "Cochrane Collaboration",
                "type": "repository",
                "url": "https://cochranelibrary.com",
                "impact_factor": None,
                "credibility": 0.94,
                "access": AccessLevel.SUBSCRIPTION,
                "doc_count": 8500
            },
            {
                "name": "UpToDate",
                "organization": "Wolters Kluwer",
                "type": "database",
                "url": "https://uptodate.com",
                "impact_factor": None,
                "credibility": 0.92,
                "access": AccessLevel.INSTITUTIONAL,
                "doc_count": 12000
            }
        ]
        
        for i, source_info in enumerate(source_data):
            source_id = f"source_{i+1:03d}"
            
            quality_metrics = {
                "content_accuracy": random.uniform(0.85, 0.98),
                "currency": random.uniform(0.80, 0.95),
                "completeness": random.uniform(0.75, 0.95),
                "citation_quality": random.uniform(0.85, 0.98),
                "peer_review_rate": random.uniform(0.70, 1.0) if source_info["type"] == "journal" else 0.0
            }
            
            source = KnowledgeSource(
                source_id=source_id,
                name=source_info["name"],
                organization=source_info["organization"],
                source_type=source_info["type"],
                url=source_info["url"],
                impact_factor=source_info["impact_factor"],
                credibility_score=source_info["credibility"],
                subscription_status=source_info["access"],
                last_indexed=datetime.now() - timedelta(days=random.randint(1, 7)),
                document_count=source_info["doc_count"],
                quality_metrics=quality_metrics
            )
            
            sources[source_id] = source
        
        return sources
    
    def _generate_processing_metadata(self) -> Dict[str, ProcessingMetadata]:
        """Generate document processing metadata"""
        metadata = {}
        
        for doc_id in list(self.documents.keys())[:100]:  # Generate for first 100 docs
            processing_id = f"proc_{doc_id}"
            
            # Simulate different extraction methods
            extraction_methods = ["pdf_parser", "ocr", "api", "manual"]
            method = random.choice(extraction_methods)
            
            # Confidence varies by method
            confidence_ranges = {
                "api": (0.95, 0.99),
                "pdf_parser": (0.85, 0.95),
                "manual": (0.98, 1.0),
                "ocr": (0.70, 0.90)
            }
            
            confidence = random.uniform(*confidence_ranges[method])
            
            # Generate errors based on confidence
            errors = []
            if confidence < 0.8:
                errors = ["Character recognition errors", "Formatting issues"]
            elif confidence < 0.9:
                errors = ["Minor formatting issues"]
            
            processing = ProcessingMetadata(
                processing_id=processing_id,
                document_id=doc_id,
                processing_date=datetime.now() - timedelta(days=random.randint(1, 90)),
                extraction_method=method,
                confidence_score=confidence,
                errors_detected=errors,
                validation_status="validated" if confidence > 0.85 else "pending",
                chunk_count=random.randint(5, 50),
                embedding_status="completed" if random.random() > 0.05 else "pending",
                indexing_status="completed" if random.random() > 0.02 else "pending"
            )
            
            metadata[processing_id] = processing
        
        return metadata
    
    def _build_search_index(self) -> Dict[str, Set[str]]:
        """Build inverted search index"""
        index = {}
        
        for doc_id, document in self.documents.items():
            # Extract searchable terms
            terms = set()
            
            # Add title words
            terms.update(document.title.lower().split())
            
            # Add abstract words
            terms.update(document.abstract.lower().split())
            
            # Add keywords
            terms.update([kw.lower() for kw in document.keywords])
            
            # Add MeSH terms
            terms.update([mesh.lower() for mesh in document.mesh_terms])
            
            # Build inverted index
            for term in terms:
                if term not in index:
                    index[term] = set()
                index[term].add(doc_id)
        
        return index
    
    def _build_citation_network(self) -> Dict[str, List[str]]:
        """Build citation network between documents"""
        network = {}
        
        # Simulate citation relationships
        doc_ids = list(self.documents.keys())
        
        for doc_id in doc_ids:
            # Each document cites 0-15 other documents
            num_citations = random.randint(0, 15)
            cited_docs = random.sample([d for d in doc_ids if d != doc_id], 
                                     min(num_citations, len(doc_ids)-1))
            network[doc_id] = cited_docs
        
        return network
    
    def _calculate_quality_metrics(self) -> Dict[str, Any]:
        """Calculate overall repository quality metrics"""
        total_docs = len(self.documents)
        
        # Document type distribution
        type_counts = {}
        for doc in self.documents.values():
            doc_type = doc.document_type.value
            type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
        
        # Evidence level distribution
        evidence_counts = {}
        for doc in self.documents.values():
            evidence = doc.evidence_level.value
            evidence_counts[evidence] = evidence_counts.get(evidence, 0) + 1
        
        # Quality scores
        quality_scores = [doc.quality_score for doc in self.documents.values()]
        avg_quality = sum(quality_scores) / len(quality_scores)
        
        # Access levels
        access_counts = {}
        for doc in self.documents.values():
            access = doc.access_level.value
            access_counts[access] = access_counts.get(access, 0) + 1
        
        # Recent content (last 5 years)
        cutoff_date = datetime.now() - timedelta(days=5*365)
        recent_docs = sum(1 for doc in self.documents.values() 
                         if doc.citation.publication_date >= cutoff_date)
        
        return {
            "total_documents": total_docs,
            "document_types": type_counts,
            "evidence_levels": evidence_counts,
            "access_levels": access_counts,
            "average_quality_score": round(avg_quality, 3),
            "recent_content_percentage": round(recent_docs / total_docs * 100, 1),
            "peer_reviewed_percentage": round(
                sum(1 for doc in self.documents.values() if doc.peer_reviewed) / total_docs * 100, 1
            ),
            "open_access_percentage": round(access_counts.get("open_access", 0) / total_docs * 100, 1)
        }
    
    def search_documents(self, query: str, filters: Dict[str, Any] = None) -> List[str]:
        """Search documents by query and filters"""
        query_terms = set(query.lower().split())
        
        # Find documents containing query terms
        matching_docs = set()
        for term in query_terms:
            if term in self.search_index:
                if not matching_docs:
                    matching_docs = self.search_index[term].copy()
                else:
                    matching_docs &= self.search_index[term]
        
        # Apply filters
        if filters:
            filtered_docs = []
            for doc_id in matching_docs:
                doc = self.documents[doc_id]
                
                # Apply specialty filter
                if "specialty" in filters:
                    if filters["specialty"] not in doc.specialties:
                        continue
                
                # Apply document type filter
                if "document_type" in filters:
                    if doc.document_type.value != filters["document_type"]:
                        continue
                
                # Apply evidence level filter
                if "evidence_level" in filters:
                    if doc.evidence_level.value != filters["evidence_level"]:
                        continue
                
                # Apply date range filter
                if "start_date" in filters:
                    if doc.citation.publication_date < filters["start_date"]:
                        continue
                
                if "end_date" in filters:
                    if doc.citation.publication_date > filters["end_date"]:
                        continue
                
                filtered_docs.append(doc_id)
            
            return filtered_docs
        
        return list(matching_docs)
    
    def get_document_statistics(self) -> Dict[str, Any]:
        """Get comprehensive repository statistics"""
        return {
            "repository_metrics": self.quality_metrics,
            "total_sources": len(self.sources),
            "processing_status": {
                "total_processed": len(self.processing_metadata),
                "validation_rate": sum(1 for p in self.processing_metadata.values() 
                                     if p.validation_status == "validated") / len(self.processing_metadata) * 100,
                "embedding_completion": sum(1 for p in self.processing_metadata.values() 
                                          if p.embedding_status == "completed") / len(self.processing_metadata) * 100
            },
            "content_coverage": {
                "specialties_covered": len(set(spec for doc in self.documents.values() 
                                            for spec in doc.specialties)),
                "languages_supported": len(set(doc.language for doc in self.documents.values())),
                "publication_years": {
                    "earliest": min(doc.citation.publication_date.year for doc in self.documents.values()),
                    "latest": max(doc.citation.publication_date.year for doc in self.documents.values())
                }
            }
        }

# Initialize global repository
knowledge_repository = KnowledgeBaseRepository()

# Convenience functions for API use
def search_knowledge_repository(query: str, filters: Dict[str, Any] = None) -> List[str]:
    """Search the knowledge repository"""
    return knowledge_repository.search_documents(query, filters)

def get_document_by_id(doc_id: str) -> Optional[KnowledgeDocument]:
    """Get document by ID"""
    return knowledge_repository.documents.get(doc_id)

def get_repository_statistics() -> Dict[str, Any]:
    """Get repository statistics"""
    return knowledge_repository.get_document_statistics()

def get_source_information(source_id: str) -> Optional[KnowledgeSource]:
    """Get knowledge source information"""
    return knowledge_repository.sources.get(source_id)

def get_processing_metadata(doc_id: str) -> Optional[ProcessingMetadata]:
    """Get processing metadata for document"""
    processing_id = f"proc_{doc_id}"
    return knowledge_repository.processing_metadata.get(processing_id)

# Example usage and testing
if __name__ == "__main__":
    print("Testing Knowledge Base Repository...")
    
    # Test repository statistics
    stats = get_repository_statistics()
    print(f"\nRepository Statistics:")
    print(f"Total Documents: {stats['repository_metrics']['total_documents']}")
    print(f"Document Types: {stats['repository_metrics']['document_types']}")
    print(f"Evidence Levels: {stats['repository_metrics']['evidence_levels']}")
    print(f"Average Quality: {stats['repository_metrics']['average_quality_score']}")
    
    # Test search functionality
    search_results = search_knowledge_repository("diabetes management")
    print(f"\nSearch Results for 'diabetes management': {len(search_results)} documents")
    
    # Test filtered search
    filtered_results = search_knowledge_repository(
        "cardiovascular", 
        {"specialty": "cardiology", "evidence_level": "A"}
    )
    print(f"Filtered search results: {len(filtered_results)} documents")
    
    # Test document retrieval
    if search_results:
        doc = get_document_by_id(search_results[0])
        if doc:
            print(f"\nSample Document:")
            print(f"Title: {doc.title}")
            print(f"Type: {doc.document_type.value}")
            print(f"Evidence Level: {doc.evidence_level.value}")
            print(f"Quality Score: {doc.quality_score}")
    
    print("\nKnowledge Repository initialized successfully!")