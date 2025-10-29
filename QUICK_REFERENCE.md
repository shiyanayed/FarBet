# 🚀 Farcaster Prediction Market - Quick Reference

## ⚡ Start Server

```bash
python main.py
```

**Access**: http://localhost:5000

---

## 📊 Prediction Types

| Type | Code | Metric | Betting |
|------|------|--------|---------|
| Casts | `casts_count` | Daily casts | Over/Under |
| Likes | `likes_total` | Daily likes | Over/Under |
| Engagement | `engagement_score` | Weighted score | Over/Under |

---

## 💰 Fees (ACTIVE ✅)

| Fee | Amount | When | Destination |
|-----|--------|------|-------------|
| Base | $0.20 | Bet placed | Treasure |
| Win | 1.5% | Withdrawal | Treasure |

**Treasure Wallet**: `0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC`

---

## 🔌 API Endpoints

### Markets
```
GET    /api/markets              Get all active markets
POST   /api/markets/create       Create new market
POST   /api/markets/<id>/settle  Settle market
```

### Bets
```
POST   /api/bets/place           Place a bet
GET    /api/bets/<id>            Get bet details
GET    /api/bets/user/<fid>      Get user's bets
```

### Users
```
GET    /api/users/<fid>          Get user profile
```

### Withdrawals
```
POST   /api/withdrawals/request           Request withdrawal
POST   /api/withdrawals/<id>/process      Process withdrawal
```

---

## 📱 Farcaster Frames

```
POST /frame/markets        Display active markets
POST /frame/create-market  Create market UI
POST /frame/place-bet      Betting interface
POST /frame/my-bets        View user's bets
POST /frame/withdraw       Withdrawal UI
```

---

## 💡 Example Workflow

### 1. Create Market
```json
POST /api/markets/create
{
  "user_fid": 1234,
  "market_type": "casts_count",
  "threshold": 5,
  "direction": "over",
  "duration_hours": 24
}
```

### 2. Place Bet
```json
POST /api/bets/place
{
  "market_id": 1,
  "user_fid": 5678,
  "prediction": "over",
  "amount": 10.0,
  "user_wallet": "0x1234..."
}
→ Total Charged: $10.20 ($10 + $0.20 fee)
```

### 3. Settle Market
```
POST /api/markets/1/settle
→ Determines winners
→ Calculates payouts
→ Charges 1.5% win fee on withdrawals
```

### 4. Withdraw
```json
POST /api/withdrawals/request
{
  "user_fid": 5678,
  "user_wallet": "0x1234...",
  "amount": 15.0
}
→ User Gets: $14.775 (15 - 1.5% fee = $0.225)
→ Treasure Gets: $0.225
```

---

## 🧪 Testing

```bash
# Full test suite
python test_prediction_market.py

# Quick test
python quick_test.py

# Complete demo
python demo_complete_workflow.py
```

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| **PREDICTION_MARKET_GUIDE.md** | Complete API guide |
| **FEE_STRUCTURE_VISUAL.md** | Visual fee flows |
| **IMPLEMENTATION_STATUS.md** | Full status report |
| **START_HERE.md** | Getting started |
| **README.md** | Project overview |

---

## 🔍 Health Check

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-29T00:51:48.123456"
}
```

---

## 📊 Database

- **Type**: SQLite
- **File**: `prediction_market.db`
- **Models**: UserProfile, MarketEvent, Bet, Withdrawal, Transaction

---

## 🔧 Configuration

**File**: `.env`

```env
FARCASTER_HUB_URL=https://hub.farcaster.builders
NEYNAR_API_KEY=your_key_here
DATABASE_URL=sqlite:///prediction_market.db
```

---

## 📈 Stats

| Metric | Value |
|--------|-------|
| Endpoints | 15+ |
| Prediction Types | 3 |
| Fee Types | 2 |
| Database Tables | 5 |
| Farcaster Frames | 5 |

---

## ✅ Status

- 🟢 **Server**: Running
- 🟢 **Database**: Connected
- 🟢 **Fees**: Active
- 🟢 **API**: Responsive
- 🟢 **Frames**: Ready

---

## 🎯 Example Bets

### Small Bet
- Amount: $5.00
- Fee: $0.20
- Total: $5.20

### Medium Bet
- Amount: $50.00
- Fee: $0.20
- Total: $50.20

### Large Bet
- Amount: $500.00
- Fee: $0.20
- Total: $500.20

### Win Withdrawal ($100)
- Amount: $100.00
- Win Fee: $1.50 (1.5%)
- User Gets: $98.50

---

## 🚨 Common Issues

### Server not responding
```bash
python main.py
```

### Database error
```bash
# Reset database
rm prediction_market.db
python main.py
```

### Missing API key
```bash
# Check .env file
cat .env
```

---

## 🔗 Quick Links

| Resource | Link |
|----------|------|
| **Farcaster Hub** | https://hub.farcaster.builders |
| **Neynar API** | https://api.neynar.com |
| **Documentation** | See markdown files |
| **GitHub** | [Your repo] |

---

## 📞 Support

1. Check logs: `prediction_market.log`
2. Run tests: `python test_prediction_market.py`
3. View docs: See markdown files
4. Debug: Enable DEBUG mode in config

---

## ⚙️ Advanced

### Enable Debug Logging
```python
# In main.py
app.run(debug=True)
```

### Change Port
```python
# In main.py
app.run(port=8080)
```

### Use PostgreSQL
```env
DATABASE_URL=postgresql://user:pass@localhost/prediction_market
```

---

## 📋 Checklist

- [ ] Server running on 0.0.0.0:5000
- [ ] Health check responding
- [ ] Markets can be created
- [ ] Bets can be placed
- [ ] Fees are collected
- [ ] User profiles accessible
- [ ] Withdrawals working
- [ ] Tests passing
- [ ] Documentation reviewed

---

## 🎓 Key Concepts

1. **Market**: A prediction about a user's activity
2. **Bet**: A user's wager on a market outcome
3. **Settlement**: Market result determination
4. **Payout**: Winnings calculation
5. **Withdrawal**: Cash-out of winnings
6. **Fee**: Revenue collected by treasure wallet

---

## 📊 Current Markets

```bash
curl http://localhost:5000/api/markets
```

---

## 👥 User Profile

```bash
curl http://localhost:5000/api/users/1234
```

---

## 🎲 Recent Bets

```bash
curl http://localhost:5000/api/bets/user/1234
```

---

**Last Updated**: October 29, 2025
**Status**: ✅ Production Ready
**Version**: 1.0.0

For detailed information: See markdown documentation files