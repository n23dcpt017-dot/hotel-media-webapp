from flask import (
    Blueprint, render_template, request,
    redirect, session, url_for, jsonify,
    send_from_directory
)
from flask_login import (
    login_user, logout_user,
    login_required, current_user
)
from app import db, login_manager
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.campaign import Campaign
from app.models.media import Media
import os, uuid
from datetime import datetime
from werkzeug.utils import secure_filename

auth = Blueprint("auth", __name__)
UPLOAD_FOLDER = "uploads"

# =================================================
# HELPER FUNCTIONS
# =================================================
def get_file_size(path):
    """Tính dung lượng file để hiển thị"""
    try:
        size = os.path.getsize(path)
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"
    except:
        return "0 KB"

def parse_date(date_str):
    """Chuyển đổi ngày từ chuỗi sang object datetime"""
    if not date_str:
        return None
    try:
        # Ưu tiên format Việt Nam: dd/mm/yyyy
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        try:
            # Fallback format ISO: yyyy-mm-dd
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return None

# =================================================
# AUTH HANDLER
# =================================================
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth.login"))

# =================================================
# LOGIN / LOGOUT
# =================================================
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for("auth.tongquan_html"))
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return render_template("login.html", error="Vui lòng nhập đủ thông tin")

    user = User.query.filter(
        (User.username == username) | (User.email == username)
    ).first()

    if not user or not user.check_password(password):
        return render_template("login.html", error="Sai thông tin đăng nhập")

    if not user.is_active:
        return render_template("login.html", error="Tài khoản đã bị khóa")

    login_user(user)
    return redirect(url_for("auth.tongquan_html"))

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("auth.login"))

# =================================================
# OAUTH (Login MXH)
# =================================================
def oauth_login(provider, email):
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(username=email.split("@")[0], email=email, role="user")
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for("auth.tongquan_html"))

@auth.route("/login/google")
def login_google(): return oauth_login("google", "google_user@gmail.com")

@auth.route("/login/facebook")
def login_facebook(): return oauth_login("facebook", "fb_user@gmail.com")

@auth.route("/login/zalo")
def login_zalo(): return oauth_login("zalo", "zalo_user@gmail.com")

@auth.route("/login/tiktok")
def login_tiktok(): return oauth_login("tiktok", "tiktok_user@gmail.com")

# =================================================
# FRONTEND PAGES (Render HTML)
# =================================================
@auth.route("/")
@auth.route("/dashboard")
@login_required
def dashboard(): return render_template("tongquan.html")

@auth.route("/index")
@login_required
def index(): return render_template("index.html")

@auth.route("/tongquan.html")
@login_required
def tongquan_html(): return render_template("tongquan.html")

@auth.route("/quanlybaiviet.html")
@login_required
def page_quanly_baiviet(): return render_template("quanlybaiviet.html")

@auth.route("/taobaiviet.html")
@login_required
def tao_baiviet(): return render_template("taobaiviet.html")

@auth.route("/suabaiviet.html")
@login_required
def sua_baiviet(): return render_template("suabaiviet.html")

@auth.route("/thuvienmedia.html")
@login_required
def page_thuvien_media(): return render_template("thuvienmedia.html")

# Các trang phụ khác...
@auth.route("/quanlylivestream.html")
@login_required
def page_quanly_livestream(): return render_template("quanlylivestream.html")

@auth.route("/thuvienmediaanh.html")
@login_required
def thuvienmedia_anh(): return render_template("thuvienmediaanh.html")

@auth.route("/thuvienmediavideo.html")
@login_required
def thuvienmedia_video(): return render_template("thuvienmediavideo.html")

@auth.route("/nguoidung.html")
@login_required
def page_nguoidung(): return render_template("nguoidung.html")

@auth.route("/analyticsvaseo.html")
@login_required
def page_analytics(): return render_template("analyticsvaseo.html")

@auth.route("/binhluan.html")
@login_required
def page_binhluan(): return render_template("binhluan.html")

@auth.route("/chiendich.html")
@login_required
def page_chiendich(): return render_template("chiendich.html")

@auth.route("/xuatban.html")
@login_required
def page_xuatban(): return render_template("xuatban.html")

@auth.route("/binhluanchoduyet.html")
@login_required
def binhluan_choduyet(): return render_template("binhluanchoduyet.html")

@auth.route("/binhluandaduyet.html")
@login_required
def binhluan_daduyet(): return render_template("binhluandaduyet.html")

