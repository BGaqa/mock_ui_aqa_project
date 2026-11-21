import allure
from playwright.sync_api import Locator, Page

from config import Config
from pages.store.base_store_page import BaseStorePage


class ProductPage(BaseStorePage):
    # База магазина к ней добавляем путь product/{id}
    URL = Config.BASE_FRONT_URL_UI

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Контейнер страницы товара, несёт data-product-id открытого товара
        self.root = page.get_by_test_id("product-page")

        # Хлебные крошки и основная информация о товаре
        self.breadcrumbs = page.get_by_test_id("product-breadcrumbs")
        self.brand = page.get_by_test_id("product-brand")
        self.name = page.get_by_test_id("product-name")
        self.price = page.get_by_test_id("product-price")
        self.stock = page.get_by_test_id("product-stock")

        # Строки таблицы характеристик
        self.spec_rows = page.get_by_test_id("product-spec-row")

        # Состояние «Товар не найден» и кнопка возврата в каталог
        self.not_found = page.get_by_test_id("product-not-found")
        self.not_found_catalog_button = page.get_by_test_id("product-not-found-catalog-button")

        # Кнопка добавления в корзину и степпер количества
        self.add_button = page.get_by_test_id("product-add-button")
        self.qty_increment = page.get_by_test_id("product-qty-increment")
        self.qty_decrement = page.get_by_test_id("product-qty-decrement")
        self.qty_input = page.get_by_test_id("product-qty-input")

        # Подпись «В корзине: N» — появляется, если товар уже лежит в корзине
        self.in_cart = page.get_by_test_id("product-in-cart")

    @allure.step("Открыть страницу товара {product_id} напрямую")
    def open_by_id(self, product_id: int, reset: bool = True) -> None:
        # reset=False используем в сценариях с корзиной
        # полная перезагрузка без reset сохраняет корзину из localStorage
        self.open_path(f"product/{product_id}", reset=reset)

    def spec_row(self, spec_name: str) -> Locator:
        """Строка характеристики по её названию, например «Мощность»."""
        # Отдельных testid у названия и значения нет, работаем со строкой целиком
        return self.spec_rows.filter(has_text=spec_name)
