from src.widget import mask_account_card, get_date


def test_mask_account_card_card():
    assert (
        mask_account_card("Visa Platinum 7000792289606361")
        == "Visa Platinum 7000 79** **** 6361"
    )
    assert (
        mask_account_card("Maestro 1596837868705199") == "Maestro 1596 83** **** 5199"
    )


def test_mask_account_card_account():
    assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"


def test_get_date():
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"


def test_mask_account_card_short_number() -> None:
    """Слишком короткий номер — ошибка."""
    import pytest
    from src.widget import mask_account_card

    with pytest.raises(ValueError, match="Номер слишком короткий"):
        mask_account_card("Visa 123")


def test_get_date_invalid_format() -> None:
    """Неверный формат даты — ошибка."""
    import pytest
    from src.widget import get_date

    with pytest.raises(ValueError):
        get_date("2024/03/11")


def test_get_date_empty() -> None:
    """Пустая строка — ошибка."""
    import pytest
    from src.widget import get_date

    with pytest.raises(ValueError):
        get_date("")


def test_mask_account_card_no_space() -> None:
    """Строка без пробела — ошибка (строка 15)."""
    import pytest
    from src.widget import mask_account_card

    with pytest.raises(
        ValueError, match="Неверный формат строки: должно быть 'тип номер'"
    ):
        mask_account_card("Visa")


def test_mask_account_card_non_digit() -> None:
    """Номер с буквами — ошибка (строка 26)."""
    import pytest
    from src.widget import mask_account_card

    with pytest.raises(
        ValueError, match="Номер должен содержать только цифры"
    ):
        mask_account_card("Visa 1234abcd5678efgh")
