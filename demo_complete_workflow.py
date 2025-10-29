#!/usr/bin/env python3
"""
Complete Farcaster Prediction Market Workflow Demonstration
Shows all features including fee structure, market creation, betting, and settlement
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"
TREASURE_WALLET = "0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC"

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def print_subsection(title):
    """Print a formatted subsection header"""
    print(f"\n{title}")
    print(f"{'-' * len(title)}\n")

def demo_1_health_check():
    """Demo 1: Health Check"""
    print_section("DEMO 1: HEALTH CHECK")
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"✅ Server Status: {response.status_code}")
    print(f"   Server is running and ready to accept requests")
    print(f"   Timestamp: {response.json()['timestamp']}")

def demo_2_view_markets():
    """Demo 2: View Existing Markets"""
    print_section("DEMO 2: VIEW EXISTING MARKETS")
    
    response = requests.get(f"{BASE_URL}/api/markets")
    markets = response.json().get('markets', [])
    
    print(f"✅ Total Active Markets: {len(markets)}")
    
    if markets:
        print(f"\nMarkets:")
        for i, market in enumerate(markets[:3], 1):
            print(f"\n  Market #{market['id']}:")
            print(f"    Type: {market['market_type'].replace('_', ' ').title()}")
            print(f"    Target User FID: {market['user_fid']}")
            print(f"    Threshold: {market['threshold']}")
            print(f"    Direction: {market['direction'].upper()}")
            print(f"    Status: {market['status']}")
            print(f"    Bets Placed: {market['bets_count']}")
            print(f"    Total Pool: ${market['total_pool']:.2f}")

def demo_3_create_market():
    """Demo 3: Create a New Prediction Market"""
    print_section("DEMO 3: CREATE A NEW PREDICTION MARKET")
    
    print("Creating a market to predict casts for user FID 1234...")
    print("Prediction: @alice will make over 5 casts in the next 24 hours\n")
    
    payload = {
        'user_fid': 1234,
        'market_type': 'casts_count',
        'threshold': 5,
        'direction': 'over',
        'duration_hours': 24
    }
    
    response = requests.post(f"{BASE_URL}/api/markets/create", json=payload)
    market = response.json()['market']
    market_id = market['id']
    
    print(f"✅ Market Created Successfully!")
    print(f"\n📊 Market Details:")
    print(f"   Market ID: {market_id}")
    print(f"   Prediction Type: {market['market_type'].replace('_', ' ').title()}")
    print(f"   Target User: FID {market['user_fid']}")
    print(f"   Threshold: {market['threshold']}")
    print(f"   Direction: {market['direction'].upper()}")
    print(f"   Duration: {market['end_time']}")
    print(f"   Status: {market['status']}")
    
    return market_id

def demo_4_place_bets(market_id):
    """Demo 4: Place Multiple Bets with Fee Collection"""
    print_section("DEMO 4: PLACE BETS (WITH FEE COLLECTION)")
    
    print("Base Fee Structure: $0.20 per bet")
    print("Fee Destination: Treasure Wallet")
    print(f"Address: {TREASURE_WALLET}\n")
    
    bets = [
        {
            'user_fid': 5001,
            'prediction': 'over',
            'amount': 10.0,
            'wallet': '0x1111111111111111111111111111111111111111'
        },
        {
            'user_fid': 5002,
            'prediction': 'over',
            'amount': 15.0,
            'wallet': '0x2222222222222222222222222222222222222222'
        },
        {
            'user_fid': 5003,
            'prediction': 'under',
            'amount': 20.0,
            'wallet': '0x3333333333333333333333333333333333333333'
        }
    ]
    
    placed_bets = []
    total_charged = 0
    total_fees = 0
    
    print("Placing bets...\n")
    
    for i, bet in enumerate(bets, 1):
        payload = {
            'market_id': market_id,
            'user_fid': bet['user_fid'],
            'prediction': bet['prediction'],
            'amount': bet['amount'],
            'user_wallet': bet['wallet']
        }
        
        response = requests.post(f"{BASE_URL}/api/bets/place", json=payload)
        bet_data = response.json()
        
        if response.status_code == 201:
            bet_id = bet_data['bet_id']
            total_cost = bet_data['total_cost']
            base_fee = 0.2
            
            placed_bets.append(bet_id)
            total_charged += total_cost
            total_fees += base_fee
            
            print(f"Bet {i} - ✅ Placed")
            print(f"  Bet ID: {bet_id}")
            print(f"  User: {bet['user_fid']}")
            print(f"  Prediction: {bet['prediction'].upper()}")
            print(f"  Bet Amount: ${bet['amount']:.2f}")
            print(f"  Base Fee: ${base_fee:.2f}")
            print(f"  Total Charged: ${total_cost:.2f}")
            print(f"  Wallet: {bet['wallet']}")
            print()
    
    print(f"✅ Summary:")
    print(f"   Total Bets Placed: {len(placed_bets)}")
    print(f"   Total Amount Wagered: ${sum(b['amount'] for b in bets):.2f}")
    print(f"   Total Fees Collected: ${total_fees:.2f}")
    print(f"   Total Charged: ${total_charged:.2f}")
    print(f"   Market Pool: ${sum(b['amount'] for b in bets):.2f}")
    
    print(f"\n💰 Fee Summary:")
    print(f"   Each $10 bet costs: $10.20 (+ $0.20 fee)")
    print(f"   All fees sent to: {TREASURE_WALLET}")
    
    return placed_bets

def demo_5_user_profile(fid):
    """Demo 5: View User Profile and Statistics"""
    print_section("DEMO 5: VIEW USER PROFILE AND STATISTICS")
    
    response = requests.get(f"{BASE_URL}/api/users/{fid}")
    
    if response.status_code == 200:
        user = response.json()['user']
        stats = user['stats']
        
        print(f"✅ User Profile Retrieved")
        print(f"\n👤 User Information:")
        print(f"   FID: {user['fid']}")
        print(f"   Username: {user.get('username', 'N/A')}")
        print(f"   Display Name: {user.get('display_name', 'N/A')}")
        print(f"   Wallet: {user.get('wallet', 'N/A')}")
        
        print(f"\n📊 Betting Statistics:")
        print(f"   Total Bets: {stats['total_bets']}")
        print(f"   Won Bets: {stats['won_bets']}")
        print(f"   Win Rate: {(stats['won_bets']/stats['total_bets']*100 if stats['total_bets'] > 0 else 0):.1f}%")
        print(f"   Total Wagered: ${stats['total_wagered']:.2f}")
        print(f"   Total Winnings: ${stats['total_winnings']:.2f}")
        print(f"   Current Balance: ${stats['balance']:.2f}")
    else:
        print(f"ℹ️  User profile not yet created (will be created on first bet)")

def demo_6_user_bets(fid):
    """Demo 6: View User's Bets"""
    print_section("DEMO 6: VIEW USER'S BETS")
    
    response = requests.get(f"{BASE_URL}/api/bets/user/{fid}")
    bets = response.json().get('bets', [])
    
    print(f"✅ Retrieved {len(bets)} bets for user {fid}\n")
    
    if bets:
        for i, bet in enumerate(bets, 1):
            print(f"Bet {i}:")
            print(f"  Bet ID: {bet['id']}")
            print(f"  Market ID: {bet['market_id']}")
            print(f"  Prediction: {bet['prediction'].upper()}")
            print(f"  Amount: ${bet['amount']:.2f}")
            print(f"  Status: {bet['status']}")
            print(f"  Placed: {bet['placed_at']}")
            if bet['payout']:
                print(f"  Payout: ${bet['payout']:.2f}")
            print()

