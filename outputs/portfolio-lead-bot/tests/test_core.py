import importlib
import pkgutil
from pathlib import Path
import tempfile
import unittest

import app
from app.database import Database, LeadRateLimitError
from app.formatters import admin_lead_message, lead_summary
from app.keyboards import BUDGETS, SERVICES


class CoreTests(unittest.TestCase):
    def test_service_and_budget_options(self) -> None:
        self.assertEqual(len(SERVICES), 5)
        self.assertEqual(len(BUDGETS), 4)
        self.assertIn("telegram_bot", SERVICES)
        self.assertIn("discuss", BUDGETS)

    def test_formatter_escapes_user_content(self) -> None:
        payload = {
            "user_id": 42,
            "username": "demo_user",
            "service": "Telegram-бот",
            "description": "<script>alert(1)</script>",
            "budget": "Нужно обсудить",
            "deadline": "В течение недели",
            "contact": "@demo_user",
        }
        summary = lead_summary(payload, 7)
        self.assertIn("Заявка №7", summary)
        self.assertNotIn("<script>", summary)
        self.assertIn("&lt;script&gt;", summary)
        self.assertIn("tg://user?id=42", admin_lead_message(payload, 7))

    def test_all_app_modules_import(self) -> None:
        modules = [name for _, name, _ in pkgutil.walk_packages(app.__path__, prefix="app.")]
        for module in modules:
            with self.subTest(module=module):
                importlib.import_module(module)


class DatabaseTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = Database(Path(self.temp_dir.name) / "test.sqlite3")
        await self.database.initialize()

    async def asyncTearDown(self) -> None:
        self.temp_dir.cleanup()

    async def test_create_read_and_stats(self) -> None:
        payload = {
            "user_id": 42,
            "username": "demo_user",
            "service": "Telegram-бот",
            "description": "Бот для приёма заявок",
            "budget": "10 000–20 000 ₽",
            "deadline": "В течение недели",
            "contact": "@demo_user",
        }
        lead_id = await self.database.create_lead(payload)
        lead = await self.database.get_lead(lead_id)
        self.assertIsNotNone(lead)
        self.assertEqual(lead["status"], "new")
        self.assertEqual(lead["service"], payload["service"])
        self.assertEqual(len(await self.database.recent()), 1)
        stats = await self.database.stats()
        self.assertEqual(stats["total"], 1)
        self.assertEqual(stats["new"], 1)

        with self.assertRaises(LeadRateLimitError):
            await self.database.create_lead(payload)
        self.assertEqual(len(await self.database.recent()), 1)


if __name__ == "__main__":
    unittest.main()
