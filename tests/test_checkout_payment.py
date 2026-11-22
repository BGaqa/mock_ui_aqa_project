import re

import allure
import pytest
from playwright.sync_api import expect

from pages.store.checkout_page import CheckoutPage
from pages.store.order_page import OrderPage


@allure.title("Оплата: валидация пустой карты, маски полей и подпись кнопки")
@pytest.mark.frontend
def test_payment_card_validation_and_formatting(checkout_payment_step: CheckoutPage) -> None:
    checkout = checkout_payment_step

    # Жмём «Оплатить» с пустой картой, четыре ошибки под полями
    checkout.pay()
    expect(checkout.card_number_error).to_have_text("Номер карты: 16 цифр")
    expect(checkout.card_expiry_error).to_have_text("Формат ММ/ГГ")
    expect(checkout.card_cvv_error).to_have_text("3 цифры")
    expect(checkout.card_holder_error).to_have_text("Обязательное поле")

    # Вводим цифры без пробелов и слешей, поля форматируют их сами
    checkout.fill_card("0000000000000000", "1229", "123", "IVAN IVANOV")
    expect(checkout.card_number_input).to_have_value("0000 0000 0000 0000")
    expect(checkout.card_expiry_input).to_have_value("12/29")

    # Подпись кнопки оплаты включает итог заказа
    expect(checkout.pay_button).to_have_text("Оплатить 17 330 ₽")


@allure.title("Сквозная покупка: отказ банка, затем успешная оплата заказа ORD-1001")
@pytest.mark.frontend
def test_payment_decline_then_success(checkout_payment_step: CheckoutPage, order_page: OrderPage) -> None:
    checkout = checkout_payment_step

    # Карта, начинающаяся с 0000, всегда отклоняется банком
    checkout.fill_card("0000000000000000", "1229", "123", "IVAN IVANOV")
    checkout.pay()

    # Красный блок отказа, адрес всё ещё чекаут
    expect(checkout.payment_error).to_contain_text("Банк отклонил операцию")
    expect(checkout.page).to_have_url(re.compile(r"/store/checkout(\?.*)?$"))

    # Счётчик корзины не изменился: заказ не создан, товары на месте
    expect(checkout.header.cart_badge).to_have_attribute("data-count", "3")

    # Заменяем номер на рабочую карту и оплачиваем повторно
    checkout.card_number_input.fill("4111111111111111")
    checkout.pay()

    # Переход на страницу заказа: номер и в адресе, и на самой странице
    expect(checkout.page).to_have_url(re.compile(r"/store/order\?.*number=ORD-1001(&|$)"))
    expect(order_page.root).to_have_attribute("data-order-number", "ORD-1001")
    expect(order_page.number).to_have_text("Заказ ORD-1001")

    # Статус оплачен, итог и способы доставки/оплаты
    expect(order_page.status).to_have_text("Оплачен")
    expect(order_page.status).to_have_attribute("data-status", "paid")
    expect(order_page.summary_total).to_have_text("17 330 ₽")
    expect(order_page.delivery).to_contain_text("Самовывоз")
    expect(order_page.payment).to_contain_text("Банковской картой")

    # Зелёный блок с email покупателя и тост об оформленном заказе
    expect(order_page.success_block).to_contain_text("vadim@example.com")
    expect(order_page.toasts).to_contain_text("Заказ ORD-1001 оформлен")

    # Корзина опустела только после успешной оплаты
    expect(order_page.header.cart_badge).to_have_attribute("data-count", "0")
