import re


def parse_price(text: str) -> int:
    """Достаёт целое число из строки цены вида «8 490 ₽»."""
    # Убираем всё, кроме цифр. Так не зависим ни от вида пробела, ни от валюты
    digits = re.sub(r"\D", "", text)
    return int(digits)
