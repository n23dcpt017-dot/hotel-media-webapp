# 🚀 HƯỚNG DẪN CÀI ĐẶT VÀ HOÀN THIỆN DỰ ÁN

## 📋 BƯỚC 1: TẢI VỀ VÀ TỔ CHỨC FILE

### 1.1 Clone repo về máy

```bash
git clone https://github.com/n23dcpt017-dot/hotel-media-webapp.git
cd hotel-media-webapp
```

### 1.2 Tạo cấu trúc thư mục đầy đủ

```bash
# Tạo folder static
mkdir -p app/static/css
mkdir -p app/static/js
mkdir -p app/static/images
mkdir -p app/static/uploads

# Tạo folder templates đầy đủ
mkdir -p app/templates/auth
mkdir -p app/templates/dashboard
mkdir -p app/templates/baiviet
mkdir -p app/templates/binhluan
mkdir -p app/templates/chienich
mkdir -p app/templates/nguoidung
mkdir -p app/templates/quanly
mkdir -p app/templates/media
mkdir -p app/templates/errors
```

---

## 📋 BƯỚC 2: COPY CÁC FILE CSS/JS

### 2.1 Copy CSS files

Từ artifacts tôi tạo, copy vào đúng vị trí:

```
app/static/css/style.css      ← Main CSS
app/static/css/upload.css     ← Upload styling
```

### 2.2 Copy JavaScript files

```
app/static/js/main.js         ← Main JS
app/static/js/upload.js       ← Upload handler
```

---

## 📋 BƯỚC 3: CẬP NHẬT HTML FILES

### 3.1 Sửa tất cả file HTML hiện tại

**LƯU Ý:** Mỗi file HTML cần thêm 3 dòng này vào `<head>`:

```html
<link rel="stylesheet" href="/static/css/style.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
```

Và trước `</body>`:

```html
<script src="/static/js/main.js"></script>
```

### 3.2 Ví dụ: index.html

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Hotel Media</title>
    
    <!-- ✅ THÊM 2 DÒNG NÀY -->
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <!-- Nội dung HTML cũ của bạn -->
    
    <!-- ✅ THÊM DÒNG NÀY TRƯỚC </body> -->
    <script src="/static/js/main.js"></script>
</body>
</html>
```

### 3.3 Copy template mẫu

File `dashboard.html` tôi tạo là TEMPLATE MẪU hoàn chỉnh. Bạn có thể:
- Copy toàn bộ để thay thế `index.html` hiện tại
- Hoặc tham khảo structure để sửa các file khác

---

## 📋 BƯỚC 4: DI CHUYỂN HTML VÀO ĐÚNG FOLDER

Di chuyển các file HTML hiện tại vào các folder tương ứng:

```bash
# Auth
mv login.html app/templates/auth/

# Dashboard
mv index.html app/templates/dashboard/
mv tongguan.html app/templates/dashboard/
mv analytics.html app/templates/dashboard/

# Bài viết
mv baiviet.html app/templates/baiviet/
mv suabaiviet.html app/templates/baiviet/
mv xuatban.html app/templates/baiviet/

# Bình luận
mv binhluan.html app/templates/binhluan/
mv binhluanchoduyet.html app/templates/binhluan/
mv binhluandaduyet.html app/templates/binhluan/
mv binhluantuchoi.html app/templates/binhluan/

# Chiến dịch
mv chienich.html app/templates/chienich/
mv chienichchitiet.html app/templates/chienich/
mv chienichchitamdung.html app/templates/chienich/
mv chienichtamdung.html app/templates/chienich/

# Người dùng
mv nguoidung.html app/templates/nguoidung/
mv nguoidungdanhmoi.html app/templates/nguoidung/
mv nguoidungngoitieu.html app/templates/nguoidung/
mv nguoidungviewer.html app/templates/nguoidung/

# Quản lý
mv quanlybaiviet.html app/templates/quanly/
mv quanlybaivietdalenlich.html app/templates/quanly/
mv quanlybaivietdauxatban.html app/templates/quanly/
mv quanlybaivienthap.html app/templates/quanly/
mv quanlylivestream.html app/templates/quanly/

