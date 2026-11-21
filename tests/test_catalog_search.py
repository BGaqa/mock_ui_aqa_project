import allure
import pytest
from playwright.sync_api import expect

from pages.store.catalog_page import CatalogPage


@allure.title("Поиск по названию «Перфоратор» находит один товар")
@pytest.mark.frontend
def test_search_by_product_name(catalog_page: CatalogPage) -> None:
    # Открываем каталог и ищем товар по части названия
    catalog_page.open()
    catalog_page.search("Перфоратор")

    # Счётчик дожидается применения фильтра, отдельный wait не нужен
    expect(catalog_page.results_count).to_have_text("Найдено: 1")

    # В списке ровно одна карточка, и это именно перфоратор
    expect(catalog_page.cards).to_have_count(1)
    card = catalog_page.first_card()
    expect(card.name).to_have_text("Перфоратор 800 Вт SDS-plus")
    expect(card.price).to_have_text("8 490 ₽")
    expect(card.stock).to_have_text("В наличии: 4")

    # При одном результате страниц нет — пагинация не отображается
    expect(catalog_page.pagination).not_to_be_visible()


@allure.title("Поиск по бренду «bosch» в нижнем регистре находит 4 товара")
@pytest.mark.frontend
def test_search_by_brand_is_case_insensitive(catalog_page: CatalogPage) -> None:
    # Открываем каталог и ищем бренд строчными буквами
    # в данных он записан как «Bosch», это и проверяет независимость от регистра
    catalog_page.open()
    catalog_page.search("bosch")

    # Проверяем счётчик и текстом, и data-атрибутом
    expect(catalog_page.results_count).to_have_text("Найдено: 4")
    expect(catalog_page.results_count).to_have_attribute("data-count", "4")

    # Все 4 товара бренда помещаются на одну страницу
    expect(catalog_page.cards).to_have_count(4)


@allure.title("Поиск без результатов показывает пустое состояние")
@pytest.mark.frontend
def test_search_without_results_shows_empty_state(catalog_page: CatalogPage) -> None:
    # Открываем каталог и вводим заведомо бессмысленный запрос
    catalog_page.open()
    catalog_page.search("ничего такого нет")

    # Вместо сетки товаров показан блок с подсказкой и кнопкой сброса.
    # to_contain_text, а не to_have_text: внутри блока есть ещё текст кнопки
    expect(catalog_page.empty_state).to_contain_text("Ничего не найдено. Попробуйте изменить фильтры")

    # Карточек нет, счётчик обнулён
    expect(catalog_page.cards).to_have_count(0)
    expect(catalog_page.results_count).to_have_text("Найдено: 0")


@allure.title("Сброс фильтров из пустого состояния возвращает весь каталог")
@pytest.mark.frontend
def test_reset_filters_from_empty_state(catalog_page: CatalogPage) -> None:
    # Открываем каталог и приводим его к пустому состоянию
    catalog_page.open()
    catalog_page.search("ничего такого нет")
    expect(catalog_page.empty_state).to_be_visible()

    # Сбрасываем фильтры кнопкой из пустого состояния
    catalog_page.reset_filters_from_empty()

    # Каталог вернулся к исходным 24 товарам, на странице снова 8 карточек
    expect(catalog_page.results_count).to_have_text("Найдено: 24")
    expect(catalog_page.cards).to_have_count(8)

    # Поле поиска очищено — сбросил не только результат, но и сам фильтр
    expect(catalog_page.search_input).to_have_value("")
