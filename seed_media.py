from app import create_app, db
from app.models.media import Media

app = create_app()

MEDIA = [
    ("phong1.png", "image"),
    ("amthuc.png", "image"),
    ("lehoi.png", "image"),
    ("khachhang.png", "image"),
]

with app.app_context():
    for filename, media_type in MEDIA:
        if not Media.query.filter_by(filename=filename).first():
            db.session.add(Media(
                filename=filename,
                type=media_type
            ))
    db.session.commit()

print("✅ Seed media cũ xong")
