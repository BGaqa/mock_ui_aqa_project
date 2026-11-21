import re

import allure
from playwright.sync_api import Page

from config import Config
from pages.base_page import BasePage
from pages.store.components.product_card import ProductCard
from utils.url_helper import build_url


class CatalogPage(BasePage):
    URL = Config.BASE_FRONT_URL_UI

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Шапка магазина
        self.logo = page.get_by_test_id("shop-header-logo")

        # Счётчик найденных товаров и контейнер пагинации
        self.results_count = page.get_by_test_id("catalog-results-count")
        self.pagination = page.get_by_test_id("catalog-pagination")

        # Кнопки страниц, у кнопок "назад"/"вперёд" текста нет (только svg)
        self.pagination_pages = self.pagination.get_by_role("button").filter(has_text=re.compile(r"^\d+$"))

        # Все карточки товаров на текущей странице каталога
        self.cards = page.get_by_test_id("product-card")

        # Поиск по названию и бренду
        self.search_input = page.get_by_test_id("catalog-search-input")

        # Пустое состояние, блок «Ничего не найдено» и кнопка сброса внутри него
        self.empty_state = page.get_by_test_id("catalog-empty")
        self.empty_reset_button = page.get_by_test_id("catalog-empty-reset-button")

    @allure.step("Открыть каталог магазина")
    def open(self) -> None:
        # reset=1 — чистое состояние площадки (пустая корзина, 24 товара)
        # delay=0 — убираем искусственную задержку каталога, она здесь не проверяется
        self.page.goto(build_url(self.URL, reset=1, delay=0))

    def first_card(self) -> ProductCard:
        """Возвращает первую карточку каталога в порядке сортировки по умолчанию."""
        # nth(0) здесь уместен, мы проверяем именно порядок по умолчанию
        # Для поиска конкретного товара будем использовать data-product-id, а не индекс
        return ProductCard(self.cards.nth(0))

    @allure.step("Ввести в поиск: {text}")
    def search(self, text: str) -> None:
        # fill() заменяет содержимое поля целиком, поэтому очистка перед вводом не нужна
        # пустая строка вернёт каталог к полному списку
        self.search_input.fill(text)

    @allure.step("Сбросить фильтры из пустого состояния")
    def reset_filters_from_empty(self) -> None:
        # Кнопка живёт внутри блока catalog-empty и доступна только при нулевом результате
        self.empty_reset_button.click()
