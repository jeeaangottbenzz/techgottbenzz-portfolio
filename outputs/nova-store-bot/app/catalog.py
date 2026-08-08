from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Product:
    id: str
    category: str
    name: str
    description: str
    price: int
    sku: str
    stock: int
    placeholder: str


CATEGORIES = {
    "clothing": "Одежда",
    "accessories": "Аксессуары",
    "new": "Новинки",
}

PRODUCTS = (
    Product("oversize_tee", "clothing", "Футболка Oversize", "Плотный хлопок и свободный силуэт.", 2490, "NOVA-TS-01", 12, "👕"),
    Product("basic_hoodie", "clothing", "Худи Base", "Мягкое худи с минималистичной вышивкой.", 4990, "NOVA-HD-02", 8, "🧥"),
    Product("wide_jeans", "clothing", "Джинсы Wide", "Свободная посадка и плотный деним.", 5790, "NOVA-JN-03", 6, "👖"),
    Product("linen_shirt", "clothing", "Рубашка Linen", "Лёгкая рубашка прямого кроя.", 4190, "NOVA-SH-04", 9, "👔"),
    Product("city_cap", "accessories", "Кепка City", "Базовая кепка с регулируемой посадкой.", 1790, "NOVA-CP-05", 15, "🧢"),
    Product("mini_bag", "accessories", "Сумка Mini", "Компактная сумка для повседневных вещей.", 3290, "NOVA-BG-06", 7, "👜"),
    Product("steel_bottle", "accessories", "Бутылка Steel", "Термобутылка из нержавеющей стали.", 2190, "NOVA-BT-07", 18, "🥤"),
    Product("soft_scarf", "accessories", "Шарф Soft", "Мягкий однотонный шарф для прохладной погоды.", 1990, "NOVA-SC-08", 10, "🧣"),
    Product("nova_bomber", "new", "Бомбер NOVA", "Лёгкий бомбер с контрастной подкладкой.", 7490, "NOVA-NW-09", 5, "🧥"),
    Product("crossbody", "new", "Сумка Crossbody", "Функциональная сумка с двумя отделениями.", 3890, "NOVA-NW-10", 11, "🎒"),
    Product("longsleeve", "new", "Лонгслив Line", "Лонгслив из мягкого хлопкового трикотажа.", 2990, "NOVA-NW-11", 14, "👚"),
    Product("sneakers", "new", "Кеды Mono", "Лаконичные текстильные кеды на каждый день.", 5490, "NOVA-NW-12", 4, "👟"),
)

PRODUCTS_BY_ID = {product.id: product for product in PRODUCTS}


def products_for_category(category: str) -> tuple[Product, ...]:
    return tuple(product for product in PRODUCTS if product.category == category)

