import sqlite3
from sqlite3 import Connection

from pydantic import BaseModel

from . import config


class Card(BaseModel):
    artist: str
    colors: str | None
    keywords: str | None
    loyalty: str
    manaCost: str
    manaValue: str
    setCode: str
    text: str
    toughness: str
    types: str | None
    uuid: str


def get_cards_db() -> Connection:
    cards_path = config.get_cards_db_path()

    # log loading cards
    print(f"Loading cards from {cards_path}")

    # load sqlite database
    return sqlite3.connect(cards_path)


def find_by_name(cards_db: Connection, name: str) -> Card | None:
    results = cards_db.execute(
        """
        SELECT
            artist,
            colors,
            keywords,
            loyalty,
            manaCost,
            manaValue,
            setCode,
            text,
            toughness,
            types,
            uuid
        FROM
            cards
        WHERE
            name = ?
        """,
        (name,),
    )

    card = results.fetchone()

    if card is None:
        return None

    return row_to_card(card)


def row_to_card(row: sqlite3.Row) -> Card:
    return Card(
        artist=row[0],
        uuid=row[1],
        colors=row[2],
        keywords=row[3],
        loyalty=row[4],
        manaCost=row[5],
        manaValue=row[6],
        setCode=row[7],
        types=row[8],
        text=row[9],
        toughness=row[10],
    )
