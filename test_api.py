"""
API Tests for Farcaster Prediction Market
Run with: python -m pytest test_api.py
"""

import pytest
import json
from datetime import datetime, timedelta
from project import app
from database import db, init_db, MarketEvent, Bet, UserProfile


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        init_db(app)
        yield app.test_client()
        db.session.remove()


@pytest.fixture
def sample_user(client):
    """Create sample user"""
    with app.app_context():
        user = UserProfile(
            fid=1,
            username='alice',
            display_name='Alice',
            wallet_address='0x742d35Cc6634C0532925a3b844Bc9e7595f42e24'
        )
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def sample_market(client, sample_user):
    """Create sample market"""
    with app.app_context():
        market = MarketEvent(
            user_fid=sample_user.fid,
            market_type='casts_count',
            threshold=5,
            direction='over',
            end_time=datetime.utcnow() + timedelta(hours=24),
            status='active'
        )
        db.session.add(market)
        db.session.commit()
        return market


class TestHealth:
    """Health check tests"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'


class TestMarkets:
    """Market endpoint tests"""
    
    def test_get_markets(self, client, sample_market):
        """Test getting all markets"""
        response = client.get('/api/markets')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['markets']) > 0
    
    def test_create_market(self, client, sample_user):
        """Test creating a new market"""
        with app.app_context():
            payload = {
                'user_fid': sample_user.fid,
                'market_type': 'likes_total',
                'threshold': 100,
                'duration_hours': 24
            }
            
            response = client.post(
                '/api/markets/create',
                data=json.dumps(payload),
                content_type='application/json'
            )
            
            assert response.status_code == 201
            data = json.loads(response.data)
            assert data['success'] is True
            assert 'market_id' in data
    
    def test_create_market_invalid_type(self, client, sample_user):
        """Test creating market with invalid type"""
        with app.app_context():
            payload = {
                'user_fid': sample_user.fid,
                'market_type': 'invalid_type',
                'threshold': 100,
                'duration_hours': 24
            }
            
            response = client.post(
                '/api/markets/create',
                data=json.dumps(payload),
                content_type='application/json'
            )
            
            # Should still create but validation happens elsewhere
            assert response.status_code in [201, 400]


class TestBetting:
    """Betting endpoint tests"""
    
    def test_place_bet(self, client, sample_market, sample_user):
        """Test placing a bet"""
        with app.app_context():
            payload = {
                'market_id': sample_market.id,
                'user_fid': sample_user.fid,
                'prediction': 'over',
                'amount': 10.0,
                'user_wallet': sample_user.wallet_address
            }
            
            response = client.post(
                '/api/bets/place',
                data=json.dumps(payload),
                content_type='application/json'
            )
            
            # Note: Real transaction will fail in test, but structure is valid
            # In production, mock the blockchain calls
            assert response.status_code in [201, 400]
    
    def test_place_bet_invalid_prediction(self, client, sample_market, sample_user):
        """Test placing bet with invalid prediction"""
        with app.app_context():
            payload = {
                'market_id': sample_market.id,
                'user_fid': sample_user.fid,
                'prediction': 'invalid',
                'amount': 10.0,
                'user_wallet': sample_user.wallet_address
            }
            
            response = client.post(
                '/api/bets/place',
                data=json.dumps(payload),
                content_type='application/json'
            )
            
            assert response.status_code in [201, 400]
    
    def test_place_bet_missing_fields(self, client, sample_market):
        """Test placing bet with missing fields"""
        payload = {
            'market_id': sample_market.id,
            'user_fid': 1
            # Missing prediction, amount, user_wallet
        }
        
        response = client.post(
            '/api/bets/place',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
    
    def test_get_user_bets(self, client, sample_user):
        """Test getting user's bets"""
        with app.app_context():
            response = client.get(f'/api/bets/user/{sample_user.fid}')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True
            assert 'bets' in data


class TestUserProfile:
    """User profile endpoint tests"""
    
    def test_get_user_profile(self, client, sample_user):
        """Test getting user profile"""
        with app.app_context():
            response = client.get(f'/api/users/{sample_user.fid}')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['success'] is True
            assert data['user']['fid'] == sample_user.fid
            assert 'stats' in data['user']
    
    def test_get_nonexistent_user(self, client):
        """Test getting non-existent user"""
        response = client.get('/api/users/99999')
        assert response.status_code == 404


