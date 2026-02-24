from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    _email_input = (By.NAME, "email")
    _password_input = (By.NAME, "password")
    _login_button = (By.XPATH, "//button[contains(text(),'Войти')]")

    def login(self, email, password):
        self.send_keys(self._email_input, email)
        self.send_keys(self._password_input, password)
        self.click(self._login_button)

    def is_login_form_displayed(self):
        return self.find_element(self._email_input).is_displayed()