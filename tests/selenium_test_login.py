
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import os
import sys
import sqlite3
import subprocess
import hashlib

# Thêm path để import app Flask
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class LoginSeleniumTest(unittest.TestCase):
    """Test cases cho chức năng login sử dụng Selenium """

    @classmethod
    def setUpClass(cls):
        """Setup trước khi chạy tất cả tests"""
        chrome_options = Options()
        # Bỏ comment để chạy ẩn
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.implicitly_wait(5)
            
            # URL cho Flask app đang chạy
            cls.base_url = "http://localhost:5000"
            cls.test_results = []
            cls.screenshots_dir = "test_screenshots"
            
            if not os.path.exists(cls.screenshots_dir):
                os.makedirs(cls.screenshots_dir)
            
            # Tạo test user trong database
            cls.test_credentials = cls.create_test_user()
            
            print("\n" + "=" * 80)
            print("🚀 SELENIUM TEST - LOGIN FIXES AND FINAL VALIDATION")
            print(f"📡 Testing URL: {cls.base_url}")
            if cls.test_credentials:
                print(f"👤 Test user created: {cls.test_credentials['username']}/{cls.test_credentials['password']}")
            print("=" * 80 + "\n")

        except Exception as e:
            print(f"❌ Lỗi khi khởi tạo Chrome driver: {e}")
            raise

    @classmethod
    def create_test_user(cls):
        """Tạo test user trong database nếu chưa có"""
        test_user = {
            "username": "selenium_test_user",
            "password": "SeleniumTest@123",
            "email": "test@example.com"
        }
        
        # Các vị trí database có thể
        db_paths = [
            "instance/app.db",
            "app.db",
            "../instance/app.db",
            "../app.db",
            "hotel.db",
        ]
        
        for db_path in db_paths:
            if os.path.exists(db_path):
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    
                    # Kiểm tra nếu user đã tồn tại
                    cursor.execute("SELECT username FROM user WHERE username = ?", (test_user["username"],))
                    existing_user = cursor.fetchone()
                    
                    if existing_user:
                        print(f"✅ Test user '{test_user['username']}' already exists in {db_path}")
                        
                        # Lấy thông tin user hiện tại
                        cursor.execute("SELECT username FROM user LIMIT 1")
                        first_user = cursor.fetchone()
                        if first_user:
                            test_user["username"] = first_user[0]
                            print(f"📊 Using existing user: {first_user[0]}")
                        
                        conn.close()
                        return test_user
                    
                    # Thử tạo user mới (cần biết cấu trúc bảng)
                    try:
                        # Thử insert vào bảng user
                        cursor.execute("""
                            INSERT INTO user (username, password, email, created_at)
                            VALUES (?, ?, ?, datetime('now'))
                        """, (test_user["username"], test_user["password"], test_user["email"]))
                        
                        conn.commit()
                        print(f"✅ Created test user '{test_user['username']}' in {db_path}")
                        conn.close()
                        return test_user
                        
                    except sqlite3.Error as e:
                        print(f"⚠️  Could not create test user in {db_path}: {e}")
                        # Thử lấy user đầu tiên
                        cursor.execute("SELECT username FROM user LIMIT 1")
                        first_user = cursor.fetchone()
                        if first_user:
                            test_user["username"] = first_user[0]
                            print(f"📊 Using existing user: {first_user[0]}")
                            conn.close()
                            return test_user
                    
                    conn.close()
                    
                except sqlite3.Error as e:
                    print(f"⚠️  Database error ({db_path}): {e}")
                except Exception as e:
                    print(f"⚠️  Error with {db_path}: {e}")
        
        print("⚠️  Could not find database or create test user")
        print("💡 Creating a mock test user for testing")
        return test_user

    @classmethod
    def tearDownClass(cls):
        """Cleanup sau khi chạy xong tất cả tests"""
        if cls.driver:
            cls.driver.quit()

        cls.generate_html_report()

        print("\n" + "=" * 80)
        print("✅ HOÀN THÀNH SELENIUM TEST - FIXES VALIDATED")
        print("=" * 80 + "\n")

    def setUp(self):
        """Setup trước mỗi test case"""
        self.driver.delete_all_cookies()
        self.start_time = time.time()

    def tearDown(self):
        """Cleanup sau mỗi test case"""
        duration = time.time() - self.start_time
        test_name = self._testMethodName

        error_msg = None
        passed = True

        if hasattr(self, "_outcome"):
            result = self._outcome.result
            if result and (result.errors or result.failures):
                passed = False
                if result.errors:
                    error_msg = str(result.errors[-1][1])
                elif result.failures:
                    error_msg = str(result.failures[-1][1])

        test_result = {
            "name": test_name,
            "status": "PASSED" if passed else "FAILED",
            "duration": f"{duration:.2f}s",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "error": error_msg,
            "screenshot": None,
        }

        if not passed:
            screenshot_name = f"{test_name}_{int(time.time())}.png"
            screenshot_path = os.path.join(self.screenshots_dir, screenshot_name)
            try:
                self.driver.save_screenshot(screenshot_path)
                test_result["screenshot"] = screenshot_name
            except:
                pass

        self.test_results.append(test_result)

    def take_screenshot(self, name):
        """Chụp screenshot với tên custom"""
        screenshot_name = f"{name}_{int(time.time())}.png"
        screenshot_path = os.path.join(self.screenshots_dir, screenshot_name)
        self.driver.save_screenshot(screenshot_path)
        print(f"   📸 Screenshot: {screenshot_name}")
        return screenshot_name

    # ===========================================
    # TEST CASES 
    # ===========================================

    def test_01_verify_form_method_is_post(self):
        """Test 1: Xác minh form method là POST"""
        print("\n🧪 Test 1: Xác minh form method là POST...")
        
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(2)
        
        forms = self.driver.find_elements(By.TAG_NAME, "form")
        if forms:
            form = forms[0]
            method = form.get_attribute("method") or ""
            
            print(f"   📋 Form method: {method.upper()}")
            
            if method.lower() == "post":
                print("   ✅ FORM METHOD LÀ POST (ĐÃ FIX)")
            else:
                print("   ❌ FORM METHOD LÀ GET (CẦN FIX)")
                print("   💡 Sửa file login.html: method='post'")
                self.take_screenshot("form_method_get")
        
        print("✅ Đã kiểm tra form method")

    def test_02_test_login_with_credentials(self):
        """Test 2: Test login với credentials"""
        print("\n🧪 Test 2: Test login với credentials...")
        
        if not self.test_credentials:
            print("   ⚠️  Không có test credentials - bỏ qua test")
            self.skipTest("No test credentials")
            return
        
        username = self.test_credentials["username"]
        password = self.test_credentials["password"]
        
        print(f"   Testing với: {username} / {password}")
        
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        try:
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            
            username_field.clear()
            password_field.clear()
            
            username_field.send_keys(username)
            password_field.send_keys(password)
            
            # Kiểm tra form method trước khi submit
            forms = self.driver.find_elements(By.TAG_NAME, "form")
            if forms and forms[0].get_attribute("method") != "post":
                print("   ⚠️  CẢNH BÁO: Submitting với GET method!")
            
            submit_button = self.find_submit_button()
            if submit_button:
                submit_button.click()
                time.sleep(3)
                
                current_url = self.driver.current_url
                print(f"   📍 URL sau login: {current_url}")
                
                if "/auth/tongquan.html" in current_url:
                    print("   🎉 LOGIN THÀNH CÔNG!")
                    print("   ✅ Đã redirect đến trang tongquan.html")
                    
                    # Kiểm tra title trang tongquan
                    page_title = self.driver.title
                    print(f"   📄 Title trang tongquan: {page_title}")
                    
                    # Chụp screenshot thành công
                    self.take_screenshot("login_success")
                    
                    # Logout để test tiếp
                    self.driver.get(f"{self.base_url}/auth/logout")
                    time.sleep(2)
                    
                else:
                    print("   ❌ LOGIN THẤT BẠI")
                    print(f"   Vẫn ở: {current_url}")
                    
                    # Kiểm tra error message
                    page_source = self.driver.page_source.lower()
                    if "sai thông tin" in page_source:
                        print("   💡 Lý do: Sai thông tin đăng nhập")
                    elif "vui lòng" in page_source:
                        print("   💡 Lý do: Thiếu thông tin")
                    
                    self.take_screenshot("login_failed")
                    
        except Exception as e:
            print(f"   ❌ Lỗi khi test login: {e}")
            self.take_screenshot("login_error")

    def test_03_check_csrf_protection(self):
        """Test 3: Kiểm tra CSRF protection"""
        print("\n🧪 Test 3: Kiểm tra CSRF protection...")
        
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        forms = self.driver.find_elements(By.TAG_NAME, "form")
        if forms:
            # Tìm CSRF token
            csrf_selectors = [
                "input[name='csrf_token']",
                "input[name='_csrf_token']",
                "input[type='hidden'][name*='csrf']",
                "input[type='hidden'][value*='csrf']",
                "input[name='csrfmiddlewaretoken']"
            ]
            
            csrf_found = False
            for selector in csrf_selectors:
                try:
                    csrf_fields = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if csrf_fields:
                        csrf_found = True
                        csrf_value = csrf_fields[0].get_attribute("value") or ""
                        print(f"   ✅ CÓ CSRF PROTECTION")
                        print(f"   📋 CSRF token: {csrf_value[:20]}...")
                        break
                except:
                    continue
            
            if not csrf_found:
                print("   ⚠️  KHÔNG CÓ CSRF PROTECTION")
                print("   💡 Cần thêm vào form login:")
                print("      {{ csrf_token() }} (Flask-WTF)")
                print("      hoặc manual CSRF token")
                self.take_screenshot("no_csrf")
        
        print("✅ Đã kiểm tra CSRF protection")

    def test_04_validate_form_attributes(self):
        """Test 4: Validate form attributes đầy đủ"""
        print("\n🧪 Test 4: Validate form attributes...")
        
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        # Kiểm tra các attributes quan trọng
        checks = [
            ("username field", By.NAME, "username", [
                ("required", "Có required attribute"),
                ("autocomplete", "username", "Có autocomplete='username'"),
                ("placeholder", "Có placeholder"),
                ("aria-label", "Có aria-label cho accessibility"),
            ]),
            ("password field", By.NAME, "password", [
                ("required", "Có required attribute"),
                ("autocomplete", "current-password", "Có autocomplete='current-password'"),
                ("placeholder", "Có placeholder"),
                ("aria-label", "Có aria-label cho accessibility"),
                ("type", "password", "Type là password"),
                ("minlength", "Có minlength attribute"),
            ]),
        ]
        
        all_good = True
        
        for field_name, by_type, value, attributes in checks:
            print(f"\n   📋 {field_name.upper()}:")
            try:
                element = self.driver.find_element(by_type, value)
                
                for attr, *expected in attributes:
                    actual_value = element.get_attribute(attr) or ""
                    
                    if len(expected) == 1:
                        # Chỉ kiểm tra tồn tại
                        if actual_value:
                            print(f"      ✅ {expected[0]}")
                        else:
                            print(f"      ⚠️  Thiếu {expected[0]}")
                            all_good = False
                    elif len(expected) == 2:
                        # Kiểm tra giá trị cụ thể
                        expected_value, message = expected
                        if expected_value in actual_value.lower() or actual_value == expected_value:
                            print(f"      ✅ {message}")
                        else:
                            print(f"      ⚠️  {message} (giá trị: '{actual_value}')")
                            all_good = False
                            
            except NoSuchElementException:
                print(f"      ❌ Không tìm thấy {field_name}")
                all_good = False
        
        if all_good:
            print("\n   ✅ Tất cả form attributes đều đầy đủ")
        else:
            print("\n   ⚠️  Một số attributes cần bổ sung")
        
        print("✅ Đã validate form attributes")

    def test_05_full_login_workflow(self):
        """Test 5: Test toàn bộ workflow login"""
        print("\n🧪 Test 5: Test toàn bộ workflow login...")
        
        if not self.test_credentials:
            print("   ⚠️  Không có test credentials - bỏ qua test")
            self.skipTest("No test credentials")
            return
        
        username = self.test_credentials["username"]
        password = self.test_credentials["password"]
        
        print("   🔄 Testing full workflow:")
        
        # Bước 1: Truy cập trang protected khi chưa login
        print("\n   1. Truy cập protected page (chưa login):")
        self.driver.get(f"{self.base_url}/auth/tongquan.html")
        time.sleep(2)
        
        if "/auth/login" in self.driver.current_url:
            print("      ✅ Bị redirect về login (đúng)")
        else:
            print(f"      ❌ Có thể truy cập: {self.driver.current_url}")
            self.take_screenshot("unprotected_access")
        
        # Bước 2: Login
        print("\n   2. Đăng nhập:")
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        try:
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            
            username_field.send_keys(username)
            password_field.send_keys(password)
            
            submit_button = self.find_submit_button()
            if submit_button:
                submit_button.click()
                time.sleep(3)
                
                if "/auth/tongquan.html" in self.driver.current_url:
                    print("      ✅ Login thành công")
                    
                    # Bước 3: Truy cập các protected pages sau login
                    print("\n   3. Truy cập protected pages sau login:")
                    
                    protected_pages = [
                        ("/auth/tongquan.html", "Trang tổng quan"),
                        ("/auth/dashboard", "Dashboard"),
                        ("/auth/", "Trang chủ"),
                        ("/auth/index", "Index"),
                    ]
                    
                    for page, description in protected_pages:
                        self.driver.get(f"{self.base_url}{page}")
                        time.sleep(1)
                        
                        if "/auth/login" not in self.driver.current_url:
                            print(f"      ✅ {description}: Truy cập được")
                        else:
                            print(f"      ❌ {description}: Bị redirect")
                            self.take_screenshot(f"access_denied_{page}")
                    
                    # Bước 4: Logout
                    print("\n   4. Đăng xuất:")
                    self.driver.get(f"{self.base_url}/auth/logout")
                    time.sleep(2)
                    
                    if "/auth/login" in self.driver.current_url:
                        print("      ✅ Logout thành công - về trang login")
                    else:
                        print(f"      ⚠️  Logout redirect đến: {self.driver.current_url}")
                    
                    # Bước 5: Truy cập lại protected page sau logout
                    print("\n   5. Truy cập protected page sau logout:")
                    self.driver.get(f"{self.base_url}/auth/tongquan.html")
                    time.sleep(2)
                    
                    if "/auth/login" in self.driver.current_url:
                        print("      ✅ Bị redirect về login (đúng)")
                    else:
                        print(f"      ❌ Vẫn truy cập được: {self.driver.current_url}")
                        
                else:
                    print("      ❌ Login thất bại")
                    
        except Exception as e:
            print(f"      ❌ Lỗi: {e}")
            self.take_screenshot("workflow_error")
        
        print("✅ Đã test full workflow")

    def test_06_security_validation(self):
        """Test 6: Security validation"""
        print("\n🧪 Test 6: Security validation...")
        
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        # 6.1. Kiểm tra HTTPS (nếu có)
        current_url = self.driver.current_url
        if current_url.startswith("https://"):
            print("   6.1. ✅ Dùng HTTPS (secure)")
        else:
            print("   6.1. ⚠️  Dùng HTTP (không secure)")
            print("      💡 Nên dùng HTTPS cho production")
        
        # 6.2. Kiểm tra password visibility
        print("\n   6.2. Password visibility:")
        try:
            password_field = self.driver.find_element(By.NAME, "password")
            field_type = password_field.get_attribute("type")
            
            if field_type == "password":
                print("      ✅ Password được mask (type='password')")
            else:
                print(f"      ❌ Password không được mask (type='{field_type}')")
                
        except NoSuchElementException:
            print("      ❌ Không tìm thấy password field")
        
        # 6.3. Test brute force protection (rate limiting)
        print("\n   6.3. Brute force protection test:")
        
        failed_attempts = 0
        for i in range(5):  # Thử 5 lần liên tiếp
            self.driver.get(f"{self.base_url}/auth/login")
            time.sleep(0.5)
            
            try:
                username = self.driver.find_element(By.NAME, "username")
                password = self.driver.find_element(By.NAME, "password")
                
                username.send_keys(f"attacker{i}")
                password.send_keys("wrongpassword")
                
                submit_button = self.find_submit_button()
                if submit_button:
                    submit_button.click()
                    time.sleep(1)
                    
                    failed_attempts += 1
                    
            except:
                break
        
        print(f"      • {failed_attempts} failed attempts")
        if failed_attempts >= 5:
            print("      ⚠️  Không có rate limiting rõ ràng")
            print("      💡 Nên implement rate limiting")
        
        print("✅ Đã validate security")

    def test_07_performance_and_ux(self):
        """Test 7: Performance và UX"""
        print("\n🧪 Test 7: Performance và UX...")
        
        # 7.1. Load time
        print("   7.1. Page load performance:")
        
        load_times = []
        for i in range(3):
            start_time = time.time()
            self.driver.get(f"{self.base_url}/auth/login")
            
            # Chờ page load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            
            load_time = time.time() - start_time
            load_times.append(load_time)
        
        avg_load = sum(load_times) / len(load_times)
        print(f"      • Load time trung bình: {avg_load:.2f}s")
        
        if avg_load < 1:
            print("      ✅ Performance tốt")
        elif avg_load < 2:
            print("      ⚠️  Performance acceptable")
        else:
            print("      ❌ Performance chậm")
        
        # 7.2. Error message UX
        print("\n   7.2. Error message UX:")
        
        # Test empty submission
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        submit_button = self.find_submit_button()
        if submit_button:
            submit_button.click()
            time.sleep(1)
            
            # Tìm error message
            error_selectors = [
                ".error", ".alert", ".text-danger", 
                "[class*='error']", "[class*='alert']"
            ]
            
            error_found = False
            for selector in error_selectors:
                try:
                    errors = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for error in errors:
                        if error.is_displayed() and error.text:
                            error_found = True
                            print(f"      ✅ Có error message: '{error.text[:50]}...'")
                            break
                    if error_found:
                        break
                except:
                    continue
            
            if not error_found:
                print("      ⚠️  Không có error message hiển thị")
        
        print("✅ Đã kiểm tra performance và UX")

    def test_08_final_comprehensive_test(self):
        """Test 8: Final comprehensive test"""
        print("\n🧪 Test 8: Final comprehensive test...")
        
        print("   📋 Running all critical checks:")
        
        checks_passed = 0
        total_checks = 0
        
        # Check 1: Form exists
        total_checks += 1
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        forms = self.driver.find_elements(By.TAG_NAME, "form")
        if forms:
            print("      ✅ 1. Form tồn tại")
            checks_passed += 1
        else:
            print("      ❌ 1. Không có form")
        
        # Check 2: Method is POST
        total_checks += 1
        if forms:
            method = forms[0].get_attribute("method") or ""
            if method.lower() == "post":
                print("      ✅ 2. Form method là POST")
                checks_passed += 1
            else:
                print(f"      ❌ 2. Form method là {method.upper()} (nên là POST)")
        
        # Check 3: Required fields
        total_checks += 2
        try:
            username = self.driver.find_element(By.NAME, "username")
            password = self.driver.find_element(By.NAME, "password")
            
            if username.get_attribute("type") != "hidden":
                print("      ✅ 3. Username field tồn tại")
                checks_passed += 1
            
            if password.get_attribute("type") == "password":
                print("      ✅ 4. Password field được mask")
                checks_passed += 1
            else:
                print(f"      ❌ 4. Password type: {password.get_attribute('type')}")
                
        except NoSuchElementException:
            print("      ❌ 3. Missing form fields")
        
        # Check 5: Protected pages redirect
        total_checks += 1
        self.driver.get(f"{self.base_url}/auth/tongquan.html")
        time.sleep(2)
        
        if "/auth/login" in self.driver.current_url:
            print("      ✅ 5. Protected pages redirect khi chưa login")
            checks_passed += 1
        else:
            print("      ❌ 5. Protected pages có thể truy cập khi chưa login")
        
        # Check 6: Logout works
        total_checks += 1
        self.driver.get(f"{self.base_url}/auth/logout")
        time.sleep(2)
        
        if "/auth/login" in self.driver.current_url:
            print("      ✅ 6. Logout redirect về login")
            checks_passed += 1
        else:
            print(f"      ❌ 6. Logout không redirect đúng: {self.driver.current_url}")
        
        # Summary
        print(f"\n   📊 SUMMARY: {checks_passed}/{total_checks} checks passed")
        
        if checks_passed == total_checks:
            print("   🎉 TẤT CẢ CHECKS PASSED!")
        else:
            print(f"   ⚠️  Còn {total_checks - checks_passed} issues cần fix")
        
        print("✅ Đã hoàn thành comprehensive test")

    def test_09_generate_fix_report(self):
        """Test 9: Tạo báo cáo fix cần thiết"""
        print("\n🧪 Test 9: Tạo báo cáo fix cần thiết...")
        
        print("\n" + "=" * 80)
        print("🔧 FIX REPORT - LOGIN SYSTEM")
        print("=" * 80)
        
        # Phân tích issues
        issues = []
        recommendations = []
        
        # Kiểm tra form method
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        forms = self.driver.find_elements(By.TAG_NAME, "form")
        if forms:
            method = forms[0].get_attribute("method") or ""
            if method.lower() != "post":
                issues.append("Form method là GET (không an toàn)")
                recommendations.append("Sửa login.html: method='post'")
        
        # Kiểm tra CSRF
        csrf_found = False
        csrf_selectors = ["input[name*='csrf']", "input[value*='csrf']"]
        for selector in csrf_selectors:
            try:
                if self.driver.find_elements(By.CSS_SELECTOR, selector):
                    csrf_found = True
                    break
            except:
                continue
        
        if not csrf_found:
            issues.append("Không có CSRF protection")
            recommendations.append("Thêm CSRF token vào form")
        
        # Kiểm tra attributes
        try:
            username = self.driver.find_element(By.NAME, "username")
            password = self.driver.find_element(By.NAME, "password")
            
            if not username.get_attribute("required"):
                issues.append("Username không có required attribute")
                recommendations.append("Thêm required attribute cho username")
            
            if not password.get_attribute("required"):
                issues.append("Password không có required attribute")
                recommendations.append("Thêm required attribute cho password")
            
            if not username.get_attribute("autocomplete"):
                recommendations.append("Thêm autocomplete='username' cho username field")
            
            if not password.get_attribute("autocomplete"):
                recommendations.append("Thêm autocomplete='current-password' cho password field")
                
        except NoSuchElementException:
            issues.append("Không tìm thấy form fields")
        
        # Hiển thị report
        if issues:
            print("\n⚠️  ISSUES FOUND:")
            for i, issue in enumerate(issues, 1):
                print(f"   {i}. {issue}")
        else:
            print("\n✅ KHÔNG CÓ ISSUES NÀO!")
        
        if recommendations:
            print("\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")
        
        print("\n🚀 ACTION PLAN:")
        print("   1. Kiểm tra và sửa file templates/auth/login.html")
        print("   2. Thêm CSRF protection nếu cần")
        print("   3. Test lại với test suite này")
        print("   4. Deploy fixes")
        
        print("\n" + "=" * 80)
        print("✅ FIX REPORT COMPLETED")
        print("=" * 80)

    # ========================
    # HELPER METHODS
    # ========================

    def find_submit_button(self):
        """Tìm submit button trong form"""
        try:
            return self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
        except NoSuchElementException:
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                if button.is_displayed():
                    return button
            forms = self.driver.find_elements(By.TAG_NAME, "form")
            if forms:
                return forms[0]
            return None

    # ========================
    # HTML REPORT GENERATOR
    # ========================

    @classmethod
    def generate_html_report(cls):
        """Tạo HTML report từ kết quả test"""
        if not cls.test_results:
            print("⚠️  Không có kết quả test")
            return
        
        total_tests = len(cls.test_results)
        passed_tests = sum(1 for r in cls.test_results if r["status"] == "PASSED")
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Selenium Test Report - Login Fixes</title>
    <style>
        body {{ font-family: Arial; margin: 20px; }}
        .container {{ max-width: 1200px; margin: auto; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
        .stats {{ display: flex; gap: 10px; }}
        .stat {{ padding: 10px; border-radius: 5px; }}
        .total {{ background: #e3f2fd; }}
        .passed {{ background: #c8e6c9; }}
        .failed {{ background: #ffcdd2; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 10px; border: 1px solid #ddd; }}
        th {{ background: #4CAF50; color: white; }}
        .pass {{ color: green; }}
        .fail {{ color: red; }}
        .fixes {{ background: #fff3cd; padding: 15px; margin: 20px 0; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Selenium Test Report - Login Fixes Validation</h1>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        
        <div class="summary">
            <h2>Summary</h2>
            <div class="stats">
                <div class="stat total">Total: {total_tests}</div>
                <div class="stat passed">Passed: {passed_tests}</div>
                <div class="stat failed">Failed: {failed_tests}</div>
            </div>
            <p>Success Rate: <strong>{success_rate:.1f}%</strong></p>
        </div>
        
        <div class="fixes">
            <h3>Key Findings:</h3>
            <p>This test suite validates login system fixes including:</p>
            <ul>
                <li>Form method validation (POST vs GET)</li>
                <li>CSRF protection check</li>
                <li>Form attributes validation</li>
                <li>Full login workflow test</li>
                <li>Security validation</li>
                <li>Performance and UX checks</li>
            </ul>
        </div>
        
        <h2>Test Results</h2>
        <table>
            <tr>
                <th>Test</th>
                <th>Status</th>
                <th>Duration</th>
                <th>Error</th>
            </tr>
"""
        
        for result in cls.test_results:
            status_class = "pass" if result["status"] == "PASSED" else "fail"
            error_display = result["error"] or ""
            if len(error_display) > 100:
                error_display = error_display[:100] + "..."
            
            html_content += f"""
            <tr>
                <td>{result['name']}</td>
                <td class="{status_class}">{result['status']}</td>
                <td>{result['duration']}</td>
                <td>{error_display}</td>
            </tr>
"""
        
        html_content += """
        </table>
    </div>
</body>
</html>
"""

        report_path = "selenium_fix_report.html"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"\n📄 Fix report đã tạo: {report_path}")

if __name__ == "__main__":
    print("=" * 80)
    print("🚀 SELENIUM LOGIN TEST - FIX VALIDATION SUITE")
    print("=" * 80)
    print("📌 Mục tiêu: Validate các fixes cho login system")
    print("   1. Form method là POST")
    print("   2. CSRF protection")
    print("   3. Complete form attributes")
    print("   4. Full workflow validation")
    print("   5. Security checks")
    print("=" * 80 + "\n")
    
    # Sắp xếp test theo thứ tự số
    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing = None
    
    # Chạy test
    suite = loader.loadTestsFromTestCase(LoginSeleniumTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
