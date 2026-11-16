import pytest
from playwright.sync_api import Page

from pages.store.catalog_page import CatalogPage


@pytest.fixture
def catalog_page(page: Page) -> CatalogPage:
    return CatalogPage(page)
