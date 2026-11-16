from playwright.sync_api import Locator


class ProductCard:
    """Динамический page element: одна карточка товара в каталоге."""

    def __init__(self, root: Locator) -> None:
        # root локатор конкретной карточки, поиск элементов ограничен ею
        self.root = root

        # Название и цена товара
        self.name = root.get_by_test_id("product-card-name")
        self.price = root.get_by_test_id("product-card-price")
