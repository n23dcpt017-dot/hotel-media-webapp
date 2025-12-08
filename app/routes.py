from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from app.models.user import User

auth = Blueprint('auth', __name__)

# Trang login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # GET -> chỉ render form
    if request.method == 'GET':
        return render_template('login.html')

    # POST -> xử lý login
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    # ❌ Nếu trống field -> ở lại trang login
    if not username or not password:
        return render_template('login.html', error="Missing fields"), 200

    # Tìm user
    user = User.get_by_username(username)

    # ❌ Sai tài khoản hoặc mật khẩu
    if not user or not user.check_password(password):
        return render_template('login.html', error="Invalid credentials"), 200

    # ❌ User bị inactive
    if not user.is_active:
        return render_template('login.html', error="User inactive"), 200

    # ✅ Login thành công
    login_user(user)

    # Selenium của m đợi redirect đến /dashboard hoặc /index
    return redirect(url_for('auth.dashboard'))


# Trang dashboard (tongquan)
@auth.route('/dashboard')
def dashboard():
    return render_template('tongquan.html')


# Logout
@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
