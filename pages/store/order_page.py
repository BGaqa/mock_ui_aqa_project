from playwright.sync_api import Page

from pages.store.base_store_page import BaseStorePage


class OrderPage(BaseStorePage):
    """Страница заказа после успешного оформления."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Контейнер заказа, несёт его номер в data-order-number
        self.root = page.get_by_test_id("order-page")

        # Заголовок с номером и статус оплаты
        self.number = page.get_by_test_id("order-number")
        self.status = page.get_by_test_id("order-status")

        # Итог заказа и способы доставки/оплаты
        self.summary_total = page.get_by_test_id("order-summary-total")
        self.delivery = page.get_by_test_id("order-delivery")
        self.payment = page.get_by_test_id("order-payment")

        # Зелёный блок успеха с контактами покупателя
        self.success_block = page.get_by_test_id("order-success")
