import allure
import pytest
from playwright.sync_api import expect

from pages.store.cart_page import CartPage


@allure.title("Отмена в диалоге удаления оставляет строку в корзине")
@pytest.mark.frontend
def test_remove_dialog_cancel_keeps_row(cart_with_two_products: CartPage) -> None:
    cart = cart_with_two_products

    # Открываем диалог удаления на строке рулетки
    cart.request_remove_row(13)

    # Диалог показывает, какой именно товар собираемся удалить
    expect(cart.remove_dialog).to_be_visible()
    expect(cart.remove_dialog_title).to_have_text("Удалить товар?")
    expect(cart.remove_dialog_text).to_have_text("«Рулетка 5 м × 25 мм» будет удалён из корзины")

    # Отменяем, диалог закрывается, корзина не меняется
    cart.cancel_remove()
    expect(cart.remove_dialog).not_to_be_visible()
    expect(cart.rows).to_have_count(2)


@allure.title("Подтверждение в диалоге удаляет строку и пересчитывает итог")
@pytest.mark.frontend
def test_remove_dialog_confirm_removes_row(cart_with_two_products: CartPage) -> None:
    cart = cart_with_two_products

    # Удаляем рулетку через подтверждение в диалоге
    cart.request_remove_row(13)
    expect(cart.remove_dialog).to_be_visible()
    cart.confirm_remove()

    # Диалог закрыт, в корзине осталась одна строка перфоратор
    expect(cart.remove_dialog).not_to_be_visible()
    expect(cart.rows).to_have_count(1)

    # Тост подтверждает удаление именно рулетки
    expect(cart.toasts).to_contain_text("«Рулетка 5 м × 25 мм» удалён из корзины")

    # Итог пересчитан, осталась только цена перфоратора
    expect(cart.total).to_have_text("8 490 ₽")


@allure.title("Очистка корзины показывает пустое состояние и обнуляет счётчик")
@pytest.mark.frontend
def test_clear_cart_empties_and_shows_empty_state(cart_with_two_products: CartPage) -> None:
    cart = cart_with_two_products

    # Очищаем корзину с подтверждением в диалоге
    cart.clear_cart()

    # Вместо таблицы блок «Корзина пуста» с кнопкой возврата в каталог
    expect(cart.empty).to_be_visible()
    expect(cart.empty_catalog_button).to_be_visible()

    # Счётчик в шапке обнулился
    expect(cart.header.cart_badge).to_have_attribute("data-count", "0")

    # Тост подтверждает очистку
    expect(cart.toasts).to_contain_text("Корзина очищена")
