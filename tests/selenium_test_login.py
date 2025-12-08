import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://n23dcpt017-dot.github.io/hotel-media-webapp/templates/login.html"

@pytest.fixture
def driver():
    d = webdriver.Chrome()
    d.maximize_window()
    yield d
    d.quit()


def wait_for(driver, element_id, timeout=5):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, element_id))
    )


def test_login_success(driver):
    driver.get(URL)
    wait_for(driver, "username").send_keys("admin@hotel.com")
    wait_for(driver, "password").send_keys("Admin@123")
    wait_for(driver, "btnLogin").click()

    WebDriverWait(driver, 3).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert "Đăng nhập thành công" in alert.text.lower()
    alert.accept()


def test_login_empty_fields(driver):
    driver.get(URL)
    wait_for(driver, "btnLogin").click()
    error_text = wait_for(driver, "errorMsg").text
    assert "Không được để trống" in error_text.lower()


def test_login_invalid_email(driver):
    driver.get(URL)
    wait_for(driver, "username").send_keys("wrong")
    wait_for(driver, "password").send_keys("Admin@123")
    wait_for(driver, "btnLogin").click()
    error_text = wait_for(driver, "errorMsg").text
    assert "Email hợp lệ" in error_text.lower()


def test_login_short_password(driver):
    driver.get(URL)
    wait_for(driver, "username").send_keys("admin@hotel.com")
    wait_for(driver, "password").send_keys("123")
    wait_for(driver, "btnLogin").click()
    error_text = wait_for(driver, "errorMsg").text
    assert "Ít nhất 6 ký tự" in error_text.lower()


def test_login_cancel_clears_fields(driver):
    driver.get(URL)
    wait_for(driver, "username").send_keys("admin@hotel.com")
    wait_for(driver, "password").send_keys("Admin@123")
    wait_for(driver, "btnCancel").click()

    assert wait_for(driver, "username").get_attribute("value") == ""
    assert wait_for(driver, "password").get_attribute("value") == ""
    assert wait_for(driver, "errorMsg").text.strip() == ""


def test_login_forgot_password_alert(driver):
    driver.get(URL)
    wait_for(driver, "forgotLink").click()
    WebDriverWait(driver, 3).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    assert "Đặt lại mật khẩu" in alert.text.lower()
    alert.accept()
