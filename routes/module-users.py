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
