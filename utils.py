"""
Utility functions and helpers for Farcaster Prediction Market
"""

import re
import hashlib
import hmac
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
import requests
import logging

logger = logging.getLogger(__name__)


# ==================== VALIDATION UTILITIES ====================

class Validator:
    """Input validation utilities"""
    
    @staticmethod
    def validate_wallet_address(address):
        """Validate Ethereum wallet address"""
        if not isinstance(address, str):
            return False
        
        pattern = r'^0x[a-fA-F0-9]{40}$'
        return bool(re.match(pattern, address))
    
    @staticmethod
    def validate_username(username):
        """Validate Farcaster username"""
        if not isinstance(username, str):
            return False
        
        if len(username) < 1 or len(username) > 32:
            return False
        
        pattern = r'^[a-zA-Z0-9_.-]+$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def validate_fid(fid):
        """Validate Farcaster ID"""
        try:
            fid_int = int(fid)
            return fid_int > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_amount(amount, min_amount=0.01, max_amount=100000):
        """Validate bet/withdrawal amount"""
        try:
            amount_float = float(amount)
            return min_amount <= amount_float <= max_amount
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_prediction(prediction):
        """Validate prediction (over/under)"""
        return prediction.lower() in ['over', 'under']
    
    @staticmethod
    def validate_market_type(market_type):
        """Validate market type"""
        valid_types = ['casts_count', 'likes_total', 'engagement_score']
        return market_type in valid_types
    
    @staticmethod
    def validate_threshold(threshold):
        """Validate threshold value"""
        try:
            threshold_float = float(threshold)
            return threshold_float >= 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_duration_hours(hours):
        """Validate market duration"""
        try:
            hours_int = int(hours)
            return 1 <= hours_int <= 7 * 24  # 1 hour to 7 days
        except (ValueError, TypeError):
            return False


# ==================== SIGNATURE VERIFICATION ====================

class SignatureVerifier:
    """Verify cryptographic signatures"""
    
    @staticmethod
    def verify_message_signature(message, signature, signer_address):
        """Verify message signature from Ethereum wallet"""
        try:
            from eth_account.messages import encode_defunct
            from eth_account import Account
            
            message_hash = encode_defunct(text=message)
            recovered_address = Account.recover_message(message_hash, signature=signature)
            
            return recovered_address.lower() == signer_address.lower()
        except Exception as e:
            logger.error(f"Signature verification error: {e}")
            return False
    
    @staticmethod
    def generate_nonce():
        """Generate a nonce for message signing"""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    
    @staticmethod
    def create_sign_message(nonce, address, timestamp=None):
        """Create a message for user to sign"""
        if timestamp is None:
            timestamp = datetime.utcnow().isoformat()
        
        message = f"""Sign this message to authenticate with Farcaster Prediction Market.

Address: {address}
Nonce: {nonce}
Timestamp: {timestamp}

This request will not trigger a blockchain transaction or cost any gas fees."""
        
        return message


# ==================== FARCASTER API UTILITIES ====================

