from app import db
from datetime import datetime

class Media(db.Model):
    __tablename__ = "media"
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(20))  # image | video
    created_at = db.Column(db.DateTime, default=db.func.now())


