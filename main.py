"""
Farcaster Prediction Market - Main Entry Point
Initializes Flask app with all blueprints and configurations
"""

import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Import main application
from project import app as main_app
from farcaster_frame import register_frame_routes
from database import db, init_db


def create_app():
    """Application factory"""
    
    # CORS configuration
    CORS(main_app, resources={
        r"/api/*": {
            "origins": ["*"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        },
        r"/frame/*": {
            "origins": ["https://frames.farcaster.xyz"],
            "methods": ["POST"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Register frame routes
    register_frame_routes(main_app)
    
    # Initialize database
    with main_app.app_context():
        init_db(main_app)
    
    return main_app


def setup_logging():
    """Setup logging configuration"""
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('prediction_market.log'),
            logging.StreamHandler()
        ]
    )


if __name__ == '__main__':
    setup_logging()
    
    app = create_app()
    
    # Get configuration from environment
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print(f"""
    ╔══════════════════════════════════════════════╗
    ║  Farcaster Prediction Market                 ║
    ║  Starting server...                          ║
    ╠══════════════════════════════════════════════╣
    ║  Host: {host:40} ║
    ║  Port: {port:40} ║
    ║  Debug: {str(debug):40} ║
    ║  Database: prediction_market.db             ║
    ╚══════════════════════════════════════════════╝
    """)
    
    app.run(debug=debug, host=host, port=port)