# backend/test_rag.py
import asyncio
from services.knowledge_processor import KnowledgeProcessor
from services.clinical_ai import ClinicalAIService
from models.schemas import ClinicalQuery, PatientContext

async def test_rag_system():
    print("Testing RAG System Setup...")
    
    # 1. Load sample medical data
    print("\n1. Loading sample medical knowledge...")
    processor = KnowledgeProcessor()
    success = processor.load_sample_medical_data()
    print(f"Sample data loaded: {success}")
    
    # 2. Test retrieval
    print("\n2. Testing document retrieval...")
    rag_service = processor.rag_service
    
    # Get index stats
    stats = rag_service.get_index_stats()
    print(f"Index stats: {stats}")
    
    # Test search
    results = rag_service.retrieve_relevant_docs("chest pain management", top_k=3)
    print(f"Found {len(results)} relevant documents for 'chest pain management'")
    for i, result in enumerate(results):
        print(f"  {i+1}. Score: {result['score']:.3f} - {result['content'][:100]}...")
    
    # 3. Test clinical AI
    print("\n3. Testing clinical AI service...")
    ai_service = ClinicalAIService()
    
    # Create test query
    test_query = ClinicalQuery(
        query="65-year-old male with chest pain, elevated troponins, and ECG changes",
        patient_context=PatientContext(
            age=65,
            gender="male",
            current_medications=["aspirin", "metoprolol"],
            medical_conditions=["hypertension", "diabetes"]
        )
    )
    
    try:
        response = ai_service.process_clinical_query(test_query)
        print(f"AI Response generated successfully!")
        print(f"Query ID: {response.query_id}")
        print(f"Processing time: {response.processing_time_ms:.2f}ms")
        print(f"Recommendations: {len(response.recommendations)}")
        
        if response.recommendations:
            rec = response.recommendations[0]
            print(f"First recommendation: {rec.recommendation[:200]}...")
            print(f"Confidence: {rec.confidence_score}")
            
    except Exception as e:
        print(f"Error testing AI service: {e}")

if __name__ == "__main__":
    asyncio.run(test_rag_system())