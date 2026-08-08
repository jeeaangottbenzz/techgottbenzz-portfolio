from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from ..config import Config
from ..database import Database
from ..formatters import lead_summary


router = Router(name="admin")


def is_admin(message: Message, config: Config) -> bool:
    return bool(config.admin_id) and message.from_user.id == config.admin_id


@router.message(Command("applications"))
async def applications(message: Message, db: Database, config: Config) -> None:
    if not is_admin(message, config):
        await message.answer("Команда доступна администратору.")
        return

    leads = await db.recent(10)
    if not leads:
        await message.answer("Заявок пока нет.")
        return

    await message.answer("<b>Последние 10 заявок</b>")
    for lead in leads:
        await message.answer(lead_summary(lead, int(lead["id"])))


@router.message(Command("stats"))
async def stats(message: Message, db: Database, config: Config) -> None:
    if not is_admin(message, config):
        await message.answer("Команда доступна администратору.")
        return

    values = await db.stats()
    await message.answer(
        "<b>Статистика заявок</b>\n\n"
        f"Всего: {values.get('total', 0)}\n"
        f"Новые: {values.get('new', 0)}\n"
        f"В работе: {values.get('contacted', 0)}\n"
        f"Завершённые: {values.get('completed', 0)}\n"
        f"Отменённые: {values.get('cancelled', 0)}"
    )
