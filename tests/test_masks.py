from src.masks import get_mask_card_number, get_mask_account


def test_get_mask_card_number():
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"


def test_get_mask_account():
    assert get_mask_account("73654108430135874305") == "**4305"


def test_get_mask_card_number_invalid_length() -> None:
    """Неверная длина номера карты."""
    import pytest
    from src.masks import get_mask_card_number

    with pytest.raises(ValueError, match="Card number must contain 16 digits"):
        get_mask_card_number("123")


def test_get_mask_account_invalid_length() -> None:
    """Неверная длина номера счёта."""
    import pytest
    from src.masks import get_mask_account

    with pytest.raises(
        ValueError, match="Account number must contain at least 4 digits"
    ):
        get_mask_account("12")
