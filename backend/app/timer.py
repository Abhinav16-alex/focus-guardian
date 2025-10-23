"""Focus timer management with threading"""
import threading
import time
import uuid
from datetime import datetime

class FocusTimer:
    """Manages focus sessions"""
    
    def __init__(self, blocker):
        self.blocker = blocker
        self.is_active = False
        self.session_id = None
        self.start_time = None
        self.duration_seconds = 0
        self.time_remaining = 0
        self.mode = None
        self.timer_thread = None
        self._stop_event = threading.Event()
    
    def start_session(self, duration_minutes, mode='custom'):
        """Start a focus session"""
        if self.is_active:
            return {'error': 'Session already active'}
        
        self.session_id = str(uuid.uuid4())
        self.duration_seconds = duration_minutes * 60
        self.time_remaining = self.duration_seconds
        self.mode = mode
        self.start_time = datetime.now()
        self.is_active = True
        self._stop_event.clear()
        
        # Start countdown thread
        self.timer_thread = threading.Thread(target=self._countdown, daemon=True)
        self.timer_thread.start()
        
        return {
            'session_id': self.session_id,
            'duration': duration_minutes,
            'mode': mode,
            'started_at': self.start_time.isoformat()
        }
    
    def stop_session(self, completed=False):
        """Stop the current session"""
        if not self.is_active:
            return {'error': 'No active session'}
        
        elapsed_seconds = (datetime.now() - self.start_time).total_seconds()
        completed_minutes = elapsed_seconds / 60
        
        self.is_active = False
        self._stop_event.set()
        
        result = {
            'session_id': self.session_id,
            'completed': completed,
            'completed_minutes': round(completed_minutes, 2),
            'duration_minutes': self.duration_seconds / 60,
            'started_at': self.start_time.isoformat(),
            'ended_at': datetime.now().isoformat()
        }
        
        # Reset
        self.session_id = None
        self.start_time = None
        self.time_remaining = 0
        
        return result
    
    def _countdown(self):
        """Countdown timer (runs in thread)"""
        while self.is_active and self.time_remaining > 0 and not self._stop_event.is_set():
            time.sleep(1)
            self.time_remaining -= 1
        
        # Timer completed
        if self.is_active and self.time_remaining <= 0:
            self.stop_session(completed=True)
    
    def get_status(self):
        """Get current timer status"""
        if not self.is_active:
            return {
                'is_active': False,
                'time_remaining': 0,
                'progress_percent': 0
            }
        
        elapsed = self.duration_seconds - self.time_remaining
        progress = (elapsed / self.duration_seconds * 100) if self.duration_seconds > 0 else 0
        
        return {
            'is_active': True,
            'session_id': self.session_id,
            'mode': self.mode,
            'time_remaining': self.time_remaining,
            'duration_seconds': self.duration_seconds,
            'progress_percent': round(progress, 2),
            'started_at': self.start_time.isoformat() if self.start_time else None
        }
