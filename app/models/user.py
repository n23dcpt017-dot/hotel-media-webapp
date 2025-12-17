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
    
    @property
    def avatar_initials(self):
        """
        Tự động tạo 2 chữ cái đầu cho Avatar.
        Logic: Lấy chữ cái đầu của (Tên lót) và (Tên).
        Ví dụ: "Nguyễn Văn An" -> "VA"
        """
        if not self.fullname:
            # Nếu chưa có tên, lấy 2 chữ đầu của username hoặc email
            name = self.username or self.email
            return name[:2].upper() if name else "US"

        parts = self.fullname.strip().split()
        
        if len(parts) >= 2:
            # Lấy chữ cái đầu của từ kế cuối (Tên lót) và từ cuối (Tên)
            # parts[-2] là tên lót, parts[-1] là tên chính
            initials = parts[-2][0] + parts[-1][0]
        else:
            # Nếu tên chỉ có 1 chữ (ví dụ: "Admin") -> Lấy 2 chữ đầu của nó
            initials = parts[0][:2]
            
        return initials.upper()

    @property
    def avatar_color(self):
        """
        (Tùy chọn) Tự động chọn màu nền dựa trên tên để mỗi người 1 màu khác nhau
        """
        colors = ['#e0e7ff', '#d1fae5', '#e0f2fe', '#feebea', '#f3e8ff', '#ffedd5']
        # Dùng hàm hash để chọn màu cố định cho mỗi user
        index = hash(self.username or "user") % len(colors)
        return colors[index]
    password_hash = db.Column(db.String(256))
    is_active = db.Column(db.Boolean, default=True)

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

    # ❗ KHÔNG override is_active → để SQLAlchemy xử lý

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
