"""Flask application factory"""
from flask import Flask
from flask_cors import CORS
from app.models import db
from app.config import config
from app.blocker import WebsiteBlocker
from app.timer import FocusTimer

def create_app(config_name='development'):
    """Create and configure Flask app"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app)
    
    # Initialize database
    db.init_app(app)
    
    # Initialize services
    blocker = WebsiteBlocker()
    timer = FocusTimer(blocker)
    
    # Register blueprints
    from app.routes import api, init_routes
    init_routes(timer, blocker)
    app.register_blueprint(api, url_prefix='/api')
    
    # Create tables
    with app.app_context():
        db.create_all()
        print("✅ Database initialized")
    
    return app
