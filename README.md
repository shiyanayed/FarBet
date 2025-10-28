# 🎯 Farcaster Prediction Market

A decentralized prediction market built on Base blockchain that allows users to bet on Farcaster user statistics like cast counts, likes, and follower growth.

## Features

- 📊 **Multiple Bet Types**
  - Number of casts in 24 hours
  - Total likes (greater than or less than a threshold)
  - Number of replies
  - Follower growth
  
- 💰 **Fee Structure**
  - Base fee: $0.20 per bet placement
  - Winning fee: 1.5% on withdrawals
  - All fees sent to configured fee collector wallet

- 🔗 **Direct Wallet Integration**
  - No deposits required
  - Bets placed directly from connected wallet
  - Automatic payout to winners

- 🖼️ **Farcaster Frame Support**
  - Interactive betting through Farcaster frames
  - Seamless integration with Farcaster feed

## Tech Stack

- **Frontend**: Next.js 14, React, TailwindCSS
- **Blockchain**: Base (Ethereum L2), Solidity, Hardhat
- **Wallet**: Wagmi, ConnectKit
- **Farcaster**: Neynar API, Farcaster Hub
- **Smart Contracts**: OpenZeppelin, Viem

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn
- A Base wallet with ETH for deployment
- Neynar API key (for Farcaster data)

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd farcaster-prediction-market
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

4. Fill in your environment variables:
```env
# Your deployment wallet private key
PRIVATE_KEY=your_private_key_here

# Your Farcaster wallet address (receives all fees)
FEE_COLLECTOR_ADDRESS=0xYourFarcasterWalletAddress

# Neynar API key for Farcaster data
NEYNAR_API_KEY=your_neynar_api_key_here

# Oracle private key for automated bet resolution
ORACLE_PRIVATE_KEY=your_oracle_private_key

# Secret for cron job authentication
CRON_SECRET=random_secret_for_cron_jobs
```

### Smart Contract Deployment

1. Compile the contracts:
```bash
npm run compile
```

2. Deploy to Base Sepolia (testnet):
```bash
npx hardhat run scripts/deploy.ts --network baseSepolia
```

3. Deploy to Base Mainnet:
```bash
npx hardhat run scripts/deploy.ts --network base
```

4. Update `.env` with the deployed contract address:
```env
NEXT_PUBLIC_CONTRACT_ADDRESS=<deployed_contract_address>
```

### Running the Application

1. Development mode:
```bash
npm run dev
```

2. Production build:
```bash
npm run build
npm start
```

The app will be available at `http://localhost:3000`

## Usage

### For Users

1. **Connect Wallet**: Click "Connect Wallet" and connect your Base-compatible wallet
2. **Place a Bet**:
   - Select bet type (casts, likes, etc.)
   - Enter target user's FID (Farcaster ID)
   - Set your predicted value/threshold
   - Choose bet amount
   - Confirm transaction (base fee + bet amount)
3. **Track Bets**: View your active and resolved bets in "My Bets" tab
4. **Collect Winnings**: Winnings are automatically sent after bet resolution (minus 1.5% fee)

### For Frame Users

Share the frame on Farcaster:
- Frame URL: `https://your-domain.com/api/frame`
- Users can interact directly from their feed

## Bet Resolution

Bets are resolved automatically 24 hours after placement using the oracle system:

```bash
# Manual resolution via API
curl -X POST https://your-domain.com/api/resolve \
  -H "Content-Type: application/json" \
  -d '{"secret": "your_cron_secret", "betId": 1}'
```

### Setting up Automated Resolution

Use a cron service (like Vercel Cron or GitHub Actions) to call the resolution endpoint:

```yaml
# Example: .github/workflows/resolve-bets.yml
name: Resolve Bets
on:
  schedule:
    - cron: '0 */1 * * *' # Every hour
jobs:
  resolve:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger resolution
        run: |
          curl -X POST ${{ secrets.APP_URL }}/api/resolve \
            -H "Content-Type: application/json" \
            -d '{"secret": "${{ secrets.CRON_SECRET }}"}'
```

## API Endpoints

### Farcaster Stats
```
GET /api/farcaster/stats?fid=<user_fid>&type=<stat_type>
```

### User Bets
```
GET /api/bets?address=<wallet_address>
```

### Specific Bet
```
GET /api/bets?betId=<bet_id>
```

### Resolve Bet
```
POST /api/resolve
Body: { "secret": "cron_secret", "betId": number }
```

## Smart Contract Functions

### Place a Bet
```solidity
function placeBet(
    uint256 _fid,
    BetType _betType,
    uint256 _predictedValue,
    uint256 _betAmount
) external payable returns (uint256)
```

### Resolve a Bet (Owner/Oracle)
```solidity
function resolveBet(
    uint256 _betId,
    uint256 _actualValue
) external onlyOwner
```

### Get User Bets
```solidity
function getUserBets(address _user) external view returns (uint256[] memory)
```

## Fee Configuration

Fees are hardcoded in the smart contract:
- **BASE_FEE**: 0.2 ether (adjust based on ETH price)
- **WINNING_FEE_PERCENT**: 150 basis points (1.5%)

To change fees, update the contract and redeploy.

## Security Considerations

- ✅ ReentrancyGuard protection on bet placement and resolution
- ✅ Owner-only access for bet resolution
- ✅ Overflow protection with Solidity 0.8+
- ✅ Input validation on all user inputs
- ⚠️ Oracle centralization (consider Chainlink for production)
- ⚠️ ETH price volatility affects fee values

## Testing

```bash
# Run contract tests
npx hardhat test

# Run with coverage
npx hardhat coverage
```

## Deployment Checklist

- [ ] Set FEE_COLLECTOR_ADDRESS to your Farcaster wallet
- [ ] Deploy contract to Base network
- [ ] Update NEXT_PUBLIC_CONTRACT_ADDRESS
- [ ] Configure Neynar API key
- [ ] Set up oracle wallet for automated resolution
- [ ] Configure cron job for bet resolution
- [ ] Test on testnet first (Base Sepolia)
- [ ] Verify contract on BaseScan

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Open an issue on GitHub
- Contact on Farcaster: [Your Farcaster handle]

## Disclaimer

This is experimental software. Use at your own risk. Always test on testnets before deploying to mainnet. Gambling may be illegal in your jurisdiction - check local laws.
