# 🧪 HƯỚNG DẪN TESTING - HOTEL MEDIA WEBAPP

## 📋 Tổng quan

Dự án có 2 loại test:
1. **Unit Test** - Test backend logic (models, functions)
2. **Selenium Test** - Test giao diện frontend (UI/UX)

---

## 🚀 BƯỚC 1: CÀI ĐẶT

### 1.1 Tạo folder tests

```bash
mkdir tests
cd tests
```

### 1.2 Copy các file test

Copy 3 file sau vào folder `tests/`:
- `unit_test_login.py`
- `selenium_test_login.py`
- `__init__.py` (tạo file trống)

### 1.3 Cài đặt dependencies

```bash
# Cài dependencies cho testing
pip install selenium==4.15.2
pip install webdriver-manager==4.0.1
pip install pytest==7.4.3
pip install coverage==7.3.2
```

### 1.4 Download ChromeDriver

**Cách 1: Tự động (Khuyến nghị)**
```python
# Code sẽ tự động download ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager
```

**Cách 2: Thủ công**
1. Kiểm tra Chrome version: `chrome://version/`
2. Download ChromeDriver tại: https://chromedriver.chromium.org/
3. Giải nén và thêm vào PATH

---

## 🧪 BƯỚC 2: CHẠY UNIT TEST

### Cách 1: Chạy trực tiếp

```bash
python tests/unit_test_login.py
```

### Cách 2: Dùng pytest

```bash
pytest tests/unit_test_login.py -v
```

### Kết quả mong đợi:

```
======================================================================
🧪 BẮT ĐẦU UNIT TEST - LOGIN LOGIC
======================================================================

🧪 Test 1: Kiểm tra tạo user...
   ✓ User được tạo thành công
   ✓ Username: newuser
   ✓ Email: new@example.com
✅ PASSED

🧪 Test 2: Kiểm tra password hashing...
   ✓ Password không được lưu plain text
   ✓ Password hash length: 102
✅ PASSED

... (các test khác)

======================================================================
📊 TEST SUMMARY
======================================================================
Tests run: 15
✅ Passed: 15
❌ Failed: 0
⚠️  Errors: 0

🎉 ALL TESTS PASSED!
======================================================================
```

---

## 🌐 BƯỚC 3: CHẠY SELENIUM TEST

### 3.1 Khởi động Flask app

**Terminal 1:**
```bash
python run.py
```

Đảm bảo app chạy ở: `http://localhost:5000`

### 3.2 Chạy Selenium test

**Terminal 2:**
```bash
python tests/selenium_test_login.py
```

### 3.3 Xem kết quả

Test sẽ tự động:
- ✅ Mở Chrome browser
- ✅ Test từng chức năng
- ✅ Chụp screenshots
- ✅ Tạo HTML report

**File output:**
- `selenium_test_report.html` - Báo cáo HTML đẹp
- `test_screenshots/` - Folder chứa screenshots

### Kết quả mong đợi:

```
======================================================================
🚀 BẮT ĐẦU SELENIUM TEST - LOGIN FUNCTIONALITY
======================================================================

🧪 Test 1: Kiểm tra trang login load...
✅ Trang login load thành công!

🧪 Test 2: Kiểm tra các elements của form...
   ✓ Username field: OK
   ✓ Password field: OK
   ✓ Submit button: OK
✅ Tất cả elements đều tồn tại!

... (các test khác)

======================================================================
✅ HOÀN THÀNH SELENIUM TEST
📊 Kết quả đã được lưu vào: selenium_test_report.html
======================================================================
```

---


