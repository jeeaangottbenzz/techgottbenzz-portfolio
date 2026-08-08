from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Service:
    id: str
    category: str
    name: str
    description: str
    duration: int
    price: int


@dataclass(frozen=True, slots=True)
class Master:
    id: str
    name: str
    role: str
    categories: tuple[str, ...]


CATEGORIES = {
    "manicure": "💅 Маникюр",
    "pedicure": "🦶 Педикюр",
    "brows": "✨ Брови",
    "lashes": "🪄 Ресницы",
    "hair": "💇 Волосы",
}

SERVICES = (
    Service("manicure_classic", "manicure", "Классический маникюр", "Аккуратная обработка ногтей и уход за кутикулой.", 60, 1800),
    Service("manicure_gel", "manicure", "Маникюр с покрытием", "Маникюр и стойкое однотонное покрытие.", 100, 2800),
    Service("nail_design", "manicure", "Маникюр с дизайном", "Покрытие с лаконичным дизайном до четырёх ногтей.", 120, 3400),
    Service("pedicure_classic", "pedicure", "Классический педикюр", "Обработка стоп и ногтей с базовым уходом.", 75, 2600),
    Service("pedicure_gel", "pedicure", "Педикюр с покрытием", "Полный педикюр и стойкое однотонное покрытие.", 110, 3600),
    Service("brow_shape", "brows", "Коррекция бровей", "Подбор формы и деликатная коррекция.", 35, 1200),
    Service("brow_color", "brows", "Коррекция и окрашивание", "Форма и окрашивание с подбором оттенка.", 60, 1900),
    Service("brow_lamination", "brows", "Ламинирование бровей", "Укладка, коррекция и уход для выразительной формы.", 75, 2500),
    Service("lashes_classic", "lashes", "Классическое наращивание", "Естественный объём и аккуратный изгиб.", 120, 3500),
    Service("lashes_lamination", "lashes", "Ламинирование ресниц", "Изгиб, окрашивание и питательный уход.", 80, 2800),
    Service("haircut", "hair", "Женская стрижка", "Консультация, стрижка и лёгкая укладка.", 75, 3200),
    Service("hair_color", "hair", "Окрашивание в один тон", "Ровный оттенок с учётом длины и состояния волос.", 150, 6500),
    Service("hair_styling", "hair", "Укладка", "Лёгкая повседневная или вечерняя укладка.", 60, 2500),
)

MASTERS = (
    Master("alina", "Алина", "Nail-мастер", ("manicure", "pedicure")),
    Master("maria", "Мария", "Brow & lash-мастер", ("brows", "lashes")),
    Master("sofia", "София", "Стилист по волосам", ("hair",)),
    Master("elena", "Елена", "Универсальный мастер", tuple(CATEGORIES)),
)

SERVICES_BY_ID = {service.id: service for service in SERVICES}
MASTERS_BY_ID = {master.id: master for master in MASTERS}


def services_for_category(category: str) -> tuple[Service, ...]:
    return tuple(service for service in SERVICES if service.category == category)


def masters_for_category(category: str) -> tuple[Master, ...]:
    return tuple(master for master in MASTERS if category in master.categories)

