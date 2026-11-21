import allure
import pytest
from playwright.sync_api import expect

from pages.store.catalog_page import CatalogPage


@allure.title("Пагинация: три страницы по 8 товаров, все 24 id уникальны")
@pytest.mark.frontend
def test_pagination_pages_have_unique_products(catalog_page: CatalogPage) -> None:
    # Открываем каталог и собираем id товаров первой страницы
    catalog_page.open()
    expect(catalog_page.cards).to_have_count(8)
    first_page_ids = catalog_page.card_ids()

    # Переходим на вторую страницу
    # Ждём смену активной кнопки, а не количество карточек
    # на каждой странице их одинаково (8), поэтому count не признак смены страницы
    catalog_page.go_to_page(2)
    expect(catalog_page.active_page).to_have_text("2")
    expect(catalog_page.cards).to_have_count(8)
    second_page_ids = catalog_page.card_ids()

    # Переходим на третью страницу и собираем id так же
    catalog_page.go_to_page(3)
    expect(catalog_page.active_page).to_have_text("3")
    expect(catalog_page.cards).to_have_count(8)
    third_page_ids = catalog_page.card_ids()

    # Всего собрано 24 id, и среди них нет повторяющихся
    all_ids = first_page_ids + second_page_ids + third_page_ids
    assert len(all_ids) == 24
    assert len(set(all_ids)) == 24

    # Дополнительно проверяем, что страницы не пересекаются попарно
    # так по сообщению об ошибке сразу видно, какие две страницы задублились
    assert set(first_page_ids).isdisjoint(second_page_ids)
    assert set(first_page_ids).isdisjoint(third_page_ids)
    assert set(second_page_ids).isdisjoint(third_page_ids)


@allure.title("Пагинация: активная кнопка помечена aria-current и меняется при переходе")
@pytest.mark.frontend
def test_active_page_attribute_changes(catalog_page: CatalogPage) -> None:
    # На первой странице активна кнопка «1» с aria-current="page"
    catalog_page.open()
    expect(catalog_page.active_page).to_have_text("1")
    expect(catalog_page.active_page).to_have_attribute("aria-current", "page")

    # Переходим на вторую страницу метка переезжает на кнопку «2»
    catalog_page.go_to_page(2)
    expect(catalog_page.active_page).to_have_text("2")
    expect(catalog_page.active_page).to_have_attribute("aria-current", "page")

    # На третьей странице активной становится кнопка «3»
    catalog_page.go_to_page(3)
    expect(catalog_page.active_page).to_have_text("3")

    # Активная кнопка всегда ровно одна
    expect(catalog_page.active_page).to_have_count(1)


@allure.title("Фильтр «Защита» даёт 4 товара и убирает пагинацию")
@pytest.mark.frontend
def test_safety_category_filter_hides_pagination(catalog_page: CatalogPage) -> None:
    # Открываем каталог до фильтра пагинация видна, страниц три
    catalog_page.open()
    expect(catalog_page.pagination).to_be_visible()
    expect(catalog_page.pagination_pages).to_have_count(3)

    # Включаем категорию «Защита» в ней всего 4 товара
    catalog_page.select_category("safety")

    # Все товары помещаются на одну страницу 4 карточки, счётчик 4
    expect(catalog_page.results_count).to_have_text("Найдено: 4")
    expect(catalog_page.cards).to_have_count(4)

    # Пагинация исчезает делить нечего
    expect(catalog_page.pagination).not_to_be_visible()
