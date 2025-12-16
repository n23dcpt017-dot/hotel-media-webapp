from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

# ========================
# Seed user
# ========================
def seed_selenium_user():
    from app.models.user import User

    if User.query.first():
        return

    admin = User(
        username="admin@hotel.com",
        email="admin@hotel.com",
        is_active=True,
        role="admin"
    )
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()




# ========================
# Application Factory
# ========================
def create_app(config_name=None):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from app.routes import auth
    app.register_blueprint(auth, url_prefix='/auth')

    with app.app_context():
        
        from app.models.user import User
        from app.models.post import Post
        from app.models.comment import Comment
        from app.models.campaign import Campaign
        from app.models.media import Media

        db.create_all()
        seed_selenium_user()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
