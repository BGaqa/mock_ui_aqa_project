import re

import allure
import pytest
from playwright.sync_api import expect

from pages.store.orders_page import OrdersPage


@allure.title("Чистый браузер: список заказов пуст, есть кнопка в каталог")
@pytest.mark.frontend
def test_orders_empty_in_clean_browser(orders_page: OrdersPage) -> None:
    # Открываем список с reset, заказов ещё нет
    orders_page.open()

    expect(orders_page.empty).to_contain_text("Заказов пока нет")
    expect(orders_page.empty_catalog_button).to_be_visible()
    expect(orders_page.rows).to_have_count(0)


@allure.title("Список заказов: новые сверху, переход по номеру и жизнь после reload")
@pytest.mark.frontend
def test_orders_list_order_navigation_and_persistence(two_orders: OrdersPage) -> None:
    orders = two_orders

    # Две строки, новые сверху. Здесь порядок сам является проверкой,
    # поэтому nth оправдан, мы утверждаем именно позицию, а не обходим уникальность
    expect(orders.rows).to_have_count(2)
    expect(orders.rows.nth(0)).to_have_attribute("data-order-number", "ORD-1002")
    expect(orders.rows.nth(1)).to_have_attribute("data-order-number", "ORD-1001")

    # Статусы в списке короткие, наличные ждут оплаты, карта оплачена
    expect(orders.row("ORD-1002").status).to_have_text("Ожидает оплаты")
    expect(orders.row("ORD-1001").status).to_have_text("Оплачен")

    # Суммы совпадают с итогами заказов: обе корзины были 17 330 ₽
    expect(orders.row("ORD-1002").total).to_have_text("17 330 ₽")
    expect(orders.row("ORD-1001").total).to_have_text("17 330 ₽")

    # Клик по номеру открывает страницу заказа, «назад» возвращает в список
    orders.row("ORD-1002").link.click()
    expect(orders.page).to_have_url(re.compile(r"/store/order\?.*number=ORD-1002(&|$)"))
    orders.page.go_back()
    expect(orders.page).to_have_url(re.compile(r"/store/orders(\?.*)?$"))

    # Перезагрузка: список живёт в localStorage, обе строки на месте
    orders.page.reload()
    expect(orders.rows).to_have_count(2)
    expect(orders.row("ORD-1002").status).to_have_text("Ожидает оплаты")
    expect(orders.row("ORD-1001").status).to_have_text("Оплачен")
