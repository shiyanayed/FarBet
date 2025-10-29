# Farcaster Prediction Market - API Documentation

## Base URL

```
http://localhost:5000  (development)
https://api.farcastermarket.com  (production)
```

## Authentication

All API requests use bearer token authentication (optional for public endpoints).

```
Authorization: Bearer <token>
```

## Response Format

All responses are JSON with the following structure:

```json
{
  "success": true/false,
  "data": {...},
  "error": "error message if failed"
}
```

## Rate Limiting

- **General endpoints**: 200 requests per hour
- **Betting endpoints**: 50 requests per hour
- **Frame endpoints**: 200 requests per hour

Headers returned:
```
X-RateLimit-Limit: 200
X-RateLimit-Remaining: 199
X-RateLimit-Reset: 1609459200
```

---

## Markets

### Get All Markets

Get list of all active prediction markets.

**Endpoint**: `GET /api/markets`

**Parameters**:
- `status` (optional): Filter by status (active, settled, cancelled)
- `limit` (optional): Limit results (default: 50, max: 100)
- `offset` (optional): Pagination offset (default: 0)

**Example Request**:
```bash
curl http://localhost:5000/api/markets?status=active&limit=10
```

**Response** (200 OK):
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
      "settled_at": null,
      "result_value": null,
      "total_pool": 100.50,
      "bets_count": 5,
      "description": "How many casts will user make?"
    }
  ]
}
```

---

### Create Market

Create a new prediction market.

**Endpoint**: `POST /api/markets/create`

**Request Body**:
```json
{
  "user_fid": 3,
  "market_type": "casts_count",
  "threshold": 5,
  "direction": "over",
  "duration_hours": 24,
  "description": "Optional description"
}
```

**Parameters**:
- `user_fid` (required): FID of the user to predict on
- `market_type` (required): Type of market
  - `casts_count`: Number of casts in period
  - `likes_total`: Total likes received
  - `engagement_score`: Overall engagement metric
- `threshold` (required): Prediction threshold value
- `direction` (required): `over` or `under`
- `duration_hours` (required): Market duration in hours (1-168)
- `description` (optional): Market description

**Example Request**:
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

**Response** (201 Created):
```json
{
  "success": true,
  "market_id": 1,
  "market": {
    "id": 1,
    "user_fid": 3,
    "market_type": "casts_count",
    "threshold": 5,
    "direction": "over",
    "status": "active",
    "created_at": "2024-01-01T12:00:00",
    "end_time": "2024-01-02T12:00:00",
    "total_pool": 0,
    "bets_count": 0
  }
}
```

**Errors**:
- 400: Missing or invalid parameters
- 409: User not found
- 500: Server error

---

## Betting

### Place Bet

Place a bet on a market.

**Endpoint**: `POST /api/bets/place`

**Request Body**:
```json
{
  "market_id": 1,
  "user_fid": 100,
  "prediction": "over",
  "amount": 10.0,
  "user_wallet": "0x742d35Cc6634C0532925a3b844Bc9e7595f42e24"
}
```

**Parameters**:
- `market_id` (required): ID of market to bet on
- `user_fid` (required): Farcaster ID of bettor
- `prediction` (required): `over` or `under`
- `amount` (required): Bet amount in USD (min: 1.0, max: 1000.0)
- `user_wallet` (required): Ethereum address for payment

**Fees**:
- Base fee: $0.20 (charged upfront)
- Total cost = amount + $0.20

**Example Request**:
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

**Response** (201 Created):
```json
{
  "success": true,
  "bet_id": 1,
  "message": "Bet placed successfully",
  "transaction": "0xabc123def456...",
  "total_cost": 10.20
}
```

**Errors**:
- 400: Invalid market, prediction, or amount
- 400: Market not active
- 400: Transaction failed
- 404: Market not found
- 500: Server error

---

### Get Bet Details

Get details of a specific bet.

**Endpoint**: `GET /api/bets/<bet_id>`

**Example Request**:
```bash
curl http://localhost:5000/api/bets/1
```

**Response** (200 OK):
```json
{
  "success": true,
  "bet": {
    "id": 1,
    "market_id": 1,
    "user_fid": 100,
    "user_wallet": "0x742d...",
    "prediction": "over",
    "amount": 10.0,
    "base_fee": 0.20,
    "payout": null,
    "fee_on_win": null,
    "status": "active",
    "transaction_hash": "0xabc123...",
    "placed_at": "2024-01-01T12:00:00",
    "settled_at": null
  }
}
```

---

### Get User Bets

Get all bets placed by a user.

**Endpoint**: `GET /api/bets/user/<fid>`

**Parameters**:
- `status` (optional): Filter by status (pending, active, won, lost)
- `limit` (optional): Limit results (default: 50)

**Example Request**:
```bash
curl http://localhost:5000/api/bets/user/100?status=active
```

**Response** (200 OK):
```json
{
  "success": true,
  "bets": [
    {
      "id": 1,
      "market_id": 1,
      "prediction": "over",
      "amount": 10.0,
      "status": "active",
      "placed_at": "2024-01-01T12:00:00"
    }
  ]
}
```

---

## Market Settlement

### Settle Market

Settle a market and determine winners/losers.

**Endpoint**: `POST /api/markets/<market_id>/settle`

**Example Request**:
```bash
curl -X POST http://localhost:5000/api/markets/1/settle
```

**Response** (200 OK):
```json
{
  "success": true,
  "market_id": 1,
  "result_value": 7,
  "winners_count": 3,
  "losers_count": 2,
  "total_pool": 100.50
}
```

**Payout Calculation**:
```
House takes 30% of pool
Winners split 70% of pool
Each winner gets: (original_bet + share_of_pool)
```

---

## Withdrawals

### Request Withdrawal

Request withdrawal of winnings.

**Endpoint**: `POST /api/withdrawals/request`

**Request Body**:
```json
{
  "user_fid": 100,
  "user_wallet": "0x742d35Cc6634C0532925a3b844Bc9e7595f42e24",
  "amount": 50.0
}
```

**Fees**:
- Win fee: 1.5% on withdrawn amount (charged on successful withdrawal)
- Net received = amount - (amount * 1.5%)

**Example Request**:
```bash
curl -X POST http://localhost:5000/api/withdrawals/request \
  -H "Content-Type: application/json" \
  -d '{
    "user_fid": 100,
    "user_wallet": "0x742d35Cc6634C0532925a3b844Bc9e7595f42e24",
    "amount": 50.0
  }'
