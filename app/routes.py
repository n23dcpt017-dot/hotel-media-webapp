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
import os

auth = Blueprint("auth", __name__)

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

    user = User.query.filter_by(username=username).first()

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

# =================================================
# POSTS (ẨN / KHÔI PHỤC)
# =================================================
@auth.route("/posts", methods=["POST"])
@login_required
def create_post():
    data = request.json
    post = Post(title=data["title"], content=data["content"])
    db.session.add(post)
    db.session.commit()
    return jsonify({"message": "Đã thêm bài viết"}), 201

@auth.route("/posts/<int:id>", methods=["PUT"])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    data = request.json
    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)
    db.session.commit()
    return jsonify({"message": "Đã cập nhật bài viết"})

@auth.route("/posts/<int:id>/hide", methods=["PUT"])
@login_required
def hide_post(id):
    post = Post.query.get_or_404(id)
    post.is_hidden = True
    db.session.commit()
    return jsonify({"message": "Đã ẩn bài viết"})

@auth.route("/posts/<int:id>/restore", methods=["PUT"])
@login_required
def restore_post(id):
    post = Post.query.get_or_404(id)
    post.is_hidden = False
    db.session.commit()
    return jsonify({"message": "Đã khôi phục bài viết"})

# =================================================
# COMMENTS (APPROVED / REJECTED / DELETED)
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
# MEDIA (UPLOAD / ẨN / TẢI)
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
