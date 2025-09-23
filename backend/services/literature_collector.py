# backend/services/literature_collector.py
import os
import requests
import time
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime, timedelta
import json
from dataclasses import dataclass
from urllib.parse import quote

logger = logging.getLogger(__name__)

@dataclass
class MedicalArticle:
    pmid: str
    title: str
    abstract: str
    authors: List[str]
    journal: str
    publication_date: str
    doi: Optional[str]
    keywords: List[str]
    mesh_terms: List[str]
    article_type: str
    url: str

class PubMedCollector:
    def __init__(self):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.email = os.getenv("PUBMED_EMAIL", "your-email@example.com")  # Required by NCBI
        self.api_key = os.getenv("PUBMED_API_KEY")  # Optional but recommended
        self.rate_limit = 0.34  # Seconds between requests (3 per second max)
        
    def search_articles(
        self, 
        query: str, 
        max_results: int = 100,
        publication_years: int = 5,
        article_types: List[str] = None
    ) -> List[str]:
        """Search PubMed and return list of PMIDs"""
        
        if article_types is None:
            article_types = [
                "Practice Guideline",
                "Systematic Review", 
                "Meta-Analysis",
                "Randomized Controlled Trial",
                "Clinical Trial"
            ]
        
        # Build search query
        search_terms = [query]
        
        # Add date filter
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365 * publication_years)
        date_filter = f"(\"{start_date.strftime('%Y/%m/%d')}\"[PDat] : \"{end_date.strftime('%Y/%m/%d')}\"[PDat])"
        search_terms.append(date_filter)
        
        # Add article type filters
        if article_types:
            type_filter = " OR ".join([f'"{atype}"[Publication Type]' for atype in article_types])
            search_terms.append(f"({type_filter})")
        
        # Add quality filters
        search_terms.extend([
            "English[Language]",
            "humans[MeSH Terms]",
            "hasabstract[text]"
        ])
        
        full_query = " AND ".join(search_terms)
        
        params = {
            'db': 'pubmed',
            'term': full_query,
            'retmax': max_results,
            'retmode': 'xml',
            'email': self.email,
            'sort': 'relevance'
        }
        
        if self.api_key:
            params['api_key'] = self.api_key
            
        try:
            response = requests.get(f"{self.base_url}/esearch.fcgi", params=params)
            time.sleep(self.rate_limit)
            
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                pmids = [pmid.text for pmid in root.findall('.//Id')]
                logger.info(f"Found {len(pmids)} articles for query: {query}")
                return pmids
            else:
                logger.error(f"PubMed search failed: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error searching PubMed: {e}")
            return []
    
    def fetch_article_details(self, pmids: List[str]) -> List[MedicalArticle]:
        """Fetch detailed information for list of PMIDs"""
        articles = []
        
        # Process in batches of 200 (NCBI limit)
        batch_size = 200
        for i in range(0, len(pmids), batch_size):
            batch_pmids = pmids[i:i + batch_size]
            batch_articles = self._fetch_batch_details(batch_pmids)
            articles.extend(batch_articles)
            
        return articles
    
    def _fetch_batch_details(self, pmids: List[str]) -> List[MedicalArticle]:
        """Fetch details for a batch of PMIDs"""
        pmid_str = ",".join(pmids)
        
        params = {
            'db': 'pubmed',
            'id': pmid_str,
            'retmode': 'xml',
            'email': self.email
        }
        
        if self.api_key:
            params['api_key'] = self.api_key
            
        try:
            response = requests.get(f"{self.base_url}/efetch.fcgi", params=params)
            time.sleep(self.rate_limit)
            
            if response.status_code == 200:
                return self._parse_pubmed_xml(response.content)
            else:
                logger.error(f"PubMed fetch failed: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching PubMed details: {e}")
            return []
    
    def _parse_pubmed_xml(self, xml_content: bytes) -> List[MedicalArticle]:
        """Parse PubMed XML response into MedicalArticle objects"""
        articles = []
        
        try:
            root = ET.fromstring(xml_content)
            
            for article_elem in root.findall('.//PubmedArticle'):
                try:
                    # Extract PMID
                    pmid_elem = article_elem.find('.//PMID')
                    pmid = pmid_elem.text if pmid_elem is not None else ""
                    
                    # Extract basic info
                    title_elem = article_elem.find('.//ArticleTitle')
                    title = title_elem.text if title_elem is not None else ""
                    
                    abstract_elem = article_elem.find('.//AbstractText')
                    abstract = abstract_elem.text if abstract_elem is not None else ""
                    
                    # Extract journal info
                    journal_elem = article_elem.find('.//Journal/Title')
                    journal = journal_elem.text if journal_elem is not None else ""
                    
                    # Extract authors
                    authors = []
                    for author in article_elem.findall('.//Author'):
                        lastname = author.find('LastName')
                        firstname = author.find('ForeName')
                        if lastname is not None and firstname is not None:
                            authors.append(f"{firstname.text} {lastname.text}")
                    
                    # Extract publication date
                    pub_date = ""
                    date_elem = article_elem.find('.//PubDate/Year')
                    if date_elem is not None:
                        pub_date = date_elem.text
                    
                    # Extract DOI
                    doi = ""
                    for article_id in article_elem.findall('.//ArticleId'):
                        if article_id.get('IdType') == 'doi':
                            doi = article_id.text
                            break
                    
                    # Extract MeSH terms
                    mesh_terms = []
                    for mesh in article_elem.findall('.//MeshHeading/DescriptorName'):
                        mesh_terms.append(mesh.text)
                    
                    # Extract keywords
                    keywords = []
                    for keyword in article_elem.findall('.//Keyword'):
                        keywords.append(keyword.text)
                    
                    # Extract article type
                    article_type = "Research Article"
                    pub_type = article_elem.find('.//PublicationType')
                    if pub_type is not None:
                        article_type = pub_type.text
                    
                    # Create URL
                    url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                    
                    if pmid and title and abstract:
                        article = MedicalArticle(
                            pmid=pmid,
                            title=title,
                            abstract=abstract,
                            authors=authors,
                            journal=journal,
                            publication_date=pub_date,
                            doi=doi,
                            keywords=keywords,
                            mesh_terms=mesh_terms,
                            article_type=article_type,
                            url=url
                        )
                        articles.append(article)
                        
                except Exception as e:
                    logger.warning(f"Error parsing individual article: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing PubMed XML: {e}")
            
        return articles

