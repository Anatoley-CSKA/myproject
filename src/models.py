"""Модели для интернет-магазина: Product и Category."""
from typing import List


class Product:
    """Товар в интернет-магазине."""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ) -> None:
        """Инициализация товара.

        :param name: название товара
        :param description: описание товара
        :param price: цена
        :param quantity: количество в наличии
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Категория товаров."""

    # Атрибуты класса — общие для всех объектов
    category_count: int = 0
    product_count: int = 0

    # Атрибуты экземпляра
    name: str
    description: str
    products: List[Product]

    def __init__(
        self,
        name: str,
        description: str,
        products: List[Product],
    ) -> None:
        """Инициализация категории.

        :param name: название категории
        :param description: описание категории
        :param products: список объектов Product
        """
        # Атрибуты экземпляра — у каждого объекта свои
        self.name = name
        self.description = description
        self.products = products

        # Атрибуты класса — общие для всех объектов
        Category.category_count += 1
        Category.product_count += len(products)
