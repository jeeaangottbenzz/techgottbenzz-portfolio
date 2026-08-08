from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from ..catalog import CATEGORIES, SERVICES_BY_ID, services_for_category
from ..database import Database
from ..formatters import appointment_text, service_card
from ..keyboards import categories_keyboard, main_menu, service_details_keyboard, services_keyboard
from ..texts import ABOUT, CONTACTS, FAQ, WELCOME


router = Router(name="common")


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(WELCOME, reply_markup=main_menu())


@router.message(Command("menu"))
async def menu_command(message: Message) -> None:
    await message.answer("Выберите нужный раздел:", reply_markup=main_menu())


@router.message(F.text == "✨ Услуги")
async def catalog(message: Message) -> None:
    await message.answer(
        "<b>Услуги LUMÉ Beauty</b>\nВыберите категорию:",
        reply_markup=categories_keyboard("category"),
    )


@router.callback_query(F.data.startswith("category:"))
async def catalog_category(callback: CallbackQuery) -> None:
    category = callback.data.split(":", maxsplit=1)[1]
    if category not in CATEGORIES:
        await callback.answer("Категория не найдена", show_alert=True)
        return
    await callback.message.edit_text(
        f"<b>{CATEGORIES[category]}</b>\nВыберите услугу:",
        reply_markup=services_keyboard(services_for_category(category), "catalog_service"),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("catalog_service:"))
async def catalog_service(callback: CallbackQuery) -> None:
    service_id = callback.data.split(":", maxsplit=1)[1]
    service = SERVICES_BY_ID.get(service_id)
    if not service:
        await callback.answer("Услуга не найдена", show_alert=True)
        return
    await callback.message.edit_text(service_card(service), reply_markup=service_details_keyboard(service.id))
    await callback.answer()


@router.callback_query(F.data == "catalog_service_back")
@router.callback_query(F.data == "catalog_back")
async def catalog_back(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "<b>Услуги LUMÉ Beauty</b>\nВыберите категорию:",
        reply_markup=categories_keyboard("category"),
    )
    await callback.answer()


@router.message(F.text == "🗓 Мои записи")
@router.message(Command("my_appointments"))
async def my_appointments(message: Message, db: Database) -> None:
    appointments = await db.recent_for_user(message.from_user.id)
    if not appointments:
        await message.answer("У вас пока нет записей. Нажмите «📅 Записаться», чтобы выбрать услугу и время.")
        return
    text = "<b>Ваши последние записи</b>\n\n" + "\n\n".join(
        appointment_text(appointment) for appointment in appointments
    )
    await message.answer(text)


@router.message(F.text == "О салоне")
async def about(message: Message) -> None:
    await message.answer(ABOUT)


@router.message(F.text == "Контакты")
async def contacts(message: Message) -> None:
    await message.answer(CONTACTS)


@router.message(F.text == "FAQ")
async def faq(message: Message) -> None:
    await message.answer(FAQ)

