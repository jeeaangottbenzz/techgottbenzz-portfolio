from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from ..database import Database
from ..formatters import order_text
from ..keyboards import main_menu
from ..texts import CONTACTS, DELIVERY, FAQ, WELCOME


router = Router(name="common")


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(WELCOME, reply_markup=main_menu())


@router.message(Command("menu"))
async def menu(message: Message) -> None:
    await message.answer("Главное меню:", reply_markup=main_menu())


@router.message(F.text == "Мои заказы")
@router.message(Command("my_orders"))
async def my_orders(message: Message, db: Database) -> None:
    orders = await db.recent_for_user(message.from_user.id, 5)
    if not orders:
        await message.answer("У вас пока нет заказов. Откройте каталог и добавьте товары в корзину.")
        return
    await message.answer("<b>Ваши последние заказы</b>\n\n" + "\n\n".join(order_text(order) for order in orders))


@router.message(F.text == "Доставка и оплата")
async def delivery(message: Message) -> None:
    await message.answer(DELIVERY)


@router.message(F.text == "Контакты")
async def contacts(message: Message) -> None:
    await message.answer(CONTACTS)


@router.message(F.text == "FAQ")
async def faq(message: Message) -> None:
    await message.answer(FAQ)

