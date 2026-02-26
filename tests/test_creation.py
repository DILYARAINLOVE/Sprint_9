import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.create_recipe_page import CreateRecipePage
from pages.registration_page import RegistrationPage

class TestCreateRecipe:
    def test_create_recipe(self, driver, user, recipe, login_page, main_page, create_recipe_page, registration_page):
        # Регистрация нового пользователя
        driver.get("https://foodgram-frontend-1.prakticum-team.ru/signin")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        create_account_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Создать аккаунт"))
        )
        create_account_link.click()
        WebDriverWait(driver, 30).until(EC.url_contains("/signup"))

        registration_page.register(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password
        )

        time.sleep(2)

        driver.get("https://foodgram-frontend-1.prakticum-team.ru/signin")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.NAME, "email")))

        username = user.email.split('@')[0]
        login_page.login(username, user.password)
        time.sleep(2)

        try:
            alert = driver.switch_to.alert
            print(f">>> Алерт: {alert.text}")
            alert.accept()
            time.sleep(1)
        except:
            pass

        assert "/signin" not in driver.current_url, "Не удалось войти"

        # Переход на страницу создания рецепта
        main_page.go_to_create_recipe()
        WebDriverWait(driver, 30).until(EC.url_contains("/create"))
        print(">>> На странице создания рецепта")

        # Заполнение формы
        create_recipe_page.fill_recipe(
            name=recipe.name,
            ingredient_name="картофель",
            ingredient_amount=5,
            description=recipe.description,
            cooking_time=recipe.time,
            image_path='/app/test.jpg'
        )

        # Ждём, что URL перестал содержать "/create" (редирект на страницу рецепта)
        WebDriverWait(driver, 60).until(
            lambda d: "/create" not in d.current_url
        )
        print(f">>> URL после создания: {driver.current_url}")
        print(">>> HTML страницы рецепта (первые 5000 символов):")
        print(driver.page_source[:5000])

        # Проверяем появление карточки с названием рецепта, пробуем разные варианты
        recipe_found = False
        # Вариант 1: заголовок h1
        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, f"//h1[contains(text(),'{recipe.name}')]"))
            )
            print(">>> Название найдено в h1")
            recipe_found = True
        except:
            pass

        if not recipe_found:
            # Вариант 2: заголовок h2
            try:
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, f"//h2[contains(text(),'{recipe.name}')]"))
                )
                print(">>> Название найдено в h2")
                recipe_found = True
            except:
                pass

        if not recipe_found:
            # Вариант 3: любой элемент с текстом
            recipe_card = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(),'{recipe.name}')]"))
            )
            print(">>> Название найдено по общему XPath")
            recipe_found = True

        assert recipe_found, f"Карточка рецепта с названием '{recipe.name}' не найдена"
        print(">>> Тест создания рецепта пройден!")