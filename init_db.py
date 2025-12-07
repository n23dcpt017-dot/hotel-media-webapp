python

# Trong Python shell:
from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    db.create_all()
    admin = User(username='admin', email='admin@hotel.com', role='admin', is_active=True)
    admin.set_password('Admin@123')
    db.session.add(admin)
    db.session.commit()
    print("✅ Database created!")
