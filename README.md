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
