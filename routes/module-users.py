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

@bp.route('/danh-moi')
@login_required
def danh_moi():
    """Người dùng được mời - nguoidungdanhmoi.html"""
    users = User.query.filter_by(role='invited').all()
    return render_template('nguoidung/nguoidungdanhmoi.html', users=users)

@bp.route('/ngoi-tieu')
@login_required
def ngoi_tieu():
    """Người dùng ngòi tiêu (editor) - nguoidungngoitieu.html"""
    users = User.query.filter_by(role='editor').all()
    return render_template('nguoidung/nguoidungngoitieu.html', users=users)

@bp.route('/viewer')
@login_required
def viewer():
    """Người dùng viewer - nguoidungviewer.html"""
    users = User.query.filter_by(role='viewer').all()
    return render_template('nguoidung/nguoidungviewer.html', users=users)
