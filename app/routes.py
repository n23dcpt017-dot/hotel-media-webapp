from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User

auth = Blueprint("auth", __name__)

# ===== LOGIN =====
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Nếu đã login → cho logout trước để test sạch session
    if current_user.is_authenticated:
        logout_user()
        session.clear()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Rỗng → ở lại login
        if not username or not password:
            return render_template('login.html', error="Vui lòng nhập đủ thông tin"), 200

        # Tìm user
        user = User.query.filter_by(username=username).first()

        # Sai tài khoản / mật khẩu
        if not user or not user.check_password(password):
            return render_template('login.html', error="Sai tài khoản hoặc mật khẩu"), 200

        # Đúng → login bằng flask-login
        login_user(user)

        return redirect(url_for('auth.dashboard'))

    return render_template('login.html')


# ===== DASHBOARD =====
@auth.route("/dashboard")
@login_required
def dashboard():
    return render_template("tongquan.html")


# Alias cho selenium test
@auth.route("/index")
@login_required
def index():
    return render_template("tongquan.html")


# ===== LOGOUT =====
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect("/auth/login")
