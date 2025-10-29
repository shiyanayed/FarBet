"""
Farcaster Prediction Market - Main Application
A prediction market platform built on Farcaster for betting on user activity metrics
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv
import requests
import hmac
import hashlib
# eth_keys and eth_utils imports removed for development mode

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
FARCASTER_HUB_URL = os.getenv("FARCASTER_HUB_URL", "https://hub.farcaster.builders")
NEYNAR_API_KEY = os.getenv("NEYNAR_API_KEY", "")
TREASURE_WALLET = "0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC"
BASE_FEE = 0.2  # $0.2
WIN_FEE_PERCENTAGE = 1.5  # 1.5%

# Import database and models
from database import db, Bet, MarketEvent, UserProfile, Withdrawal
from blockchain import WalletManager, TransactionHandler

# Note: Database initialization is handled in main.py create_app()

# Initialize blockchain handlers
wallet_manager = WalletManager()
tx_handler = TransactionHandler()


# ==================== MARKET ENDPOINTS ====================

@app.route('/api/markets', methods=['GET'])
def get_markets():
    """Get all active prediction markets"""
    try:
        markets = MarketEvent.query.filter_by(status='active').all()
        return jsonify({
            'success': True,
            'markets': [market.to_dict() for market in markets]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/markets/create', methods=['POST'])
def create_market():
    """Create a new prediction market"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['user_fid', 'market_type', 'threshold', 'duration_hours']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        market_type = data['market_type']  # 'casts_count', 'likes_total', 'engagement_score'
        
        market = MarketEvent(
            user_fid=data['user_fid'],
            market_type=market_type,
            threshold=data['threshold'],
            direction=data.get('direction', 'over'),  # 'over' or 'under'
            end_time=datetime.utcnow() + timedelta(hours=data['duration_hours']),
            status='active'
        )
        
        db.session.add(market)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'market_id': market.id,
            'market': market.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== BETTING ENDPOINTS ====================

