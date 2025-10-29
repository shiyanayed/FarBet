# Execution Guide - How to Run the Farcaster Prediction Market

## 🎯 Quick Start (Choose One Method)

### Method 1: Direct Python Execution (Windows)

```powershell
# 1. Navigate to project directory
cd c:\Users\HP\Desktop\Python

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
.\venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file and configure
Copy-Item .env.example .env
notepad .env  # Edit with your API keys

# 6. Initialize database
python -c "from project import app; from database import init_db; app_context = app.app_context(); app_context.push(); init_db(app)"

# 7. Run the application
python main.py
```

Server will start at: **http://localhost:5000**

---

### Method 2: Docker Execution

```powershell
# 1. Navigate to project directory
cd c:\Users\HP\Desktop\Python

# 2. Create .env file
Copy-Item .env.example .env
# Edit .env with your configuration

# 3. Build Docker image
docker build -t prediction-market:latest .

# 4. Run container
docker run -p 5000:5000 --env-file .env prediction-market:latest

# Or use Docker Compose for full stack
docker-compose up
```

Server will start at: **http://localhost:5000**

---

### Method 3: Docker Compose (Full Stack)

```powershell
# 1. Navigate to project directory
cd c:\Users\HP\Desktop\Python

# 2. Create .env file
Copy-Item .env.example .env

# 3. Start all services
docker-compose up -d

# 4. Check status
docker-compose logs -f web

# 5. Stop services
docker-compose down
```

Services running:
- Flask API: http://localhost:5000
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- Nginx: http://localhost:80

---

## 📋 Prerequisites

### Minimum Requirements
- Python 3.9+ (for direct execution)
- pip (Python package manager)
- 2GB RAM
- 500MB disk space

