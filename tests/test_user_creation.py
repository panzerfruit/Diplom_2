import requests
import allure
from conftest import BASE_URL

@allure.suite("API: Создание пользователя")
class TestUserCreation: # Тестовый класс для проверки создания пользователя через API
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, user_data): # Тест для создания уникального пользователя с помощью данных из фикстуры
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data) # Отправка POST-запроса на создание пользователя с данными из фикстуры
        assert response.status_code == 200 # Проверка, что статус код ответа 200 (успешное создание пользователя)
        assert response.json()["success"] is True # Проверка, что в ответе указано, что операция успешна

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, created_user): # Тест для проверки создания пользователя с данными уже зарегистрированного пользователя
        user_data, _ = created_user # Получение данных уже зарегистрированного пользователя из фикстуры
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data) # Отправка POST-запроса на создание пользователя с данными уже зарегистрированного пользователя
        assert response.status_code == 403 # Проверка, что статус код ответа 403 при попытке создать пользователя с уже существующими данными
        assert response.json()["message"] == "User already exists" # Проверка, что в ответе указано сообщение о том, что пользователь уже существует

    @allure.title("Создание пользователя без обязательного поля")
    def test_create_user_missing_field(self, user_data): # Тест для проверки создания пользователя без одного из обязательных полей (например, email)
        user_data.pop("email") # Удаление поля email из данных пользователя для проверки реакции API на отсутствие обязательного поля
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data) # Отправка POST-запроса на создание пользователя с неполными данными
        assert response.status_code == 403 # Проверка, что статус код ответа 403 при попытке создать пользователя с неполными данными
        assert response.json()["message"] == "Email, password and name are required fields" # Проверка, что в ответе указано сообщение о том, что email, password и name являются обязательными полями