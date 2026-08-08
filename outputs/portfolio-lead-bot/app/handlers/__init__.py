from aiogram import Dispatcher

from .admin import router as admin_router
from .common import router as common_router
from .lead import router as lead_router


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.include_router(common_router)
    dispatcher.include_router(lead_router)
    dispatcher.include_router(admin_router)

