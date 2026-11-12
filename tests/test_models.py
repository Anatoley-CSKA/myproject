import pytest
from src.models import Category, Product


@pytest.fixture(autouse=True)
def reset_counters():
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def product_iphone():
    return Product("iPhone 15", "Apple", 99999.99, 10)


@pytest.fixture
def product_galaxy():
    return Product("Galaxy S24", "Samsung", 89999.50, 5)


@pytest.fixture
def category(product_iphone):
    return Category("Смартфоны", "Телефоны", [product_iphone])


def test_product_init(product_iphone):
    assert product_iphone.name == "iPhone 15"
    assert product_iphone.price == 99999.99
    assert product_iphone.quantity == 10


def test_products_returns_string(category):
    assert isinstance(category.products, str)


def test_products_format(category):
    assert "iPhone 15, 99999.99 руб. Остаток: 10 шт." in category.products


def test_products_multiple(product_iphone, product_galaxy):
    cat = Category("Тест", "Описание", [product_iphone, product_galaxy])
    result = cat.products
    assert "iPhone 15" in result
    assert "Galaxy S24" in result


def test_products_empty():
    cat = Category("Пустая", "Описание", [])
    assert cat.products == ""


def test_products_is_private(category):
    with pytest.raises(AttributeError):
        _ = category.__products


def test_add_product(category, product_galaxy):
    before = category.products.count(chr(10))
    category.add_product(product_galaxy)
    after = category.products.count(chr(10))
    assert after > before


def test_add_product_increments_count(category, product_galaxy):
    assert Category.product_count == 1
    category.add_product(product_galaxy)
    assert Category.product_count == 2


def test_category_count_increments(product_iphone):
    assert Category.category_count == 0
    Category("A", "", [product_iphone])
    assert Category.category_count == 1


def test_new_product_creates_object():
    """new_product создаёт объект Product из словаря."""
    data = {
        "name": "iPhone 15",
        "description": "Смартфон Apple",
        "price": 99999.99,
        "quantity": 10,
    }
    product = Product.new_product(data)

    assert isinstance(product, Product)
    assert product.name == "iPhone 15"
    assert product.description == "Смартфон Apple"
    assert product.price == 99999.99
    assert product.quantity == 10


def test_new_product_converts_types():
    """new_product приводит price к float, quantity к int."""
    data = {
        "name": "Тест",
        "description": "Описание",
        "price": "199.99",
        "quantity": "5",
    }
    product = Product.new_product(data)

    assert isinstance(product.price, float)
    assert isinstance(product.quantity, int)


def test_new_product_with_category():
    """new_product работает с Category."""
    from src.models import Category

    data = {
        "name": "Товар",
        "description": "Описание",
        "price": 100.0,
        "quantity": 1,
    }
    product = Product.new_product(data)
    category = Category("Тест", "Описание", [product])

    assert "Товар" in category.products


def test_new_product_without_duplicates():
    """Новый товар создаётся, если дубликатов нет."""
    existing = [Product("Galaxy S24", "Samsung", 89999.5, 5)]
    data = {
        "name": "iPhone 15",
        "description": "Apple",
        "price": 99999.99,
        "quantity": 10,
    }

    product = Product.new_product(data, existing)

    assert product.name == "iPhone 15"
    assert product.quantity == 10
    assert product.price == 99999.99
    assert len(existing) == 1  # не добавился автоматически


def test_new_product_merges_quantity():
    """Количество складывается при совпадении имени."""
    existing = [Product("iPhone 15", "Apple", 90000.0, 10)]
    data = {
        "name": "iPhone 15",
        "description": "Apple",
        "price": 90000.0,
        "quantity": 5,
    }

    product = Product.new_product(data, existing)

    assert product.quantity == 15
    assert product is existing[0]


def test_new_product_picks_higher_price():
    """Выбирается более высокая цена."""
    existing = [Product("iPhone 15", "Apple", 90000.0, 10)]
    data = {
        "name": "iPhone 15",
        "description": "Apple",
        "price": 99999.99,
        "quantity": 5,
    }

    product = Product.new_product(data, existing)

    assert product.price == 99999.99


def test_new_product_keeps_higher_existing_price():
    """Если старая цена выше — остаётся она."""
    existing = [Product("iPhone 15", "Apple", 120000.0, 10)]
    data = {
        "name": "iPhone 15",
        "description": "Apple",
        "price": 90000.0,
        "quantity": 5,
    }

    product = Product.new_product(data, existing)

    assert product.price == 120000.0


