import csv
import datetime
import os
import uuid
import sqlite3

import chromadb
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware


def get_app():
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


def get_cards_db(
        cards_path="mtg_rules_chatgpt_plugin/data/AllPrintings.sqlite",
):
    # log loading cards
    print(f"Loading cards from {cards_path}")

    # load sqlite database
    return sqlite3.connect(cards_path)


def get_rules_db(
    rules_path="mtg_rules_chatgpt_plugin/data/magic-rules-2023-04-14.csv",
):
    # log loading rules
    print(f"Loading rules from {rules_path}")

    # load rules as csv
    with open(rules_path, newline="") as rules_file:
        reader = csv.DictReader(rules_file)
        documents = list(reader)

    # create db
    client = chromadb.Client()

    # log creating collection
    print("Creating collection")
    collection = client.create_collection("rules")

    # log adding documents
    print("Adding documents")
    # add documents to collection
    collection.add(
        documents=[
            # join all fields into one text
            "|".join(doc.values())
            for doc in documents
        ],
        # add all fields as metadata
        metadatas=documents,
        ids=[
            # generate uuids for each document
            uuid.uuid4().hex
            for _ in documents
        ],
    )

    # log done
    print("Done")
    return collection


# start app
rules_db, app, start_time = get_rules_db(), get_app(), datetime.datetime.now()
print(f"Started: {start_time}")


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.get("/rules")
def query_rules(q: str):
    """
    Query an up to date edition of the Magic: The Gathering rules database for a given query string.
    """  # noqa
    matches = rules_db.query(
        query_texts=[q],
        n_results=5,
    )

    try:
        matches = matches["documents"][0]
    except IndexError:
        matches = []

    return {"matches": matches}


@app.get("/card")
def query_cards(q: str):
    """
    Query an up to date edition of the Magic: The Gathering cards database by exact card name.
    """  # noqa
    cards_db = get_cards_db()

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
                types,
                text,
                toughness
            FROM
                cards
            WHERE
                name = ?
            """,
        (q,),
    )

    card = results.fetchone()

    # return card formatted as dict
    return {
        "match": {
            "artist": card[0],
            "colors": card[1],
            "keywords": card[2],
            "loyalty": card[3],
            "manaCost": card[4],
            "manaValue": card[5],
            "setCode": card[6],
            "types": card[7],
            "text": card[8],
            "toughness": card[9],
        },
    }


@app.get("/logo.png")
def get_logo():
    return FileResponse("mtg_rules_chatgpt_plugin/data/logo.png")


@app.get("/.well-known/ai-plugin.json")
def get_ai_plugin():
    return FileResponse("mtg_rules_chatgpt_plugin/data/ai-plugin.json")


def get_host():
    return os.getenv("HOST", "localhost")


def get_port():
    return os.getenv("PORT", 5003)


def get_env():
    return os.getenv("ENV", "LOCAL")


def start():
    dev_mode = get_env() == "LOCAL"

    uvicorn.run(
        "mtg_rules_chatgpt_plugin.main:app",
        host=get_host(),
        port=get_port(),
        reload=dev_mode,
    )
