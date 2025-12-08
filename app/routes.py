from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import db
from app.models.user import User

auth = Blueprint("auth", __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Thiếu username hoặc password", "danger")
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("User không tồn tại", "danger")
            return redirect(url_for('auth.login'))

        if not user.is_active:
            flash("Tài khoản bị khóa", "danger")
            return redirect(url_for('auth.login'))

        if not user.check_password(password):
            flash("Sai mật khẩu", "danger")
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect('/auth/tongquan.html')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
