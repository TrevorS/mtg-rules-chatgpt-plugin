from dotenv import load_dotenv  # noqa

load_dotenv()  # noqa

from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from . import cards, config, rules


def get_app() -> FastAPI:
    # log starting api
    print("Starting api")

    app = FastAPI()

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


@app.get("/")
def read_root():
    return {
        "status": "ok",
        "started_at": start_time.isoformat(),
    }


@app.get(
    "/rules",
    description="""
    Accepts a search query in the form of a snippet of Magic: The Gathering rules text. Returns relevant rules as a result.
    """,  # noqa
)
def query_rules(q: str) -> List[rules.Rule]:
    return rules.query_rules(
        rules_db,
        q,
    )


@app.get(
    "/card",
    description="""
    Accepts a Magic: The Gathering card name. Returns relevant card information as a result.
    """,  # noqa
)
def find_card(name: str) -> cards.Card | None:
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
