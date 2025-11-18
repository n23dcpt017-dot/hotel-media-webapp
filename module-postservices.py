from app.models.post import Post
from app import db
from datetime import datetime

class PostService:
    @staticmethod
    def get_all_posts():
        """Lấy tất cả bài viết"""
        return Post.query.order_by(Post.created_at.desc()).all()
    
    @staticmethod
    def create_post(title, content, author_id):
        """Tạo bài viết mới"""
        post = Post(
            title=title,
            content=content,
            author_id=author_id,
            status='draft'
        )
        db.session.add(post)
        db.session.commit()
        return post
    
    @staticmethod
    def publish_post(post_id):
        """Xuất bản bài viết"""
        post = Post.query.get(post_id)
        if post:
            post.status = 'published'
            post.published_at = datetime.utcnow()
            db.session.commit()
        return post
    
    @staticmethod
    def delete_post(post_id):
        """Xóa bài viết"""
        post = Post.query.get(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
        return True
