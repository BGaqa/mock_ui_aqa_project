import pytest
from playwright.sync_api import Page

from pages.store.cart_page import CartPage
from pages.store.catalog_page import CatalogPage
from pages.store.checkout_page import CheckoutPage
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
