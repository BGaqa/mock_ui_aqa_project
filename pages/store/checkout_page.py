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

        # Переключатели способа доставки
        self.delivery_courier = page.get_by_test_id("checkout-delivery-courier")
        self.delivery_pickup = page.get_by_test_id("checkout-delivery-pickup")

        # Блок адреса курьера и его поля, виден только при курьере
        self.address_block = page.get_by_test_id("checkout-address")
        self.city_input = page.get_by_test_id("checkout-city-input")
        self.street_input = page.get_by_test_id("checkout-street-input")
        self.house_input = page.get_by_test_id("checkout-house-input")
        self.date_input = page.get_by_test_id("checkout-date-input")

        # Ошибки под полями адреса
        self.city_error = page.get_by_test_id("checkout-city-error")
        self.street_error = page.get_by_test_id("checkout-street-error")
        self.house_error = page.get_by_test_id("checkout-house-error")
        self.date_error = page.get_by_test_id("checkout-date-error")

        # Адрес пункта выдачи, показывается вместо блока адреса при самовывозе
        self.pickup_address = page.get_by_test_id("checkout-pickup-address")

        # Итоги в правой колонке чекаута, пересчитываются сразу при переключении
        self.summary_delivery = page.get_by_test_id("checkout-summary-delivery")
        self.summary_total = page.get_by_test_id("checkout-summary-total")

        # Кнопка возврата на предыдущий шаг
        self.back_button = page.get_by_test_id("checkout-back-button")

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

    @allure.step("Заполнить адрес курьера: {city}, {street}, {house}, {date}")
    def fill_address(self, city: str, street: str, house: str, date: str) -> None:
        self.city_input.fill(city)
        self.street_input.fill(street)
        self.house_input.fill(house)
        self.date_input.fill(date)

    @allure.step("Выбрать доставку курьером")
    def select_courier(self) -> None:
        self.delivery_courier.click()

    @allure.step("Выбрать самовывоз")
    def select_pickup(self) -> None:
        self.delivery_pickup.click()

    @allure.step("Вернуться на предыдущий шаг оформления")
    def back(self) -> None:
        self.back_button.click()
