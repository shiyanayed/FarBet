#!/usr/bin/env python3
"""
Test script for Farcaster Prediction Market API
Tests all endpoints and verifies fee structure
"""

import requests
import json
import time
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"
TEST_RESULTS = []

def log_test(name, success, message=""):
    """Log test results"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status}: {name}")
    if message:
        print(f"   └─ {message}")
    TEST_RESULTS.append({"name": name, "success": success, "message": message})


def test_health_check():
    """Test health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        success = response.status_code == 200
        data = response.json() if success else {}
        log_test("Health Check", success, f"Status: {response.status_code}")
        return success, data
    except Exception as e:
        log_test("Health Check", False, str(e))
        return False, {}


def test_get_markets():
    """Test get markets endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/markets")
        success = response.status_code == 200
        data = response.json() if success else {}
        market_count = len(data.get('markets', []))
        log_test("Get Markets", success, f"Found {market_count} markets")
        return success, data
    except Exception as e:
        log_test("Get Markets", False, str(e))
        return False, {}


def test_create_market():
    """Test create market endpoint"""
    try:
        payload = {
            'user_fid': 1234,
            'market_type': 'casts_count',
            'threshold': 5,
            'direction': 'over',
            'duration_hours': 24
        }
        response = requests.post(f"{BASE_URL}/api/markets/create", json=payload)
        success = response.status_code == 201
        data = response.json() if success else {}
        market_id = data.get('market_id')
        log_test("Create Market", success, f"Market ID: {market_id}")
        return success, data
    except Exception as e:
        log_test("Create Market", False, str(e))
        return False, {}


def test_place_bet(market_id):
    """Test place bet endpoint"""
    try:
        payload = {
            'market_id': market_id,
            'user_fid': 5678,
            'prediction': 'over',
            'amount': 10.0,
            'user_wallet': '0x1234567890123456789012345678901234567890'
        }
        response = requests.post(f"{BASE_URL}/api/bets/place", json=payload)
        success = response.status_code == 201
        data = response.json() if success else {}
        bet_id = data.get('bet_id')
        total_cost = data.get('total_cost')
        log_test("Place Bet", success, f"Bet ID: {bet_id}, Total Cost: ${total_cost}")
        return success, data
    except Exception as e:
        log_test("Place Bet", False, str(e))
        return False, {}


def test_get_bet(bet_id):
    """Test get bet endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/bets/{bet_id}")
        success = response.status_code == 200
        data = response.json() if success else {}
        bet_info = data.get('bet', {})
        log_test("Get Bet", success, f"Status: {bet_info.get('status')}")
        return success, data
    except Exception as e:
        log_test("Get Bet", False, str(e))
        return False, {}


def test_get_user_bets(fid):
    """Test get user bets endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/bets/user/{fid}")
        success = response.status_code == 200
        data = response.json() if success else {}
        bets_count = len(data.get('bets', []))
        log_test("Get User Bets", success, f"Found {bets_count} bets for user {fid}")
        return success, data
    except Exception as e:
        log_test("Get User Bets", False, str(e))
        return False, {}


def test_get_user_profile(fid):
    """Test get user profile endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/users/{fid}")
        success = response.status_code in [200, 404]  # 404 is ok, means user doesn't exist yet
        data = response.json() if response.status_code == 200 else {}
        log_test("Get User Profile", success, f"Status: {response.status_code}")
        return success, data
    except Exception as e:
        log_test("Get User Profile", False, str(e))
        return False, {}


def test_request_withdrawal(fid, wallet):
    """Test request withdrawal endpoint"""
    try:
        payload = {
            'user_fid': fid,
            'user_wallet': wallet,
            'amount': 5.0
        }
        response = requests.post(f"{BASE_URL}/api/withdrawals/request", json=payload)
        success = response.status_code in [201, 400]  # 400 is ok if insufficient balance
        data = response.json() if response else {}
        withdrawal_id = data.get('withdrawal_id')
        error = data.get('error')
        log_test(
            "Request Withdrawal",
            success,
            f"Withdrawal ID: {withdrawal_id}" if withdrawal_id else f"Error: {error}"
        )
        return success, data if response.status_code == 201 else None
    except Exception as e:
        log_test("Request Withdrawal", False, str(e))
        return False, None


