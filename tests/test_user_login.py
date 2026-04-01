import allure
from helpers import ApiRequests

@allure.suite("API: Логин пользователя")
class TestUserLogin: # тесты для входа пользователя
    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user(self, created_user): # Используем фикстуру для создания пользователя
        user_data, _ = created_user # Получаем данные пользователя из фикстуры
        payload = {"email": user_data["email"], "password": user_data["password"]} # Используем email и пароль из данных пользователя
        response = ApiRequests.login_user(payload) # Отправка POST-запроса на авторизацию с валидными данными
        assert response.status_code == 200 # Проверяем, что статус код 200
        assert response.json()["success"] is True # Проверяем, что в ответе есть ключ "success" со значением True

    @allure.title("Вход с неверным логином и паролем")
    def test_login_invalid_credentials(self): # Тестируем вход с неверными данными
        payload = {"email": "wrong_email@test.ru", "password": "wrong_password"} # Используем неверные email и пароль
        response = ApiRequests.login_user(payload) # Отправка POST-запроса на авторизацию с невалидными данными
        assert response.status_code == 401 # Проверяем, что статус код 401 Unauthorized
        assert response.json()["success"] is False  # Проверяем, что в ответе есть ключ "success" со значением False