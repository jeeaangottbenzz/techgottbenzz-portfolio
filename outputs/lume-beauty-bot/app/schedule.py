from datetime import date, timedelta


BASE_TIMES = ("10:00", "11:30", "13:00", "14:30", "16:00", "17:30", "19:00")


def upcoming_dates(days: int = 7) -> list[date]:
    """Return the next working dates, excluding Sundays."""
    result: list[date] = []
    current = date.today()
    while len(result) < days:
        if current.weekday() != 6:
            result.append(current)
        current += timedelta(days=1)
    return result


def available_times(day: date, master_id: str, booked: set[str] | None = None) -> list[str]:
    """Generate stable demo slots and exclude times already stored in the database."""
    booked = booked or set()
    offset = (day.toordinal() + sum(map(ord, master_id))) % 3
    generated = [time for index, time in enumerate(BASE_TIMES) if (index + offset) % 3 != 0]
    return [time for time in generated if time not in booked]

