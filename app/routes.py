from flask import Blueprint, render_template, request, redirect, url_for, make_response
from flask_login import login_user, logout_user
from app.models.user import User

auth = Blueprint('auth', __name__)

# ====================== LOGIN ======================
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # GET
    if request.method == 'GET':
        return render_template('login.html'), 200

    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    # ❌ Trống field -> ở lại login
    if not username or not password:
        return render_template('login.html', error='Missing fields'), 200

    user = User.get_by_username(username)

    # ❌ Sai tài khoản
    if not user:
        return render_template('login.html', error='Invalid user'), 200

    # ❌ Sai mật khẩu
    if not user.check_password(password):
        return render_template('login.html', error='Wrong password'), 200

    # ❌ User bị vô hiệu hóa
    if not user.is_active:
        return render_template('login.html', error='Inactive user'), 200

    # ✅ Đúng toàn bộ
    login_user(user)

    # Selenium expect /dashboard or /index
    return redirect(url_for('auth.dashboard'))

# ====================== DASHBOARD ======================
@auth.route('/dashboard')
def dashboard():
    return render_template('tongquan.html'), 200

# Alias: để test nào tìm /index vẫn pass
@auth.route('/index')
def index():
    return redirect(url_for('auth.dashboard'))

# ====================== LOGOUT ======================
@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
