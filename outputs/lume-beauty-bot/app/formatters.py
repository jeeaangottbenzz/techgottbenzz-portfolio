from datetime import date
import re

from .catalog import Service


STATUS_LABELS = {
    "new": "🟣 Новая",
    "confirmed": "🔵 Подтверждена",
    "completed": "🟢 Завершена",
    "cancelled": "⚪ Отменена",
}


def money(value: int) -> str:
    return f"{value:,}".replace(",", " ") + " ₽"


def service_card(service: Service) -> str:
    return (
        f"<b>{service.name}</b>\n\n"
        f"{service.description}\n\n"
        f"⏱ {service.duration} мин.\n"
        f"Стоимость: <b>{money(service.price)}</b>"
    )


def short_date(value: date) -> str:
    weekdays = ("Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")
    return f"{weekdays[value.weekday()]}, {value.strftime('%d.%m')}"


def valid_phone(value: str) -> bool:
    digits = re.sub(r"\D", "", value)
    return 10 <= len(digits) <= 15


def appointment_text(appointment: dict, *, include_client: bool = False) -> str:
    lines = [
        f"<b>Запись №{appointment['id']}</b>",
        f"{STATUS_LABELS.get(appointment['status'], appointment['status'])}",
        "",
        f"Услуга: {appointment['service_name']}",
        f"Мастер: {appointment['master_name']}",
        f"Дата: {appointment['appointment_date']}",
        f"Время: {appointment['appointment_time']}",
    ]
    if include_client:
        lines.extend((f"Клиент: {appointment['client_name']}", f"Телефон: {appointment['phone']}"))
        if appointment.get("comment"):
            lines.append(f"Комментарий: {appointment['comment']}")
    return "\n".join(lines)