def test_new_product_empty_list():
    """Пустой список — создаётся новый товар."""
    data = {
        "name": "iPhone 15",
        "description": "Apple",
        "price": 99999.99,
        "quantity": 10,
    }

    product = Product.new_product(data, [])

    assert product.name == "iPhone 15"
    assert product.quantity == 10


def test_new_product_none_list():
    """None вместо списка — создаётся новый товар."""
    data = {
        "name": "iPhone 15",
        "description": "Apple",
        "price": 99999.99,
        "quantity": 10,
    }

    product = Product.new_product(data, None)

    assert product.name == "iPhone 15"


def test_price_getter(product_iphone):
    """Геттер возвращает цену."""
    assert product_iphone.price == 99999.99


def test_price_setter_valid(product_iphone):
    """Сеттер устанавливает корректную цену (повышение)."""
    product_iphone.price = 150000.0
    assert product_iphone.price == 150000.0


def test_price_setter_zero(product_iphone, capsys):
    """Нулевая цена — сообщение, цена не меняется."""
    product_iphone.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product_iphone.price == 99999.99


def test_price_setter_negative(product_iphone, capsys):
    """Отрицательная цена — сообщение, цена не меняется."""
    product_iphone.price = -100
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product_iphone.price == 99999.99


def test_price_is_private(product_iphone):
    """Атрибут __price недоступен напрямую."""
    with pytest.raises(AttributeError):
        _ = product_iphone.__price


def test_price_setter_lower_confirmed(product_iphone, monkeypatch):
    """Понижение с подтверждением 'y' — цена меняется."""
    monkeypatch.setattr("builtins.input", lambda _: "y")
    product_iphone.price = 50000.0
    assert product_iphone.price == 50000.0


def test_price_setter_lower_cancelled(product_iphone, monkeypatch, capsys):
    """Понижение с отменой — цена не меняется."""
    monkeypatch.setattr("builtins.input", lambda _: "n")
    product_iphone.price = 50000.0

    captured = capsys.readouterr()
    assert "Понижение цены отменено" in captured.out
    assert product_iphone.price == 99999.99


def test_price_setter_lower_random_answer(product_iphone, monkeypatch, capsys):
    """Любой ответ кроме 'y' — отмена."""
    monkeypatch.setattr("builtins.input", lambda _: "maybe")
    product_iphone.price = 50000.0

    captured = capsys.readouterr()
    assert "Понижение цены отменено" in captured.out
    assert product_iphone.price == 99999.99


def test_price_setter_higher_no_input(product_iphone, monkeypatch):
    """Повышение цены — без input."""
    def fail_input(_):
        raise AssertionError("input не должен вызываться")

    monkeypatch.setattr("builtins.input", fail_input)
    product_iphone.price = 150000.0
    assert product_iphone.price == 150000.0


def test_price_setter_zero_no_input(product_iphone, monkeypatch, capsys):
    """Нулевая цена — без input, только сообщение."""
    def fail_input(_):
        raise AssertionError("input не должен вызываться")

    monkeypatch.setattr("builtins.input", fail_input)
    product_iphone.price = 0

    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product_iphone.price == 99999.99


# ============================================================
# Тесты сеттера цены с подтверждением
# ============================================================

def test_price_setter_decrease_confirmed(product_iphone, monkeypatch):
    """Понижение с 'y' — цена меняется."""
    monkeypatch.setattr("builtins.input", lambda _: "y")
    product_iphone.price = 50000.0
    assert product_iphone.price == 50000.0


def test_price_setter_decrease_confirmed_uppercase(product_iphone, monkeypatch):
    """Понижение с 'Y' — тоже работает."""
    monkeypatch.setattr("builtins.input", lambda _: "Y")
    product_iphone.price = 50000.0
    assert product_iphone.price == 50000.0


def test_price_setter_decrease_confirmed_with_spaces(product_iphone, monkeypatch):
    """Понижение с ' y ' — работает (strip)."""
    monkeypatch.setattr("builtins.input", lambda _: "  y  ")
    product_iphone.price = 50000.0
    assert product_iphone.price == 50000.0


def test_price_setter_decrease_cancelled(product_iphone, monkeypatch, capsys):
    """Понижение с 'n' — отмена, цена не меняется."""
    monkeypatch.setattr("builtins.input", lambda _: "n")
    product_iphone.price = 50000.0

    captured = capsys.readouterr()
    assert "Понижение цены отменено" in captured.out
    assert product_iphone.price == 99999.99


