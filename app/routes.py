from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_user, logout_user

from app import db
from app.models.user import User

auth = Blueprint('auth', __name__)


# ==============================
# GET: hiển thị trang login
# POST: xử lý đăng nhập
# ==============================
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # ---------- GET ----------
    if request.method == 'GET':
        return make_response(render_template('login.html'), 200)

    # ---------- POST ----------
    username = request.form.get('username')
    password = request.form.get('password')

    # Case: field rỗng
    if not username or not password:
        return make_response(render_template('login.html', error="Missing fields"), 400)

    user = User.query.filter_by(username=username).first()

    # Case: không tìm thấy user
    if user is None:
        return make_response(render_template('login.html', error="User not found"), 401)

    # Case: user bị disable
    if not user.is_active:
        return make_response(render_template('login.html', error="User inactive"), 403)

    # Case: sai mật khẩu
    if not user.check_password(password):
        return make_response(render_template('login.html', error="Wrong password"), 401)

    # ✅ Case: login thành công
    login_user(user)
    return make_response(render_template('login_success.html'), 200)


# ==============================
# LOGOUT
# ==============================
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
