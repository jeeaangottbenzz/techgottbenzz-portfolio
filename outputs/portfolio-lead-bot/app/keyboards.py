from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


SERVICES = {
    "telegram_bot": "Telegram-бот",
    "business_card": "Сайт-визитка",
    "landing": "Лендинг",
    "automation": "Автоматизация",
    "other": "Другая задача",
}

BUDGETS = {
    "under_10": "До 10 000 ₽",
    "10_20": "10 000–20 000 ₽",
    "20_50": "20 000–50 000 ₽",
    "discuss": "Нужно обсудить",
}


def main_menu(personal_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Оставить заявку", callback_data="lead:start")],
            [InlineKeyboardButton(text="Услуги", callback_data="services:show")],
            [InlineKeyboardButton(text="Написать лично", url=personal_url)],
        ]
    )


def service_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=label, callback_data=f"lead:service:{key}")]
        for key, label in SERVICES.items()
    ]
    rows.append([InlineKeyboardButton(text="Отмена", callback_data="lead:cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def budget_keyboard() -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=label, callback_data=f"lead:budget:{key}")]
        for key, label in BUDGETS.items()
    ]
    rows.append([InlineKeyboardButton(text="Отмена", callback_data="lead:cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def contact_keyboard(username: str | None) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    if username:
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"Использовать @{username}", callback_data="lead:contact:telegram"
                )
            ]
        )
    rows.append([InlineKeyboardButton(text="Отмена", callback_data="lead:cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Подтвердить заявку", callback_data="lead:confirm")],
            [InlineKeyboardButton(text="Изменить", callback_data="lead:change")],
            [InlineKeyboardButton(text="Отмена", callback_data="lead:cancel")],
        ]
    )


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Оставить ещё заявку", callback_data="lead:start")],
            [InlineKeyboardButton(text="Главное меню", callback_data="menu:main")],
        ]
    )

