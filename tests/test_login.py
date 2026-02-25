from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.main_page import MainPage

class TestLogin:
    def test_login(self, driver, user, login_page, main_page):
        driver.get("https://foodgram-frontend-1.prakticum-team.ru/login")

        # Ждём загрузки страницы
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        login_page.login(user.email, user.password)

        # Ожидаем появления кнопки выхода (замените селектор на реальный, например, ".logout-button")
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".logout-button"))
        )
        assert main_page.is_logout_displayed(), "Кнопка выхода не отображается"