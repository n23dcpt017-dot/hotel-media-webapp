from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # ==== CORE FIELDS ====
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    fullname = db.Column(db.String(100))      
    role = db.Column(db.String(20), default='viewer') 
    
    # Password hash
    password_hash = db.Column(db.String(256))
    
    # Trạng thái hoạt động
    is_active = db.Column(db.Boolean, default=True)   
    
    # Thời gian
    last_login = db.Column(db.DateTime) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ==== RELATIONSHIPS ====
    # Quan hệ với bảng Post (1 User có nhiều Post)
    # Lưu ý: Bảng Post phải có cột user_id làm ForeignKey
    posts = db.relationship('Post', backref='author_user', lazy='dynamic')

    # ==== HELPER METHODS (AVATAR) ====
    @property
    def avatar_initials(self):
        """
        Tự động tạo 2 chữ cái đầu cho Avatar.
        """
        if not self.fullname:
            name = self.username or self.email
            return name[:2].upper() if name else "US"

        parts = self.fullname.strip().split()
        
        if len(parts) >= 2:
            initials = parts[-2][0] + parts[-1][0]
        else:
            initials = parts[0][:2]
            
        return initials.upper()

    @property
    def avatar_color(self):
        """
        Tự động chọn màu nền dựa trên tên
        """
        colors = ['#e0e7ff', '#d1fae5', '#e0f2fe', '#feebea', '#f3e8ff', '#ffedd5']
        index = hash(self.username or "user") % len(colors)
        return colors[index]

    # ==== PASSWORD METHODS ====
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    # ==== HỖ TRỢ FLASK-LOGIN ====
    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # ==== STATIC METHODS HỖ TRỢ LOGIN ====
    @staticmethod
    def get_by_id(user_id):
        try:
            return User.query.get(int(user_id))
        except:
            return None

    @staticmethod
    def get_by_username(username):
        try:
            return User.query.filter_by(username=username).first()
        except:
            return None

    def __repr__(self):
        return f'<User {self.username}>'
