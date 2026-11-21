from playwright.sync_api import Locator


class CartRow:
    """Динамический page element, одна строка таблицы корзины."""

    def __init__(self, root: Locator) -> None:
        # root локатор конкретной строки, поиск элементов ограничен ею
        self.root = root

        # Цена товара, поле количества и кнопки степпера
        self.price = root.get_by_test_id("cart-row-price")
        self.qty_input = root.get_by_test_id("cart-row-qty-input")
        self.increment = root.get_by_test_id("cart-row-qty-increment")
        self.decrement = root.get_by_test_id("cart-row-qty-decrement")

        # Сумма строки, цена умноженная на количество
        self.total = root.get_by_test_id("cart-row-total")
