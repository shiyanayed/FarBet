# ⚡ QUICK LAUNCH GUIDE - 30 MINUTES TO LIVE

**Goal**: Get your prediction market live in 30 minutes with minimal setup

---

## 🚀 FASTEST PATH: Use Heroku (5 minutes)

### Step 1: Create Heroku Account (2 minutes)
```bash
# Go to https://www.heroku.com/signup
# Sign up with email/password
# Verify email
```

### Step 2: Install Heroku CLI (2 minutes)
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
# Install and verify
heroku --version
```

### Step 3: Deploy Your Code (1 minute)
```bash
# In your project directory
cd c:\Users\HP\Desktop\Python

# Login
heroku login

# Create app
heroku create your-prediction-market

# Set up environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-super-secret-key-12345
heroku config:set NEYNAR_API_KEY=your-neynar-key
heroku config:set WALLET_PRIVATE_KEY=0xYourPrivateKeyHere
heroku config:set RPC_ENDPOINT=https://base.llamarpc.com

# Deploy
git push heroku main

# Done! Your app is live
heroku open
```

**Your URL**: `https://your-prediction-market.herokuapp.com`

---

## 💻 ALTERNATIVE: Use Railway (3 minutes)

### Step 1: Connect Repository
```bash
# Go to https://railway.app
# Click "New Project"
# Select "Deploy from GitHub"
# Authorize and select your repo
```

### Step 2: Add Environment Variables
```
In Railway Dashboard → Variables:
FLASK_ENV=production
SECRET_KEY=your-secret-key
NEYNAR_API_KEY=your-key
WALLET_PRIVATE_KEY=0x...
RPC_ENDPOINT=https://base.llamarpc.com
```

### Step 3: Deploy
```bash
# Click Deploy
# Railway auto-detects Flask and deploys
# Your URL appears in dashboard
```

---

## 🔧 CONFIGURE FOR PRODUCTION (10 minutes)

### 1. Update Treasure Wallet Address
**File**: `project.py` (line 25)
```python
TREASURE_WALLET = "0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC"  # ✅ Already configured!
```

### 2. Update Domain
**File**: `project.py`
```python
API_BASE_URL = "https://your-domain.com/api"
FRAME_URL = "https://your-domain.com/frame"
```

### 3. Setup Database (2 options)

**Option A: Use Heroku Postgres (Easiest)**
```bash
heroku addons:create heroku-postgresql:hobby-dev
# Heroku auto-sets DATABASE_URL
```

**Option B: Use External Database**
```bash
heroku config:set DATABASE_URL=postgresql://user:pass@host:5432/db
```

### 4. Fund Treasure Wallet
```bash
# Send 1-5 ETH to your treasure wallet:
# 0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC
# 
# This covers transaction fees for:
# - Sending fees to treasure wallet
# - Processing withdrawals
```

---

## ✅ TEST YOUR LIVE APP (5 minutes)

### Test 1: Check Health
```bash
curl https://your-prediction-market.herokuapp.com/api/health
# Expected: {"status": "ok"}
```

### Test 2: Create Market
```bash
curl -X POST https://your-prediction-market.herokuapp.com/api/markets/create \
  -H "Content-Type: application/json" \
  -d '{
    "user_fid": 1234,
    "market_type": "casts_count",
    "threshold": 10,
    "direction": "over",
    "duration_hours": 24
  }'
```

### Test 3: View Markets
```bash
curl https://your-prediction-market.herokuapp.com/api/markets
```

---

## 🌐 SETUP CUSTOM DOMAIN (5 minutes)

### Get Domain
1. Buy at GoDaddy, Namecheap, or similar ($10-15/year)
2. Get domain name: `predictions.yoursite.com`

### Connect to Heroku
```bash
heroku domains:add predictions.yoursite.com
# Heroku gives you DNS target

# Update DNS records at your registrar:
# Add CNAME: predictions.yoursite.com → your-app.herokuapp.com
```

