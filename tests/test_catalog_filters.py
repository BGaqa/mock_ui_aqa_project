import allure
import pytest
from playwright.sync_api import expect

from pages.store.catalog_page import CatalogPage
from utils.price_parser import parse_price


@allure.title("Категория «Электроинструмент» и «Только в наличии» дают 5 товаров")
@pytest.mark.frontend
def test_category_and_in_stock_filters(catalog_page: CatalogPage) -> None:
    # Открываем каталог и включаем два фильтра: категорию и наличие
    catalog_page.open()
    catalog_page.select_category("power")
    catalog_page.set_in_stock(True)

    # Счётчик дожидается пересчёта выдачи страница не перезагружается
    expect(catalog_page.results_count).to_have_text("Найдено: 5")
    expect(catalog_page.cards).to_have_count(5)

    # Берём карточки как компоненты и проверяем категорию у каждой
    cards = catalog_page.all_cards()
    categories = [card.category.inner_text() for card in cards]
    assert categories == ["Электроинструмент"] * 5

    # Нулевого остатка быть не должно фильтр наличия отсеял лобзик
    stocks = [card.stock.get_attribute("data-stock") for card in cards]
    assert "0" not in stocks


@allure.title("Сортировка «Сначала дешёвые» выстраивает цены по возрастанию")
@pytest.mark.frontend
def test_sort_by_price_ascending(catalog_page: CatalogPage) -> None:
    # Готовим выдачу: электроинструмент в наличии, сортировка по возрастанию цены
    catalog_page.open()
    catalog_page.select_category("power")
    catalog_page.set_in_stock(True)
    catalog_page.select_sort("price-asc")
    expect(catalog_page.results_count).to_have_text("Найдено: 5")
    expect(catalog_page.cards).to_have_count(5)

    # Крайние карточки задают границы диапазона фен 2 990 и перфоратор 8 490
    cards = catalog_page.all_cards()
    expect(cards[0].name).to_have_text("Строительный фен 2000 Вт")
    expect(cards[0].price).to_have_text("2 990 ₽")
    expect(cards[-1].name).to_have_text("Перфоратор 800 Вт SDS-plus")
    expect(cards[-1].price).to_have_text("8 490 ₽")

    # Проверяем весь список, а не только крайние, собираем цены
    # переводим в числа и сравниваем с отсортированной копией
    prices = [parse_price(card.price.inner_text()) for card in cards]
    assert prices == sorted(prices)


@allure.title("Сброс фильтров возвращает каталог и контролы к исходному состоянию")
@pytest.mark.frontend
def test_reset_filters(catalog_page: CatalogPage) -> None:
    # Применяем все три фильтра, чтобы было что сбрасывать
    catalog_page.open()
    catalog_page.select_category("power")
    catalog_page.set_in_stock(True)
    catalog_page.select_sort("price-asc")
    expect(catalog_page.results_count).to_have_text("Найдено: 5")

    # Сбрасываем фильтры кнопкой в панели фильтров
    catalog_page.reset_filters()

    # Каталог снова полный 24 товара, на первой странице 8 карточек
    expect(catalog_page.results_count).to_have_text("Найдено: 24")
    expect(catalog_page.cards).to_have_count(8)

    # Сброшено состояние самих контролов, а не только выдача
    expect(catalog_page.category_checkbox("power")).not_to_be_checked()
    expect(catalog_page.in_stock_switch).not_to_be_checked()
    expect(catalog_page.sort_select).to_contain_text("Популярные")

    # Сбрасывать больше нечего, кнопка неактивна
    expect(catalog_page.reset_button).to_be_disabled()
