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

## 🎯 BƯỚC 4: CHẠY TẤT CẢ TESTS

### Dùng script tổng hợp

```bash
python run_tests.py
```

Script này sẽ:
1. Cho bạn chọn test nào muốn chạy
2. Chạy tests theo thứ tự
3. Hiển thị tổng kết cuối cùng

---

## 📊 BƯỚC 5: XEM BÁO CÁO

### Unit Test Report (CMD)

Kết quả hiển thị trực tiếp trong terminal với màu sắc và emoji.

### Selenium Test Report (HTML)

1. Mở file: `selenium_test_report.html`
2. Xem trong browser

**Report bao gồm:**
- 📈 Tổng số tests
- ✅ Tests passed
- ❌ Tests failed
- 📸 Screenshots của mỗi test
- ⏱️ Thời gian chạy
- 🐛 Error messages (nếu có)

---

## 🔧 TROUBLESHOOTING

### Lỗi: ChromeDriver not found

**Giải pháp:**
```bash
pip install webdriver-manager
```

Hoặc download manual:
https://chromedriver.chromium.org/

### Lỗi: Connection refused (localhost:5000)

**Nguyên nhân:** Flask app chưa chạy

**Giải pháp:**
```bash
# Terminal 1
python run.py

# Terminal 2
python tests/selenium_test_login.py
```

### Lỗi: ModuleNotFoundError: No module named 'app'

**Giải pháp:**
```bash
# Đảm bảo chạy từ root folder
cd /path/to/hotel-media-webapp
python tests/unit_test_login.py
```

### Lỗi: Database is locked

**Giải pháp:**
```bash
# Xóa file database cũ
rm hotel_media.db
python init_db.py
```

---

## 📝 STRUCTURE FILE

```
hotel-media-webapp/
├── tests/
│   ├── __init__.py
│   ├── unit_test_login.py          # Unit tests
│   ├── selenium_test_login.py      # Selenium tests
│   └── test_screenshots/           # Screenshots (auto-generated)
├── run_tests.py                     # Script chạy tất cả tests
├── selenium_test_report.html        # HTML report (auto-generated)
├── requirements_test.txt            # Test dependencies
└── TESTING_README.md               # File này
```

---

## 🎓 GIẢI THÍCH CHI TIẾT

### Unit Test gồm:

1. **test_01_user_creation** - Tạo user mới
2. **test_02_password_hashing** - Password được hash
3. **test_03_password_verification_correct** - Verify password đúng
4. **test_04_password_verification_wrong** - Verify password sai
5. **test_05_user_repr** - User representation
6. **test_06_login_page_get** - GET request trang login
7. **test_07_login_with_correct_credentials** - Login đúng
8. **test_08_login_with_wrong_username** - Login sai username
9. **test_09_login_with_wrong_password** - Login sai password
10. **test_10_login_with_empty_fields** - Login trống
11. **test_11_login_with_inactive_user** - Login user inactive
12. **test_12_logout_functionality** - Logout
13. **test_13_user_query_by_username** - Query by username
14. **test_14_user_query_by_email** - Query by email
15. **test_15_unique_username_constraint** - Username unique

### Selenium Test gồm:

1. **test_01_login_page_loads** - Trang login load
2. **test_02_login_form_elements_exist** - Elements tồn tại
3. **test_03_login_with_empty_fields** - Login trống
4. **test_04_login_with_wrong_credentials** - Login sai
5. **test_05_login_with_correct_credentials** - Login đúng
6. **test_06_remember_me_checkbox** - Checkbox Remember Me
7. **test_07_password_field_masked** - Password được mask
8. **test_08_navigation_after_login** - Navigate sau login
9. **test_09_logout_functionality** - Logout

---

## 💡 TIPS

### Tăng tốc độ test

```python
# Trong selenium_test_login.py
chrome_options.add_argument('--headless')  # Chạy background
```

### Chạy test cụ thể

```bash
# Unit test
python -m unittest tests.unit_test_login.LoginUnitTest.test_01_user_creation

# Selenium test
python -m unittest tests.selenium_test_login.LoginSeleniumTest.test_01_login_page_loads
```

### Test coverage

```bash
coverage run -m pytest tests/
coverage report
coverage html  # Tạo HTML report
```

---

## 📸 DEMO SCREENSHOTS

Selenium test tự động chụp screenshot:
- ✅ Mỗi bước test quan trọng
- ❌ Khi test fail
- 📊 Lưu trong folder `test_screenshots/`

---

## ✅ CHECKLIST

- [ ] Đã cài đặt dependencies
- [ ] ChromeDriver đã sẵn sàng
- [ ] Flask app đang chạy (cho Selenium test)
- [ ] Database đã được khởi tạo
- [ ] Đã tạo folder `tests/`
- [ ] Đã copy các file test
- [ ] Unit test chạy thành công
- [ ] Selenium test chạy thành công
- [ ] HTML report được tạo
- [ ] Screenshots được lưu

---

## 🆘 HỖ TRỢ

Nếu gặp vấn đề:

1. Check logs trong terminal
2. Xem screenshot trong `test_screenshots/`
3. Đọc error message chi tiết
4. Kiểm tra Flask app có chạy không
5. Verify ChromeDriver version

---

## 📚 TÀI LIỆU THAM KHẢO

- Selenium Docs: https://selenium-python.readthedocs.io/
- unittest Docs: https://docs.python.org/3/library/unittest.html
- Flask Testing: https://flask.palletsprojects.com/en/2.3.x/testing/

---

**Good luck với testing! 🚀**
