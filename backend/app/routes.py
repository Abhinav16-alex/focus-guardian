"""API routes for FocusGuard"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models import db, FocusSession, BlockedSite, BlockAttempt, Setting
from app.analytics import AnalyticsService

api = Blueprint('api', __name__)

# Global instances (will be set by app factory)
timer_service = None
blocker_service = None

def init_routes(timer, blocker):
    """Initialize routes with services"""
    global timer_service, blocker_service
    timer_service = timer
    blocker_service = blocker

# ==================== FOCUS SESSION ROUTES ====================

@api.route('/focus/start', methods=['POST'])
def start_focus():
    """Start a focus session"""
    try:
        data = request.json
        duration = data.get('duration', 25)
        mode = data.get('mode', 'pomodoro')
        
        # Get active blocked sites
        blocked_sites = BlockedSite.query.filter_by(is_active=True).all()
        site_urls = [site.url for site in blocked_sites]
        
        # Enable blocking
        if site_urls:
            blocker_service.enable_blocking(site_urls)
        
        # Start timer
        result = timer_service.start_session(duration, mode)
        
        return jsonify({'success': True, **result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/focus/stop', methods=['POST'])
def stop_focus():
    """Stop focus session"""
    try:
        data = request.json
        completed = data.get('completed', False)
        
        result = timer_service.stop_session(completed)
        
        if 'error' in result:
            return jsonify(result), 400
        
        # Disable blocking
        blocker_service.disable_blocking()
        
        # Save to database
        session = FocusSession(
            session_id=result['session_id'],
            mode=result.get('mode', 'custom'),
            duration_minutes=result['duration_minutes'],
            completed_minutes=result['completed_minutes'],
            completed=completed,
            started_at=datetime.fromisoformat(result['started_at']),
            ended_at=datetime.fromisoformat(result['ended_at']),
            date=datetime.fromisoformat(result['started_at']).date().isoformat()
        )
        db.session.add(session)
        db.session.commit()
        
        return jsonify({'success': True, **result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/focus/status', methods=['GET'])
def focus_status():
    """Get current focus status"""
    try:
        status = timer_service.get_status()
        return jsonify(status), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== BLOCKLIST ROUTES ====================

@api.route('/blocklist', methods=['GET'])
def get_blocklist():
    """Get all blocked sites"""
    try:
        sites = BlockedSite.query.filter_by(is_active=True).all()
        return jsonify({
            'success': True,
            'sites': [site.to_dict() for site in sites],
            'count': len(sites)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/blocklist', methods=['POST'])
def add_to_blocklist():
    """Add site to blocklist"""
    try:
        data = request.json
        url = data.get('url', '').strip()
        category = data.get('category', 'custom')
        
        if not url:
            return jsonify({'error': 'URL required'}), 400
        
        # Validate URL
        clean_url = blocker_service.validate_url(url)
        if not clean_url:
            return jsonify({'error': 'Invalid URL'}), 400
        
        # Check if exists
        existing = BlockedSite.query.filter_by(url=clean_url).first()
        if existing:
            return jsonify({'error': 'Site already blocked'}), 400
        
        # Add to database
        site = BlockedSite(url=clean_url, category=category)
        db.session.add(site)
        db.session.commit()
        
        return jsonify({'success': True, 'site': site.to_dict()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/blocklist/<int:site_id>', methods=['DELETE'])
def remove_from_blocklist(site_id):
    """Remove site from blocklist"""
    try:
        site = BlockedSite.query.get(site_id)
        if not site:
            return jsonify({'error': 'Site not found'}), 404
        
        db.session.delete(site)
        db.session.commit()
        
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/blocklist/preset/<category>', methods=['POST'])
def add_preset_category(category):
    """Add preset category"""
    try:
        sites = blocker_service.get_preset_sites(category)
        if not sites:
            return jsonify({'error': 'Unknown category'}), 400
        
        added = []
        for url in sites:
            existing = BlockedSite.query.filter_by(url=url).first()
            if not existing:
                site = BlockedSite(url=url, category=category)
                db.session.add(site)
                added.append(url)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'added_count': len(added),
            'sites': added
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ANALYTICS ROUTES ====================

@api.route('/analytics/overview', methods=['GET'])
def analytics_overview():
    """Get analytics overview"""
    try:
        days = request.args.get('days', 7, type=int)
        stats = AnalyticsService.get_overview(days)
        return jsonify({'success': True, 'data': stats}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/analytics/daily', methods=['GET'])
def analytics_daily():
    """Get daily statistics"""
    try:
        days = request.args.get('days', 30, type=int)
        stats = AnalyticsService.get_daily_stats(days)
        return jsonify({'success': True, 'data': stats}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/analytics/streaks', methods=['GET'])
def analytics_streaks():
    """Get streak information"""
    try:
        streaks = AnalyticsService.get_streaks()
        return jsonify({'success': True, **streaks}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/analytics/history', methods=['GET'])
def analytics_history():
    """Get session history"""
    try:
        limit = request.args.get('limit', 50, type=int)
        history = AnalyticsService.get_session_history(limit)
        return jsonify({'success': True, 'sessions': history}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== HEALTH CHECK ====================

@api.route('/health', methods=['GET'])
def health_check():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200
