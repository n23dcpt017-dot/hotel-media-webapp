from app import db
from datetime import datetime

class Campaign(db.Model):
    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    platform = db.Column(db.String(50)) # facebook, google, tiktok, youtube
    
    # active (Đang chạy), paused (Tạm dừng), scheduled (Đã lên lịch), completed (Hoàn thành)
    status = db.Column(db.String(20), default="active")
    
    # Tiền tệ
    budget = db.Column(db.Float, default=0.0) # Ngân sách
    spent = db.Column(db.Float, default=0.0)  # Đã chi
    
    # Thống kê hiệu quả
    reach = db.Column(db.Integer, default=0)
    clicks = db.Column(db.Integer, default=0)
    conversions = db.Column(db.Integer, default=0)
    
    # Thời gian
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "platform": self.platform,
            "status": self.status,
            "budget": self.budget,
            "spent": self.spent,
            "reach": "{:,}".format(self.reach), # Format số: 1,000
            "clicks": "{:,}".format(self.clicks),
            "conversions": "{:,}".format(self.conversions),
            # Format ngày: 20/11/2025
            "start_date": self.start_date.strftime("%d/%m/%Y") if self.start_date else "",
            "end_date": self.end_date.strftime("%d/%m/%Y") if self.end_date else "",
            # Raw data cho form sửa
            "raw_start_date": self.start_date.strftime("%Y-%m-%d") if self.start_date else "",
            "raw_end_date": self.end_date.strftime("%Y-%m-%d") if self.end_date else ""
        }