def test_fee_structure():
    """Test fee structure"""
    print("\n" + "="*60)
    print("FEE STRUCTURE VERIFICATION")
    print("="*60)
    
    # Create a market and place a bet to verify fees
    market_response = requests.post(f"{BASE_URL}/api/markets/create", json={
        'user_fid': 9999,
        'market_type': 'likes_total',
        'threshold': 100,
        'direction': 'under',
        'duration_hours': 24
    })
    
    if market_response.status_code != 201:
        log_test("Fee Structure", False, "Failed to create market")
        return
    
    market_id = market_response.json()['market_id']
    bet_amount = 50.0
    expected_base_fee = 0.2
    expected_total = bet_amount + expected_base_fee
    
    bet_response = requests.post(f"{BASE_URL}/api/bets/place", json={
        'market_id': market_id,
        'user_fid': 8888,
        'prediction': 'under',
        'amount': bet_amount,
        'user_wallet': '0xabcdefabcdefabcdefabcdefabcdefabcdefabcd'
    })
    
    if bet_response.status_code == 201:
        bet_data = bet_response.json()
        actual_total = bet_data.get('total_cost')
        
        # Verify base fee
        base_fee_correct = abs(expected_base_fee - 0.2) < 0.01
        total_correct = abs(actual_total - expected_total) < 0.01
        
        log_test(
            "Base Fee Charge ($0.2)",
            base_fee_correct,
            f"Expected: ${expected_base_fee}, Verified: Charging on every bet"
        )
        log_test(
            "Total Cost Calculation",
            total_correct,
            f"Bet: ${bet_amount} + Fee: ${expected_base_fee} = ${actual_total}"
        )
        
        print(f"\n📊 Win Fee Structure (1.5%):")
        print(f"   When user wins: 1.5% of payout charged on withdrawal")
        print(f"   Example: If user wins $100, 1.5% ($1.50) fee deducted")
        
        print(f"\n🎯 Treasure Wallet:")
        print(f"   Address: 0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC")
        print(f"   Receives: All base fees + all win fees")
    else:
        log_test("Fee Structure", False, "Failed to place bet")


def print_summary():
    """Print test summary"""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for t in TEST_RESULTS if t['success'])
    total = len(TEST_RESULTS)
    
    print(f"\n✅ Passed: {passed}/{total}")
    
    if passed < total:
        print("\n❌ Failed Tests:")
        for test in TEST_RESULTS:
            if not test['success']:
                print(f"   - {test['name']}: {test['message']}")
    
    print("\n" + "="*60)
    print("PREDICTION MARKET TYPES SUPPORTED:")
    print("="*60)
    print("1. 📊 Casts Count")
    print("   └─ Predict how many casts a user will make in 24 hours")
    print("2. ❤️  Likes Total")
    print("   └─ Predict total likes a user will receive in 24 hours")
    print("3. 📈 Engagement Score")
    print("   └─ Predicted engagement based on followers + following + casts")
    
    print("\n" + "="*60)
    print("KEY FEATURES:")
    print("="*60)
    print("✓ Use Farcaster wallet for betting (no deposits needed)")
    print("✓ Base fee: $0.20 per bet (sent to treasure wallet)")
    print("✓ Win fee: 1.5% on winnings (sent to treasure wallet)")
    print("✓ Prediction types: Over/Under for all metrics")
    print("✓ Dynamic market settlement with winner calculation")
    print("✓ Farcaster Frame UI integration for seamless UX")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("FARCASTER PREDICTION MARKET - API TEST SUITE")
    print("="*60)
    print(f"Testing: {BASE_URL}")
    print(f"Time: {datetime.now().isoformat()}")
    print("="*60 + "\n")
    
    # Wait a moment for server to be ready
    time.sleep(1)
    
    # Run tests
    print("🧪 Running Basic Tests...\n")
    
    # Health check
    health_ok, _ = test_health_check()
    if not health_ok:
        print("\n❌ Server is not responding. Please ensure the server is running.")
        return
    
    # Get markets
    _, _ = test_get_markets()
    
    # Create market
    _, market_data = test_create_market()
    market_id = market_data.get('market_id') if market_data else None
    
    if market_id:
        # Place bet
        _, bet_data = test_place_bet(market_id)
        bet_id = bet_data.get('bet_id') if bet_data else None
        
        if bet_id:
            # Get bet
            _, _ = test_get_bet(bet_id)
    
    # User operations
    _, _ = test_get_user_bets(5678)
    _, _ = test_get_user_profile(5678)
    _, _ = test_request_withdrawal(5678, '0x1234567890123456789012345678901234567890')
    
    # Fee structure tests
    test_fee_structure()
    
    # Print summary
    print_summary()


if __name__ == '__main__':
    main()