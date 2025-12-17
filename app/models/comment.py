from app import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    
    # Thông tin người bình luận (Guest)
    author_name = db.Column(db.String(100), nullable=False)
    author_email = db.Column(db.String(120))
    avatar_text = db.Column(db.String(5)) # Ví dụ: "VA", "HE"
    avatar_bg = db.Column(db.String(20))  # Ví dụ: "#e0e7ff"
    
    # Nguồn bình luận (Website, Facebook, Zalo...)
    source = db.Column(db.String(50), default="Website")
    
    # Nội dung & Bài viết liên quan
    content = db.Column(db.Text, nullable=False)
    post_title = db.Column(db.String(255)) # Lưu tên bài viết (hoặc dùng Relationship nếu muốn chặt chẽ)
    
    # Trạng thái: pending, approved, rejected
    status = db.Column(db.String(20), default="pending") 

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "author_name": self.author_name,
            "author_email": self.author_email,
            "avatar_text": self.avatar_text,
            "avatar_bg": self.avatar_bg,
            "source": self.source,
            "content": self.content,
            "post_title": self.post_title,
            "status": self.status,
            "created_at": self.created_at.strftime("%d/%m/%Y %H:%M")
        }
