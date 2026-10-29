"""Утилиты для работы с файлами."""
import json
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models import Category


def read_json(path: str) -> dict:
    """Читает JSON-файл относительно корня проекта."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, path)
    with open(full_path, "r", encoding="UTF-8") as file:
        return json.load(file)


def load_settings(path: str = "data/data.json") -> dict:
    """Загружает настройки пользователя.

    :param path: путь к JSON-файлу относительно корня проекта
    :return: словарь с настройками
    """
    return read_json(path)


def load_categories_from_json(path: str) -> list["Category"]:
    """Загружает категории и товары из JSON-файла.

    :param path: путь к JSON-файлу относительно корня проекта
    :return: список объектов Category
    """
    from src.models import Category, Product

    data = read_json(path)
    categories: list[Category] = []

    for cat_data in data:
        products = [
            Product(
                name=p["name"],
                description=p["description"],
                price=float(p["price"]),
                quantity=int(p["quantity"]),
            )
            for p in cat_data.get("products", [])
        ]
        category = Category(
            name=cat_data["name"],
            description=cat_data["description"],
            products=products,
        )
        categories.append(category)

    return categories


if __name__ == "__main__":
    print(load_settings())
