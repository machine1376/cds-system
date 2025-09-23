# backend/services/rag_service.py
import os
import openai
from pinecone import Pinecone, ServerlessSpec
import numpy as np
from typing import List, Dict, Any, Optional
import logging
from dataclasses import dataclass
import hashlib
import json

logger = logging.getLogger(__name__)

@dataclass
class Document:
    content: str
    metadata: Dict[str, Any]
    doc_id: str
    embedding: Optional[List[float]] = None

class RAGService:
    def __init__(self):
        self.openai_client = None
        self.pc = None
        self.index = None
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "medical-knowledge")
        self._initialized = False
    
    def _ensure_initialized(self):
        """Initialize clients only when needed"""
        if not self._initialized:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable not set")
            
            self.openai_client = openai.OpenAI(api_key=api_key)
            
            pinecone_key = os.getenv("PINECONE_API_KEY")
            if not pinecone_key:
                raise ValueError("PINECONE_API_KEY environment variable not set")
            
            self.pc = Pinecone(api_key=pinecone_key)
            self._initialize_index()
            self._initialized = True
        self.embedding_model = "text-embedding-ada-002"
        self.embedding_dimension = 1536
        
    def _initialize_index(self):
        """Initialize Pinecone index if it doesn't exist"""
        self._ensure_initialized()
        try:
            # Check if index exists
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            
            if self.index_name not in existing_indexes:
                logger.info(f"Creating new Pinecone index: {self.index_name}")
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.embedding_dimension,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",  # or "gcp" depending on your setup
                        region="us-east-1"  # adjust based on your region
                    )
                )
            
            self.index = self.pc.Index(self.index_name)
            logger.info(f"Connected to Pinecone index: {self.index_name}")
            
        except Exception as e:
            logger.error(f"Error initializing Pinecone index: {e}")
            raise
    
    def create_embedding(self, text: str) -> List[float]:
        """Create embedding for a piece of text using OpenAI"""
        self._ensure_initialized()
        try:
            response = self.openai_client.embeddings.create(
                input=text,
                model=self.embedding_model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            raise
    
    def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for multiple texts in batch"""
        self._ensure_initialized()
        try:
            response = self.openai_client.embeddings.create(
                input=texts,
                model=self.embedding_model
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            logger.error(f"Error creating batch embeddings: {e}")
            raise
    
    def add_documents(self, documents: List[Document]) -> bool:
        """Add documents to the vector database"""
        self._ensure_initialized()
        try:
            # Create embeddings for documents that don't have them
            texts_to_embed = []
            doc_indices = []
            
            for i, doc in enumerate(documents):
                if doc.embedding is None:
                    texts_to_embed.append(doc.content)
                    doc_indices.append(i)
            
            if texts_to_embed:
                embeddings = self.create_embeddings_batch(texts_to_embed)
                for i, embedding in enumerate(embeddings):
                    documents[doc_indices[i]].embedding = embedding
            
            # Prepare vectors for Pinecone
            vectors = []
            for doc in documents:
                vectors.append({
                    "id": doc.doc_id,
                    "values": doc.embedding,
                    "metadata": {
                        **doc.metadata,
                        "content": doc.content[:1000]  # Store first 1000 chars in metadata
                    }
                })
            
            # Upsert to Pinecone in batches
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)
            
            logger.info(f"Successfully added {len(documents)} documents to index")
            return True
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return False
    
    def retrieve_relevant_docs(
        self, 
        query: str, 
        top_k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for a query"""
        self._ensure_initialized()
        try:
            # Create embedding for query
            query_embedding = self.create_embedding(query)
            
            # Search in Pinecone
            search_response = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=filter_dict
            )
            
            # Format results
            results = []
            for match in search_response.matches:
                results.append({
                    "id": match.id,
                    "score": match.score,
                    "content": match.metadata.get("content", ""),
                    "metadata": match.metadata
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the index"""
        self._ensure_initialized()
        try:
            stats = self.index.describe_index_stats()
            return {
                "total_vectors": stats.total_vector_count,
                "dimension": stats.dimension,
                "index_fullness": stats.index_fullness
            }
        except Exception as e:
            logger.error(f"Error getting index stats: {e}")
            return {}
    
    def delete_documents(self, doc_ids: List[str]) -> bool:
        """Delete documents from the index"""
        try:
            self.index.delete(ids=doc_ids)
            logger.info(f"Deleted {len(doc_ids)} documents from index")
            return True
        except Exception as e:
            logger.error(f"Error deleting documents: {e}")
            return False