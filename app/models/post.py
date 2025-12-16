from app import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    author = db.Column(db.String(100))
    status = db.Column(
        db.String(20),
        default="draft"  # draft | published | scheduled
    )
    publish_at = db.Column(db.DateTime, nullable=True)

    is_deleted = db.Column(db.Boolean, default=False)

    created_at = db.Column(
        db.DateTime,
        default=db.func.now()
    )
    updated_at = db.Column(
        db.DateTime,
        default=db.func.now(),
        onupdate=db.func.now()
    )
