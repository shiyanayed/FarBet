# Farcaster Prediction Market - Fee Structure Visual Guide

## 📊 Complete Fee Flow

### Summary
```
INCOMING              OUTGOING
════════              ════════

User Places Bet $10  ──→  Base Fee $0.20      ──→  Treasure Wallet
                     ──→  Bet Pool $10.00     ──→  Market Settlement

Market Ends
User Wins $15        ──→  Win Amount $15      ──→  User Account Balance
                     
User Withdraws $15   ──→  Win Fee $0.225 (1.5%) ──→  Treasure Wallet
                     ──→  Net Amount $14.775      ──→  User Wallet
```

---

## 💸 Detailed Fee Breakdown

### SCENARIO 1: User Places $10 Bet (LOSES)

```
┌─────────────────────────────────────────────────────────┐
│ BET PLACEMENT - User $10 Over/Under Prediction           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  User Wallet Balance: $100.00                           │
│                                                          │
│  Bet Amount:        $10.00                              │
│  Base Fee:           $0.20  ──┐                         │
│                               │                         │
│  Total Charged:     $10.20    ├─→ Treasure Wallet       │
│                               │   0xf2B6664bF...        │
│  User Balance:      $89.80    │                         │
│                               │                         │
│  Market Pool:       +$10.00   ├─→ Used for Settlement   │
│                                                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Market Settles (24 hours later)                        │
│  Actual Value: 3 casts (User predicted OVER 5)          │
│  Result: BET LOST ❌                                    │
│                                                          │
│  User Balance: $89.80 (no change)                       │
│                                                          │
└─────────────────────────────────────────────────────────┘

FEES COLLECTED:
├─ Base Fee: $0.20 → Treasure Wallet ✅
├─ Total Fees: $0.20
└─ User Net: -$10.20
```

---

### SCENARIO 2: User Places $50 Bet (WINS)

```
┌──────────────────────────────────────────────────────────┐
│ BET PLACEMENT - User $50 Over Prediction                 │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  User Wallet Balance: $500.00                            │
│                                                           │
│  Bet Amount:        $50.00                               │
│  Base Fee:           $0.20  ──┐                          │
│                               │                          │
│  Total Charged:     $50.20    ├─→ Treasure Wallet        │
│                               │   0xf2B6664bF...         │
│  User Balance:     $449.80    │                          │
│                               │                          │
│  Market Pool:      +$50.00    ├─→ Used for Settlement    │
│                                                           │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  Market Settles (24 hours later)                         │
│  Actual Value: 8 casts (User predicted OVER 5)           │
│  Result: BET WON ✅                                      │
│                                                           │
│  Payout Calculation:                                     │
│  ├─ Bet Amount: $50.00 (returned)                        │
│  ├─ Prize Pool Share: $30.00 (70% pool split)            │
│  └─ Total Winnings: $80.00                               │
│                                                           │
│  User Balance Updated:                                   │
│  $449.80 + $80.00 = $529.80                              │
│                                                           │
└──────────────────────────────────────────────────────────┘

BET PHASE FEES COLLECTED:
├─ Base Fee: $0.20 → Treasure Wallet ✅
└─ Running Total: $0.20
```

---

### SCENARIO 2b: User Withdraws Winnings

```
┌──────────────────────────────────────────────────────────┐
│ WITHDRAWAL - User Requests to Cash Out Winnings          │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  Current Balance: $529.80                                │
│  (Original: $500 + Winnings: $80 - Base Fee: $0.20)      │
│                                                           │
│  Withdrawal Request Amount: $80.00                       │
│                                                           │
│  Win Fee Calculation:                                    │
│  ├─ Win Fee Percentage: 1.5%                             │
│  ├─ Win Fee Amount: $80.00 × 1.5% = $1.20               │
│  │                                                        │
│  │  $1.20  ──→ Treasure Wallet ✅                        │
│  │          0xf2B6664bF...                               │
│  │                                                        │
│  └─ Amount to User: $80.00 - $1.20 = $78.80              │
│                                                           │
│  $78.80  ──→ User Wallet                                 │
│           Direct Transfer                                 │
│                                                           │
│  Remaining Balance: $529.80 - $80.00 = $449.80           │
│                                                           │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  WITHDRAWAL COMPLETE                                     │
│  └─ User Wallet: $578.80 ($500 start + $78.80 net win)   │
│                                                           │
└──────────────────────────────────────────────────────────┘

WITHDRAWAL PHASE FEES COLLECTED:
├─ Win Fee: $1.20 → Treasure Wallet ✅
└─ Total Fees This Cycle: $0.20 + $1.20 = $1.40
```

