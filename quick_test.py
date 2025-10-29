#!/usr/bin/env python3
import requests
import json

BASE_URL = 'http://localhost:5000'

# Create a market
market_payload = {
    'user_fid': 1234,
    'market_type': 'casts_count',
    'threshold': 5,
    'direction': 'over',
    'duration_hours': 24
}

market_response = requests.post(f'{BASE_URL}/api/markets/create', json=market_payload)
print('✅ Market Creation:')
print(f'Market ID: {market_response.json().get("market_id")}')

if market_response.status_code == 201:
    market_id = market_response.json()['market_id']
    
    # Try to place a bet
    bet_payload = {
        'market_id': market_id,
        'user_fid': 5678,
        'prediction': 'over',
        'amount': 10.0,
        'user_wallet': '0x1234567890123456789012345678901234567890'
    }
    
    bet_response = requests.post(f'{BASE_URL}/api/bets/place', json=bet_payload)
    print('\n✅ Bet Placement:')
    print(f'Status: {bet_response.status_code}')
    bet_data = bet_response.json()
    print(f'Response: {json.dumps(bet_data, indent=2)}')
    
    if bet_response.status_code == 201:
        print(f'\n✅ Bet ID: {bet_data.get("bet_id")}')
        print(f'Total Cost: ${bet_data.get("total_cost")}')
        print(f'\nFee Breakdown:')
        print(f'  - Bet Amount: $10.00')
        print(f'  - Base Fee: $0.20')
        print(f'  - Total: ${bet_data.get("total_cost")}')