from selenium.webdriver.common.by import By
from .base_page import BasePage

class RegistrationPage(BasePage):
    # Локаторы
    _first_name_input = (By.NAME, "firstName")   # уточните по реальному приложению
    _last_name_input = (By.NAME, "lastName")
    _email_input = (By.NAME, "email")
    _password_input = (By.NAME, "password")
    _register_button = (By.XPATH, "//button[contains(text(),'Создать аккаунт')]")

    def register(self, first_name, last_name, email, password):
        self.send_keys(self._first_name_input, first_name)
        self.send_keys(self._last_name_input, last_name)
        self.send_keys(self._email_input, email)
        self.send_keys(self._password_input, password)
        self.click(self._register_button)