def demo_7_withdrawal_flow():
    """Demo 7: Withdrawal Flow with Win Fee"""
    print_section("DEMO 7: WITHDRAWAL FLOW (WITH WIN FEE)")
    
    print("Win Fee Structure: 1.5% on withdrawal")
    print("Fee Destination: Treasure Wallet")
    print(f"Address: {TREASURE_WALLET}\n")
    
    user_fid = 5001
    withdrawal_amount = 50.0
    win_fee_percentage = 1.5
    win_fee = withdrawal_amount * (win_fee_percentage / 100)
    amount_received = withdrawal_amount - win_fee
    
    print(f"Withdrawal Example:")
    print(f"  User FID: {user_fid}")
    print(f"  Requested Amount: ${withdrawal_amount:.2f}")
    print(f"  Win Fee (1.5%): ${win_fee:.2f}")
    print(f"  User Receives: ${amount_received:.2f}\n")
    
    # Request withdrawal
    payload = {
        'user_fid': user_fid,
        'user_wallet': '0x1111111111111111111111111111111111111111',
        'amount': withdrawal_amount
    }
    
    response = requests.post(f"{BASE_URL}/api/withdrawals/request", json=payload)
    
    if response.status_code == 201:
        withdrawal_data = response.json()
        withdrawal_id = withdrawal_data['withdrawal_id']
        
        print(f"✅ Withdrawal Requested")
        print(f"   Withdrawal ID: {withdrawal_id}")
        print(f"\n💰 Fee Breakdown:")
        print(f"   Amount Requested: ${withdrawal_amount:.2f}")
        print(f"   Less Win Fee (1.5%): -${win_fee:.2f}")
        print(f"   Amount to Receive: ${amount_received:.2f}")
        print(f"   To Treasure: ${win_fee:.2f}")
        
        print(f"\n⏳ Withdrawal Status: Pending")
        print(f"   Awaiting admin processing...")
    else:
        print(f"ℹ️  Withdrawal not available (may require winnings first)")

