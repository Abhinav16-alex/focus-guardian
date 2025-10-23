"""Configuration settings for FocusGuard"""
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///focusguard.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS settings
    CORS_HEADERS = 'Content-Type'
    
    # Timer presets (in minutes)
    TIMER_PRESETS = {
        'pomodoro': 25,
        'short_break': 5,
        'long_break': 15,
        'deepwork': 90,
        'quick': 15
    }
    
    # Default settings
    DEFAULT_SETTINGS = {
        'auto_start_break': False,
        'notification_sound': True,
        'strict_mode': True,
        'daily_goal_minutes': 120
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
