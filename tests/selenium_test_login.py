"""
SELENIUM TEST - Login Functionality (FIXED FOR PYTHON 3.13)
"""
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
from datetime import datetime
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class LoginSeleniumTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Setup trước khi chạy tất cả tests"""
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        # Tắt bớt log rác của Chrome
        chrome_options.add_argument("--log-level=3") 
        
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.implicitly_wait(5) # Giảm wait ngầm định để tránh conflict với wait rõ ràng
            
            # QUAN TRỌNG: Dùng 127.0.0.1 thay vì localhost để tránh lỗi IPv6 trên Windows
            cls.base_url = "http://127.0.0.1:5000"
            
            cls.test_results = []
            cls.screenshots_dir = "test_screenshots"
            
            if not os.path.exists(cls.screenshots_dir):
                os.makedirs(cls.screenshots_dir)
                
            print("\n" + "="*70)
            print("🚀 BẮT ĐẦU SELENIUM TEST (PYTHON 3.13 COMPATIBLE)")
            print("="*70 + "\n")

            # Check kết nối server
            try:
                cls.driver.get(f"{cls.base_url}/auth/login")
                print("✅ Kết nối đến Server thành công!")
            except WebDriverException:
                print("❌ KHÔNG THỂ KẾT NỐI ĐẾN SERVER!")
                print("💡 Hãy đảm bảo bạn đã chạy 'python run.py' ở một cửa sổ khác.")
                cls.driver.quit()
                sys.exit(1)
            
        except Exception as e:
            print(f"❌ Lỗi khởi tạo Driver: {e}")
            raise
    
    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver') and cls.driver:
            cls.driver.quit()
        cls.generate_html_report()
        print("\n✅ HOÀN THÀNH TEST. Xem báo cáo tại: selenium_test_report.html\n")
    
    def setUp(self):
        self.start_time = time.time()
    
    def tearDown(self):
        """Cleanup (Đã sửa lỗi crash trên Python 3.11+)"""
        duration = time.time() - self.start_time
        
        # --- LOGIC BẮT LỖI MỚI CHO PYTHON 3.13 ---
        has_error = False
        error_msg = None

        # Kiểm tra result từ _outcome (cấu trúc mới)
        if hasattr(self._outcome, 'result'):
            result = self._outcome.result
            if result.errors:
                has_error = True
                error_msg = str(result.errors[0][1])
            elif result.failures:
                has_error = True
                error_msg = str(result.failures[0][1])
        # Fallback cho Python cũ (nếu có)
        elif hasattr(self._outcome, 'errors') and self._outcome.errors:
            has_error = True
            error_msg = str(self._outcome.errors[0][1])

        status = 'FAILED' if has_error else 'PASSED'
        
        # Chụp màn hình nếu lỗi
        screenshot_name = None
        if has_error and hasattr(self, 'driver') and self.driver:
            try:
                screenshot_name = f"{self._testMethodName}_{int(time.time())}.png"
                self.driver.save_screenshot(os.path.join(self.screenshots_dir, screenshot_name))
                print(f"   📸 Đã chụp ảnh lỗi: {screenshot_name}")
            except:
                pass
        
        self.test_results.append({
            'name': self._testMethodName,
            'status': status,
            'duration': f"{duration:.2f}s",
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'error': error_msg,
            'screenshot': screenshot_name
        })

    def take_screenshot(self, name):
        if hasattr(self, 'driver'):
            fname = f"{name}_{int(time.time())}.png"
            self.driver.save_screenshot(os.path.join(self.screenshots_dir, fname))
            return fname
        return None

    # ========================
    # TEST CASES (ĐÃ CẬP NHẬT WAIT)
    # ========================
    
    def test_01_login_page_loads(self):
        """Test 1: Trang login load thành công"""
        print("\n🧪 Test 1: Kiểm tra trang login load...")
        self.driver.get(f"{self.base_url}/auth/login")
        
        # FIX: Chờ thẻ body xuất hiện để đảm bảo trang đã load
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            # Chờ tiêu đề trang không còn rỗng
            WebDriverWait(self.driver, 5).until(lambda d: d.title != "")
        except TimeoutException:
            self.fail("Trang web không tải được (Timeout)")

        self.assertIn("Login", self.driver.title, f"Title sai: '{self.driver.title}'")
        print("✅ OK")

    def test_02_login_form_elements_exist(self):
        """Test 2: Các elements của form login tồn tại"""
        print("\n🧪 Test 2: Kiểm tra elements...")
        self.driver.get(f"{self.base_url}/auth/login")
        
        try:
            # Chờ form xuất hiện tối đa 5s
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            
            self.driver.find_element(By.NAME, "username")
            self.driver.find_element(By.NAME, "password")
            # Tìm nút submit linh hoạt hơn
            try:
                self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            except NoSuchElementException:
                self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
                
            print("✅ OK")
        except TimeoutException:
            self.fail("Form login không hiển thị (Timeout)")
        except NoSuchElementException as e:
            self.fail(f"Thiếu element: {e}")

    def test_03_login_with_empty_fields(self):
        """Test 3: Login với fields trống"""
        print("\n🧪 Test 3: Login rỗng...")
        self.driver.get(f"{self.base_url}/auth/login")
        
        # Tìm và click nút submit
        try:
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"))
            )
            btn.click()
            time.sleep(1)
            # Vẫn phải ở trang login
            self.assertIn("/auth/login", self.driver.current_url)
            print("✅ OK")
        except Exception as e:
            self.fail(f"Lỗi thao tác: {e}")

    def test_04_login_with_wrong_credentials(self):
        """Test 4: Login sai"""
        print("\n🧪 Test 4: Login sai...")
        self.driver.get(f"{self.base_url}/auth/login")
        
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, "username")))
            self.driver.find_element(By.NAME, "username").send_keys("wrong_user")
            self.driver.find_element(By.NAME, "password").send_keys("wrong_pass")
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
            
            time.sleep(1)
            self.assertIn("/auth/login", self.driver.current_url)
            print("✅ OK")
        except Exception as e:
            self.fail(f"Lỗi: {e}")

    def test_05_login_with_correct_credentials(self):
        """Test 5: Login đúng"""
        print("\n🧪 Test 5: Login đúng...")
        self.driver.get(f"{self.base_url}/auth/login")
        
        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, "username")))
            self.driver.find_element(By.NAME, "username").send_keys("admin")
            self.driver.find_element(By.NAME, "password").send_keys("Admin@123")
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
            
            # Chờ redirect
            WebDriverWait(self.driver, 10).until(
                lambda d: "/dashboard" in d.current_url or "/index" in d.current_url
            )
            print("✅ OK - Đã vào Dashboard")
        except TimeoutException:
            print(f"⚠️ URL hiện tại: {self.driver.current_url}")
            self.fail("Không redirect sang Dashboard sau khi login")

    def test_06_remember_me_checkbox(self):
        """Test 6: Remember Me"""
        print("\n🧪 Test 6: Checkbox...")
        self.driver.get(f"{self.base_url}/auth/login")
        try:
            chk = self.driver.find_element(By.NAME, "remember")
            if not chk.is_selected():
                chk.click()
            print("✅ OK")
        except NoSuchElementException:
            print("⚠️ Bỏ qua (Không có checkbox)")

    def test_07_password_field_masked(self):
        """Test 7: Password mask"""
        print("\n🧪 Test 7: Password mask...")
        self.driver.get(f"{self.base_url}/auth/login")
        try:
            pwd = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, "password")))
            self.assertEqual(pwd.get_attribute("type"), "password")
            print("✅ OK")
        except Exception as e:
            self.fail(str(e))

    def test_08_navigation_after_login(self):
        """Test 8: Navigation"""
        print("\n🧪 Test 8: Navigation...")
        # Login lại để chắc chắn
        self.driver.get(f"{self.base_url}/auth/login")
        self.driver.find_element(By.NAME, "username").send_keys("admin")
        self.driver.find_element(By.NAME, "password").send_keys("Admin@123")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']").click()
        time.sleep(1)
        
        # Thử vào trang bài viết
        self.driver.get(f"{self.base_url}/baiviet")
        time.sleep(1)
        self.assertNotIn("/auth/login", self.driver.current_url)
        print("✅ OK")

    def test_09_logout_functionality(self):
        """Test 9: Logout"""
        print("\n🧪 Test 9: Logout...")
        # Giả sử đang login từ test trước
        self.driver.get(f"{self.base_url}/auth/logout")
        
        # Chờ redirect về login
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: "/auth/login" in d.current_url
            )
            print("✅ OK")
        except TimeoutException:
            self.fail("Không redirect về login sau khi logout")

    @classmethod
    def generate_html_report(cls):
        # (Code tạo HTML giữ nguyên như cũ hoặc rút gọn, phần quan trọng là logic test)
        with open('selenium_test_report.html', 'w', encoding='utf-8') as f:
            f.write("<html><body><h1>Test Report</h1><ul>")
            for r in cls.test_results:
                color = "green" if r['status'] == 'PASSED' else "red"
                f.write(f"<li style='color:{color}'>{r['name']}: {r['status']} (Error: {r['error']})</li>")
            f.write("</ul></body></html>")

if __name__ == '__main__':
    unittest.main(verbosity=2)
