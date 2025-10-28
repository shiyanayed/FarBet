# 🎯 Feature Overview

## Core Features

### 1. Multiple Bet Types

#### Cast Count Prediction
- Predict exact number of casts a user will make in 24 hours
- Exact match required to win
- Example: "User @alice will make exactly 15 casts in the next 24 hours"

#### Likes Prediction (Greater/Less)
- Bet on whether total likes will be above or below a threshold
- Two variations:
  - **Greater**: Total likes > threshold
  - **Less**: Total likes < threshold
- Example: "User @bob will get MORE than 100 likes in 24 hours"

#### Reply Count Prediction
- Predict number of replies a user will receive
- Exact match required
- Example: "User @charlie will receive 8 replies"

#### Follower Growth Prediction
- Bet on follower count increase/decrease
- Useful for trending accounts
- Example: "User @dave will gain 50 followers"

### 2. Fee Structure

#### Base Fee: $0.20 (0.0002 ETH)
- Charged on every bet placement
- Non-refundable
- Sent immediately to fee collector
- Covers platform operation costs

#### Winning Fee: 1.5%
- Charged only on winning payouts
- Calculated from gross payout
- Sent to fee collector on bet resolution
- Example: Win $100 → Fee = $1.50 → You receive $98.50

#### Fee Flow
```
User places bet → Base fee to collector
User wins → 1.5% of payout to collector
User loses → Bet amount stays in pool
```

### 3. Direct Wallet Integration

#### No Deposits Required
- Bets placed directly from connected wallet
- No need to deposit funds to platform
- No withdrawal delays
- Full control of funds

#### Supported Wallets
- MetaMask
- Coinbase Wallet
- WalletConnect compatible wallets
- Any Base-compatible wallet

#### Payment Flow
1. Connect wallet to Base network
2. Approve transaction with bet amount + base fee
3. Funds sent to smart contract
4. Win → Automatic payout to your wallet
5. Lose → Funds remain in contract pool

### 4. Farcaster Frame Integration

#### Interactive Betting in Feed
- Bet directly from Farcaster without leaving the app
- Native frame UI for seamless experience
- Share bet frames with friends
- Viral betting mechanics

#### Frame Features
- Choose bet type within frame
- Enter user FID and prediction
- Transaction signing via Farcaster
- View bet history in frame
- Share results on timeline

#### Frame Actions
1. **Home**: Browse bet types
2. **Place Bet**: Interactive bet placement
3. **My Bets**: View your active/past bets
4. **Results**: See bet outcomes

### 5. Smart Contract Features

#### Decentralized & Trustless
- All bets stored on Base blockchain
- Transparent bet resolution
- Immutable bet records
- No central point of failure

#### Security Features
- ReentrancyGuard protection
- Owner-only bet resolution
- Input validation on all bets
- Overflow protection (Solidity 0.8+)

#### Gas Optimizations
- Efficient storage layout
- Minimal on-chain computation
- Event-based indexing
- Batch operations support

### 6. Automated Bet Resolution

#### Oracle System
- Automatic bet resolution after 24 hours
- Fetches real data from Farcaster
- Compares against predictions
- Distributes payouts automatically

#### Resolution Process
1. Timer hits 24 hours
2. Oracle fetches Farcaster stats
3. Compares actual vs predicted
4. Updates bet status on-chain
5. Transfers winnings (if won)
6. Emits resolution event

#### Manual Override
- Owner can resolve manually if oracle fails
- Useful for edge cases
- Transparent resolution logs

### 7. Bet Tracking & History

#### User Dashboard
- View all your active bets
- See bet resolution countdowns
- Track wins and losses
- Calculate total P&L

#### Bet Details
- Bet ID and timestamp
- Target user information
- Predicted vs actual values
- Bet amount and potential payout
- Resolution time remaining
- Current status

#### Stats Display
- Total bets placed
- Win/loss ratio
- Total amount wagered
- Total winnings
- Total fees paid

### 8. Real-Time Farcaster Data

