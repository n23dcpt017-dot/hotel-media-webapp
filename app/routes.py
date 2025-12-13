from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db, login_manager
from werkzeug.security import check_password_hash

auth = Blueprint("auth", __name__)

# ===== UNAUTHORIZED HANDLER =====
@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/auth/login")

# ===== LOGIN PAGE =====
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Chỉ logout nếu đang login
        if current_user.is_authenticated:
            logout_user()
            session.clear()
        return render_template('/login.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Debug: In ra thông tin nhận được
        print(f"DEBUG: Username received: {username}")
        print(f"DEBUG: Password received: {password}")
        
        if not username or not password:
            flash("Vui lòng nhập đủ thông tin", "error")
            return render_template('auth/login.html', error="Vui lòng nhập đủ thông tin")

        # Tìm user theo username
        user = User.query.filter_by(username=username).first()
        
        if not user:
            # Thử tìm theo email
            user = User.query.filter_by(email=username).first()
        
        if not user:
            print(f"DEBUG: User not found: {username}")
            flash("Sai thông tin đăng nhập", "error")
            return render_template('auth/login.html', error="Sai thông tin đăng nhập")
        
        # Kiểm tra password
        if not user.check_password(password):
            print(f"DEBUG: Wrong password for user: {username}")
            flash("Sai thông tin đăng nhập", "error")
            return render_template('auth/login.html', error="Sai thông tin đăng nhập")
        
        # Login thành công
        login_user(user, remember=request.form.get('remember') == 'on')
        print(f"DEBUG: Login successful for user: {username}")
        
        # Chuyển hướng đến trang tổng quan
        return redirect("/auth/tongquan.html")

# ===== DASHBOARD PAGE =====
@auth.route("/dashboard")
@login_required
def dashboard():
    return render_template("tongquan.html")

# ===== INDEX/HOME PAGE =====
@auth.route("/")
@auth.route("/index")
@login_required
def index():
    return render_template("index.html")

# ===== TONGQUAN PAGE =====
@auth.route("/tongquan.html")
@login_required
def tongquan_html():
    return render_template("tongquan.html")

# ===== LOGOUT =====
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect("/auth/login")

# ===== DEBUG: Xem tất cả users =====
@auth.route("/debug/users")
def debug_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password_hash': user.password_hash[:20] + '...' if user.password_hash else None
        })
    return {"users": result}
