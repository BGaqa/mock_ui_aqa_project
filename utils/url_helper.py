from urllib.parse import urlencode, urljoin


def build_url(base_url: str, path: str = "", **params: str | int) -> str:
    """Собирает URL из базы, относительного пути и query-параметров."""
    # urljoin корректно склеивает части, только если base_url заканчивается на "/"
    # В конфиге BASE_FRONT_URL_UI = "https://dev.aqa-boris.ru/store/" — слеш уже есть
    url = urljoin(base_url, path)

    # Флаги площадки (reset, delay, paymentDelay, autohide) передаём через query
    if params:
        url = f"{url}?{urlencode(params)}"

    return url
