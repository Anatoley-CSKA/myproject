"""Тесты для модуля utils."""
import json

import pytest

from src.utils import load_settings, read_json


# ============================================================
# Тесты read_json
# ============================================================

def test_read_json_returns_dict(tmp_path) -> None:
    """read_json читает JSON-объект."""
    file = tmp_path / "test.json"
    file.write_text('{"key": "value"}', encoding="utf-8")

    result = read_json(str(file))
    assert result == {"key": "value"}


def test_read_json_returns_list(tmp_path) -> None:
    """read_json читает JSON-массив."""
    file = tmp_path / "test.json"
    file.write_text("[1, 2, 3]", encoding="utf-8")

    result = read_json(str(file))
    assert result == [1, 2, 3]


def test_read_json_nested(tmp_path) -> None:
    """read_json читает вложенные структуры."""
    data = {"users": [{"name": "Alice"}], "count": 1}
    file = tmp_path / "test.json"
    file.write_text(json.dumps(data), encoding="utf-8")

    result = read_json(str(file))
    assert result == data


def test_read_json_cyrillic(tmp_path) -> None:
    """read_json корректно читает кириллицу."""
    file = tmp_path / "test.json"
    file.write_text('{"name": "Иван"}', encoding="utf-8")

    result = read_json(str(file))
    assert result == {"name": "Иван"}


def test_read_json_empty_object(tmp_path) -> None:
    """read_json читает пустой объект."""
    file = tmp_path / "test.json"
    file.write_text("{}", encoding="utf-8")

    result = read_json(str(file))
    assert result == {}


def test_read_json_file_not_found() -> None:
    """read_json выбрасывает FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        read_json("nonexistent.json")


def test_read_json_invalid_json(tmp_path) -> None:
    """read_json выбрасывает JSONDecodeError."""
    file = tmp_path / "test.json"
    file.write_text("not a json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        read_json(str(file))


def test_load_settings_default_path() -> None:
    """load_settings загружает data/data.json по умолчанию."""
    result = load_settings()
    assert "user_currencies" in result
    assert "user_stocks" in result


def test_load_settings_custom_path(tmp_path) -> None:
    """load_settings работает с произвольным путём."""
    file = tmp_path / "custom.json"
    file.write_text('{"key": "value"}', encoding="utf-8")

    result = load_settings(str(file))
    assert result == {"key": "value"}


def test_main_block(capsys) -> None:
    """Проверяет блок __main__ в utils.py."""
    import runpy

    runpy.run_module("src.utils", run_name="__main__")
    captured = capsys.readouterr()
    assert "user_currencies" in captured.out


def test_load_categories_from_json(tmp_path) -> None:
    """Загрузка категорий и товаров из JSON."""
    import json

    from src.utils import load_categories_from_json

    data = [
        {
            "name": "Смартфоны",
            "description": "Мобильные телефоны",
            "products": [
                {
                    "name": "iPhone 15",
                    "description": "Смартфон Apple",
                    "price": 99999.99,
                    "quantity": 10,
                }
            ],
        }
    ]
    file = tmp_path / "products.json"
    file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    categories = load_categories_from_json(str(file))

    assert len(categories) == 1
    assert categories[0].name == "Смартфоны"
    assert len(categories[0].products) == 1
    assert categories[0].products[0].name == "iPhone 15"
    assert categories[0].products[0].price == 99999.99


def test_load_categories_from_json_empty(tmp_path) -> None:
    """Пустой JSON — пустой список категорий."""
    from src.utils import load_categories_from_json

    file = tmp_path / "empty.json"
    file.write_text("[]", encoding="utf-8")

    categories = load_categories_from_json(str(file))
    assert categories == []


def test_load_categories_from_json_no_products(tmp_path) -> None:
    """Категория без товаров."""
    import json

    from src.utils import load_categories_from_json

    data = [{"name": "Пустая", "description": "Описание", "products": []}]
    file = tmp_path / "empty_cat.json"
    file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    categories = load_categories_from_json(str(file))
    assert len(categories) == 1
    assert categories[0].products == []


def test_load_categories_creates_objects(tmp_path) -> None:
    """Функция создаёт объекты Product и Category."""
    import json

    from src.models import Category, Product
    from src.utils import load_categories_from_json

    data = [
        {
            "name": "Тест",
            "description": "Описание",
            "products": [
                {
                    "name": "Товар",
                    "description": "Описание товара",
                    "price": 100.0,
                    "quantity": 1,
                }
            ],
        }
    ]
    file = tmp_path / "test.json"
    file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    categories = load_categories_from_json(str(file))

    assert isinstance(categories[0], Category)
    assert isinstance(categories[0].products[0], Product)
