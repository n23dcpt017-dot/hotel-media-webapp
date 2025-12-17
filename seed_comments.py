from app import create_app, db
from app.models.comment import Comment
from datetime import datetime

app = create_app()

# Dữ liệu mẫu lấy từ HTML của bạn
SAMPLE_COMMENTS = [
    {
        "author_name": "Nguyễn Văn A",
        "author_email": "nguyenvana@hotel.com",
        "avatar_text": "VA",
        "avatar_bg": "#e0e7ff",
        "source": "Website",
        "content": "Phòng khách sạn rất đẹp và sang trọng. Dịch vụ tuyệt vời!",
        "post_title": "Khám phá không gian phòng Deluxe mới",
        "status": "pending",
        "created_at": "05/11/2025 14:30"
    },
    {
        "author_name": "Hoàng Văn E",
        "author_email": "hoangvane@gmail.com",
        "avatar_text": "HE",
        "avatar_bg": "#e0e7ff",
        "source": "Tiktok",
        "content": "Hồ bơi đẹp, view xịn, rất tuyệt.",
        "post_title": "Spa & chăm sóc sức khỏe cao cấp",
        "status": "pending",
        "created_at": "04/11/2025 18:20"
    },
    {
        "author_name": "Hoàng Văn E",
        "author_email": "hoangvane@gmail.com",
        "avatar_text": "HE",
        "avatar_bg": "#e0e7ff",
        "source": "Zalo",
        "content": "Dịch vụ tốt",
        "post_title": "Spa & chăm sóc sức khỏe cao cấp",
        "status": "pending",
        "created_at": "04/11/2025 18:15"
    },
    {
        "author_name": "Trần Thị B",
        "author_email": "tranthib@hotel.com",
        "avatar_text": "TB",
        "avatar_bg": "#d1fae5",
        "source": "Facebook",
        "content": "Giá cả hợp lý, sẽ quay lại lần sau.",
        "post_title": "Thực đơn buffet sáng đặc biệt cuối tuần",
        "status": "approved",
        "created_at": "05/11/2025 12:15"
    },
    {
        "author_name": "Lê Văn C",
        "author_email": "levanc@hotel.com",
        "avatar_text": "LC",
        "avatar_bg": "#e0f2fe",
        "source": "Youtube",
        "content": "Nhân viên thân thiện, phòng ốc thoải mái.",
        "post_title": "Khám phá không gian phòng Deluxe mới",
        "status": "approved",
        "created_at": "05/11/2025 10:45"
    },
    {
        "author_name": "Phạm Thị D",
        "author_email": "spammer@spam.com",
        "avatar_text": "PD",
        "avatar_bg": "#feebea",
        "source": "Website",
        "content": "Click here to win free money!! www.scam.com",
        "post_title": "Ưu đãi đặc biệt mùa lễ hội",
        "status": "rejected",
        "created_at": "04/11/2025 22:30"
    }
]

with app.app_context():
    # 1. Tạo bảng nếu chưa có (hoặc cập nhật schema)
    db.create_all()
    
    print("🌱 Đang tạo dữ liệu bình luận mẫu...")

    # Xóa dữ liệu cũ để tránh trùng lặp khi chạy nhiều lần (Tùy chọn)
    # Comment.query.delete() 
    
    count = 0
    for data in SAMPLE_COMMENTS:
        # Kiểm tra xem comment nội dung này đã có chưa để tránh duplicate
        if not Comment.query.filter_by(content=data["content"], author_email=data["author_email"]).first():
            cmt = Comment(
                author_name=data["author_name"],
                author_email=data["author_email"],
                avatar_text=data["avatar_text"],
                avatar_bg=data["avatar_bg"],
                source=data["source"],
                content=data["content"],
                post_title=data["post_title"],
                status=data["status"],
                # Chuyển chuỗi ngày tháng thành object datetime
                created_at=datetime.strptime(data["created_at"], "%d/%m/%Y %H:%M")
            )
            db.session.add(cmt)
            count += 1
    
    db.session.commit()
    print(f"✅ Đã thêm {count} bình luận vào Database!")
