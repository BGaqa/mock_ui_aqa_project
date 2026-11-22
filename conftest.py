import re

import pytest
from playwright.sync_api import Page, expect

from pages.store.cart_page import CartPage
from pages.store.catalog_page import CatalogPage
from pages.store.checkout_page import CheckoutPage
from pages.store.order_page import OrderPage
from pages.store.orders_page import OrdersPage
from pages.store.product_page import ProductPage


@pytest.fixture
def catalog_page(page: Page) -> CatalogPage:
    return CatalogPage(page)


@pytest.fixture
def product_page(page: Page) -> ProductPage:
    return ProductPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest.fixture
def cart_default(catalog_page: CatalogPage, cart_page: CartPage) -> CartPage:
    catalog_page.open()
    catalog_page.add_product("Перфоратор", times=2)
    catalog_page.add_product("Рулетка")
    catalog_page.header.open_cart()
    return cart_page


@pytest.fixture
def cart_small(catalog_page: CatalogPage, cart_page: CartPage) -> CartPage:
    catalog_page.open()
    catalog_page.add_product("Рулетка")
    catalog_page.header.open_cart()
    return cart_page


@pytest.fixture
def cart_with_two_products(catalog_page: CatalogPage, cart_page: CartPage) -> CartPage:
    catalog_page.open()
    catalog_page.add_product("Перфоратор")
    catalog_page.add_product("Рулетка")
    catalog_page.header.open_cart()
    return cart_page


@pytest.fixture
def checkout_delivery_step(cart_small: CartPage, checkout_page: CheckoutPage) -> CheckoutPage:
    cart_small.go_to_checkout()
    checkout_page.fill_contacts("Вадим", "vadim@example.com", "+7 900 123-45-67")
    checkout_page.next_step()
    expect(checkout_page.stepper).to_have_attribute("data-active-step", "1")
    return checkout_page


@pytest.fixture
def order_page(page: Page) -> OrderPage:
    return OrderPage(page)


@pytest.fixture
def checkout_payment_step(cart_default: CartPage, checkout_page: CheckoutPage) -> CheckoutPage:
    cart_default.go_to_checkout()
    checkout_page.fill_contacts("Вадим", "vadim@example.com", "+7 900 123-45-67")
    checkout_page.next_step()
    # Самовывоз не требует адреса, поэтому со шага доставки проходим сразу
    checkout_page.select_pickup()
    checkout_page.next_step()
    # Гарантируем, что тест стартует именно со шага оплаты
    expect(checkout_page.stepper).to_have_attribute("data-active-step", "2")
    return checkout_page


@pytest.fixture
def orders_page(page: Page) -> OrdersPage:
    return OrdersPage(page)


def _place_order(catalog_page: CatalogPage, cart_page: CartPage, checkout_page: CheckoutPage, by_card: bool) -> None:
    """Оформляет один заказ самовывозом: картой или наличными.
    Без reset, чтобы не стереть уже оформленные заказы."""
    catalog_page.open(reset=False)
    catalog_page.add_product("Перфоратор", times=2)
    catalog_page.add_product("Рулетка")
    catalog_page.header.open_cart()
    cart_page.go_to_checkout()
    checkout_page.fill_contacts("Вадим", "vadim@example.com", "+7 900 123-45-67")
    checkout_page.next_step()
    checkout_page.select_pickup()
    checkout_page.next_step()
    if by_card:
        checkout_page.fill_card("4111111111111111", "1229", "123", "IVAN IVANOV")
    else:
        checkout_page.select_cash()
    checkout_page.pay()
    # Дожидаемся страницы заказа, заказ попадает в localStorage только после
    # перехода. Без этого ожидания следующая навигация обрывает запись,
    # и в списке заказов не хватает строки
    expect(checkout_page.page).to_have_url(re.compile(r"/store/order\?.*number=ORD-"))


@pytest.fixture
def two_orders(
    orders_page: OrdersPage,
    catalog_page: CatalogPage,
    cart_page: CartPage,
    checkout_page: CheckoutPage,
) -> OrdersPage:
    """Два заказа в чистом браузере: ORD-1001 картой, ORD-1002 наличными.
    Возвращает открытый список заказов."""
    orders_page.open()
    _place_order(catalog_page, cart_page, checkout_page, by_card=True)
    _place_order(catalog_page, cart_page, checkout_page, by_card=False)
    checkout_page.header.open_orders()
    return orders_page
