from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage

class TestRegistration:
    def test_successful_registration(self, driver, user, registration_page, login_page):
        # Ждём загрузки страницы
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Ожидаем появления ссылки "Создать аккаунт" и кликаем
        create_account_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Создать аккаунт"))
        )
        create_account_link.click()

        # Вызываем регистрацию (предполагается, что внутри registration_page.register есть ожидания)
        registration_page.register(user.first_name, user.last_name, user.email, user.password)

        # После регистрации ожидаем появления формы логина (замените селектор, если нужно)
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".login-form"))
        )
        assert login_page.is_login_form_displayed(), "Форма логина не отображается"