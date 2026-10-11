from unittest.mock import Mock, patch
import pytest
from calculator import read_number
from lab_5_calculator_service import CalculatorService
from lab_5_history import History


@pytest.fixture
def history_mock():
    """Заглушка вместо настоящей истории"""
    return Mock(spec=History)


@pytest.fixture
def service(history_mock):
    """Сервис, в который вместо настоящей истории передана заглушка."""
    return CalculatorService(history_mock)


def test_evaluate_returns_correct_result(service):
    """Сервис считает правильно, хотя история - просто заглушка."""
    assert service.evaluate("2 + 3") == 5


def test_history_add_is_called_with_correct_arguments(service, history_mock):
    """
    assert_called_once_with проверяет два факта:
    метод вызвали ровно один раз и именно с такими аргументами.
    """
    service.evaluate("2 + 3")

    history_mock.add.assert_called_once_with("2 + 3", 5.0)


def test_history_add_is_called_for_each_calculation(service, history_mock):
    """call_count - сколько раз вызвали метод заглушки."""
    service.evaluate("1 + 1")
    service.evaluate("5 * 5")

    assert history_mock.add.call_count == 2


def test_division_by_zero_is_not_saved(service, history_mock):
    """При ошибке вычисления в историю ничего записываться не должно."""
    with pytest.raises(ZeroDivisionError):
        service.evaluate("5 / 0")

    # assert_not_called - заглушку не вызывали ни разу
    history_mock.add.assert_not_called()


def test_invalid_expression_is_not_saved(service, history_mock):
    """Неверный формат выражения тоже не попадает в историю."""
    with pytest.raises(ValueError):
        service.evaluate("abc + 1")

    history_mock.add.assert_not_called()


def test_unknown_operator_is_not_saved(service, history_mock):
    with pytest.raises(ValueError):
        service.evaluate("5 % 2")

    history_mock.add.assert_not_called()


# patch: подмена соседних модулей

@patch("lab_5_calculator_service.parse_expression")
def test_service_with_mocked_parser(mock_parse, service):
    """
    Изолируем сервис от настоящего парсера: заглушка сразу
    возвращает готовый результат разбора.
    """
    # return_value - что вернёт заглушка при вызове
    mock_parse.return_value = (10.0, "-", 4.0)

    result = service.evaluate("любая строка")

    assert result == 6.0
    # Проверяем, что сервис передал парсеру исходную строку
    mock_parse.assert_called_once_with("любая строка")


@patch("lab_5_calculator_service.parse_expression")
def test_service_when_parser_fails(mock_parse, service, history_mock):
    """
    side_effect с исключением: заглушка при вызове выбросит ошибку.
    Так можно имитировать сбой, который сложно получить по-настоящему.
    """
    mock_parse.side_effect = ValueError("Неверный формат")

    with pytest.raises(ValueError, match="Неверный формат"):
        service.evaluate("2 + 3")

    history_mock.add.assert_not_called()


def test_service_with_mocked_add_function():
    """
    Изолируем сервис от настоящей функции add из калькулятора.
    Сервис собирает словарь операций при создании, поэтому
    создаём его уже ВНУТРИ блока with.
    """
    with patch("lab_5_calculator_service.add", return_value=100) as mock_add:
        service = CalculatorService(Mock(spec=History))

        result = service.evaluate("2 + 3")

    # Вернулось значение заглушки, а не настоящая сумма
    assert result == 100
    # Сервис вызвал add с числами, которые разобрал парсер
    mock_add.assert_called_once_with(2.0, 3.0)


# =====================================================================
# Часть 3. Подмена ввода с клавиатуры
# =====================================================================
# Функция read_number вызывает input() и ждёт, пока пользователь
# что-то введёт. В тесте нам нужно, чтобы "пользователь" ввёл
# значение автоматически, поэтому подменяем встроенную функцию input.

@patch("builtins.input", return_value="2,5")
def test_read_number_with_comma(mock_input):
    """Заглушка input всегда возвращает строку "2,5"."""
    assert read_number("Введите число: ") == 2.5


@patch("builtins.input", return_value="7")
def test_read_number_passes_prompt_to_input(mock_input):
    """Проверяем, что приглашение попало в input."""
    read_number("Введите число: ")

    mock_input.assert_called_once_with("Введите число: ")


@patch("builtins.input", side_effect=["abc", "xyz", "5"])
def test_read_number_repeats_until_correct(mock_input):
    """
    side_effect со списком: при каждом вызове input вернёт
    следующее значение. Два раза неверный ввод, на третий - число.
    """
    result = read_number("Введите число: ")

    assert result == 5.0
    assert mock_input.call_count == 3