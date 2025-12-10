from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from app.models.user import User

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # GET: hiển thị form
    if request.method == 'GET':
        return render_template('login.html')

    # POST: xử lý login
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    # Case 1: bỏ trống field
    if not username or not password:
        flash("Vui lòng nhập đầy đủ thông tin", "error")
        return render_template('login.html'), 200   # QUAN TRỌNG

    user = User.query.filter_by(username=username).first()

    # Case 2: sai account
    if not user or not user.check_password(password):
        flash("Sai tài khoản hoặc mật khẩu", "error")
        return render_template('login.html'), 200

    # Case 3: login đúng
    login_user(user)

    # ✅ Selenium cần redirect sang dashboard
    return redirect('/dashboard')   # hoặc '/index'
@auth.route('/dashboard')
def dashboard():
    return render_template('tongquan.html')
