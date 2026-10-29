"""Полные тесты для классов Product и Category."""
import pytest

from src.models import Category, Product


# ============================================================
# Фикстуры
# ============================================================

@pytest.fixture(autouse=True)
def reset_category_counters() -> None:
    """Сбрасывает счётчики Category перед каждым тестом.

    Атрибуты класса общие для всех объектов и «накапливаются»
    между тестами. Без сброса тесты будут зависеть друг от друга.
    """
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def product_iphone() -> Product:
    """Товар: iPhone."""
    return Product(
        name="iPhone 15",
        description="Смартфон Apple",
        price=99999.99,
        quantity=10,
    )


@pytest.fixture
def product_galaxy() -> Product:
    """Товар: Galaxy."""
    return Product(
        name="Galaxy S24",
        description="Смартфон Samsung",
        price=89999.50,
        quantity=5,
    )


@pytest.fixture
def product_macbook() -> Product:
    """Товар: MacBook."""
    return Product(
        name="MacBook Pro",
        description="Ноутбук Apple",
        price=249999.00,
        quantity=3,
    )


@pytest.fixture
def category_smartphones(
    product_iphone: Product,
    product_galaxy: Product,
) -> Category:
    """Категория: Смартфоны (2 товара)."""
    return Category(
        name="Смартфоны",
        description="Мобильные телефоны",
        products=[product_iphone, product_galaxy],
    )


@pytest.fixture
def category_laptops(product_macbook: Product) -> Category:
    """Категория: Ноутбуки (1 товар)."""
    return Category(
        name="Ноутбуки",
        description="Портативные компьютеры",
        products=[product_macbook],
    )


# ============================================================
# 1. Тесты для Product — инициализация
# ============================================================

def test_product_init(product_iphone: Product) -> None:
    """Корректность инициализации Product."""
    assert product_iphone.name == "iPhone 15"
    assert product_iphone.description == "Смартфон Apple"
    assert product_iphone.price == 99999.99
    assert product_iphone.quantity == 10


def test_product_types(product_iphone: Product) -> None:
    """Типы атрибутов Product."""
    assert isinstance(product_iphone.name, str)
    assert isinstance(product_iphone.description, str)
    assert isinstance(product_iphone.price, float)
    assert isinstance(product_iphone.quantity, int)


def test_product_price_with_kopecks() -> None:
    """Цена может быть с копейками."""
    product = Product("Тест", "Описание", 199.99, 1)
    assert product.price == 199.99


def test_product_zero_quantity() -> None:
    """Товар с нулевым количеством."""
    product = Product("Тест", "Описание", 100.0, 0)
    assert product.quantity == 0


def test_products_are_independent(
    product_iphone: Product,
    product_galaxy: Product,
) -> None:
    """Два товара — независимые объекты."""
    assert product_iphone is not product_galaxy
    assert product_iphone.name != product_galaxy.name


# ============================================================
# 2. Тесты для Category — инициализация
# ============================================================

def test_category_init(category_smartphones: Category) -> None:
    """Корректность инициализации Category."""
    assert category_smartphones.name == "Смартфоны"
    assert category_smartphones.description == "Мобильные телефоны"
    assert len(category_smartphones.products) == 2


def test_category_products_are_products(category_smartphones: Category) -> None:
    """В products хранятся объекты Product."""
    assert all(isinstance(p, Product) for p in category_smartphones.products)


def test_category_types(category_smartphones: Category) -> None:
    """Типы атрибутов Category."""
    assert isinstance(category_smartphones.name, str)
    assert isinstance(category_smartphones.description, str)
    assert isinstance(category_smartphones.products, list)


def test_category_empty_products() -> None:
    """Категория без товаров."""
    category = Category("Пустая", "Описание", [])
    assert category.products == []
    assert len(category.products) == 0


def test_categories_are_independent(
    category_smartphones: Category,
    category_laptops: Category,
) -> None:
    """Две категории — независимые объекты."""
    assert category_smartphones is not category_laptops
    assert category_smartphones.name != category_laptops.name


# ============================================================
# 3. Тесты подсчёта категорий
# ============================================================

def test_category_count_starts_at_zero() -> None:
    """До создания категорий счётчик = 0."""
    assert Category.category_count == 0


