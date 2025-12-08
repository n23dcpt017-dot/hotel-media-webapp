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

URL = "https://n23dcpt017-dot.github.io/hotel-media-webapp/templates/login.html"


class LoginSeleniumTest(unittest.TestCase):
    """Test cases cho chức năng login sử dụng Selenium"""

    @classmethod
    def setUpClass(cls):
        """Setup trước khi chạy tất cả tests"""
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')

        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.implicitly_wait(10)
            cls.base_url = "http://localhost:5000"
            cls.test_results = []
            cls.screenshots_dir = "test_screenshots"

            if not os.path.exists(cls.screenshots_dir):
                os.makedirs(cls.screenshots_dir)

            print("\n" + "=" * 70)
            print("🚀 BẮT ĐẦU SELENIUM TEST - LOGIN FUNCTIONALITY")
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
            self.driver.save_screenshot(screenshot_path)
            test_result["screenshot"] = screenshot_name
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
        print("\n🧪 Test 1: Kiểm tra trang login load...")
        self.driver.get(f"{self.base_url}/auth/login")

        self.assertIn("Login", self.driver.title)
        self.assertIn("/auth/login", self.driver.current_url)

        self.take_screenshot("login_page_loaded")
        print("✅ Trang login load thành công!")

    def test_02_login_form_elements_exist(self):
        print("\n🧪 Test 2: Kiểm tra các elements của form...")

        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)

        try:
            username_field = self.driver.find_element(By.NAME, "username")
            self.assertTrue(username_field.is_displayed())
            print("   ✓ Username field: OK")
        except NoSuchElementException:
            self.fail("Không tìm thấy username field")

        try:
            password_field = self.driver.find_element(By.NAME, "password")
            self.assertTrue(password_field.is_displayed())
            print("   ✓ Password field: OK")
        except NoSuchElementException:
            self.fail("Không tìm thấy password field")

        try:
            submit_button = self.driver.find_element(
                By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"
            )
            self.assertTrue(submit_button.is_displayed())
            print("   ✓ Submit button: OK")
        except NoSuchElementException:
            self.fail("Không tìm thấy submit button")

        self.take_screenshot("login_form_elements")
        print("✅ Tất cả elements đều tồn tại!")

    # Các test còn lại giữ nguyên code của m (indent đã tự đúng)


if __name__ == "__main__":
    unittest.main(verbosity=2)
