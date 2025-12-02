from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.user import User
from app import db

bp = Blueprint('nguoidung', __name__, url_prefix='/nguoidung')

@bp.route('/')
@login_required
def index():
    """Tất cả người dùng - nguoidung.html"""
    users = User.query.all()
    return render_template('nguoidung/nguoidung.html', users=users)

@bp.route('/admin')
@login_required
def admin():
    """Người dùng admin - nguoidungadmin.html"""
    users = User.query.filter_by(role='admin').all()
    return render_template('nguoidung/nguoidungadmin.html', users=users)

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = Users.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.user_id
        return redirect('/dashboard')
    else:
        return "Sai tài khoản hoặc mật khẩu"

@bp.route('/editor')
@login_required
def ngoi_tieu():
    """Người dùng editor - nguoidungeditor.html"""
    users = User.query.filter_by(role='editor').all()
    return render_template('nguoidung/nguoidungeditor.html', users=users)

@bp.route('/viewer')
@login_required
def viewer():
    """Người dùng viewer - nguoidungviewer.html"""
    users = User.query.filter_by(role='viewer').all()
    return render_template('nguoidung/nguoidungviewer.html', users=users)
