from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


# ========================
# Seed user for Selenium
# ========================
def seed_selenium_user():
    from app.models.user import User
    with db.session.no_autoflush:
        if not User.query.filter_by(username="admin").first():
            admin = User(
                username="admin",
                is_active=True
            )
            admin.set_password("Admin@123")
            db.session.add(admin)
            db.session.commit()


# ========================
# Application Factory
# ========================
def create_app(config_name=None):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # Base config
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Database config
    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from app.routes import auth
    app.register_blueprint(auth, url_prefix='/auth')

    # Setup DB + optional seed
    with app.app_context():
        db.create_all()

        
        if config_name != 'testing':
            seed_selenium_user()

    
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