#### Live Stats Fetching
- Current cast count
- Total likes received
- Reply counts
- Follower growth
- Activity trends

#### 24-Hour Windows
- All predictions based on 24-hour windows
- Snapshot taken at bet placement
- Final snapshot at resolution time
- Delta calculated for growth metrics

### 9. Market Types

#### Individual Bets
- Bet against the house
- Fixed 2x payout multiplier
- Simple win/loss outcome
- Instant bet placement

#### Pool-Based Markets (Future)
- Bet against other users
- Dynamic odds based on pool
- Larger potential payouts
- Market maker functionality

## User Experience Features

### Beautiful UI
- Modern gradient design
- Responsive mobile layout
- Clear bet forms
- Intuitive navigation
- Real-time updates

### Wallet Management
- Easy connect/disconnect
- Address display with truncation
- Network detection
- Balance checking
- Transaction history

### Transaction Feedback
- Loading states during tx
- Success/error messages
- Transaction hash display
- Block explorer links
- Gas fee estimation

### Accessibility
- Keyboard navigation
- Screen reader support
- High contrast mode
- Mobile-first design
- Error handling

## Developer Features

### API Endpoints
- RESTful API design
- JSON responses
- Error handling
- Rate limiting ready
- CORS configured

### Event System
- On-chain events for indexing
- Real-time bet placement notifications
- Resolution event tracking
- Fee collection monitoring

### Extensibility
- Modular contract design
- Easy to add new bet types
- Pluggable oracle system
- Customizable fee structure

## Coming Soon

### Social Features
- [ ] Leaderboard for top bettors
- [ ] Share bets on Farcaster
- [ ] Follow other bettors
- [ ] Bet groups and tournaments

### Advanced Betting
- [ ] Multi-bet parlays
- [ ] Live betting on active casts
- [ ] Bet on engagement ratios
- [ ] Custom time windows

### Gamification
- [ ] Achievement badges
- [ ] Streak bonuses
- [ ] Referral rewards
- [ ] Loyalty tiers

### Analytics
- [ ] Bet success heatmaps
- [ ] User performance graphs
- [ ] Market trends
- [ ] Predictive insights

### Platform Expansion
- [ ] Support for more chains
- [ ] Fiat on-ramp integration
- [ ] Mobile app (iOS/Android)
- [ ] API for third-party integrations

## Technical Specifications

### Smart Contract
- Language: Solidity 0.8.20
- Framework: Hardhat
- Libraries: OpenZeppelin
- Network: Base (Ethereum L2)
- Gas: ~150k per bet placement

### Frontend
- Framework: Next.js 14
- Language: TypeScript
- Styling: TailwindCSS
- Wallet: Wagmi + ConnectKit
- State: React Query

### Backend
- Runtime: Next.js API Routes
- Data: Neynar API (Farcaster)
- Oracle: Automated with private key
- Hosting: Vercel (recommended)

### Infrastructure
- Blockchain: Base Mainnet
- RPC: Alchemy/Infura
- Analytics: BaseScan
- Monitoring: Vercel Analytics
- Cron: Vercel Cron/GitHub Actions

## Performance Metrics

### Transaction Times
- Bet placement: ~2 seconds
- Bet resolution: ~5 seconds
- Payout: Instant (same tx)

### Costs
- Base fee: $0.20 per bet
- Gas fees: ~$0.01-0.05 per tx
- Resolution: Free (oracle pays gas)

### Scalability
- Concurrent users: Unlimited
- Bets per second: 10+ (Base limit)
- Storage: On-chain (permanent)
- API rate limit: 10 req/sec (Neynar)

## Security & Trust

### Audits
- OpenZeppelin contracts (audited)
- Internal security review
- Testnet battle-testing
- Community bug bounty (planned)

### Transparency
- Open source code
- Verified contracts on BaseScan
- Public bet data
- Transparent fee structure

### Risk Management
- Smart contract security
- Oracle redundancy (planned)
- Emergency pause (owner)
- Gradual rollout strategy
