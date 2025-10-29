"""
Configuration settings for Farcaster Prediction Market
"""

import os
from datetime import timedelta

# Flask Configuration
class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///prediction_market.db'
    )
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CORS configuration
    CORS_ORIGINS = [
        "https://frames.farcaster.xyz",
        "https://*.farcaster.xyz",
        "http://localhost:3000",
        "http://localhost:5000"
    ]
    
    # API Configuration
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Rate limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_DEFAULT = "200 per day, 50 per hour"


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Get configuration from environment
def get_config():
    """Get appropriate configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development').lower()
    
    if env == 'production':
        return ProductionConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return DevelopmentConfig


# Betting Configuration
class BettingConfig:
    """Betting-related configuration"""
    BASE_FEE = float(os.getenv('BASE_FEE', 0.2))  # $0.20
    WIN_FEE_PERCENTAGE = float(os.getenv('WIN_FEE_PERCENTAGE', 1.5))  # 1.5%
    HOUSE_CUT_PERCENTAGE = float(os.getenv('HOUSE_CUT_PERCENTAGE', 30))  # 30% of losing pool
    
    # Market configuration
    MIN_BET_AMOUNT = 1.0
    MAX_BET_AMOUNT = 1000.0
    MIN_POOL_AMOUNT = 10.0
    
    # Durations
    MIN_MARKET_DURATION_HOURS = 1
    MAX_MARKET_DURATION_HOURS = 7 * 24  # 7 days


# Blockchain Configuration
class BlockchainConfig:
    """Blockchain-related configuration"""
    # Treasure wallet that receives fees
    TREASURE_WALLET = os.getenv(
        'TREASURE_WALLET',
        '0xf2B6664bF4d507C8889f07174A6A6dE53CEFD7fC'
    )
    
    # RPC Configuration
    ALCHEMY_RPC_URL = os.getenv(
        'ALCHEMY_RPC_URL',
        'https://eth-mainnet.g.alchemy.com/v2/demo'
    )
    
    # Chain configuration
    CHAIN_ID = int(os.getenv('CHAIN_ID', 1))  # Ethereum mainnet
    CHAIN_NAME = 'ethereum' if int(os.getenv('CHAIN_ID', 1)) == 1 else 'sepolia'
    
    # Contract addresses
    USDC_CONTRACT = os.getenv(
        'USDC_CONTRACT',
        '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
    )
    
    # Gas configuration
    GAS_LIMIT = 200000
    GAS_PRICE_MULTIPLIER = 1.1


# Farcaster Configuration
class FarcasterConfig:
    """Farcaster-related configuration"""
    HUB_URL = os.getenv(
        'FARCASTER_HUB_URL',
        'https://hub.farcaster.builders'
    )
    
    NEYNAR_API_KEY = os.getenv('NEYNAR_API_KEY', '')
    NEYNAR_BASE_URL = 'https://api.neynar.com/v2/farcaster'
    
    # Cache configuration
    CACHE_ENABLED = True
    CACHE_TTL_SECONDS = 300  # 5 minutes


# Payment Configuration
class PaymentConfig:
    """Payment processor configuration"""
    STRIPE_API_KEY = os.getenv('STRIPE_KEY', '')
    STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')
    
    COINBASE_API_KEY = os.getenv('COINBASE_KEY', '')
    COINBASE_WEBHOOK_SECRET = os.getenv('COINBASE_WEBHOOK_SECRET', '')
    
    # Supported currencies
    SUPPORTED_CURRENCIES = ['USD', 'ETH', 'USDC']
    PRIMARY_CURRENCY = 'USD'


# Logging Configuration
class LoggingConfig:
    """Logging configuration"""
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = 'prediction_market.log'
    LOG_MAX_BYTES = 10485760  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # Log format
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


# Email Configuration (for notifications)
class EmailConfig:
    """Email configuration"""
    SMTP_SERVER = os.getenv('SMTP_SERVER', '')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    FROM_EMAIL = os.getenv('FROM_EMAIL', 'noreply@farcastermarket.com')
    
    # Email templates
    SEND_EMAILS = os.getenv('SEND_EMAILS', 'False').lower() == 'true'


# API Rate Limiting
class RateLimitConfig:
    """Rate limiting configuration"""
    ENABLED = True
    
    # Per endpoint limits
    LIMITS = {
        '/api/markets': '100 per hour',
        '/api/bets/place': '50 per hour',
        '/api/withdrawals/request': '20 per hour',
        '/frame/*': '200 per hour',
    }
    
    # Storage for rate limit tracking
    STORAGE_URL = os.getenv('REDIS_URL', 'memory://')


# Cache Configuration
class CacheConfig:
    """Caching configuration"""
    ENABLED = True
    TYPE = os.getenv('CACHE_TYPE', 'simple')  # 'simple' or 'redis'
    
    # Redis configuration (if using Redis)
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # Cache timeouts (in seconds)
    TIMEOUTS = {
        'user_profile': 300,  # 5 minutes
        'market_data': 60,    # 1 minute
        'user_balance': 60,   # 1 minute
        'farcaster_data': 300  # 5 minutes
    }


# Feature Flags
class FeatureFlags:
    """Feature flags for enabling/disabling features"""
    ENABLE_BETTING = os.getenv('ENABLE_BETTING', 'True').lower() == 'true'
    ENABLE_WITHDRAWALS = os.getenv('ENABLE_WITHDRAWALS', 'True').lower() == 'true'
    ENABLE_FRAMES = os.getenv('ENABLE_FRAMES', 'True').lower() == 'true'
    ENABLE_AUTO_SETTLEMENT = os.getenv('ENABLE_AUTO_SETTLEMENT', 'True').lower() == 'true'
    ENABLE_NOTIFICATIONS = os.getenv('ENABLE_NOTIFICATIONS', 'False').lower() == 'true'
    
    # Beta features
    ENABLE_BETA_FEATURES = os.getenv('ENABLE_BETA_FEATURES', 'False').lower() == 'true'


# Security Configuration
class SecurityConfig:
    """Security-related configuration"""
    # JWT
    JWT_SECRET = os.getenv('JWT_SECRET', 'jwt-secret-key')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_HOURS = 24
    
    # CORS
    CORS_ALLOW_CREDENTIALS = True
    CORS_MAX_AGE = 3600
    
    # Security headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
    }
    
    # Password requirements (if applicable)
    MIN_PASSWORD_LENGTH = 12
    REQUIRE_SPECIAL_CHARS = True
    REQUIRE_NUMBERS = True
    REQUIRE_UPPERCASE = True


# Validation Rules
class ValidationConfig:
    """Input validation configuration"""
    # Username validation
    USERNAME_MIN_LENGTH = 1
    USERNAME_MAX_LENGTH = 32
    USERNAME_PATTERN = r'^[a-zA-Z0-9_.-]+$'
    
    # Wallet address validation
    WALLET_PATTERN = r'^0x[a-fA-F0-9]{40}$'
    
    # URL validation
    URL_MAX_LENGTH = 2048
    
    # Description validation
    DESCRIPTION_MAX_LENGTH = 1000