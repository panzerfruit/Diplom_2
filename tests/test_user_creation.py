import pytest
import allure
from helpers import UserHelpers, ApiRequests
from constants import Messages

@allure.suite("API: Создание пользователя")
class TestUserCreation: # Тестовый класс для проверки создания пользователя через API
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, cleanup_user): # Создания уникального пользователя
        user_data = UserHelpers.generate_user_data() # Генерация случайных данных нового пользователя
        response = ApiRequests.register_user(user_data) # Отправка запроса на регистрацию пользователя
        assert response.status_code == 200 # Проверка, что статус код ответа 200 (успешное создание пользователя)
        assert response.json()["success"] is True # Проверка, что в ответе указано, что операция успешна
        cleanup_user(response.json().get("accessToken")) # Добавление токена в список для последующего удаления пользователя

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, created_user): # Тест для проверки создания пользователя с данными уже зарегистрированного пользователя
        user_data, _ = created_user # Получение данных уже зарегистрированного пользователя из фикстуры
        response = ApiRequests.register_user(user_data) # Отправка запроса на регистрацию пользователя с уже существующими данными
        assert response.status_code == 403 # Проверка, что статус код ответа 403 при попытке создать пользователя с уже существующими данными
        assert response.json()["message"] == Messages.USER_EXISTS

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"]) # Параметризация теста для трёх обязательных полей
    def test_create_user_missing_field(self, missing_field): # Создание пользователя без обязательного поля
        user_data = UserHelpers.generate_user_data() # Генерация случайных данных пользователя
        user_data.pop(missing_field) # Удаление одного обязательного поля из словаря
        response = ApiRequests.register_user(user_data) # Отправка запроса на регистрацию пользователя без одного обязательного поля
        assert response.status_code == 403 # Проверка, что статус код ответа 403 при попытке создать пользователя с неполными данными
        assert response.json()["message"] == Messages.MISSING_FIELDS # Проверка, что в ответе вернулось сообщение об отсутствующих полях