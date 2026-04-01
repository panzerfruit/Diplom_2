import allure
from helpers import ApiRequests
from constants import Messages

@allure.suite("API: Создание заказа")
class TestCreateOrder: # тесты для создания заказа
    def get_ingredient_hash(self): # метод для получения хеша ингредиента
        res = ApiRequests.get_ingredients() # Выполнение GET-запроса для получения полного списка ингредиентов
        return res.json()["data"][0]["_id"] # возвращаем хеш первого ингредиента из списка

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth(self, created_user): # тест для создания заказа с авторизацией и ингредиентами
        _, token = created_user # получаем токен из фикстуры created_user
        ingredient = self.get_ingredient_hash() # получаем хеш ингредиента
        payload = {"ingredients": [ingredient]} # создаем полезную нагрузку с хешем ингредиента
        response = ApiRequests.create_order(payload, token)
        assert response.status_code == 200 # получаем статус код ответа 200
        assert response.json()["success"] is True # проверяем, что в ответе есть поле success со значением True

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self): # тест для создания заказа без авторизации
        ingredient = self.get_ingredient_hash() # Вызов метода для получения хеша ингредиента
        payload = {"ingredients": [ingredient]} # Формирование тела запроса с одним ингредиентом
        response = ApiRequests.create_order(payload) # Отправка POST-запроса на создание заказа без токена (без авторизации)
        assert response.status_code == 200 # получаем статус код ответа 200
        assert response.json()["success"] is True # получаем, что в ответе есть поле success со значением True
        assert "order" in response.json() # Проверяем, что в JSON-ответе присутствует ключ "order" с данными созданного заказа

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self): # тест для создания заказа без ингредиентов
        response = ApiRequests.create_order({"ingredients": []}) # Отправка POST-запроса с пустым массивом ингредиентов
        assert response.status_code == 400 # проверяем, что статус код ответа 400
        assert response.json()["message"] == Messages.INGREDIENTS_REQUIRED # проверяем, что в ответе есть сообщение об ошибке

    @allure.title("Создание заказа с неверным хешем")
    def test_create_order_invalid_hash(self): # тест для создания заказа с неверным хешем ингредиента
        payload = {"ingredients": ["invalid_hash_123"]} # создаем полезную нагрузку с неверным хешем ингредиента
        response = ApiRequests.create_order(payload) # Отправка POST-запроса на создание заказа с некорректным хешем
        assert response.status_code == 500 # проверяем, что статус код ответа 500