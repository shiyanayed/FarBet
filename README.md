<<<<<<< HEAD
# Farcaster Prediction Market

A decentralized prediction market platform built on Farcaster for betting on user activity metrics. Users can create markets and place bets on how many casts a user will make, total likes received, engagement scores, and more.

## Features

### 🎲 Core Betting Features
- **Casts Prediction**: Bet on how many casts a user will make in 24 hours
- **Likes Prediction**: Bet on total likes a user will receive
- **Engagement Scores**: Bet on engagement metrics
- **Over/Under Markets**: Simple binary betting on outcome ranges

### 💰 Fee Structure
- **Base Fee**: $0.20 per bet (charged upfront)
- **Win Fee**: 1.5% on total winnings (charged on withdrawal)
- **Fee Recipient**: `0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC`

### 👛 Wallet Integration
- Uses Farcaster verified wallets (no deposit required)
- Automatic payment from user's wallet
- Native ETH/USDC support

### 🖼️ Farcaster Frames
- Interactive frames for market browsing
- One-click betting interface
- Real-time balance and bet tracking
- Easy withdrawal management

## Installation

### Prerequisites
- Python 3.9+
- Node.js 16+ (for Farcaster tools)
- Ethereum RPC endpoint (Alchemy recommended)
- Farcaster API keys (Neynar)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/farcaster-prediction-market.git
cd farcaster-prediction-market
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**
```bash
python
>>> from project import app, init_db
>>> with app.app_context():
...     init_db(app)
```

6. **Run the server**
```bash
python project.py
```

Server will start at `http://localhost:5000`

## Environment Configuration

Create a `.env` file with the following variables:

```env
# Farcaster
FARCASTER_HUB_URL=https://hub.farcaster.builders
NEYNAR_API_KEY=your_api_key

# Blockchain
ALCHEMY_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/your-key
CHAIN_ID=1
PRIVATE_KEY=your_wallet_private_key

# Contracts
USDC_CONTRACT=0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48
TREASURE_WALLET=0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC

# Payment
STRIPE_KEY=sk_live_...
COINBASE_KEY=your_coinbase_api_key
=======
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
>>>>>>> 8d6235062c7700e48053a749bc45f4d6e52ca169
```

## API Endpoints

<<<<<<< HEAD
### Markets

#### Get All Markets
```
GET /api/markets
```
Returns list of all active prediction markets.

**Response:**
```json
{
  "success": true,
  "markets": [
    {
      "id": 1,
      "user_fid": 3,
      "market_type": "casts_count",
      "threshold": 5,
      "direction": "over",
      "status": "active",
      "created_at": "2024-01-01T12:00:00",
      "end_time": "2024-01-02T12:00:00",
      "total_pool": 100.0,
      "bets_count": 5
    }
  ]
}
```

#### Create Market
```
POST /api/markets/create
```
Create a new prediction market.

**Request:**
```json
{
  "user_fid": 3,
  "market_type": "casts_count",
  "threshold": 5,
  "direction": "over",
  "duration_hours": 24
}
```

**Response:**
```json
{
  "success": true,
  "market_id": 1,
  "market": { ... }
}
```

### Betting

#### Place Bet
```
POST /api/bets/place
```
Place a bet on a market.

**Request:**
```json
{
  "market_id": 1,
  "user_fid": 100,
  "prediction": "over",
  "amount": 10.0,
  "user_wallet": "0x742d35Cc6634C0532925a3b844Bc9e7595f42e24"
}
```

**Response:**
```json
{
  "success": true,
  "bet_id": 1,
  "message": "Bet placed successfully",
  "transaction": "0xabc123...",
  "total_cost": 10.2
}
```

#### Get Bet
```
GET /api/bets/<bet_id>
```
Get details of a specific bet.

#### Get User Bets
```
GET /api/bets/user/<fid>
```
Get all bets placed by a user.

### Market Settlement

#### Settle Market
```
POST /api/markets/<market_id>/settle
```
Settle a market and determine winners.

**Response:**
```json
{
  "success": true,
  "market_id": 1,
  "result_value": 7,
  "winners_count": 3,
  "losers_count": 2,
  "total_pool": 100.0
}
```

### Withdrawals

#### Request Withdrawal
```
POST /api/withdrawals/request
```
Request withdrawal of winnings.

**Request:**
```json
{
  "user_fid": 100,
  "user_wallet": "0x742d35Cc6634C0532925a3b844Bc9e7595f42e24",
  "amount": 50.0
}
```

#### Process Withdrawal
```
POST /api/withdrawals/<withdrawal_id>/process
```
Process a pending withdrawal.

### User Profile

#### Get User Profile
```
GET /api/users/<fid>
```
Get user profile and statistics.

**Response:**
```json
{
  "success": true,
  "user": {
    "fid": 100,
    "username": "alice",
    "wallet": "0x742d...",
    "stats": {
      "total_bets": 10,
      "won_bets": 7,
      "win_rate": 70.0,
      "total_wagered": 100.0,
      "total_winnings": 150.0,
      "balance": 50.0
    }
  }
}
```

