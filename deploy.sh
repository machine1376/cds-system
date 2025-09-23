#!/bin/bash

# CDS System Deployment Script
echo "🚀 CDS System Deployment Script"
echo "================================"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Check if user is logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway:"
    railway login
fi

echo "📦 Deploying to Railway..."
railway up

echo "🔧 Setting up environment variables..."
echo "Please set your API keys:"
echo ""

# Set environment variables
read -p "Enter your OpenAI API Key: " openai_key
railway variables set OPENAI_API_KEY="$openai_key"

read -p "Enter your Pinecone API Key: " pinecone_key
railway variables set PINECONE_API_KEY="$pinecone_key"

railway variables set PINECONE_INDEX_NAME="medical-knowledge"
railway variables set HOST="0.0.0.0"
railway variables set PORT="8000"

echo "✅ Environment variables set!"

echo "🌐 Getting your deployment URL..."
railway domain

echo ""
echo "🎉 Deployment complete!"
echo "Your CDS System is now live on Railway!"
echo ""
echo "📚 Next steps:"
echo "1. Visit your deployment URL"
echo "2. Test the /health endpoint"
echo "3. Check the /docs for API documentation"
echo "4. Monitor logs with: railway logs"
