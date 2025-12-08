from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Logic này phục vụ cho Unit Test (Test Backend)
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password) and user.is_active:
            login_user(user)
            return 'Login success', 200
        
        flash('Sai tài khoản hoặc mật khẩu')

    # --- SỬA ĐỔI QUAN TRỌNG Ở ĐÂY ---
    # Thay vì return 'Login Page', hãy render file HTML giao diện đẹp của bạn
    return render_template('login.html') 

@auth.route('/logout')
def logout():
    logout_user()
    return 'Logged out', 200
