import allure
from playwright.sync_api import Page

from pages.store.base_store_page import BaseStorePage
from pages.store.components.cart_row import CartRow


class CartPage(BaseStorePage):
    """Страница корзины: строки товаров и блок итогов."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Все строки корзины и блок итогов
        self.rows = page.get_by_test_id("cart-row")
        self.subtotal = page.get_by_test_id("cart-summary-subtotal")
        self.delivery = page.get_by_test_id("cart-summary-delivery")
        self.total = page.get_by_test_id("cart-summary-total")

        # Промокод, поле ввода, кнопка применения и ошибка под полем
        self.promo_input = page.get_by_test_id("cart-promo-input")
        self.promo_apply_button = page.get_by_test_id("cart-promo-apply-button")
        self.promo_error = page.get_by_test_id("cart-promo-error")

        # Чип применённого промокода и крестик удаления на нём
        self.promo_chip = page.get_by_test_id("cart-promo-applied")
        self.promo_remove_button = page.get_by_test_id("cart-promo-remove-button")

        # Строка скидки в итогах: появляется только с процентным или фиксированным кодом
        self.discount = page.get_by_test_id("cart-summary-discount")

    @allure.step("Открыть корзину")
    def open(self, reset: bool = True) -> None:
        self.open_path("cart", reset=reset)

    def row(self, product_id: int) -> CartRow:
        """Строка корзины по id товара."""
        # Ищем по связке testid + data-product-id строки различаются товаром,
        # а не порядком, поэтому индекс здесь не нужен
        return CartRow(self.page.locator(f'[data-testid="cart-row"][data-product-id="{product_id}"]'))

    @allure.step("Применить промокод: {code}")
    def apply_promo(self, code: str) -> None:
        self.promo_input.fill(code)
        self.promo_apply_button.click()

    @allure.step("Удалить применённый промокод")
    def remove_promo(self) -> None:
        self.promo_remove_button.click()
