from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    print("🔧 Đang khởi tạo database...")

    db.create_all()

    # Check xem admin có tồn tại chưa
    existing = User.query.filter_by(username="admin").first()

    if existing:
        print("✅ User 'admin' đã tồn tại – bỏ qua việc tạo mới.")
    else:
        print("➕ Tạo user 'admin' mới...")

        admin = User(
            username="admin",
            email="admin@hotel.com",
            fullname="Admin",
            role="admin",
            is_active=True
        )
        admin.set_password("admin123")
        
        db.session.add(admin)
        db.session.commit()

        print("🎉 User 'admin' đã được tạo!")

    print("✅ Database setup hoàn tất!")