class GuidelineCollector:
    """Collect clinical guidelines from major medical organizations"""
    
    def __init__(self):
        self.guidelines_sources = {
            "AHA/ACC": {
                "base_url": "https://www.ahajournals.org",
                "search_terms": ["guidelines", "scientific statement", "consensus"]
            },
            "ADA": {
                "base_url": "https://care.diabetesjournals.org",
                "search_terms": ["standards of care", "position statement", "consensus"]
            },
            "IDSA": {
                "base_url": "https://www.idsociety.org",
                "search_terms": ["practice guidelines", "clinical practice"]
            }
        }
    
    def collect_guidelines(self, specialty: str, max_guidelines: int = 50) -> List[Dict[str, Any]]:
        """Collect recent guidelines for a medical specialty"""
        # This would implement web scraping or API calls to guideline sources
        # For now, return curated list of important guidelines
        
        specialty_guidelines = {
            "cardiology": [
                {
                    "title": "2022 AHA/ACC/HFSA Guideline for the Management of Heart Failure",
                    "organization": "AHA/ACC/HFSA",
                    "year": 2022,
                    "specialty": "cardiology",
                    "evidence_level": "A",
                    "url": "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001063",
                    "topics": ["heart failure", "ACE inhibitors", "beta blockers", "diuretics"]
                },
                {
                    "title": "2021 ACC/AHA/SCAI Guideline for Coronary Artery Revascularization",
                    "organization": "ACC/AHA/SCAI", 
                    "year": 2021,
                    "specialty": "cardiology",
                    "evidence_level": "A",
                    "url": "https://www.ahajournals.org/doi/10.1161/CIR.0000000000001038",
                    "topics": ["PCI", "CABG", "coronary artery disease", "revascularization"]
                }
            ],
            "endocrinology": [
                {
                    "title": "Standards of Care in Diabetes 2024",
                    "organization": "ADA",
                    "year": 2024,
                    "specialty": "endocrinology", 
                    "evidence_level": "A",
                    "url": "https://care.diabetesjournals.org/content/47/Supplement_1",
                    "topics": ["diabetes", "HbA1c", "metformin", "insulin", "GLP-1"]
                }
            ],
            "infectious_disease": [
                {
                    "title": "IDSA Practice Guidelines for Healthcare-Associated Ventriculitis and Meningitis",
                    "organization": "IDSA",
                    "year": 2017,
                    "specialty": "infectious_disease",
                    "evidence_level": "A", 
                    "url": "https://academic.oup.com/cid/article/64/6/e34/2895274",
                    "topics": ["meningitis", "ventriculitis", "antibiotics", "CSF"]
                }
            ]
        }
        
        return specialty_guidelines.get(specialty, [])

class MedicalKnowledgeExpander:
    """Main class to orchestrate medical knowledge expansion"""
    
    def __init__(self):
        self.pubmed_collector = PubMedCollector()
        self.guideline_collector = GuidelineCollector()
        
    def expand_knowledge_base(self, specialties: List[str], articles_per_specialty: int = 100):
        """Expand knowledge base across multiple specialties"""
        
        specialty_queries = {
            "cardiology": [
                "acute coronary syndrome management",
                "heart failure treatment guidelines", 
                "hypertension management",
                "atrial fibrillation anticoagulation",
                "cardiac arrest resuscitation"
            ],
            "endocrinology": [
                "diabetes mellitus management",
                "thyroid disorders treatment",
                "adrenal insufficiency",
                "diabetic ketoacidosis",
                "hypoglycemia management"
            ],
            "emergency_medicine": [
                "sepsis management protocol",
                "trauma resuscitation guidelines",
                "stroke acute management",
                "anaphylaxis treatment",
                "overdose management"
            ],
            "infectious_disease": [
                "antibiotic resistance guidelines",
                "pneumonia treatment protocols", 
                "UTI management guidelines",
                "sepsis antibiotic therapy",
                "meningitis treatment"
            ],
            "pulmonology": [
                "asthma management guidelines",
                "COPD treatment protocols",
                "pneumonia diagnosis treatment",
                "pulmonary embolism management",
                "mechanical ventilation"
            ]
        }
        
        all_articles = []
        all_guidelines = []
        
        for specialty in specialties:
            logger.info(f"Expanding knowledge for {specialty}...")
            
            # Collect guidelines
            guidelines = self.guideline_collector.collect_guidelines(specialty)
            all_guidelines.extend(guidelines)
            
            # Collect research articles
            if specialty in specialty_queries:
                for query in specialty_queries[specialty]:
                    pmids = self.pubmed_collector.search_articles(
                        query, 
                        max_results=articles_per_specialty // len(specialty_queries[specialty])
                    )
                    
                    if pmids:
                        articles = self.pubmed_collector.fetch_article_details(pmids[:20])  # Limit for demo
                        all_articles.extend(articles)
        
        return all_articles, all_guidelines