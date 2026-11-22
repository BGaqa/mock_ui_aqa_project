from playwright.sync_api import Locator


class OrderRow:
    """Динамический page element: одна строка таблицы заказов."""

    def __init__(self, root: Locator) -> None:
        # root локатор конкретной строки, поиск элементов ограничен ею
        self.root = root

        # Ссылка на страницу заказа по номеру
        self.link = root.get_by_test_id("order-row-link")

        # Короткий статус в списке и сумма заказа
        self.status = root.get_by_test_id("order-row-status")
        self.total = root.get_by_test_id("order-row-total")
