# 🚀 Quick Deploy Guide - CDS System

## ⚡ **Fastest Deployment (5 minutes)**

### **Option 1: Railway (Recommended)**

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login to Railway
railway login

# 3. Deploy (one command!)
./deploy.sh
```

**That's it!** Your app will be live in ~5 minutes.

---

## 🎯 **Step-by-Step Manual Deployment**

### **Step 1: Prepare Your Repository**

```bash
# Make sure your code is pushed to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main
```

### **Step 2: Choose Your Platform**

#### **🚂 Railway (Easiest)**

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Railway auto-detects Dockerfile
5. Add environment variables:
   - `OPENAI_API_KEY`
   - `PINECONE_API_KEY`
   - `PINECONE_INDEX_NAME=medical-knowledge`

#### **🎨 Render (Free Tier)**

1. Go to [render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect GitHub repository
4. Use these settings:
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Start Command**: `cd backend && pip install -r requirements-prod.txt && gunicorn main_prod:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
   - **Environment**: Python 3.13

#### **🌊 DigitalOcean App Platform**

1. Go to [cloud.digitalocean.com](https://cloud.digitalocean.com)
2. Click "Create" → "Apps"
3. Connect GitHub repository
4. Configure build settings (same as Render)

---

## 🔧 **Environment Variables Required**

| Variable              | Description           | Example             |
| --------------------- | --------------------- | ------------------- |
| `OPENAI_API_KEY`      | Your OpenAI API key   | `sk-proj-...`       |
| `PINECONE_API_KEY`    | Your Pinecone API key | `pcsk_...`          |
| `PINECONE_INDEX_NAME` | Pinecone index name   | `medical-knowledge` |
| `HOST`                | Server host           | `0.0.0.0`           |
| `PORT`                | Server port           | `8000` or `$PORT`   |

---

## ✅ **Deployment Checklist**

- [ ] Code pushed to GitHub
- [ ] Environment variables set
- [ ] Build successful
- [ ] Health check passing (`/health`)
- [ ] Frontend loading at root URL
- [ ] API docs accessible (`/docs`)

---

## 🧪 **Test Your Deployment**

```bash
# Test health endpoint
curl https://your-app.railway.app/health

# Test frontend
open https://your-app.railway.app

# Test API docs
open https://your-app.railway.app/docs
```

---

## 🆘 **Troubleshooting**

### **Build Fails**

- Check Node.js version (needs 20+)
- Verify all dependencies in requirements-prod.txt
- Check build logs in platform dashboard

### **App Won't Start**

- Verify start command is correct
- Check environment variables are set
- Ensure port is set to `$PORT` or `8000`

### **Frontend Not Loading**

- Verify static files are built
- Check main_prod.py has static file mounting
- Ensure build process completed successfully

---

## 📊 **Platform Comparison**

| Platform     | Setup Time | Free Tier | Ease       | Best For         |
| ------------ | ---------- | --------- | ---------- | ---------------- |
| Railway      | 2 min      | $5/month  | ⭐⭐⭐⭐⭐ | Quick deployment |
| Render       | 5 min      | Yes       | ⭐⭐⭐⭐   | Free hosting     |
| DigitalOcean | 10 min     | No        | ⭐⭐⭐     | Full control     |
| AWS          | 30 min     | No        | ⭐⭐       | Enterprise       |

---

## 🎉 **You're Live!**

Once deployed, your CDS System will be available at:

- **Frontend**: `https://your-app.railway.app`
- **API**: `https://your-app.railway.app/docs`
- **Health**: `https://your-app.railway.app/health`

**Congratulations!** Your Clinical Decision Support System is now running in the cloud! 🚀
