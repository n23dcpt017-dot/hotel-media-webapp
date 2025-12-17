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
from datetime import datetime # Import datetime ở đầu file luôn cho chuẩn

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

    user = User.query.filter((User.username == username) | (User.email == username)).first()

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
# FRONTEND PAGES
# =================================================
@auth.route("/")
@auth.route("/dashboard")
@login_required
def dashboard():
    return render_template("tongquan.html")

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

# ... (Giữ nguyên các route render template khác của bạn ở đây: quanlylivestream, thuvienmedia...) ...
# Để ngắn gọn mình không paste lại hết các route render html không thay đổi logic

# =================================================
# POSTS API (ĐÃ SỬA LỖI NGÀY THÁNG)
# =================================================

@auth.route("/api/posts", methods=["POST"])
@login_required
def create_post():
    data = request.json

    if not data.get("title"):
        return jsonify({"error": "Thiếu tiêu đề"}), 400

    publish_at = None
    # XỬ LÝ NGÀY THÁNG CHUẨN VIỆT NAM (dd/mm/yyyy)
    if data.get("publish_at"):
        try:
            # Sửa từ fromisoformat sang strptime để khớp với frontend
            publish_at = datetime.strptime(data["publish_at"], "%d/%m/%Y")
        except ValueError:
            return jsonify({"error": "Định dạng ngày không hợp lệ (yêu cầu: dd/mm/yyyy)"}), 400

    post = Post(
        title=data["title"],
        content=data.get("content"),
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
    post.status = data.get("status", post.status)
    
    # Cũng sửa logic ngày tháng cho phần update
    if data.get("publish_at"):
        try:
            post.publish_at = datetime.strptime(data["publish_at"], "%d/%m/%Y")
        except ValueError:
             return jsonify({"error": "Định dạng ngày không hợp lệ"}), 400

    db.session.commit()
    return jsonify({"message": "Cập nhật thành công"})


@auth.route("/api/posts/<int:id>", methods=["DELETE"])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    # Nếu bạn dùng Soft Delete (is_deleted) thì giữ dòng dưới
    # post.is_deleted = True 
    # Nếu muốn xóa thật thì dùng:
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Đã xóa"})

@auth.route("/api/posts")
@login_required
def list_posts():
    # Sửa lại logic lấy list nếu cần
    posts = Post.query.order_by(Post.created_at.desc()).all()
    
    return jsonify([
        {
            "id": p.id,
            "title": p.title,
            "status": p.status,
            # Trả về ngày định dạng dd/mm/yyyy cho dễ nhìn
            "publish_at": p.publish_at.strftime("%d/%m/%Y") if p.publish_at else None,
            "image": p.image,
            "category": getattr(p, 'category', 'Tin tức'), # getattr để tránh lỗi nếu chưa có cột category
            "author": getattr(p, 'author', 'Admin')
        }
        for p in posts
    ])

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
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    return jsonify({
        "url": f"/uploads/{filename}"
    })
