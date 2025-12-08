from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # ==== CORE FIELDS ====
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # ==== EXTRA FIELDS CHO UNIT TEST ====
    full_name = db.Column(db.String(128))
    role = db.Column(db.String(32), default='user')

    password_hash = db.Column(db.String(256))
    is_active = db.Column(db.Boolean, default=True)

    # ==== PASSWORD METHODS ====
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # ==== HỖ TRỢ FLASK-LOGIN ====

    
    def get_id(self):
        return str(self.id)

   
    def is_active(self):
        return self.is_active

    
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
