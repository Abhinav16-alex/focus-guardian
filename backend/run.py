"""Run FocusGuard Flask application"""
from app import create_app
import os

app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    print("=" * 60)
    print("🛡️  FocusGuard Backend Starting...")
    print("=" * 60)
    print("📍 API Server: http://localhost:5000")
    print("📊 Dashboard: http://localhost:5173 (run frontend separately)")
    print("=" * 60)
    print("\n⚠️  IMPORTANT: Run with admin/sudo for website blocking:")
    print("   sudo python run.py (Linux/Mac)")
    print("   Run as Administrator (Windows)")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
