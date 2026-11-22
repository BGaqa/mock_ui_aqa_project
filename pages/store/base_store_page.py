import allure
from playwright.sync_api import Page

from config import Config
from pages.base_page import BasePage
from pages.store.components.shop_header import ShopHeader
from utils.url_helper import build_url


class BaseStorePage(BasePage):
    """База всех страниц магазина общая шапка, тосты и флаги площадки."""

    URL = Config.BASE_FRONT_URL_UI

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        # Шапка одинакова на всех страницах магазина, поэтому живёт в базе
        self.header = ShopHeader(page)

        # Зелёные тосты об успехе. Флаг autohide=0 в URL не даёт им исчезать
        self.success_toasts = page.locator('[data-testid="toast"][data-severity="success"]')

        # Тосты ошибок
        self.error_toasts = page.locator('[data-testid="toast"][data-severity="error"]')

        # Любой тост независимо от severity
        self.toasts = page.get_by_test_id("toast")

        # Страница «не найдено», блок, путь и кнопка возврата в каталог
        # Живет в базе, потому что доступна с любого адреса магазина
        self.not_found = page.get_by_test_id("not-found")
        self.not_found_path = page.get_by_test_id("not-found-path")
        self.not_found_catalog_button = page.get_by_test_id("not-found-catalog-button")

        # Крестик закрытия тоста, отдельного testid у него нет,
        # ищем по роли и доступному имени внутри самого тоста
        self.toast_close_button = page.get_by_test_id("toast").get_by_role("button", name="Close")

    @allure.step("Открыть страницу магазина")
    def open_path(self, path: str = "", reset: bool = True) -> None:
        # reset=1 очищает корзину и заказы, поэтому после первых добавлений
        # товара переходим только с reset=False: корзина хранится в localStorage
        # paymentDelay=0 убирает двухсекундную «обработку оплаты»
        flags: dict[str, int] = {"delay": 0, "autohide": 0, "paymentDelay": 0}
        if reset:
            flags["reset"] = 1
        self.page.goto(build_url(self.URL, path, **flags))

    @allure.step("Открыть страницу магазина с произвольными флагами")
    def open_with_flags(self, path: str = "", **flags: int) -> None:
        # В отличие от open_path не добавляет ничего своего
        # нужно для проверок переноса query-параметров, где важен точный набор флагов
        self.page.goto(build_url(self.URL, path, **flags))

    @allure.step("Закрыть тост крестиком")
    def close_toast(self) -> None:
        self.toast_close_button.click()
