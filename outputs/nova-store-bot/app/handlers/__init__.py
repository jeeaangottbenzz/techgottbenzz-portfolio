from aiogram import Dispatcher

from . import admin, cart, catalog, checkout, common


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.include_router(admin.router)
    dispatcher.include_router(checkout.router)
    dispatcher.include_router(cart.router)
    dispatcher.include_router(catalog.router)
    dispatcher.include_router(common.router)

