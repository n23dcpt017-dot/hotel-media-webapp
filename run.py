"""
run.py - File chính để chạy Flask application
Vị trí: ROOT folder (hotel-media-webapp/run.py)

Chạy: python run.py
"""
import os
import sys

# Add project root to path để import được app
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import Flask app
try:
    from app import create_app, db
except ImportError:
    print("❌ Không thể import app!")
    print("💡 Hãy đảm bảo:")
    print("   1. Đang chạy từ root folder")
    print("   2. File app/__init__.py tồn tại")
    print("   3. Đã cài đặt dependencies: pip install -r requirements_test.txt")
    sys.exit(1)

# Tạo Flask app instance
try:
    app = create_app()
except Exception as e:
    print(f"❌ Lỗi khi tạo app: {e}")
    print("💡 Kiểm tra file config.py và app/__init__.py")
    sys.exit(1)

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 KHỞI ĐỘNG FLASK APPLICATION")
    print("="*70)
    
    # Kiểm tra và tạo database nếu chưa có
    with app.app_context():
        try:
            # Kiểm tra database
            db.engine.connect()
            print("✅ Database connection: OK")
        except Exception as e:
            print(f"⚠️  Database chưa được khởi tạo!")
            print(f"💡 Chạy: python init_db.py")
            print(f"   Error: {e}")
    
    print("\n📋 Thông tin:")
    print(f"   - App name: {app.name}")
    print(f"   - Debug mode: {app.debug}")
    print(f"   - Environment: {app.config.get('ENV', 'production')}")
    print(f"   - Database: {app.config.get('SQLALCHEMY_DATABASE_URI', 'N/A')}")
    
    print("\n🌐 Server sẽ chạy tại:")
    print("   - Local:   http://127.0.0.1:5000")
    print("   - Network: http://localhost:5000")
    
    print("\n👤 Login credentials (mặc định):")
    print("   - Username: admin")
    print("   - Password: Admin@123")
    
    print("\n📚 Routes chính:")
    print("   - Login:     /auth/login")
    print("   - Dashboard: templates/dashboardlayout.html")
    print("   - Bài viết:  templates/baiviet.html")
    print("   - Media:     templates/thuvienmedia.html")
    
    print("\n⚠️  Nhấn CTRL+C để dừng server")
    print("="*70 + "\n")
    
    # Chạy Flask development server
    try:
        app.run(
            host='0.0.0.0',  # Cho phép truy cập từ network
            port=5000,       # Port 5000
            debug=True,      # Debug mode
            use_reloader=True  # Auto-reload khi code thay đổi
        )
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("👋 Server đã dừng!")
        print("="*70 + "\n")
    except Exception as e:
        print(f"\n❌ Lỗi khi chạy server: {e}")
        sys.exit(1)
