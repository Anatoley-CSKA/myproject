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
