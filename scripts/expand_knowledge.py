# backend/scripts/expand_knowledge.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from services.knowledge_processor import KnowledgeProcessor
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    """Main function to expand medical knowledge base"""
    print("Starting Medical Knowledge Base Expansion...")
    
    # Initialize processor
    processor = KnowledgeProcessor()
    
    # Define specialties to expand
    specialties = [
        "cardiology",
        "endocrinology", 
        "emergency_medicine",
        "infectious_disease",
        "pulmonology"
    ]
    
    print(f"Expanding knowledge for specialties: {', '.join(specialties)}")
    
    # Load expanded knowledge
    success = processor.load_expanded_medical_knowledge(specialties)
    
    if success:
        print("✅ Knowledge base expansion completed successfully!")
        
        # Get final stats
        stats = processor.rag_service.get_index_stats()
        print(f"📊 Final Index Stats: {stats}")
        
    else:
        print("❌ Knowledge base expansion failed!")
    
    print("Done.")

if __name__ == "__main__":
    asyncio.run(main())