@auth.route("/binhluantuchoi.html")
@login_required
def binhluan_tuchoi(): return render_template("binhluantuchoi.html")

@auth.route("/chiendichdalenlich.html")
@login_required
def chiendich_dalenlich(): return render_template("chiendichdalenlich.html")

@auth.route("/chiendichdangchay.html")
@login_required
def chiendich_dangchay(): return render_template("chiendichdangchay.html")

@auth.route("/chiendichtamdung.html")
@login_required
def chiendich_tamdung(): return render_template("chiendichtamdung.html")

@auth.route("/nguoidungadmin.html")
@login_required
def nguoidung_admin(): return render_template("nguoidungadmin.html")

@auth.route("/nguoidungeditor.html")
@login_required
def nguoidung_editor(): return render_template("nguoidungeditor.html")

@auth.route("/nguoidungviewer.html")
@login_required
def nguoidung_viewer(): return render_template("nguoidungviewer.html")

@auth.route("/quanlybaivietdalenlich.html")
@login_required
def quanlybaiviet_dalenlich(): return render_template("quanlybaivietdalenlich.html")

@auth.route("/quanlybaivietdaxuatban.html")
@login_required
def quanlybaiviet_daxuatban(): return render_template("quanlybaivietdaxuatban.html")

@auth.route("/quanlybaivietnhap.html")
@login_required
def quanlybaiviet_nhap(): return render_template("quanlybaivietnhap.html")


# =================================================
# API BÀI VIẾT (POSTS)
# =================================================

@auth.route("/api/posts", methods=["POST"])
@login_required
def create_post():
    data = request.json
    if not data.get("title"):
        return jsonify({"error": "Thiếu tiêu đề"}), 400

    publish_at = parse_date(data.get("publish_at"))

    post = Post(
        title=data["title"],
        content=data.get("content"),
        category=data.get("category"),
        status=data.get("status", "draft"),
        publish_at=publish_at,
        image=data.get("image") or "/static/images/phong1.png",
        author=current_user.username,
        author=current_user.fullname or current_user.username, 
        author_user=current_user,
    )
    db.session.add(post)
    db.session.commit()

    return jsonify({"message": "Tạo bài viết thành công", "id": post.id}), 201

@auth.route("/api/posts/<int:id>", methods=["GET"])
@login_required
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify({
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "category": post.category,
        "status": post.status,
        "publish_at": post.publish_at.strftime("%d/%m/%Y") if post.publish_at else None,
        "image": post.image,
        "author": post.author
    })

@auth.route("/api/posts/<int:id>", methods=["PUT"])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    data = request.json

    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)
    post.category = data.get("category", post.category)
    post.status = data.get("status", post.status)
    
    if data.get("publish_at"):
        new_date = parse_date(data["publish_at"])
        if new_date:
            post.publish_at = new_date
        else:
            return jsonify({"error": "Sai định dạng ngày"}), 400

    if data.get("image"):
        post.image = data.get("image")

    db.session.commit()
    return jsonify({"message": "Cập nhật thành công"})

@auth.route("/api/posts/<int:id>", methods=["DELETE"])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    # Xóa trực tiếp khỏi DB (hoặc dùng soft delete nếu muốn)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Đã xóa"})

@auth.route("/api/posts", methods=["GET"])
@login_required
def list_posts():
    status = request.args.get("status")
    query = Post.query # Nếu có cột is_deleted thì thêm .filter_by(is_deleted=False)

    if status:
        query = query.filter_by(status=status)

    posts = query.order_by(Post.created_at.desc()).all()

    return jsonify([
        {
            "id": p.id,
            "title": p.title,
            "status": p.status,
            "publish_at": p.publish_at.strftime("%d/%m/%Y") if p.publish_at else None,
            "image": p.image,
            "category": p.category,
            "author": p.author
        }
        for p in posts
    ])

# =================================================
# API MEDIA & UPLOAD (THƯ VIỆN ẢNH)
# =================================================

# 1. API Upload Thumbnail (Dùng khi tạo/sửa bài viết)
# -> Tự động thêm vào thư viện Media
@auth.route("/api/upload-thumbnail", methods=["POST"])
@login_required
def upload_thumbnail():
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Xử lý tên file và lưu
    ext = file.filename.rsplit(".", 1)[1].lower() if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    # === [QUAN TRỌNG] Lưu vào Database Media ===
    media_type = "video" if ext in ["mp4", "mov", "avi", "webm"] else "image"
    media = Media(filename=filename, type=media_type)
    db.session.add(media)
    db.session.commit()
    # ===========================================

    return jsonify({
        "url": f"/uploads/{filename}",
        "media_id": media.id
    })

