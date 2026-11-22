import allure
import pytest
from playwright.sync_api import expect

from pages.store.checkout_page import CheckoutPage
from pages.store.order_page import OrderPage


@allure.title("Оплата наличными: без карты, заказ со статусом ожидания оплаты")
@pytest.mark.frontend
def test_cash_payment_creates_processing_order(checkout_payment_step: CheckoutPage, order_page: OrderPage) -> None:
    checkout = checkout_payment_step

    # Выбираем наличные, блок полей карты скрывается, заполнять нечего
    checkout.select_cash()
    expect(checkout.card_block).not_to_be_visible()

    # Подпись кнопки меняется на подтверждение с итогом корзины
    # самовывоз бесплатный, поэтому итог равен сумме товаров
    expect(checkout.pay_button).to_have_text("Подтвердить заказ на 17 330 ₽")

    # Подтверждаем заказ: банковской обработки нет, статус сразу ожидает оплаты
    checkout.pay()

    # На странице заказа статус ожидания и способ оплаты наличными
    expect(order_page.status).to_have_text("Ожидает оплаты при получении")
    expect(order_page.status).to_have_attribute("data-status", "processing")
    expect(order_page.payment).to_contain_text("Наличными при получении")