### For Full Stack (Docker)
- Docker Desktop (https://www.docker.com/products/docker-desktop)
- Docker Compose (included with Docker Desktop)
- Same hardware as above

### API Keys Required
- Neynar API Key (https://neynar.com)
- Alchemy RPC URL (https://alchemy.com)
- Private Key from Ethereum wallet
- (Optional) Stripe/Coinbase for payments

---

## 🔧 Configuration

### Create .env File

```bash
# Copy template
cp .env.example .env

# Edit with your settings
```

### Required Environment Variables

```env
# Farcaster
NEYNAR_API_KEY=your_neynar_key_here
FARCASTER_HUB_URL=https://hub.farcaster.builders

# Blockchain
ALCHEMY_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/your-key
CHAIN_ID=1
PRIVATE_KEY=0x...your_wallet_private_key

# Contracts
USDC_CONTRACT=0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
TREASURE_WALLET=0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC

# Flask
SECRET_KEY=your-random-secret-key-here
FLASK_ENV=development
```

---

## 🧪 Testing the Application

### Health Check

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}
```

### Get Markets

```bash
curl http://localhost:5000/api/markets
```

### Create a Market

```bash
curl -X POST http://localhost:5000/api/markets/create \
  -H "Content-Type: application/json" \
  -d '{
    "user_fid": 3,
    "market_type": "casts_count",
    "threshold": 5,
    "direction": "over",
    "duration_hours": 24
  }'
```

### Access Farcaster Frames

- Markets Frame: http://localhost:5000/frame/markets
- Place Bet: http://localhost:5000/frame/place-bet
- My Bets: http://localhost:5000/frame/my-bets
- Profile: http://localhost:5000/frame/profile
- Withdraw: http://localhost:5000/frame/withdraw

---

## 🚀 Running Unit Tests

### Run All Tests

```powershell
# Install pytest
pip install pytest pytest-cov

# Run all tests
python -m pytest test_api.py -v

# Run with coverage report
python -m pytest test_api.py --cov=. -v

# Run specific test class
python -m pytest test_api.py::TestBetting -v

# Run specific test
python -m pytest test_api.py::TestBetting::test_place_bet -v
```

---

## 📊 Database Management

### Initialize Database

```powershell
python -c "from project import app; from database import init_db; app.app_context().push(); init_db(app)"
```

### Reset Database (WARNING: Clears all data)

```powershell
# Delete database file
Remove-Item prediction_market.db

# Reinitialize
python -c "from project import app; from database import init_db; app.app_context().push(); init_db(app)"
```

### Access Database (SQLite)

```powershell
# Install sqlite3 CLI
# Then run:
sqlite3 prediction_market.db

# Common queries:
sqlite> SELECT * FROM user_profiles;
sqlite> SELECT * FROM market_events;
sqlite> SELECT * FROM bets;
sqlite> .exit
```

---

## 🔍 Debugging

### Enable Debug Mode

In `.env`:
```env
FLASK_DEBUG=True
```

Then run with Python:
```powershell
python main.py
```

### View Logs

```powershell
# Last 50 lines
Get-Content -Tail 50 prediction_market.log

# Follow logs in real-time
Get-Content -Path prediction_market.log -Wait
```

### Check Running Processes

```powershell
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill process on port 5000 (if needed)
taskkill /PID <PID> /F
```

---

## 🐳 Docker Commands Reference

### Build Image

```bash
docker build -t prediction-market:latest .
docker build -t prediction-market:v1.0 .
```

### Run Container

```bash
# Basic run
docker run -p 5000:5000 prediction-market:latest

# With environment file
docker run -p 5000:5000 --env-file .env prediction-market:latest

# Detached mode
docker run -d -p 5000:5000 --env-file .env prediction-market:latest

# With volume mount
docker run -p 5000:5000 -v $(pwd):/app prediction-market:latest
```

### Docker Compose Commands

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Scale services
docker-compose up -d --scale web=3
```

### Docker Cleanup

```bash
# Remove unused images
docker image prune

# Remove unused containers
docker container prune

# Remove everything
docker system prune -a
```

---

## 📈 Performance Tips

### Optimize for Development

```env
FLASK_ENV=development
FLASK_DEBUG=True
CACHE_TYPE=simple
SQLALCHEMY_ECHO=False
```

### Optimize for Production

```env
FLASK_ENV=production
FLASK_DEBUG=False
CACHE_TYPE=redis
DATABASE_URL=postgresql://user:pass@localhost/market
```

### Enable Caching

```python
# In config.py
CACHE_ENABLED = True
CACHE_TTL_SECONDS = 300
```

---

## 🆘 Troubleshooting

### Import Errors

```powershell
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Clear pip cache
pip cache purge
```

### Port Already in Use

```powershell
# Check what's using port 5000
netstat -ano | findstr :5000

# Kill the process
taskkill /PID <PID> /F

# Or use different port
$env:FLASK_PORT = 5001
python main.py
```

### Database Errors

```powershell
# Reset database
Remove-Item prediction_market.db
python -c "from project import app; from database import init_db; app.app_context().push(); init_db(app)"
```

### Missing API Keys

```powershell
# Check .env file
cat .env

# Verify keys are set
$env:NEYNAR_API_KEY
```

### Connection Errors

```powershell
# Check if services are running
docker ps

# Check logs
docker-compose logs web
docker-compose logs db

# Restart services
docker-compose restart
```

---

## 📱 Testing with Farcaster

### Setup Warpcast for Testing

1. Download Warpcast app or use Web version
2. Create test account
3. Navigate to frame URL: `http://your-server/frame/markets`
4. Interact with the frame

### Local Testing

- Add `http://localhost:5000/frame/markets` in Warpcast
- Test frame interactions
- Check browser console for errors

---

## 🔐 Security Checklist Before Production

- [ ] Change SECRET_KEY to random value
- [ ] Use strong database password
- [ ] Enable HTTPS/SSL
- [ ] Set FLASK_ENV=production
- [ ] Update CORS origins
- [ ] Secure private key storage
- [ ] Enable rate limiting
- [ ] Setup monitoring/logging
- [ ] Review all environment variables
- [ ] Test with real wallets

---

## 📊 Monitoring

### Setup Basic Monitoring

```powershell
# Install Sentry
pip install sentry-sdk[flask]

# Configure in main.py
import sentry_sdk
sentry_sdk.init("your-sentry-dsn")
```

### View Metrics

```bash
# Check API response times
curl -w "@curl-format.txt" http://localhost:5000/api/markets

# Monitor system resources
docker stats

# Check database queries
sqlite3 prediction_market.db "SELECT * FROM sqlite_master WHERE type='table';"
```

---

## 🚢 Deployment

### To Production

1. **Prepare server**
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

2. **Setup domain**
   ```bash
   # Point domain to server IP
   A record: your-domain.com → server-ip
   ```

3. **Enable SSL**
   ```bash
   docker exec nginx certbot renew
   ```

4. **Verify**
   ```bash
   curl https://your-domain.com/health
   ```

---

## 📞 Support

If you encounter issues:

1. **Check logs**: `docker-compose logs web`
2. **Review config**: Check `.env` file settings
3. **Test endpoints**: Use curl or Postman
4. **Read documentation**: Check README.md or API_DOCUMENTATION.md
5. **GitHub Issues**: Report bugs on GitHub

---

## 🎉 Success!

Your Farcaster Prediction Market is ready to:
- ✅ Accept bets from Farcaster users
- ✅ Process payments from verified wallets
- ✅ Settle markets and calculate payouts
- ✅ Handle withdrawals with fees
- ✅ Provide interactive Frames UI

**Start with:**
```powershell
python main.py
```

**Access at:**
```
http://localhost:5000
```

**Good luck! 🚀**