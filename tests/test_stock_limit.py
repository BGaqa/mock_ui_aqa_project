import allure
import pytest
from playwright.sync_api import expect

from pages.store.catalog_page import CatalogPage
from pages.store.product_page import ProductPage


@allure.title("Лимит склада, пятый перфоратор не добавить ни с карточки, ни со страницы")
@pytest.mark.frontend
def test_stock_limit_blocks_fifth_add(catalog_page: CatalogPage, product_page: ProductPage) -> None:
    # Находим перфоратор и кладём в корзину 4 штуки, ровно столько, сколько на складе
    catalog_page.open()
    catalog_page.search("Перфоратор")
    expect(catalog_page.cards).to_have_count(1)
    card = catalog_page.first_card()

    # Четыре успешных добавления подряд цикл вместо четырёх одинаковых строк
    for _ in range(4):
        card.add_button.click()

    # Счётчик подтверждает, что все четыре добавления прошли
    expect(catalog_page.header.cart_badge).to_have_attribute("data-count", "4")

    # Пятое нажатие, склад не позволяет добавить больше
    card.add_button.click()

    # Прилетает красный тост с текстом про лимит
    # Severity зашит в сам локатор error_toasts, поэтому здесь проверяем только текст
    expect(catalog_page.error_toasts).to_contain_text("Больше 4 шт. нет в наличии")

    # Счётчик не сдвинулся, пятого товара в корзине нет
    expect(catalog_page.header.cart_badge).to_have_attribute("data-count", "4")

    # Открываем страницу перфоратора БЕЗ reset корзина живёт в localStorage
    product_page.open_by_id(8, reset=False)

    # На странице видно, сколько уже в корзине, и добавление заблокировано
    expect(product_page.in_cart).to_have_text("В корзине: 4")
    expect(product_page.add_button).to_be_disabled()
