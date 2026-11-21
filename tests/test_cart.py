import allure
import pytest
from playwright.sync_api import expect

from pages.store.cart_page import CartPage
from pages.store.catalog_page import CatalogPage
from pages.store.product_page import ProductPage


@allure.title("Добавление в корзину, пересчёт сумм и сохранение после перезагрузки")
@pytest.mark.frontend
def test_add_products_and_recalculate_cart(
    catalog_page: CatalogPage,
    product_page: ProductPage,
    cart_page: CartPage,
) -> None:
    # Чистое состояние корзина пуста, тосты не исчезают сами
    catalog_page.open()
    catalog_page.search("Перфоратор")
    expect(catalog_page.cards).to_have_count(1)

    # Тосты не накапливаются, а заменяют друг друга,
    # поэтому в DOM всегда ровно один success-тост.
    # Факт добавления проверяем бейджем, а тостом наличие уведомления
    card = catalog_page.first_card()
    card.add_button.click()
    expect(catalog_page.success_toasts).to_have_count(1)
    expect(catalog_page.header.cart_badge).to_have_attribute("data-count", "1")

    card.add_button.click()
    expect(catalog_page.success_toasts).to_have_count(1)
    expect(catalog_page.header.cart_badge).to_have_attribute("data-count", "2")

    # Открываем рулетку БЕЗ reset, полная загрузка, но корзина берётся
    # из localStorage, поэтому добавленные товары не теряются
    product_page.open_by_id(13, reset=False)
    product_page.add_button.click()
    expect(product_page.success_toasts).to_have_count(1)
    expect(product_page.header.cart_badge).to_have_attribute("data-count", "3")

    # Переходим в корзину кликом по иконке в шапке, как пользователь
    product_page.header.open_cart()

    # Две строки, перфоратор количеством 2 и рулетка количеством 1
    expect(cart_page.rows).to_have_count(2)

    perforator = cart_page.row(8)
    expect(perforator.price).to_have_text("8 490 ₽")
    expect(perforator.qty_input).to_have_value("2")
    expect(perforator.total).to_have_text("16 980 ₽")

    roulette = cart_page.row(13)
    expect(roulette.price).to_have_text("350 ₽")
    expect(roulette.qty_input).to_have_value("1")
    expect(roulette.total).to_have_text("350 ₽")

    # Итоги, доставка бесплатна, потому что сумма выше 5 000
    expect(cart_page.subtotal).to_have_text("17 330 ₽")
    expect(cart_page.delivery).to_have_text("бесплатно")
    expect(cart_page.total).to_have_text("17 330 ₽")

    # «+» пересчитывает строку и итог, 3 перфоратора плюс рулетка
    perforator.increment.click()
    expect(perforator.total).to_have_text("25 470 ₽")
    expect(cart_page.subtotal).to_have_text("25 820 ₽")

    # «−» возвращает значения обратно
    perforator.decrement.click()
    expect(perforator.total).to_have_text("16 980 ₽")
    expect(cart_page.subtotal).to_have_text("17 330 ₽")

    # Перезагрузка, в текущем URL нет reset, поэтому корзина переживает reload
    cart_page.page.reload()
    expect(cart_page.rows).to_have_count(2)
    expect(cart_page.subtotal).to_have_text("17 330 ₽")
    expect(cart_page.header.cart_badge).to_have_attribute("data-count", "3")
