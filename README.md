# Учебный проект по Python

---

## 🏗️ Модели данных: Product и Category

### Класс `Product`

Описывает товар в интернет-магазине.

| Атрибут | Тип | Описание |
|---------|-----|----------|
| `name` | `str` | Название товара |
| `description` | `str` | Описание товара |
| `price` | `float` | Цена (может быть с копейками) |
| `quantity` | `int` | Количество в наличии (штук) |

**Пример:**
```python
from src.models import Product

product = Product(
    name="iPhone 15",
    description="Смартфон Apple",
    price=99999.99,
    quantity=10,
)
print(product.name)   # iPhone 15
print(product.price)  # 99999.99


---

## 🔒 Приватные атрибуты и валидация

### Приватная цена и подтверждение понижения

Атрибут price в классе Product стал приватным (__price). Доступ — через геттер и сеттер.

Сеттер с проверками:
1. Если цена <= 0 — сообщение «Цена не должна быть нулевая или отрицательная», цена не меняется.
2. Если новая цена ниже текущей — запрос подтверждения (y — понизить, иначе — отмена).
3. Иначе — цена устанавливается.

### Приватный список товаров

Атрибут products в классе Category стал приватным (__products).

- add_product(product) — добавление товара.
- products (property) — строка с описанием всех товаров.

### Класс-метод new_product

Product.new_product(product_data, existing_products) создаёт товар из словаря. При совпадении имени: количество складывается, выбирается более высокая цена.

### Тестирование

poetry run pytest --cov=src --cov-report=term-missing

Покрытие всех модулей — 100%.

## ➕ Сложение товаров

У класса `Product` реализован магический метод `__add__`, который позволяет
получать общую стоимость товаров на складе:

```python
from src.models import Product

a = Product("Товар A", "Описание", 100, 10)   # 100 × 10 = 1000
b = Product("Товар B", "Описание", 200, 2)    # 200 × 2  = 400

total = a + b
print(total)   # 1400

---

## 🔄 Перебор товаров категории

Для итерации по товарам одной категории добавлен класс `CategoryIterator`.

```python
from src.models import Category, CategoryIterator, Product

category = Category("Фрукты", "Свежие", [
    Product("Яблоко", "Свежее", 80, 15),
    Product("Груша", "Спелая", 120, 8),
])

for product in CategoryIterator(category):
    print(product)
```

Также у `Category` появилось свойство `products_list`, возвращающее список объектов `Product`.
