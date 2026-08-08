from dataclasses import dataclass
from pathlib import Path
import os
import re
from urllib.parse import urlsplit

from dotenv import load_dotenv


BOT_TOKEN_PATTERN = re.compile(r"\d{8,12}:[A-Za-z0-9_-]{30,}")


@dataclass(frozen=True, slots=True)
class Config:
    bot_token: str
    admin_id: int
    database_path: Path
    personal_telegram_url: str


def load_config() -> Config:
    load_dotenv()

    token = os.getenv("BOT_TOKEN", "").strip()
    admin_raw = os.getenv("ADMIN_ID", "0").strip()
    database_path = Path(os.getenv("DATABASE_PATH", "data/leads.sqlite3").strip())
    personal_url = os.getenv(
        "PERSONAL_TELEGRAM_URL", "https://t.me/techgottbenzz"
    ).strip()

    if not token:
        raise RuntimeError("BOT_TOKEN не задан в переменных окружения.")
    if not BOT_TOKEN_PATTERN.fullmatch(token):
        raise RuntimeError("BOT_TOKEN имеет некорректный формат.")
    if not admin_raw.lstrip("-").isdigit():
        raise RuntimeError("ADMIN_ID должен быть числовым Telegram ID.")
    admin_id = int(admin_raw)
    if admin_id < 0:
        raise RuntimeError("ADMIN_ID должен быть положительным Telegram ID или 0.")

    parsed_personal_url = urlsplit(personal_url)
    if (
        parsed_personal_url.scheme != "https"
        or parsed_personal_url.netloc != "t.me"
        or not parsed_personal_url.path.strip("/")
        or parsed_personal_url.query
        or parsed_personal_url.fragment
    ):
        raise RuntimeError("PERSONAL_TELEGRAM_URL должен вести на профиль https://t.me/username.")

    return Config(
        bot_token=token,
        admin_id=admin_id,
        database_path=database_path,
        personal_telegram_url=personal_url,
    )
