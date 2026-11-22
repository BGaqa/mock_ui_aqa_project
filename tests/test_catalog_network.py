import allure
import pytest
from playwright.sync_api import expect

from pages.store.catalog_page import CatalogPage

# Единственный сетевой запрос магазина, его и перехватываем
PRODUCTS_URL = "**/mock/store/products.json"


@allure.title("Загрузка: скелетоны и счётчик без data-count, затем 8 карточек")
@pytest.mark.frontend
def test_loading_state_then_cards(catalog_page: CatalogPage) -> None:
    # Открываем БЕЗ флагов, дефолтные 600 мс задержки дают окно, чтобы поймать скелетоны
    catalog_page.open_with_flags()

    # Пока запрос идёт: скелетоны видны, счётчик в состоянии загрузки и без data-count
    expect(catalog_page.loading).to_be_visible()
    expect(catalog_page.results_count).to_have_text("Загружаем каталог…")
    assert catalog_page.results_count.get_attribute("data-count") is None

    # После загрузки скелетоны исчезают, первая страница из 8 карточек
    expect(catalog_page.loading).not_to_be_visible()
    expect(catalog_page.cards).to_have_count(8)


@allure.title("Ошибка 500: блок ошибки, повтор без перехвата возвращает каталог")
@pytest.mark.frontend
def test_error_500_then_retry_restores(catalog_page: CatalogPage) -> None:
    page = catalog_page.page
    # Подменяем ответ каталога на 500 ДО открытия страницы
    page.route(PRODUCTS_URL, lambda route: route.fulfill(status=500, body="Internal Server Error"))
    catalog_page.open()

    # Красный блок ошибки с кодом и кнопкой повтора, карточек нет
    expect(catalog_page.error).to_contain_text("Не удалось загрузить каталог (500)")
    expect(catalog_page.retry_button).to_be_visible()
    expect(catalog_page.cards).to_have_count(0)

    # Снимаем перехват и жмём повтор, приходит настоящий ответ, 24 товара
    page.unroute(PRODUCTS_URL)
    catalog_page.retry()
    expect(catalog_page.results_count).to_have_text("Найдено: 24")
    expect(catalog_page.cards).to_have_count(8)


@allure.title("Пустой ответ: пустое состояние и нулевой счётчик")
@pytest.mark.frontend
def test_empty_response_shows_empty_state(catalog_page: CatalogPage) -> None:
    page = catalog_page.page
    # Каталог возвращает пустой массив товаров нет, но это не ошибка сети
    page.route(PRODUCTS_URL, lambda route: route.fulfill(status=200, content_type="application/json", body="[]"))
    catalog_page.open()

    expect(catalog_page.empty_state).to_contain_text("Ничего не найдено. Попробуйте изменить фильтры")
    expect(catalog_page.results_count).to_have_text("Найдено: 0")

    # Снимаем перехват и перезагружаем, в пустом состоянии кнопки «Повторить» нет
    page.unroute(PRODUCTS_URL)
    page.reload()
    expect(catalog_page.results_count).to_have_text("Найдено: 24")


@allure.title("Контракт products.json: статус 200 и 24 товара с обязательными полями")
@pytest.mark.frontend
def test_products_json_contract(catalog_page: CatalogPage) -> None:
    page = catalog_page.page
    # Ловим ответ каталога вокруг обычной загрузки
    with page.expect_response(lambda r: "products.json" in r.url) as info:
        catalog_page.open()
    response = info.value

    assert response.status == 200
    products = response.json()
    assert isinstance(products, list)
    assert len(products) == 24

    # У каждого товара есть обязательные поля контракта
    for product in products:
        assert {"id", "name", "price", "stock"} <= product.keys()
