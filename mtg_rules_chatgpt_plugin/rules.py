import csv
import uuid
from typing import List

import chromadb
from chromadb.api.models.Collection import Collection
from chromadb.config import Settings
from pydantic import BaseModel

from . import config


class Rule(BaseModel):
    title: str
    text: str
    number: str

    class Config:
        schema_extra = {
            "example": {
                "title": "General",
                "number": "100.1.",
                "text": "These Magic rules apply to any Magic game with two or more players, including two-player games and multiplayer games.",  # noqa
            }
        }

    @staticmethod
    def from_row(row: dict) -> "Rule":
        return Rule(
            title=row["title"],
            text=row["text"],
            number=row["number"],
        )


def get_rules_db() -> Collection:
    # create db or load existing rules vectorstore
    client = chromadb.Client(
        Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=config.get_rules_vs_path(),
        ),
    )

    # log creating collection
    print("Loading existing or creating new rules collection")
    collection = client.get_or_create_collection("rules")

    # if collection is empty, add documents
    if collection.count() == 0:
        print("Collection is empty, adding rules")
        rules_path = config.get_rules_csv_path()

        # log loading rules
        print(f"Loading rules from {rules_path}")

        # load rules as csv
        with open(rules_path, newline="") as rules_file:
            reader = csv.DictReader(rules_file)
            documents = list(reader)

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


def query_rules(
    rules_db: Collection,
    q: str,
    n_results: int = 10,
) -> List[Rule]:
    rules = rules_db.query(
        query_texts=[q],
        n_results=5,
    )

    try:
        rows = rules["metadatas"][0]
    except IndexError:
        rows = []

    return [Rule.from_row(row) for row in rows]