# Media
mv thuvienmedia.html app/templates/media/
mv thuvienmediaanh.html app/templates/media/
mv thuvienmediavideo.html app/templates/media/
```

---

## 📋 BƯỚC 5: CẬP NHẬT ROUTES (Python)

### 5.1 Update file `app/routes/media.py`

Thay thế function `upload()` cũ bằng version mới trong artifact "all_remaining_routes" (đã update).

### 5.2 Cần thêm import

Đầu file `app/routes/media.py`:

```python
from datetime import datetime
```

---

## 📋 BƯỚC 6: CÀI ĐẶT DEPENDENCIES

### 6.1 Update requirements.txt

Thêm Pillow để xử lý ảnh:

```txt
pymysql
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-Migrate==4.0.5
Flask-WTF==1.2.1
WTForms==3.1.1
email-validator==2.1.0
python-dotenv==1.0.0
Pillow==10.1.0
gunicorn==21.2.0
unidecode==1.3.7
```

### 6.2 Cài đặt

```bash
pip install -r requirements.txt
```

---

## 📋 BƯỚC 7: TEST LOCAL

### 7.1 Khởi tạo database

```bash
python run.py
```

Hoặc:

```bash
python init_db.py
```

### 7.2 Chạy server

```bash
python run.py
```

### 7.3 Truy cập

```
http://localhost:5000/auth/login
```

**Login:**
- Username: `admin`
- Password: `Admin@123`

---

## 📋 BƯỚC 8: TEST CHỨC NĂNG

### 8.1 Test các trang chính

✅ Dashboard: `http://localhost:5000/dashboard`
✅ Bài viết: `http://localhost:5000/baiviet`
✅ Bình luận: `http://localhost:5000/binhluan`
✅ Upload: `http://localhost:5000/media`

### 8.2 Test upload file

1. Vào `/media`
2. Kéo thả file ảnh/video vào dropzone
3. Click "Upload tất cả"
4. Kiểm tra file trong `app/static/uploads/`

---

## 📋 BƯỚC 9: COMMIT VÀ PUSH LÊN GITHUB

```bash
# Add tất cả file
git add .

# Commit
git commit -m "Add complete frontend (CSS/JS) and file upload"

# Push
git push origin main
```

---

## 📋 BƯỚC 10: DEPLOY LÊN RENDER

### 10.1 Đảm bảo có các file

- ✅ `requirements.txt`
- ✅ `wsgi.py`
- ✅ `render.yaml`
- ✅ `Procfile`

### 10.2 Trên Render.com

1. Vào Dashboard
2. Click service hiện tại
3. Click "Manual Deploy" → "Deploy latest commit"
4. Chờ build xong (~5 phút)

### 10.3 Khởi tạo database trên Render

Vào **Shell** tab, chạy:

```bash
python init_db.py
```

---

## ✅ CHECKLIST HOÀN THIỆN

- [ ] CSS files đã copy vào `app/static/css/`
- [ ] JS files đã copy vào `app/static/js/`
- [ ] Tất cả HTML đã thêm link CSS/JS
- [ ] HTML files đã di chuyển vào đúng folder
- [ ] Routes đã update (media upload)
- [ ] Dependencies đã cài đặt
- [ ] Database đã khởi tạo
- [ ] Test local thành công
- [ ] Commit và push lên GitHub
- [ ] Deploy lên Render thành công

---

## 🎯 KẾT QUẢ CUỐI CÙNG

Sau khi hoàn thành, bạn sẽ có:

✅ **Frontend đẹp** với CSS responsive
✅ **Upload file** hoạt động với drag & drop
✅ **Dashboard** với thống kê và charts
✅ **Tất cả trang** có UI/UX hoàn chỉnh
✅ **Deploy thành công** trên Render
✅ **Sẵn sàng** cho báo cáo và demo!

---

## 💡 TIPS QUAN TRỌNG

1. **Luôn test local trước** khi push lên GitHub
2. **Backup database** trước khi deploy
3. **Check logs** nếu có lỗi: Render Dashboard → Logs
4. **Đổi mật khẩu admin** ngay sau khi deploy
5. **Chụp ảnh màn hình** các trang để làm báo cáo

---

## 🆘 NẾU GẶP LỖI

### Lỗi: CSS không load

**Nguyên nhân:** Path sai

**Giải pháp:**
```html
<!-- Thay vì -->
<link rel="stylesheet" href="static/css/style.css">

<!-- Dùng -->
<link rel="stylesheet" href="/static/css/style.css">
```

### Lỗi: Upload không hoạt động

**Nguyên nhân:** Folder uploads không tồn tại

**Giải pháp:**
```bash
mkdir -p app/static/uploads
chmod 755 app/static/uploads
```

### Lỗi: 404 Not Found

**Nguyên nhân:** Route không đúng

**Kiểm tra:** File HTML có ở đúng folder trong `app/templates/` không?

---

## 📞 HỖ TRỢ

Nếu cần giúp đỡ, cung cấp:
1. Screenshot lỗi
2. Log từ terminal
3. File bạn đang sửa
