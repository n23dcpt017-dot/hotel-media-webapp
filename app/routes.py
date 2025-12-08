from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, login_manager
from app.models import User

# ================================
# Flask-Login user loader (BẮT BUỘC)
# ================================
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


# ================================
# ROUTE: LOGIN
# ================================
@app.route("/auth/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        # 1️. Rỗng
        if not username or not password:
            flash("Vui lòng nhập đầy đủ tài khoản và mật khẩu!", "danger")
            return redirect(url_for("login"))

        # 2️. Check user
        user = User.get_by_username(username)

        if not user:
            flash("Tài khoản không tồn tại!", "danger")
            return redirect(url_for("login"))

        # 3️. Check mật khẩu
        if not user.check_password(password):
            flash("Sai mật khẩu!", "danger")
            return redirect(url_for("login"))

        # 4️. Login thành công
        login_user(user)
        return redirect(url_for("dashboard"))

    return render_template("login.html")


# ================================
# ROUTE: DASHBOARD
# ================================
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("tongquan.html")


# ================================
# ROUTE: LOGOUT
# ================================
@app.route("/auth/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
