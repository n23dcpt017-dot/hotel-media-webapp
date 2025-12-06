from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

BASE_URL = "https://hotel-media-webapp-group11.onrender.com/frontend/login.html"

def setup_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def test_login_success():
    driver = setup_driver()
    driver.get(BASE_URL)

    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "email").send_keys("admin@hotel.com")

    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys("admin123")

    driver.find_element(By.CLASS_NAME, "btn-login").click()
    time.sleep(1)

    assert "tongquan.html" in driver.current_url

    driver.quit()


def test_login_wrong_password():
    driver = setup_driver()
    driver.get(BASE_URL)

    driver.find_element(By.ID, "email").send_keys("admin@hotel.com")
    driver.find_element(By.ID, "password").send_keys("sai_mat_khau")
    driver.find_element(By.CLASS_NAME, "btn-login").click()
    time.sleep(1)

    error = driver.find_element(By.ID, "error-message").is_displayed()
    assert error is True

    driver.quit()


def test_login_wrong_email_format():
    driver = setup_driver()
    driver.get(BASE_URL)

    driver.find_element(By.ID, "email").send_keys("khongcop@")
    driver.find_element(By.ID, "password").send_keys("123456")
    driver.find_element(By.CLASS_NAME, "btn-login").click()
    time.sleep(1)

    error = driver.find_element(By.ID, "error-message").is_displayed()
    assert error is True

    driver.quit()


def test_login_empty_fields():
    driver = setup_driver()
    driver.get(BASE_URL)

    driver.find_element(By.CLASS_NAME, "btn-login").click()
    time.sleep(1)

    error = driver.find_element(By.ID, "error-message").is_displayed()
    assert error is True

    driver.quit()
