from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from .catalog import CATEGORIES, Product


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Каталог"), KeyboardButton(text="Корзина")],
            [KeyboardButton(text="Мои заказы")],
            [KeyboardButton(text="Доставка и оплата"), KeyboardButton(text="Контакты")],
            [KeyboardButton(text="FAQ")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите раздел",
    )


def categories_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=label, callback_data=f"category:{key}")]
            for key, label in CATEGORIES.items()
        ]
    )


def products_keyboard(products: tuple[Product, ...]) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=f"{product.placeholder} {product.name}", callback_data=f"product:{product.id}")]
        for product in products
    ]
    rows.append([InlineKeyboardButton(text="← Категории", callback_data="catalog:back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def product_keyboard(product_id: str, category: str, available: bool) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    if available:
        rows.append([InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add:{product_id}")])
    rows.append([InlineKeyboardButton(text="← К товарам", callback_data=f"category:{category}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def cart_keyboard(items: list[dict]) -> InlineKeyboardMarkup | None:
    if not items:
        return None
    rows: list[list[InlineKeyboardButton]] = []
    for item in items:
        product_id = item["product_id"]
        rows.append([InlineKeyboardButton(text=item["name"], callback_data="cart:noop")])
        rows.append(
            [
                InlineKeyboardButton(text="−", callback_data=f"cart:dec:{product_id}"),
                InlineKeyboardButton(text=str(item["quantity"]), callback_data="cart:noop"),
                InlineKeyboardButton(text="+", callback_data=f"cart:inc:{product_id}"),
                InlineKeyboardButton(text="Удалить", callback_data=f"cart:remove:{product_id}"),
            ]
        )
    rows.extend(
        (
            [InlineKeyboardButton(text="Оформить заказ", callback_data="checkout:start")],
            [InlineKeyboardButton(text="Очистить корзину", callback_data="cart:clear")],
        )
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def phone_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Поделиться номером", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="+7 900 000-00-00",
    )


def fulfillment_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Самовывоз", callback_data="fulfillment:pickup")],
            [InlineKeyboardButton(text="Доставка", callback_data="fulfillment:delivery")],
        ]
    )


def review_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить заказ", callback_data="order:confirm")],
            [
                InlineKeyboardButton(text="Изменить", callback_data="order:edit"),
                InlineKeyboardButton(text="Отмена", callback_data="order:cancel"),
            ],
        ]
    )

