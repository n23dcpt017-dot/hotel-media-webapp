from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models.post import Post
from app.services.post_service import PostService
from app import db

bp = Blueprint('baiviet', __name__, url_prefix='/baiviet')

@bp.route('/')
@login_required
def index():
    """Hiển thị danh sách bài viết - baiviet.html"""
    posts = PostService.get_all_posts()
    return render_template('baiviet/baiviet.html', posts=posts)

@bp.route('/tao-moi', methods=['GET', 'POST'])
@login_required
def create():
    """Tạo bài viết mới"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        post = PostService.create_post(title, content)
        flash('Tạo bài viết thành công!', 'success')
        return redirect(url_for('baiviet.index'))
    
    return render_template('baiviet/taomoi.html')

@bp.route('/sua/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """Sửa bài viết - suabaiviet.html"""
    post = Post.query.get_or_404(id)
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        db.session.commit()
        flash('Cập nhật bài viết thành công!', 'success')
        return redirect(url_for('baiviet.index'))
    
    return render_template('baiviet/suabaiviet.html', post=post)

@bp.route('/xoa/<int:id>', methods=['POST'])
@login_required
def delete(id):
    """Xóa bài viết"""
    PostService.delete_post(id)
    flash('Đã xóa bài viết!', 'success')
    return redirect(url_for('baiviet.index'))

@bp.route('/xuat-ban/<int:id>', methods=['POST'])
@login_required 
def publish(id):
    """Xuất bản bài viết - xuatban.html"""
    PostService.publish_post(id)
    flash('Đã xuất bản bài viết!', 'success')
    return redirect(url_for('baiviet.index'))
