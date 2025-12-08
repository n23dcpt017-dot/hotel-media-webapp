"""
SELENIUM TEST - Login Frontend UI
(Đã chỉnh sửa để khớp với HTML id="email" và Logic JavaScript)
"""
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import time
import os
import sys

# Add parent directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class LoginUITest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        # Tắt log rác
        chrome_options.add_argument("--log-level=3")
        
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.implicitly_wait(3) # Wait ngắn
            # Dùng 127.0.0.1 để ổn định hơn localhost trên Windows
            cls.base_url = "http://127.0.0.1:5000"
            
            # Tạo folder ảnh
            cls.screenshots_dir = "test_screenshots"
            if not os.path.exists(cls.screenshots_dir):
                os.makedirs(cls.screenshots_dir)

            print("\n" + "="*70)
            print("🚀 BẮT ĐẦU TEST GIAO DIỆN (KHỚP VỚI HTML CỦA BẠN)")
            print("="*70 + "\n")
        except Exception as e:
            print(f"❌ Lỗi Driver: {e}")
            raise
    
    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'): cls.driver.quit()
        print("\n✅ TEST COMPLETE.\n")

    def setUp(self):
        # Trước mỗi test, load lại trang login
        self.driver.get(f"{self.base_url}/auth/login")

    def tearDown(self):
        # Chụp ảnh nếu lỗi
        if hasattr(self._outcome, 'result'):
            result = self._outcome.result
            if result.errors or result.failures:
                try:
                    fname = f"{self._testMethodName}_{int(time.time())}.png"
                    self.driver.save_screenshot(os.path.join(self.screenshots_dir, fname))
                    print(f"   📸 Đã chụp ảnh lỗi: {fname}")
                except: pass

    # ==========================================
    # CÁC TEST CASE ĐƯỢC VIẾT LẠI CHO ID="EMAIL"
    # ==========================================

    def test_01_ui_elements(self):
        """Test 1: Kiểm tra các phần tử (Input, Button)"""
        print("\n🧪 Test 1: Kiểm tra UI...")
        try:
            # Chờ trang load
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # Kiểm tra Title
            self.assertIn("Đăng nhập", self.driver.title)
            
            # QUAN TRỌNG: Tìm theo ID vì HTML của bạn dùng id="email"
            self.driver.find_element(By.ID, "email")
            self.driver.find_element(By.ID, "password")
            
            # Tìm nút login theo class
            self.driver.find_element(By.CLASS_NAME, "btn-login")
            
            print("✅ UI hiển thị đúng")
        except Exception as e:
            self.fail(f"Lỗi UI: {e}")

    def test_02_js_empty_submit(self):
        """Test 2: Submit rỗng (HTML5 required chặn lại)"""
        print("\n🧪 Test 2: Submit rỗng...")
        btn = self.driver.find_element(By.CLASS_NAME, "btn-login")
        btn.click()
        time.sleep(1)
        # URL không đổi vì trình duyệt chặn submit
        self.assertIn("/auth/login", self.driver.current_url)
        print("✅ HTML5 required hoạt động")

    def test_03_js_invalid_email(self):
        """Test 3: Email sai định dạng (JS check)"""
        print("\n🧪 Test 3: Email thiếu @...")
        
        self.driver.find_element(By.ID, "email").send_keys("admin_khong_co_a_cong")
        self.driver.find_element(By.ID, "password").send_keys("123")
        self.driver.find_element(By.CLASS_NAME, "btn-login").click()
        
        # Chờ thông báo lỗi của JS hiện ra
        try:
            error_msg = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.ID, "error-message"))
            )
            print(f"   Thông báo: {error_msg.text}")
            self.assertIn("@", error_msg.text) # JS báo lỗi email
            print("✅ JS bắt lỗi email thành công")
        except TimeoutException:
            self.fail("Không thấy thông báo lỗi JS")

    def test_04_js_wrong_credentials(self):
        """Test 4: Sai mật khẩu (JS check)"""
        print("\n🧪 Test 4: Sai mật khẩu...")
        
        email = self.driver.find_element(By.ID, "email")
        password = self.driver.find_element(By.ID, "password")
        
        email.clear(); email.send_keys("admin@hotel.com") # Email đúng
        password.clear(); password.send_keys("sai_pass")  # Pass sai
        
        self.driver.find_element(By.CLASS_NAME, "btn-login").click()
        
        try:
            error_msg = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.ID, "error-message"))
            )
            print(f"   Thông báo: {error_msg.text}")
            self.assertIn("Sai tài khoản", error_msg.text)
            print("✅ JS bắt lỗi sai pass thành công")
        except TimeoutException:
            self.fail("Không thấy thông báo lỗi sai pass")

    def test_05_js_login_success(self):
        """Test 5: Đăng nhập đúng (Tài khoản cứng trong JS)"""
        print("\n🧪 Test 5: Đăng nhập đúng...")
        
        email = self.driver.find_element(By.ID, "email")
        password = self.driver.find_element(By.ID, "password")
        
        # Nhập đúng tài khoản demo trong HTML của bạn
        email.clear(); email.send_keys("admin@hotel.com")
        password.clear(); password.send_keys("admin123")
        
        self.driver.find_element(By.CLASS_NAME, "btn-login").click()
        
        # JS chuyển hướng sang tongquan.html
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: "tongquan.html" in d.current_url
            )
            print("✅ Redirect sang tongquan.html thành công")
        except TimeoutException:
            self.fail(f"Không redirect. URL hiện tại: {self.driver.current_url}")

    def test_06_toggle_password(self):
        """Test 6: Ẩn hiện mật khẩu"""
        print("\n🧪 Test 6: Ẩn/Hiện mật khẩu...")
        pwd = self.driver.find_element(By.ID, "password")
        btn = self.driver.find_element(By.ID, "password-toggle")
        
        # Ban đầu password ẩn
        self.assertEqual(pwd.get_attribute("type"), "password")
        
        # Click hiện
        btn.click()
        time.sleep(0.5)
        self.assertEqual(pwd.get_attribute("type"), "text")
        print("✅ Chức năng Toggle hoạt động")

if __name__ == '__main__':
    unittest.main(verbosity=2)
