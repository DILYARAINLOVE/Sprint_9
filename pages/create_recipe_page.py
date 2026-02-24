from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from .base_page import BasePage

class CreateRecipePage(BasePage):
    _name_input = (By.NAME, "name")
    _ingredient_input = (By.CSS_SELECTOR, "input[placeholder='Начните вводить ингредиент']")
    _ingredient_dropdown_item = (By.XPATH, "//div[contains(@class, 'dropdown-item')]")  # уточнить
    _description_input = (By.NAME, "description")
    _time_input = (By.NAME, "cooking_time")
    _file_input = (By.CSS_SELECTOR, "input[type='file']")
    _submit_button = (By.XPATH, "//button[contains(text(),'Создать рецепт')]")

    def fill_recipe(self, name, ingredient_text, description, time, image_path):
        self.send_keys(self._name_input, name)
        # ввод ингредиента и выбор из дропдауна
        self.send_keys(self._ingredient_input, ingredient_text)
        # ждём появления элемента списка и кликаем по нему
        item = self.find_element(self._ingredient_dropdown_item)
        item.click()
        self.send_keys(self._description_input, description)
        self.send_keys(self._time_input, time)
        # загрузка файла
        self.send_keys(self._file_input, str(image_path))
        self.click(self._submit_button)