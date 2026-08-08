from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from ..catalog import PRODUCTS_BY_ID
from ..database import Database
from ..formatters import cart_text
from ..keyboards import cart_keyboard
from ..store import enriched_cart


router = Router(name="cart")


async def show_cart(message: Message, db: Database, user_id: int, *, edit: bool = False) -> None:
    items = await enriched_cart(db, user_id)
    if edit:
        await message.edit_text(cart_text(items), reply_markup=cart_keyboard(items))
    else:
        await message.answer(cart_text(items), reply_markup=cart_keyboard(items))


@router.message(F.text == "Корзина")
async def cart(message: Message, db: Database) -> None:
    await show_cart(message, db, message.from_user.id)


@router.callback_query(F.data.startswith("add:"))
async def add_product(callback: CallbackQuery, db: Database) -> None:
    product_id = callback.data.split(":", maxsplit=1)[1]
    product = PRODUCTS_BY_ID.get(product_id)
    if not product or product.stock <= 0:
        await callback.answer("Товар недоступен", show_alert=True)
        return
    items = await enriched_cart(db, callback.from_user.id)
    current = next((item["quantity"] for item in items if item["product_id"] == product_id), 0)
    if current >= product.stock:
        await callback.answer("Больше единиц нет в наличии", show_alert=True)
        return
    await db.add_to_cart(callback.from_user.id, product_id)
    await callback.answer("Добавлено в корзину")


@router.callback_query(F.data == "cart:noop")
async def cart_noop(callback: CallbackQuery) -> None:
    await callback.answer()


@router.callback_query(F.data.startswith("cart:inc:"))
async def increment(callback: CallbackQuery, db: Database) -> None:
    product_id = callback.data.split(":", maxsplit=2)[2]
    product = PRODUCTS_BY_ID.get(product_id)
    items = await enriched_cart(db, callback.from_user.id)
    item = next((item for item in items if item["product_id"] == product_id), None)
    if not product or not item:
        await callback.answer("Товар не найден", show_alert=True)
        return
    if item["quantity"] >= product.stock:
        await callback.answer("Достигнут доступный остаток", show_alert=True)
        return
    await db.set_cart_quantity(callback.from_user.id, product_id, item["quantity"] + 1)
    await show_cart(callback.message, db, callback.from_user.id, edit=True)
    await callback.answer()


@router.callback_query(F.data.startswith("cart:dec:"))
async def decrement(callback: CallbackQuery, db: Database) -> None:
    product_id = callback.data.split(":", maxsplit=2)[2]
    items = await enriched_cart(db, callback.from_user.id)
    item = next((item for item in items if item["product_id"] == product_id), None)
    if not item:
        await callback.answer("Товар уже удалён")
        return
    await db.set_cart_quantity(callback.from_user.id, product_id, item["quantity"] - 1)
    await show_cart(callback.message, db, callback.from_user.id, edit=True)
    await callback.answer()


@router.callback_query(F.data.startswith("cart:remove:"))
async def remove(callback: CallbackQuery, db: Database) -> None:
    product_id = callback.data.split(":", maxsplit=2)[2]
    await db.remove_from_cart(callback.from_user.id, product_id)
    await show_cart(callback.message, db, callback.from_user.id, edit=True)
    await callback.answer("Товар удалён")


@router.callback_query(F.data == "cart:clear")
async def clear(callback: CallbackQuery, db: Database) -> None:
    await db.clear_cart(callback.from_user.id)
    await show_cart(callback.message, db, callback.from_user.id, edit=True)
    await callback.answer("Корзина очищена")

