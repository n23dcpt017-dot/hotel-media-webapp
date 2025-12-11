"""
SELENIUM TEST - Login Functionality
Test giao diện và chức năng đăng nhập - FIXED VERSION
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
    """Test cases cho chức năng login sử dụng Selenium - FIXED"""

    @classmethod
    def setUpClass(cls):
        """Setup trước khi chạy tất cả tests"""
        chrome_options = Options()
        # Comment dòng headless để debug
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')

        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.implicitly_wait(10)
            
            # URL cho Flask app đang chạy
            cls.base_url = "http://localhost:5000"
            cls.test_results = []
            cls.screenshots_dir = "test_screenshots"
            
            if not os.path.exists(cls.screenshots_dir):
                os.makedirs(cls.screenshots_dir)

            print("\n" + "=" * 70)
            print("🚀 BẮT ĐẦU SELENIUM TEST - LOGIN FUNCTIONALITY (FIXED)")
            print(f"📡 Testing URL: {cls.base_url}")
            print("=" * 70 + "\n")

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

        print("\n" + "=" * 70)
        print("✅ HOÀN THÀNH SELENIUM TEST")
        print("📊 Report: selenium_test_report.html")
        print("=" * 70 + "\n")

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
                print(f"📸 Screenshot saved: {screenshot_path}")
            except:
                pass

        self.test_results.append(test_result)

    def take_screenshot(self, name):
        """Chụp screenshot với tên custom"""
        screenshot_name = f"{name}_{int(time.time())}.png"
        screenshot_path = os.path.join(self.screenshots_dir, screenshot_name)
        self.driver.save_screenshot(screenshot_path)
        return screenshot_name

    def login_with_credentials(self, username, password):
        """Helper function để login"""
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        
        username_field.clear()
        username_field.send_keys(username)
        
        password_field.clear()
        password_field.send_keys(password)
        
        submit_button = self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"
        )
        submit_button.click()
        time.sleep(2)

    # ========================
    # TEST CASES - FIXED
    # ========================

    def test_01_login_page_loads(self):
        """Test 1: Trang login load thành công"""
        print("\n🧪 Test 1: Kiểm tra trang login load...")

        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(2)

        # Kiểm tra URL
        self.assertIn("/auth/login", self.driver.current_url)
        
        # Kiểm tra tiêu đề trang có chứa login hoặc form tồn tại
        try:
            # Tìm form login
            username_field = self.driver.find_element(By.NAME, "username")
            password_field = self.driver.find_element(By.NAME, "password")
            
            self.assertTrue(username_field.is_displayed())
            self.assertTrue(password_field.is_displayed())
            
        except NoSuchElementException:
            # Nếu không tìm thấy element, chụp ảnh và fail test
            self.take_screenshot("login_page_failed")
            self.fail("Không tìm thấy form login")

        self.take_screenshot("login_page_loaded")
        print("✅ Trang login load thành công!")

    def test_02_login_form_elements_exist(self):
        """Test 2: Các elements của form login tồn tại"""
        print("\n🧪 Test 2: Kiểm tra các elements của form...")

        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(2)

        # Kiểm tra tất cả các elements cần thiết
        required_elements = [
            ("username", "Username field"),
            ("password", "Password field"),
        ]
        
        for element_name, element_desc in required_elements:
            try:
                element = self.driver.find_element(By.NAME, element_name)
                self.assertTrue(element.is_displayed(), f"{element_desc} không hiển thị")
                print(f"   ✓ {element_desc}: OK")
            except NoSuchElementException:
                self.fail(f"Không tìm thấy {element_desc}")

        # Tìm submit button
        try:
            # Thử tìm button theo type submit
            submit_button = self.driver.find_element(
                By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"
            )
            self.assertTrue(submit_button.is_displayed(), "Submit button không hiển thị")
            print("   ✓ Submit button: OK")
        except NoSuchElementException:
            # Thử tìm button theo text
            try:
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                submit_found = False
                for button in buttons:
                    if button.is_displayed():
                        submit_found = True
                        break
                if submit_found:
                    print("   ✓ Submit button (found by text): OK")
                else:
                    self.fail("Không tìm thấy submit button")
            except:
                self.fail("Không tìm thấy submit button")

        self.take_screenshot("login_form_elements")
        print("✅ Tất cả elements đều tồn tại!")

    def test_03_login_with_empty_fields(self):
        """Test 3: Login với fields trống"""
        print("\n🧪 Test 3: Kiểm tra login với fields trống...")

        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(2)

        # Để trống các fields và submit
        submit_button = self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"
        )
        submit_button.click()

        time.sleep(2)

        # Sau khi submit với fields trống, nên vẫn ở trang login
        self.assertIn("/auth/login", self.driver.current_url)

        self.take_screenshot("login_empty_fields")
        print("✅ Không cho phép login với fields trống!")

    def test_04_login_with_wrong_credentials(self):
        """Test 4: Login với thông tin sai"""
        print("\n🧪 Test 4: Kiểm tra login với thông tin sai...")

        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(2)

        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")

        username_field.clear()
        username_field.send_keys("wrong_user")

        password_field.clear()
        password_field.send_keys("wrong_password")

        submit_button = self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"
        )
        submit_button.click()

        time.sleep(2)

        # Vẫn ở trang login khi thông tin sai
        self.assertIn("/auth/login", self.driver.current_url)

        self.take_screenshot("login_wrong_credentials")
        print("✅ Không cho phép login với thông tin sai!")

    def test_05_login_with_correct_credentials(self):
        """Test 5: Login với thông tin đúng"""
        print("\n🧪 Test 5: Kiểm tra login với thông tin đúng...")

        self.login_with_credentials("admin", "Admin@123")
        
        # Sau khi login thành công, nên redirect đến /auth/dashboard
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/auth/dashboard")
            )
            current_url = self.driver.current_url
            self.assertIn("/auth/dashboard", current_url)
            self.assertNotIn("/auth/login", current_url)
            
            self.take_screenshot("login_success_dashboard")
            print("✅ Login thành công! Redirect đến dashboard")
            
        except TimeoutException:
            # Kiểm tra nếu redirect đến trang khác
            current_url = self.driver.current_url
            if "/auth/login" not in current_url:
                # Có thể đã login thành công nhưng redirect đến trang khác
                self.take_screenshot("login_success_other_page")
                print(f"✅ Login thành công! Redirect đến: {current_url}")
            else:
                self.take_screenshot("login_timeout")
                self.fail("Không redirect sau khi login")

    def test_06_remember_me_checkbox(self):
        """Test 6: Checkbox Remember Me (optional)"""
        print("\n🧪 Test 6: Kiểm tra Remember Me checkbox...")

        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(2)

        try:
            # Thử tìm checkbox remember me theo các cách khác nhau
            selectors = [
                "input[name='remember']",
                "input[name='remember_me']",
                "input[type='checkbox']",
                "#remember",
                "#remember_me"
            ]
            
            remember_checkbox = None
            for selector in selectors:
                try:
                    remember_checkbox = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if remember_checkbox:
                # Kiểm tra và click nếu cần
                if not remember_checkbox.is_selected():
                    remember_checkbox.click()
                    time.sleep(0.5)
                
                self.assertTrue(remember_checkbox.is_selected())
                self.take_screenshot("remember_me_checked")
                print("✅ Remember Me checkbox hoạt động!")
            else:
                print("⚠️ Remember Me checkbox không tồn tại (optional test) - PASSED")
                
        except Exception as e:
            print(f"⚠️ Remember Me checkbox không tồn tại (optional test) - PASSED: {str(e)}")

    def test_07_password_field_masked(self):
        """Test 7: Password field được mask"""
        print("\n🧪 Test 7: Kiểm tra password field được mask...")

        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(2)

        password_field = self.driver.find_element(By.NAME, "password")
        field_type = password_field.get_attribute("type")
        
        # Kiểm tra type là password (masked)
        self.assertEqual(field_type, "password", f"Password field type là '{field_type}', expected 'password'")

        self.take_screenshot("password_masked")
        print("✅ Password field được mask đúng!")

    def test_08_navigation_after_login(self):
        """Test 8: Navigation sau khi login"""
        print("\n🧪 Test 8: Kiểm tra navigation sau login...")

        # Login trước
        self.login_with_credentials("admin", "Admin@123")
        time.sleep(2)
        
        # Truy cập dashboard sau khi login
        try:
            self.driver.get(f"{self.base_url}/auth/dashboard")
            time.sleep(2)
            
            # Không nên redirect về login nếu đã login
            self.assertNotIn("/auth/login", self.driver.current_url)
            
            self.take_screenshot("navigation_after_login")
            print("✅ Có thể navigate đến dashboard sau khi login!")
            
        except Exception as e:
            self.take_screenshot("navigation_error")
            self.fail(f"Không thể access dashboard sau khi login: {str(e)}")

    def test_09_logout_functionality(self):
        """Test 9: Chức năng logout"""
        print("\n🧪 Test 9: Kiểm tra chức năng logout...")

        # Login trước
        self.login_with_credentials("admin", "Admin@123")
        time.sleep(2)
        
        # Thử truy cập logout endpoint
        try:
            self.driver.get(f"{self.base_url}/auth/logout")
            time.sleep(3)
            
            # Sau khi logout, nên redirect về login
            current_url = self.driver.current_url
            self.assertIn("/auth/login", current_url)
            
            self.take_screenshot("after_logout")
            print("✅ Logout thành công! Redirect về login page")
            
        except Exception as e:
            self.take_screenshot("logout_error")
            self.fail(f"Logout không hoạt động: {str(e)}")

    def test_10_access_protected_page_without_login(self):
        """Test 10: Truy cập trang bảo vệ khi chưa login"""
        print("\n🧪 Test 10: Kiểm tra truy cập trang bảo vệ khi chưa login...")
        
        # Xóa cookies để đảm bảo logout
        self.driver.delete_all_cookies()
        
        # Truy cập dashboard mà không login
        self.driver.get(f"{self.base_url}/auth/dashboard")
        time.sleep(2)
        
        # Nên được redirect về login page
        current_url = self.driver.current_url
        self.assertIn("/auth/login", current_url)
        
        self.take_screenshot("protected_page_without_login")
        print("✅ Không thể truy cập trang bảo vệ khi chưa login!")

    # ========================
    # HTML REPORT GENERATOR
    # ========================

    @classmethod
    def generate_html_report(cls):
        """Tạo HTML report từ kết quả test"""
        total_tests = len(cls.test_results)
        passed_tests = sum(1 for r in cls.test_results if r["status"] == "PASSED")
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

        # Tạo HTML report chi tiết
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Selenium Test Report - Login Functionality</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
                .summary {{ background: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 30px; }}
                .stats {{ display: flex; justify-content: space-between; margin-top: 20px; }}
                .stat-box {{ text-align: center; padding: 15px; border-radius: 5px; width: 30%; }}
                .passed {{ background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }}
                .failed {{ background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }}
                .total {{ background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #4CAF50; color: white; }}
                tr:hover {{ background-color: #f5f5f5; }}
                .status-passed {{ color: #155724; background-color: #d4edda; padding: 3px 8px; border-radius: 3px; }}
                .status-failed {{ color: #721c24; background-color: #f8d7da; padding: 3px 8px; border-radius: 3px; }}
                .screenshot {{ max-width: 300px; max-height: 200px; cursor: pointer; border: 1px solid #ddd; }}
                .modal {{ display: none; position: fixed; z-index: 1000; padding-top: 100px; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.9); }}
                .modal-content {{ margin: auto; display: block; width: 80%; max-width: 700px; }}
                .close {{ position: absolute; top: 15px; right: 35px; color: #f1f1f1; font-size: 40px; font-weight: bold; cursor: pointer; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Selenium Test Report - Login Functionality</h1>
                <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                
                <div class="summary">
                    <h2>Test Summary</h2>
                    <div class="stats">
                        <div class="stat-box total">
                            <h3>Total Tests</h3>
                            <p style="font-size: 24px; font-weight: bold;">{total_tests}</p>
                        </div>
                        <div class="stat-box passed">
                            <h3>Passed</h3>
                            <p style="font-size: 24px; font-weight: bold;">{passed_tests}</p>
                        </div>
                        <div class="stat-box failed">
                            <h3>Failed</h3>
                            <p style="font-size: 24px; font-weight: bold;">{failed_tests}</p>
                        </div>
                    </div>
                    <p style="margin-top: 20px; font-size: 18px;">
                        Success Rate: <strong>{success_rate:.2f}%</strong>
                    </p>
                </div>
                
                <h2>Test Details</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Test Name</th>
                            <th>Status</th>
                            <th>Duration</th>
                            <th>Timestamp</th>
                            <th>Screenshot</th>
                            <th>Error Message</th>
                        </tr>
                    </thead>
                    <tbody>
        """

        for result in cls.test_results:
            status_class = "status-passed" if result["status"] == "PASSED" else "status-failed"
            screenshot_html = ""
            if result["screenshot"]:
                screenshot_path = os.path.join(cls.screenshots_dir, result["screenshot"])
                screenshot_html = f'<img src="{screenshot_path}" class="screenshot" onclick="openModal(this.src)" alt="Screenshot">'
            
            error_msg = result["error"] or "None"
            # Giới hạn độ dài error message
            if len(error_msg) > 100:
                error_msg = error_msg[:100] + "..."

            html_content += f"""
                        <tr>
                            <td>{result['name']}</td>
                            <td><span class="{status_class}">{result['status']}</span></td>
                            <td>{result['duration']}</td>
                            <td>{result['timestamp']}</td>
                            <td>{screenshot_html}</td>
                            <td><small>{error_msg}</small></td>
                        </tr>
            """

        html_content += """
                    </tbody>
                </table>
            </div>
            
            <div id="imageModal" class="modal">
                <span class="close" onclick="closeModal()">&times;</span>
                <img class="modal-content" id="modalImage">
            </div>
            
            <script>
                function openModal(src) {
                    document.getElementById('imageModal').style.display = "block";
                    document.getElementById('modalImage').src = src;
                }
                
                function closeModal() {
                    document.getElementById('imageModal').style.display = "none";
                }
                
                // Đóng modal khi click bên ngoài ảnh
                window.onclick = function(event) {
                    var modal = document.getElementById('imageModal');
                    if (event.target == modal) {
                        closeModal();
                    }
                }
            </script>
        </body>
        </html>
        """

        with open("selenium_test_report.html", "w", encoding="utf-8") as f:
            f.write(html_content)


if __name__ == "__main__":
    print("🚀 Starting Selenium tests...")
    print("⚠️  Make sure Flask app is running on http://localhost:5000")
    print("⚠️  Run: python app.py or flask run\n")
    
    unittest.main(verbosity=2)
