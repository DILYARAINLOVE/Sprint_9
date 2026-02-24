# Sprint 9 review
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from data import User, Recipe

from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.create_recipe_page import CreateRecipePage

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--remote", action="store_true", help="Run tests in Selenoid")
    parser.addoption("--selenoid_url", action="store", default="http://localhost:4444/wd/hub")

@pytest.fixture
def driver(request):
    remote = request.config.getoption("--remote")
    selenoid_url = request.config.getoption("--selenoid_url")

    try:
        if remote:
            options = Options()
            options.set_capability("browserVersion", "128.0")
            options.set_capability("selenoid:options", {
                "enableVNC": True,
                "enableVideo": False
            })
            driver = webdriver.Remote(command_executor=selenoid_url, options=options)
        else:
            service = Service()
            options = Options()
            # Базовые флаги для обхода типичных проблем
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--disable-web-security")
            options.add_argument("--disable-features=VizDisplayCompositor")
            options.add_argument("--no-proxy-server")
            # Если сайт требует реального User-Agent
            options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            driver = webdriver.Chrome(service=service, options=options)

        driver.maximize_window()
        driver.get("https://foodgram-frontend-1.prakticum-team.ru")
        yield driver
        driver.quit()
    except WebDriverException as e:
        pytest.fail(f"Failed to create driver: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")

@pytest.fixture
def user():
    return User()

@pytest.fixture
def recipe():
    return Recipe()

@pytest.fixture
def registration_page(driver):
    return RegistrationPage(driver)

@pytest.fixture
def login_page(driver):
    return LoginPage(driver)

@pytest.fixture
def main_page(driver):
    return MainPage(driver)

@pytest.fixture
def create_recipe_page(driver):
    return CreateRecipePage(driver)
