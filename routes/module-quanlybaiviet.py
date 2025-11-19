from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models.post import Post

bp = Blueprint('quanly', __name__, url_prefix='/quanly')

@bp.route('/baiviet')
@login_required
def baiviet():
    """Quản lý bài viết - quanlybaiviet.html"""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('quanly/quanlybaiviet.html', posts=posts)

@bp.route('/baiviet-dalenlich')
@login_required
def baiviet_dalenlich():
    """Bài viết đã lên lịch - quanlybaivietdalenlich.html"""
    posts = Post.query.filter_by(status='scheduled').order_by(Post.scheduled_at).all()
    return render_template('quanly/quanlybaivietdalenlich.html', posts=posts)

@bp.route('/baiviet-dauxatban')
@login_required
def baiviet_dauxatban():
    """Bài viết đã xuất bản - quanlybaivietdauxatban.html"""
    posts = Post.query.filter_by(status='published').order_by(Post.published_at.desc()).all()
    return render_template('quanly/quanlybaivietdauxatban.html', posts=posts)

@bp.route('/baiviet-nhap')
@login_required
def baiviet_nhap():
    """Bài viết nháp - quanlybaivienthap.html"""
    posts = Post.query.filter_by(status='draft').order_by(Post.updated_at.desc()).all()
    return render_template('quanly/quanlybaivienthap.html', posts=posts)

@bp.route('/livestream')
@login_required
def livestream():
    """Quản lý livestream - quanlylivestream.html"""
    return render_template('quanly/quanlylivestream.html')
