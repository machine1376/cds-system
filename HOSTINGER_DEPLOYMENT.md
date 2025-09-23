# CDS System - Hostinger VPS Deployment Guide

## 🚀 Overview

This guide will help you deploy your Clinical Decision Support (CDS) system to Hostinger VPS using Docker. The system includes a FastAPI backend with AI/ML capabilities and a React frontend.

## 📋 Prerequisites

- Hostinger VPS with Ubuntu 22.04 LTS or newer
- Root access to your VPS
- Domain name pointed to your VPS IP
- Required API keys (OpenAI, Pinecone)

## 🛠️ Method 1: Using Hostinger Docker Manager (Recommended)

### Step 1: Access Docker Manager

1. Log in to your Hostinger control panel
2. Navigate to your VPS dashboard
3. Click on "Docker Manager" in the left sidebar

### Step 2: Deploy with Docker Compose

1. **Create New Project**:

   - Project Name: `cds-system`
   - Choose "Docker Compose" deployment method

2. **Upload Docker Compose File**:

   ```yaml
   version: "3.8"

   services:
     cds-backend:
       build: .
       ports:
         - "8000:8000"
       environment:
         - HOST=0.0.0.0
         - PORT=8000
         - OPENAI_API_KEY=${OPENAI_API_KEY}
         - PINECONE_API_KEY=${PINECONE_API_KEY}
         - PINECONE_ENVIRONMENT=${PINECONE_ENVIRONMENT}
         - DATABASE_URL=${DATABASE_URL}
       volumes:
         - ./data:/app/data
       restart: unless-stopped
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
         interval: 30s
         timeout: 10s
         retries: 3

     postgres:
       image: postgres:15-alpine
       environment:
         - POSTGRES_DB=cds_system
         - POSTGRES_USER=cds_user
         - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
       volumes:
         - postgres_data:/var/lib/postgresql/data
       ports:
         - "5432:5432"
       restart: unless-stopped

   volumes:
     postgres_data:
   ```

3. **Set Environment Variables**:

   - `OPENAI_API_KEY`: Your OpenAI API key
   - `PINECONE_API_KEY`: Your Pinecone API key
   - `PINECONE_ENVIRONMENT`: Your Pinecone environment
   - `POSTGRES_PASSWORD`: Strong password for PostgreSQL
   - `DATABASE_URL`: `postgresql://cds_user:${POSTGRES_PASSWORD}@postgres:5432/cds_system`

4. **Deploy**: Click "Deploy" to start the deployment process

### Step 3: Configure Nginx (Optional but Recommended)

Create an Nginx configuration file:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🛠️ Method 2: Manual VPS Deployment

### Step 1: Connect to Your VPS

```bash
ssh root@your-vps-ip
```

### Step 2: Update System and Install Dependencies

```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Install Git
apt install git -y
```

### Step 3: Clone and Deploy Application

```bash
# Clone your repository
git clone https://github.com/your-username/cds-system.git
cd cds-system

# Create environment file
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment
POSTGRES_PASSWORD=your_secure_password_here
DATABASE_URL=postgresql://cds_user:your_secure_password_here@postgres:5432/cds_system
EOF

# Build and start containers
docker-compose up -d --build
```

### Step 4: Install and Configure Nginx

```bash
# Install Nginx
apt install nginx -y

# Create Nginx configuration
cat > /etc/nginx/sites-available/cds-system << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
ln -s /etc/nginx/sites-available/cds-system /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default

# Test and restart Nginx
nginx -t
systemctl restart nginx
systemctl enable nginx
```

### Step 5: Set Up SSL Certificate

```bash
# Install Certbot
apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
certbot --nginx -d your-domain.com

# Test auto-renewal
certbot renew --dry-run
```

## 🔧 Method 3: Using Dokploy (Advanced)

### Step 1: Deploy Dokploy

1. In Hostinger VPS dashboard, go to "Templates"
2. Find and deploy "Dokploy" template
3. Access Dokploy at `http://your-vps-ip:3000`

### Step 2: Create Project in Dokploy

1. Create new project: "CDS System"
2. Connect your Git repository
3. Configure build settings:
   - Build Command: `docker build -t cds-system .`
   - Start Command: `docker-compose up -d`

### Step 3: Configure Environment Variables

Set all required environment variables in Dokploy dashboard.

## 🔒 Security Configuration

### Firewall Setup

```bash
# Install UFW
apt install ufw -y

# Configure firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80
ufw allow 443
ufw allow 8000
ufw enable
```

### Database Security

```bash
# Secure PostgreSQL
sudo -u postgres psql
ALTER USER cds_user PASSWORD 'your_secure_password';
\q
```

## 📊 Monitoring and Maintenance

### Health Checks

```bash
# Check application status
curl http://localhost:8000/health

# Check container status
docker-compose ps

# View logs
docker-compose logs -f
```

### Backup Script

Create a backup script:

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
docker-compose exec postgres pg_dump -U cds_user cds_system > $BACKUP_DIR/db_backup_$DATE.sql

# Backup application data
tar -czf $BACKUP_DIR/app_data_$DATE.tar.gz ./data

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

### Automated Backups

```bash
# Add to crontab
crontab -e

# Add this line for daily backups at 2 AM
0 2 * * * /path/to/backup.sh
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**:

   ```bash
   sudo netstat -tulpn | grep :8000
   sudo kill -9 <PID>
   ```

2. **Docker Build Fails**:

   ```bash
   docker-compose down
   docker system prune -a
   docker-compose up -d --build
   ```

3. **Database Connection Issues**:

   ```bash
   docker-compose exec postgres psql -U cds_user -d cds_system
   ```

4. **SSL Certificate Issues**:
   ```bash
   certbot renew --force-renewal
   systemctl reload nginx
   ```

### Logs and Debugging

```bash
# Application logs
docker-compose logs cds-backend

# Database logs
docker-compose logs postgres

# Nginx logs
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
```

## 📈 Performance Optimization

### Resource Monitoring

```bash
# Install htop for monitoring
apt install htop -y

# Monitor resources
htop
```

### Docker Resource Limits

Update your `docker-compose.yml`:

```yaml
services:
  cds-backend:
    # ... existing configuration
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: "1.0"
        reservations:
          memory: 1G
          cpus: "0.5"
```

## 🎯 Success Checklist

- [ ] VPS is running Ubuntu 22.04 LTS
- [ ] Docker and Docker Compose are installed
- [ ] Application is deployed and running
- [ ] Domain is configured and pointing to VPS
- [ ] SSL certificate is installed and working
- [ ] Database is accessible and configured
- [ ] Environment variables are set correctly
- [ ] Firewall is configured properly
- [ ] Monitoring and backups are set up
- [ ] Application is accessible via HTTPS

## 📞 Support

If you encounter issues:

1. Check the logs using the commands above
2. Verify all environment variables are set correctly
3. Ensure your domain DNS is pointing to the correct IP
4. Check Hostinger VPS resource usage
5. Contact Hostinger support for VPS-specific issues

## 🔄 Updates and Maintenance

### Updating the Application

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### Monitoring Commands

```bash
# Check system resources
htop

# Check disk usage
df -h

# Check memory usage
free -h

# Check running processes
ps aux | grep docker
```

Your CDS system should now be successfully deployed on Hostinger VPS! 🎉
