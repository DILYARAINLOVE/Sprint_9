from selenium.webdriver.common.by import By
from .base_page import BasePage

class MainPage(BasePage):
    _logout_button = (By.XPATH, "//a[contains(text(),'Выход')]")   # изменено с button на a
    _create_recipe_tab = (By.XPATH, "//a[contains(text(),'Создать рецепт')]")

    def is_logout_displayed(self):
        return self.find_element(self._logout_button).is_displayed()

    def go_to_create_recipe(self):
        self.click(self._create_recipe_tab)