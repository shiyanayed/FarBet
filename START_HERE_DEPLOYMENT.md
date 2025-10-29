# 🚀 START HERE - DEPLOYMENT GUIDE

Welcome! This guide will help you deploy your Farcaster Prediction Market to production in the fastest way possible.

---

## 📊 DEPLOYMENT OPTIONS QUICK COMPARISON

| Option | Time | Difficulty | Cost | Best For |
|--------|------|-----------|------|----------|
| **Heroku** | 5 min | ⭐ Easy | $7-50/mo | Quick launch |
| **Railway** | 5 min | ⭐ Easy | $5-50/mo | Fast setup |
| **Docker** | 10 min | ⭐⭐ Medium | $5+/mo | Any host |
| **AWS** | 30 min | ⭐⭐⭐ Hard | $1-100+/mo | Scale |
| **Local** | 5 min | ⭐ Easy | $0 | Testing |

**RECOMMENDATION: Start with Heroku or Railway (5 minutes to live!)**

---

## ⚡ OPTION 1: HEROKU DEPLOYMENT (FASTEST)

### Prerequisites
- [Heroku account](https://www.heroku.com/signup) (free)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- Git installed

### 30-Second Setup

```bash
# 1. Login to Heroku
heroku login

# 2. Create app
heroku create your-prediction-market

# 3. Set environment variables
heroku config:set \
  FLASK_ENV=production \
  SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))') \
  NEYNAR_API_KEY=your_key \
  WALLET_PRIVATE_KEY=0xyourkey \
  RPC_ENDPOINT=https://base.llamarpc.com

# 4. Deploy
git push heroku main

# 5. Add database
heroku addons:create heroku-postgresql:hobby-dev

# 6. Done! Open app
heroku open

# 7. View logs (if needed)
heroku logs --tail
```

**Your URL**: `https://your-prediction-market.herokuapp.com`

**Cost**: Free to $50/month depending on traffic

---

## 🚄 OPTION 2: RAILWAY DEPLOYMENT (ALTERNATIVE)

### Prerequisites
- [Railway account](https://railway.app) (free)
- GitHub account
- Repository on GitHub

### 3-Minute Setup

```bash
# 1. Go to https://railway.app
# 2. Click "New Project"
# 3. Select "Deploy from GitHub"
# 4. Authorize GitHub
# 5. Select your repository
# 6. Railway auto-detects Flask
# 7. Add environment variables:
#    - FLASK_ENV=production
#    - NEYNAR_API_KEY=...
#    - WALLET_PRIVATE_KEY=...
#    - RPC_ENDPOINT=https://base.llamarpc.com
# 8. Deploy!
```

**Cost**: Free to $50/month

---

## 🐳 OPTION 3: DOCKER DEPLOYMENT (Most Flexible)

### Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop) installed
- Hosting account (DigitalOcean, AWS, etc.)

### Local Docker Testing

```bash
# 1. Create .env file from .env.example
cp .env.example .env

# 2. Edit .env with your values
# Important: Set WALLET_PRIVATE_KEY

# 3. Build image
docker build -t prediction-market .

# 4. Run with docker-compose
docker-compose up -d

# 5. Check if running
curl http://localhost:5000/api/health

# 6. View logs
docker-compose logs -f api

# 7. Stop
docker-compose down
```

### Deploy to Production (DigitalOcean)

```bash
# 1. Create DigitalOcean droplet ($6/month)
# 2. SSH into droplet
ssh root@your-droplet-ip

# 3. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 4. Clone your repo
git clone https://github.com/yourusername/prediction-market.git
cd prediction-market

# 5. Create .env in production
nano .env
# Add: WALLET_PRIVATE_KEY, NEYNAR_API_KEY, etc.

# 6. Deploy
docker-compose up -d

# 7. Setup SSL with Nginx
# (See PRODUCTION_DEPLOYMENT_GUIDE.md)
```

---

## 💻 OPTION 4: LOCAL DEPLOYMENT (Testing Only)

### Prerequisites
- Python 3.8+
- Git

### Quick Start

```bash
# 1. Clone and setup
git clone https://github.com/yourusername/prediction-market.git
cd prediction-market

# 2. Create virtual environment
python -m venv venv

# 3. Activate venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
cp .env.example .env
# Edit .env with your keys

# 6. Run server
python main.py

# 7. Test
curl http://localhost:5000/api/health

# 8. View app
# Open http://localhost:5000
```

---

## 🔑 CONFIGURE ENVIRONMENT VARIABLES

### Get Required Keys

**1. Neynar API Key** (Free)
```bash
# Go to https://app.neynar.com
# Sign up for free
# Generate API key
# Copy into NEYNAR_API_KEY
```

**2. Wallet Private Key**
```bash
# Use existing wallet or create new one
# Export private key from MetaMask, ethers.js, etc.
# Add to WALLET_PRIVATE_KEY in .env
# NEVER share this key!
```

**3. RPC Endpoint** (Free)
```bash
# Use public endpoint (included):
https://base.llamarpc.com  # Base network (recommended)

# OR get your own from (free tier available):
# - Alchemy: https://www.alchemy.com
# - Infura: https://infura.io
# - Ankr: https://www.ankr.com
```

### Set Variables

**Heroku:**
```bash
heroku config:set NEYNAR_API_KEY=your-key
heroku config:set WALLET_PRIVATE_KEY=0x...
```

**Railway:**
Dashboard → Project → Variables

**Docker:**
Edit `.env` file directly

**Local:**
Edit `.env` file

---

## 💰 FUND YOUR WALLET

Your treasure wallet needs funds to pay for transaction fees:

```bash
Treasure Wallet: 0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC

Recommended funding:
- Base network: 1-5 ETH (or equivalent)
- Ethereum: 0.5-2 ETH
- Arbitrum: 1-5 ETH

Check balance: https://basescan.org/address/0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC
```

---

## ✅ VERIFY DEPLOYMENT

After deployment, test these endpoints:

```bash
# 1. Health check
curl https://your-domain.com/api/health
# Expected: {"status": "ok"}

# 2. Get markets
curl https://your-domain.com/api/markets

# 3. Create market
curl -X POST https://your-domain.com/api/markets/create \
  -H "Content-Type: application/json" \
  -d '{
    "user_fid": 1234,
    "market_type": "casts_count",
    "threshold": 10,
    "direction": "over",
    "duration_hours": 24
  }'

# 4. Check treasure wallet
# Visit: https://basescan.org/address/0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC
```

---

## 🌐 ADD CUSTOM DOMAIN (Optional)

### Get Domain
1. Buy at GoDaddy, Namecheap, etc. ($10-15/year)
2. Example: `predictions.yoursite.com`

### For Heroku
```bash
heroku domains:add predictions.yoursite.com
# Get DNS target from output
# Update CNAME at registrar
# Wait 5-10 minutes
```

### For Railway
```bash
# Railway dashboard → Settings → Domains
# Add custom domain
# Update CNAME at registrar
```

### For Docker/DigitalOcean
```bash
# Update A record to droplet IP at registrar
# Setup SSL with certbot:
certbot --nginx -d predictions.yoursite.com
```

---

## 🎭 FARCASTER FRAME SETUP (Optional)

### 1. Create Signer
```bash
curl -X POST https://api.neynar.com/v2/farcaster/signer \
  -H "Content-Type: application/json" \
  -H "api_key: YOUR_NEYNAR_API_KEY" \
  -d '{
    "app_fid": YOUR_FID
  }'
```

### 2. Add to Profile
Update your Farcaster profile bio:
```
Check predictions: https://your-domain.com/frame
```

### 3. Test in Farcaster
- Open Farcaster client
- Visit your profile
- Click frame to test

---

## 🛠️ TROUBLESHOOTING

### "502 Bad Gateway"
```bash
# Usually means database not configured
# Heroku:
heroku addons:create heroku-postgresql:hobby-dev
# Railway: Add PostgreSQL database in dashboard
# Docker: Check docker-compose.yml, ensure db is running
```

### "Module not found" error
```bash
# Update requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Wallet transactions failing
```bash
# Check if treasure wallet has funds
# If not, send 1-5 ETH to:
0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC

# Verify on: https://basescan.org
```

### "Connection refused" from Farcaster
```bash
# Check NEYNAR_API_KEY is correct
# Verify network connectivity
# Check RPC endpoint is working
```

---

## 📊 MONITORING

### Check Logs

**Heroku:**
```bash
heroku logs --tail
```

**Railway:**
```bash
# Dashboard → Deployments → View Logs
```

**Docker:**
```bash
docker-compose logs -f api
```

### Monitor Metrics
- API response time: Should be <100ms
- Error rate: Should be <1%
- Wallet balance: Should be >0.5 ETH
- User signups: Track growth

---

## 🚀 POST-LAUNCH CHECKLIST

```
BEFORE LAUNCHING
✅ Deployment tested on staging
✅ All API endpoints verified
✅ Fee system tested
✅ Wallet funded with gas
✅ Monitoring configured
✅ Backup strategy in place

DURING LAUNCH
✅ Monitor logs closely
✅ Test bet placement
✅ Verify fee collection
✅ Check transaction success rate

AFTER LAUNCH
✅ Gather user feedback
✅ Monitor performance
✅ Plan improvements
✅ Scale as needed
```

---

## 📚 NEXT STEPS

1. **Choose deployment option** (Heroku recommended)
2. **Follow quick setup** above
3. **Configure environment variables**
4. **Fund treasure wallet**
5. **Test all endpoints**
6. **Add custom domain** (optional)
7. **Setup Farcaster frame** (optional)
8. **Launch & monitor**

---

## 🆘 NEED HELP?

| Question | Answer |
|----------|--------|
| Which deployment is fastest? | Heroku or Railway (5 minutes) |
| Which deployment is cheapest? | Local or Docker on DigitalOcean ($5-6/mo) |
| Which deployment is easiest? | Heroku (auto-everything) |
| How do I get my private key? | Export from MetaMask or ethers.js |
| How much money do I need upfront? | $0 for keys, $10-50 for hosting/domain |
| Can I test locally first? | Yes! Follow "Local" option above |

---

## ✨ You're Ready to Launch!

**Next action**: Choose deployment option and follow steps above.

**Typical timeline**:
- 5 min: Choose hosting
- 5-10 min: Deploy code
- 5 min: Configure environment
- 5 min: Test endpoints
- **Total: ~20 minutes to live!**

Good luck! 🚀