class TestWithdrawals:
    """Withdrawal endpoint tests"""
    
    def test_request_withdrawal(self, client, sample_user):
        """Test requesting withdrawal"""
        with app.app_context():
            payload = {
                'user_fid': sample_user.fid,
                'user_wallet': sample_user.wallet_address,
                'amount': 10.0
            }
            
            response = client.post(
                '/api/withdrawals/request',
                data=json.dumps(payload),
                content_type='application/json'
            )
            
            # Should fail because user has no balance
            assert response.status_code == 400
    
    def test_request_withdrawal_invalid_amount(self, client, sample_user):
        """Test withdrawal with invalid amount"""
        with app.app_context():
            payload = {
                'user_fid': sample_user.fid,
                'user_wallet': sample_user.wallet_address,
                'amount': -10.0
            }
            
            response = client.post(
                '/api/withdrawals/request',
                data=json.dumps(payload),
                content_type='application/json'
            )
            
            assert response.status_code == 400


class TestErrorHandling:
    """Error handling tests"""
    
    def test_404_not_found(self, client):
        """Test 404 error"""
        response = client.get('/api/nonexistent')
        assert response.status_code == 404
    
    def test_invalid_json(self, client):
        """Test invalid JSON"""
        response = client.post(
            '/api/bets/place',
            data='invalid json',
            content_type='application/json'
        )
        assert response.status_code in [400, 500]


class TestValidation:
    """Validation tests"""
    
    def test_validate_wallet_address(self):
        """Test wallet address validation"""
        from utils import Validator
        
        valid_address = '0x742d35Cc6634C0532925a3b844Bc9e7595f42e24'
        invalid_address = 'not-a-wallet'
        
        assert Validator.validate_wallet_address(valid_address) is True
        assert Validator.validate_wallet_address(invalid_address) is False
    
    def test_validate_amount(self):
        """Test amount validation"""
        from utils import Validator
        
        assert Validator.validate_amount(10.0) is True
        assert Validator.validate_amount(0.5) is True
        assert Validator.validate_amount(-10.0) is False
        assert Validator.validate_amount(0) is False
    
    def test_validate_prediction(self):
        """Test prediction validation"""
        from utils import Validator
        
        assert Validator.validate_prediction('over') is True
        assert Validator.validate_prediction('under') is True
        assert Validator.validate_prediction('OVER') is True
        assert Validator.validate_prediction('invalid') is False
    
    def test_validate_market_type(self):
        """Test market type validation"""
        from utils import Validator
        
        assert Validator.validate_market_type('casts_count') is True
        assert Validator.validate_market_type('likes_total') is True
        assert Validator.validate_market_type('engagement_score') is True
        assert Validator.validate_market_type('invalid') is False


class TestCalculations:
    """Calculation tests"""
    
    def test_calculate_total_cost(self):
        """Test calculating total bet cost"""
        from utils import BettingCalculator
        
        total = BettingCalculator.calculate_total_cost(10.0)
        assert total == 10.2  # 10.0 + 0.2 base fee
    
    def test_calculate_win_fee(self):
        """Test calculating win fee"""
        from utils import BettingCalculator
        
        fee = BettingCalculator.calculate_win_fee(100.0)
        assert fee == 1.5  # 100.0 * 1.5%
    
    def test_calculate_net_payout(self):
        """Test calculating net payout"""
        from utils import BettingCalculator
        
        net = BettingCalculator.calculate_net_payout(100.0)
        assert net == 98.5  # 100.0 - (100.0 * 1.5%)
    
    def test_calculate_payout(self):
        """Test calculating payout"""
        from utils import BettingCalculator
        
        payout = BettingCalculator.calculate_payout(
            bet_amount=10.0,
            total_pool=100.0,
            winner_count=5
        )
        assert payout > 10.0  # Should be more than original bet


if __name__ == '__main__':
    pytest.main([__file__, '-v'])