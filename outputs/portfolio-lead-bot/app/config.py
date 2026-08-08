from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


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
    if not admin_raw.lstrip("-").isdigit():
        raise RuntimeError("ADMIN_ID должен быть числовым Telegram ID.")
    if not personal_url.startswith("https://t.me/"):
        raise RuntimeError("PERSONAL_TELEGRAM_URL должен начинаться с https://t.me/.")

    return Config(
        bot_token=token,
        admin_id=int(admin_raw),
        database_path=database_path,
        personal_telegram_url=personal_url,
    )

