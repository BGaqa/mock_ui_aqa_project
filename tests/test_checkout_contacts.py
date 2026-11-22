import re

import allure
import pytest
from playwright.sync_api import expect

from pages.store.cart_page import CartPage
from pages.store.checkout_page import CheckoutPage


@allure.title("Чекаут, шаг 1, валидация контактов и переход на второй шаг")
@pytest.mark.frontend
def test_checkout_contacts_validation(cart_with_two_products: CartPage, checkout_page: CheckoutPage) -> None:
    cart = cart_with_two_products

    # Переходим к оформлению кнопкой из корзины
    cart.go_to_checkout()

    # Адрес чекаута и степпер, активен первый шаг (индекс 0)
    expect(checkout_page.page).to_have_url(re.compile(r"/store/checkout(\?.*)?$"))
    expect(checkout_page.stepper).to_have_attribute("data-active-step", "0")

    # Жмём «Далее» с пустыми полями, появляются все три ошибки
    checkout_page.next_step()
    expect(checkout_page.name_error).to_have_text("Введите имя")
    expect(checkout_page.email_error).to_have_text("Некорректный email")
    expect(checkout_page.phone_error).to_have_text("Некорректный телефон")

    # Заполняем имя и телефон верно, email оставляем битым
    checkout_page.fill_contacts("Вадим", "vadim@", "+7 900 123-45-67")
    checkout_page.next_step()

    # Осталась только ошибка email, валидные поля больше не подсвечены
    expect(checkout_page.email_error).to_have_text("Некорректный email")
    expect(checkout_page.name_error).not_to_be_visible()
    expect(checkout_page.phone_error).not_to_be_visible()

    # Исправляем email и проходим дальше, степпер переключается на шаг 1
    checkout_page.email_input.fill("vadim@example.com")
    checkout_page.next_step()
    expect(checkout_page.stepper).to_have_attribute("data-active-step", "1")


@allure.title("Чекаут с пустой корзиной редиректит обратно в корзину")
@pytest.mark.frontend
def test_checkout_redirects_when_cart_empty(checkout_page: CheckoutPage, cart_page: CartPage) -> None:
    # Открываем чекаут напрямую с reset=1: корзина гарантированно пуста
    checkout_page.open()

    # Площадка перекидывает в корзину и показывает блок пустой корзины
    expect(checkout_page.page).to_have_url(re.compile(r"/store/cart(\?.*)?$"))
    expect(cart_page.empty).to_be_visible()
