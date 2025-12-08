from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app.models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password) and user.is_active:
            login_user(user)
            return redirect('/dashboard')

        
        flash('Sai tài khoản hoặc mật khẩu')
        return render_template('login.html'), 401
        
    return render_template('login.html'), 200

@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/auth/login')
