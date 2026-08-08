from datetime import date

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ..config import Config
from ..database import Database
from ..formatters import STATUS_LABELS, appointment_text


router = Router(name="admin")


async def ensure_admin(message: Message, config: Config) -> bool:
    if message.from_user.id == config.admin_id:
        return True
    await message.answer("Эта команда доступна только администратору.")
    return False


@router.message(Command("id"))
async def telegram_id(message: Message) -> None:
    await message.answer(f"Ваш Telegram ID: <code>{message.from_user.id}</code>")


@router.message(Command("appointments"))
async def appointments(message: Message, db: Database, config: Config) -> None:
    if not await ensure_admin(message, config):
        return
    items = await db.recent(10)
    if not items:
        await message.answer("Записей пока нет.")
        return
    await message.answer("<b>Последние записи</b>\n\n" + "\n\n".join(
        appointment_text(item, include_client=True) for item in items
    ))


@router.message(Command("today"))
async def today(message: Message, db: Database, config: Config) -> None:
    if not await ensure_admin(message, config):
        return
    items = await db.for_date(date.today().isoformat())
    if not items:
        await message.answer("На сегодня записей нет.")
        return
    await message.answer("<b>Записи на сегодня</b>\n\n" + "\n\n".join(
        appointment_text(item, include_client=True) for item in items
    ))


@router.message(Command("stats"))
async def stats(message: Message, db: Database, config: Config) -> None:
    if not await ensure_admin(message, config):
        return
    values = await db.stats()
    await message.answer(
        "<b>Статистика записей</b>\n\n"
        f"Всего: {values.get('total', 0)}\n"
        f"Сегодня: {values.get('today', 0)}\n"
        f"{STATUS_LABELS['new']}: {values.get('new', 0)}\n"
        f"{STATUS_LABELS['confirmed']}: {values.get('confirmed', 0)}\n"
        f"{STATUS_LABELS['completed']}: {values.get('completed', 0)}\n"
        f"{STATUS_LABELS['cancelled']}: {values.get('cancelled', 0)}"
    )

