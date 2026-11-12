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
        """Инициализация товара."""
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Категория товаров."""

    # Атрибуты класса — общие для всех объектов
    category_count: int = 0
    product_count: int = 0

    name: str
    description: str
    __products: List[Product]  # приватный атрибут

    def __init__(
        self,
        name: str,
        description: str,
        products: List[Product],
    ) -> None:
        """Инициализация категории.

        :param name: название категории
        :param description: описание категории
        :param products: список товаров
        """
        self.name = name
        self.description = description
        self.__products = list(products)

        # Увеличиваем счётчики
        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        """Добавляет товар в категорию.

        :param product: объект Product
        """
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> List[Product]:
        """Возвращает список товаров категории (только для чтения)."""
        return self.__products
