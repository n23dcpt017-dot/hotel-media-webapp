"""
app/__init__.py
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name=None):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # --- CẤU HÌNH DB ---
    # Nếu đang chạy test unit (config_name='testing'), dùng RAM để sạch sẽ
    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
    else:
        # Chạy thật hoặc Selenium thì dùng file DB
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
        app.config['TESTING'] = False

    db.init_app(app)
    login_manager.init_app(app)
    
    # Redirect về trang login nếu chưa đăng nhập
    login_manager.login_view = 'auth.login'

    # --- BẮT BUỘC PHẢI CÓ ĐOẠN NÀY ĐỂ LOGIN/LOGOUT HOẠT ĐỘNG ---
    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    # -----------------------------------------------------------

    from app.routes import auth
    app.register_blueprint(auth, url_prefix='/auth')

    return app