def test_category_count_increments(product_iphone: Product) -> None:
    """Счётчик категорий увеличивается при создании."""
    assert Category.category_count == 0

    Category("Смартфоны", "Описание", [product_iphone])
    assert Category.category_count == 1

    Category("Ноутбуки", "Описание", [product_iphone])
    assert Category.category_count == 2


def test_category_count_shared(
    product_iphone: Product,
    product_galaxy: Product,
) -> None:
    """Счётчик категорий общий для всех объектов."""
    cat1 = Category("Смартфоны", "Описание", [product_iphone])
    cat2 = Category("Ноутбуки", "Описание", [product_galaxy])

    assert Category.category_count == 2
    assert cat1.category_count == 2
    assert cat2.category_count == 2


def test_category_count_many(
    category_smartphones: Category,
    category_laptops: Category,
) -> None:
    """Счётчик после создания нескольких категорий."""
    assert Category.category_count == 2


# ============================================================
# 4. Тесты подсчёта продуктов
# ============================================================

def test_product_count_starts_at_zero() -> None:
    """До создания категорий счётчик товаров = 0."""
    assert Category.product_count == 0


def test_product_count_increments(
    product_iphone: Product,
    product_galaxy: Product,
) -> None:
    """Счётчик товаров увеличивается на длину products."""
    assert Category.product_count == 0

    Category("Смартфоны", "Описание", [product_iphone, product_galaxy])
    assert Category.product_count == 2

    Category("Ноутбуки", "Описание", [product_iphone])
    assert Category.product_count == 3


def test_product_count_empty_category() -> None:
    """Пустая категория не увеличивает счётчик товаров."""
    assert Category.product_count == 0

    Category("Пустая", "Описание", [])
    assert Category.category_count == 1
    assert Category.product_count == 0


def test_product_count_shared(
    product_iphone: Product,
    product_galaxy: Product,
) -> None:
    """Счётчик товаров общий для всех объектов."""
    cat1 = Category("Смартфоны", "Описание", [product_iphone])
    cat2 = Category("Ноутбуки", "Описание", [product_galaxy])

    assert Category.product_count == 2
    assert cat1.product_count == 2
    assert cat2.product_count == 2


def test_product_count_many(
    category_smartphones: Category,
    category_laptops: Category,
) -> None:
    """Счётчик товаров после создания нескольких категорий."""
    assert Category.product_count == 3  # 2 + 1


# ============================================================
# 5. Интеграционные тесты
# ============================================================

def test_full_scenario(
    product_iphone: Product,
    product_galaxy: Product,
    product_macbook: Product,
) -> None:
    """Полный сценарий: создание товаров и категорий."""
    assert Category.category_count == 0
    assert Category.product_count == 0

    cat1 = Category("Смартфоны", "Описание", [product_iphone, product_galaxy])
    assert Category.category_count == 1
    assert Category.product_count == 2

    cat2 = Category("Ноутбуки", "Описание", [product_macbook])
    assert Category.category_count == 2
    assert Category.product_count == 3

    # Проверяем, что данные объектов корректны
    assert cat1.products[0].name == "iPhone 15"
    assert cat2.products[0].name == "MacBook Pro"


def test_shared_counter_via_instances(
    category_smartphones: Category,
    category_laptops: Category,
) -> None:
    """Счётчики видны через любой объект."""
    assert category_smartphones.category_count == 2
    assert category_laptops.category_count == 2
    assert category_smartphones.product_count == 3
    assert category_laptops.product_count == 3


# ============================================================
# 6. Тесты типизации
# ============================================================

def test_product_attributes_have_correct_types(product_iphone: Product) -> None:
    """Атрибуты Product имеют правильные типы."""
    assert type(product_iphone.name) is str
    assert type(product_iphone.description) is str
    assert type(product_iphone.price) is float
    assert type(product_iphone.quantity) is int


def test_category_attributes_have_correct_types(category_smartphones: Category) -> None:
    """Атрибуты Category имеют правильные типы."""
    assert type(category_smartphones.name) is str
    assert type(category_smartphones.description) is str
    assert type(category_smartphones.products) is list
