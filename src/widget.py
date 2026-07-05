from src.masks import get_mask_card_number, get_mask_account

def mask_account_card(info: str) -> str:
    """
    Принимает строку с типом и номером карты/счета, возвращает строку с замаскированным номером.
    Пример: "Visa Platinum 7000792289606361" -> "Visa Platinum 7000 79** **** 6361"
             "Счет 73654108430135874305" -> "Счет **4305"
    """
    parts = info.rsplit(" ", 1)
    if len(parts) != 2:
        raise ValueError("Неверный формат строки: должно быть 'тип номер'")
    type_part, number = parts[0], parts[1]
    if number.isdigit():
        if len(number) == 16:
            masked = get_mask_card_number(number)
        elif len(number) >= 4:
            masked = get_mask_account(number)
        else:
            raise ValueError("Номер слишком короткий")
        return f"{type_part} {masked}"
    else:
        raise ValueError("Номер должен содержать только цифры")

def get_date(date_str: str) -> str:
    """
    Принимает строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает "11.03.2024"
    """
    from datetime import datetime
    date_part = date_str.split("T")[0]
    dt = datetime.strptime(date_part, "%Y-%m-%d")
    return dt.strftime("%d.%m.%Y")
