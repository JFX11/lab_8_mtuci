
# ---------- Часть 1. Логика калькулятора ----------

def add(a, b):
    """Сложение двух чисел."""
    return a + b


def subtract(a, b):
    """Вычитание: из a вычитаем b."""
    return a - b


def multiply(a, b):
    """Умножение двух чисел."""
    return a * b


def divide(a, b):
    """Деление a на b. При делении на ноль выбрасываем исключение."""
    if b == 0:
        # Проверяем сами, чтобы сообщение об ошибке было понятным
        raise ZeroDivisionError("Деление на ноль невозможно")
    return a / b


def power(a, b):
    """Возведение числа a в степень b."""
    # Если a = 0, а b отрицательное, ZeroDivisionError
    return a ** b


# ---------- Часть 2. Интерфейс пользователя ----------

def read_number(prompt):
    """
    Просит пользователя ввести число и повторяет запрос,
    пока не будет введено корректное значение.
    """
    while True:
        text = input(prompt)
        # Заменяем запятую на точку, чтобы можно было вводить 2,5
        text = text.replace(",", ".")
        try:
            return float(text)
        except ValueError:
            # float() не смог превратить строку в число (например, "abc")
            print("Ошибка: нужно ввести число. Попробуйте ещё раз.")


def print_menu():
    """Выводит меню доступных операций."""
    print("\n=== Калькулятор ===")
    print("1 - Сложение")
    print("2 - Вычитание")
    print("3 - Умножение")
    print("4 - Деление")
    print("5 - Возведение в степень")
    print("0 - Выход")


def main():
    """Главный цикл программы."""
    # Словарь: номер пункта меню -> функция, которую нужно вызвать
    operations = {
        "1": add,
        "2": subtract,
        "3": multiply,
        "4": divide,
        "5": power,
    }

    while True:
        print_menu()
        choice = input("Выберите операцию: ").strip()

        if choice == "0":
            print("До свидания!")
            break

        if choice not in operations:
            print("Ошибка: такого пункта нет в меню.")
            continue  # возвращаемся к началу цикла

        a = read_number("Введите первое число: ")
        b = read_number("Введите второе число: ")

        # Берём нужную функцию из словаря и вызываем её
        operation = operations[choice]
        try:
            result = operation(a, b)
            print(f"Результат: {result}")
        except ZeroDivisionError as error:
            # Ловим ошибку, чтобы программа не завершалась аварийно
            print(f"Ошибка: {error}")


# Этот блок запускается только при прямом запуске файла,
# но не при импорте (например, из файла с тестами)
if __name__ == "__main__":
    main()