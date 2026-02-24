# Sprint 9 review
from selenium.webdriver.common.by import By
import pytest
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.create_recipe_page import CreateRecipePage
from data import TEST_IMAGE

class TestCreateRecipe:
    def test_create_recipe(self, driver, user, recipe, login_page, main_page, create_recipe_page):
        # Авторизация
        driver.get("https://foodgram.example.com/login")
        login_page.login(user.email, user.password)
        main_page.go_to_create_recipe()
        # Создание рецепта
        create_recipe_page.fill_recipe(
            name=recipe.name,
            ingredient_text=recipe.ingredient,
            description=recipe.description,
            time=recipe.time,
            image_path=TEST_IMAGE
        )
        # Проверка: на главной должна появиться карточка с названием рецепта
        recipe_card = driver.find_element(By.XPATH, f"//div[contains(text(),'{recipe.name}')]")
        assert recipe_card.is_displayed(), "Карточка рецепта не отображается"