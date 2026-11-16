from playwright.sync_api import Page


class BasePage:
    # Адрес страницы по умолчанию, наследники переопределяют его
    URL: str = ""

    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self) -> None:
        """Открывает страницу по адресу URL."""
        self.page.goto(self.URL)
