import pytest
from playwright.sync_api import Page

from pages.store.catalog_page import CatalogPage
from pages.store.product_page import ProductPage


@pytest.fixture
def catalog_page(page: Page) -> CatalogPage:
    return CatalogPage(page)


@pytest.fixture
def product_page(page: Page) -> ProductPage:
    return ProductPage(page)
