from flask import Blueprint, render_template, request, redirect, session, url_for
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app import db, login_manager
import secrets  # Thêm import này

auth = Blueprint("auth", __name__)

# ===== UNAUTHORIZED HANDLER =====
@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/auth/login")

# ===== GENERATE CSRF TOKEN =====
def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']

# ===== LOGIN PAGE =====
@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'GET':
        logout_user()
        session.clear()
        # Generate CSRF token
        csrf_token = generate_csrf_token()
        return render_template('auth/login.html', csrf_token=csrf_token)

    if request.method == 'POST':
        # Validate CSRF token
        form_token = request.form.get('csrf_token')
        session_token = session.get('csrf_token')
        
        if not form_token or form_token != session_token:
            return render_template('auth/login.html', error="Invalid request", csrf_token=generate_csrf_token()), 400
        
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('auth/login.html', error="Vui lòng nhập đủ thông tin", csrf_token=generate_csrf_token()), 200

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return render_template('auth/login.html', error="Sai thông tin đăng nhập", csrf_token=generate_csrf_token()), 200

        login_user(user)
        return redirect("/auth/tongquan.html")

@auth.route("/dashboard")
@login_required
def dashboard():
    return render_template("tongquan.html")

@auth.route("/")
@auth.route("/index")
@login_required
def index():
    return render_template("index.html")

@auth.route("/tongquan.html")
@login_required
def tongquan_html():
    return render_template("tongquan.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect("/auth/login")
