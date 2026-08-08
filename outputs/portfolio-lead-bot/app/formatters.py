from html import escape
from typing import Mapping


def lead_summary(data: Mapping[str, object], lead_id: int | None = None) -> str:
    lines: list[str] = []
    if lead_id is not None:
        lines.append(f"<b>Заявка №{lead_id}</b>")

    fields = (
        ("Услуга", "service"),
        ("Задача", "description"),
        ("Бюджет", "budget"),
        ("Срок", "deadline"),
        ("Контакт", "contact"),
    )
    lines.extend(
        f"<b>{label}:</b> {escape(str(data.get(key, '—')))}" for label, key in fields
    )
    return "\n".join(lines)


def admin_lead_message(data: Mapping[str, object], lead_id: int) -> str:
    username = data.get("username")
    username_text = f"@{escape(str(username))}" if username else "не указан"
    user_id = int(data["user_id"])
    return (
        "🆕 <b>Новая заявка с сайта</b>\n\n"
        f"{lead_summary(data, lead_id)}\n\n"
        f"<b>Пользователь:</b> {username_text}\n"
        f"<b>Telegram ID:</b> <code>{user_id}</code>\n"
        f'<a href="tg://user?id={user_id}">Открыть профиль</a>'
    )

