"""
Database models and initialization for Farcaster Prediction Market
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()


def init_db(app):
    """Initialize database"""
    db_path = os.path.join(os.path.dirname(__file__), 'prediction_market.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    with app.app_context():
        db.create_all()


class UserProfile(db.Model):
    """User profile information"""
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    fid = db.Column(db.Integer, unique=True, nullable=False, index=True)
    username = db.Column(db.String(255), nullable=True)
    display_name = db.Column(db.String(255), nullable=True)
    pfp_url = db.Column(db.String(512), nullable=True)
    wallet_address = db.Column(db.String(255), nullable=True, index=True)
    bio = db.Column(db.Text, nullable=True)
    followers_count = db.Column(db.Integer, default=0)
    following_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    bets = db.relationship('Bet', backref='user_profile', lazy=True)
    markets = db.relationship('MarketEvent', backref='user_profile', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'fid': self.fid,
            'username': self.username,
            'display_name': self.display_name,
            'pfp_url': self.pfp_url,
            'wallet_address': self.wallet_address,
            'followers_count': self.followers_count,
            'following_count': self.following_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class MarketEvent(db.Model):
    """Prediction market event"""
    __tablename__ = 'market_events'
    
    id = db.Column(db.Integer, primary_key=True)
    user_fid = db.Column(db.Integer, db.ForeignKey('user_profiles.fid'), nullable=False, index=True)
    market_type = db.Column(db.String(50), nullable=False)  # 'casts_count', 'likes_total', 'engagement_score'
    threshold = db.Column(db.Float, nullable=False)
    direction = db.Column(db.String(10), default='over')  # 'over' or 'under'
    status = db.Column(db.String(20), default='active', index=True)  # 'active', 'settled', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    end_time = db.Column(db.DateTime, nullable=False, index=True)
    settled_at = db.Column(db.DateTime, nullable=True)
    result_value = db.Column(db.Float, nullable=True)
    total_pool = db.Column(db.Float, default=0)
    description = db.Column(db.Text, nullable=True)
    
    bets = db.relationship('Bet', backref='market', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_fid': self.user_fid,
            'market_type': self.market_type,
            'threshold': self.threshold,
            'direction': self.direction,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'end_time': self.end_time.isoformat(),
            'settled_at': self.settled_at.isoformat() if self.settled_at else None,
            'result_value': self.result_value,
            'total_pool': self.total_pool,
            'bets_count': len(self.bets),
            'description': self.description
        }


class Bet(db.Model):
    """Individual bet placed on a market"""
    __tablename__ = 'bets'
    
    id = db.Column(db.Integer, primary_key=True)
    market_id = db.Column(db.Integer, db.ForeignKey('market_events.id'), nullable=False, index=True)
    user_fid = db.Column(db.Integer, db.ForeignKey('user_profiles.fid'), nullable=False, index=True)
    user_wallet = db.Column(db.String(255), nullable=False)
    prediction = db.Column(db.String(10), nullable=False)  # 'over' or 'under'
    amount = db.Column(db.Float, nullable=False)  # Bet amount in USD
    base_fee = db.Column(db.Float, default=0.2)  # Base fee charged at bet time
    payout = db.Column(db.Float, nullable=True)  # Payout if won
    fee_on_win = db.Column(db.Float, nullable=True)  # 1.5% fee on winnings
    status = db.Column(db.String(20), default='pending', index=True)  # 'pending', 'active', 'won', 'lost', 'cancelled'
    transaction_hash = db.Column(db.String(255), nullable=True)
    placed_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    settled_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'market_id': self.market_id,
            'user_fid': self.user_fid,
            'user_wallet': self.user_wallet,
            'prediction': self.prediction,
            'amount': self.amount,
            'base_fee': self.base_fee,
            'payout': self.payout,
            'fee_on_win': self.fee_on_win,
            'status': self.status,
            'transaction_hash': self.transaction_hash,
            'placed_at': self.placed_at.isoformat(),
            'settled_at': self.settled_at.isoformat() if self.settled_at else None
        }


class Withdrawal(db.Model):
    """Withdrawal request and history"""
    __tablename__ = 'withdrawals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_fid = db.Column(db.Integer, db.ForeignKey('user_profiles.fid'), nullable=False, index=True)
    user_wallet = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending', index=True)  # 'pending', 'processing', 'completed', 'failed'
    transaction_hash = db.Column(db.String(255), nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    requested_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    processed_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_fid': self.user_fid,
            'user_wallet': self.user_wallet,
            'amount': self.amount,
            'status': self.status,
            'transaction_hash': self.transaction_hash,
            'error_message': self.error_message,
            'requested_at': self.requested_at.isoformat(),
            'processed_at': self.processed_at.isoformat() if self.processed_at else None
        }


class Transaction(db.Model):
    """Transaction history for auditing"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    tx_hash = db.Column(db.String(255), unique=True, nullable=False, index=True)
    from_address = db.Column(db.String(255), nullable=False)
    to_address = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    tx_type = db.Column(db.String(50), nullable=False)  # 'bet_payment', 'base_fee', 'win_fee', 'payout', 'withdrawal'
    related_id = db.Column(db.Integer, nullable=True)  # bet_id, withdrawal_id, etc.
    status = db.Column(db.String(20), default='pending')  # 'pending', 'confirmed', 'failed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'tx_hash': self.tx_hash,
            'from_address': self.from_address,
            'to_address': self.to_address,
            'amount': self.amount,
            'tx_type': self.tx_type,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'confirmed_at': self.confirmed_at.isoformat() if self.confirmed_at else None
        }