---

## 📈 COMPLETE CYCLE EXAMPLE

```
COMPLETE BETTING CYCLE - Full Flow with All Fees

┌─────────────────────────────────────────────────────────────┐
│                    INITIAL STATE                             │
│  User Wallet: $1000.00                                      │
│  Treasure Wallet: $0.00                                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                 STEP 1: PLACE BET                           │
│  • Market: Over 10 Casts for User XYZ                       │
│  • Bet Amount: $100.00                                      │
│  • Base Fee: $0.20                                          │
│  • Total Charged: $100.20                                   │
│                                                              │
│  Base Fee Flow:                                              │
│  $0.20 ──→ Treasure Wallet                                  │
├─────────────────────────────────────────────────────────────┤
│  User Wallet: $1000 - $100.20 = $899.80                     │
│  Treasure Wallet: $0.00 + $0.20 = $0.20 ✅                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
          [WAIT 24 HOURS - MARKET SETTLES]
                            ↓
┌─────────────────────────────────────────────────────────────┐
│            STEP 2: MARKET SETTLEMENT                        │
│  • Actual Value: 12 Casts (Over threshold)                  │
│  • Prediction: OVER                                         │
│  • Result: ✅ BET WON                                       │
│                                                              │
│  Payout Calculation:                                         │
│  ├─ Bet Amount: $100.00 (returned)                          │
│  ├─ Prize Pool Share: $60.00                                │
│  └─ Total Payout: $160.00                                   │
├─────────────────────────────────────────────────────────────┤
│  User Balance: $899.80 + $160.00 = $1059.80                 │
│  Treasure Wallet: $0.20 (no change yet)                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│           STEP 3: REQUEST WITHDRAWAL                        │
│  • User Requests: $160.00 (their winnings)                  │
│  • Win Fee: 1.5%                                            │
│  • Win Fee Amount: $160.00 × 1.5% = $2.40                  │
│                                                              │
│  Win Fee Flow:                                               │
│  $2.40 ──→ Treasure Wallet                                  │
├─────────────────────────────────────────────────────────────┤
│  Amount to User: $160.00 - $2.40 = $157.60                  │
│  User Wallet: $1059.80 - $160.00 + $157.60 = $1057.40       │
│  Treasure Wallet: $0.20 + $2.40 = $2.60 ✅                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    FINAL STATE                               │
│  User Wallet: $1057.40                                      │
│    └─ Net Gain: $57.40 ($1000 → $1057.40)                  │
│    └─ Breakdown: +$160 win - $2.40 fee = +$157.60          │
│    └─ Plus: -$100.20 initial bet already deducted          │
│                                                              │
│  Treasure Wallet: $2.60                                     │
│    └─ Base Fee: $0.20                                       │
│    └─ Win Fee: $2.40                                        │
│    └─ Total Collected: $2.60 ✅                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 💰 FEE COLLECTION SUMMARY

### Per Transaction Type

```
╔════════════════════════════════════════════════════════════╗
║                   FEE COLLECTION FLOW                      ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║ 1. BET PLACEMENT                                          ║
║    Fee: $0.20 (fixed)                                    ║
║    Destination: 0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC
║    Frequency: Every single bet                           ║
║    Status: CHARGED IMMEDIATELY ✅                         ║
║                                                            ║
║ 2. WITHDRAWAL                                             ║
║    Fee: 1.5% of withdrawal amount                         ║
║    Destination: 0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC
║    Frequency: Only when withdrawing winnings             ║
║    Status: DEDUCTED ON WITHDRAWAL ✅                      ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

---

## 📊 Example: Multiple Users

