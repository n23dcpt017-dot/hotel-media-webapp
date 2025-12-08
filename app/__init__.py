from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name=None):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ✅ Quan trọng: nếu là unit test thì dùng DB trong RAM
    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'

    db.init_app(app)
    login_manager.init_app(app)

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import auth
    app.register_blueprint(auth, url_prefix='/auth')

    # ✅ Tự tạo bảng khi chạy test
    if config_name == 'testing':
        with app.app_context():
            db.create_all()

    return app
