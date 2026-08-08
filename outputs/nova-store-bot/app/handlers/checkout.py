from html import escape

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from ..config import Config
from ..database import Database
from ..formatters import FULFILLMENT_LABELS, cart_total, money, order_text, valid_phone
from ..keyboards import fulfillment_keyboard, main_menu, phone_keyboard, review_keyboard
from ..states import CheckoutStates
from ..store import enriched_cart


router = Router(name="checkout")


def review_text(data: dict, items: list[dict]) -> str:
    lines = ["<b>Проверьте заказ</b>", ""]
    for item in items:
        lines.append(f"{item['name']} · {item['quantity']} × {money(item['price'])}")
    lines.extend(
        (
            "",
            f"Итого: <b>{money(cart_total(items))}</b>",
            "",
            f"Имя: {escape(data['client_name'])}",
            f"Телефон: {escape(data['phone'])}",
            f"Получение: {FULFILLMENT_LABELS[data['fulfillment']]}",
            f"Город / адрес: {escape(data['location'])}",
            f"Комментарий: {escape(data.get('comment') or '—')}",
        )
    )
    return "\n".join(lines)


@router.callback_query(F.data == "checkout:start")
async def start_checkout(callback: CallbackQuery, state: FSMContext, db: Database) -> None:
    if not await enriched_cart(db, callback.from_user.id):
        await callback.answer("Корзина пуста", show_alert=True)
        return
    await state.clear()
    await state.set_state(CheckoutStates.entering_name)
    await callback.message.answer("<b>Оформление заказа</b>\nКак к вам обращаться?", reply_markup=ReplyKeyboardRemove())
    await callback.answer()


@router.message(CheckoutStates.entering_name, F.text)
async def enter_name(message: Message, state: FSMContext) -> None:
    name = message.text.strip()
    if not 2 <= len(name) <= 60:
        await message.answer("Введите имя длиной от 2 до 60 символов.")
        return
    await state.update_data(client_name=name)
    await state.set_state(CheckoutStates.entering_phone)
    await message.answer("Отправьте номер или введите его вручную:", reply_markup=phone_keyboard())


async def ask_fulfillment(message: Message, state: FSMContext, phone: str) -> None:
    await state.update_data(phone=phone)
    await state.set_state(CheckoutStates.choosing_fulfillment)
    await message.answer("Как вы хотите получить заказ?", reply_markup=fulfillment_keyboard())


@router.message(CheckoutStates.entering_phone, F.contact)
async def enter_contact(message: Message, state: FSMContext) -> None:
    await ask_fulfillment(message, state, message.contact.phone_number)


@router.message(CheckoutStates.entering_phone, F.text)
async def enter_phone(message: Message, state: FSMContext) -> None:
    phone = message.text.strip()
    if not valid_phone(phone):
        await message.answer("Проверьте номер. Например: +7 900 000-00-00.")
        return
    await ask_fulfillment(message, state, phone)


@router.callback_query(CheckoutStates.choosing_fulfillment, F.data.startswith("fulfillment:"))
async def choose_fulfillment(callback: CallbackQuery, state: FSMContext) -> None:
    fulfillment = callback.data.split(":", maxsplit=1)[1]
    if fulfillment not in FULFILLMENT_LABELS:
        await callback.answer("Способ получения не найден", show_alert=True)
        return
    await state.update_data(fulfillment=fulfillment)
    await state.set_state(CheckoutStates.entering_location)
    prompt = "Укажите город для самовывоза:" if fulfillment == "pickup" else "Укажите город и адрес доставки:"
    await callback.message.answer(prompt)
    await callback.answer()


@router.message(CheckoutStates.entering_location, F.text)
async def enter_location(message: Message, state: FSMContext) -> None:
    location = message.text.strip()
    if not 2 <= len(location) <= 200:
        await message.answer("Укажите город или адрес длиной до 200 символов.")
        return
    await state.update_data(location=location)
    await state.set_state(CheckoutStates.entering_comment)
    await message.answer("Добавьте комментарий или отправьте «—»:")


@router.message(CheckoutStates.entering_comment, F.text)
async def enter_comment(message: Message, state: FSMContext, db: Database) -> None:
    comment = message.text.strip()
    if len(comment) > 500:
        await message.answer("Комментарий слишком длинный. Используйте не более 500 символов.")
        return
    await state.update_data(comment=None if comment in {"-", "—"} else comment)
    items = await enriched_cart(db, message.from_user.id)
    if not items:
        await state.clear()
        await message.answer("Корзина была очищена. Добавьте товары и начните оформление заново.", reply_markup=main_menu())
        return
    await state.set_state(CheckoutStates.reviewing)
    await message.answer(review_text(await state.get_data(), items), reply_markup=review_keyboard())


@router.callback_query(CheckoutStates.reviewing, F.data == "order:edit")
async def edit_order(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(CheckoutStates.entering_name)
    await callback.message.edit_text("Изменим данные заказа. Как к вам обращаться?")
    await callback.answer()


@router.callback_query(F.data == "order:cancel")
async def cancel_order_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text("Оформление отменено. Товары остались в корзине.")
    await callback.message.answer("Главное меню:", reply_markup=main_menu())
    await callback.answer()


@router.message(Command("cancel"))
async def cancel_order_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Текущий сценарий отменён. Товары остались в корзине.", reply_markup=main_menu())


@router.callback_query(CheckoutStates.reviewing, F.data == "order:confirm")
async def confirm_order(
    callback: CallbackQuery,
    state: FSMContext,
    db: Database,
    config: Config,
    bot: Bot,
) -> None:
    items = await enriched_cart(db, callback.from_user.id)
    if not items:
        await state.clear()
        await callback.answer("Корзина пуста. Начните оформление заново.", show_alert=True)
        return
    data = await state.get_data()
    data.update(user_id=callback.from_user.id, username=callback.from_user.username)
    order_id = await db.create_order(data, items, cart_total(items))
    order = await db.get_order(order_id)
    await state.clear()

    await callback.message.edit_text("◼️ <b>Заказ оформлен</b>\n\n" + order_text(order))
    await callback.message.answer("Спасибо! Корзина очищена, главное меню снова доступно.", reply_markup=main_menu())
    await callback.answer("Заказ подтверждён")

    admin_items = "\n".join(
        f"• {item['name']} · {item['quantity']} × {money(item['price'])}"
        for item in order["items"]
    )
    try:
        await bot.send_message(
            config.admin_id,
            "🛍 <b>Новый заказ</b>\n\n"
            + order_text(order, include_client=True)
            + "\n\n<b>Состав</b>\n"
            + admin_items,
        )
    except TelegramAPIError:
        # Client flow remains successful if the demo admin has not started the bot.
        pass

