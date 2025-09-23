# CDS System - Production Build Guide

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# 1. Configure environment
cp env.template .env
# Edit .env with your API keys

# 2. Start production build
./start-production.sh
```

### Option 2: Manual Build

```bash
# 1. Build frontend
cd frontend
npm run build

# 2. Install backend dependencies
cd ../backend
pip install -r ../requirements-prod.txt

# 3. Start backend with static files
cd ..
python -m backend.main
```

## 📁 Build Outputs

### Frontend Build

- **Location**: `frontend/dist/`
- **Files**:
  - `index.html` - Main HTML file
  - `assets/index-*.js` - Bundled JavaScript (307KB gzipped: 89KB)
  - `assets/index-*.css` - Bundled CSS (54KB gzipped: 8KB)

### Backend Production

- **Requirements**: `requirements-prod.txt`
- **Docker**: `Dockerfile` + `docker-compose.yml`
- **Static Files**: Served from `backend/static/`

## 🔧 Production Configuration

### Environment Variables

Copy `env.template` to `.env` and configure:

```bash
# Required
OPENAI_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
PINECONE_ENVIRONMENT=your_env_here

# Optional
DATABASE_URL=postgresql://user:pass@localhost:5432/cds
POSTGRES_PASSWORD=secure_password
```

### Docker Services

- **cds-backend**: Main application (port 8000)
- **postgres**: Database (port 5432, optional)

## 📊 Build Statistics

### Frontend Bundle Analysis

- **Total Size**: 361.45 KB
- **Gzipped**: 97.75 KB
- **Build Time**: ~2 seconds
- **Modules**: 1,725 transformed

### Performance Optimizations

- ✅ Code splitting
- ✅ Tree shaking
- ✅ Gzip compression
- ✅ Asset optimization
- ✅ CSS minification

## 🚀 Deployment Options

### 1. Docker Compose (Local/Server)

```bash
docker-compose up -d
```

### 2. Docker Image (Cloud)

```bash
docker build -t cds-system .
docker run -p 8000:8000 --env-file .env cds-system
```

### 3. Manual Deployment

1. Build frontend: `npm run build`
2. Copy `dist/` to web server
3. Deploy backend with `requirements-prod.txt`

## 🔍 Health Checks

- **API Health**: `GET /health`
- **Frontend**: `GET /` (serves built React app)
- **API Docs**: `GET /docs`

## 📝 Production Notes

- Frontend is served as static files from the backend
- CORS is configured for production domains
- Database is optional (can run without PostgreSQL)
- All API keys should be set via environment variables
- Use HTTPS in production for security

## 🛠️ Troubleshooting

### Build Issues

```bash
# Clear node modules and rebuild
rm -rf frontend/node_modules frontend/dist
cd frontend && npm install && npm run build
```

### Docker Issues

```bash
# Check logs
docker-compose logs

# Rebuild from scratch
docker-compose down
docker-compose up --build
```

### Port Conflicts

- Frontend: 3000-3002 (dev), 8000 (prod)
- Backend: 8000
- Database: 5432
