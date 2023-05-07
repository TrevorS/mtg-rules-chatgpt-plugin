import databases
import sqlalchemy
from sqlalchemy import Column, Date, Float, Integer, String, select

from . import config

database = databases.Database(f"sqlite:///{config.get_cards_db_path()}")
metadata = sqlalchemy.MetaData()

cards = sqlalchemy.Table(
    "cards",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("artist", String, nullable=True),
    Column("colors", String, nullable=True),
    Column("keywords", String, nullable=True),
    Column("loyalty", String, nullable=True),
    Column("manaCost", String, nullable=True),
    Column("manaValue", Float, nullable=True),
    Column("name", String, nullable=True),
    Column("power", String, nullable=True),
    Column("scryfallId", String, nullable=True),
    Column("setCode", String, nullable=True),
    Column("text", String, nullable=True),
    Column("toughness", String, nullable=True),
    Column("types", String, nullable=True),
    Column("uuid", String, primary_key=True),
)


def get_random_card() -> select:
    return select(cards.c).order_by(sqlalchemy.func.random()).limit(1)


def build_card_query(
    artist: str | None = None,
    colors: str | None = None,
    keywords: str | None = None,
    loyalty: str | None = None,
    mana_cost: str | None = None,
    mana_value: float | None = None,
    name: str | None = None,
    power: str | None = None,
    scryfall_id: str | None = None,
    set_code: str | None = None,
    text: str | None = None,
    toughness: str | None = None,
    types: str | None = None,
    uuid: str | None = None,
) -> select:
    stmt = select(cards.c)

    for column, value in (
        ("artist", artist),
        ("colors", colors),
        ("keywords", keywords),
        ("loyalty", loyalty),
        ("manaCost", mana_cost),
        ("manaValue", mana_value),
        ("name", name),
        ("power", power),
        ("scryfallId", scryfall_id),
        ("setCode", set_code),
        ("text", text),
        ("toughness", toughness),
        ("types", types),
        ("uuid", uuid),
    ):
        if value:
            stmt = stmt.where(getattr(cards.c, column) == value)

    return stmt


def get_cards_by_uuids(uuids: list[str]) -> select:
    return select(cards.c).where(cards.c.uuid.in_(uuids))


sets = sqlalchemy.Table(
    "sets",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("baseSetSize", Integer, nullable=True),
    Column("block", String, nullable=True),
    Column("booster", String, nullable=True),
    Column("code", String(8), unique=True, nullable=False),
    Column("name", String, nullable=True),
    Column("releaseDate", Date, nullable=True),
    Column("tokenSetCode", String, nullable=True),
    Column("totalSetSize", Integer, nullable=True),
    Column("type", String, nullable=True),
)


def build_set_query(set_code: str):
    return select(sets.c).where(sets.c.code == set_code)
