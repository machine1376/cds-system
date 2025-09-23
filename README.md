cat > README.md << 'EOF'
# Clinical Decision Support System

An AI-powered clinical decision support system that provides evidence-based medical recommendations.

## Setup

1. Clone the repository
2. Create virtual environment: `python -m venv backend/venv`
3. Activate virtual environment: `source backend/venv/bin/activate` (or `backend/venv/Scripts/activate` on Windows)
4. Install dependencies: `cd backend && pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your API keys
6. Run the application: `uvicorn main:app --reload`

## Development

- Backend API runs on `http://localhost:8000`
- API documentation available at `http://localhost:8000/docs`

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `PINECONE_API_KEY`: Your Pinecone API key
- `PINECONE_ENVIRONMENT`: Your Pinecone environment
- `DATABASE_URL`: PostgreSQL connection string

## Testing

Run tests with: `pytest`
EOF
# cds-system
