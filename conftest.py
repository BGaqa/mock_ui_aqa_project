import pytest
from playwright.sync_api import Page, expect

from pages.store.cart_page import CartPage
from pages.store.catalog_page import CatalogPage
from pages.store.checkout_page import CheckoutPage
from pages.store.order_page import OrderPage
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
