from dotenv import load_dotenv  # noqa

load_dotenv()  # noqa


import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from . import cards, config, rules, types


def get_app() -> FastAPI:
    # log starting api
    print("Starting api")

    app = FastAPI(
        title="Unofficial Magic: The Gathering ChatGPT Plugin",
        description="An unofficial plugin for the OpenAI ChatGPT API that provides Magic: The Gathering rules and card information.",  # noqa
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
rules_db, app, start_time = (
    rules.get_rules_db(),
    get_app(),
    config.get_current_datetime(),
)
print(f"Started: {start_time}")


@app.get("/", summary="Status")
def read_root() -> types.RootResponse:
    """Returns the status of the API."""
    return {
        "status": "ok",
        "started_at": start_time.isoformat(),
    }


@app.get("/rules")
def query_rules(q: str) -> types.RulesResponse:
    """Accepts a search query in the form of a snippet of Magic: The Gathering rules text. Returns relevant rules as a result."""  # noqa
    return rules.query_rules(
        rules_db,
        q,
    )


@app.get("/card")
def find_card(name: str) -> types.CardResponse:
    """Accepts a Magic: The Gathering card name. Returns relevant card information as a result."""  # noqa
    return cards.find_by_name(
        cards.get_cards_db(),
        name,
    )


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
