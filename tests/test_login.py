from pages.login_page import LoginPage
from pages.main_page import MainPage

class TestLogin:
    def test_login(self, driver, user, login_page, main_page):
        # Предварительно нужно создать пользователя (через API или UI)
        # Для простоты будем считать, что пользователь уже существует
        driver.get("https://foodgram.example.com/login")  # прямой переход
        login_page.login(user.email, user.password)
        assert main_page.is_logout_displayed(), "Кнопка выхода не отображается"