def demo_8_fee_summary():
    """Demo 8: Complete Fee Summary"""
    print_section("DEMO 8: COMPLETE FEE STRUCTURE SUMMARY")
    
    print("📊 FEE STRUCTURE\n")
    
    print("1️⃣  BASE FEE (On Bet Placement):")
    print("   Amount: $0.20")
    print("   When: Charged immediately on bet placement")
    print("   Frequency: Every single bet")
    print("   Destination: Treasure Wallet")
    print("   Status: ✅ ACTIVE\n")
    
    print("2️⃣  WIN FEE (On Withdrawal):")
    print("   Amount: 1.5% of withdrawal amount")
    print("   When: Charged on withdrawal of winnings")
    print("   Frequency: Only when withdrawing")
    print("   Destination: Treasure Wallet")
    print("   Status: ✅ ACTIVE\n")
    
    print("💼 TREASURE WALLET:")
    print(f"   Address: {TREASURE_WALLET}")
    print("   Receives: All base fees + all win fees")
    print("   Status: ✅ CONFIGURED\n")
    
    print("📈 EXAMPLE CALCULATION:")
    print("\n   Scenario: User places $100 bet, wins, withdraws $150\n")
    print("   Step 1 - Place Bet:")
    print("      Bet Amount: $100")
    print("      Base Fee: $0.20")
    print("      Total Charged: $100.20 → Treasure Wallet")
    print("      User Balance: -$100.20\n")
    
    print("   Step 2 - Market Settles (User Wins):")
    print("      Winnings: $150 added to balance")
    print("      User Balance: +$49.80 (150 - 100.20)\n")
    
    print("   Step 3 - Withdraw:")
    print("      Withdrawal Amount: $49.80")
    print("      Win Fee (1.5%): $0.75")
    print("      Amount Received: $49.05 → User Wallet")
    print("      Fee to Treasure: $0.75\n")
    
    print("   Total Fees Collected:")
    print("      Base Fee: $0.20")
    print("      Win Fee: $0.75")
    print("      Total Treasure: $0.95 per cycle")

def main():
    """Run complete workflow demonstration"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  FARCASTER PREDICTION MARKET - COMPLETE WORKFLOW DEMO".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    try:
        # Run demonstrations
        demo_1_health_check()
        time.sleep(0.5)
        
        demo_2_view_markets()
        time.sleep(0.5)
        
        market_id = demo_3_create_market()
        time.sleep(0.5)
        
        demo_4_place_bets(market_id)
        time.sleep(0.5)
        
        demo_5_user_profile(5001)
        time.sleep(0.5)
        
        demo_6_user_bets(5001)
        time.sleep(0.5)
        
        demo_7_withdrawal_flow()
        time.sleep(0.5)
        
        demo_8_fee_summary()
        
        print_section("✅ DEMO COMPLETE")
        print("All features demonstrated successfully!")
        print("\n📚 For detailed API documentation, see: PREDICTION_MARKET_GUIDE.md")
        print("🚀 Server running at: http://localhost:5000")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()