import allure
from playwright.sync_api import Page

from pages.store.base_store_page import BaseStorePage
from pages.store.components.order_row import OrderRow


class OrdersPage(BaseStorePage):
    """Список заказов: новые сверху, хранится в localStorage."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Контейнер списка и пустое состояние с кнопкой в каталог
        self.root = page.get_by_test_id("orders-page")
        self.empty = page.get_by_test_id("orders-empty")
        self.empty_catalog_button = page.get_by_test_id("orders-empty-catalog-button")

        # Все строки заказов
        self.rows = page.get_by_test_id("order-row")

    @allure.step("Открыть список заказов")
    def open(self, reset: bool = True) -> None:
        self.open_path("orders", reset=reset)

    def row(self, number: str) -> OrderRow:
        """Строка заказа по его номеру."""
        # Строки различаются номером, а не позицией
        # порядок проверяем отдельно, поэтому здесь индекс не нужен
        return OrderRow(self.page.locator(f'[data-testid="order-row"][data-order-number="{number}"]'))
