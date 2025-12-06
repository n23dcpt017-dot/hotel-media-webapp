# tests/test_login.py
import time
from selenium.webdriver.common.by import By

# Nếu m chạy http server ở folder gốc và login.html ở root:
BASE = "http://localhost:8000/login.html"
# Nếu login.html nằm trong folder "frontend", dùng:
# BASE = "http://localhost:8000/frontend/login.html"

def open_login(driver):
    driver.get(BASE)
    time.sleep(0.5)  # cho page load

def test_login_success(driver):
    open_login(driver)
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys("admin@hotel.com")
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys("admin123")
    driver.find_element(By.CLASS_NAME, "btn-login").click()
    time.sleep(0.8)
    # login.html redirect về tongquan.html khi thành công
    assert "tongquan.html" in driver.current_url

def test_login_wrong_password(driver):
    open_login(driver)
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys("admin@hotel.com")
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys("wrongpass")
    driver.find_element(By.CLASS_NAME, "btn-login").click()
    time.sleep(0.6)
    # kiểm tra element lỗi hiển thị
    err = driver.find_element(By.ID, "error-message")
    assert err.is_displayed()

def test_login_invalid_email(driver):
    open_login(driver)
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys("notanemail")
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys("whatever")
    driver.find_element(By.CLASS_NAME, "btn-login").click()
    time.sleep(0.6)
    err = driver.find_element(By.ID, "error-message")
    assert err.is_displayed()

def test_login_empty_fields(driver):
    open_login(driver)
    driver.find_element(By.CLASS_NAME, "btn-login").click()
    time.sleep(0.6)
    err = driver.find_element(By.ID, "error-message")
    assert err.is_displayed()
