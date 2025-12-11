from flask import Blueprint, render_template, request, redirect, session, url_for
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app import db, login_manager

auth = Blueprint("auth", __name__)

# ===== UNAUTHORIZED HANDLER =====
@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/auth/login")


# ===== LOGIN PAGE =====
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Force logout khi vào trang login (fix selenium fail)
    if request.method == 'GET':
        logout_user()
        session.clear()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('login.html', error="Vui lòng nhập đủ thông tin"), 200

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return render_template('login.html', error="Sai thông tin đăng nhập"), 200

        login_user(user)
        return redirect(url_for("auth.tongquan"))

    return render_template('login.html')


# ===== DASHBOARD PAGE =====
@auth.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


# ===== INDEX/HOME PAGE =====
@auth.route("/")
@auth.route("/index")
@login_required
def index():
    return render_template("index.html")


# ===== TONGQUAN PAGE =====
@auth.route("/tongquan")
@login_required
def tongquan():
    return render_template("tongquan.html")


# ===== LOGOUT =====
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect("/auth/login")
