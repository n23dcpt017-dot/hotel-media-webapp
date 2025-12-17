from app import create_app, db
from app.models.user import User
from datetime import datetime, timedelta

app = create_app()

SAMPLE_USERS = [
    # (Email, Username, Fullname, Role, Is_Active)
    ("admin@hotel.com", "admin", "Nguyễn Văn A", "admin", True),
    ("tranthib@hotel.com", "tranthib", "Trần Thị B", "editor", True),
    ("levanc@hotel.com", "levanc", "Lê Văn C", "viewer", True),
    ("phamthid@hotel.com", "phamthid", "Phạm Thị D", "viewer", True),
    ("hoangvane@hotel.com", "hoangvane", "Hoàng Văn E", "editor", False), # Không hoạt động
    ("nguyenvane@hotel.com", "nguyenvane", "Nguyễn Văn E", "viewer", True),
]

with app.app_context():
    db.create_all()

    print("🌱 Đang tạo dữ liệu người dùng mẫu...")
    
    for email, username, fullname, role, active in SAMPLE_USERS:
        
        if not User.query.filter_by(email=email).first():
            user = User(
                email=email,
                username=username,
                fullname=fullname,
                role=role,
                is_active=active,
                last_login=datetime.now() - timedelta(days=1) 
            )
            user.set_password("123456") 
            db.session.add(user)
            print(f"   + Đã thêm: {fullname} ({role})")
    
    db.session.commit()
    print("✅ Hoàn tất! Database đã tải lên.")
