from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models.media import Media
from app import db
from werkzeug.utils import secure_filename
import os

bp = Blueprint('media', __name__, url_prefix='/media')

@bp.route('/')
@login_required
def index():
    """Tất cả media - thuvienmedia.html"""
    page = request.args.get('page', 1, type=int)
    media = Media.query.order_by(Media.created_at.desc()).paginate(
        page=page, per_page=30, error_out=False
    )
    return render_template('media/thuvienmedia.html', media=media)

@bp.route('/anh')
@login_required
def anh():
    """Thư viện ảnh - thuvienmediaanh.html"""
    page = request.args.get('page', 1, type=int)
    media = Media.query.filter_by(file_type='image').order_by(
        Media.created_at.desc()
    ).paginate(page=page, per_page=30, error_out=False)
    return render_template('media/thuvienmediaanh.html', media=media)

@bp.route('/video')
@login_required
def video():
    """Thư viện video - thuvienmediavideo.html"""
    page = request.args.get('page', 1, type=int)
    media = Media.query.filter_by(file_type='video').order_by(
        Media.created_at.desc()
    ).paginate(page=page, per_page=30, error_out=False)
    return render_template('media/thuvienmediavideo.html', media=media)

@bp.route('/upload', methods=['POST'])
@login_required
def upload():
    """Upload file media"""
    if 'file' not in request.files:
        return jsonify({'error': 'Không có file'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Không có file được chọn'}), 400
    
    # Kiểm tra extension
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'mp4'})
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed:
        return jsonify({'error': 'Định dạng file không được hỗ trợ'}), 400
    
    # Lưu file
    filename = secure_filename(file.filename)
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
    os.makedirs(upload_folder, exist_ok=True)
    
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)
    
    # Tạo record trong database
    media = Media(
        filename=filename,
        filepath=filename,
        file_type='image' if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) else 'video',
        uploaded_by=current_user.id
    )
    db.session.add(media)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Upload thành công',
        'media_id': media.id,
        'url': media.url
    })

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    """Xóa media"""
    media = Media.query.get_or_404(id)
    
    # Xóa file vật lý
    try:
        filepath = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads'), media.filepath)
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f"Error deleting file: {e}")
    
    # Xóa record
    db.session.delete(media)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Đã xóa media'})
