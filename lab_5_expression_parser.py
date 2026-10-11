"""
Модуль разбора выражений.
Превращает строку вида "2 + 3" в тройку (2.0, "+", 3.0).
"""


def parse_expression(text):
    """
    Разбирает строку формата "число оператор число".
    Элементы должны быть разделены пробелами.
    Возвращает кортеж (a, operator, b).
    При неверном формате выбрасывает ValueError.
    """
    # split() без аргументов делит строку по пробелам
    parts = text.split()

    if len(parts) != 3:
        raise ValueError("Выражение должно иметь вид: число оператор число")

    left, operator, right = parts

    try:
        # Заменяем запятую на точку, чтобы можно было писать 2,5
        a = float(left.replace(",", "."))
        b = float(right.replace(",", "."))
    except ValueError:
        raise ValueError("Операнды должны быть числами")

    return a, operator, b