import allure
from playwright.sync_api import Page


class ShopHeader:
    """Статический page element: шапка магазина, общая для всех страниц."""

    def __init__(self, page: Page) -> None:
        # Кнопка корзины и счётчик товаров на ней
        self.cart_button = page.get_by_test_id("shop-header-cart-button")
        self.cart_badge = page.get_by_test_id("shop-header-cart-badge")

    @allure.step("Перейти в корзину по иконке в шапке")
    def open_cart(self) -> None:
        self.cart_button.click()
