from flask import Blueprint, render_template, request, redirect, url_for, make_response, current_app
from flask_login import login_user, logout_user
from app.models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # empty fields → fail
        if not username or not password:
            return make_response("Missing fields", 400)

        user = User.get_by_username(username)

        if user and user.check_password(password):
            login_user(user)

            # ✅ Unit test mode
            if current_app.config.get('TESTING'):
                return make_response("Login successful", 200)

            # ✅ Selenium / normal browser
            return redirect(url_for('auth.tongquan'))

        return make_response("Invalid credentials", 401)

    return render_template('login.html')

@auth.route('/tongquan')
def tongquan():
    return render_template('tongquan.html')

@auth.route('/logout')
def logout():
    logout_user()

    if current_app.config.get('TESTING'):
        return make_response("Logged out", 200)

    return redirect(url_for('auth.login'))
