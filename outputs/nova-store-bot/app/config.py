from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


@dataclass(frozen=True, slots=True)
class Config:
    bot_token: str
    admin_id: int
    database_path: Path


def load_config() -> Config:
    load_dotenv()
    token = os.getenv("BOT_TOKEN", "").strip()
    admin_raw = os.getenv("ADMIN_ID", "").strip()
    database_path = Path(os.getenv("DATABASE_PATH", "data/nova_store.sqlite3"))

    if not token:
        raise RuntimeError("BOT_TOKEN не задан. Скопируйте .env.example в .env и добавьте токен.")
    if not admin_raw.isdigit():
        raise RuntimeError("ADMIN_ID должен быть числовым Telegram ID.")

    return Config(bot_token=token, admin_id=int(admin_raw), database_path=database_path)

