import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from .config import load_config
from .database import Database
from .handlers import register_handlers


async def set_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Открыть главное меню"),
            BotCommand(command="apply", description="Оставить заявку"),
            BotCommand(command="cancel", description="Отменить текущую заявку"),
            BotCommand(command="id", description="Показать Telegram ID"),
        ]
    )


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    config = load_config()
    database = Database(config.database_path)
    await database.initialize()

    bot = Bot(config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dispatcher = Dispatcher()
    register_handlers(dispatcher)

    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot)

    try:
        await dispatcher.start_polling(
            bot,
            db=database,
            config=config,
            allowed_updates=dispatcher.resolve_used_update_types(),
        )
    finally:
        await bot.session.close()