# 2. API Lấy danh sách Media (Cho trang Thư viện)
@auth.route("/api/media", methods=["GET"])
@login_required
def list_media():
    media_type = request.args.get("type")
    query = Media.query
    if media_type: query = query.filter_by(type=media_type)
    media_list = query.order_by(Media.id.desc()).all()
    
    results = []
    for m in media_list:
        
        if m.filename.startswith("http"):
            
            url = m.filename
            size_str = "Online"
        elif m.filename.startswith("static/"):
           
            url = f"/{m.filename}"
        
            real_path = os.path.join(os.getcwd(), "app", m.filename)
            size_str = get_file_size(real_path)
        else:
            url = f"/uploads/{m.filename}"
            real_path = os.path.join(UPLOAD_FOLDER, m.filename)
            size_str = get_file_size(real_path)

        results.append({
            "id": m.id,
            "filename": m.filename,
            "type": m.type,
            "url": url, 
            "created_at": m.created_at.strftime("%d/%m/%Y"),
            "size": size_str
        })
    return jsonify(results)

@auth.route("/api/media/upload", methods=["POST"])
@login_required
def upload_media_library():
    return upload_thumbnail() 

# 4. API Xóa Media
@auth.route("/api/media/<int:id>", methods=["DELETE"])
@login_required
def delete_media(id):
    media = Media.query.get_or_404(id)
    
    
    if not media.filename.startswith("http"):
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, media.filename))
        except:
            pass # File không tồn tại thì bỏ qua
            
    db.session.delete(media)
    db.session.commit()
    return jsonify({"message": "Đã xóa media"})

# 5. Route phục vụ file ảnh 
@auth.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@auth.route("/comments/<int:id>/approve", methods=["PUT"])
@login_required
def approve_comment(id):
    c = Comment.query.get_or_404(id); c.status = "approved"; db.session.commit()
    return jsonify({"message": "Đã duyệt"})

@auth.route("/comments/<int:id>/reject", methods=["PUT"])
@login_required
def reject_comment(id):
    c = Comment.query.get_or_404(id); c.status = "rejected"; db.session.commit()
    return jsonify({"message": "Đã từ chối"})

@auth.route("/comments/<int:id>/delete", methods=["PUT"])
@login_required
def delete_comment(id):
    c = Comment.query.get_or_404(id); c.status = "deleted"; db.session.commit()
    return jsonify({"message": "Đã xóa"})

@auth.route("/campaigns", methods=["POST"])
@login_required
def create_campaign():
    data = request.json; camp = Campaign(name=data["name"]); db.session.add(camp); db.session.commit()
    return jsonify({"message": "Đã tạo"})

@auth.route("/campaigns/<int:id>/pause", methods=["PUT"])
@login_required
def pause_campaign(id):
    camp = Campaign.query.get_or_404(id); camp.status = "paused"; db.session.commit()
    return jsonify({"message": "Đã tạm dừng"})

@auth.route("/campaigns/<int:id>/delete", methods=["PUT"])
@login_required
def delete_campaign(id):
    camp = Campaign.query.get_or_404(id); camp.status = "deleted"; db.session.commit()
    return jsonify({"message": "Đã xóa"})

@auth.route("/api/users", methods=["GET"])
@login_required
def list_users():
    # Lấy toàn bộ user, sắp xếp mới nhất
    users = User.query.order_by(User.id.desc()).all()
    
    results = []
    for u in users:
        # Đếm số bài viết thật
        post_count = 0 
        # Nếu model Post có liên kết user thì dùng: u.posts.count()
        
        results.append({
            "id": u.id,
            "fullname": u.fullname or u.username,
            "email": u.email,
            "role": u.role,
            "is_active": u.is_active,
            "post_count": post_count,
            "last_login": u.last_login.strftime("%d/%m/%Y %H:%M") if u.last_login else "Chưa đăng nhập",
            # Gửi kèm thông tin avatar tự động để Frontend vẽ
            "avatar_text": u.avatar_initials,
            "avatar_bg": u.avatar_color
        })
        
    return jsonify(results)

@auth.route("/api/users", methods=["POST"])
@login_required
def create_user():
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email đã tồn tại"}), 400
        
    new_user = User(
        fullname=data['fullname'],
        email=data['email'],
        username=data['email'].split('@')[0],
        role=data['role']
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Thêm thành công"}), 201
