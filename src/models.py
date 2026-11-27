"""Модели для интернет-магазина: Product и Category."""
from typing import Any, Dict, List, Optional


class Product:
    """Товар в интернет-магазине."""

    name: str
    description: str
    __price: float
    quantity: int

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    __repr__ = __str__   # удобно для отладки

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        if new_price < self.__price:
            answer = input(
                f"Новая цена {new_price} ниже текущей {self.__price}. "
                "Понизить цену? (y/n): "
            )
            if answer.strip().lower() != "y":
                print("Понижение цены отменено")
                return
        self.__price = new_price

    @classmethod
    def new_product(
        cls,
        product_data: Dict[str, Any],
        existing_products: Optional[List["Product"]] = None,
    ) -> "Product":
        name = product_data["name"]
        description = product_data["description"]
        price = float(product_data["price"])
        quantity = int(product_data["quantity"])

        if existing_products:
            for existing in existing_products:
                if existing.name == name:
                    existing.quantity += quantity
                    existing.price = max(existing.price, price)
                    return existing

        return cls(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
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
        self.name = name
        self.description = description
        self.__products = list(products)
        Category.category_count += 1
        Category.product_count += len(self.__products)

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product: Product) -> None:
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        return "\n".join(str(p) for p in self.__products)


# === Проверка ===
if __name__ == "__main__":
    p1 = Product("Яблоко", "Свежее", 80, 15)
    p2 = Product("Груша", "Спелая", 120, 8)

    cat = Category("Фрукты", "Свежие фрукты", [p1, p2])
    cat.add_product(Product("Апельсин", "Сочный", 90, 20))

    print(p1)
    # Яблоко, 80 руб. Остаток: 15 шт.

    print(cat)
    # Фрукты, количество продуктов: 43 шт.

    print(cat.products)
    # Яблоко, 80 руб. Остаток: 15 шт.
    # Груша, 120 руб. Остаток: 8 шт.
    # Апельсин, 90 руб. Остаток: 20 шт.
