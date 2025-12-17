from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime

db = SQLAlchemy()
login_manager = LoginManager()


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


def seed_sample_posts():
    from app.models.post import Post
    
    
    if Post.query.first():
        return

    samples = [
        Post(
            title="Khám phá không gian phòng Deluxe mới",
            content="Bài viết giới thiệu phòng Deluxe mới của khách sạn.",
            author="Nguyễn Văn A",
            view=1234,
            status="published",
            category="phong",
            image="/static/images/phong1.png",
            publish_at=datetime(2025, 11, 5)
        ),
        Post(
            title="Thực đơn buffet sáng đặc biệt cuối tuần",
            content="Giới thiệu buffet sáng cuối tuần.",
            author="Trần Thị B",
            view=987,
            status="published",
            category="am-thuc",
            image="/static/images/amthuc.png",
            publish_at=datetime(2025, 11, 5)
        ),
        Post(
            title="Ưu đãi đặc biệt mùa lễ hội",
            content="Ưu đãi mùa lễ hội sắp diễn ra.",
            author="Lê Văn C",
            view=0,
            status="scheduled",
            category="khuyen-mai",
            image="/static/images/lehoi.png",
            publish_at=datetime(2025, 11, 8)
        ),
        Post(
            title="Hội nghị & sự kiện tại khách sạn",
            content="Giới thiệu dịch vụ hội nghị và sự kiện.",
            author="Phạm Thị D",
            view=0,
            status="draft",
            category="su-kien",
            image="/static/images/khachhang.png",
            publish_at=datetime(2025, 11, 4)
        ),
    ]

    db.session.add_all(samples)
    db.session.commit()

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

    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
        
   
from flask import send_from_directory
import os

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
    
    from app.routes import auth
    app.register_blueprint(auth, url_prefix='/auth')

    
    with app.app_context():
        
        from app.models.user import User
        from app.models.post import Post
        
        
        db.create_all()         
        seed_sample_posts()     
        seed_selenium_user()    
        
    return app  
