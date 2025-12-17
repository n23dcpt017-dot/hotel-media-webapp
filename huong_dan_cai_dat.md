# HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY THỬ DỰ ÁN

## Cấu trúc
- Thư mục `routes`: chứa toàn bộ code (CRUD + demo).
- `hotel_media_platform.sql`: script tạo database + bảng.
- `requirements.txt`: thư viện cần cài.
  
## Cài đặt

```bash
git clone https://github.com/n23dcpt017-dot/hotel-media-webapp.git
cd hotel-media-webapp
```

## Hướng dẫn chạy

### Khởi tạo database

Chạy theo thứ tự các lệnh sau:

```bash
python seed_users.py
python seed_media.py
python seed_comments.py
python seed_campaigns.py
```

### Khởi tạo môi trường chạy trên localhost

```bash
python run.py
```

Ứng dụng sẽ chạy tại: `http://127.0.0.1:5000/`

### Truy cập ứng dụng

Truy cập trang đăng nhập: `http://127.0.0.1:5000/auth/login`
