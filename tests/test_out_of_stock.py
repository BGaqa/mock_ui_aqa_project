import allure
import pytest
from playwright.sync_api import expect

from pages.store.catalog_page import CatalogPage
from pages.store.product_page import ProductPage


@allure.title("Товар без остатка: в корзину нельзя ни с карточки, ни со страницы")
@pytest.mark.frontend
def test_out_of_stock_product_unavailable(catalog_page: CatalogPage, product_page: ProductPage) -> None:
    # Через поиск находим единственный товар без остатка электрический лобзик
    catalog_page.open()
    catalog_page.search("Лобзик")
    expect(catalog_page.cards).to_have_count(1)

    # Чип остатка говорит об отсутствии товара
    # и несёт data-stock="0" проверяем и текст, и атрибут
    card = catalog_page.first_card()
    expect(card.stock).to_have_text("Нет в наличии")
    expect(card.stock).to_have_attribute("data-stock", "0")

    # Кнопка добавления неактивна, интерфейс блокирует заказ заранее
    expect(card.add_button).to_be_disabled()

    # Открываем страницу товара из карточки и убеждаемся, что это именно лобзик
    # по справочным данным площадки его id равен 10
    card.open()
    expect(product_page.root).to_have_attribute("data-product-id", "10")

    # Страница товара, кнопка добавления и обе кнопки степпера неактивны,
    # то есть количество нельзя ни увеличить, ни уменьшить
    expect(product_page.add_button).to_be_disabled()
    expect(product_page.qty_increment).to_be_disabled()
    expect(product_page.qty_decrement).to_be_disabled()

    # Поле количества осталось со значением по умолчанию
    # to_have_value смотрит value инпута, а не видимый текст
    expect(product_page.qty_input).to_have_value("1")
