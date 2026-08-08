import importlib
import pkgutil
from pathlib import Path
import tempfile
import unittest

import app
from app.catalog import CATEGORIES, PRODUCTS, PRODUCTS_BY_ID, products_for_category
from app.database import Database
from app.formatters import cart_text, cart_total, money, valid_phone
from app.store import enriched_cart


class CatalogTests(unittest.TestCase):
    def test_catalog_has_required_categories_and_products(self) -> None:
        self.assertEqual(set(CATEGORIES), {"clothing", "accessories", "new"})
        self.assertGreaterEqual(len(PRODUCTS), 12)
        self.assertEqual(len(PRODUCTS_BY_ID), len(PRODUCTS))

    def test_each_category_has_products(self) -> None:
        for category in CATEGORIES:
            with self.subTest(category=category):
                self.assertGreaterEqual(len(products_for_category(category)), 1)

    def test_product_data_is_complete(self) -> None:
        for product in PRODUCTS:
            with self.subTest(product=product.id):
                self.assertTrue(product.name)
                self.assertTrue(product.description)
                self.assertGreater(product.price, 0)
                self.assertTrue(product.sku)
                self.assertGreaterEqual(product.stock, 0)
                self.assertTrue(product.placeholder)

    def test_formatters(self) -> None:
        items = [{"placeholder": "👕", "name": "Тест", "price": 1200, "quantity": 2}]
        self.assertEqual(cart_total(items), 2400)
        self.assertIn("2 400 ₽", cart_text(items))
        self.assertEqual(money(7490), "7 490 ₽")
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

    async def test_cart_quantity_and_removal(self) -> None:
        await self.db.add_to_cart(42, "oversize_tee")
        await self.db.add_to_cart(42, "oversize_tee")
        cart = await enriched_cart(self.db, 42)
        self.assertEqual(cart[0]["quantity"], 2)

        await self.db.set_cart_quantity(42, "oversize_tee", 1)
        cart = await enriched_cart(self.db, 42)
        self.assertEqual(cart[0]["quantity"], 1)

        await self.db.remove_from_cart(42, "oversize_tee")
        self.assertEqual(await enriched_cart(self.db, 42), [])

    async def test_order_transaction_saves_items_and_clears_cart(self) -> None:
        await self.db.add_to_cart(42, "oversize_tee")
        await self.db.add_to_cart(42, "city_cap")
        items = await enriched_cart(self.db, 42)
        checkout = {
            "user_id": 42,
            "username": "demo_user",
            "client_name": "Никита",
            "phone": "+7 900 000-00-00",
            "fulfillment": "delivery",
            "location": "Москва, демонстрационный адрес",
            "comment": "Тестовый заказ",
        }
        order_id = await self.db.create_order(checkout, items, cart_total(items))
        order = await self.db.get_order(order_id)

        self.assertEqual(order["status"], "new")
        self.assertEqual(len(order["items"]), 2)
        self.assertEqual(await enriched_cart(self.db, 42), [])
        self.assertEqual(len(await self.db.recent_for_user(42)), 1)
        stats = await self.db.stats()
        self.assertEqual(stats["total"], 1)
        self.assertEqual(stats["new"], 1)
        self.assertEqual(stats["revenue"], cart_total(items))

    async def test_empty_order_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            await self.db.create_order({"user_id": 1}, [], 0)


if __name__ == "__main__":
    unittest.main()

