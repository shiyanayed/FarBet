"""
Farcaster Frame Integration for Prediction Market UI
Provides interactive frames for betting, viewing markets, and withdrawals
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import json
import os

frame_bp = Blueprint('frame', __name__, url_prefix='/frame')


# ==================== FRAME ROUTES ====================

@frame_bp.route('/markets', methods=['POST'])
def markets_frame():
    """Display active prediction markets"""
    try:
        body = request.json
        
        # Get active markets
        from database import MarketEvent
        markets = MarketEvent.query.filter_by(status='active').limit(10).all()
        
        if not markets:
            return create_frame({
                'title': 'Prediction Markets',
                'content': 'No active markets available',
                'buttons': [
                    {'label': 'Refresh', 'action': 'post', 'target': '/frame/markets'},
                    {'label': 'Create Market', 'action': 'post', 'target': '/frame/create-market'}
                ]
            })
        
        # Build market list
        market_text = "**Active Prediction Markets**\n\n"
        for i, market in enumerate(markets[:3], 1):
            market_text += f"{i}. **{market.market_type.replace('_', ' ').title()}**\n"
            market_text += f"   Target: {market.threshold} ({market.direction.upper()})\n"
            market_text += f"   Pool: ${market.total_pool:.2f}\n"
            market_text += f"   Bets: {len(market.bets)}\n\n"
        
        return create_frame({
            'title': 'Prediction Markets',
            'content': market_text,
            'image': 'https://via.placeholder.com/1200x630?text=Farcaster+Prediction+Markets',
            'buttons': [
                {'label': 'View Details', 'action': 'post', 'target': '/frame/market-details'},
                {'label': 'Place Bet', 'action': 'post', 'target': '/frame/place-bet'},
                {'label': 'Create New', 'action': 'post', 'target': '/frame/create-market'}
            ]
        })
    except Exception as e:
        return create_error_frame(str(e))


@frame_bp.route('/create-market', methods=['POST'])
def create_market_frame():
    """Create a new prediction market"""
    try:
        body = request.json
        user_fid = body.get('interactor', {}).get('fid')
        
        if not user_fid:
            return create_error_frame('User not authenticated')
        
        # Get user input
        input_text = body.get('text_input', '')
        
        # Parse market creation input
        # Format: "username casts_count 5 24" -> predict casts for username will be >5 in 24 hours
        
        if not input_text:
            return create_frame({
                'title': 'Create Prediction Market',
                'content': 'Enter prediction details:\nFormat: @username metric threshold hours\nExample: @alice casts_count 5 24',
                'image': 'https://via.placeholder.com/1200x630?text=Create+Market',
                'buttons': [
                    {'label': 'Back', 'action': 'post', 'target': '/frame/markets'}
                ]
            }, input_field=True)
        
        # Parse and validate input
        parts = input_text.split()
        if len(parts) < 4:
            return create_error_frame('Invalid format. Use: @username metric threshold hours')
        
        username = parts[0].lstrip('@')
        market_type = parts[1]  # 'casts_count', 'likes_total', 'engagement_score'
        try:
            threshold = float(parts[2])
            hours = int(parts[3])
        except ValueError:
            return create_error_frame('Invalid threshold or hours')
        
        # Validate market type
        valid_types = ['casts_count', 'likes_total', 'engagement_score']
        if market_type not in valid_types:
            return create_error_frame(f'Invalid metric. Use: {", ".join(valid_types)}')
        
        # Create market
        from project import db
        from database import MarketEvent, UserProfile
        
        # Get target user's FID
        target_user = UserProfile.query.filter_by(username=username).first()
        if not target_user:
            return create_error_frame(f'User {username} not found')
        
        market = MarketEvent(
            user_fid=target_user.fid,
            market_type=market_type,
            threshold=threshold,
            direction='over',
            end_time=datetime.utcnow() + timedelta(hours=hours),
            status='active'
        )
        
        db.session.add(market)
        db.session.commit()
        
        return create_frame({
            'title': 'Market Created!',
            'content': f'New prediction market created:\n\n' +
                      f'**Target:** @{username}\n' +
                      f'**Metric:** {market_type.replace("_", " ").title()}\n' +
                      f'**Threshold:** {threshold}\n' +
                      f'**Duration:** {hours} hours\n\n' +
                      f'Market ID: {market.id}',
            'image': 'https://via.placeholder.com/1200x630?text=Market+Created',
            'buttons': [
                {'label': 'Place Bet', 'action': 'post', 'target': '/frame/place-bet'},
                {'label': 'View Markets', 'action': 'post', 'target': '/frame/markets'}
            ]
        })
    except Exception as e:
        return create_error_frame(str(e))


@frame_bp.route('/place-bet', methods=['POST'])
def place_bet_frame():
    """Place a bet on a market"""
    try:
        body = request.json
        user_fid = body.get('interactor', {}).get('fid')
        user_wallet = body.get('interactor', {}).get('verified_addresses', {}).get('eth_addresses', [None])[0]
        
        if not user_fid or not user_wallet:
            return create_error_frame('Wallet verification required')
        
        input_text = body.get('text_input', '')
        
        if not input_text:
            return create_frame({
                'title': 'Place Bet',
                'content': 'Enter your bet:\nFormat: market_id prediction amount\nExample: 1 over 10\n\n' +
                          'Prediction: over or under\n' +
                          'Amount: USD amount to bet',
                'image': 'https://via.placeholder.com/1200x630?text=Place+Bet',
                'buttons': [
                    {'label': 'Back', 'action': 'post', 'target': '/frame/markets'}
                ]
            }, input_field=True)
        
        # Parse bet input
        parts = input_text.split()
        if len(parts) < 3:
            return create_error_frame('Invalid format. Use: market_id prediction amount')
        
        try:
            market_id = int(parts[0])
            prediction = parts[1].lower()  # 'over' or 'under'
            amount = float(parts[2])
        except ValueError:
            return create_error_frame('Invalid market ID, prediction, or amount')
        
        if prediction not in ['over', 'under']:
            return create_error_frame('Prediction must be "over" or "under"')
        
        if amount <= 0:
            return create_error_frame('Amount must be greater than 0')
        
        # Place bet via API
        import requests
        
        response = requests.post('http://localhost:5000/api/bets/place', json={
            'market_id': market_id,
            'user_fid': user_fid,
            'prediction': prediction,
            'amount': amount,
            'user_wallet': user_wallet
        })
        
        if response.status_code != 201:
            return create_error_frame(response.json().get('error', 'Failed to place bet'))
        
        bet_data = response.json()
        
        return create_frame({
            'title': 'Bet Placed Successfully!',
            'content': f'Bet confirmed:\n\n' +
                      f'**Market ID:** {market_id}\n' +
                      f'**Prediction:** {prediction.upper()}\n' +
                      f'**Amount:** ${amount:.2f}\n' +
                      f'**Base Fee:** $0.20\n' +
                      f'**Total Cost:** ${amount + 0.20:.2f}\n\n' +
                      f'Bet ID: {bet_data.get("bet_id")}\n' +
                      f'TX: {bet_data.get("transaction", "...")[:16]}...',
            'image': 'https://via.placeholder.com/1200x630?text=Bet+Placed',
            'buttons': [
                {'label': 'View My Bets', 'action': 'post', 'target': '/frame/my-bets'},
                {'label': 'Markets', 'action': 'post', 'target': '/frame/markets'}
            ]
        })
    except Exception as e:
        return create_error_frame(str(e))


@frame_bp.route('/my-bets', methods=['POST'])
def my_bets_frame():
    """Display user's bets"""
    try:
        body = request.json
        user_fid = body.get('interactor', {}).get('fid')
        
        if not user_fid:
            return create_error_frame('User not authenticated')
        
        import requests
        
        response = requests.get(f'http://localhost:5000/api/bets/user/{user_fid}')
        
        if response.status_code != 200:
            return create_error_frame('Failed to fetch bets')
        
        bets = response.json().get('bets', [])
        
        if not bets:
            return create_frame({
                'title': 'My Bets',
                'content': 'You have no bets yet. Start predicting!',
                'image': 'https://via.placeholder.com/1200x630?text=No+Bets',
                'buttons': [
                    {'label': 'Place Bet', 'action': 'post', 'target': '/frame/place-bet'},
                    {'label': 'Markets', 'action': 'post', 'target': '/frame/markets'}
                ]
            })
        
        # Build bets list
        bets_text = "**Your Bets**\n\n"
        for i, bet in enumerate(bets[:5], 1):
            status_emoji = {'active': '🟡', 'won': '✅', 'lost': '❌', 'pending': '⏳'}
            status = status_emoji.get(bet['status'], '❓')
            
            bets_text += f"{i}. {status} Market #{bet['market_id']}\n"
            bets_text += f"   Prediction: {bet['prediction'].upper()}\n"
            bets_text += f"   Amount: ${bet['amount']:.2f}\n"
            if bet['payout']:
                bets_text += f"   Payout: ${bet['payout']:.2f}\n"
            bets_text += "\n"
        
        return create_frame({
            'title': 'My Bets',
            'content': bets_text,
            'image': 'https://via.placeholder.com/1200x630?text=My+Bets',
            'buttons': [
                {'label': 'Place Bet', 'action': 'post', 'target': '/frame/place-bet'},
                {'label': 'Withdraw', 'action': 'post', 'target': '/frame/withdraw'},
                {'label': 'Markets', 'action': 'post', 'target': '/frame/markets'}
            ]
        })
    except Exception as e:
        return create_error_frame(str(e))


