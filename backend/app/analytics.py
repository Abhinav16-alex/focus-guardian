"""Analytics service for focus statistics"""
from datetime import datetime, timedelta
from sqlalchemy import func
from app.models import db, FocusSession, BlockAttempt

class AnalyticsService:
    """Provides analytics and statistics"""
    
    @staticmethod
    def get_overview(days=7):
        """Get overview statistics"""
        start_date = (datetime.now() - timedelta(days=days)).date().isoformat()
        
        sessions = FocusSession.query.filter(FocusSession.date >= start_date).all()
        
        total_sessions = len(sessions)
        completed_sessions = sum(1 for s in sessions if s.completed)
        total_minutes = sum(s.completed_minutes for s in sessions)
        avg_session = total_minutes / total_sessions if total_sessions > 0 else 0
        completion_rate = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
        
        # Block attempts
        block_attempts = BlockAttempt.query.filter(
            BlockAttempt.timestamp >= datetime.now() - timedelta(days=days)
        ).count()
        
        return {
            'total_sessions': total_sessions,
            'completed_sessions': completed_sessions,
            'total_minutes': round(total_minutes, 2),
            'avg_session_length': round(avg_session, 2),
            'completion_rate': round(completion_rate, 2),
            'block_attempts': block_attempts,
            'period_days': days
        }
    
    @staticmethod
    def get_daily_stats(days=30):
        """Get daily breakdown"""
        start_date = (datetime.now() - timedelta(days=days)).date()
        
        daily_data = db.session.query(
            FocusSession.date,
            func.count(FocusSession.id).label('sessions'),
            func.sum(FocusSession.completed_minutes).label('minutes')
        ).filter(
            FocusSession.date >= start_date.isoformat()
        ).group_by(FocusSession.date).all()
        
        result = []
        for date, sessions, minutes in daily_data:
            result.append({
                'date': date,
                'sessions': sessions,
                'minutes': round(minutes or 0, 2)
            })
        
        return result
    
    @staticmethod
    def get_streaks():
        """Calculate current and best streaks"""
        sessions = FocusSession.query.filter(
            FocusSession.completed == True
        ).order_by(FocusSession.date.desc()).all()
        
        if not sessions:
            return {'current': 0, 'best': 0, 'total': 0}
        
        dates = list(set(s.date for s in sessions))
        dates.sort(reverse=True)
        
        # Current streak
        current_streak = 0
        today = datetime.now().date()
        check_date = today
        
        for date_str in dates:
            date = datetime.fromisoformat(date_str).date()
            if date == check_date:
                current_streak += 1
                check_date -= timedelta(days=1)
            else:
                break
        
        # Best streak
        best_streak = 1
        temp_streak = 1
        
        for i in range(len(dates) - 1):
            current = datetime.fromisoformat(dates[i]).date()
            next_date = datetime.fromisoformat(dates[i + 1]).date()
            
            if (current - next_date).days == 1:
                temp_streak += 1
                best_streak = max(best_streak, temp_streak)
            else:
                temp_streak = 1
        
        return {
            'current': current_streak,
            'best': max(best_streak, current_streak),
            'total': len(sessions)
        }
    
    @staticmethod
    def get_session_history(limit=50):
        """Get recent session history"""
        sessions = FocusSession.query.order_by(
            FocusSession.started_at.desc()
        ).limit(limit).all()
        
        return [s.to_dict() for s in sessions]
