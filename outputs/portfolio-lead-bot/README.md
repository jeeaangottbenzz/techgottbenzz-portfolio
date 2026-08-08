# techgottbenzz — бот для заявок

Telegram-бот для приёма заявок с сайта-портфолио. Бот проводит пользователя через короткую форму, сохраняет заявку в SQLite и отправляет уведомление администратору.

## Возможности

- `/start` — приветствие и главное меню;
- пошаговая заявка: услуга, описание, бюджет, срок и контакт;
- подтверждение, изменение и отмена заявки;
- сохранение заявок в SQLite;
- уведомление администратора в Telegram;
- `/applications` — последние 10 заявок для администратора;
- `/stats` — статистика для администратора;
- `/id` — показать числовой Telegram ID;
- `/cancel` — отменить текущий сценарий.

## Локальный запуск

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python main.py
```

Заполните `.env`:

```env
BOT_TOKEN=токен_из_BotFather
ADMIN_ID=ваш_числовой_Telegram_ID
DATABASE_PATH=data/leads.sqlite3
PERSONAL_TELEGRAM_URL=https://t.me/techgottbenzz
```

`BOT_TOKEN` нельзя публиковать, добавлять в Git или отправлять в открытые сообщения.

## Railway

1. Создайте отдельный сервис из этого репозитория.
2. Укажите Root Directory: `/outputs/portfolio-lead-bot`.
3. Добавьте Variables: `BOT_TOKEN`, `ADMIN_ID`, `DATABASE_PATH=/data/leads.sqlite3`, `PERSONAL_TELEGRAM_URL`.
4. Для сохранности SQLite подключите Volume с mount path `/data`.
5. Публичный HTTP-домен этому worker-сервису не нужен.

Команда запуска берётся из `railway.json`: `python main.py`.

