from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from ..config import Config
from ..keyboards import main_menu, service_keyboard
from ..states import LeadForm
from ..texts import ASK_SERVICE, CANCELLED, SERVICES_TEXT, WELCOME


router = Router(name="common")


@router.message(CommandStart())
async def start(message: Message, state: FSMContext, config: Config) -> None:
    await state.clear()
    await message.answer(WELCOME, reply_markup=main_menu(config.personal_telegram_url))


@router.callback_query(F.data == "menu:main")
async def show_main_menu(callback: CallbackQuery, state: FSMContext, config: Config) -> None:
    await state.clear()
    if callback.message:
        await callback.message.edit_text(
            WELCOME, reply_markup=main_menu(config.personal_telegram_url)
        )
    await callback.answer()


@router.callback_query(F.data == "services:show")
async def show_services(callback: CallbackQuery, config: Config) -> None:
    if callback.message:
        await callback.message.edit_text(
            SERVICES_TEXT, reply_markup=main_menu(config.personal_telegram_url)
        )
    await callback.answer()


@router.message(Command("apply"))
async def apply_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(LeadForm.service)
    await message.answer(ASK_SERVICE, reply_markup=service_keyboard())


@router.message(Command("cancel"))
async def cancel_command(message: Message, state: FSMContext, config: Config) -> None:
    await state.clear()
    await message.answer(CANCELLED, reply_markup=main_menu(config.personal_telegram_url))


@router.message(Command("id"))
async def id_command(message: Message) -> None:
    await message.answer(f"Ваш Telegram ID: <code>{message.from_user.id}</code>")