## Farcaster Frames

### Market Discovery
Interactive frame to browse and view all active markets.

```
/frame/markets
```

### Create Market
Create a new prediction market directly from Farcaster.

```
/frame/create-market
```
Input format: `@username metric_type threshold hours`

Example: `@alice casts_count 5 24`

### Place Bet
Place a bet on a market from Farcaster.

```
/frame/place-bet
```
Input format: `market_id prediction amount`

Example: `1 over 10.5`

### My Bets
View all your active and completed bets.

```
/frame/my-bets
```

### Profile
View your profile, statistics, and balance.

```
/frame/profile
```

### Withdraw
Withdraw your winnings to your wallet.

```
/frame/withdraw
```

## Database Schema

### UserProfile
- `fid`: Farcaster ID
- `username`: Farcaster username
- `display_name`: Display name
- `wallet_address`: Primary Ethereum wallet
- `followers_count`: Number of followers
- `following_count`: Number of following

### MarketEvent
- `user_fid`: Target user's FID
- `market_type`: Type of prediction (casts_count, likes_total, engagement_score)
- `threshold`: Prediction threshold
- `direction`: Over or Under
- `status`: active, settled, cancelled
- `end_time`: When market closes
- `result_value`: Actual outcome (after settlement)
- `total_pool`: Sum of all bets

### Bet
- `market_id`: Related market
- `user_fid`: Bettor's FID
- `user_wallet`: Bettor's wallet
- `prediction`: Over or Under
- `amount`: Bet amount in USD
- `base_fee`: $0.20
- `payout`: Winnings (if won)
- `fee_on_win`: 1.5% fee on payout
- `status`: pending, active, won, lost
- `transaction_hash`: Blockchain transaction

### Withdrawal
- `user_fid`: User requesting withdrawal
- `user_wallet`: Target wallet
- `amount`: Withdrawal amount
- `status`: pending, processing, completed, failed
- `transaction_hash`: Withdrawal transaction

## Fee Model

### Base Fee ($0.20)
Charged when user places a bet, sent to:
```
0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC
```

### Win Fee (1.5%)
Charged when user withdraws winnings:
- Calculated: `winnings * 1.5 / 100`
- Sent to: `0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC`

### Example
- User bets: $10
- Base fee: $0.20
- Total cost: $10.20
- If user wins $20
- Win fee: $0.30 (1.5%)
- User receives: $19.70

## Payout Calculation

Payouts are calculated using a pool-based system:

```
Losing Pool = (Total Pool) * 0.7
Payout per Winner = (Losing Pool / Number of Winners) + Original Bet
```

## Security Considerations

1. **Wallet Verification**: All transactions require verified Farcaster wallet
2. **Transaction Signing**: Private key never exposed to client
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **Input Validation**: All user inputs are validated server-side
5. **Database**: Use SQLAlchemy ORM to prevent SQL injection

## Supported Networks

- **Ethereum Mainnet** (Chain ID: 1)
- **Ethereum Sepolia** (Chain ID: 11155111) - For testing

## Testing

### Run tests
```bash
pytest tests/
```

### Test environment
Create `.env.test` for testing configuration:
```env
CHAIN_ID=11155111  # Sepolia
# ... other test config
```

## Deployment

### Docker Deployment
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "project.py"]
```

### Vercel Deployment
```bash
vercel deploy
```

### AWS Lambda
Use AWS Lambda with Flask API Gateway integration.

## Performance Optimization

1. **Database Indexing**: Indexes on frequently queried fields
2. **Caching**: Cache user profiles and market data
3. **Batch Processing**: Process market settlements in batches
4. **Connection Pooling**: Reuse database connections

## Future Enhancements

- [ ] Multi-chain support (Polygon, Arbitrum)
- [ ] Advanced betting options (parlays, teasers)
- [ ] Leaderboards and rankings
- [ ] Social trading features
- [ ] Mobile app
- [ ] Advanced analytics dashboard
- [ ] Automated market maker (AMM)
- [ ] Options markets

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
=======
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
>>>>>>> 8d6235062c7700e48053a749bc45f4d6e52ca169

## License

MIT License - see LICENSE file for details

## Support

<<<<<<< HEAD
- **Discord**: [Join our Discord](https://discord.gg/your-invite)
- **Twitter**: [@FarcasterMarket](https://twitter.com/farcastermarket)
- **Email**: support@farcastermarket.com

## Disclaimer

This is a prediction market platform. Betting involves risk. Past performance is not indicative of future results. Only bet what you can afford to lose.

---

**Built with ❤️ on Farcaster**
=======
For issues and questions:
- Open an issue on GitHub
- Contact on Farcaster: [Your Farcaster handle]

## Disclaimer

This is experimental software. Use at your own risk. Always test on testnets before deploying to mainnet. Gambling may be illegal in your jurisdiction - check local laws.
>>>>>>> 8d6235062c7700e48053a749bc45f4d6e52ca169
