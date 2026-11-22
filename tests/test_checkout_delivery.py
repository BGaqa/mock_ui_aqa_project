import allure
import pytest
from playwright.sync_api import expect

from pages.store.checkout_page import CheckoutPage


@allure.title("Курьер: валидация пустого адреса и итог с доставкой 390 ₽")
@pytest.mark.frontend
def test_courier_address_validation_and_totals(checkout_delivery_step: CheckoutPage) -> None:
    checkout = checkout_delivery_step

    # Жмём «Далее» с пустым адресом, остаются на шаге доставки и видим ошибки
    checkout.next_step()
    expect(checkout.city_error).to_have_text("Обязательное поле")
    expect(checkout.street_error).to_have_text("Обязательное поле")
    expect(checkout.house_error).to_have_text("Обязательное поле")
    expect(checkout.date_error).to_have_text("Выберите дату")
    expect(checkout.stepper).to_have_attribute("data-active-step", "1")

    # Заполняем адрес и дату, ошибки живут до следующего "Далее"
    checkout.fill_address("Москва", "Ленина", "10", "2026-12-01")

    # Сумма товаров 350 ₽ ниже порога 5 000 ₽, поэтому курьер стоит 390 ₽
    expect(checkout.summary_delivery).to_have_text("390 ₽")
    expect(checkout.summary_total).to_have_text("740 ₽")


@allure.title("Самовывоз: адрес скрыт, доставка бесплатна, итог 350 ₽")
@pytest.mark.frontend
def test_pickup_hides_address_and_free_delivery(checkout_delivery_step: CheckoutPage) -> None:
    checkout = checkout_delivery_step

    # Переключаем способ доставки, блок адреса исчезает, вместо него пункт выдачи
    checkout.select_pickup()
    expect(checkout.address_block).not_to_be_visible()
    expect(checkout.pickup_address).to_be_visible()

    # Самовывоз бесплатен независимо от суммы корзины
    expect(checkout.summary_delivery).to_have_text("бесплатно")
    expect(checkout.summary_total).to_have_text("350 ₽")


@allure.title("«Назад» сохраняет контакты, повторный проход доходит до шага оплаты")
@pytest.mark.frontend
def test_back_preserves_contacts_and_forward_to_payment(checkout_delivery_step: CheckoutPage) -> None:
    checkout = checkout_delivery_step

    # Заполняем адрес, чтобы шаг доставки был валидным для прохода вперёд
    checkout.fill_address("Москва", "Ленина", "10", "2026-12-01")

    # Возвращаемся на шаг контактов, данные не потерялись
    checkout.back()
    expect(checkout.stepper).to_have_attribute("data-active-step", "0")
    expect(checkout.name_input).to_have_value("Вадим")
    expect(checkout.email_input).to_have_value("vadim@example.com")
    expect(checkout.phone_input).to_have_value("+7 900 123-45-67")

    # Снова вперёд, контакты / доставка / оплата (индекс 2)
    checkout.next_step()
    expect(checkout.stepper).to_have_attribute("data-active-step", "1")
    checkout.next_step()
    expect(checkout.stepper).to_have_attribute("data-active-step", "2")
