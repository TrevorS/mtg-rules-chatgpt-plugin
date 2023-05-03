import databases
import sqlalchemy
from sqlalchemy import Column, Float, String, select

from . import config

database = databases.Database(f"sqlite:///{config.get_cards_db_path()}")
metadata = sqlalchemy.MetaData()

cards = sqlalchemy.Table(
    "cards",
    metadata,
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
