# Smart Contracts

## PredictionMarket.sol

Main contract for the Farcaster prediction market.

### Key Features

1. **Bet Placement**: Users can place bets with base fee
2. **Multiple Bet Types**: Casts count, likes, replies, followers
3. **Automated Resolution**: Oracle-based bet settlement
4. **Fee Collection**: Base fee + winning fee sent to collector
5. **Security**: ReentrancyGuard, Ownable, input validation

### Contract Functions

#### Public Functions

##### placeBet
```solidity
function placeBet(
    uint256 _fid,
    BetType _betType,
    uint256 _predictedValue,
    uint256 _betAmount
) external payable returns (uint256)
```
Place a new bet. Requires payment = betAmount + BASE_FEE.

**Parameters:**
- `_fid`: Farcaster ID of target user
- `_betType`: Type of bet (0-4)
- `_predictedValue`: Predicted value or threshold
- `_betAmount`: Amount to bet (in wei)

**Returns:** Bet ID

**Emits:** `BetPlaced` event

##### betOnMarket
```solidity
function betOnMarket(
    uint256 _marketId,
    bool _betYes,
    uint256 _betAmount
) external payable
```
Place a bet on a binary market.

#### Owner-Only Functions

##### resolveBet
```solidity
function resolveBet(
    uint256 _betId,
    uint256 _actualValue
) external onlyOwner nonReentrant
```
Resolve a bet after 24 hours. Only callable by oracle/owner.

##### createMarket
```solidity
function createMarket(
    uint256 _fid,
    BetType _betType,
    uint256 _threshold
) external onlyOwner returns (uint256)
```
Create a new binary prediction market.

##### updateFeeCollector
```solidity
function updateFeeCollector(address _newCollector) external onlyOwner
```
Update the fee collector address.

#### View Functions

##### getUserBets
```solidity
function getUserBets(address _user) external view returns (uint256[] memory)
```
Get all bet IDs for a user.

##### getBet
```solidity
function getBet(uint256 _betId) external view returns (Bet memory)
```
Get detailed information about a specific bet.

### Data Structures

#### Bet
```solidity
struct Bet {
    uint256 betId;
    address bettor;
    uint256 fid;
    BetType betType;
    uint256 predictedValue;
    uint256 betAmount;
    uint256 timestamp;
    uint256 resolutionTime;
    BetStatus status;
    uint256 actualValue;
}
```

#### BetType Enum
```solidity
enum BetType {
    CASTS_COUNT,      // 0: Exact cast count
    LIKES_GREATER,    // 1: Likes > threshold
    LIKES_LESS,       // 2: Likes < threshold
    REPLIES_COUNT,    // 3: Reply count
    FOLLOWERS_GAIN    // 4: Follower growth
}
```

#### BetStatus Enum
```solidity
enum BetStatus {
    ACTIVE,           // 0: Waiting for resolution
    RESOLVED_WON,     // 1: Bet won
    RESOLVED_LOST,    // 2: Bet lost
    CANCELLED         // 3: Bet cancelled
}
```

### Events

#### BetPlaced
```solidity
event BetPlaced(
    uint256 indexed betId,
    address indexed bettor,
    uint256 fid,
    BetType betType,
    uint256 amount,
    uint256 predictedValue
)
```

#### BetResolved
```solidity
event BetResolved(
    uint256 indexed betId,
    BetStatus status,
    uint256 actualValue,
    uint256 payout
)
```

#### MarketCreated
```solidity
event MarketCreated(
    uint256 indexed marketId,
    uint256 fid,
    BetType betType,
    uint256 threshold
)
```

### Fee Structure

#### Constants
- `BASE_FEE = 0.2 ether` - Base fee per bet (adjust based on ETH/USD)
- `WINNING_FEE_PERCENT = 150` - 1.5% in basis points
- `BASIS_POINTS = 10000` - For percentage calculations

#### Fee Calculation
```solidity
// Base fee: charged on bet placement
baseFee = BASE_FEE

// Winning fee: charged on payout
winningFee = (grossPayout * WINNING_FEE_PERCENT) / BASIS_POINTS
netPayout = grossPayout - winningFee
```

### Security Features

1. **ReentrancyGuard**: Prevents reentrancy attacks on bet placement and resolution
2. **Ownable**: Only owner can resolve bets and manage markets
3. **Input Validation**: All inputs are validated
4. **Safe Math**: Solidity 0.8+ automatic overflow protection
5. **Pull Payment Pattern**: Winners receive payouts via transactions

### Gas Optimization

- Events for off-chain indexing
- Efficient storage layout
- Minimal loops in critical functions
- View functions for data retrieval

### Upgradeability

This contract is NOT upgradeable. To update:
1. Deploy new contract
2. Migrate active bets (if possible)
3. Update frontend to use new address

### Testing

```bash
# Compile
npx hardhat compile

# Test
npx hardhat test

# Coverage
npx hardhat coverage

# Gas report
REPORT_GAS=true npx hardhat test
```

### Deployment

```bash
# Sepolia testnet
npx hardhat run scripts/deploy.ts --network baseSepolia

# Base mainnet
npx hardhat run scripts/deploy.ts --network base
```

### Verification

```bash
npx hardhat verify --network base <CONTRACT_ADDRESS> <FEE_COLLECTOR_ADDRESS>
```

### Known Limitations

1. **Oracle Centralization**: Bet resolution requires trusted oracle
2. **24-Hour Window**: Fixed resolution time
3. **ETH Price Volatility**: BASE_FEE value in USD varies
4. **No Bet Cancellation**: Active bets cannot be cancelled
5. **Simple Payout**: 2x multiplier for individual bets

### Future Improvements

- [ ] Chainlink oracle integration
- [ ] Variable resolution windows
- [ ] Pool-based betting with dynamic odds
- [ ] Bet cancellation within grace period
- [ ] Multi-signature oracle
- [ ] Stablecoin support for fees
- [ ] Progressive fee structure based on volume

### License

MIT License
