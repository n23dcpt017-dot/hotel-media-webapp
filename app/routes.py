from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app import db

auth = Blueprint("auth", __name__)

# ===== LOGIN PAGE =====
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # ❌ Rỗng → ở lại login
        if not username or not password:
            return render_template('login.html', error="Vui lòng nhập đủ thông tin"), 200

        # ✅ Query user đúng cách
        user = User.query.filter_by(username=username).first()

        # ❌ User không tồn tại
        if not user:
            return render_template('login.html', error="Sai tài khoản"), 200

        # ❌ Sai password
        if not user.check_password(password):
            return render_template('login.html', error="Sai mật khẩu"), 200

        # ✅ Login thành công
        login_user(user)
        session['user_id'] = user.id

        # Selenium + Unit test cần redirect này
        return redirect("/auth/dashboard")

    return render_template('login.html')


# ===== PAGE SAU LOGIN =====
@auth.route("/dashboard")
@login_required
def dashboard():
    return render_template("tongquan.html")


# Alias cho unit test
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
