import importlib
import pkgutil
from datetime import date
from pathlib import Path
import tempfile
import unittest

import app
from app.catalog import CATEGORIES, MASTERS, SERVICES, masters_for_category, services_for_category
from app.database import Database
from app.formatters import money, valid_phone
from app.schedule import available_times, upcoming_dates


class CatalogTests(unittest.TestCase):
    def test_demo_catalog_has_required_volume(self) -> None:
        self.assertGreaterEqual(len(SERVICES), 10)
        self.assertGreaterEqual(len(MASTERS), 4)
        self.assertEqual(set(CATEGORIES), {"manicure", "pedicure", "brows", "lashes", "hair"})

    def test_each_category_has_services_and_masters(self) -> None:
        for category in CATEGORIES:
            self.assertTrue(services_for_category(category), category)
            self.assertTrue(masters_for_category(category), category)

    def test_schedule_is_future_facing_and_excludes_booked_slots(self) -> None:
        dates = upcoming_dates(7)
        self.assertEqual(len(dates), 7)
        self.assertTrue(all(day >= date.today() for day in dates))
        self.assertTrue(all(day.weekday() != 6 for day in dates))
        slots = available_times(dates[0], "alina")
        self.assertTrue(slots)
        filtered = available_times(dates[0], "alina", {slots[0]})
        self.assertNotIn(slots[0], filtered)

    def test_formatting_and_phone_validation(self) -> None:
        self.assertEqual(money(2800), "2 800 ₽")
        self.assertTrue(valid_phone("+7 900 000-00-00"))
        self.assertFalse(valid_phone("123"))

    def test_all_app_modules_import(self) -> None:
        modules = [name for _, name, _ in pkgutil.walk_packages(app.__path__, prefix="app.")]
        for module in modules:
            with self.subTest(module=module):
                importlib.import_module(module)


class DatabaseTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db = Database(Path(self.temp_dir.name) / "test.sqlite3")
        await self.db.initialize()

    async def asyncTearDown(self) -> None:
        self.temp_dir.cleanup()

    async def test_create_read_and_stats(self) -> None:
        payload = {
            "user_id": 42,
            "username": "demo_user",
            "service_id": "manicure_gel",
            "service_name": "Маникюр с покрытием",
            "master_id": "alina",
            "master_name": "Алина",
            "appointment_date": upcoming_dates(1)[0].isoformat(),
            "appointment_time": "11:30",
            "client_name": "Никита",
            "phone": "+7 900 000-00-00",
            "comment": "Демонстрационная запись",
        }
        appointment_id = await self.db.create_appointment(payload)
        appointment = await self.db.get_appointment(appointment_id)
        self.assertEqual(appointment["status"], "new")
        self.assertEqual(appointment["service_name"], payload["service_name"])
        self.assertEqual(len(await self.db.recent_for_user(42)), 1)
        self.assertIn("11:30", await self.db.booked_times("alina", payload["appointment_date"]))
        stats = await self.db.stats()
        self.assertEqual(stats["total"], 1)
        self.assertEqual(stats["new"], 1)


if __name__ == "__main__":
    unittest.main()

