"""
SELENIUM TEST - Login UI & JavaScript Logic
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
            cls.driver.implicitly_wait(3)
            cls.base_url = "http://127.0.0.1:5000"
            cls.screenshots_dir = "test_screenshots"
            if not os.path.exists(cls.screenshots_dir):
                os.makedirs(cls.screenshots_dir)

            print("\n" + "="*70)
            print("🚀 BẮT ĐẦU TEST GIAO DIỆN (HTML/JS)")
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

    def tearDown(self):
        # Chụp ảnh lỗi
        has_error = False
        if hasattr(self._outcome, 'result'):
             if self._outcome.result.errors or self._outcome.result.failures: has_error = True
        elif hasattr(self._outcome, 'errors') and self._outcome.errors: has_error = True

        if has_error:
            try:
                fname = f"{self._testMethodName}_{int(time.time())}.png"
                self.driver.save_screenshot(os.path.join(self.screenshots_dir, fname))
            except: pass

    # --- TEST CASES KHỚP VỚI HTML CỦA BẠN ---

    def test_01_ui_elements(self):
        print("\n🧪 Test 1: Kiểm tra UI...")
        try:
            # Chờ thẻ body load
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # HTML của bạn dùng id="email" và id="password"
            self.driver.find_element(By.ID, "email")
            self.driver.find_element(By.ID, "password")
            self.driver.find_element(By.CLASS_NAME, "btn-login")
            
            print("✅ Đã tìm thấy các ô nhập liệu và nút bấm")
        except Exception as e:
            self.fail(f"Lỗi UI: Không tìm thấy phần tử HTML. {e}")

    def test_02_js_validation_empty(self):
        print("\n🧪 Test 2: Submit rỗng...")
        self.driver.find_element(By.CLASS_NAME, "btn-login").click()
        time.sleep(1)
        # HTML5 required sẽ chặn submit, URL giữ nguyên
        self.assertIn("/auth/login", self.driver.current_url)
        print("✅ HTML5 chặn submit rỗng thành công")

    def test_03_js_wrong_credentials(self):
        print("\n🧪 Test 3: Test JS báo lỗi sai pass...")
        
        self.driver.find_element(By.ID, "email").clear()
        self.driver.find_element(By.ID, "email").send_keys("admin@hotel.com")
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").send_keys("sai_pass_roi")
        
        self.driver.find_element(By.CLASS_NAME, "btn-login").click()
        
        # Chờ JS hiển thị thông báo lỗi
        try:
            error_msg = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "error-message"))
            )
            print(f"   JS báo lỗi: '{error_msg.text}'")
            self.assertIn("Sai tài khoản", error_msg.text)
            print("✅ JS hoạt động đúng logic")
        except TimeoutException:
            self.fail("JS không hiển thị thông báo lỗi (class='error-message')")

    def test_04_js_login_success(self):
        print("\n🧪 Test 4: Test JS login thành công...")
        
        # Nhập đúng tài khoản cứng trong file HTML
        self.driver.find_element(By.ID, "email").clear()
        self.driver.find_element(By.ID, "email").send_keys("admin@hotel.com")
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").send_keys("admin123")
        
        self.driver.find_element(By.CLASS_NAME, "btn-login").click()
        
        # JS chuyển hướng sang tongquan.html
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: "tongquan.html" in d.current_url
            )
            print("✅ JS redirect sang trang tongquan.html thành công")
        except TimeoutException:
            self.fail("Không redirect. Kiểm tra lại JS trong file HTML.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
