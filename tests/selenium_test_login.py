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
        """Test 1: Trang login load thành công"""
        print("\n🧪 Test 1: Kiểm tra trang login load...")

        self.driver.get(f"{self.base_url}/auth/login")

        self.assertIn("Login", self.driver.title, "Title không chứa 'Login'")
        self.assertIn("/auth/login", self.driver.current_url)

        self.take_screenshot("login_page_loaded")
        print("✅ Trang login load thành công!")

    def test_02_login_form_elements_exist(self):
        """Test 2: Các elements của form login tồn tại"""
        print("\n🧪 Test 2: Kiểm tra các elements của form...")

        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)

        try:
            username_field = self.driver.find_element(By.NAME, "username")
            self.assertTrue(username_field.is_displayed(), "Username field không hiển thị")
            print("   ✓ Username field: OK")
        except NoSuchElementException:
            self.fail("Không tìm thấy username field")

        try:
            password_field = self.driver.find_element(By.NAME, "password")
            self.assertTrue(password_field.is_displayed(), "Password field không hiển thị")
            print("   ✓ Password field: OK")
        except NoSuchElementException:
            self.fail("Không tìm thấy password field")

        try:
            submit_button = self.driver.find_element(
                By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"
            )
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

        submit_button = self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"
        )
        submit_button.click()

        time.sleep(1)

        self.assertIn("/auth/login", self.driver.current_url)

        self.take_screenshot("login_empty_fields")
        print("✅ Không cho phép login với fields trống!")

    def test_04_login_with_wrong_credentials(self):
        """Test 4: Login với thông tin sai"""
        print("\n🧪 Test 4: Kiểm tra login với thông tin sai...")

        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)

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

        self.assertIn("/auth/login", self.driver.current_url)

        self.take_screenshot("login_wrong_credentials")
        print("✅ Không cho phép login với thông tin sai!")

    def test_05_login_with_correct_credentials(self):
        """Test 5: Login với thông tin đúng"""
        print("\n🧪 Test 5: Kiểm tra login với thông tin đúng...")

        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)

        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")

        username_field.clear()
        username_field.send_keys("admin")

        password_field.clear()
        password_field.send_keys("Admin@123")

        self.take_screenshot("login_before_submit")

        submit_button = self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit'], input[type='submit']"
        )
        submit_button.click()

        time.sleep(3)

        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: "/dashboard" in driver.current_url or "/index" in driver.current_url
            )
            self.assertNotIn("/auth/login", self.driver.current_url)
            self.take_screenshot("login_success_dashboard")
            print("✅ Login thành công!")
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

            if not remember_checkbox.is_selected():
                remember_checkbox.click()
                time.sleep(0.5)

            self.assertTrue(remember_checkbox.is_selected())

            self.take_screenshot("remember_me_checked")
            print("✅ Remember Me checkbox hoạt động!")
        except NoSuchElementException:
            print("⚠️ Remember Me checkbox không tồn tại (optional)")

    def test_07_password_field_masked(self):
        """Test 7: Password field được mask"""
        print("\n🧪 Test 7: Kiểm tra password field được mask...")

        self.driver.get(f"{self.base_url}/auth/login")
        time.sleep(1)

        password_field = self.driver.find_element(By.NAME, "password")
        field_type = password_field.get_attribute("type")

        self.assertEqual(field_type, "password")

        self.take_screenshot("password_masked")
        print("✅ Password field được mask đúng!")

    def test_08_navigation_after_login(self):
        """Test 8: Navigation sau khi login"""
        print("\n🧪 Test 8: Kiểm tra navigation sau login...")

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

        time.sleep(3)

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

        time.sleep(3)

        try:
            self.driver.get(f"{self.base_url}/auth/logout")
            time.sleep(2)

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
        passed_tests = sum(1 for r in cls.test_results if r["status"] == "PASSED")
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

        
        with open("selenium_test_report.html", "w", encoding="utf-8") as f:
            f.write("<html><body><h1>Report generated</h1></body></html>")


if __name__ == "__main__":
    unittest.main(verbosity=2)
