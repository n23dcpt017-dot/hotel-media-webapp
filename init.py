from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Đăng ký blueprints
    from app.routes import auth, dashboard, baiviet, binhluan, chienich, nguoidung, quanly, media
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(baiviet.bp)
    app.register_blueprint(binhluan.bp)
    app.register_blueprint(chienich.bp)
    app.register_blueprint(nguoidung.bp)
    app.register_blueprint(quanly.bp)
    app.register_blueprint(media.bp)
    
    return app
