from flask import Blueprint, render_template, request, redirect, url_for, make_response, current_app
from flask_login import login_user, logout_user, current_user
from app.models.user import User

auth = Blueprint('auth', __name__)

# ============ LOGIN ============
@auth.route('/login', methods=['GET', 'POST'])
def login():
   
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    
    if not username or not password:
        if current_app.config.get('TESTING'):
            return make_response("Missing fields", 400)
        return redirect(url_for('auth.login'))

    user = User.get_by_username(username)

    
    if not user or not user.check_password(password):
        if current_app.config.get('TESTING'):
            return make_response("Invalid credentials", 401)
        return redirect(url_for('auth.login'))

    
    login_user(user)

    
    if current_app.config.get('TESTING'):
        return make_response("Login successful", 200)

    
    return redirect(url_for('auth.dashboard'))


# ============ DASHBOARD ============
@auth.route('/dashboard')
def dashboard():
    
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    
    return render_template('tongquan.html')



@auth.route('/index')
def index():
    return redirect(url_for('auth.dashboard'))


# ============ LOGOUT ============
@auth.route('/logout')
def logout():
    logout_user()

    if current_app.config.get('TESTING'):
        return make_response("Logged out", 200)

    return redirect(url_for('auth.login'))
