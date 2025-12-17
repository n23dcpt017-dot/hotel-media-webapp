from app import create_app, db
from app.models.media import Media

app = create_app()

MEDIA = [
    ("/static/images/phong1.png", "image"),
    ("/static/images/amthuc.png", "image"),
    ("/static/images/lehoi.png", "image"),
    ("/static/images/khachhang.png", "image"),
    ("https://res.cloudinary.com/dadlq8qha/video/upload/v1765170630/tour-phong-suite_abpion.mp4", "video"),
    ("https://res.cloudinary.com/dadlq8qha/video/upload/v1765170430/gioi-thieu-nha-hang_lupzcn.mp4", "video"),
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
