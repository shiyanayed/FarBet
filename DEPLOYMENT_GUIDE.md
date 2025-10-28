# 🚀 Deployment Guide

Complete step-by-step guide to deploy your Farcaster Prediction Market.

## Prerequisites

1. **Wallets Setup**
   - [ ] Main wallet with Base ETH for deployment (~0.02 ETH)
   - [ ] Fee collector wallet (your Farcaster connected wallet)
   - [ ] Oracle wallet with small ETH balance for bet resolution (~0.01 ETH)

2. **API Keys**
   - [ ] Neynar API key: https://neynar.com (free tier available)
   - [ ] BaseScan API key: https://basescan.org/apis (optional, for verification)
   - [ ] WalletConnect Project ID: https://cloud.walletconnect.com (free)

3. **Infrastructure**
   - [ ] Vercel account (recommended) or other hosting
   - [ ] Domain name (optional)
   - [ ] Cron job service (Vercel Cron, GitHub Actions, or cron-job.org)

## Step 1: Environment Setup

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Fill in all environment variables:

```env
# === BLOCKCHAIN CONFIGURATION ===
PRIVATE_KEY=0x... # Your deployment wallet private key (DO NOT SHARE!)
BASE_RPC_URL=https://mainnet.base.org
BASE_SEPOLIA_RPC_URL=https://sepolia.base.org
BASESCAN_API_KEY=your_basescan_api_key

# === CONTRACT CONFIGURATION ===
NEXT_PUBLIC_CONTRACT_ADDRESS= # Leave empty, will fill after deployment
NEXT_PUBLIC_CHAIN_ID=8453 # 8453 for Base Mainnet, 84532 for Sepolia

# === FEE COLLECTOR ===
# IMPORTANT: This is YOUR Farcaster wallet where all fees go
FEE_COLLECTOR_ADDRESS=0xYourFarcasterWalletAddress

# === FARCASTER HUB ===
FARCASTER_HUB_URL=https://hub.farcaster.xyz
NEYNAR_API_KEY=your_neynar_api_key_here

# === APPLICATION ===
NEXT_PUBLIC_APP_URL=https://your-domain.com # Or http://localhost:3000 for dev
NEXT_PUBLIC_FRAME_URL=https://your-domain.com/api/frame
NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID=your_project_id

# === ORACLE CONFIGURATION ===
ORACLE_PRIVATE_KEY=0x... # Different wallet for automated resolution
CRON_SECRET=create_a_random_secret_here_use_openssl_rand_base64_32
```

## Step 2: Test Locally

1. Install dependencies:
```bash
npm install
```

2. Compile contracts:
```bash
npm run compile
```

3. Run development server:
```bash
npm run dev
```

4. Visit http://localhost:3000 to verify the UI works

## Step 3: Deploy to Base Sepolia (Testnet)

**IMPORTANT: Always test on testnet first!**

1. Get Sepolia ETH:
   - Visit https://www.alchemy.com/faucets/base-sepolia
   - Or bridge from Sepolia ETH

2. Deploy contract:
```bash
npx hardhat run scripts/deploy.ts --network baseSepolia
```

3. Copy the deployed contract address from output:
```
PredictionMarket deployed to: 0x1234...
```

4. Update `.env`:
```env
NEXT_PUBLIC_CONTRACT_ADDRESS=0x1234... # Your deployed address
NEXT_PUBLIC_CHAIN_ID=84532 # Sepolia chain ID
```

5. Test the application:
```bash
npm run dev
```

6. Place a test bet and verify it works

## Step 4: Deploy to Base Mainnet

1. Ensure you have enough Base ETH (~0.02 ETH for deployment)

2. Update `.env` for mainnet:
```env
NEXT_PUBLIC_CHAIN_ID=8453
```

3. Deploy to Base mainnet:
```bash
npx hardhat run scripts/deploy.ts --network base
```

4. **SAVE THE CONTRACT ADDRESS IMMEDIATELY**

5. Update `.env`:
```env
NEXT_PUBLIC_CONTRACT_ADDRESS=0xYourMainnetAddress
```

6. Verify contract on BaseScan (optional but recommended):
```bash
npx hardhat verify --network base <CONTRACT_ADDRESS> <FEE_COLLECTOR_ADDRESS>
```

## Step 5: Deploy Frontend to Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy:
```bash
vercel --prod
```

4. Or connect GitHub repository:
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - Add environment variables from `.env`
   - Deploy

5. **IMPORTANT**: Add all environment variables in Vercel dashboard:
   - Go to Project Settings → Environment Variables
   - Add each variable from your `.env` file
   - Mark secrets as "Sensitive"

6. Update `.env` with your Vercel URL:
```env
NEXT_PUBLIC_APP_URL=https://your-app.vercel.app
NEXT_PUBLIC_FRAME_URL=https://your-app.vercel.app/api/frame
```

7. Redeploy to apply new URLs

## Step 6: Set Up Automated Bet Resolution

### Option A: Vercel Cron (Recommended)

1. Create `vercel.json`:
```json
{
  "crons": [
    {
      "path": "/api/cron/resolve",
      "schedule": "0 */1 * * *"
    }
  ]
}
```

