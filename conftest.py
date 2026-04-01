import pytest
from helpers import UserHelpers, ApiRequests

@pytest.fixture
def created_user(): # Фикстура, создающая и удаляющая тестового пользователя
    user_data = UserHelpers.generate_user_data() # Генерация данных нового пользователя
    response = ApiRequests.register_user(user_data) # Регистрация пользователя через API
    token = response.json().get("accessToken") # Извлечение accessToken из ответа
    yield user_data, token # Возврат данных и токена в тесты
    if token: # Проверка наличия токена перед удалением
        ApiRequests.delete_user(token) # Удаление созданного пользователя после завершения теста

@pytest.fixture
def cleanup_user(): # Фикстура для отложенного удаления пользователей
    tokens_to_delete = [] # Создание пустого списка для хранения токенов
    def _add_token(token): # Внутренняя функция для добавления токена в список
        if token: # Проверка, что токен существует
            tokens_to_delete.append(token) # Добавление токена в список на удаление
    yield _add_token # Возврат функции _add_token в тест
    for token in tokens_to_delete: # Перебор всех собранных токенов
        ApiRequests.delete_user(token) # Удаление каждого пользователя после завершения теста