class FarcasterAPI:
    """Farcaster API interaction utilities"""
    
    def __init__(self, api_key, base_url="https://api.neynar.com/v2/farcaster"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {'X-API-Key': api_key}
    
    def get_user(self, fid):
        """Fetch user by FID"""
        try:
            url = f"{self.base_url}/user/bulk"
            params = {'fids': str(fid)}
            
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                users = response.json().get('users', [])
                return users[0] if users else None
            
            logger.warning(f"Failed to fetch user {fid}: {response.status_code}")
            return None
        except Exception as e:
            logger.error(f"Error fetching user {fid}: {e}")
            return None
    
    def get_user_casts(self, fid, limit=1000):
        """Fetch user's casts"""
        try:
            url = f"{self.base_url}/user/casts"
            params = {'fid': str(fid), 'limit': limit}
            
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get('casts', [])
            
            logger.warning(f"Failed to fetch casts for {fid}")
            return []
        except Exception as e:
            logger.error(f"Error fetching casts for {fid}: {e}")
            return []
    
    def get_recent_casts(self, fid, hours=24):
        """Get user's casts from last N hours"""
        try:
            casts = self.get_user_casts(fid)
            now = datetime.utcnow()
            cutoff = now - timedelta(hours=hours)
            
            recent_casts = [
                cast for cast in casts
                if self._parse_datetime(cast.get('created_at')) > cutoff
            ]
            
            return recent_casts
        except Exception as e:
            logger.error(f"Error filtering recent casts: {e}")
            return []
    
    def get_user_stats(self, fid):
        """Get user statistics"""
        try:
            url = f"{self.base_url}/user/stats"
            params = {'fid': str(fid)}
            
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            
            logger.warning(f"Failed to fetch stats for {fid}")
            return {}
        except Exception as e:
            logger.error(f"Error fetching stats for {fid}: {e}")
            return {}
    
    @staticmethod
    def _parse_datetime(date_string):
        """Parse ISO format datetime"""
        try:
            return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        except:
            return datetime.utcnow()


# ==================== CALCULATION UTILITIES ====================

class BettingCalculator:
    """Betting calculation utilities"""
    
    BASE_FEE = 0.2
    WIN_FEE_PERCENTAGE = 1.5
    HOUSE_CUT_PERCENTAGE = 30
    
    @staticmethod
    def calculate_total_cost(bet_amount):
        """Calculate total cost including base fee"""
        return bet_amount + BettingCalculator.BASE_FEE
    
    @staticmethod
    def calculate_win_fee(payout):
        """Calculate fee on winnings"""
        return payout * (BettingCalculator.WIN_FEE_PERCENTAGE / 100)
    
    @staticmethod
    def calculate_net_payout(payout):
        """Calculate net payout after win fee"""
        fee = BettingCalculator.calculate_win_fee(payout)
        return payout - fee
    
    @staticmethod
    def calculate_payout(bet_amount, total_pool, winner_count):
        """Calculate payout for winning bet"""
        if winner_count == 0:
            return bet_amount
        
        # House takes 30%, remaining 70% goes to winners
        distribution_pool = total_pool * (BettingCalculator.HOUSE_CUT_PERCENTAGE / 100)
        
        # Additional payout from losing bets' pool
        losing_bets_pool = total_pool * ((100 - BettingCalculator.HOUSE_CUT_PERCENTAGE) / 100)
        
        # Each winner gets share of losing bets
        additional_payout = losing_bets_pool / winner_count
        
        return bet_amount + additional_payout
    
    @staticmethod
    def calculate_house_profit(total_pool, winner_count):
        """Calculate house profit from settlement"""
        if winner_count == 0:
            return total_pool  # All bets lost, house gets all
        
        return total_pool * (BettingCalculator.HOUSE_CUT_PERCENTAGE / 100)


# ==================== DECORATORS ====================

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'success': False, 'error': 'Missing authorization header'}), 401
        
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != 'bearer':
                return jsonify({'success': False, 'error': 'Invalid authorization scheme'}), 401
            
            # Verify token (implement your token verification logic)
            # user_id = verify_token(token)
            # if not user_id:
            #     return jsonify({'success': False, 'error': 'Invalid token'}), 401
            
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid authorization header'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def rate_limit(calls_per_minute=60):
    """Decorator for rate limiting"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Implement rate limiting logic
            # This is a placeholder - integrate with Redis or similar
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator


def handle_errors(f):
    """Decorator to handle and log errors"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {e}", exc_info=True)
            return jsonify({
                'success': False,
                'error': 'An error occurred processing your request'
            }), 500
    
    return decorated_function


# ==================== FORMATTING UTILITIES ====================

class Formatter:
    """Text formatting utilities"""
    
    @staticmethod
    def format_usd(amount):
        """Format amount as USD"""
        return f"${amount:,.2f}"
    
    @staticmethod
    def format_percentage(value, decimals=2):
        """Format value as percentage"""
        return f"{value:.{decimals}f}%"
    
    @staticmethod
    def format_address(address, prefix_length=6, suffix_length=4):
        """Format wallet address for display"""
        if len(address) < prefix_length + suffix_length:
            return address
        
        return f"{address[:prefix_length]}...{address[-suffix_length:]}"
    
    @staticmethod
    def format_timestamp(dt):
        """Format datetime for display"""
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt)
        
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def format_relative_time(dt):
        """Format datetime as relative time"""
        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt)
        
        now = datetime.utcnow()
        diff = now - dt
        
        if diff.days > 0:
            return f"{diff.days}d ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600}h ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60}m ago"
        else:
            return "just now"


# ==================== TRANSACTION UTILITIES ====================

class TransactionHelper:
    """Transaction-related utilities"""
    
    @staticmethod
    def generate_tx_id():
        """Generate unique transaction ID"""
        import uuid
        return str(uuid.uuid4())
    
    @staticmethod
    def create_transaction_hash(data):
        """Create transaction hash from data"""
        import json
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    @staticmethod
    def verify_transaction_integrity(data, hash_value):
        """Verify transaction hasn't been tampered with"""
        calculated_hash = TransactionHelper.create_transaction_hash(data)
        return calculated_hash == hash_value


# ==================== CACHING UTILITIES ====================

class Cache:
    """Simple caching utilities"""
    
    _cache = {}
    
    @staticmethod
    def get(key):
        """Get cached value"""
        if key in Cache._cache:
            value, expires_at = Cache._cache[key]
            if expires_at and datetime.utcnow() > expires_at:
                del Cache._cache[key]
                return None
            return value
        return None
    
    @staticmethod
    def set(key, value, ttl_seconds=300):
        """Set cache value with TTL"""
        expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds) if ttl_seconds else None
        Cache._cache[key] = (value, expires_at)
    
    @staticmethod
    def delete(key):
        """Delete cached value"""
        if key in Cache._cache:
            del Cache._cache[key]
    
    @staticmethod
    def clear():
        """Clear all cache"""
        Cache._cache.clear()


# ==================== LOGGING UTILITIES ====================

def setup_logger(name, log_file=None, level=logging.INFO):
    """Setup logger with console and file handlers"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger