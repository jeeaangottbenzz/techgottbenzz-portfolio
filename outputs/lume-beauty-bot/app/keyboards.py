from datetime import date

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from .catalog import CATEGORIES, Master, Service
from .formatters import money, short_date


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✨ Услуги"), KeyboardButton(text="📅 Записаться")],
            [KeyboardButton(text="🗓 Мои записи")],
            [KeyboardButton(text="О салоне"), KeyboardButton(text="Контакты")],
            [KeyboardButton(text="FAQ")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите раздел",
    )


def categories_keyboard(prefix: str = "category") -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=label, callback_data=f"{prefix}:{key}")]
        for key, label in CATEGORIES.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def services_keyboard(services: tuple[Service, ...], prefix: str) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=f"{service.name} · {money(service.price)}", callback_data=f"{prefix}:{service.id}")]
        for service in services
    ]
    rows.append([InlineKeyboardButton(text="← Категории", callback_data=f"{prefix}_back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def service_details_keyboard(service_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Записаться на услугу", callback_data=f"quickbook:{service_id}")],
            [InlineKeyboardButton(text="← К списку", callback_data="catalog_back")],
        ]
    )


def masters_keyboard(masters: tuple[Master, ...]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{master.name} · {master.role}", callback_data=f"master:{master.id}")]
            for master in masters
        ]
    )


def dates_keyboard(dates: list[date]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=short_date(day), callback_data=f"date:{day.isoformat()}")]
            for day in dates
        ]
    )


def times_keyboard(times: list[str]) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    for index in range(0, len(times), 3):
        rows.append([
            InlineKeyboardButton(text=time, callback_data=f"time:{time}")
            for time in times[index:index + 3]
        ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def phone_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Поделиться номером", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="+7 900 000-00-00",
    )


def review_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✓ Подтвердить", callback_data="booking:confirm")],
            [
                InlineKeyboardButton(text="Изменить", callback_data="booking:edit"),
                InlineKeyboardButton(text="Отмена", callback_data="booking:cancel"),
            ],
        ]
    )

