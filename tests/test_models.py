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
