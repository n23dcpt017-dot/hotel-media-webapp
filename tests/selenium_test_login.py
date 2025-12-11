"""
SELENIUM TEST - Login Functionality
Test giao diện và chức năng đăng nhập - FINAL VERSION
"""
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from datetime import datetime
import os
import sys

# Thêm path để import app Flask
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class LoginSeleniumTest(unittest.TestCase):
    """Test cases cho chức năng login sử dụng Selenium"""

    @classmethod
    def setUpClass(cls):
        """Setup trước khi chạy tất cả tests"""
        chrome_options = Options()
        # Bỏ comment dòng dưới nếu muốn chạy ẩn
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.implicitly_wait(3)
            
            # URL cho Flask app đang chạy
            cls.base_url = "http://localhost:5000"
            cls.test_results = []
            cls.screenshots_dir = "test_screenshots"
            
            if not os.path.exists(cls.screenshots_dir):
                os.makedirs(cls.screenshots_dir)

            print("\n" + "=" * 80)
            print("🚀 BẮT ĐẦU SELENIUM TEST - LOGIN FUNCTIONALITY")
            print(f"📡 Testing URL: {cls.base_url}")
            print("=" * 80 + "\n")

        except Exception as e:
            print(f"❌ Lỗi khi khởi tạo Chrome driver: {e}")
            print("💡 Cài ChromeDriver: https://chromedriver.chromium.org/")
            raise

    @classmethod
    def tearDownClass(cls):
        """Cleanup sau khi chạy xong tất cả tests"""
        if cls.driver:
            cls.driver.quit()

        cls.generate_html_report()

        print("\n" + "=" * 80)
        print("✅ HOÀN THÀNH SELENIUM TEST")
        print("📊 Report: selenium_test_report.html")
        print("📸 Screenshots: test_screenshots/")
        print("=" * 80 + "\n")

    def setUp(self):
        """Setup trước mỗi test case"""
        self.driver.delete_all_cookies()
        self.start_time = time.time()
        self.test_start_time = datetime.now().strftime("%H:%M:%S")

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
                print(f"   📸 Screenshot saved: {screenshot_path}")
            except:
                pass

        self.test_results.append(test_result)

    def take_screenshot(self, name):
        """Chụp screenshot với tên custom"""
        screenshot_name = f"{name}_{int(time.time())}.png"
        screenshot_path = os.path.join(self.screenshots_dir, screenshot_name)
        self.driver.save_screenshot(screenshot_path)
        return screenshot_name

    def wait_for_element(self, by, value, timeout=5):
        """Chờ element xuất hiện"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            return None

    def login_with_credentials(self, username, password):
        """Helper function để login"""
        print(f"   Đang login với: {username}/{'*' * len(password)}")
        
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        # Tìm các input field
        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        
        username_field.clear()
        username_field.send_keys(username)
        
        password_field.clear()
        password_field.send_keys(password)
        
        # Tìm submit button
        submit_button = None
        try:
            submit_button = self.driver.find_element(
                By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"
            )
        except NoSuchElementException:
            # Thử tìm button khác
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                if button.is_displayed():
                    submit_button = button
                    break
        
        if submit_button:
            submit_button.click()
            time.sleep(2)
        else:
            # Nếu không tìm thấy button, thử Enter
            password_field.submit()
            time.sleep(2)

    def is_login_page(self):
        """Kiểm tra có đang ở trang login không"""
        current_url = self.driver.current_url
        page_source = self.driver.page_source.lower()
        
        # Kiểm tra URL
        if "/auth/login" in current_url:
            return True
        
        # Kiểm tra nội dung trang
        if "login" in page_source or "username" in page_source or "password" in page_source:
            return True
        
        return False

    def is_dashboard_page(self):
        """Kiểm tra có đang ở dashboard/tongquan không"""
        current_url = self.driver.current_url
        page_source = self.driver.page_source.lower()
        
        # Kiểm tra URL
        url_indicators = [
            "/auth/dashboard",
            "/dashboard",
            "/tongquan",
            "/auth/tongquan",
            "/tongquan.html"
        ]
        
        for indicator in url_indicators:
            if indicator in current_url:
                return True
        
        # Kiểm tra nội dung trang
        content_indicators = [
            "dashboard",
            "tongquan",
            "tổng quan",
            "welcome",
            "chào mừng"
        ]
        
        for indicator in content_indicators:
            if indicator in page_source:
                return True
        
        return False

    # ========================
    # TEST CASES
    # ========================

    def test_01_login_page_loads(self):
        """Test 1: Trang login load thành công"""
        print(f"\n🧪 Test 1: Kiểm tra trang login load...")

        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(2)

        # Kiểm tra không phải 404
        page_source = self.driver.page_source.lower()
        if "not found" in page_source:
            self.take_screenshot("404_not_found")
            self.fail("Trang login không tồn tại (404 Not Found)")

        # Kiểm tra form login
        try:
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            
            self.assertTrue(username_field.is_displayed())
            self.assertTrue(password_field.is_displayed())
            
            print("   ✓ Username field: OK")
            print("   ✓ Password field: OK")
            
        except NoSuchElementException:
            self.take_screenshot("login_form_missing")
            self.fail("Không tìm thấy form login")

        self.take_screenshot("login_page")
        print("✅ Trang login load thành công!")

    def test_02_login_form_elements_exist(self):
        """Test 2: Các elements của form login tồn tại"""
        print(f"\n🧪 Test 2: Kiểm tra các elements của form...")

        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(2)

        # Kiểm tra các elements
        elements_to_check = [
            ("username", "Username field"),
            ("password", "Password field"),
        ]
        
        for element_name, description in elements_to_check:
            try:
                element = self.driver.find_element(By.NAME, element_name)
                self.assertTrue(element.is_displayed())
                print(f"   ✓ {description}: OK")
            except NoSuchElementException:
                self.fail(f"Không tìm thấy {description}")

        # Kiểm tra submit button
        try:
            submit_selectors = [
                "button[type='submit']",
                "input[type='submit']",
                "button"
            ]
            
            submit_found = False
            for selector in submit_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for button in buttons:
                        if button.is_displayed():
                            submit_found = True
                            break
                    if submit_found:
                        break
                except:
                    continue
            
            if submit_found:
                print("   ✓ Submit button: OK")
            else:
                self.fail("Không tìm thấy submit button")
                
        except Exception as e:
            self.fail(f"Lỗi khi tìm submit button: {str(e)}")

        self.take_screenshot("login_form")
        print("✅ Tất cả elements đều tồn tại!")

    def test_03_login_with_empty_fields(self):
        """Test 3: Login với fields trống"""
        print(f"\n🧪 Test 3: Kiểm tra login với fields trống...")

        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(2)

        # Tìm submit button
        submit_button = None
        try:
            submit_button = self.driver.find_element(
                By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"
            )
        except NoSuchElementException:
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            submit_button = buttons[0] if buttons else None
        
        if not submit_button:
            self.fail("Không tìm thấy submit button")
        
        # Submit form trống
        submit_button.click()
        time.sleep(2)

        # Nên vẫn ở trang login
        self.assertTrue(self.is_login_page(), "Không ở trang login sau khi submit form trống")

        self.take_screenshot("empty_fields")
        print("✅ Không cho phép login với fields trống!")

    def test_04_login_with_wrong_credentials(self):
        """Test 4: Login với thông tin sai"""
        print(f"\n🧪 Test 4: Kiểm tra login với thông tin sai...")

        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(2)

        # Nhập thông tin sai
        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")

        username_field.send_keys("wrong_user")
        password_field.send_keys("wrong_password")

        # Submit
        submit_button = self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"
        )
        submit_button.click()
        time.sleep(2)

        # Nên vẫn ở trang login
        self.assertTrue(self.is_login_page(), "Không ở trang login sau khi nhập thông tin sai")

        self.take_screenshot("wrong_credentials")
        print("✅ Không cho phép login với thông tin sai!")

    def test_05_login_with_correct_credentials(self):
        """Test 5: Login với thông tin đúng"""
        print(f"\n🧪 Test 5: Kiểm tra login với thông tin đúng...")

        # Login với admin
        self.login_with_credentials("admin", "Admin@123")
        
        # Kiểm tra đã login thành công (không còn ở trang login)
        self.assertFalse(self.is_login_page(), "Vẫn ở trang login sau khi nhập thông tin đúng")
        
        # Kiểm tra đã chuyển đến dashboard/tongquan
        self.assertTrue(self.is_dashboard_page(), "Không chuyển đến dashboard sau login")

        self.take_screenshot("login_success")
        print("✅ Login thành công! Chuyển đến dashboard")

    def test_06_remember_me_checkbox(self):
        """Test 6: Checkbox Remember Me (optional)"""
        print(f"\n🧪 Test 6: Kiểm tra Remember Me checkbox...")

        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(2)

        # Tìm checkbox (nếu có)
        checkbox_found = False
        checkbox_selectors = [
            "input[name='remember']",
            "input[name='remember_me']",
            "input[type='checkbox']"
        ]
        
        for selector in checkbox_selectors:
            try:
                checkboxes = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for checkbox in checkboxes:
                    if checkbox.is_displayed():
                        # Kiểm tra checkbox
                        initial_state = checkbox.is_selected()
                        checkbox.click()
                        time.sleep(0.5)
                        new_state = checkbox.is_selected()
                        
                        self.assertNotEqual(initial_state, new_state, "Checkbox không thay đổi trạng thái")
                        checkbox_found = True
                        print("   ✓ Remember Me checkbox: OK")
                        break
                if checkbox_found:
                    break
            except:
                continue
        
        if not checkbox_found:
            print("   ⚠️ Remember Me checkbox không tồn tại (optional)")

        self.take_screenshot("remember_me")
        print("✅ Đã kiểm tra Remember Me!")

    def test_07_password_field_masked(self):
        """Test 7: Password field được mask"""
        print(f"\n🧪 Test 7: Kiểm tra password field được mask...")

        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(2)

        password_field = self.driver.find_element(By.NAME, "password")
        field_type = password_field.get_attribute("type")
        
        self.assertEqual(field_type, "password", f"Password field type là '{field_type}', expected 'password'")

        self.take_screenshot("password_masked")
        print("✅ Password field được mask đúng!")

    def test_08_navigation_after_login(self):
        """Test 8: Navigation sau khi login"""
        print(f"\n🧪 Test 8: Kiểm tra navigation sau login...")

        # Login trước
        self.login_with_credentials("admin", "Admin@123")
        time.sleep(2)
        
        # Kiểm tra đã login
        if self.is_login_page():
            self.skipTest("Login thất bại, không thể test navigation")
        
        # Lấy URL hiện tại
        current_url = self.driver.current_url
        print(f"   URL hiện tại: {current_url}")
        
        # Refresh trang
        self.driver.refresh()
        time.sleep(2)
        
        # Vẫn phải ở dashboard, không về login
        self.assertFalse(self.is_login_page(), "Bị logout sau khi refresh")
        self.assertTrue(self.is_dashboard_page(), "Không ở dashboard sau refresh")

        self.take_screenshot("navigation")
        print("✅ Có thể refresh trang sau khi login!")

    def test_09_logout_functionality(self):
        """Test 9: Chức năng logout"""
        print(f"\n🧪 Test 9: Kiểm tra chức năng logout...")

        # Login trước
        self.login_with_credentials("admin", "Admin@123")
        time.sleep(2)
        
        if self.is_login_page():
            self.skipTest("Login thất bại, không thể test logout")
        
        # Truy cập logout
        self.driver.get(f"{self.base_url}/auth/logout")
        time.sleep(2)
        
        # Sau logout nên về trang login
        self.assertTrue(self.is_login_page(), "Không về trang login sau logout")

        self.take_screenshot("logout")
        print("✅ Logout thành công!")

    def test_10_access_protected_page_without_login(self):
        """Test 10: Truy cập trang bảo vệ khi chưa login"""
        print(f"\n🧪 Test 10: Kiểm tra truy cập trang bảo vệ khi chưa login...")
        
        # Đảm bảo logout
        self.driver.delete_all_cookies()
        
        # Thử truy cập dashboard
        self.driver.get(f"{self.base_url}/auth/dashboard")
        time.sleep(2)
        
        # Nên bị redirect về login
        self.assertTrue(self.is_login_page(), "Không bị redirect về login khi truy cập dashboard chưa đăng nhập")

        self.take_screenshot("protected_page")
        print("✅ Không thể truy cập trang bảo vệ khi chưa login!")

    def test_11_check_app_routes(self):
        """Test 11: Kiểm tra các routes của app"""
        print(f"\n🧪 Test 11: Kiểm tra các routes của app...")
        
        routes = [
            ("/auth/login", "Login page", True),
            ("/auth/logout", "Logout", False),  # Cần login
            ("/auth/dashboard", "Dashboard", False),  # Cần login
            ("/auth/tongquan", "Tongquan", False),  # Cần login
            ("/auth/index", "Index", False),  # Cần login
        ]
        
        print("   Kiểm tra routes:")
        for route, description, should_be_accessible in routes:
            self.driver.get(f"{self.base_url}{route}")
            time.sleep(1)
            
            current_url = self.driver.current_url
            status = "✅" if "/auth/login" not in current_url else "❌"
            
            if should_be_accessible:
                if "/auth/login" not in current_url:
                    print(f"   {status} {route} - {description}: Truy cập được")
                else:
                    print(f"   {status} {route} - {description}: Bị redirect về login (không đúng)")
            else:
                if "/auth/login" in current_url:
                    print(f"   {status} {route} - {description}: Bị redirect về login (đúng)")
                else:
                    print(f"   {status} {route} - {description}: Truy cập được (có thể đã login)")
        
        self.take_screenshot("routes_check")
        print("✅ Đã kiểm tra các routes!")

    def test_12_form_validation_workflow(self):
        """Test 12: Kiểm tra workflow validation của form"""
        print(f"\n🧪 Test 12: Kiểm tra workflow validation của form...")

        # Test 1: Form trống
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        submit_button = self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"
        )
        submit_button.click()
        time.sleep(1)
        
        # Vẫn ở trang login
        self.assertTrue(self.is_login_page(), "Không ở trang login sau submit form trống")
        
        # Test 2: Chỉ username
        username_field = self.driver.find_element(By.NAME, "username")
        username_field.send_keys("test")
        submit_button.click()
        time.sleep(1)
        
        self.assertTrue(self.is_login_page(), "Không ở trang login sau chỉ nhập username")
        
        # Test 3: Chỉ password
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys("test")
        submit_button = self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"
        )
        submit_button.click()
        time.sleep(1)
        
        self.assertTrue(self.is_login_page(), "Không ở trang login sau chỉ nhập password")
        
        # Test 4: Thông tin đúng
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        
        username_field.send_keys("admin")
        password_field.send_keys("Admin@123")
        
        submit_button = self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"
        )
        submit_button.click()
        time.sleep(2)
        
        # Nên chuyển đến dashboard
        self.assertFalse(self.is_login_page(), "Vẫn ở trang login sau nhập thông tin đúng")
        self.assertTrue(self.is_dashboard_page(), "Không chuyển đến dashboard")

        self.take_screenshot("form_workflow")
        print("✅ Workflow form validation hoạt động đúng!")

    # ========================
    # HTML REPORT GENERATOR
    # ========================

    @classmethod
    def generate_html_report(cls):
        """Tạo HTML report từ kết quả test"""
        if not cls.test_results:
            print("⚠️  Không có kết quả test để tạo report")
            return
        
        total_tests = len(cls.test_results)
        passed_tests = sum(1 for r in cls.test_results if r["status"] == "PASSED")
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Màu sắc cho report
        if success_rate >= 90:
            overall_color = "#28a745"
        elif success_rate >= 70:
            overall_color = "#17a2b8"
        elif success_rate >= 50:
            overall_color = "#ffc107"
        else:
            overall_color = "#dc3545"

        # Tạo HTML
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Selenium Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid {overall_color}; padding-bottom: 10px; }}
        .summary {{ background: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 30px; }}
        .stats {{ display: flex; justify-content: space-between; margin-top: 20px; }}
        .stat-box {{ text-align: center; padding: 15px; border-radius: 5px; width: 23%; }}
        .total {{ background: #d1ecf1; color: #0c5460; }}
        .passed {{ background: #d4edda; color: #155724; }}
        .failed {{ background: #f8d7da; color: #721c24; }}
        .rate {{ background: #fff3e0; color: #856404; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #2c3e50; color: white; }}
        .status-passed {{ color: #155724; background-color: #d4edda; padding: 3px 8px; border-radius: 3px; }}
        .status-failed {{ color: #721c24; background-color: #f8d7da; padding: 3px 8px; border-radius: 3px; }}
        .screenshot {{ max-width: 150px; cursor: pointer; border: 1px solid #ddd; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Selenium Test Report - Login</h1>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | URL: {cls.base_url}</p>
        
        <div class="summary">
            <h2>Summary</h2>
            <div class="stats">
                <div class="stat-box total">
                    <h3>Total Tests</h3>
                    <p>{total_tests}</p>
                </div>
                <div class="stat-box passed">
                    <h3>Passed</h3>
                    <p>{passed_tests}</p>
                </div>
                <div class="stat-box failed">
                    <h3>Failed</h3>
                    <p>{failed_tests}</p>
                </div>
                <div class="stat-box rate">
                    <h3>Success Rate</h3>
                    <p>{success_rate:.1f}%</p>
                </div>
            </div>
        </div>
        
        <h2>Test Details</h2>
        <table>
            <tr>
                <th>Test</th>
                <th>Status</th>
                <th>Duration</th>
                <th>Timestamp</th>
                <th>Screenshot</th>
            </tr>
"""
        
        for result in cls.test_results:
            status_class = "status-passed" if result["status"] == "PASSED" else "status-failed"
            screenshot_html = ""
            
            if result["screenshot"]:
                screenshot_path = os.path.join(cls.screenshots_dir, result["screenshot"])
                screenshot_html = f'<img src="{screenshot_path}" class="screenshot" style="max-width: 100px;">'
            
            html_content += f"""
            <tr>
                <td>{result['name']}</td>
                <td><span class="{status_class}">{result['status']}</span></td>
                <td>{result['duration']}</td>
                <td>{result['timestamp']}</td>
                <td>{screenshot_html}</td>
            </tr>
"""
        
        html_content += """
        </table>
    </div>
</body>
</html>
"""

        with open("selenium_test_report.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"📄 Report: selenium_test_report.html")

if __name__ == "__main__":
    print("🚀 Starting Selenium Login Tests...")
    print("=" * 80)
    print("📌 Lưu ý:")
    print("1. Đảm bảo Flask app đang chạy: python app.py")
    print("2. User 'admin' với password 'Admin@123' phải tồn tại")
    print("3. Dashboard và tongquan là cùng một trang")
    print("=" * 80 + "\n")
    
    unittest.main(verbosity=2)
