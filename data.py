import random
import string
from pathlib import Path

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / 'assets'
TEST_IMAGE = ASSETS_DIR / 'recipe.jpg'

class User:
    def __init__(self, first_name=None, last_name=None, email=None, password=None):
        self.first_name = first_name or f"Test{random_string(5)}"
        self.last_name = last_name or f"User{random_string(5)}"
        self.email = email or f"{random_string(10)}@example.com"
        self.password = password or random_string(10)

class Recipe:
    def __init__(self, name=None, ingredient=None, description=None, time=None):
        self.name = name or f"Recipe {random_string(6)}"
        self.ingredient = ingredient or "tomato"
        self.description = description or "Test description"
        self.time = time or "30"
