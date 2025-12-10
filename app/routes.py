from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app import db

auth = Blueprint("auth", __name__)

# ===== LOGIN PAGE =====
@auth.route("/login", methods=["GET", "POST"])
def login():
    # GET: hiển thị form
    if request.method == "GET":
        return render_template("login.html")

    # POST: xử lý login
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    # ❌ Nếu trống → ở lại /auth/login
    if not username or not password:
        flash("Thiếu thông tin")
        return render_template("login.html"), 200

    user = User.query.filter_by(username=username).first()

    # ❌ Sai tài khoản
    if not user or not user.check_password(password):
        flash("Sai tài khoản hoặc mật khẩu")
        return render_template("login.html"), 200

    # ✅ Đúng tài khoản
    login_user(user)
    return redirect("/dashboard")


# ===== DASHBOARD =====
@auth.route("/dashboard")
@login_required
def dashboard():
    # file dashboard là tongquan.html theo project m
    return render_template("tongquan.html")


# ===== LOGOUT =====
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/auth/login")
