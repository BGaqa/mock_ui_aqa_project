import allure
import pytest
from playwright.sync_api import expect

from pages.store.cart_page import CartPage


@allure.title("Неexistent промокод: ошибка без чипа и без изменения итога")
@pytest.mark.frontend
def test_invalid_promo_code_shows_error(cart_default: CartPage) -> None:
    # База до применения, скидок нет, итог полный
    expect(cart_default.total).to_have_text("17 330 ₽")

    cart_default.apply_promo("NOPE")

    # Ошибка под полем, чип применённого кода не появился
    expect(cart_default.promo_error).to_have_text("Промокод не найден")
    expect(cart_default.promo_chip).not_to_be_visible()

    # Итог не изменился, невалидный код ничего не списал
    expect(cart_default.total).to_have_text("17 330 ₽")


@allure.title("Регистр не важен: sale10 применяется как SALE10")
@pytest.mark.frontend
def test_promo_code_is_case_insensitive(cart_default: CartPage) -> None:
    # Вводим код строчными буквами магазин приводит его к верхнему регистру
    cart_default.apply_promo("sale10")

    # Чип хранит код в верхнем регистре и в тексте, и в data-code
    expect(cart_default.promo_chip).to_have_attribute("data-code", "SALE10")
    expect(cart_default.promo_chip).to_contain_text("SALE10: Скидка 10%")

    # Скидка 10% от суммы товаров и пересчитанный итог
    expect(cart_default.discount).to_have_text("- 1 733 ₽")
    expect(cart_default.total).to_have_text("15 597 ₽")

    # Тост подтверждает применение кодом в верхнем регистре
    expect(cart_default.success_toasts).to_contain_text("Промокод SALE10 применён")


@allure.title("Удаление промокода возвращает поле ввода и полный итог")
@pytest.mark.frontend
def test_remove_promo_code_restores_total(cart_default: CartPage) -> None:
    cart_default.apply_promo("SALE10")

    # Пока код применён, виден чип, а поле ввода спрятано
    expect(cart_default.promo_chip).to_be_visible()
    expect(cart_default.promo_input).not_to_be_visible()

    # Удаляем код крестиком на чипе
    cart_default.remove_promo()

    # Чип исчез, поле ввода снова доступно
    expect(cart_default.promo_chip).not_to_be_visible()
    expect(cart_default.promo_input).to_be_visible()

    # Итог вернулся к сумме без скидки
    expect(cart_default.total).to_have_text("17 330 ₽")


@allure.title("SALE500 списывает 500 ₽ с большой корзины")
@pytest.mark.frontend
def test_sale500_on_large_cart(cart_default: CartPage) -> None:
    # Сумма товаров 17 330 ₽ выше порога 3 000 ₽, код должен примениться
    cart_default.apply_promo("SALE500")

    expect(cart_default.discount).to_have_text("- 500 ₽")
    expect(cart_default.total).to_have_text("16 830 ₽")


@allure.title("SALE500 отклоняется на корзине ниже порога 3 000 ₽")
@pytest.mark.frontend
def test_sale500_rejected_on_small_cart(cart_small: CartPage) -> None:
    # В корзине 350 ₽ меньше порога действия кода
    cart_small.apply_promo("SALE500")

    expect(cart_small.promo_error).to_have_text("Промокод действует от 3 000 ₽")
    expect(cart_small.promo_chip).not_to_be_visible()
    expect(cart_small.total).to_have_text("350 ₽")


@allure.title("FREESHIP делает доставку бесплатной даже на маленькой корзине")
@pytest.mark.frontend
def test_freeship_makes_delivery_free(cart_small: CartPage) -> None:
    # Без промокода доставка на сумме 350 ₽ ещё не рассчитана
    expect(cart_small.delivery).to_have_text("рассчитается при оформлении")

    cart_small.apply_promo("FREESHIP")

    # Доставка бесплатна, хотя сумма сильно ниже порога 5 000 ₽
    expect(cart_small.delivery).to_have_text("бесплатно")
    expect(cart_small.promo_chip).to_have_attribute("data-code", "FREESHIP")