```

**Response** (201 Created):
```json
{
  "success": true,
  "withdrawal_id": 1,
  "message": "Withdrawal request submitted"
}
```

**Errors**:
- 400: Insufficient balance
- 400: Invalid amount
- 500: Server error

---

### Process Withdrawal

Process a pending withdrawal (admin endpoint).

**Endpoint**: `POST /api/withdrawals/<withdrawal_id>/process`

**Response** (200 OK):
```json
{
  "success": true,
  "withdrawal_id": 1,
  "status": "completed",
  "transaction": "0xabc123..."
}
```

---

## User Profile

### Get User Profile

Get user profile and statistics.

**Endpoint**: `GET /api/users/<fid>`

**Example Request**:
```bash
curl http://localhost:5000/api/users/100
```

**Response** (200 OK):
```json
{
  "success": true,
  "user": {
    "fid": 100,
    "username": "alice",
    "display_name": "Alice",
    "wallet": "0x742d35Cc6634C0532925a3b844Bc9e7595f42e24",
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

---

## Error Responses

### Common Errors

**400 Bad Request**:
```json
{
  "success": false,
  "error": "Invalid market type"
}
```

**401 Unauthorized**:
```json
{
  "success": false,
  "error": "Missing authorization header"
}
```

**404 Not Found**:
```json
{
  "success": false,
  "error": "Market not found"
}
```

**429 Too Many Requests**:
```json
{
  "success": false,
  "error": "Rate limit exceeded"
}
```

**500 Internal Server Error**:
```json
{
  "success": false,
  "error": "Internal server error"
}
```

---

## Farcaster Frames

### Market Discovery Frame

**URL**: `/frame/markets`

Browse and discover active prediction markets.

---

### Create Market Frame

**URL**: `/frame/create-market`

Create a new prediction market with inputs.

---

### Place Bet Frame

**URL**: `/frame/place-bet`

Place a bet on a market directly.

---

### My Bets Frame

**URL**: `/frame/my-bets`

View all your active and completed bets.

---

### Withdraw Frame

**URL**: `/frame/withdraw`

Request withdrawal of winnings.

---

### Profile Frame

**URL**: `/frame/profile`

View your profile and statistics.

---

## Webhooks (Optional)

### Bet Placed

Fired when a bet is successfully placed.

```json
{
  "event": "bet.placed",
  "bet_id": 1,
  "market_id": 1,
  "user_fid": 100,
  "amount": 10.0,
  "timestamp": "2024-01-01T12:00:00"
}
```

### Market Settled

Fired when a market is settled.

```json
{
  "event": "market.settled",
  "market_id": 1,
  "result_value": 7,
  "winners_count": 3,
  "timestamp": "2024-01-02T12:00:00"
}
```

### Withdrawal Completed

Fired when a withdrawal is processed.

```json
{
  "event": "withdrawal.completed",
  "withdrawal_id": 1,
  "user_fid": 100,
  "amount": 50.0,
  "timestamp": "2024-01-01T12:30:00"
}
```

---

## Code Examples

### JavaScript/Node.js

```javascript
const API_BASE = 'http://localhost:5000';

// Get markets
async function getMarkets() {
  const response = await fetch(`${API_BASE}/api/markets`);
  return response.json();
}

// Place bet
async function placeBet(marketId, fid, prediction, amount, wallet) {
  const response = await fetch(`${API_BASE}/api/bets/place`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      market_id: marketId,
      user_fid: fid,
      prediction,
      amount,
      user_wallet: wallet
    })
  });
  return response.json();
}
```

### Python

```python
import requests

API_BASE = 'http://localhost:5000'

# Get markets
response = requests.get(f'{API_BASE}/api/markets')
markets = response.json()

# Place bet
data = {
    'market_id': 1,
    'user_fid': 100,
    'prediction': 'over',
    'amount': 10.0,
    'user_wallet': '0x742d35Cc6634C0532925a3b844Bc9e7595f42e24'
}
response = requests.post(f'{API_BASE}/api/bets/place', json=data)
result = response.json()
```

### cURL

```bash
# Get markets
curl http://localhost:5000/api/markets

# Place bet
curl -X POST http://localhost:5000/api/bets/place \
  -H "Content-Type: application/json" \
  -d '{"market_id":1,"user_fid":100,"prediction":"over","amount":10.0,"user_wallet":"0x742d35Cc6634C0532925a3b844Bc9e7595f42e24"}'
```

---

## Support

For API issues or questions:
- GitHub Issues: [Report bugs](https://github.com/yourusername/farcaster-prediction-market/issues)
- Discord: [Join community](https://discord.gg/your-invite)
- Email: api-support@farcastermarket.com

---

**Last Updated**: 2024-01-01  
**API Version**: 1.0.0