"""
SELENIUM TEST - Login Functionality
Test giao diện và chức năng đăng nhập
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

URL="https://n23dcpt017-dot.github.io/hotel-media-webapp/templates/login.html"

class LoginSeleniumTest(unittest.TestCase):
    """Test cases cho chức năng login sử dụng Selenium"""
    
    @classmethod
    def setUpClass(cls):
        """Setup trước khi chạy tất cả tests"""
        # Cấu hình Chrome options
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # Bỏ comment nếu muốn chạy background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.implicitly_wait(10)
            cls.base_url = "http://localhost:5000"  # Đổi thành URL của bạn
            cls.test_results = []
            cls.screenshots_dir = "test_screenshots"
            
            # Tạo folder screenshots nếu chưa có
            if not os.path.exists(cls.screenshots_dir):
                os.makedirs(cls.screenshots_dir)
                
            print("\n" + "="*70)
            print("🚀 BẮT ĐẦU SELENIUM TEST - LOGIN FUNCTIONALITY")
            print("="*70 + "\n")
            
        except Exception as e:
            print(f"❌ Lỗi khi khởi tạo Chrome driver: {e}")
            print("💡 Hướng dẫn: Cài ChromeDriver từ https://chromedriver.chromium.org/")
            raise
    
    @classmethod
    def tearDownClass(cls):
        """Cleanup sau khi chạy xong tất cả tests"""
        if cls.driver:
            cls.driver.quit()
        
        # Tạo HTML report
        cls.generate_html_report()
        
        print("\n" + "="*70)
        print("✅ HOÀN THÀNH SELENIUM TEST")
        print("📊 Kết quả đã được lưu vào: selenium_test_report.html")
        print("="*70 + "\n")
    
    def setUp(self):
        """Setup trước mỗi test case"""
        self.start_time = time.time()
    
    def tearDown(self):
        """Cleanup sau mỗi test case"""
        duration = time.time() - self.start_time
        
        # Lưu kết quả test
        test_name = self._testMethodName
        test_result = {
            'name': test_name,
            'status': 'PASSED' if self._outcome.success else 'FAILED',
            'duration': f"{duration:.2f}s",
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'error': str(self._outcome.errors[0][1]) if self._outcome.errors else None,
            'screenshot': None
        }
        
        # Chụp screenshot nếu test fail
        if not self._outcome.success:
            screenshot_name = f"{test_name}_{int(time.time())}.png"
            screenshot_path = os.path.join(self.screenshots_dir, screenshot_name)
            self.driver.save_screenshot(screenshot_path)
            test_result['screenshot'] = screenshot_name
            print(f"📸 Screenshot saved: {screenshot_path}")
        
        self.test_results.append(test_result)
    
    def take_screenshot(self, name):
        """Chụp screenshot với tên custom"""
        screenshot_name = f"{name}_{int(time.time())}.png"
        screenshot_path = os.path.join(self.screenshots_dir, screenshot_name)
        self.driver.save_screenshot(screenshot_path)
        return screenshot_name
    
    # ========================
    # TEST CASES
    # ========================
    
    def test_01_login_page_loads(self):
        """Test 1: Trang login load thành công"""
        print("\n🧪 Test 1: Kiểm tra trang login load...")
        
        self.driver.get(f"{self.base_url}/auth/login")
        
        # Kiểm tra title
        self.assertIn("Login", self.driver.title, "Title không chứa 'Login'")
        
        # Kiểm tra URL
        self.assertIn("/auth/login", self.driver.current_url)
        
        # Chụp screenshot
        self.take_screenshot("login_page_loaded")
        
        print("✅ Trang login load thành công!")
    
    def test_02_login_form_elements_exist(self):
        """Test 2: Các elements của form login tồn tại"""
        print("\n🧪 Test 2: Kiểm tra các elements của form...")
        
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        # Kiểm tra username field
        try:
            username_field = self.driver.find_element(By.NAME, "username")
            self.assertTrue(username_field.is_displayed(), "Username field không hiển thị")
            print("   ✓ Username field: OK")
        except NoSuchElementException:
            self.fail("Không tìm thấy username field")
        
        # Kiểm tra password field
        try:
            password_field = self.driver.find_element(By.NAME, "password")
            self.assertTrue(password_field.is_displayed(), "Password field không hiển thị")
            print("   ✓ Password field: OK")
        except NoSuchElementException:
            self.fail("Không tìm thấy password field")
        
        # Kiểm tra submit button
        try:
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
            self.assertTrue(submit_button.is_displayed(), "Submit button không hiển thị")
            print("   ✓ Submit button: OK")
        except NoSuchElementException:
            self.fail("Không tìm thấy submit button")
        
        self.take_screenshot("login_form_elements")
        print("✅ Tất cả elements đều tồn tại!")
    
    def test_03_login_with_empty_fields(self):
        """Test 3: Login với fields trống"""
        print("\n🧪 Test 3: Kiểm tra login với fields trống...")
        
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        # Click submit mà không nhập gì
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
        submit_button.click()
        
        time.sleep(1)
        
        # Kiểm tra vẫn ở trang login
        self.assertIn("/auth/login", self.driver.current_url)
        
        self.take_screenshot("login_empty_fields")
        print("✅ Không cho phép login với fields trống!")
    
    def test_04_login_with_wrong_credentials(self):
        """Test 4: Login với thông tin sai"""
        print("\n🧪 Test 4: Kiểm tra login với thông tin sai...")
        
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        # Nhập thông tin sai
        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        
        username_field.clear()
        username_field.send_keys("wrong_user")
        
        password_field.clear()
        password_field.send_keys("wrong_password")
        
        # Click submit
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
        submit_button.click()
        
        time.sleep(2)
        
        # Kiểm tra có thông báo lỗi hoặc vẫn ở trang login
        self.assertIn("/auth/login", self.driver.current_url)
        
        self.take_screenshot("login_wrong_credentials")
        print("✅ Không cho phép login với thông tin sai!")
    
    def test_05_login_with_correct_credentials(self):
        """Test 5: Login với thông tin đúng"""
        print("\n🧪 Test 5: Kiểm tra login với thông tin đúng...")
        
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        # Nhập thông tin đúng
        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        
        username_field.clear()
        username_field.send_keys("admin")
        
        password_field.clear()
        password_field.send_keys("Admin@123")
        
        self.take_screenshot("login_before_submit")
        
        # Click submit
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
        submit_button.click()
        
        time.sleep(3)
        
        # Kiểm tra redirect đến dashboard
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: "/dashboard" in driver.current_url or "/index" in driver.current_url
            )
            self.assertNotIn("/auth/login", self.driver.current_url)
            
            self.take_screenshot("login_success_dashboard")
            print("✅ Login thành công và redirect đến dashboard!")
        except TimeoutException:
            self.take_screenshot("login_timeout")
            self.fail("Không redirect đến dashboard sau khi login")
    
    def test_06_remember_me_checkbox(self):
        """Test 6: Checkbox Remember Me"""
        print("\n🧪 Test 6: Kiểm tra Remember Me checkbox...")
        
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        try:
            remember_checkbox = self.driver.find_element(By.NAME, "remember")
            
            # Click checkbox
            if not remember_checkbox.is_selected():
                remember_checkbox.click()
                time.sleep(0.5)
            
            self.assertTrue(remember_checkbox.is_selected(), "Remember checkbox không được chọn")
            
            self.take_screenshot("remember_me_checked")
            print("✅ Remember Me checkbox hoạt động!")
        except NoSuchElementException:
            print("⚠️  Remember Me checkbox không tồn tại (optional)")
    
    def test_07_password_field_masked(self):
        """Test 7: Password field được mask"""
        print("\n🧪 Test 7: Kiểm tra password field được mask...")
        
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        password_field = self.driver.find_element(By.NAME, "password")
        
        # Kiểm tra type="password"
        field_type = password_field.get_attribute("type")
        self.assertEqual(field_type, "password", "Password field không được mask")
        
        self.take_screenshot("password_masked")
        print("✅ Password field được mask đúng!")
    
    def test_08_navigation_after_login(self):
        """Test 8: Navigation sau khi login"""
        print("\n🧪 Test 8: Kiểm tra navigation sau login...")
        
        # Login trước
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        
        username_field.send_keys("admin")
        password_field.send_keys("Admin@123")
        
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
        submit_button.click()
        
        time.sleep(3)
        
        # Kiểm tra có thể access các trang khác
        try:
            self.driver.get(f"{self.base_url}/baiviet")
            time.sleep(2)
            
            self.assertNotIn("/auth/login", self.driver.current_url)
            
            self.take_screenshot("navigation_after_login")
            print("✅ Có thể navigate sau khi login!")
        except:
            self.fail("Không thể access trang sau khi login")
    
    def test_09_logout_functionality(self):
        """Test 9: Chức năng logout"""
        print("\n🧪 Test 9: Kiểm tra chức năng logout...")
        
        # Login trước
        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)
        
        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        
        username_field.send_keys("admin")
        password_field.send_keys("Admin@123")
        
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
        submit_button.click()
        
        time.sleep(3)
        
        # Logout
        try:
            self.driver.get(f"{self.base_url}/auth/logout")
            time.sleep(2)
            
            # Kiểm tra redirect về login
            self.assertIn("/auth/login", self.driver.current_url)
            
            self.take_screenshot("after_logout")
            print("✅ Logout thành công!")
        except:
            self.fail("Logout không hoạt động")
    
    # ========================
    # HTML REPORT GENERATOR
    # ========================
    
    @classmethod
    def generate_html_report(cls):
        """Tạo HTML report từ kết quả test"""
        
        total_tests = len(cls.test_results)
        passed_tests = sum(1 for r in cls.test_results if r['status'] == 'PASSED')
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        html_content = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Selenium Test Report - Hotel Media WebApp</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 16px;
            opacity: 0.9;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }}
        
        .summary-card {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .summary-card h3 {{
            font-size: 14px;
            color: #6b7280;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .summary-card .value {{
            font-size: 36px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .summary-card.total .value {{ color: #3b82f6; }}
        .summary-card.passed .value {{ color: #10b981; }}
        .summary-card.failed .value {{ color: #ef4444; }}
        .summary-card.rate .value {{ color: #8b5cf6; }}
        
        .tests {{
            padding: 40px;
        }}
        
        .test-item {{
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s;
        }}
        
        .test-item:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }}
        
        .test-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .test-name {{
            font-size: 18px;
            font-weight: 600;
            color: #111827;
        }}
        
        .test-status {{
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .test-status.passed {{
            background: #d1fae5;
            color: #065f46;
        }}
        
        .test-status.failed {{
            background: #fee2e2;
            color: #991b1b;
        }}
        
        .test-info {{
            display: flex;
            gap: 20px;
            font-size: 14px;
            color: #6b7280;
            margin-top: 10px;
        }}
        
        .test-info span {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .screenshot {{
            margin-top: 15px;
            max-width: 100%;
        }}
        
        .screenshot img {{
            max-width: 100%;
            border-radius: 8px;
            border: 2px solid #e5e7eb;
        }}
        
        .error-message {{
            margin-top: 15px;
            padding: 15px;
            background: #fef2f2;
            border-left: 4px solid #ef4444;
            border-radius: 4px;
            color: #991b1b;
            font-size: 14px;
            font-family: monospace;
            white-space: pre-wrap;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6b7280;
            font-size: 14px;
        }}
        
        @media print {{
            body {{
                background: white;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 SELENIUM TEST REPORT</h1>
            <p>Hotel Media WebApp - Login Functionality Test</p>
            <p style="margin-top: 10px; opacity: 0.8;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card total">
                <h3>Total Tests</h3>
                <div class="value">{total_tests}</div>
            </div>
            <div class="summary-card passed">
                <h3>Passed</h3>
                <div class="value">{passed_tests}</div>
            </div>
            <div class="summary-card failed">
                <h3>Failed</h3>
                <div class="value">{failed_tests}</div>
            </div>
            <div class="summary-card rate">
                <h3>Success Rate</h3>
                <div class="value">{success_rate:.1f}%</div>
            </div>
        </div>
        
        <div class="tests">
            <h2 style="margin-bottom: 20px; color: #111827;">📋 Test Cases Detail</h2>
"""
        
        # Add test results
        for result in cls.test_results:
            status_class = result['status'].lower()
            error_html = ""
            screenshot_html = ""
            
            if result['error']:
                error_html = f'<div class="error-message">{result["error"]}</div>'
            
            if result['screenshot']:
                screenshot_path = os.path.join(cls.screenshots_dir, result['screenshot'])
                screenshot_html = f'''
                <div class="screenshot">
                    <strong>📸 Screenshot:</strong><br>
                    <img src="{screenshot_path}" alt="Screenshot">
                </div>
                '''
            
            html_content += f"""
            <div class="test-item">
                <div class="test-header">
                    <div class="test-name">{result['name'].replace('_', ' ').title()}</div>
                    <div class="test-status {status_class}">{result['status']}</div>
                </div>
                <div class="test-info">
                    <span>⏱️ Duration: {result['duration']}</span>
                    <span>🕐 Time: {result['timestamp']}</span>
                </div>
                {error_html}
                {screenshot_html}
            </div>
            """
        
        html_content += """
        </div>
        
        <div class="footer">
            <p>Generated by Selenium WebDriver | Hotel Media WebApp Testing Suite</p>
            <p style="margin-top: 5px;">© 2025 All Rights Reserved</p>
        </div>
    </div>
</body>
</html>
"""
        
        # Save HTML file
        with open('selenium_test_report.html', 'w', encoding='utf-8') as f:
            f.write(html_content)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
