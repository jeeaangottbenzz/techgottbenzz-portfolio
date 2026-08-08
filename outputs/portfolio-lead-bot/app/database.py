from collections.abc import Mapping
from pathlib import Path

import aiosqlite


LEAD_COOLDOWN_SECONDS = 60


class LeadRateLimitError(RuntimeError):
    """Raised when one Telegram user submits leads too quickly."""


class Database:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)

    async def initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.path) as connection:
            await connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    username TEXT,
                    service TEXT NOT NULL,
                    description TEXT NOT NULL,
                    budget TEXT NOT NULL,
                    deadline TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'new'
                        CHECK (status IN ('new', 'contacted', 'completed', 'cancelled')),
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE INDEX IF NOT EXISTS idx_leads_created
                    ON leads(created_at DESC, id DESC);
                CREATE INDEX IF NOT EXISTS idx_leads_user
                    ON leads(user_id, created_at DESC);
                """
            )
            await connection.commit()

    async def create_lead(self, data: Mapping[str, object]) -> int:
        async with aiosqlite.connect(self.path) as connection:
            await connection.execute("BEGIN IMMEDIATE")
            cursor = await connection.execute(
                """
                SELECT 1
                FROM leads
                WHERE user_id = ?
                  AND created_at >= datetime('now', ?)
                LIMIT 1
                """,
                (data["user_id"], f"-{LEAD_COOLDOWN_SECONDS} seconds"),
            )
            if await cursor.fetchone():
                raise LeadRateLimitError(
                    f"Повторная заявка доступна через {LEAD_COOLDOWN_SECONDS} секунд."
                )

            cursor = await connection.execute(
                """
                INSERT INTO leads (
                    user_id, username, service, description,
                    budget, deadline, contact, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'new')
                """,
                (
                    data["user_id"],
                    data.get("username"),
                    data["service"],
                    data["description"],
                    data["budget"],
                    data["deadline"],
                    data["contact"],
                ),
            )
            await connection.commit()
            return int(cursor.lastrowid)

    async def get_lead(self, lead_id: int) -> dict | None:
        rows = await self._fetch_all("SELECT * FROM leads WHERE id = ?", (lead_id,))
        return rows[0] if rows else None

    async def recent(self, limit: int = 10) -> list[dict]:
        return await self._fetch_all(
            "SELECT * FROM leads ORDER BY created_at DESC, id DESC LIMIT ?", (limit,)
        )

    async def stats(self) -> dict[str, int]:
        async with aiosqlite.connect(self.path) as connection:
            connection.row_factory = aiosqlite.Row
            cursor = await connection.execute(
                "SELECT status, COUNT(*) AS count FROM leads GROUP BY status"
            )
            result = {row["status"]: row["count"] for row in await cursor.fetchall()}
            cursor = await connection.execute("SELECT COUNT(*) AS count FROM leads")
            result["total"] = (await cursor.fetchone())["count"]
            return result

    async def _fetch_all(self, query: str, parameters: tuple = ()) -> list[dict]:
        async with aiosqlite.connect(self.path) as connection:
            connection.row_factory = aiosqlite.Row
            cursor = await connection.execute(query, parameters)
            return [dict(row) for row in await cursor.fetchall()]
