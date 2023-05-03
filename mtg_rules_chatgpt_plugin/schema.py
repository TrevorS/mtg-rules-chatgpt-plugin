import decimal

from pydantic import BaseModel


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
                "setCode": "PLC",
                "text": "Destroy all creatures. They can’t be regenerated.",
                "toughness": None,
                "types": "Sorcery",
                "uuid": "280111ea-c53a-552f-9078-41148322ee96",
            }
        }


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
