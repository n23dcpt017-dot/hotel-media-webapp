from app import db

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    status = db.Column(
        db.String(20),
        default="active"  # active / paused / deleted
    )
