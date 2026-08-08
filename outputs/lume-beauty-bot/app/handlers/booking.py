from datetime import date
import sqlite3

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from ..catalog import (
    CATEGORIES,
    MASTERS_BY_ID,
    SERVICES_BY_ID,
    masters_for_category,
    services_for_category,
)
from ..config import Config
from ..database import Database
from ..formatters import appointment_text, money, valid_phone
from ..keyboards import (
    categories_keyboard,
    dates_keyboard,
    main_menu,
    masters_keyboard,
    phone_keyboard,
    review_keyboard,
    services_keyboard,
    times_keyboard,
)
from ..schedule import available_times, upcoming_dates
from ..states import BookingStates


router = Router(name="booking")


async def show_master_choice(message: Message, state: FSMContext, service_id: str) -> None:
    service = SERVICES_BY_ID[service_id]
    await state.update_data(
        service_id=service.id,
        service_name=service.name,
        service_price=service.price,
        category=service.category,
    )
    await state.set_state(BookingStates.choosing_master)
    await message.answer(
        f"Вы выбрали <b>{service.name}</b>.\nКто будет вашим мастером?",
        reply_markup=masters_keyboard(masters_for_category(service.category)),
    )


def review_text(data: dict) -> str:
    comment = data.get("comment") or "—"
    return (
        "<b>Проверьте запись</b>\n\n"
        f"Услуга: {data['service_name']}\n"
        f"Мастер: {data['master_name']}\n"
        f"Дата: {data['appointment_date']}\n"
        f"Время: {data['appointment_time']}\n"
        f"Имя: {data['client_name']}\n"
        f"Телефон: {data['phone']}\n"
        f"Комментарий: {comment}\n"
        f"Стоимость: <b>{money(data['service_price'])}</b>"
    )


