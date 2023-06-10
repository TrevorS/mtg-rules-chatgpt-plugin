# ruff: noqa: E402
from dotenv import load_dotenv  # noqa: E402

load_dotenv()  # noqa: E402

import uuid

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from . import config, models, rules, schema, scryfall, types


def get_app() -> FastAPI:
    # log starting api
    print("Starting api")

    app = FastAPI(
        title="MagiCodex",
        description="Ask about Magic: The Gathering cards, rules and interactions.",  # noqa
        version="0.1.0",
    )

    # add cors for chat.openai.com
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://chat.openai.com"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


# start app
rules_db, app, start_time, scryfall_db = (
    rules.get_rules_db(),
    get_app(),
    config.get_current_datetime(),
    scryfall.Scryfall(
        config.get_scryfall_cache_path(),
        config.get_scryfall_url(),
    ),
)
print(f"Started: {start_time}")


@app.on_event("startup")
async def startup():
    await models.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await models.database.disconnect()


@app.get("/", include_in_schema=False)
def read_root() -> types.RootResponse:
    return {"status": "ok", "started_at": start_time.isoformat()}


@app.get("/rules", summary="Query rules by semantic query.")
def query_rules(q: str) -> types.RulesResponse:
    """
    Accepts a semantic query in the form of a snippet of
    Magic: The Gathering rules text.
    * Returns relevant rules as a result.
    """
    results = rules.query_rules(
        rules_db,
        q,
    )

    return [schema.Rule(**result.dict()) for result in results]


@app.get("/cards", summary="Query cards by exact parameters.")
async def query_cards(
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
    uuid: uuid.UUID | None = None,
):
    """
    Accepts a search query in the form of a GET request
    with multiple optional query parameters.
    * Returns relevant cards as a result.
    * Parameters are combined with AND logic.
    * Limited to 10 results at a time.
    """
    str_uuid = None

    if uuid is not None:
        str_uuid = str(uuid)

    stmt = models.build_card_query(
        artist=artist,
        colors=colors,
        keywords=keywords,
        loyalty=loyalty,
        mana_cost=mana_cost,
        mana_value=mana_value,
        name=name,
        power=power,
        scryfall_id=scryfall_id,
        set_code=set_code,
        text=text,
        toughness=toughness,
        types=types,
        uuid=str_uuid,
    ).limit(10)

    cards = await models.database.fetch_all(stmt)

    return [schema.Card.from_orm(card, scryfall_db) for card in cards]


@app.get("/fuzzy", summary="Get card by fuzzy search on card name.")
async def get_fuzzy_card_name(card_name: str):
    """Accepts a card name and returns the card with the closest name."""
    scryfall_card = scryfall_db.get_card_by_fuzzy_name(card_name)

    if scryfall_card is None:
        raise HTTPException(status_code=404, detail="Card not found")

    if scryfall_card["object"] == "error":
        raise HTTPException(status_code=400, detail=scryfall_card["details"])

    stmt = models.build_card_query(scryfall_id=scryfall_card["id"])

    card = await models.database.fetch_one(stmt)

    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")

    return schema.Card.from_orm(card, scryfall_db)


@app.get("/random", summary="Get a random card")
async def get_random_card():
    """Returns a random card"""
    stmt = models.get_random_card()

    card = await models.database.fetch_one(stmt)

    if card is None:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return schema.Card.from_orm(card, scryfall_db)


@app.get(
    "/booster/{set_code}",
    summary="Get a booster pack from a set by set code.",
)
async def get_booster(set_code: str) -> types.CardsResponse:
    stmt = models.build_set_query(set_code=set_code)

    draft_set = await models.database.fetch_one(stmt)

    if draft_set is None:
        raise HTTPException(status_code=404, detail="Set not found")

    draft_set = schema.DraftSet.from_orm(draft_set)

    if draft_set is None:
        raise HTTPException(status_code=500, detail="Something went wrong")

    uuids = schema.generate_booster(draft_set)  # type: ignore

    stmt = models.get_cards_by_uuids(uuids)

    cards = await models.database.fetch_all(stmt)

    return [schema.Card.from_orm(card, scryfall_db) for card in cards]


@app.get("/logo.png")
def get_logo():
    return FileResponse("mtg_rules_chatgpt_plugin/data/logo.png")


@app.get("/.well-known/ai-plugin.json")
def get_ai_plugin():
    return FileResponse("mtg_rules_chatgpt_plugin/data/ai-plugin.json")


def start():
    uvicorn.run(
        "mtg_rules_chatgpt_plugin.main:app",
        host=config.get_host(),
        port=config.get_port(),
        reload=config.is_dev_mode(),
    )
