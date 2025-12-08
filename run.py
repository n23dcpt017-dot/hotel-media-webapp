import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from app import create_app, db

app = create_app()

if __name__ == '__main__':
    print("🚀 Flask đang khởi động...")

    with app.app_context():
        try:
            db.engine.connect()
            print("✅ Database connected")
        except Exception as e:
            print(f"❌ Database lỗi: {e}")

    app.run(host='127.0.0.1', port=5000, debug=True)
