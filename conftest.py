import pytest
import requests
import random
import string

BASE_URL = "https://stellarburgers.education-services.ru"

def generate_random_string(length=8): # Генерация случайной строки для уникальных данных
    return ''.join(random.choices(string.ascii_lowercase, k=length)) # Генерация случайной строки для уникальных данных

@pytest.fixture
def user_data():
    return {
        "email": f"{generate_random_string()}@ya.ru",
        "password": "password123",
        "name": generate_random_string()
    } # Генерация уникальных данных пользователя для тестов

@pytest.fixture
def created_user(user_data): # Фикстура для создания пользователя и получения токена доступа
    response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data) # Создание пользователя через API
    token = response.json().get("accessToken") # Получение токена доступа из ответа при регистрации
    yield user_data, token # Передача данных пользователя и токена в тесты
    if token: # Удаление пользователя после тестов для очистки данных
        requests.delete(f"{BASE_URL}/api/auth/user", headers={"Authorization": token}) # Удаление пользователя через API с использованием токена доступа