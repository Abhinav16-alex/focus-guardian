"""Database models for FocusGuard"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class FocusSession(db.Model):
    """Focus session model"""
    __tablename__ = 'focus_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(50), unique=True, nullable=False)
    mode = db.Column(db.String(20), nullable=False)
    duration_minutes = db.Column(db.Float, nullable=False)
    completed_minutes = db.Column(db.Float, nullable=False, default=0)
    completed = db.Column(db.Boolean, default=False)
    started_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime)
    date = db.Column(db.String(10))
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'mode': self.mode,
            'duration_minutes': self.duration_minutes,
            'completed_minutes': round(self.completed_minutes, 2),
            'completed': self.completed,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'date': self.date
        }

class BlockedSite(db.Model):
    """Blocked website model"""
    __tablename__ = 'blocked_sites'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True, nullable=False)
    category = db.Column(db.String(50), default='custom')
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'category': self.category,
            'added_at': self.added_at.isoformat() if self.added_at else None,
            'is_active': self.is_active
        }

class BlockAttempt(db.Model):
    """Block attempt tracking model"""
    __tablename__ = 'block_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    during_session = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'during_session': self.during_session
        }

class Setting(db.Model):
    """User settings model"""
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'key': self.key,
            'value': self.value,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
