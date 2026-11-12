"""Модели для интернет-магазина: Product и Category."""
from typing import Any, Dict, List


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

    @classmethod
    def new_product(cls, product_data: Dict[str, Any]) -> "Product":
        """Создаёт объект Product из словаря.

        :param product_data: словарь с ключами name, description, price, quantity
        :return: объект Product
        """
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=float(product_data["price"]),
            quantity=int(product_data["quantity"]),
        )


class Category:
    """Категория товаров."""

    category_count: int = 0
    product_count: int = 0

    name: str
    description: str
    __products: List[Product]

    def __init__(
        self,
        name: str,
        description: str,
        products: List[Product],
    ) -> None:
        """Инициализация категории."""
        self.name = name
        self.description = description
        self.__products = list(products)
        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        """Добавляет товар в категорию."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает строку с описанием всех товаров."""
        result = ""
        for p in self.__products:
            result += f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт." + chr(10)
        return result
