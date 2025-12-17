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
# OAUTH (GOOGLE / FACEBOOK / ZALO / TIKTOK)
# =================================================
def oauth_login(provider, email):
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            username=email.split("@")[0],
            email=email,
            role="user"
        )
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for("auth.tongquan_html"))

@auth.route("/login/google")
def login_google():
    return oauth_login("google", "google_user@gmail.com")

@auth.route("/login/facebook")
def login_facebook():
    return oauth_login("facebook", "fb_user@gmail.com")

@auth.route("/login/zalo")
def login_zalo():
    return oauth_login("zalo", "zalo_user@gmail.com")

@auth.route("/login/tiktok")
def login_tiktok():
    return oauth_login("tiktok", "tiktok_user@gmail.com")

# =================================================
# FRONTEND PAGES
# =================================================
@auth.route("/")
@auth.route("/dashboard")
@login_required
def dashboard():
    return render_template("tongquan.html")

@auth.route("/index")
@login_required
def index():
    return render_template("index.html")

@auth.route("/tongquan.html")
@login_required
def tongquan_html():
    return render_template("tongquan.html")

@auth.route("/quanlybaiviet.html")
@login_required
def page_quanly_baiviet():
    return render_template("quanlybaiviet.html")

@auth.route("/taobaiviet.html")
@login_required
def tao_baiviet():
    return render_template("taobaiviet.html")

@auth.route("/suabaiviet.html")
@login_required
def sua_baiviet():
    return render_template("suabaiviet.html")

# Các route trang khác (giữ nguyên hoặc thêm nếu cần)
@auth.route("/quanlylivestream.html")
@login_required
def page_quanly_livestream():
    return render_template("quanlylivestream.html")

@auth.route("/thuvienmedia.html")
@login_required
def page_thuvien_media():
    return render_template("thuvienmedia.html")

@auth.route("/nguoidung.html")
@login_required
def page_nguoidung():
    return render_template("nguoidung.html")

@auth.route("/analyticsvaseo.html")
@login_required
def page_analytics():
    return render_template("analyticsvaseo.html")

@auth.route("/binhluan.html")
@login_required
def page_binhluan():
    return render_template("binhluan.html")

@auth.route("/chiendich.html")
@login_required
def page_chiendich():
    return render_template("chiendich.html")

@auth.route("/xuatban.html")
@login_required
def page_xuatban():
    return render_template("xuatban.html")

# =================================================
# POSTS API (CREATE / UPDATE / DELETE / LIST)
# =================================================

@auth.route("/api/posts", methods=["POST"])
@login_required
def create_post():
    data = request.json

    if not data.get("title"):
        return jsonify({"error": "Thiếu tiêu đề"}), 400

    publish_at = None
    if data.get("publish_at"):
        try:
            # Sửa thành %d/%m/%Y để khớp với Frontend (dd/mm/yyyy)
            publish_at = datetime.strptime(data["publish_at"], "%d/%m/%Y")
        except ValueError:
            return jsonify({"error": "Định dạng ngày không hợp lệ (dd/mm/yyyy)"}), 400

    post = Post(
        title=data["title"],
        content=data.get("content"),
        category=data.get("category", "phong"),
        status=data.get("status", "draft"),
        publish_at=publish_at,
        image=data.get("image") or "/static/images/phong1.png",
        author=current_user.username if current_user.is_authenticated else "Admin",
        view=0
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({
        "message": "Tạo bài viết thành công",
        "id": post.id
    }), 201


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
        try:
            post.publish_at = datetime.strptime(data["publish_at"], "%d/%m/%Y")
        except ValueError:
            return jsonify({"error": "Định dạng ngày không hợp lệ (dd/mm/yyyy)"}), 400

    if data.get("image"):
        post.image = data["image"]

    db.session.commit()
    return jsonify({"message": "Cập nhật thành công"})


@auth.route("/api/posts/<int:id>", methods=["DELETE"])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    # Nếu dùng soft delete thì: post.is_deleted = True
    # Nếu xóa thật thì:
    db.session.delete(post)
    
    db.session.commit()
    return jsonify({"message": "Đã xóa"})


@auth.route("/api/posts")
@login_required
def list_posts():
    status = request.args.get("status")
    
    # Nếu model không có is_deleted thì bỏ filter này
    query = Post.query
    # query = Post.query.filter_by(is_deleted=False) 

    if status:
        query = query.filter_by(status=status)

    posts = query.order_by(Post.created_at.desc()).all()

    return jsonify([
        {
            "id": p.id,
            "title": p.title,
            "status": p.status,
            # Trả về ngày hiển thị đẹp
            "publish_at": p.publish_at.strftime("%d/%m/%Y") if p.publish_at else None,
            "image": p.image,
            "category": getattr(p, "category", ""),
            "author": getattr(p, "author", "Admin")
        }
        for p in posts
    ])

# =================================================
# UPLOAD THUMBNAIL
# =================================================
@auth.route("/api/upload-thumbnail", methods=["POST"])
@login_required
def upload_thumbnail():
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.jpg"
    path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
    file.save(path)

    return jsonify({
        "url": f"/uploads/{filename}"
    })

@auth.route("/uploads/<path:filename>")
@login_required
def get_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# =================================================
# COMMENTS
# =================================================
@auth.route("/comments/<int:id>/approve", methods=["PUT"])
@login_required
def approve_comment(id):
    c = Comment.query.get_or_404(id)
    c.status = "approved"
    db.session.commit()
    return jsonify({"message": "Đã duyệt comment"})


@auth.route("/comments/<int:id>/reject", methods=["PUT"])
@login_required
def reject_comment(id):
    c = Comment.query.get_or_404(id)
    c.status = "rejected"
    db.session.commit()
    return jsonify({"message": "Đã từ chối comment"})


@auth.route("/comments/<int:id>/delete", methods=["PUT"])
@login_required
def delete_comment(id):
    c = Comment.query.get_or_404(id)
    c.status = "deleted"
    db.session.commit()
    return jsonify({"message": "Đã xóa comment"})

# =================================================
# CAMPAIGNS
# =================================================
@auth.route("/campaigns", methods=["POST"])
@login_required
def create_campaign():
    data = request.json
    camp = Campaign(name=data["name"])
    db.session.add(camp)
    db.session.commit()
    return jsonify({"message": "Đã tạo campaign"})


@auth.route("/campaigns/<int:id>/pause", methods=["PUT"])
@login_required
def pause_campaign(id):
    camp = Campaign.query.get_or_404(id)
    camp.status = "paused"
    db.session.commit()
    return jsonify({"message": "Đã tạm dừng campaign"})


@auth.route("/campaigns/<int:id>/delete", methods=["PUT"])
@login_required
def delete_campaign(id):
    camp = Campaign.query.get_or_404(id)
    camp.status = "deleted"
    db.session.commit()
    return jsonify({"message": "Đã xóa campaign"})

# =================================================
# MEDIA
# =================================================
@auth.route("/media/upload", methods=["POST"])
@login_required
def upload_media():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "Không có file"}), 400

    os.makedirs("uploads", exist_ok=True)
    file.save(f"uploads/{file.filename}")

    media = Media(filename=file.filename)
    db.session.add(media)
    db.session.commit()

    return jsonify({"message": "Upload thành công"})


@auth.route("/media/<filename>")
@login_required
def get_media(filename):
    return send_from_directory("uploads", filename)


@auth.route("/media/<int:id>/hide", methods=["PUT"])
@login_required
def hide_media(id):
    m = Media.query.get_or_404(id)
    m.is_hidden = True
    db.session.commit()
    return jsonify({"message": "Đã ẩn media"})
