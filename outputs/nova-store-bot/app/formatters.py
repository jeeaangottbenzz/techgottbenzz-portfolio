import re
from html import escape

from .catalog import CATEGORIES, Product


STATUS_LABELS = {
    "new": "🟣 Новый",
    "confirmed": "🔵 Подтверждён",
    "packing": "🟡 Собирается",
    "shipped": "🟠 Отправлен",
    "completed": "🟢 Завершён",
    "cancelled": "⚪ Отменён",
}

FULFILLMENT_LABELS = {
    "pickup": "Самовывоз",
    "delivery": "Доставка",
}


def money(value: int) -> str:
    return f"{value:,}".replace(",", " ") + " ₽"


def valid_phone(value: str) -> bool:
    digits = re.sub(r"\D", "", value)
    return 10 <= len(digits) <= 15


def product_text(product: Product) -> str:
    category = CATEGORIES[product.category]
    availability = f"В наличии: {product.stock} шт." if product.stock else "Нет в наличии"
    return (
        f"{product.placeholder} <b>{product.name}</b>\n\n"
        f"{product.description}\n\n"
        f"Категория: {category}\n"
        f"Артикул: <code>{product.sku}</code>\n"
        f"{availability}\n"
        f"Цена: <b>{money(product.price)}</b>\n\n"
        "<i>Изображение товара: демонстрационный placeholder</i>"
    )


def cart_total(items: list[dict]) -> int:
    return sum(item["price"] * item["quantity"] for item in items)


def cart_text(items: list[dict]) -> str:
    if not items:
        return "<b>Корзина пуста</b>\n\nДобавьте товары из каталога."
    lines = ["<b>Корзина</b>", ""]
    for item in items:
        lines.append(f"{item['placeholder']} {item['name']} · {item['quantity']} × {money(item['price'])}")
    lines.extend(("", f"Итого: <b>{money(cart_total(items))}</b>"))
    return "\n".join(lines)


def order_text(order: dict, *, include_client: bool = False) -> str:
    lines = [
        f"<b>Заказ №{order['id']}</b>",
        STATUS_LABELS.get(order["status"], order["status"]),
        f"Дата: {order['created_at']}",
        f"Сумма: <b>{money(order['total'])}</b>",
    ]
    if include_client:
        lines.extend(
            (
                f"Клиент: {escape(order['client_name'])}",
                f"Телефон: {escape(order['phone'])}",
                f"Получение: {FULFILLMENT_LABELS.get(order['fulfillment'], order['fulfillment'])}",
                f"Город / адрес: {escape(order['location'])}",
            )
        )
        if order.get("comment"):
            lines.append(f"Комментарий: {escape(order['comment'])}")
    return "\n".join(lines)
