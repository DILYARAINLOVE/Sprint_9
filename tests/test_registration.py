import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

class TestRegistration:
    def test_successful_registration(self, driver, user, registration_page, login_page):
        print("\n=== НАЧАЛО ТЕСТА РЕГИСТРАЦИИ ===")
        sys.stdout.flush()

        # 1. Переход на страницу входа
        print("1. Переходим на страницу входа")
        driver.get("https://foodgram-frontend-1.prakticum-team.ru/signin")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("   ✅ Страница входа загружена")
        sys.stdout.flush()

        # 2. Клик по ссылке "Создать аккаунт"
        print("2. Ищем ссылку 'Создать аккаунт'")
        try:
            create_account_link = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Создать аккаунт"))
            )
            print("   ✅ Ссылка найдена по тексту")
        except:
            create_account_link = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/signup']"))
            )
            print("   ✅ Ссылка найдена по href='/signup'")
        create_account_link.click()
        print("   ✅ Клик выполнен")
        sys.stdout.flush()

        # 3. Проверка URL после клика
        WebDriverWait(driver, 10).until(EC.url_contains("/signup"))
        current_url = driver.current_url
        print(f"3. Текущий URL после клика: {current_url}")
        if "/signup" not in current_url:
            pytest.fail("❌ Переход на страницу регистрации не произошёл")
        sys.stdout.flush()

        # 4. Ожидание появления поля имени
        print("4. Ожидаем появление поля имени (форма регистрации)")
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#root > div > main > div > form > div:nth-child(3) > label > input"))
            )
            print("   ✅ Поле имени найдено по CSS-селектору")
        except Exception as e:
            print(f"   ❌ Поле имени не найдено: {e}")
            print("   HTML страницы в момент ошибки:")
            print(driver.page_source[:2000])
            pytest.fail("Страница регистрации не содержит поле имени")
        sys.stdout.flush()

        # 5. Вызов Page Object
        print("5. Вызываем registration_page.register()")
        sys.stdout.flush()
        try:
            registration_page.register(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                password=user.password
            )
            print("   ✅ Метод register отработал без исключений")
        except Exception as e:
            print(f"   ❌ Ошибка в registration_page.register: {e}")
            print(f"   Текущий URL: {driver.current_url}")
            pytest.fail("Регистрация не выполнена")
        sys.stdout.flush()

        # 6. Ожидание редиректа на страницу входа
        print("6. Ожидаем редирект на страницу входа и появление поля email")
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            print("   ✅ Поле email появилось на странице входа")
        except Exception as e:
            print(f"   ❌ Поле email не появилось: {e}")
            print(f"   Текущий URL: {driver.current_url}")
            pytest.fail("Редирект на страницу входа не произошёл")
        sys.stdout.flush()

        # 7. Финальная проверка
        print("7. Проверяем login_page.is_login_form_displayed()")
        try:
            assert login_page.is_login_form_displayed(), "Форма логина не отображается"
            print("   ✅ Тест пройден успешно!")
        except AssertionError as e:
            print(f"   ❌ {e}")
            pytest.fail("Форма логина не отображается после регистрации")
        sys.stdout.flush()