# ⚡ Quick Start Guide

Get your Farcaster Prediction Market up and running in 10 minutes!

## Prerequisites

- Node.js 18+
- A wallet with Base Sepolia ETH for testing
- 5-10 minutes of time

## 1. Clone & Install (2 min)

```bash
# If you haven't already, clone the repo
git clone <your-repo-url>
cd farcaster-prediction-market

# Install dependencies
npm install
```

## 2. Set Up Environment (2 min)

```bash
# Copy example env
cp .env.example .env
```

Edit `.env` and add these MINIMUM required values:

```env
# Get testnet ETH from https://www.alchemy.com/faucets/base-sepolia
PRIVATE_KEY=your_wallet_private_key

# Your wallet address (where fees go)
FEE_COLLECTOR_ADDRESS=0xYourWalletAddress

# Get free API key from https://neynar.com
NEYNAR_API_KEY=your_neynar_api_key

# Random secret for oracle
CRON_SECRET=any_random_string_here
ORACLE_PRIVATE_KEY=another_wallet_private_key
```

## 3. Deploy Smart Contract (2 min)

```bash
# Compile contract
npm run compile

# Deploy to Base Sepolia testnet
npx hardhat run scripts/deploy.ts --network baseSepolia
```

Copy the deployed contract address from output:
```
PredictionMarket deployed to: 0x1234567890...
```

Add to `.env`:
```env
NEXT_PUBLIC_CONTRACT_ADDRESS=0x1234567890...
NEXT_PUBLIC_CHAIN_ID=84532
```

## 4. Run Development Server (1 min)

```bash
npm run dev
```

Visit http://localhost:3000

## 5. Place Your First Test Bet (3 min)

1. **Connect Wallet**
   - Click "Connect Wallet" button
   - Select your wallet (MetaMask, etc.)
   - Approve connection to Base Sepolia

2. **Place a Bet**
   - Click "Launch App"
   - Select bet type: "Cast Count"
   - Enter a Farcaster user ID (try: `3621`)
   - Set predicted value: `5`
   - Bet amount: `0.001` ETH
   - Click "Place Bet"
   - Approve transaction in wallet

3. **View Your Bet**
   - Click "My Bets" tab
   - See your active bet with countdown
   - Wait 24 hours for auto-resolution!

## 🎉 Done!

You now have a working prediction market!

## What's Next?

### For Testing
- Place multiple bets to test different scenarios
- Try different bet types (likes, replies, etc.)
- Test bet resolution after 24 hours
- Check fee collector receives fees

### For Production

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for:
- Deploying to Base Mainnet
- Deploying frontend to Vercel
- Setting up automated resolution
- Configuring Farcaster frames

## Common Issues

### "Insufficient funds"
- Get Base Sepolia ETH: https://www.alchemy.com/faucets/base-sepolia
- Need minimum 0.01 ETH for testing

### "Transaction failed"
- Check you're on Base Sepolia network
- Verify contract address is correct
- Try increasing gas limit

### "Neynar API error"
- Verify your API key is valid
- Check you haven't hit rate limit
- Try a different FID

### "Cannot connect wallet"
- Make sure you have MetaMask or compatible wallet
- Switch to Base Sepolia network
- Refresh page and try again

## Test Data

Use these Farcaster IDs for testing:
- **3621** (dwr.eth) - Farcaster founder, very active
- **2** (v) - varunsrin.eth, active user
- **99** - Another active user

## Development Tips

### Watch Contract Events
```bash
# In another terminal
npx hardhat node --fork https://sepolia.base.org
```

### Check Bet Status
```bash
curl http://localhost:3000/api/bets?betId=1
```

### Get User Stats
```bash
curl "http://localhost:3000/api/farcaster/stats?fid=3621"
```

### Manual Bet Resolution (after 24h)
```bash
curl -X POST http://localhost:3000/api/resolve \
  -H "Content-Type: application/json" \
  -d '{"secret": "your_cron_secret", "betId": 1}'
```

## Project Structure

```
farcaster-prediction-market/
├── contracts/          # Solidity smart contracts
│   └── PredictionMarket.sol
├── scripts/           # Deployment scripts
│   └── deploy.ts
├── app/               # Next.js application
│   ├── page.tsx       # Landing page
│   ├── app/           # Main app
│   └── api/           # API routes
│       ├── frame/     # Farcaster frame
│       ├── bets/      # Bet queries
│       ├── farcaster/ # FC stats
│       └── resolve/   # Bet resolution
├── lib/               # Utilities
└── hardhat.config.ts  # Hardhat config
```

## Helpful Commands

```bash
# Development
npm run dev              # Start dev server
npm run build           # Build for production
npm run start           # Start production server

# Smart Contracts
npm run compile         # Compile contracts
npm run deploy:sepolia  # Deploy to testnet
npm run deploy:base     # Deploy to mainnet

# Testing
npm test               # Run tests (if added)
npm run lint           # Lint code
```

## Need Help?

1. Check [README.md](./README.md) for detailed info
2. See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for production setup
3. Review [FEATURES.md](./FEATURES.md) for feature details
4. Check contract docs in [contracts/README.md](./contracts/README.md)

## Ready for Production?

When you're ready to deploy to mainnet:

1. Follow [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
2. Get Base mainnet ETH
3. Deploy contract to Base
4. Deploy frontend to Vercel
5. Set up automated resolution
6. Test with small amounts first
7. Announce on Farcaster! 🎯

Happy betting! 🚀
