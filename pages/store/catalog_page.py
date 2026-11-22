import re

import allure
from playwright.sync_api import Locator, Page, expect

from config import Config
from pages.store.base_store_page import BaseStorePage
from pages.store.components.product_card import ProductCard


class CatalogPage(BaseStorePage):
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

        # Фильтры, переключатель наличия, селект сортировки и кнопка сброса
        self.in_stock_switch = page.get_by_test_id("catalog-instock-switch")
        self.sort_select = page.get_by_test_id("catalog-sort-select")
        self.reset_button = page.get_by_test_id("catalog-reset-button")

        # Активная кнопка страницы
        self.active_page = self.pagination.locator("button[aria-current='page']")

        # Состояния загрузки каталога, скелетоны, блок ошибки и кнопка повтора
        self.loading = page.get_by_test_id("catalog-loading")
        self.error = page.get_by_test_id("catalog-error")
        self.retry_button = page.get_by_test_id("catalog-retry-button")

    @allure.step("Открыть каталог магазина")
    def open(self, reset: bool = True) -> None:
        self.open_path(reset=reset)

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

    def category_checkbox(self, category: str) -> Locator:
        """Чекбокс категории по её data-category (power, protection и т.д.)."""
        # Категории различаются data-атрибутом, а не порядком в списке
        # поэтому ищем по связке testid + data-category
        return self.page.locator(f'[data-testid="catalog-category-checkbox"][data-category="{category}"]')

    @allure.step("Отметить категорию: {category}")
    def select_category(self, category: str) -> None:
        self.category_checkbox(category).check()

    @allure.step("Установить «Только в наличии»: {enabled}")
    def set_in_stock(self, enabled: bool) -> None:
        # set_checked приводит контрол к нужному состоянию
        # в отличие от click не зависит от того, включён он сейчас или нет
        self.in_stock_switch.set_checked(enabled)

    @allure.step("Выбрать сортировку: {value}")
    def select_sort(self, value: str) -> None:
        # MUI Select не нативный <select>, поэтому select_option не подходит
        # сначала открываем список, затем кликаем пункт
        # Опции рендерятся в портале в конце body, поэтому ищем от page, а не от sort_select
        self.sort_select.click()
        self.page.locator(f'[data-testid="catalog-sort-option"][data-value="{value}"]').click()

    @allure.step("Сбросить фильтры")
    def reset_filters(self) -> None:
        self.reset_button.click()

    def all_cards(self) -> list[ProductCard]:
        """Все карточки текущей страницы как компоненты."""
        # all() не ждёт появления элементов, вызывать после expect(...).to_have_count(...)
        return [ProductCard(root) for root in self.cards.all()]

    def card_ids(self) -> list[str]:
        """Собирает data-product-id всех карточек текущей страницы."""
        # all() не ждёт появления элементов, вызывать после expect(...).to_have_count(...)
        product_ids: list[str] = []
        for card in self.cards.all():
            product_id = card.get_attribute("data-product-id")
            # get_attribute возвращает str | None; assert отсекает None для mypy
            assert product_id is not None
            product_ids.append(product_id)
        return product_ids

    @allure.step("Перейти на страницу каталога: {number}")
    def go_to_page(self, number: int) -> None:
        # pagination_pages уже отфильтрован по тексту-цифре
        # дополнительный фильтр выбирает кнопку с точным номером
        self.pagination_pages.filter(has_text=re.compile(rf"^{number}$")).click()

    @allure.step("Добавить в корзину товар: {title} × {times}")
    def add_product(self, title: str, times: int = 1) -> None:
        # Поиск сужает выдачу до одной карточки ждём это ДО клика
        # иначе клик может попасть в карточку из старой выдачи
        # expect внутри page object здесь уместен: это не проверка результата,
        # а внутренняя синхронизация метода перед действием
        self.search(title)
        expect(self.cards).to_have_count(1)
        for _ in range(times):
            self.first_card().add_button.click()

    @allure.step("Повторить загрузку каталога")
    def retry(self) -> None:
        self.retry_button.click()
