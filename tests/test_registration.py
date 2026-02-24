from selenium.webdriver.common.by import By
import pytest
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage

class TestRegistration:
    def test_successful_registration(self, driver, user, registration_page, login_page):
        # Предположим, что на главной есть кнопка "Создать аккаунт"
        driver.find_element(By.LINK_TEXT, "Создать аккаунт").click()
        registration_page.register(user.first_name, user.last_name, user.email, user.password)
        # Проверяем, что произошёл переход на страницу логина
        assert login_page.is_login_form_displayed(), "Форма логина не отображается"