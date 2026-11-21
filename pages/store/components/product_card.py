import allure
from playwright.sync_api import Locator


class ProductCard:
    """Динамический page element, одна карточка товара в каталоге."""

    def __init__(self, root: Locator) -> None:
        # root локатор конкретной карточки, поиск элементов ограничен ею
        self.root = root

        # Название и цена товара
        self.name = root.get_by_test_id("product-card-name")
        self.price = root.get_by_test_id("product-card-price")

        # Остаток на складе, «В наличии: 4» или «Нет в наличии»
        self.stock = root.get_by_test_id("product-card-stock")

        # Категория товара «Электроинструмент», «Защита» и т.д.
        self.category = root.get_by_test_id("product-card-category")

        # Ссылка на страницу товара, клик по ней уводит на /store/product/{id}
        self.link = root.get_by_test_id("product-card-link")

        # Кнопка добавления в корзину неактивна, если товара нет в наличии
        self.add_button = root.get_by_test_id("product-card-add-button")

    @allure.step("Открыть страницу товара из карточки")
    def open(self) -> None:
        self.link.click()
