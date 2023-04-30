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
    scryfall_id: str | None
    scryfall_uri: str | None
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
                "scryfall_id": "26c68473-70ca-40ba-b5c6-71ec30f88a2c",
                "scryfall_uri": "https://scryfall.com/card/plc/85/damnation?utm_source=api",  # noqa
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
            scryfall_id=row[7],
            scryfall_uri=None,
            setCode=row[8],
            text=row[9],
            toughness=row[10],
            types=row[11],
            uuid=row[12],
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
            scryfallId,
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