2. Create `/app/api/cron/resolve/route.ts`:
```typescript
import { NextRequest, NextResponse } from 'next/server';

export async function GET(req: NextRequest) {
  // Vercel Cron automatically sets this header
  if (req.headers.get('authorization') !== `Bearer ${process.env.CRON_SECRET}`) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Implement your resolution logic here
  // Call /api/resolve for each pending bet
  
  return NextResponse.json({ success: true });
}
```

### Option B: GitHub Actions

Create `.github/workflows/resolve-bets.yml`:
```yaml
name: Resolve Bets Hourly
on:
  schedule:
    - cron: '0 * * * *'  # Every hour
  workflow_dispatch:  # Manual trigger

jobs:
  resolve:
    runs-on: ubuntu-latest
    steps:
      - name: Call resolution endpoint
        run: |
          curl -X POST ${{ secrets.APP_URL }}/api/resolve \
            -H "Content-Type: application/json" \
            -d '{"secret": "${{ secrets.CRON_SECRET }}"}'
```

### Option C: External Cron Service

Use https://cron-job.org or similar:
1. Create account
2. Add job to call: `POST https://your-app.vercel.app/api/resolve`
3. Add header: `Authorization: Bearer <CRON_SECRET>`
4. Schedule: Every hour

## Step 7: Test Production Deployment

1. **Test Wallet Connection**
   - Visit your production URL
   - Connect wallet
   - Verify it connects to Base mainnet

2. **Place a Small Test Bet**
   - Use minimum amounts
   - Verify transaction goes through
   - Check bet appears in "My Bets"

3. **Wait 24 Hours and Verify Resolution**
   - Check if bet resolves automatically
   - Verify fees are sent to fee collector
   - Verify winnings are paid out correctly

4. **Test Farcaster Frame**
   - Share frame URL in a Farcaster cast
   - Test interactions from Farcaster app
   - Verify transactions work from frame

## Step 8: Configure Fee Collector

1. Log into the wallet specified as `FEE_COLLECTOR_ADDRESS`

2. Monitor incoming fees:
   - Base fees: 0.0002 ETH per bet
   - Winning fees: 1.5% of payouts

3. Periodically withdraw fees or reinvest

## Step 9: Post-Deployment Checklist

- [ ] Contract deployed to Base mainnet
- [ ] Frontend deployed and accessible
- [ ] All environment variables set correctly
- [ ] Automated resolution working
- [ ] Test bet placed and resolved successfully
- [ ] Farcaster frame working
- [ ] Fee collector receiving payments
- [ ] Documentation updated with your URLs
- [ ] Smart contract verified on BaseScan

## Monitoring & Maintenance

### Track Your Contract

1. Add contract to BaseScan watchlist:
   - https://basescan.org/address/<YOUR_CONTRACT>

2. Monitor events:
   - BetPlaced events
   - BetResolved events
   - Fee transfers

### Update Contract Address

If you need to deploy a new contract:

1. Deploy new contract
2. Update `NEXT_PUBLIC_CONTRACT_ADDRESS`
3. Redeploy frontend
4. Announce migration to users

### Oracle Wallet Management

- Keep oracle wallet funded with ~0.01 ETH
- Monitor gas costs
- Top up when balance is low
- Use a monitoring service for alerts

## Troubleshooting

### Contract Deployment Fails
- Check you have enough ETH for gas
- Verify RPC URL is correct
- Try increasing gas price

### Bets Not Resolving
- Check oracle wallet has ETH
- Verify cron job is running
- Check cron secret matches
- View logs in Vercel dashboard

### Farcaster Data Not Loading
- Verify Neynar API key is valid
- Check API rate limits
- Ensure FID exists and is valid

### Transactions Failing
- Check contract address is correct
- Verify user has enough ETH
- Check Base network is not congested
- Ensure contract is not paused

## Security Best Practices

1. **Never commit `.env` file**
2. **Use separate wallets** for deployment, fees, and oracle
3. **Start with small bet limits** until proven stable
4. **Monitor for suspicious activity**
5. **Keep oracle private key secure**
6. **Regular security audits** if handling large volumes
7. **Set up alerts** for large transactions
8. **Backup all private keys** securely

## Costs Estimate

### One-Time Costs
- Contract deployment: ~0.01-0.02 ETH
- Domain name: ~$10-15/year (optional)

### Ongoing Costs
- Vercel hosting: Free tier sufficient
- Oracle gas fees: ~0.001 ETH per resolution
- Neynar API: Free tier for development

### Revenue
- $0.20 per bet placement (base fee)
- 1.5% of all winning payouts

## Next Steps

After successful deployment:

1. **Promote on Farcaster**
   - Share your frame
   - Engage with community
   - Run promotional campaigns

2. **Add Features**
   - More bet types
   - Leaderboards
   - Referral system
   - Social sharing

3. **Scale**
   - Optimize gas costs
   - Add more Farcaster data sources
   - Implement pool-based betting
   - Add liquidity providers

## Support

If you run into issues:
- Check logs in Vercel dashboard
- Verify all environment variables
- Test on Sepolia first
- Review transaction on BaseScan

Good luck with your deployment! 🎯🚀
