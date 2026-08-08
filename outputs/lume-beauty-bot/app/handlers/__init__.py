from aiogram import Dispatcher

from . import admin, booking, common


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.include_router(admin.router)
    dispatcher.include_router(booking.router)
    dispatcher.include_router(common.router)

