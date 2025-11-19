from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from app.services.comment_service import CommentService

bp = Blueprint('binhluan', __name__, url_prefix='/binhluan')

@bp.route('/')
@login_required
def index():
    """Tất cả bình luận - binhluan.html"""
    comments = CommentService.get_all_comments()
    return render_template('binhluan/binhluan.html', comments=comments)

@bp.route('/cho-duyet')
@login_required
def cho_duyet():
    """Bình luận chờ duyệt - binhluanchoduyet.html"""
    comments = CommentService.get_pending_comments()
    return render_template('binhluan/binhluanchoduyet.html', comments=comments)

@bp.route('/da-duyet')
@login_required
def da_duyet():
    """Bình luận đã duyệt - binhluandaduyet.html"""
    comments = CommentService.get_approved_comments()
    return render_template('binhluan/binhluandaduyet.html', comments=comments)

@bp.route('/tu-choi')
@login_required
def tu_choi():
    """Bình luận từ chối - binhluantuchoi.html"""
    comments = CommentService.get_rejected_comments()
    return render_template('binhluan/binhluantuchoi.html', comments=comments)

@bp.route('/duyet/<int:id>', methods=['POST'])
@login_required
def approve(id):
    """Duyệt bình luận"""
    CommentService.approve_comment(id)
    return jsonify({'success': True, 'message': 'Đã duyệt bình luận'})

@bp.route('/tu-choi/<int:id>', methods=['POST'])
@login_required
def reject(id):
    """Từ chối bình luận"""
    CommentService.reject_comment(id)
    return jsonify({'success': True, 'message': 'Đã từ chối bình luận'})
