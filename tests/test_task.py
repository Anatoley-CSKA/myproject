"""Тесты для модуля task."""
from src.task import process_transactions


def test_process_transactions_empty() -> None:
    """Пустой список — пустой результат."""
    assert process_transactions([]) == []


def test_process_transactions_returns_list() -> None:
    """Функция возвращает список."""
    result = process_transactions([{"id": 1}])
    assert isinstance(result, list)


def test_process_transactions_preserves_data() -> None:
    """Данные сохраняются без изменений."""
    data = [{"id": 1, "amount": 100}]
    assert process_transactions(data) == data
