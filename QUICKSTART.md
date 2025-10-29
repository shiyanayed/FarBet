# Farcaster Prediction Market - Quick Start Guide

## 🚀 5-Minute Setup

### 1. Prerequisites
- Python 3.9+
- pip (Python package manager)
- Git

### 2. Clone & Setup
```bash
# Clone repository
git clone https://github.com/yourusername/farcaster-prediction-market.git
cd farcaster-prediction-market

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your settings
# Required:
# - NEYNAR_API_KEY: Get from https://neynar.com
# - ALCHEMY_RPC_URL: Get from https://alchemy.com
# - PRIVATE_KEY: Your wallet's private key (for fees)
```

### 4. Initialize Database
```bash
python -c "from project import app; from database import init_db; app_context = app.app_context(); app_context.push(); init_db(app)"
```

### 5. Run Server
```bash
python main.py
```

Server runs at: `http://localhost:5000`

## 📱 Testing with Farcaster Frames

### Access Frames
Once running, your frames are available at:
- `/frame/markets` - Browse all markets
- `/frame/create-market` - Create new market
- `/frame/place-bet` - Place a bet
- `/frame/my-bets` - View your bets
- `/frame/withdraw` - Withdraw winnings

### Test on Warpcast
1. Install Warpcast app or use Web client
2. Add frame URL: `your-server-url/frame/markets`
3. Interact with the frame!

## 💰 API Quick Test

### Get Markets
```bash
curl http://localhost:5000/api/markets
```

### Create Market
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

### Place Bet
```bash
curl -X POST http://localhost:5000/api/bets/place \
  -H "Content-Type: application/json" \
  -d '{
    "market_id": 1,
    "user_fid": 100,
    "prediction": "over",
    "amount": 10.0,
    "user_wallet": "0x742d35Cc6634C0532925a3b844Bc9e7595f42e24"
  }'
```

### Get Your Bets
```bash
curl http://localhost:5000/api/bets/user/100
```

## 🔧 Configuration Checklist

- [ ] NEYNAR_API_KEY configured
- [ ] ALCHEMY_RPC_URL configured
- [ ] PRIVATE_KEY set for fee wallet
- [ ] Database initialized
- [ ] Server running on port 5000

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "Database connection error"
```bash
# Reset database
rm prediction_market.db
python main.py
```

### "API key errors"
Check your `.env` file has correct keys from:
- Neynar: https://neynar.com/app/api-keys
- Alchemy: https://dashboard.alchemy.com

## 📚 Next Steps

1. **Deploy to Production**
   - Use Gunicorn: `gunicorn -w 4 main:app`
   - Deploy to Heroku/Railway/Vercel

2. **Setup Monitoring**
   - Add Sentry for error tracking
   - Setup analytics

3. **Customize Markets**
   - Modify market types in `project.py`
   - Adjust fee percentages in `config.py`

4. **Scale Database**
   - Migrate from SQLite to PostgreSQL
   - Setup Redis cache

## 📖 Learn More

- [Full Documentation](README.md)
- [API Reference](README.md#api-endpoints)
- [Database Schema](README.md#database-schema)
- [Farcaster Developer Docs](https://docs.farcaster.xyz/)

## 💬 Support

- **Discord**: [Join Community](https://discord.gg/your-invite)
- **GitHub Issues**: Report bugs here
- **Twitter**: [@YourHandle](https://twitter.com/yourhandle)

## 🎉 You're Ready!

Your Farcaster prediction market is now running. Start creating markets and placing bets!

---

**Questions?** Check the [FAQ](#faq) section or open an issue on GitHub.

## FAQ

**Q: How do users fund bets?**
A: Through their Farcaster verified wallet. No deposits needed!

**Q: What's the fee structure?**
A: $0.20 base fee + 1.5% on winnings at withdrawal.

**Q: How are markets settled?**
A: Automatically or manually by calling `/api/markets/<id>/settle`.

**Q: Can I customize market types?**
A: Yes! Edit the market types in `project.py` and `utils.py`.

**Q: How do I withdraw funds?**
A: Call `/api/withdrawals/request` endpoint or use the `/frame/withdraw` frame.