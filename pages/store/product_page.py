import allure
from playwright.sync_api import Locator, Page

from config import Config
from pages.base_page import BasePage
from utils.url_helper import build_url


class ProductPage(BasePage):
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

    @allure.step("Открыть страницу товара {product_id} напрямую")
    def open_by_id(self, product_id: int) -> None:
        # Отдельный метод, а не переопределение open()
        # у BasePage.open() нет аргументов, mypy не примет другую сигнатуру
        self.page.goto(build_url(self.URL, f"product/{product_id}", reset=1, delay=0))

    def spec_row(self, spec_name: str) -> Locator:
        """Строка характеристики по её названию, например «Мощность»."""
        # Отдельных testid у названия и значения нет, работаем со строкой целиком
        return self.spec_rows.filter(has_text=spec_name)
