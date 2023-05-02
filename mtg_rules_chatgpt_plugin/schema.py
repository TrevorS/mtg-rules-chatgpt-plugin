import decimal

from pydantic import BaseModel

from . import models, rules, scryfall


def decimal_to_float(value: decimal.Decimal | None) -> float | None:
    if value is None:
        return None

    return float(value)


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
        orm_mode = (True,)
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
    def from_record(record: models.Card) -> "Card":
        return Card(
            artist=record.artist,
            colors=record.colors,
            keywords=record.keywords,
            loyalty=record.loyalty,
            manaCost=record.manaCost,
            manaValue=decimal_to_float(record.manaValue),
            power=record.power,
            scryfall_id=record.scryfallId,
            scryfall_uri=scryfall.get_uri(record.scryfallId),
            setCode=record.setCode,
            text=record.text,
            toughness=record.toughness,
            types=record.types,
            uuid=record.uuid,
        )


class Rule(BaseModel):
    distance: float
    number: str
    text: str
    title: str

    class Config:
        orm_mode = (True,)
        schema_extra = {
            "example": {
                "distance": 1.42,
                "number": "100.1.",
                "text": "These Magic rules apply to any Magic game with two or more players, including two-player games and multiplayer games.",  # noqa
                "title": "General",
            }
        }

    @staticmethod
    def from_record(record: rules.Rule) -> "Rule":
        return Rule(
            distance=float(record.distance),
            number=record.number,
            text=record.text,
            title=record.title,
        )