@app.route('/api/bets/place', methods=['POST'])
def place_bet():
    """Place a bet on a market"""
    try:
        data = request.json
        
        required_fields = ['market_id', 'user_fid', 'prediction', 'amount', 'user_wallet']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        market = MarketEvent.query.get(data['market_id'])
        if not market:
            return jsonify({'success': False, 'error': 'Market not found'}), 404
        
        if market.status != 'active':
            return jsonify({'success': False, 'error': 'Market is not active'}), 400
        
        # Calculate fees
        bet_amount = float(data['amount'])
        total_cost = bet_amount + BASE_FEE
        
        # Create bet record
        bet = Bet(
            market_id=data['market_id'],
            user_fid=data['user_fid'],
            user_wallet=data['user_wallet'],
            prediction=data['prediction'],  # 'yes' or 'no'
            amount=bet_amount,
            base_fee=BASE_FEE,
            status='pending',
            placed_at=datetime.utcnow()
        )
        
        # Process wallet transaction
        tx_result = wallet_manager.process_bet_payment(
            from_wallet=data['user_wallet'],
            amount=total_cost,
            bet_id=bet.id,
            market_id=data['market_id']
        )
        
        if not tx_result['success']:
            return jsonify({
                'success': False,
                'error': f"Transaction failed: {tx_result['error']}"
            }), 400
        
        # Send base fee to treasure wallet
        fee_tx = tx_handler.send_transaction(
            to_address=TREASURE_WALLET,
            amount=BASE_FEE,
            description=f"Market prediction base fee for bet {bet.id}"
        )
        
        bet.transaction_hash = tx_result['hash']
        bet.status = 'active'
        
        db.session.add(bet)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'bet_id': bet.id,
            'message': 'Bet placed successfully',
            'transaction': tx_result['hash'],
            'total_cost': total_cost
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/bets/<int:bet_id>', methods=['GET'])
def get_bet(bet_id):
    """Get bet details"""
    try:
        bet = Bet.query.get(bet_id)
        if not bet:
            return jsonify({'success': False, 'error': 'Bet not found'}), 404
        
        return jsonify({
            'success': True,
            'bet': bet.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/bets/user/<int:fid>', methods=['GET'])
def get_user_bets(fid):
    """Get all bets for a user"""
    try:
        bets = Bet.query.filter_by(user_fid=fid).all()
        return jsonify({
            'success': True,
            'bets': [bet.to_dict() for bet in bets]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== MARKET SETTLEMENT ENDPOINTS ====================

@app.route('/api/markets/<int:market_id>/settle', methods=['POST'])
def settle_market(market_id):
    """Settle a market and determine winners"""
    try:
        market = MarketEvent.query.get(market_id)
        if not market:
            return jsonify({'success': False, 'error': 'Market not found'}), 404
        
        if market.status != 'active':
            return jsonify({'success': False, 'error': 'Market is not active'}), 400
        
        # Fetch actual data for the user
        actual_value = fetch_user_metrics(market.user_fid, market.market_type)
        
        # Determine winners
        winners = []
        losers = []
        
        for bet in market.bets:
            is_winner = determine_winner(
                bet.prediction,
                actual_value,
                market.threshold,
                market.direction
            )
            
            if is_winner:
                winners.append(bet)
                bet.status = 'won'
            else:
                losers.append(bet)
                bet.status = 'lost'
        
        # Calculate payouts
        total_pool = sum(bet.amount for bet in market.bets)
        
        for winner_bet in winners:
            # Calculate win amount based on odds
            payout = calculate_payout(
                bet_amount=winner_bet.amount,
                total_pool=total_pool,
                winner_count=len(winners)
            )
            
            # Apply 1.5% fee on winnings
            win_fee = payout * (WIN_FEE_PERCENTAGE / 100)
            net_payout = payout - win_fee
            
            winner_bet.payout = net_payout
            winner_bet.fee_on_win = win_fee
            
            # Send fee to treasure wallet
            tx_handler.send_transaction(
                to_address=TREASURE_WALLET,
                amount=win_fee,
                description=f"Win fee for bet {winner_bet.id}"
            )
        
        market.status = 'settled'
        market.settled_at = datetime.utcnow()
        market.result_value = actual_value
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'market_id': market_id,
            'result_value': actual_value,
            'winners_count': len(winners),
            'losers_count': len(losers),
            'total_pool': total_pool
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== WITHDRAWAL ENDPOINTS ====================

@app.route('/api/withdrawals/request', methods=['POST'])
def request_withdrawal():
    """Request withdrawal of winnings"""
    try:
        data = request.json
        
        required_fields = ['user_fid', 'user_wallet', 'amount']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        # Verify user has enough balance
        user_balance = calculate_user_balance(data['user_fid'])
        if user_balance < float(data['amount']):
            return jsonify({
                'success': False,
                'error': f'Insufficient balance. Available: ${user_balance}'
            }), 400
        
        withdrawal = Withdrawal(
            user_fid=data['user_fid'],
            user_wallet=data['user_wallet'],
            amount=float(data['amount']),
            status='pending',
            requested_at=datetime.utcnow()
        )
        
        db.session.add(withdrawal)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'withdrawal_id': withdrawal.id,
            'message': 'Withdrawal request submitted'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/withdrawals/<int:withdrawal_id>/process', methods=['POST'])
def process_withdrawal(withdrawal_id):
    """Process a withdrawal"""
    try:
        withdrawal = Withdrawal.query.get(withdrawal_id)
        if not withdrawal:
            return jsonify({'success': False, 'error': 'Withdrawal not found'}), 404
        
        if withdrawal.status != 'pending':
            return jsonify({'success': False, 'error': 'Withdrawal is not pending'}), 400
        
        # Send funds to user wallet
        tx_result = tx_handler.send_transaction(
            to_address=withdrawal.user_wallet,
            amount=withdrawal.amount,
            description=f"Withdrawal payout for user {withdrawal.user_fid}"
        )
        
        if tx_result['success']:
            withdrawal.status = 'completed'
            withdrawal.transaction_hash = tx_result['hash']
            withdrawal.processed_at = datetime.utcnow()
        else:
            withdrawal.status = 'failed'
            withdrawal.error_message = tx_result['error']
        
        db.session.commit()
        
        return jsonify({
            'success': tx_result['success'],
            'withdrawal_id': withdrawal_id,
            'status': withdrawal.status,
            'transaction': tx_result.get('hash')
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== USER PROFILE ENDPOINTS ====================

@app.route('/api/users/<int:fid>', methods=['GET'])
def get_user_profile(fid):
    """Get user profile and statistics"""
    try:
        user = UserProfile.query.filter_by(fid=fid).first()
        if not user:
            # Try to fetch from Farcaster and create profile
            fc_user = fetch_farcaster_user(fid)
            if not fc_user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            user = UserProfile(
                fid=fid,
                username=fc_user.get('username'),
                display_name=fc_user.get('display_name'),
                pfp_url=fc_user.get('pfp_url'),
                wallet_address=fc_user.get('verified_addresses', {}).get('eth_addresses', [None])[0]
            )
            db.session.add(user)
            db.session.commit()
        
        # Get user stats
        total_bets = Bet.query.filter_by(user_fid=fid).count()
        won_bets = Bet.query.filter_by(user_fid=fid, status='won').count()
        total_wagered = db.session.query(db.func.sum(Bet.amount)).filter_by(user_fid=fid).scalar() or 0
        total_winnings = db.session.query(db.func.sum(Bet.payout)).filter_by(user_fid=fid, status='won').scalar() or 0
        
        return jsonify({
            'success': True,
            'user': {
                'fid': user.fid,
                'username': user.username,
                'display_name': user.display_name,
                'wallet': user.wallet_address,
                'stats': {
                    'total_bets': total_bets,
                    'won_bets': won_bets,
                    'win_rate': (won_bets / total_bets * 100) if total_bets > 0 else 0,
                    'total_wagered': float(total_wagered),
                    'total_winnings': float(total_winnings),
                    'balance': calculate_user_balance(fid)
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== HELPER FUNCTIONS ====================

def fetch_user_metrics(fid, metric_type):
    """Fetch user metrics from Farcaster"""
    try:
        headers = {'Authorization': f'Bearer {NEYNAR_API_KEY}'}
        
        if metric_type == 'casts_count':
            # Get number of casts in last 24 hours
            url = f"{FARCASTER_HUB_URL}/api/v1/casts"
            params = {'fid': fid, 'limit': 1000}
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                casts = response.json().get('data', {}).get('casts', [])
                # Filter casts from last 24 hours
                now = datetime.utcnow()
                recent_casts = [c for c in casts if datetime.fromisoformat(c.get('created_at', '')) > now - timedelta(hours=24)]
                return len(recent_casts)
        
        elif metric_type == 'likes_total':
            # Get total likes in last 24 hours
            url = f"{FARCASTER_HUB_URL}/api/v1/user/likes"
            params = {'fid': fid}
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                likes_data = response.json().get('data', {})
                return likes_data.get('total_likes', 0)
        
        elif metric_type == 'engagement_score':
            # Calculate engagement score
            url = f"{FARCASTER_HUB_URL}/api/v1/user/stats"
            params = {'fid': fid}
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                stats = response.json().get('data', {})
                engagement = (stats.get('followers_count', 0) * 0.3 + 
                            stats.get('following_count', 0) * 0.2 +
                            stats.get('casts_count', 0) * 0.5)
                return engagement
        
        return 0
    except Exception as e:
        print(f"Error fetching metrics: {e}")
        return 0


def fetch_farcaster_user(fid):
    """Fetch user information from Farcaster"""
    try:
        headers = {'Authorization': f'Bearer {NEYNAR_API_KEY}'}
        url = f"{FARCASTER_HUB_URL}/api/v1/user"
        params = {'fid': fid}
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json().get('data', {})
        return None
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None


def determine_winner(prediction, actual_value, threshold, direction):
    """Determine if a bet prediction is correct"""
    if prediction == 'over' or direction == 'over':
        return actual_value > threshold
    else:  # 'under'
        return actual_value < threshold


def calculate_payout(bet_amount, total_pool, winner_count):
    """Calculate payout for a winning bet"""
    if winner_count == 0:
        return bet_amount
    
    # Split losing pool among winners, plus return original bet
    losing_pool = total_pool * 0.7  # 70% of pool goes to winners
    payout_per_winner = losing_pool / winner_count
    return bet_amount + payout_per_winner


def calculate_user_balance(fid):
    """Calculate available balance for a user"""
    try:
        # Sum of payouts from won bets minus withdrawals
        total_winnings = db.session.query(db.func.sum(Bet.payout)).filter_by(
            user_fid=fid, status='won'
        ).scalar() or 0
        
        total_withdrawn = db.session.query(db.func.sum(Withdrawal.amount)).filter_by(
            user_fid=fid, status='completed'
        ).scalar() or 0
        
        return float(total_winnings) - float(total_withdrawn)
    except Exception as e:
        print(f"Error calculating balance: {e}")
        return 0


# ==================== HEALTH CHECK ====================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run(debug=True, host='0.0.0.0', port=5000)