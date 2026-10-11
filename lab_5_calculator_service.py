from calculator import add, subtract, multiply, divide, power
from lab_5_expression_parser import parse_expression


class CalculatorService:
    """Вычисляет выражения-строки и записывает их в историю."""

    def __init__(self, history):

        self.history = history
        # Соответствие символа оператора и функции калькулятора
        self.operations = {
            "+": add,
            "-": subtract,
            "*": multiply,
            "/": divide,
            "^": power,
        }

    def evaluate(self, text):

        a, operator, b = parse_expression(text)

        if operator not in self.operations:
            raise ValueError(f"Неизвестный оператор: {operator}")

        result = self.operations[operator](a, b)
        self.history.add(text.strip(), result)

        return result

# Этот блок выполняется только при прямом запуске файла
if __name__ == "__main__":
    from lab_5_history import History

    history = History("history.json")
    service = CalculatorService(history)

    print(service.evaluate("2 + 3"))
    print(service.evaluate("10 / 4"))
    print(history.get_all())