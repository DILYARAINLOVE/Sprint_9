from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.create_recipe_page import CreateRecipePage
from data import TEST_IMAGE

class TestCreateRecipe:
    def test_create_recipe(self, driver, user, recipe, login_page, main_page, create_recipe_page):
        driver.get("https://foodgram-frontend-1.prakticum-team.ru/login")

        # Ждём загрузки страницы логина
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        login_page.login(user.email, user.password)

        # После логина ждём загрузки главной страницы
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        main_page.go_to_create_recipe()

        create_recipe_page.fill_recipe(
            name=recipe.name,
            ingredient_text=recipe.ingredient,
            description=recipe.description,
            time=recipe.time,
            image_path=TEST_IMAGE
        )

        # После создания рецепта ожидаем появления карточки с названием на главной
        recipe_card = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, f"//div[contains(text(),'{recipe.name}')]"))
        )
        assert recipe_card.is_displayed(), "Карточка рецепта не отображается"