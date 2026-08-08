from collections.abc import Mapping
from datetime import date
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
                CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    username TEXT,
                    service_id TEXT NOT NULL,
                    service_name TEXT NOT NULL,
                    master_id TEXT NOT NULL,
                    master_name TEXT NOT NULL,
                    appointment_date TEXT NOT NULL,
                    appointment_time TEXT NOT NULL,
                    client_name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    comment TEXT,
                    status TEXT NOT NULL DEFAULT 'new'
                        CHECK (status IN ('new', 'confirmed', 'completed', 'cancelled')),
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(master_id, appointment_date, appointment_time)
                );

                CREATE INDEX IF NOT EXISTS idx_appointments_user
                    ON appointments(user_id, created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_appointments_date
                    ON appointments(appointment_date, appointment_time);
                """
            )
            await connection.commit()

    async def create_appointment(self, data: Mapping[str, object]) -> int:
        async with aiosqlite.connect(self.path) as connection:
            cursor = await connection.execute(
                """
                INSERT INTO appointments (
                    user_id, username, service_id, service_name,
                    master_id, master_name, appointment_date, appointment_time,
                    client_name, phone, comment, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'new')
                """,
                (
                    data["user_id"],
                    data.get("username"),
                    data["service_id"],
                    data["service_name"],
                    data["master_id"],
                    data["master_name"],
                    data["appointment_date"],
                    data["appointment_time"],
                    data["client_name"],
                    data["phone"],
                    data.get("comment"),
                ),
            )
            await connection.commit()
            return int(cursor.lastrowid)

    async def get_appointment(self, appointment_id: int) -> dict | None:
        query = "SELECT * FROM appointments WHERE id = ?"
        rows = await self._fetch_all(query, (appointment_id,))
        return rows[0] if rows else None

    async def recent_for_user(self, user_id: int, limit: int = 5) -> list[dict]:
        return await self._fetch_all(
            "SELECT * FROM appointments WHERE user_id = ? ORDER BY created_at DESC, id DESC LIMIT ?",
            (user_id, limit),
        )

    async def recent(self, limit: int = 10) -> list[dict]:
        return await self._fetch_all(
            "SELECT * FROM appointments ORDER BY created_at DESC, id DESC LIMIT ?",
            (limit,),
        )

    async def for_date(self, appointment_date: str) -> list[dict]:
        return await self._fetch_all(
            "SELECT * FROM appointments WHERE appointment_date = ? ORDER BY appointment_time",
            (appointment_date,),
        )

    async def booked_times(self, master_id: str, appointment_date: str) -> set[str]:
        rows = await self._fetch_all(
            """
            SELECT appointment_time FROM appointments
            WHERE master_id = ? AND appointment_date = ? AND status != 'cancelled'
            """,
            (master_id, appointment_date),
        )
        return {row["appointment_time"] for row in rows}

    async def stats(self) -> dict[str, int]:
        async with aiosqlite.connect(self.path) as connection:
            connection.row_factory = aiosqlite.Row
            cursor = await connection.execute(
                "SELECT status, COUNT(*) AS count FROM appointments GROUP BY status"
            )
            result = {row["status"]: row["count"] for row in await cursor.fetchall()}
            cursor = await connection.execute("SELECT COUNT(*) AS count FROM appointments")
            result["total"] = (await cursor.fetchone())["count"]
            cursor = await connection.execute(
                "SELECT COUNT(*) AS count FROM appointments WHERE appointment_date = ?",
                (date.today().isoformat(),),
            )
            result["today"] = (await cursor.fetchone())["count"]
            return result

    async def _fetch_all(self, query: str, parameters: tuple = ()) -> list[dict]:
        async with aiosqlite.connect(self.path) as connection:
            connection.row_factory = aiosqlite.Row
            cursor = await connection.execute(query, parameters)
            return [dict(row) for row in await cursor.fetchall()]