```
MARKET: Likes Total for @alice (Over 100)
DURATION: 24 hours
THRESHOLD: 100 likes

USER 1: Bets OVER $10
├─ Bet Amount: $10.00
├─ Base Fee: $0.20
└─ Total Charged: $10.20 → Treasure: $0.20

USER 2: Bets OVER $20
├─ Bet Amount: $20.00
├─ Base Fee: $0.20
└─ Total Charged: $20.20 → Treasure: $0.20

USER 3: Bets UNDER $15
├─ Bet Amount: $15.00
├─ Base Fee: $0.20
└─ Total Charged: $15.20 → Treasure: $0.20

MARKET SETTLES: @alice got 125 likes (OVER wins)

PAYOUT CALCULATION:
├─ Total Pool: $45.00
├─ Losing Pool (30%): $13.50
├─ Winner Pool Distribution: 50% for each over-bettor
│
├─ USER 1 Winnings: $10.00 + $6.75 = $16.75
├─ USER 2 Winnings: $20.00 + $6.75 = $26.75

USER 1 WITHDRAWS $16.75:
├─ Win Fee (1.5%): $0.25
├─ Amount to User: $16.50
└─ Treasure: $0.25 ✅

USER 2 WITHDRAWS $26.75:
├─ Win Fee (1.5%): $0.40
├─ Amount to User: $26.35
└─ Treasure: $0.40 ✅

TREASURE WALLET TOTAL:
├─ Base Fees: $0.20 × 3 = $0.60
├─ Win Fees: $0.25 + $0.40 = $0.65
└─ TOTAL COLLECTED: $1.25 ✅
```

---

## 🔄 Fee Flow Diagram

```
                    TREASURE WALLET
                  0xf2B6664bF4d507...
                           ▲
                           │
                ┌──────────┼──────────┐
                │          │          │
          BASE FEES    WIN FEES   AUDIT LOG
          ($0.20)      (1.5%)     (all fees)
                │          │          │
                ↓          ↓          ↓
         ┌───────────┬───────────────────────┐
         │           │                       │
    BETTING      WITHDRAWAL            MONITORING
    PHASE        PHASE                 & REPORTING
         │           │                       │
         ↓           ↓                       ↓
   User Places    User Requests        Admin Views
   Bet $X         Withdrawal $Y         Fee Report
         │           │                       │
         └──────────┬────────────────────────┘
                    │
                    ↓
            FEE COLLECTED ✅
```

---

## 💡 Key Points

### Base Fee ($0.20)
- ✅ Charged IMMEDIATELY when bet is placed
- ✅ Fixed amount per bet (not percentage-based)
- ✅ Sent to treasure wallet before market starts
- ✅ No refunds if bet loses
- ✅ Applies to ALL bets regardless of size

### Win Fee (1.5%)
- ✅ Charged ONLY on withdrawal
- ✅ Percentage-based on winnings
- ✅ Only charged if user wins and withdraws
- ✅ Sent to treasure wallet with withdrawal
- ✅ Deducted before transfer to user

### Treasure Wallet
- ✅ Central fee collection address
- ✅ Receives ALL base fees
- ✅ Receives ALL win fees
- ✅ Address: `0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC`
- ✅ No user funds stored here
- ✅ Pure fee collection

---

## 📝 Transaction Receipt Example

```
════════════════════════════════════════════════════
  FARCASTER PREDICTION MARKET - RECEIPT
════════════════════════════════════════════════════

Transaction Type: BET PLACEMENT
Date: October 29, 2025 10:30:45 UTC
Status: ✅ CONFIRMED

Market: Casts Count for @alice (Over 5 in 24h)
Your Prediction: OVER
Your Wallet: 0x1111...1111

CHARGES:
├─ Bet Amount        $10.00
├─ Base Fee (Fixed)   $0.20
├─ Service Charge     $0.00
└─ TOTAL CHARGED     $10.20

TRANSACTION ID: 0xbet_1_5_1761695570

FEES BREAKDOWN:
├─ Base Fee: $0.20 → 0xf2B664...7fC ✅
└─ Total Fees Collected: $0.20

YOUR NEXT STEPS:
1. Wait 24 hours for market to settle
2. Check result (actual casts vs 5)
3. If you win, request withdrawal
4. Winnings transferred (minus 1.5% fee)

════════════════════════════════════════════════════
Questions? See PREDICTION_MARKET_GUIDE.md
════════════════════════════════════════════════════
```

---

## ✅ Fee Implementation Checklist

- ✅ Base fee calculation: $0.20 fixed
- ✅ Win fee calculation: 1.5% percentage
- ✅ Treasure wallet address: 0xf2B664...
- ✅ Base fee charged on bet placement
- ✅ Win fee charged on withdrawal
- ✅ Fees sent to treasure wallet
- ✅ Database recording of all fees
- ✅ User balance tracking
- ✅ Withdrawal deduction logic
- ✅ Audit trail complete

---

For more information, see: **PREDICTION_MARKET_GUIDE.md**