@frame_bp.route('/withdraw', methods=['POST'])
def withdraw_frame():
    """Request withdrawal of winnings"""
    try:
        body = request.json
        user_fid = body.get('interactor', {}).get('fid')
        user_wallet = body.get('interactor', {}).get('verified_addresses', {}).get('eth_addresses', [None])[0]
        
        if not user_fid or not user_wallet:
            return create_error_frame('Wallet verification required')
        
        input_text = body.get('text_input', '')
        
        if not input_text:
            # Show balance first
            import requests
            
            response = requests.get(f'http://localhost:5000/api/users/{user_fid}')
            
            if response.status_code == 200:
                balance = response.json().get('user', {}).get('stats', {}).get('balance', 0)
                balance_text = f'**Available Balance:** ${balance:.2f}'
            else:
                balance_text = 'Could not fetch balance'
            
            return create_frame({
                'title': 'Withdraw Winnings',
                'content': f'{balance_text}\n\n' +
                          'Enter amount to withdraw:\nExample: 10.50',
                'image': 'https://via.placeholder.com/1200x630?text=Withdraw',
                'buttons': [
                    {'label': 'Back', 'action': 'post', 'target': '/frame/my-bets'}
                ]
            }, input_field=True)
        
        try:
            amount = float(input_text)
        except ValueError:
            return create_error_frame('Invalid amount')
        
        if amount <= 0:
            return create_error_frame('Amount must be greater than 0')
        
        # Request withdrawal via API
        import requests
        
        response = requests.post('http://localhost:5000/api/withdrawals/request', json={
            'user_fid': user_fid,
            'user_wallet': user_wallet,
            'amount': amount
        })
        
        if response.status_code != 201:
            return create_error_frame(response.json().get('error', 'Failed to request withdrawal'))
        
        withdrawal_data = response.json()
        
        return create_frame({
            'title': 'Withdrawal Requested!',
            'content': f'Withdrawal requested:\n\n' +
                      f'**Amount:** ${amount:.2f}\n' +
                      f'**Wallet:** {user_wallet[:6]}...{user_wallet[-4:]}\n' +
                      f'**Status:** Pending\n\n' +
                      f'Withdrawal ID: {withdrawal_data.get("withdrawal_id")}\n' +
                      f'Your funds will be transferred shortly.',
            'image': 'https://via.placeholder.com/1200x630?text=Withdrawal+Pending',
            'buttons': [
                {'label': 'My Bets', 'action': 'post', 'target': '/frame/my-bets'},
                {'label': 'Markets', 'action': 'post', 'target': '/frame/markets'}
            ]
        })
    except Exception as e:
        return create_error_frame(str(e))


