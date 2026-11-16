import allure
import pytest
from playwright.sync_api import expect

from pages.store.catalog_page import CatalogPage


@allure.title("Смок, каталог открывается и показывает 24 товара")
@pytest.mark.frontend
@pytest.mark.smoke
def test_catalog_opens(catalog_page: CatalogPage) -> None:
    # Открываем каталог
    catalog_page.open()

    # В шапке есть логотип с названием магазина
    expect(catalog_page.logo).to_contain_text("Инструмент Маркет")

    # Счётчик результатов, проверяем и текст, и data-атрибут
    expect(catalog_page.results_count).to_have_text("Найдено: 24")
    expect(catalog_page.results_count).to_have_attribute("data-count", "24")

    # На странице ровно 8 карточек (24 товара на 3 страницы).
    # Этот expect сам дожидается окончания загрузки каталога, отдельный wait не нужен
    expect(catalog_page.cards).to_have_count(8)

    # Пагинация видна и содержит 3 страницы
    expect(catalog_page.pagination).to_be_visible()
    expect(catalog_page.pagination_pages).to_have_count(3)

    # Первая карточка в порядке по умолчанию to_have_text нормализует пробелы,
    # поэтому в ожидаемом значении пишем обычный пробел
    first_card = catalog_page.first_card()
    expect(first_card.name).to_have_text("Набор гаечных ключей 8–22 мм")
    expect(first_card.price).to_have_text("2 490 ₽")
