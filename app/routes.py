from flask import Blueprint, request, redirect, url_for
from flask_login import login_user, logout_user
from app.models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return 'Login Page', 200

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password) and user.is_active:
        login_user(user)
        return redirect('/dashboard')

    return 'Invalid credentials', 401


@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/login')
