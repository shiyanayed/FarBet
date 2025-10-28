// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title PredictionMarket
 * @dev Decentralized prediction market for Farcaster user statistics
 */
contract PredictionMarket is ReentrancyGuard, Ownable {
    
    // Fee configuration
    uint256 public constant BASE_FEE = 0.2 ether; // $0.2 in ETH (adjust based on ETH price)
    uint256 public constant WINNING_FEE_PERCENT = 150; // 1.5% = 150 basis points
    uint256 public constant BASIS_POINTS = 10000;
    
    address public feeCollector;
    
    enum BetType {
        CASTS_COUNT,          // Bet on number of casts in 24h
        LIKES_GREATER,        // Bet on likes > threshold
        LIKES_LESS,           // Bet on likes < threshold
        REPLIES_COUNT,        // Bet on number of replies
        FOLLOWERS_GAIN        // Bet on follower growth
    }
    
    enum BetStatus {
        ACTIVE,
        RESOLVED_WON,
        RESOLVED_LOST,
        CANCELLED
    }
    
    struct Bet {
        uint256 betId;
        address bettor;
        uint256 fid;              // Farcaster ID of target user
        BetType betType;
        uint256 predictedValue;   // Predicted threshold/value
        uint256 betAmount;
        uint256 timestamp;
        uint256 resolutionTime;   // When to resolve (timestamp + 24h)
        BetStatus status;
        uint256 actualValue;      // Actual value after resolution
    }
    
    struct Market {
        uint256 marketId;
        uint256 fid;
        BetType betType;
        uint256 threshold;
        uint256 totalPoolYes;
        uint256 totalPoolNo;
        uint256 endTime;
        bool resolved;
        bool outcome;             // true = yes, false = no
    }
    
    uint256 private nextBetId;
    uint256 private nextMarketId;
    
    mapping(uint256 => Bet) public bets;
    mapping(uint256 => Market) public markets;
    mapping(address => uint256[]) public userBets;
    mapping(uint256 => uint256[]) public marketBets; // marketId => betIds[]
    
    event BetPlaced(
        uint256 indexed betId,
        address indexed bettor,
        uint256 fid,
        BetType betType,
        uint256 amount,
        uint256 predictedValue
    );
    
    event BetResolved(
        uint256 indexed betId,
        BetStatus status,
        uint256 actualValue,
        uint256 payout
    );
    
    event MarketCreated(
        uint256 indexed marketId,
        uint256 fid,
        BetType betType,
        uint256 threshold
    );
    
    event FeesCollected(address indexed collector, uint256 amount);
    
    constructor(address _feeCollector) Ownable(msg.sender) {
        feeCollector = _feeCollector;
        nextBetId = 1;
        nextMarketId = 1;
    }
    
    /**
     * @dev Place a bet on a Farcaster user's statistics
     */
    function placeBet(
        uint256 _fid,
        BetType _betType,
        uint256 _predictedValue,
        uint256 _betAmount
    ) external payable nonReentrant returns (uint256) {
        require(msg.value >= _betAmount + BASE_FEE, "Insufficient payment");
        require(_betAmount > 0, "Bet amount must be positive");
        
        // Transfer base fee to fee collector
        (bool feeSent, ) = feeCollector.call{value: BASE_FEE}("");
        require(feeSent, "Fee transfer failed");
        
        uint256 betId = nextBetId++;
        uint256 resolutionTime = block.timestamp + 24 hours;
        
        bets[betId] = Bet({
            betId: betId,
            bettor: msg.sender,
            fid: _fid,
            betType: _betType,
            predictedValue: _predictedValue,
            betAmount: _betAmount,
            timestamp: block.timestamp,
            resolutionTime: resolutionTime,
            status: BetStatus.ACTIVE,
            actualValue: 0
        });
        
        userBets[msg.sender].push(betId);
        
        emit BetPlaced(betId, msg.sender, _fid, _betType, _betAmount, _predictedValue);
        
        // Refund excess payment
        if (msg.value > _betAmount + BASE_FEE) {
            (bool refunded, ) = msg.sender.call{value: msg.value - _betAmount - BASE_FEE}("");
            require(refunded, "Refund failed");
        }
        
        return betId;
    }
    
    /**
     * @dev Create a market for binary predictions
     */
    function createMarket(
        uint256 _fid,
        BetType _betType,
        uint256 _threshold
    ) external onlyOwner returns (uint256) {
        uint256 marketId = nextMarketId++;
        
        markets[marketId] = Market({
            marketId: marketId,
            fid: _fid,
            betType: _betType,
            threshold: _threshold,
            totalPoolYes: 0,
            totalPoolNo: 0,
            endTime: block.timestamp + 24 hours,
            resolved: false,
            outcome: false
        });
        
        emit MarketCreated(marketId, _fid, _betType, _threshold);
        return marketId;
    }
    
    /**
     * @dev Place a bet on a market (Yes/No)
     */
    function betOnMarket(
        uint256 _marketId,
        bool _betYes,
        uint256 _betAmount
    ) external payable nonReentrant {
        Market storage market = markets[_marketId];
        require(!market.resolved, "Market already resolved");
        require(block.timestamp < market.endTime, "Market ended");
        require(msg.value >= _betAmount + BASE_FEE, "Insufficient payment");
        
        // Transfer base fee
        (bool feeSent, ) = feeCollector.call{value: BASE_FEE}("");
        require(feeSent, "Fee transfer failed");
        
        if (_betYes) {
            market.totalPoolYes += _betAmount;
        } else {
            market.totalPoolNo += _betAmount;
        }
        
        uint256 betId = nextBetId++;
        bets[betId] = Bet({
            betId: betId,
            bettor: msg.sender,
            fid: market.fid,
            betType: market.betType,
            predictedValue: _betYes ? 1 : 0, // 1 = Yes, 0 = No
            betAmount: _betAmount,
            timestamp: block.timestamp,
            resolutionTime: market.endTime,
            status: BetStatus.ACTIVE,
            actualValue: 0
        });
        
        userBets[msg.sender].push(betId);
        marketBets[_marketId].push(betId);
        
        emit BetPlaced(betId, msg.sender, market.fid, market.betType, _betAmount, _betYes ? 1 : 0);
    }
    
    /**
     * @dev Resolve a bet (called by oracle/owner)
     */
    function resolveBet(
        uint256 _betId,
        uint256 _actualValue
    ) external onlyOwner nonReentrant {
        Bet storage bet = bets[_betId];
        require(bet.status == BetStatus.ACTIVE, "Bet not active");
        require(block.timestamp >= bet.resolutionTime, "Too early to resolve");
        
        bet.actualValue = _actualValue;
        bool won = false;
        
        // Determine if bet won based on type
        if (bet.betType == BetType.CASTS_COUNT || bet.betType == BetType.REPLIES_COUNT || bet.betType == BetType.FOLLOWERS_GAIN) {
            won = (_actualValue == bet.predictedValue);
        } else if (bet.betType == BetType.LIKES_GREATER) {
            won = (_actualValue > bet.predictedValue);
        } else if (bet.betType == BetType.LIKES_LESS) {
            won = (_actualValue < bet.predictedValue);
        }
        
        uint256 payout = 0;
        
        if (won) {
            bet.status = BetStatus.RESOLVED_WON;
            // Simplified payout: 2x bet amount (can be made more sophisticated with pools)
            uint256 grossPayout = bet.betAmount * 2;
            uint256 winningFee = (grossPayout * WINNING_FEE_PERCENT) / BASIS_POINTS;
            payout = grossPayout - winningFee;
            
            // Transfer winning fee to fee collector
            (bool feeSent, ) = feeCollector.call{value: winningFee}("");
            require(feeSent, "Fee transfer failed");
            
            // Transfer payout to bettor
            (bool payoutSent, ) = bet.bettor.call{value: payout}("");
            require(payoutSent, "Payout transfer failed");
        } else {
            bet.status = BetStatus.RESOLVED_LOST;
            // Losing bet amount goes to contract pool
        }
        
        emit BetResolved(_betId, bet.status, _actualValue, payout);
    }
    
    /**
     * @dev Resolve a market
     */
    function resolveMarket(
        uint256 _marketId,
        bool _outcome,
        uint256 _actualValue
    ) external onlyOwner nonReentrant {
        Market storage market = markets[_marketId];
        require(!market.resolved, "Already resolved");
        require(block.timestamp >= market.endTime, "Too early");
        
        market.resolved = true;
        market.outcome = _outcome;
        
        uint256 totalPool = market.totalPoolYes + market.totalPoolNo;
        uint256 winningPool = _outcome ? market.totalPoolYes : market.totalPoolNo;
        
        // Resolve all bets in this market
        uint256[] memory betIds = marketBets[_marketId];
        for (uint256 i = 0; i < betIds.length; i++) {
            Bet storage bet = bets[betIds[i]];
            if (bet.status != BetStatus.ACTIVE) continue;
            
            bool betWon = (bet.predictedValue == 1) == _outcome;
            bet.actualValue = _actualValue;
            
            if (betWon && winningPool > 0) {
                bet.status = BetStatus.RESOLVED_WON;
                uint256 grossPayout = (bet.betAmount * totalPool) / winningPool;
                uint256 winningFee = (grossPayout * WINNING_FEE_PERCENT) / BASIS_POINTS;
                uint256 payout = grossPayout - winningFee;
                
                (bool feeSent, ) = feeCollector.call{value: winningFee}("");
                require(feeSent, "Fee transfer failed");
                
                (bool payoutSent, ) = bet.bettor.call{value: payout}("");
                require(payoutSent, "Payout transfer failed");
                
                emit BetResolved(betIds[i], bet.status, _actualValue, payout);
            } else {
                bet.status = BetStatus.RESOLVED_LOST;
                emit BetResolved(betIds[i], bet.status, _actualValue, 0);
            }
        }
    }
    
    /**
     * @dev Get user's active bets
     */
    function getUserBets(address _user) external view returns (uint256[] memory) {
        return userBets[_user];
    }
    
    /**
     * @dev Get bet details
     */
    function getBet(uint256 _betId) external view returns (Bet memory) {
        return bets[_betId];
    }
    
    /**
     * @dev Update fee collector address
     */
    function updateFeeCollector(address _newCollector) external onlyOwner {
        feeCollector = _newCollector;
    }
    
    /**
     * @dev Emergency withdraw (owner only)
     */
    function emergencyWithdraw() external onlyOwner {
        (bool sent, ) = owner().call{value: address(this).balance}("");
        require(sent, "Withdrawal failed");
    }
    
    receive() external payable {}
}
