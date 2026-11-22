import allure
import pytest
from playwright.sync_api import expect

from pages.store.catalog_page import CatalogPage


@allure.title("С autohide=0 тост живёт дольше трёх секунд")
@pytest.mark.frontend
def test_toast_persists_with_autohide_zero(catalog_page: CatalogPage) -> None:
    # Открываем ровно с флагом autohide=0 тост не должен исчезать сам
    catalog_page.open_with_flags(autohide=0)
    catalog_page.add_product("Перфоратор")
    expect(catalog_page.toasts).to_be_visible()

    # Ждём заведомо больше времени жизни тоста (3 с)
    # sleep здесь оправдан, предмет проверки именно длительность, а не ожидание элемента
    catalog_page.page.wait_for_timeout(3500)
    expect(catalog_page.toasts).to_be_visible()


@allure.title("Без флага тост появляется и исчезает сам")
@pytest.mark.frontend
def test_toast_autohides_without_flag(catalog_page: CatalogPage) -> None:
    # Открываем без флагов autohide по умолчанию 3000мс
    catalog_page.open_with_flags()
    catalog_page.add_product("Перфоратор")

    # Тост появился, затем исчез сам, not_to_be_visible сам дождётся 3с
    expect(catalog_page.toasts).to_be_visible()
    expect(catalog_page.toasts).not_to_be_visible()


@allure.title("Клик мимо тоста не закрывает его, крестик закрывает")
@pytest.mark.frontend
def test_toast_click_outside_keeps_and_cross_closes(catalog_page: CatalogPage) -> None:
    # autohide=0, чтобы тост не исчез сам во время проверок кликов
    catalog_page.open_with_flags(autohide=0)
    catalog_page.add_product("Перфоратор")
    expect(catalog_page.toasts).to_be_visible()

    # Клик мимо тоста, по неинтерактивному счётчику, чтобы не уйти со страницы
    catalog_page.results_count.click()
    expect(catalog_page.toasts).to_be_visible()

    # Крестик закрывает тост
    catalog_page.close_toast()
    expect(catalog_page.toasts).not_to_be_visible()
