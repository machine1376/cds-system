#!/bin/bash

# CDS System Production Startup Script

echo "🚀 Starting CDS System in Production Mode..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy env.template to .env and configure your environment variables."
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running!"
    echo "Please start Docker and try again."
    exit 1
fi

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ CDS System is running successfully!"
    echo "🌐 Frontend: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
    echo "💚 Health Check: http://localhost:8000/health"
else
    echo "❌ Error: Services failed to start properly"
    echo "Check logs with: docker-compose logs"
    exit 1
fi