def test_price_setter_decrease_empty_answer(product_iphone, monkeypatch, capsys):
    """Пустой ответ — отмена."""
    monkeypatch.setattr("builtins.input", lambda _: "")
    product_iphone.price = 50000.0

    captured = capsys.readouterr()
    assert "Понижение цены отменено" in captured.out
    assert product_iphone.price == 99999.99


def test_price_setter_decrease_random_answer(product_iphone, monkeypatch, capsys):
    """Случайный ответ — отмена."""
    monkeypatch.setattr("builtins.input", lambda _: "maybe")
    product_iphone.price = 50000.0

    captured = capsys.readouterr()
    assert "Понижение цены отменено" in captured.out
    assert product_iphone.price == 99999.99


def test_price_setter_equal_price_no_input(product_iphone, monkeypatch):
    """Равная цена — без input."""
    def fail_input(_):
        raise AssertionError("input не должен вызываться")

    monkeypatch.setattr("builtins.input", fail_input)
    product_iphone.price = 99999.99
    assert product_iphone.price == 99999.99


def test_price_setter_increase_no_input(product_iphone, monkeypatch):
    """Повышение — без input."""
    def fail_input(_):
        raise AssertionError("input не должен вызываться")

    monkeypatch.setattr("builtins.input", fail_input)
    product_iphone.price = 150000.0
    assert product_iphone.price == 150000.0


def test_price_setter_negative_no_input(product_iphone, monkeypatch, capsys):
    """Отрицательная цена — без input, только сообщение."""
    def fail_input(_):
        raise AssertionError("input не должен вызываться")

    monkeypatch.setattr("builtins.input", fail_input)
    product_iphone.price = -100

    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product_iphone.price == 99999.99


# ============================================================
# Интеграционные тесты: new_product + сеттер
# ============================================================

def test_new_product_merges_price_via_setter(monkeypatch):
    """new_product использует сеттер — понижение цены подтверждается."""
    monkeypatch.setattr("builtins.input", lambda _: "y")

    existing = [Product("iPhone 15", "Apple", 120000.0, 10)]
    data = {
        "name": "iPhone 15",
        "description": "Apple",
        "price": 90000.0,
        "quantity": 5,
    }

    product = Product.new_product(data, existing)

    # Цена должна остаться 120000 (max), сеттер не вызывается
    assert product.price == 120000.0
    assert product.quantity == 15


def test_new_product_picks_higher_without_input(monkeypatch):
    """Если новая цена выше — input не вызывается."""
    def fail_input(_):
        raise AssertionError("input не должен вызываться")

    monkeypatch.setattr("builtins.input", fail_input)

    existing = [Product("iPhone 15", "Apple", 90000.0, 10)]
    data = {
        "name": "iPhone 15",
        "description": "Apple",
        "price": 99999.99,
        "quantity": 5,
    }

    product = Product.new_product(data, existing)

    assert product.price == 99999.99
    assert product.quantity == 15


# ============================================================
# Тесты граничных случаев
# ============================================================

def test_price_setter_very_small_decrease(product_iphone, monkeypatch):
    """Понижение на копейку — тоже требует подтверждения."""
    monkeypatch.setattr("builtins.input", lambda _: "y")
    product_iphone.price = 99999.98
    assert product_iphone.price == 99999.98


def test_price_setter_very_small_increase(product_iphone, monkeypatch):
    """Повышение на копейку — без подтверждения."""
    def fail_input(_):
        raise AssertionError("input не должен вызываться")

    monkeypatch.setattr("builtins.input", fail_input)
    product_iphone.price = 100000.0
    assert product_iphone.price == 100000.0


def test_new_product_empty_existing_list():
    """Пустой список existing — создаётся новый товар."""
    data = {
        "name": "iPhone 15",
        "description": "Apple",
        "price": 99999.99,
        "quantity": 10,
    }
    product = Product.new_product(data, [])
    assert product.name == "iPhone 15"
    assert product.quantity == 10


def test_new_product_none_existing():
    """None вместо списка — создаётся новый товар."""
    data = {
        "name": "iPhone 15",
        "description": "Apple",
        "price": 99999.99,
        "quantity": 10,
    }
    product = Product.new_product(data, None)
    assert product.name == "iPhone 15"


def test_new_product_different_names_no_merge():
    """Разные имена — не объединяются."""
    existing = [Product("Galaxy S24", "Samsung", 89999.5, 5)]
    data = {
        "name": "iPhone 15",
        "description": "Apple",
        "price": 99999.99,
        "quantity": 10,
    }
    product = Product.new_product(data, existing)
    assert product.name == "iPhone 15"
    assert existing[0].quantity == 5  # не изменился
