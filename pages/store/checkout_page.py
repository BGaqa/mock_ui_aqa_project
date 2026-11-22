import allure
from playwright.sync_api import Page

from pages.store.base_store_page import BaseStorePage


class CheckoutPage(BaseStorePage):
    """Страница оформления заказа. Шаг 1 контакты."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Степпер: в data-active-step лежит индекс текущего шага, начиная с нуля
        self.stepper = page.get_by_test_id("checkout-stepper")

        # Кнопка перехода к следующему шагу, она же запускает валидацию полей
        self.next_button = page.get_by_test_id("checkout-next-button")

        # Поля контактов первого шага
        self.name_input = page.get_by_test_id("checkout-name-input")
        self.email_input = page.get_by_test_id("checkout-email-input")
        self.phone_input = page.get_by_test_id("checkout-phone-input")

        # Ошибки под полями, появляются после «Далее» с невалидными данными
        self.name_error = page.get_by_test_id("checkout-name-error")
        self.email_error = page.get_by_test_id("checkout-email-error")
        self.phone_error = page.get_by_test_id("checkout-phone-error")

    @allure.step("Открыть оформление заказа")
    def open(self, reset: bool = True) -> None:
        self.open_path("checkout", reset=reset)

    @allure.step("Заполнить контакты: {name}, {email}, {phone}")
    def fill_contacts(self, name: str, email: str, phone: str) -> None:
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.phone_input.fill(phone)

    @allure.step("Перейти к следующему шагу оформления")
    def next_step(self) -> None:
        self.next_button.click()
