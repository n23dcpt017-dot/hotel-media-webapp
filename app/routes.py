from flask import Blueprint, render_template, request, redirect, url_for, make_response, current_app
from flask_login import login_user, logout_user
from app.models.user import User

auth = Blueprint('auth', __name__)

# ================== LOGIN ==================
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Trường hợp trống field
        if not username or not password:
            if current_app.config.get('TESTING'):
                return make_response("Missing fields", 400)
            return render_template('login.html')  # ở lại trang login

        user = User.get_by_username(username)

        # Sai user hoặc sai password
        if not user or not user.check_password(password):
            if current_app.config.get('TESTING'):
                return make_response("Invalid credentials", 401)
            return render_template('login.html')

        # Login thành công
        login_user(user)

        if current_app.config.get('TESTING'):
            return make_response("Login successful", 200)

        
        return redirect(url_for('auth.tongquan'))

    return render_template('login.html')


# ================== DASHBOARD / TỔNG QUAN ==================
@auth.route('/tongquan.html')
def tongquan():
    return render_template('tongquan.html')



@auth.route('/dashboard')
def dashboard():
    return redirect(url_for('auth.tongquan'))


# ================== LOGOUT ==================
@auth.route('/logout')
def logout():
    logout_user()

    if current_app.config.get('TESTING'):
        return make_response("Logged out", 200)

    return redirect(url_for('auth.login'))
