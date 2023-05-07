import decimal
import json
import random

from pydantic import BaseModel


def decimal_to_float(value: decimal.Decimal | None) -> float | None:
    if value is None:
        return None

    return float(value)


def generate_booster(draft_set: "DraftSet"):
    data = json.loads(draft_set.booster)

    boosters = data["default"]["boosters"]
    booster_choice = random.choices(
        boosters, weights=[booster["weight"] for booster in boosters], k=1
    )[0]

    # Generate a booster pack
    booster_pack = []
    sheets = data["default"]["sheets"]

    for card_type, count in booster_choice["contents"].items():
        cards = sheets[card_type]["cards"]
        card_uuids = random.choices(list(cards.keys()), k=count)
        booster_pack.extend(card_uuids)

    return booster_pack


class DraftSet(BaseModel):
    id: int
    base_set_size: int
    block: str | None
    booster: str
    code: str
    name: str
    release_date: str
    token_set_code: str | None
    total_set_size: int | None
    set_type: str

    class Config:
        orm_mode = (True,)

    @classmethod
    def from_orm(cls, set_orm):
        return cls(
            id=set_orm.id,
            base_set_size=set_orm.baseSetSize,
            block=set_orm.block,
            booster=set_orm.booster,
            code=set_orm.code,
            name=set_orm.name,
            release_date=set_orm.releaseDate.isoformat(),
            token_set_code=set_orm.tokenSetCode,
            total_set_size=set_orm.totalSetSize,
            set_type=set_orm.type,
        )


class Card(BaseModel):
    artist: str | None
    colors: str | None
    keywords: str | None
    loyalty: str | None
    mana_cost: str | None
    mana_value: float | None
    name: str | None
    power: str | None
    scryfall_id: str | None
    set_code: str | None
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
                "mana_cost": "{2}{B}{B}",
                "mana_value": "4",
                "name": "Damnation",
                "scryfall_id": "26c68473-70ca-40ba-b5c6-71ec30f88a2c",
                "set_code": "PLC",
                "text": "Destroy all creatures. They can’t be regenerated.",
                "toughness": None,
                "types": "Sorcery",
                "uuid": "280111ea-c53a-552f-9078-41148322ee96",
            }
        }

    @classmethod
    def from_orm(cls, card_orm):
        return cls(
            artist=card_orm.artist,
            colors=card_orm.colors,
            keywords=card_orm.keywords,
            loyalty=card_orm.loyalty,
            mana_cost=card_orm.manaCost,
            mana_value=decimal_to_float(card_orm.manaValue),
            name=card_orm.name,
            power=card_orm.power,
            scryfall_id=card_orm.scryfallId,
            set_code=card_orm.setCode,
            text=card_orm.text,
            toughness=card_orm.toughness,
            types=card_orm.types,
            uuid=card_orm.uuid,
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

    @classmethod
    def from_orm(cls, rule_orm):
        return cls(
            distance=rule_orm.distance,
            number=rule_orm.number,
            text=rule_orm.text,
            title=rule_orm.title,
        )
