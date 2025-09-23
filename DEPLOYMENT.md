# CDS System - Cloud Deployment Guide

## 🚀 Deployment Options

### 1. **Railway** (Recommended - Easiest)

### 2. **Render** (Free Tier Available)

### 3. **DigitalOcean App Platform**

### 4. **AWS ECS/Fargate**

### 5. **Google Cloud Run**

---

## 🚂 **Option 1: Railway (Easiest)**

### Setup Steps:

1. **Install Railway CLI**:

   ```bash
   npm install -g @railway/cli
   railway login
   ```

2. **Deploy**:

   ```bash
   railway init
   railway up
   ```

3. **Set Environment Variables**:
   ```bash
   railway variables set OPENAI_API_KEY=your_key_here
   railway variables set PINECONE_API_KEY=your_key_here
   railway variables set PINECONE_INDEX_NAME=medical-knowledge
   ```

### Railway Configuration:

- **Auto-deploys** from GitHub
- **Built-in PostgreSQL** database
- **Custom domains** available
- **Free tier** with usage limits

---

## 🎨 **Option 2: Render**

### Setup Steps:

1. **Connect GitHub** repository to Render
2. **Create Web Service**:

   - Build Command: `cd frontend && npm install && npm run build`
   - Start Command: `cd backend && pip install -r requirements-prod.txt && gunicorn main_prod:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
   - Environment: Python 3.13

3. **Add Environment Variables**:
   - `OPENAI_API_KEY`
   - `PINECONE_API_KEY`
   - `PINECONE_INDEX_NAME`

### Render Features:

- **Free tier** available
- **Auto-deploy** from Git
- **Custom domains**
- **Built-in monitoring**

---

## 🌊 **Option 3: DigitalOcean App Platform**

### Setup Steps:

1. **Create App** in DigitalOcean dashboard
2. **Connect GitHub** repository
3. **Configure Build**:

   - Source: `/`
   - Build Command: `cd frontend && npm install && npm run build`
   - Run Command: `cd backend && pip install -r requirements-prod.txt && gunicorn main_prod:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

4. **Add Environment Variables**:
   - `OPENAI_API_KEY`
   - `PINECONE_API_KEY`
   - `PINECONE_INDEX_NAME`

---

## ☁️ **Option 4: AWS ECS/Fargate**

### Setup Steps:

1. **Push to ECR**:

   ```bash
   aws ecr create-repository --repository-name cds-system
   docker tag cds-system-cds-backend:latest your-account.dkr.ecr.region.amazonaws.com/cds-system:latest
   docker push your-account.dkr.ecr.region.amazonaws.com/cds-system:latest
   ```

2. **Create ECS Task Definition**:

   - CPU: 1 vCPU
   - Memory: 2 GB
   - Port: 8000

3. **Create ECS Service**:
   - Application Load Balancer
   - Auto-scaling enabled

---

## 🔧 **Option 5: Google Cloud Run**

### Setup Steps:

1. **Build and Push**:

   ```bash
   gcloud builds submit --tag gcr.io/PROJECT-ID/cds-system
   gcloud run deploy --image gcr.io/PROJECT-ID/cds-system --platform managed --region us-central1 --allow-unauthenticated
   ```

2. **Set Environment Variables**:
   ```bash
   gcloud run services update cds-system --set-env-vars="OPENAI_API_KEY=your_key,PINECONE_API_KEY=your_key"
   ```

---

## 📋 **Pre-Deployment Checklist**

### ✅ **Required Environment Variables**:

- `OPENAI_API_KEY` - Your OpenAI API key
- `PINECONE_API_KEY` - Your Pinecone API key
- `PINECONE_INDEX_NAME` - Your Pinecone index name
- `PINECONE_ENVIRONMENT` - Your Pinecone environment (optional)

### ✅ **Optional Environment Variables**:

- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - For JWT tokens (generate secure key)
- `DEBUG` - Set to `False` for production
- `HOST` - Set to `0.0.0.0` for containerized deployment
- `PORT` - Set to `8000` or use platform's `$PORT`

### ✅ **Security Considerations**:

- Use HTTPS in production
- Set secure `SECRET_KEY`
- Configure CORS properly
- Use environment variables for secrets
- Enable database encryption if using PostgreSQL

---

## 🚀 **Quick Start - Railway (Recommended)**

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login to Railway
railway login

# 3. Initialize project
railway init

# 4. Deploy
railway up

# 5. Set environment variables
railway variables set OPENAI_API_KEY=your_key_here
railway variables set PINECONE_API_KEY=your_key_here
railway variables set PINECONE_INDEX_NAME=medical-knowledge

# 6. Get your URL
railway domain
```

---

## 📊 **Cost Comparison**

| Platform     | Free Tier | Paid Starting | Best For         |
| ------------ | --------- | ------------- | ---------------- |
| Railway      | $5/month  | $5/month      | Quick deployment |
| Render       | Yes       | $7/month      | Static + API     |
| DigitalOcean | No        | $5/month      | Full control     |
| AWS          | No        | $10/month     | Enterprise       |
| Google Cloud | Yes       | $5/month      | Serverless       |

---

## 🔍 **Monitoring & Maintenance**

### Health Checks:

- **Endpoint**: `GET /health`
- **Response**: `{"status": "healthy"}`

### Logs:

- **Railway**: `railway logs`
- **Render**: Dashboard logs
- **DigitalOcean**: App Platform logs
- **AWS**: CloudWatch logs
- **Google Cloud**: Cloud Logging

### Updates:

- **Automatic**: Push to GitHub triggers rebuild
- **Manual**: Platform-specific CLI commands

---

## 🆘 **Troubleshooting**

### Common Issues:

1. **Build Failures**: Check Node.js version (20+)
2. **Port Issues**: Use `$PORT` environment variable
3. **CORS Errors**: Update allowed origins
4. **Database**: Ensure connection string is correct
5. **Memory**: Increase container memory if needed

### Debug Commands:

```bash
# Check logs
railway logs

# SSH into container
railway shell

# Check environment
railway variables
```
