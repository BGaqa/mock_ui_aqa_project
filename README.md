# mock_ui_aqa_project

UI-автотесты учебного магазина «Инструмент Маркет»
(учебная площадка `dev.aqa-boris.ru/store`) на **Python + Playwright + pytest**.

Проект покрывает 18 учебных сценариев: от смоука каталога до сквозной покупки,
перехвата сети и проверки таймеров тостов.

## Стек

- Python 3.14, pytest, pytest-playwright (sync API)
- Allure (`allure-pytest`) для отчётов и шагов
- pre-commit: isort, black, flake8, mypy (strict)
- python-dotenv для конфигурации окружения

## Архитектура

- **Page Object + компоненты**: страницы магазина и переиспользуемые
  элементы (`ProductCard`, `CartRow`, `OrderRow`, `ShopHeader`).
- **`BaseStorePage`**: общая шапка, тосты и единая сборка URL с учебными флагами.
- **Фикстуры как DI**: состояния корзин и шаги чекаута собираются в `conftest.py`.
- **Маркеры pytest** и **allure-шаги** для читаемых отчётов.
- **Строгая типизация**: mypy в strict-режиме, аннотации во всех page objects и тестах.

## Структура

```
pages/
  base_page.py
  store/
    base_store_page.py
    catalog_page.py
    product_page.py
    cart_page.py
    checkout_page.py
    order_page.py
    orders_page.py
    components/
      shop_header.py
      product_card.py
      cart_row.py
      order_row.py
tests/            # 18 сценариев, по файлу на группу проверок
utils/            # build_url, parse_price
conftest.py       # фикстуры-состояния и page objects
config.py         # чтение .env
pyproject.toml    # pytest, black, isort, mypy
requirements.txt
.env.example
```

## Покрытие

- **Каталог**: смоук, поиск по названию/бренду, фильтры и сортировка, пагинация.
- **Товар**: страница товара, характеристики, отсутствие на складе, лимит склада.
- **Корзина**: арифметика и пересчёт, промокоды (регистр, порог, freeship),
  удаление и очистка через диалоги подтверждения.
- **Чекаут**: валидация контактов, доставка курьер/самовывоз, оплата картой
  (отказ банка и успех) и наличными.
- **Заказы**: список, порядок «новые сверху», навигация и persistence.
- **Инфраструктура**: перенос query-флагов, страница «не найдено»,
  перехват сети (загрузка / 500 / пустой каталог / контракт products.json),
  таймеры и жизненный цикл тостов.

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
pre-commit install
pytest -v
```

## Полезные команды

```bash
# видимый браузер и замедление для наблюдения
pytest -v --headed --slowmo 300

# только смоук
pytest -m smoke -v

# Allure-отчёт
pytest --alluredir=allure-results
allure serve allure-results

# линтеры и типы
pre-commit run --all-files
```

## Особенности площадки

- Единственный сетевой запрос магазина — `GET /mock/store/products.json`.
- Учебные флаги в query (`reset`, `delay`, `autohide`, `paymentDelay`)
  переносятся на все следующие адреса; `reset=1` очищает корзину и заказы.
- Корзина и заказы хранятся в `localStorage` браузера.