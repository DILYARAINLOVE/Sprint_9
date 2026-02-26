import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class RegistrationPage(BasePage):
    _first_name_input = (By.NAME, "first_name")
    _last_name_input = (By.NAME, "last_name")
    _username_input = (By.NAME, "username")
    _email_input = (By.NAME, "email")
    _password_input = (By.NAME, "password")
    _submit_button = (By.XPATH, "//button[text()='Создать аккаунт']")

    def register(self, first_name, last_name, email, password):
        print(f"\n>>> Регистрация: заполняем first_name")
        self.send_keys(self._first_name_input, first_name)
        print(">>> first_name заполнено")

        self.send_keys(self._last_name_input, last_name)
        print(">>> last_name заполнено")

        username = email.split('@')[0]
        print(f">>> Заполняем username: {username}")
        self.send_keys(self._username_input, username)
        print(">>> username заполнено")

        self.send_keys(self._email_input, email)
        print(">>> email заполнено")
        self.send_keys(self._password_input, password)
        print(">>> password заполнено")
        sys.stdout.flush()

        time.sleep(1)
        print(">>> Ожидаем активацию кнопки отправки")
        button = self.wait.until(EC.element_to_be_clickable(self._submit_button))
        print(">>> Кнопка активна, кликаем")
        button.click()
        print(">>> Форма отправлена")

        # Ждём редиректа на страницу логина
        try:
            WebDriverWait(self.driver, 10).until(EC.url_contains("/signin"))
            print(">>> Редирект на страницу логина произошёл")
        except:
            print(">>> Редирект не произошёл, остаёмся на текущей странице")
        sys.stdout.flush()