import re

import allure
import pytest
from playwright.sync_api import expect

from pages.store.catalog_page import CatalogPage


@allure.title("Флаг delay переносится на адрес корзины")
@pytest.mark.frontend
def test_cart_link_preserves_flags(catalog_page: CatalogPage) -> None:
    # Открываем каталог ровно с одним флагом, без наших стандартных добавок
    catalog_page.open_with_flags(delay=0)

    # Кликаем иконку корзины параметр должен пережить переход
    catalog_page.header.open_cart()
    expect(catalog_page.page).to_have_url(re.compile(r"/store/cart\?delay=0$"))


@allure.title("Несуществующий путь: страница «не найдено» и кнопка в каталог")
@pytest.mark.frontend
# проблемы с редиректом, как в пятом задании
def test_not_found_page_and_catalog_button(catalog_page: CatalogPage) -> None:
    # Открываем заведомо несуществующий адрес, флаг оставляем для чистоты эксперимента
    catalog_page.open_with_flags("nowhere", delay=0)

    # Блок «не найдено» показывает и сообщение, и конкретный путь
    expect(catalog_page.not_found).to_contain_text("Страница не найдена")
    expect(catalog_page.not_found_path).to_have_text("/store/nowhere")

    # Кнопка возвращает в каталог
    catalog_page.not_found_catalog_button.click()
    expect(catalog_page.page).to_have_url(re.compile(r"/store/(\?.*)?$"))


@allure.title("Логотип ведёт в каталог и сохраняет флаги")
@pytest.mark.frontend
# аналогияная проблема
def test_logo_preserves_flags(catalog_page: CatalogPage) -> None:
    # Стартуем с несуществующего адреса с флагом
    # логотип должен вернуть в каталог, не потеряв параметр
    catalog_page.open_with_flags("nowhere", delay=0)

    catalog_page.logo.click()
    expect(catalog_page.page).to_have_url(re.compile(r"/store/\?delay=0$"))
