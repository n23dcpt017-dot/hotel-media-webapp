"""
SELENIUM TEST - Login Frontend UI
(Tương thích với file HTML giao diện tĩnh)
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
        chrome_options.add_argument("--log-level=3")
        
        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.implicitly_wait(5)
            cls.base_url = "http://127.0.0.1:5000"
            print("\n" + "="*70)
            print("🚀 BẮT ĐẦU TEST GIAO DIỆN LOGIN (FRONTEND JS)")
            print("="*70 + "\n")
        except Exception as e:
            print(f"❌ Lỗi Driver: {e}")
            raise
    
    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'): cls.driver.quit()
        print("\n✅ TEST COMPLETE.\n")

    def setUp(self):
        self.driver.get(f"{self.base_url}/auth/login")

    def test_01_ui_elements(self):
        """Test 1: Kiểm tra hiển thị các phần tử giao diện"""
        print("\n🧪 Test 1: Kiểm tra UI...")
        try:
            # Kiểm tra tiêu đề
            self.assertIn("Đăng nhập - Hotel CMS", self.driver.title)
            
            # Kiểm tra input bằng ID (theo code HTML của bạn)
            self.driver.find_element(By.ID, "email")
            self.driver.find_element(By.ID, "password")
            self.driver.find_element(By.CLASS_NAME, "btn-login")
            
            # Kiểm tra các nút Social
            socials = self.driver.find_elements(By.CLASS_NAME, "btn-social")
            self.assertEqual(len(socials), 4, "Phải có đủ 4 nút mạng xã hội")
            
            print("✅ UI hiển thị đúng (Input, Button, Socials)")
        except Exception as e:
            self.fail(f"Lỗi UI: {e}")

    def test_02_js_validation_empty(self):
        """Test 2: Kiểm tra validate rỗng của HTML5"""
        print("\n🧪 Test 2: Submit form rỗng...")
        btn = self.driver.find_element(By.CLASS_NAME, "btn-login")
        btn.click()
        
        # HTML5 'required' sẽ chặn submit, URL không đổi
        time.sleep(1)
        self.assertIn("/auth/login", self.driver.current_url)
        print("✅ Form không submit khi rỗng")

    def test_03_js_validation_wrong_email(self):
        """Test 3: Kiểm tra JS validate email sai định dạng"""
        print("\n🧪 Test 3: Nhập sai định dạng Email...")
        
        email = self.driver.find_element(By.ID, "email")
        password = self.driver.find_element(By.ID, "password")
        btn = self.driver.find_element(By.CLASS_NAME, "btn-login")
        
        email.clear(); email.send_keys("admin_khong_co_a_cong")
        password.clear(); password.send_keys("123")
        btn.click()
        
        # Chờ thông báo lỗi hiện ra
        try:
            error_msg = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "error-message"))
            )
            print(f"   Thông báo: '{error_msg.text}'")
            self.assertIn("@", error_msg.text) # Code JS báo lỗi phải chứa ký tự @
            print("✅ JS bắt lỗi email thành công")
        except TimeoutException:
            self.fail("Không thấy thông báo lỗi của JS")

    def test_04_js_login_wrong_credentials(self):
        """Test 4: Nhập sai pass (Check logic JS)"""
        print("\n🧪 Test 4: Nhập sai Password...")
        
        email = self.driver.find_element(By.ID, "email")
        password = self.driver.find_element(By.ID, "password")
        btn = self.driver.find_element(By.CLASS_NAME, "btn-login")
        
        email.clear(); email.send_keys("admin@hotel.com")
        password.clear(); password.send_keys("sai_mat_khau")
        btn.click()
        
        try:
            error_msg = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "error-message"))
            )
            print(f"   Thông báo: '{error_msg.text}'")
            self.assertIn("Sai tài khoản", error_msg.text)
            print("✅ JS bắt lỗi sai pass thành công")
        except TimeoutException:
            self.fail("Không thấy thông báo lỗi sai pass")

    def test_05_js_login_success(self):
        """Test 5: Đăng nhập đúng (Theo tài khoản Demo trong HTML)"""
        print("\n🧪 Test 5: Đăng nhập đúng...")
        
        email = self.driver.find_element(By.ID, "email")
        password = self.driver.find_element(By.ID, "password")
        btn = self.driver.find_element(By.CLASS_NAME, "btn-login")
        
        # Nhập đúng theo hardcode trong JS của bạn
        email.clear(); email.send_keys("admin@hotel.com")
        password.clear(); password.send_keys("admin123")
        btn.click()
        
        # JS sẽ redirect sang tongquan.html (Dù file này chưa có, URL sẽ thay đổi)
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: "tongquan.html" in d.current_url
            )
            print("✅ Redirect sang tongquan.html thành công")
        except TimeoutException:
            self.fail(f"Không redirect. URL hiện tại: {self.driver.current_url}")

    def test_06_show_hide_password(self):
        """Test 6: Nút ẩn/hiện mật khẩu"""
        print("\n🧪 Test 6: Toggle Password...")
        
        pwd_input = self.driver.find_element(By.ID, "password")
        toggle_btn = self.driver.find_element(By.ID, "password-toggle")
        
        # Ban đầu là password
        self.assertEqual(pwd_input.get_attribute("type"), "password")
        
        # Click để hiện
        toggle_btn.click()
        time.sleep(0.5)
        self.assertEqual(pwd_input.get_attribute("type"), "text")
        
        # Click để ẩn
        toggle_btn.click()
        time.sleep(0.5)
        self.assertEqual(pwd_input.get_attribute("type"), "password")
        print("✅ Chức năng ẩn hiện mật khẩu hoạt động")

if __name__ == '__main__':
    unittest.main(verbosity=2)
