from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from ..catalog import CATEGORIES, PRODUCTS_BY_ID, products_for_category
from ..formatters import product_text
from ..keyboards import categories_keyboard, product_keyboard, products_keyboard


router = Router(name="catalog")


@router.message(F.text == "Каталог")
async def catalog(message: Message) -> None:
    await message.answer(
        "<b>Каталог NOVA Store</b>\nВыберите категорию:",
        reply_markup=categories_keyboard(),
    )


@router.callback_query(F.data.startswith("category:"))
async def category(callback: CallbackQuery) -> None:
    category_id = callback.data.split(":", maxsplit=1)[1]
    if category_id not in CATEGORIES:
        await callback.answer("Категория не найдена", show_alert=True)
        return
    await callback.message.edit_text(
        f"<b>{CATEGORIES[category_id]}</b>\nВыберите товар:",
        reply_markup=products_keyboard(products_for_category(category_id)),
    )
    await callback.answer()


@router.callback_query(F.data == "catalog:back")
async def catalog_back(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "<b>Каталог NOVA Store</b>\nВыберите категорию:",
        reply_markup=categories_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("product:"))
async def product(callback: CallbackQuery) -> None:
    product_id = callback.data.split(":", maxsplit=1)[1]
    item = PRODUCTS_BY_ID.get(product_id)
    if not item:
        await callback.answer("Товар не найден", show_alert=True)
        return
    await callback.message.edit_text(
        product_text(item),
        reply_markup=product_keyboard(item.id, item.category, item.stock > 0),
    )
    await callback.answer()

