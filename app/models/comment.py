from app import db
from datetime import datetime

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    status = db.Column(
        db.String(20),
        default="pending"  # pending / approved / rejected / deleted
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
