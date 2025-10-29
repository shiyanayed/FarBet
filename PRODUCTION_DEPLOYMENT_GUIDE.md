# 🚀 FARCASTER PREDICTION MARKET - PRODUCTION DEPLOYMENT GUIDE

**Status**: Ready for Launch ✅

---

## 📋 TABLE OF CONTENTS
1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Setup](#environment-setup)
3. [Hosting Options](#hosting-options)
4. [Database Configuration](#database-configuration)
5. [Blockchain Configuration](#blockchain-configuration)
6. [Farcaster Frame Setup](#farcaster-frame-setup)
7. [API Deployment](#api-deployment)
8. [Testing in Production](#testing-in-production)
9. [Monitoring & Alerts](#monitoring--alerts)
10. [Launch Timeline](#launch-timeline)

---

## ✅ PRE-DEPLOYMENT CHECKLIST

### Technical Requirements
- [ ] Domain name purchased (e.g., `predictions.farcaster.app`)
- [ ] SSL certificate obtained (free via Let's Encrypt)
- [ ] Hosting provider selected
- [ ] Database provider selected
- [ ] Blockchain provider (RPC endpoint) selected
- [ ] Monitoring tools configured
- [ ] Backup strategy defined

### Farcaster Configuration
- [ ] Farcaster account created for the bot/app
- [ ] Signer registered for frame interactions
- [ ] Frame URL configured
- [ ] Webhook endpoints configured

### Security
- [ ] API keys secured (environment variables)
- [ ] Wallet private key secured (environment variables, NOT in code)
- [ ] CORS configured for production domain
- [ ] Input validation enabled
- [ ] Rate limiting configured
- [ ] Error logging setup

### Documentation
- [ ] User guide written
- [ ] API documentation complete
- [ ] Terms of Service drafted
- [ ] Privacy Policy written
- [ ] Help/support system setup

---

## 🔧 ENVIRONMENT SETUP

### 1. Create Production Environment Variables

**Create `.env.production` file:**
```bash
# Server Configuration
FLASK_ENV=production
FLASK_DEBUG=False
HOST=0.0.0.0
PORT=5000
SECRET_KEY=your-super-secret-key-here-min-32-chars

# Database Configuration
DATABASE_URL=postgresql://user:password@db-host:5432/prediction_market
# OR for MySQL: mysql+pymysql://user:password@db-host:3306/prediction_market

# Farcaster Configuration
FARCASTER_HUB_URL=https://hub.farcaster.builders
NEYNAR_API_KEY=your-neynar-api-key-here
FARCASTER_SIGNER_UUID=your-signer-uuid

# Blockchain Configuration
RPC_ENDPOINT=https://base.llamarpc.com
# OR: https://eth.llamarpc.com (for Ethereum)
# OR: https://arbitrum.llamarpc.com (for Arbitrum)

# Wallet Configuration
TREASURE_WALLET=0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC
WALLET_PRIVATE_KEY=your-private-key-here
# WARNING: Never commit this to Git!

# Fee Configuration
BASE_FEE=0.2
WIN_FEE_PERCENTAGE=1.5

# API Configuration
API_BASE_URL=https://your-domain.com/api
FRAME_URL=https://your-domain.com/frame

# Logging & Monitoring
LOG_LEVEL=INFO
SENTRY_DSN=your-sentry-dsn-for-error-tracking
```

### 2. Secure Your Private Key

**Never commit private key to Git!**

```bash
# Add to .gitignore
echo ".env.production" >> .gitignore
echo ".env.*.local" >> .gitignore
echo "*.key" >> .gitignore
```

**Store securely in production:**
- Use hosting provider's secrets management (recommended)
- Use AWS Secrets Manager
- Use Hashicorp Vault
- Use environment variables on hosting platform

---

## 🏠 HOSTING OPTIONS

### Option 1: Heroku (Easiest for Beginners) ⭐

**Pros**: Easy deployment, free tier available, auto-scaling
**Cons**: Limited free tier, can get expensive

**Setup Steps:**
```bash
# 1. Create Heroku account at https://www.heroku.com

# 2. Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# 3. Login to Heroku
heroku login

# 4. Create app
heroku create your-prediction-market

# 5. Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set DATABASE_URL=postgresql://...
heroku config:set WALLET_PRIVATE_KEY=your-key
# ... add all variables from .env.production

# 6. Create Procfile for Heroku
echo "web: gunicorn main:app" > Procfile

# 7. Deploy
git push heroku main

# 8. View logs
heroku logs --tail
```

### Option 2: Railway (Fast & Modern) ⭐⭐

**Pros**: Modern interface, easy GitHub integration, good pricing
**Cons**: Newer platform

**Setup Steps:**
```bash
# 1. Visit https://railway.app
# 2. Connect GitHub account
# 3. Create new project from GitHub repo
# 4. Railway auto-detects Flask and deploys
# 5. Add environment variables in Railway dashboard
# 6. Auto-deploy on push to main
```

### Option 3: AWS (EC2 + RDS) (Most Control)

**Pros**: Scalable, industry standard, good pricing
**Cons**: More complex setup

**Setup Steps:**
```
1. Create EC2 instance (Ubuntu 22.04 recommended)
2. Create RDS database (PostgreSQL recommended)
3. SSH into EC2 and clone repo
4. Install dependencies: pip install -r requirements.txt
5. Install gunicorn: pip install gunicorn
6. Run with gunicorn: gunicorn -w 4 -b 0.0.0.0:5000 main:app
7. Use systemd or supervisor to keep service running
8. Setup Nginx as reverse proxy
9. Setup SSL certificate with Let's Encrypt
```

### Option 4: DigitalOcean (Balanced) ⭐⭐⭐

**Pros**: Good pricing, easy deployment, managed databases available
**Cons**: Less automated than Heroku

**Setup Steps:**
```
1. Create Droplet (Ubuntu 22.04, $6/month)
2. Create managed PostgreSQL database
3. SSH into droplet
4. Clone repository
5. Install Python and dependencies
6. Setup Gunicorn + Nginx
7. Configure SSL with Let's Encrypt
8. Setup auto-deploy from GitHub
```

### Option 5: Google Cloud Run (Serverless)

**Pros**: Serverless, auto-scaling, pay per request
**Cons**: Not ideal for persistent connections

**Setup Steps:**
```
1. Create Google Cloud project
2. Create Cloud SQL instance (PostgreSQL)
3. Containerize app with Docker (Dockerfile provided below)
4. Push to Cloud Registry
5. Deploy to Cloud Run
6. Configure environment variables
```

---

## 💾 DATABASE CONFIGURATION

### Option 1: PostgreSQL (Recommended for Production) ⭐

**Setup:**
```bash
# Local development
psql -U postgres -c "CREATE DATABASE prediction_market;"

# Production (managed service)
# Use Railway, Heroku, AWS RDS, or DigitalOcean's managed PostgreSQL

# Update connection string:
DATABASE_URL=postgresql://user:password@host:5432/prediction_market
```

**Update in project.py:**
```python
# Change from SQLite to PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/prediction_market')
```

### Option 2: MySQL (Alternative)

```bash
DATABASE_URL=mysql+pymysql://user:password@host:3306/prediction_market
```

### Database Migrations

**Create migration script:**
```bash
# Install alembic
pip install alembic

# Initialize migrations
alembic init migrations

# Create initial migration
alembic revision --autogenerate -m "initial_schema"

# Run migrations in production
alembic upgrade head
```

### Backup Strategy

```bash
# PostgreSQL backup
pg_dump prediction_market > backup_$(date +%Y%m%d).sql

# Setup automated daily backups
# Most hosting providers offer this in dashboard
```

---

## ⛓️ BLOCKCHAIN CONFIGURATION

### 1. Choose Network

**Base (Recommended for Farcaster)** - Built on Optimism
```
RPC Endpoint: https://base.llamarpc.com
Chain ID: 8453
Network: Mainnet
```

**Ethereum Mainnet** - Most secure, most expensive
```
RPC Endpoint: https://eth.llamarpc.com
Chain ID: 1
Network: Mainnet
```

**Arbitrum** - Lower fees, good for testing
```
RPC Endpoint: https://arbitrum.llamarpc.com
Chain ID: 42161
Network: Mainnet
```

### 2. Fund Treasure Wallet

**Treasure Wallet Address**: `0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC`

```bash
# Add funds to cover transaction fees
# Recommended: 1-5 ETH or equivalent on Base/Arbitrum

# Check balance:
# https://basescan.org/address/0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC
```

### 3. Setup RPC Provider (Optional: Better Reliability)

**Recommended RPC providers:**
- Alchemy: https://www.alchemy.com (free tier available)
- Infura: https://infura.io (free tier available)
- Ankr: https://www.ankr.com (free endpoint)

```python
# Update blockchain.py
RPC_ENDPOINT = os.getenv('RPC_ENDPOINT', 'https://base.llamarpc.com')
```

### 4. Test Transaction

```python
# Run test transaction
from blockchain import TransactionHandler

tx_handler = TransactionHandler()
result = tx_handler.send_transaction(
    to_address='0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC',
    amount=0.001,
    description='Test transaction'
)
print(result)
```

---

## 🎭 FARCASTER FRAME SETUP

### 1. Create Farcaster Signer

**Via Neynar API:**
```bash
curl -X POST https://api.neynar.com/v2/farcaster/signer \
  -H "Content-Type: application/json" \
  -H "api_key: YOUR_NEYNAR_API_KEY" \
  -d '{
    "signer_uuid": "unique-id",
    "app_fid": YOUR_APP_FID
  }'
```

### 2. Configure Frame URL

**In project.py:**
```python
FRAME_URL = os.getenv('FRAME_URL', 'https://your-domain.com/frame')
```

**Create frame endpoint:**
```python
@app.route('/frame', methods=['GET', 'POST'])
def prediction_frame():
    """Farcaster frame for prediction market"""
    return {
        "version": "vNext",
        "image": "https://your-domain.com/preview.png",
        "buttons": [
            {"label": "View Markets"},
            {"label": "Place Bet"},
            {"label": "My Bets"}
        ]
    }
```

### 3. Add Frame to Farcaster Profile

Update your Farcaster profile bio with frame URL:
```
Check out the Prediction Market: https://your-domain.com/frame
```

---

## 🚀 API DEPLOYMENT

### Option A: Docker Deployment (Recommended)

**Create Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=main.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
```

**Create docker-compose.yml:**
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:5000"
    environment:
      DATABASE_URL: postgresql://user:password@db:5432/prediction_market
      FLASK_ENV: production
      WALLET_PRIVATE_KEY: ${WALLET_PRIVATE_KEY}
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: prediction_market
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - pgdata:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  pgdata:
```

**Deploy:**
```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f api
```

### Option B: Direct Server Deployment

**1. Install dependencies:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip postgresql nginx

pip3 install -r requirements.txt
pip3 install gunicorn
```

**2. Create systemd service:**
```bash
sudo tee /etc/systemd/system/prediction-market.service > /dev/null <<EOF
[Unit]
Description=Farcaster Prediction Market
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/prediction-market
Environment="PATH=/var/www/prediction-market/venv/bin"
ExecStart=/var/www/prediction-market/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```

**3. Start service:**
```bash
sudo systemctl daemon-reload
sudo systemctl start prediction-market
sudo systemctl enable prediction-market
```

**4. Setup Nginx reverse proxy:**
```bash
sudo tee /etc/nginx/sites-available/prediction-market > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
```

**5. Enable Nginx config:**
```bash
sudo ln -s /etc/nginx/sites-available/prediction-market /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**6. Setup SSL (Let's Encrypt):**
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 🧪 TESTING IN PRODUCTION

### 1. Health Check

```bash
curl https://your-domain.com/api/health
# Expected: {"status": "ok", "database": "connected"}
```

### 2. Create Test Market

```bash
curl -X POST https://your-domain.com/api/markets/create \
  -H "Content-Type: application/json" \
  -d '{
    "user_fid": 1234,
    "market_type": "casts_count",
    "threshold": 10,
    "direction": "over",
    "duration_hours": 24
  }'
```

### 3. Test Betting

```bash
curl -X POST https://your-domain.com/api/bets/place \
  -H "Content-Type: application/json" \
  -d '{
    "market_id": 1,
    "user_fid": 1234,
    "prediction": "yes",
    "amount": 10.0,
    "user_wallet": "0x123..."
  }'
```

### 4. Verify Fee Collection

```bash
# Check treasure wallet balance
https://basescan.org/address/0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC
```

---

## 📊 MONITORING & ALERTS

### 1. Setup Error Tracking (Sentry)

```bash
# Install
pip install sentry-sdk

# Add to main.py
import sentry_sdk
sentry_sdk.init("https://your-sentry-dsn@sentry.io/PROJECT_ID")
```

### 2. Setup Logging

**Update config.py:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### 3. Monitor Key Metrics

```python
# Database connection checks
# API response times
# Error rates
# Transaction success rates
# Wallet balance
# Fee collection amounts
```

### 4. Setup Alerts

**Email alerts for:**
- API downtime (uptime monitoring via Uptime Robot)
- High error rates (via Sentry)
- Low wallet balance (custom script)
- Database issues (hosting provider alerts)

---

## 📅 LAUNCH TIMELINE

### Week 1: Pre-Launch
- [ ] Day 1-2: Setup hosting account, domain, SSL
- [ ] Day 3: Configure production database
- [ ] Day 4: Configure blockchain and wallet
- [ ] Day 5: Deploy to staging environment
- [ ] Day 6-7: Full staging testing

### Week 2: Launch
- [ ] Day 1-2: Final production setup
- [ ] Day 3: Deploy to production
- [ ] Day 4-5: Monitor closely, fix any issues
- [ ] Day 6-7: Soft launch to internal testers

### Week 3+: Post-Launch
- [ ] Monitor metrics
- [ ] Gather user feedback
- [ ] Fix bugs
- [ ] Plan features
- [ ] Scale as needed

---

## 🎯 PRODUCTION CHECKLIST

### Before Going Live

```
TECHNICAL
- [ ] Staging environment matches production
- [ ] All tests pass
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Backups configured
- [ ] Monitoring setup
- [ ] Error tracking enabled
- [ ] SSL certificate installed
- [ ] Wallet funded with gas
- [ ] Rate limiting enabled
- [ ] CORS configured for production

FARCASTER
- [ ] Signer registered
- [ ] Frame URL configured
- [ ] Frame tested in Farcaster
- [ ] Bot account ready

SECURITY
- [ ] Private keys not in code
- [ ] API keys secured
- [ ] Input validation enabled
- [ ] Rate limiting configured
- [ ] CORS whitelisted
- [ ] SQL injection protection enabled

DOCUMENTATION
- [ ] API documentation complete
- [ ] User guide written
- [ ] Terms of Service ready
- [ ] Privacy Policy ready
- [ ] Support system in place

BUSINESS
- [ ] Legal review complete
- [ ] Insurance considerations reviewed
- [ ] Marketing plan ready
- [ ] Support plan ready
```

---

## 🆘 TROUBLESHOOTING

### Issue: "Connection refused" from Farcaster API
**Solution**: Check NEYNAR_API_KEY is correct and network is accessible

### Issue: Wallet transactions failing
**Solution**: Check if treasure wallet has enough gas; fund with 1-5 ETH

### Issue: Database connection error
**Solution**: Verify DATABASE_URL is correct and database is running

### Issue: Frame not appearing in Farcaster
**Solution**: Check frame URL is publicly accessible; verify signer UUID

### Issue: High error rates
**Solution**: Check logs in Sentry; review database performance; check API rate limits

---

## 📞 SUPPORT

- Documentation: See all `.md` files in repo
- Issues: Check TROUBLESHOOTING.md
- API Docs: See PREDICTION_MARKET_GUIDE.md
- Code Issues: Check comments in source code

---

## ✨ NEXT STEPS

1. **Choose hosting** (Heroku recommended for beginners)
2. **Configure environment variables**
3. **Deploy to staging**
4. **Run full test suite**
5. **Deploy to production**
6. **Monitor first 24 hours closely**
7. **Launch announcement**

**You're ready to go live! 🚀**