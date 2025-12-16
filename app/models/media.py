from app import db
from datetime import datetime

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)

    is_hidden = db.Column(db.Boolean, default=False)

    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