@router.message(F.text == "📅 Записаться")
@router.message(Command("book"))
async def start_booking(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(BookingStates.choosing_category)
    await message.answer(
        "<b>Новая запись</b>\nСначала выберите категорию:",
        reply_markup=categories_keyboard("book_category"),
    )


@router.callback_query(F.data.startswith("book_category:"))
async def choose_category(callback: CallbackQuery, state: FSMContext) -> None:
    category = callback.data.split(":", maxsplit=1)[1]
    if category not in CATEGORIES:
        await callback.answer("Категория не найдена", show_alert=True)
        return
    await state.update_data(category=category)
    await state.set_state(BookingStates.choosing_service)
    await callback.message.edit_text(
        f"<b>{CATEGORIES[category]}</b>\nВыберите услугу:",
        reply_markup=services_keyboard(services_for_category(category), "book_service"),
    )
    await callback.answer()


@router.callback_query(F.data == "book_service_back")
async def booking_categories_back(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(BookingStates.choosing_category)
    await callback.message.edit_text(
        "<b>Новая запись</b>\nВыберите категорию:",
        reply_markup=categories_keyboard("book_category"),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("book_service:"))
async def choose_service(callback: CallbackQuery, state: FSMContext) -> None:
    service_id = callback.data.split(":", maxsplit=1)[1]
    if service_id not in SERVICES_BY_ID:
        await callback.answer("Услуга не найдена", show_alert=True)
        return
    await callback.answer()
    await show_master_choice(callback.message, state, service_id)


@router.callback_query(F.data.startswith("quickbook:"))
async def quick_booking(callback: CallbackQuery, state: FSMContext) -> None:
    service_id = callback.data.split(":", maxsplit=1)[1]
    if service_id not in SERVICES_BY_ID:
        await callback.answer("Услуга не найдена", show_alert=True)
        return
    await callback.answer()
    await show_master_choice(callback.message, state, service_id)


@router.callback_query(BookingStates.choosing_master, F.data.startswith("master:"))
async def choose_master(callback: CallbackQuery, state: FSMContext) -> None:
    master_id = callback.data.split(":", maxsplit=1)[1]
    master = MASTERS_BY_ID.get(master_id)
    if not master:
        await callback.answer("Мастер не найден", show_alert=True)
        return
    await state.update_data(master_id=master.id, master_name=master.name)
    await state.set_state(BookingStates.choosing_date)
    await callback.message.answer(
        f"Мастер: <b>{master.name}</b>\nВыберите дату:",
        reply_markup=dates_keyboard(upcoming_dates()),
    )
    await callback.answer()


@router.callback_query(BookingStates.choosing_date, F.data.startswith("date:"))
async def choose_date(callback: CallbackQuery, state: FSMContext, db: Database) -> None:
    raw_date = callback.data.split(":", maxsplit=1)[1]
    try:
        selected_date = date.fromisoformat(raw_date)
    except ValueError:
        await callback.answer("Некорректная дата", show_alert=True)
        return
    data = await state.get_data()
    booked = await db.booked_times(data["master_id"], raw_date)
    times = available_times(selected_date, data["master_id"], booked)
    if not times:
        await callback.answer("На эту дату свободных слотов нет", show_alert=True)
        return
    await state.update_data(appointment_date=raw_date)
    await state.set_state(BookingStates.choosing_time)
    await callback.message.answer("Выберите доступное время:", reply_markup=times_keyboard(times))
    await callback.answer()


@router.callback_query(BookingStates.choosing_time, F.data.startswith("time:"))
async def choose_time(callback: CallbackQuery, state: FSMContext) -> None:
    appointment_time = callback.data.split(":", maxsplit=1)[1]
    await state.update_data(appointment_time=appointment_time)
    await state.set_state(BookingStates.entering_name)
    await callback.message.answer("Как к вам обращаться?", reply_markup=ReplyKeyboardRemove())
    await callback.answer()


@router.message(BookingStates.entering_name, F.text)
async def enter_name(message: Message, state: FSMContext) -> None:
    name = message.text.strip()
    if not 2 <= len(name) <= 60:
        await message.answer("Введите имя длиной от 2 до 60 символов.")
        return
    await state.update_data(client_name=name)
    await state.set_state(BookingStates.entering_phone)
    await message.answer(
        "Отправьте номер кнопкой ниже или введите его вручную:",
        reply_markup=phone_keyboard(),
    )


@router.message(BookingStates.entering_phone, F.contact)
async def enter_contact(message: Message, state: FSMContext) -> None:
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(BookingStates.entering_comment)
    await message.answer("Добавьте комментарий к записи или отправьте «—»:", reply_markup=ReplyKeyboardRemove())


@router.message(BookingStates.entering_phone, F.text)
async def enter_phone(message: Message, state: FSMContext) -> None:
    phone = message.text.strip()
    if not valid_phone(phone):
        await message.answer("Проверьте номер. Например: +7 900 000-00-00.")
        return
    await state.update_data(phone=phone)
    await state.set_state(BookingStates.entering_comment)
    await message.answer("Добавьте комментарий к записи или отправьте «—»:", reply_markup=ReplyKeyboardRemove())


@router.message(BookingStates.entering_comment, F.text)
async def enter_comment(message: Message, state: FSMContext) -> None:
    comment = message.text.strip()
    if len(comment) > 500:
        await message.answer("Комментарий слишком длинный. Используйте не более 500 символов.")
        return
    await state.update_data(comment=None if comment in {"-", "—"} else comment)
    await state.set_state(BookingStates.reviewing)
    await message.answer(review_text(await state.get_data()), reply_markup=review_keyboard())


@router.callback_query(BookingStates.reviewing, F.data == "booking:edit")
async def edit_booking(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(BookingStates.choosing_category)
    await callback.message.edit_text(
        "Изменим запись. Выберите категорию:",
        reply_markup=categories_keyboard("book_category"),
    )
    await callback.answer()


@router.callback_query(F.data == "booking:cancel")
async def cancel_booking_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text("Запись отменена. Вы можете начать заново в главном меню.")
    await callback.message.answer("Главное меню:", reply_markup=main_menu())
    await callback.answer()


@router.message(Command("cancel"))
async def cancel_booking_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Текущий сценарий отменён.", reply_markup=main_menu())


@router.callback_query(BookingStates.reviewing, F.data == "booking:confirm")
async def confirm_booking(
    callback: CallbackQuery,
    state: FSMContext,
    db: Database,
    config: Config,
    bot: Bot,
) -> None:
    data = await state.get_data()
    data.update(user_id=callback.from_user.id, username=callback.from_user.username)
    try:
        appointment_id = await db.create_appointment(data)
    except (sqlite3.IntegrityError, ValueError):
        await callback.answer("Этот слот уже занят. Начните запись заново и выберите другое время.", show_alert=True)
        await state.clear()
        return

    appointment = await db.get_appointment(appointment_id)
    await state.clear()
    await callback.message.edit_text(
        "✨ <b>Запись подтверждена</b>\n\n" + appointment_text(appointment)
    )
    await callback.message.answer("Будем ждать вас! Главное меню снова доступно ниже.", reply_markup=main_menu())
    await callback.answer("Готово")

    try:
        await bot.send_message(
            config.admin_id,
            "🔔 <b>Новая запись</b>\n\n" + appointment_text(appointment, include_client=True),
        )
    except TelegramAPIError:
        # The client confirmation must not fail if the demo admin has not started the bot yet.
        pass

