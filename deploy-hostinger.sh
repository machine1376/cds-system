#!/bin/bash

# CDS System - Hostinger VPS Deployment Script
# This script automates the deployment process on Hostinger VPS

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root (use sudo)"
    exit 1
fi

print_status "Starting CDS System deployment on Hostinger VPS..."

# Update system
print_status "Updating system packages..."
apt update && apt upgrade -y

# Install required packages
print_status "Installing required packages..."
apt install -y curl wget git unzip software-properties-common apt-transport-https ca-certificates gnupg lsb-release

# Install Docker
print_status "Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    systemctl start docker
    systemctl enable docker
    print_success "Docker installed successfully"
else
    print_warning "Docker is already installed"
fi

# Install Docker Compose
print_status "Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    print_success "Docker Compose installed successfully"
else
    print_warning "Docker Compose is already installed"
fi

# Install Nginx
print_status "Installing Nginx..."
if ! command -v nginx &> /dev/null; then
    apt install -y nginx
    systemctl start nginx
    systemctl enable nginx
    print_success "Nginx installed successfully"
else
    print_warning "Nginx is already installed"
fi

# Install Certbot for SSL
print_status "Installing Certbot for SSL certificates..."
apt install -y certbot python3-certbot-nginx

# Create application directory
APP_DIR="/opt/cds-system"
print_status "Creating application directory at $APP_DIR..."
mkdir -p $APP_DIR
cd $APP_DIR

# Check if repository is already cloned
if [ ! -d ".git" ]; then
    print_status "Please clone your repository to $APP_DIR first:"
    print_warning "git clone https://github.com/your-username/cds-system.git ."
    print_warning "Then run this script again."
    exit 1
fi

# Create environment file template
print_status "Creating environment file template..."
cat > .env.template << EOF
# CDS System Environment Variables
# Copy this file to .env and fill in your actual values

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment

# Database Configuration
POSTGRES_PASSWORD=your_secure_password_here
DATABASE_URL=postgresql://cds_user:your_secure_password_here@postgres:5432/cds_system

# Application Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False
EOF

# Check if .env exists
if [ ! -f ".env" ]; then
    print_warning "Environment file not found. Creating from template..."
    cp .env.template .env
    print_warning "Please edit .env file with your actual API keys and configuration:"
    print_warning "nano .env"
    print_warning "Then run this script again."
    exit 1
fi

# Create Nginx configuration
print_status "Creating Nginx configuration..."
cat > /etc/nginx/sites-available/cds-system << EOF
server {
    listen 80;
    server_name _;  # Replace with your domain
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Health check endpoint
    location /health {
        proxy_pass http://localhost:8000/health;
        access_log off;
    }
}
EOF

# Enable the site
print_status "Enabling Nginx site..."
ln -sf /etc/nginx/sites-available/cds-system /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
print_status "Testing Nginx configuration..."
nginx -t

# Restart Nginx
print_status "Restarting Nginx..."
systemctl restart nginx

# Configure firewall
print_status "Configuring firewall..."
if command -v ufw &> /dev/null; then
    ufw --force enable
    ufw allow ssh
    ufw allow 80
    ufw allow 443
    ufw allow 8000
    print_success "Firewall configured"
else
    print_warning "UFW not available, please configure firewall manually"
fi

# Build and start Docker containers
print_status "Building and starting Docker containers..."
docker-compose down 2>/dev/null || true
docker-compose up -d --build

# Wait for services to start
print_status "Waiting for services to start..."
sleep 30

# Check if services are running
print_status "Checking service status..."
if docker-compose ps | grep -q "Up"; then
    print_success "Services are running!"
else
    print_error "Some services failed to start. Check logs:"
    docker-compose logs
    exit 1
fi

# Test application
print_status "Testing application..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_success "Application is responding!"
else
    print_warning "Application health check failed. Check logs:"
    docker-compose logs cds-backend
fi

# Create backup script
print_status "Creating backup script..."
cat > /opt/backup-cds.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups"
APP_DIR="/opt/cds-system"

mkdir -p $BACKUP_DIR

# Backup database
cd $APP_DIR
docker-compose exec -T postgres pg_dump -U cds_user cds_system > $BACKUP_DIR/db_backup_$DATE.sql

# Backup application data
tar -czf $BACKUP_DIR/app_data_$DATE.tar.gz ./data

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
EOF

chmod +x /opt/backup-cds.sh

# Create systemd service for auto-start
print_status "Creating systemd service..."
cat > /etc/systemd/system/cds-system.service << EOF
[Unit]
Description=CDS System Docker Compose
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$APP_DIR
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable cds-system.service

# Create monitoring script
print_status "Creating monitoring script..."
cat > /opt/monitor-cds.sh << 'EOF'
#!/bin/bash
APP_DIR="/opt/cds-system"
LOG_FILE="/var/log/cds-monitor.log"

cd $APP_DIR

# Check if containers are running
if ! docker-compose ps | grep -q "Up"; then
    echo "$(date): Containers not running, restarting..." >> $LOG_FILE
    docker-compose up -d
fi

# Check application health
if ! curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "$(date): Application health check failed" >> $LOG_FILE
    docker-compose restart cds-backend
fi
EOF

chmod +x /opt/monitor-cds.sh

# Add monitoring to crontab
print_status "Setting up monitoring..."
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/monitor-cds.sh") | crontab -

print_success "Deployment completed successfully!"
print_status "Next steps:"
echo "1. Update your domain DNS to point to this server's IP"
echo "2. Run: certbot --nginx -d your-domain.com"
echo "3. Access your application at: http://your-domain.com"
echo "4. Check logs: docker-compose logs -f"
echo "5. Monitor status: docker-compose ps"

print_status "Application is running on port 8000"
print_status "Nginx is configured as reverse proxy"
print_status "SSL certificate setup required for HTTPS"
print_status "Backup script created at: /opt/backup-cds.sh"
print_status "Monitoring script created at: /opt/monitor-cds.sh"

print_success "CDS System deployment completed! 🎉"
