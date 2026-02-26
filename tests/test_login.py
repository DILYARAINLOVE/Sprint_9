import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.registration_page import RegistrationPage

def handle_alert(driver):
    try:
        alert = driver.switch_to.alert
        text = alert.text
        print(f">>> Обнаружен алерт: {text}")
        alert.accept()
        time.sleep(1)
        return text
    except NoAlertPresentException:
        return None

class TestLogin:
    def test_login(self, driver, user, login_page, main_page, registration_page):
        driver.get("https://foodgram-frontend-1.prakticum-team.ru/signin")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        create_account_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Создать аккаунт"))
        )
        create_account_link.click()
        WebDriverWait(driver, 30).until(EC.url_contains("/signup"))

        registration_page.register(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password
        )

        time.sleep(2)  # даём время серверу

        driver.get("https://foodgram-frontend-1.prakticum-team.ru/signin")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "email")))

        username = user.email.split('@')[0]
        login_page.login(username, user.password)
        time.sleep(2)
        handle_alert(driver)

        assert "/signin" not in driver.current_url, "Вход не удался"
        # Проверяем наличие кнопки выхода через метод главной страницы
        assert main_page.is_logout_displayed(), "Кнопка выхода не отображается"
        print(">>> Тест логина пройден!")