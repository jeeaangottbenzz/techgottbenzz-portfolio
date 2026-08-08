from collections.abc import Mapping
from pathlib import Path

import aiosqlite


class Database:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)

    async def initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.path) as connection:
            await connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS cart_items (
                    user_id INTEGER NOT NULL,
                    product_id TEXT NOT NULL,
                    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
                    PRIMARY KEY (user_id, product_id)
                );

                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    username TEXT,
                    client_name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    fulfillment TEXT NOT NULL CHECK (fulfillment IN ('pickup', 'delivery')),
                    location TEXT NOT NULL,
                    comment TEXT,
                    total INTEGER NOT NULL CHECK (total >= 0),
                    status TEXT NOT NULL DEFAULT 'new'
                        CHECK (status IN ('new', 'confirmed', 'packing', 'shipped', 'completed', 'cancelled')),
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
                    product_id TEXT NOT NULL,
                    sku TEXT NOT NULL,
                    name TEXT NOT NULL,
                    price INTEGER NOT NULL,
                    quantity INTEGER NOT NULL CHECK (quantity > 0)
                );

                CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id, created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status, created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
                """
            )
            await connection.commit()

    async def add_to_cart(self, user_id: int, product_id: str) -> None:
        async with aiosqlite.connect(self.path) as connection:
            await connection.execute(
                """
                INSERT INTO cart_items (user_id, product_id, quantity) VALUES (?, ?, 1)
                ON CONFLICT(user_id, product_id)
                DO UPDATE SET quantity = quantity + 1
                """,
                (user_id, product_id),
            )
            await connection.commit()

    async def set_cart_quantity(self, user_id: int, product_id: str, quantity: int) -> None:
        async with aiosqlite.connect(self.path) as connection:
            if quantity <= 0:
                await connection.execute(
                    "DELETE FROM cart_items WHERE user_id = ? AND product_id = ?",
                    (user_id, product_id),
                )
            else:
                await connection.execute(
                    "UPDATE cart_items SET quantity = ? WHERE user_id = ? AND product_id = ?",
                    (quantity, user_id, product_id),
                )
            await connection.commit()

    async def remove_from_cart(self, user_id: int, product_id: str) -> None:
        async with aiosqlite.connect(self.path) as connection:
            await connection.execute(
                "DELETE FROM cart_items WHERE user_id = ? AND product_id = ?",
                (user_id, product_id),
            )
            await connection.commit()

    async def clear_cart(self, user_id: int) -> None:
        async with aiosqlite.connect(self.path) as connection:
            await connection.execute("DELETE FROM cart_items WHERE user_id = ?", (user_id,))
            await connection.commit()

    async def raw_cart(self, user_id: int) -> list[dict]:
        return await self._fetch_all(
            "SELECT product_id, quantity FROM cart_items WHERE user_id = ? ORDER BY rowid",
            (user_id,),
        )

    async def create_order(
        self,
        checkout: Mapping[str, object],
        items: list[dict],
        total: int,
    ) -> int:
        if not items:
            raise ValueError("Нельзя оформить заказ с пустой корзиной")

        async with aiosqlite.connect(self.path) as connection:
            await connection.execute("PRAGMA foreign_keys = ON")
            try:
                await connection.execute("BEGIN IMMEDIATE")
                cursor = await connection.execute(
                    """
                    INSERT INTO orders (
                        user_id, username, client_name, phone,
                        fulfillment, location, comment, total, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'new')
                    """,
                    (
                        checkout["user_id"],
                        checkout.get("username"),
                        checkout["client_name"],
                        checkout["phone"],
                        checkout["fulfillment"],
                        checkout["location"],
                        checkout.get("comment"),
                        total,
                    ),
                )
                order_id = int(cursor.lastrowid)
                await connection.executemany(
                    """
                    INSERT INTO order_items (
                        order_id, product_id, sku, name, price, quantity
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    [
                        (
                            order_id,
                            item["product_id"],
                            item["sku"],
                            item["name"],
                            item["price"],
                            item["quantity"],
                        )
                        for item in items
                    ],
                )
                await connection.execute(
                    "DELETE FROM cart_items WHERE user_id = ?",
                    (checkout["user_id"],),
                )
                await connection.commit()
                return order_id
            except Exception:
                await connection.rollback()
                raise

    async def get_order(self, order_id: int) -> dict | None:
        rows = await self._fetch_all("SELECT * FROM orders WHERE id = ?", (order_id,))
        if not rows:
            return None
        order = rows[0]
        order["items"] = await self._fetch_all(
            "SELECT * FROM order_items WHERE order_id = ? ORDER BY id",
            (order_id,),
        )
        return order

    async def recent_for_user(self, user_id: int, limit: int = 5) -> list[dict]:
        return await self._fetch_all(
            "SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC, id DESC LIMIT ?",
            (user_id, limit),
        )

    async def recent_orders(self, limit: int = 10) -> list[dict]:
        orders = await self._fetch_all(
            "SELECT * FROM orders ORDER BY created_at DESC, id DESC LIMIT ?",
            (limit,),
        )
        for order in orders:
            order["items"] = await self._fetch_all(
                "SELECT * FROM order_items WHERE order_id = ? ORDER BY id",
                (order["id"],),
            )
        return orders

    async def stats(self) -> dict[str, int]:
        async with aiosqlite.connect(self.path) as connection:
            connection.row_factory = aiosqlite.Row
            cursor = await connection.execute("SELECT status, COUNT(*) AS count FROM orders GROUP BY status")
            result = {row["status"]: row["count"] for row in await cursor.fetchall()}
            cursor = await connection.execute("SELECT COUNT(*) AS count, COALESCE(SUM(total), 0) AS revenue FROM orders")
            totals = await cursor.fetchone()
            result["total"] = totals["count"]
            result["revenue"] = totals["revenue"]
            return result

    async def _fetch_all(self, query: str, parameters: tuple = ()) -> list[dict]:
        async with aiosqlite.connect(self.path) as connection:
            connection.row_factory = aiosqlite.Row
            cursor = await connection.execute(query, parameters)
            return [dict(row) for row in await cursor.fetchall()]