@frame_bp.route('/profile', methods=['POST'])
def profile_frame():
    """Display user profile and statistics"""
    try:
        body = request.json
        user_fid = body.get('interactor', {}).get('fid')
        
        if not user_fid:
            return create_error_frame('User not authenticated')
        
        import requests
        
        response = requests.get(f'http://localhost:5000/api/users/{user_fid}')
        
        if response.status_code != 200:
            return create_error_frame('Failed to fetch profile')
        
        user_data = response.json().get('user', {})
        stats = user_data.get('stats', {})
        
        profile_text = f"**@{user_data.get('username', 'Unknown')}**\n\n"
        profile_text += f"📊 **Statistics**\n"
        profile_text += f"• Total Bets: {stats.get('total_bets', 0)}\n"
        profile_text += f"• Won: {stats.get('won_bets', 0)}\n"
        profile_text += f"• Win Rate: {stats.get('win_rate', 0):.1f}%\n"
        profile_text += f"• Total Wagered: ${stats.get('total_wagered', 0):.2f}\n"
        profile_text += f"• Total Winnings: ${stats.get('total_winnings', 0):.2f}\n"
        profile_text += f"• Available Balance: ${stats.get('balance', 0):.2f}\n"
        
        return create_frame({
            'title': 'My Profile',
            'content': profile_text,
            'image': 'https://via.placeholder.com/1200x630?text=Profile',
            'buttons': [
                {'label': 'My Bets', 'action': 'post', 'target': '/frame/my-bets'},
                {'label': 'Withdraw', 'action': 'post', 'target': '/frame/withdraw'},
                {'label': 'Markets', 'action': 'post', 'target': '/frame/markets'}
            ]
        })
    except Exception as e:
        return create_error_frame(str(e))


# ==================== HELPER FUNCTIONS ====================

def create_frame(data, input_field=False):
    """Create a Farcaster Frame response"""
    buttons = []
    for btn in data.get('buttons', []):
        buttons.append({
            'label': btn['label'],
            'action': btn.get('action', 'post'),
            'target': btn.get('target', '')
        })
    
    frame = {
        'title': data.get('title', ''),
        'description': data.get('content', ''),
        'imageUrl': data.get('image', 'https://via.placeholder.com/1200x630?text=Farcaster+Market'),
        'buttons': buttons
    }
    
    if input_field:
        frame['input'] = {
            'text': 'Enter input...'
        }
    
    return jsonify({'frames': [frame]})


def create_error_frame(error_message):
    """Create an error frame"""
    return create_frame({
        'title': 'Error',
        'content': f'❌ {error_message}',
        'image': 'https://via.placeholder.com/1200x630?text=Error',
        'buttons': [
            {'label': 'Back', 'action': 'post', 'target': '/frame/markets'}
        ]
    })


# Register blueprint
def register_frame_routes(app):
    """Register frame routes with Flask app"""
    app.register_blueprint(frame_bp)