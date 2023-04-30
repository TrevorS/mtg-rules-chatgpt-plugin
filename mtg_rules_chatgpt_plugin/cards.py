import sqlite3
from sqlite3 import Connection

from pydantic import BaseModel

from . import config


class Card(BaseModel):
    artist: str | None
    colors: str | None
    keywords: str | None
    loyalty: str | None
    manaCost: str | None
    manaValue: float | None
    power: str | None
    setCode: str | None
    text: str | None
    toughness: str | None
    types: str | None
    uuid: str

    class Config:
        schema_extra = {
            "example": {
                "artist": "Kev Walker",
                "colors": "B",
                "keywords": None,
                "loyalty": None,
                "manaCost": "{2}{B}{B}",
                "manaValue": "4",
                "setCode": "PLC",
                "text": "Destroy all creatures. They can’t be regenerated.",
                "toughness": None,
                "types": "Sorcery",
                "uuid": "280111ea-c53a-552f-9078-41148322ee96",
            }
        }

    @staticmethod
    def from_row(row: sqlite3.Row) -> "Card":
        return Card(
            artist=row[0],
            colors=row[1],
            keywords=row[2],
            loyalty=row[3],
            manaCost=row[4],
            manaValue=row[5],
            power=row[6],
            setCode=row[7],
            text=row[8],
            toughness=row[9],
            types=row[10],
            uuid=row[11],
        )


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
            power,
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

    return Card.from_row(card)
