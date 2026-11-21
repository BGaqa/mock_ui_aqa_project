import re

import allure
import pytest
from playwright.sync_api import expect

from pages.store.catalog_page import CatalogPage
from pages.store.product_page import ProductPage


@allure.title("Клик по карточке открывает страницу товара с её содержимым")
@pytest.mark.frontend
def test_open_product_from_catalog_card(catalog_page: CatalogPage, product_page: ProductPage) -> None:
    # Находим перфоратор через поиск и открываем его карточку
    catalog_page.open()
    catalog_page.search("Перфоратор")
    expect(catalog_page.cards).to_have_count(1)
    catalog_page.first_card().open()

    # Адрес заканчивается на /store/product/8
    # Флаги площадки (?reset=1&delay=0) переносятся на все страницы
    # поэтому проверяем путь регуляркой с необязательным query, а не точным URL
    expect(product_page.page).to_have_url(re.compile(r"/store/product/8(\?.*)?$"))
    expect(product_page.root).to_have_attribute("data-product-id", "8")

    # Хлебные крошки показывают путь каталог категория
    expect(product_page.breadcrumbs).to_contain_text("Каталог")
    expect(product_page.breadcrumbs).to_contain_text("Электроинструмент")

    # Основные данные товара
    # Остаток здесь с «шт.» на карточке каталога было без него, это разные элементы
    expect(product_page.brand).to_have_text("Makita")
    expect(product_page.name).to_have_text("Перфоратор 800 Вт SDS-plus")
    expect(product_page.price).to_have_text("8 490 ₽")
    expect(product_page.stock).to_have_text("В наличии: 4 шт.")


@allure.title("Таблица характеристик перфоратора содержит 3 строки и мощность 800 Вт")
@pytest.mark.frontend
def test_product_specs(product_page: ProductPage) -> None:
    # Открываем страницу товара напрямую по ссылке, без перехода из каталога
    product_page.open_by_id(8)
    expect(product_page.root).to_have_attribute("data-product-id", "8")

    # В таблице ровно три характеристики
    expect(product_page.spec_rows).to_have_count(3)

    # В строке «Мощность» указано значение 800 Вт
    # to_contain_text, а не to_have_text строка содержит и название, и значение
    expect(product_page.spec_row("Мощность")).to_contain_text("800 Вт")


@allure.title("Несуществующий id показывает «Товар не найден» и возврат в каталог")
@pytest.mark.frontend
def test_product_not_found_returns_to_catalog(catalog_page: CatalogPage, product_page: ProductPage) -> None:
    # Открываем заведомо несуществующий товар (кидает на таски и тест заваливается)
    product_page.open_by_id(999)

    # Вместо страницы товара блок с сообщением и кнопкой возврата
    expect(product_page.not_found).to_contain_text("Товар не найден")
    expect(product_page.not_found_catalog_button).to_be_visible()

    # Кнопка возвращает в каталог адрес /store/ и снова полная выдача
    product_page.not_found_catalog_button.click()
    expect(catalog_page.page).to_have_url(re.compile(r"/store/(\?.*)?$"))
    expect(catalog_page.cards).to_have_count(8)