### Verify
```bash
# Wait 5-10 minutes for DNS to propagate
curl https://predictions.yoursite.com/api/health
```

---

## 🎭 ADD TO FARCASTER (5 minutes)

### Step 1: Get Neynar API Key
```bash
# Go to https://app.neynar.com
# Create free account
# Generate API key
```

### Step 2: Create Signer
```bash
curl -X POST https://api.neynar.com/v2/farcaster/signer \
  -H "Content-Type: application/json" \
  -H "api_key: YOUR_NEYNAR_API_KEY" \
  -d '{
    "app_fid": YOUR_FID_HERE
  }'
```

### Step 3: Add Frame URL to Profile
```
Update your Farcaster profile bio:
"Check out Prediction Market: https://predictions.yoursite.com/frame"
```

---

## 📊 PRODUCTION CHECKLIST

```
DEPLOYMENT
✅ Code deployed to hosting
✅ Domain configured
✅ SSL certificate (auto with Heroku)
✅ Database connected
✅ Environment variables set

BLOCKCHAIN
✅ Treasure wallet configured
✅ Wallet funded with gas (1-5 ETH)
✅ RPC endpoint configured
✅ Private key secured

FARCASTER
✅ Signer created
✅ Frame URL added to profile
✅ NEYNAR_API_KEY configured

SECURITY
✅ Private keys in environment only
✅ API keys not in code
✅ CORS configured
✅ Rate limiting enabled

TESTING
✅ Health check passes
✅ Markets can be created
✅ Bets can be placed
✅ Fees are charged
✅ Withdrawals work
```

---

## 🎯 YOUR LIVE SYSTEM

### URLs
- **API**: `https://your-app.herokuapp.com/api/`
- **Health**: `https://your-app.herokuapp.com/api/health`
- **Markets**: `https://your-app.herokuapp.com/api/markets`
- **Frame**: `https://your-app.herokuapp.com/frame`

### Key Endpoints
```
POST /api/markets/create         - Create prediction market
POST /api/bets/place             - Place bet
POST /api/markets/{id}/settle    - Settle market
GET  /api/user/{fid}             - Get user profile
POST /api/withdrawals/request    - Request withdrawal
```

### Fee Structure
- **Base Fee**: $0.20 per bet (charged immediately)
- **Win Fee**: 1.5% on withdrawal amounts
- **All fees go to**: 0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC

---

## 🆘 TROUBLESHOOTING

### "502 Bad Gateway" Error
```bash
# Check logs
heroku logs --tail
# Usually means database isn't configured
# Run: heroku addons:create heroku-postgresql:hobby-dev
```

### "No module named 'flask'"
```bash
# Update requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push heroku main
```

### Transactions failing
```bash
# Check wallet balance
# Send more ETH to treasure wallet
# Minimum: 0.5 ETH for gas fees
```

### Farcaster frame not showing
```bash
# Verify URL is public and accessible
curl https://your-app.herokuapp.com/frame
# Should return frame JSON
```

---

## 📚 NEXT STEPS

1. **Monitor**: Watch for errors first 24 hours
   ```bash
   heroku logs --tail
   ```

2. **Share**: Tell your community about the market
   ```
   "Hey! Join the prediction market: https://your-app.herokuapp.com"
   ```

3. **Iterate**: Monitor usage and improve
   - Check analytics
   - Gather feedback
   - Add features

4. **Scale**: As you grow
   - Upgrade Heroku dyno
   - Add more features
   - Improve UI/UX

---

## 🎊 YOU'RE LIVE!

Your Farcaster Prediction Market is now **LIVE** and **ACCEPTING BETS**.

**First steps:**
1. Test the API endpoints
2. Create a test market
3. Place a test bet
4. Verify fees are collected

**Next:**
- Promote to your community
- Gather feedback
- Iterate and improve

---

**Need help?** Check: `PRODUCTION_DEPLOYMENT_GUIDE.md`

**Total time to launch**: ~30 minutes ✨