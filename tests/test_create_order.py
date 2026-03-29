import requests
import allure
from conftest import BASE_URL

@allure.suite("API: Создание заказа")
class TestCreateOrder: # тесты для создания заказа
    def get_ingredient_hash(self): # метод для получения хеша ингредиента
        res = requests.get(f"{BASE_URL}/api/ingredients") # отправляем GET запрос для получения списка ингредиентов
        return res.json()["data"][0]["_id"] # возвращаем хеш первого ингредиента из списка

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth(self, created_user): # тест для создания заказа с авторизацией и ингредиентами
        _, token = created_user # получаем токен из фикстуры created_user
        ingredient = self.get_ingredient_hash() # получаем хеш ингредиента
        headers = {"Authorization": token} # создаем заголовки с токеном авторизации
        payload = {"ingredients": [ingredient]} # создаем полезную нагрузку с хешем ингредиента
        response = requests.post(f"{BASE_URL}/api/orders", headers=headers, json=payload) # отправляем POST запрос для создания заказа
        assert response.status_code == 200 # проверяем, что статус код ответа 200
        assert response.json()["success"] is True # проверяем, что в ответе есть поле success со значением True

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self): # тест для создания заказа без авторизации
        payload = {"ingredients": ["61c0c5a71d1f82001bda4651"]} # создаем полезную нагрузку с хешем ингредиента
        response = requests.post(f"{BASE_URL}/api/orders", json=payload) # отправляем POST запрос для создания заказа без заголовков авторизации
        assert response.status_code == 401 or response.json()["success"] is False # проверяем, что статус код ответа 401 или в ответе есть поле success со значением False

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self): # тест для создания заказа без ингредиентов
        response = requests.post(f"{BASE_URL}/api/orders", json={"ingredients": []}) # отправляем POST запрос для создания заказа с пустым списком ингредиентов
        assert response.status_code == 400 # проверяем, что статус код ответа 400
        assert response.json()["message"] == "Ingredient ids must be provided" # проверяем, что в ответе есть сообщение об ошибке

    @allure.title("Создание заказа с неверным хешем")
    def test_create_order_invalid_hash(self): # тест для создания заказа с неверным хешем ингредиента
        payload = {"ingredients": ["invalid_hash_123"]} # создаем полезную нагрузку с неверным хешем ингредиента
        response = requests.post(f"{BASE_URL}/api/orders", json=payload) # отправляем POST запрос для создания заказа
        assert response.status_code == 500 # проверяем, что статус код ответа 500