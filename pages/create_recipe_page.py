import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class CreateRecipePage(BasePage):
    # Поля формы
    _name_input = (By.XPATH, "//label[contains(.,'Название рецепта')]/input")
    _description_input = (By.XPATH, "//label[contains(.,'Описание рецепта')]/textarea")
    _time_input = (By.XPATH, "//label[contains(.,'Время приготовления')]/input")
    _file_input = (By.CSS_SELECTOR, "input[type='file']")
    _submit_button = (By.XPATH, "//button[contains(text(),'Создать рецепт')]")

    # Поля для ингредиента
    _ingredient_name_input = (By.XPATH, "//label[contains(.,'Ингредиенты')]//input")
    _ingredient_amount_input = (By.CSS_SELECTOR, "input[class*='ingredientsAmountValue']")
    _ingredient_dropdown_item = (By.XPATH, "//div[contains(@class, 'dropdown-item')]")
    _add_ingredient_button = (By.XPATH, "//div[text()='Добавить ингредиент']")
    _added_ingredients_container = (By.CSS_SELECTOR, ".styles_ingredientsAdded__35vNf")

    def add_ingredient(self, name, amount):
        """Добавляет ингредиент: вводит название, выбирает из списка, вводит количество, нажимает 'Добавить'."""
        print(f">>> Добавляем ингредиент: {name} {amount}")
        # Вводим название ингредиента
        self.send_keys(self._ingredient_name_input, name)
        print(">>> Текст введен, ожидаем появления выпадающего списка...")
        time.sleep(2)

        # Отладочный вывод HTML после ввода
        print(">>> HTML после ввода (первые 2000 символов):")
        print(self.driver.page_source[:2000])
        sys.stdout.flush()

        # Пытаемся найти элементы выпадающего списка с увеличенным таймаутом
        try:
            items = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(self._ingredient_dropdown_item)
            )
            print(f">>> Найдено элементов в выпадающем списке: {len(items)}")
            if items:
                items[0].click()
                print(">>> Ингредиент выбран из списка")
        except Exception as e:
            print(f">>> Выпадающий список не появился: {e}")
            # Если список не появился, пробуем найти любой элемент с текстом, содержащим название
            try:
                alt_item = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(),'{name}')]"))
                )
                alt_item.click()
                print(">>> Ингредиент выбран по альтернативному XPath")
            except:
                print(">>> Не удалось выбрать ингредиент, продолжаем без выбора")

        # Вводим количество
        amount_input = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self._ingredient_amount_input)
        )
        amount_input.send_keys(str(amount))
        print(">>> Количество введено")

        # Нажимаем кнопку "Добавить ингредиент"
        add_btn = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self._add_ingredient_button)
        )
        print(f">>> Кнопка 'Добавить ингредиент' найдена, disabled={add_btn.get_attribute('disabled')}")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", add_btn)
        time.sleep(0.5)
        try:
            add_btn.click()
        except:
            self.driver.execute_script("arguments[0].click();", add_btn)
        print(">>> Кнопка 'Добавить ингредиент' нажата")

        # Отладочный вывод HTML контейнера после клика
        time.sleep(1)
        try:
            container = self.driver.find_element(*self._added_ingredients_container)
            print(">>> HTML контейнера добавленных ингредиентов после клика:")
            print(container.get_attribute("outerHTML"))
        except:
            print(">>> Контейнер не найден или пуст")

        # Ожидаем, что контейнер добавленных ингредиентов станет видимым
        container = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self._added_ingredients_container)
        )
        # Ищем внутри контейнера элемент с текстом названия ингредиента
        ingredient_element = container.find_element(By.XPATH, f".//*[contains(text(),'{name}')]")
        assert ingredient_element.is_displayed(), f"Ингредиент '{name}' не отображается в списке добавленных"
        print(">>> Ингредиент добавлен и виден в списке")

    def fill_recipe(self, name, ingredient_name, ingredient_amount, description, cooking_time, image_path):
        """Заполняет форму создания рецепта и отправляет."""
        print(f"\n>>> Текущий URL: {self.driver.current_url}")
        print(">>> ПОЛНЫЙ HTML страницы (первые 10000 символов):")
        print(self.driver.page_source[:10000])
        sys.stdout.flush()

        print(">>> Заполняем название")
        self.send_keys(self._name_input, name)
        print(">>> Название заполнено")

        # Добавляем ингредиент
        self.add_ingredient(ingredient_name, ingredient_amount)

        print(">>> Заполняем описание")
        self.send_keys(self._description_input, description)

        print(">>> Заполняем время")
        self.send_keys(self._time_input, str(cooking_time))

        print(">>> Загружаем изображение")
        file_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self._file_input)
        )
        file_input.send_keys(str(image_path))
        print(">>> Изображение загружено")

        print(">>> Проверяем состояние кнопки отправки")
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self._submit_button)
        )
        is_disabled = submit_button.get_attribute("disabled")
        print(f">>> Кнопка 'Создать рецепт' disabled={is_disabled}")

        if is_disabled is not None:
            print(">>> Кнопка всё ещё неактивна, пробуем выбрать тег (если есть)")
            # Попробуем выбрать первый тег, если они есть
            try:
                first_tag = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'checkbox-container')]//button"))
                )
                first_tag.click()
                print(">>> Тег выбран")
                time.sleep(1)
            except:
                print(">>> Теги не найдены или не требуются")

        # Повторная проверка
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self._submit_button)
        )
        print(">>> Кнопка активна, кликаем")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(0.5)
        try:
            submit_button.click()
        except:
            self.driver.execute_script("arguments[0].click();", submit_button)
        print(">>> Форма отправлена")

        # Ждём изменения URL с увеличенным таймаутом
        WebDriverWait(self.driver, 60).until(
            EC.url_contains("/recipes")
        )
        print(">>> Редирект на страницу со списком рецептов произошёл")