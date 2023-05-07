import json

import requests

from . import config


class Scryfall:
    def __init__(self, data_path: str, url: str):
        self.cache = load_local_scryfall_data(data_path)
        self.url = url

    def get_uri(self, scryfall_id: str) -> str | None:
        print(f"getting uri for scryfall uuid: {scryfall_id}")

        card = self.get_card(scryfall_id)

        if card is None:
            print(f"card not found in scryfall: {scryfall_id}")
            return None

        uri = card["scryfall_uri"]

        if uri is None:
            print(f"card has no scryfall uri: {scryfall_id}")
            return None

        # remove utm
        uri = uri.split("?")[0]

        return str(uri)

    def get_card(self, scryfall_id: str) -> dict | None:
        print(f"getting card by id: {scryfall_id}")

        card = self.cache.get(scryfall_id)

        if card is not None:
            return dict(card)

        print(f"card not found in local cache: {scryfall_id}")

        try:
            return dict(
                requests.get(
                    f"{config.get_scryfall_url()}/cards/{scryfall_id}",
                ).json(),
            )
        except Exception as e:
            print(
                f"ran into error getting scryfall results for id: {scryfall_id} / {e}",  # noqa
            )

            return None

    def get_card_by_fuzzy_name(self, name: str) -> dict | None:
        print(f"getting card by fuzzy name: {name}")

        try:
            return dict(
                requests.get(f"{self.url}/cards/named?fuzzy={name}").json(),
            )
        except Exception as e:
            print(
                f"ran into error getting scryfall results for name: {name} / {e}",  # noqa
            )

            return None


def load_local_scryfall_data(data_path: str):
    print(f"loading local scryfall data: {data_path}")
    with open(data_path) as f:
        data = json.loads(f.read())

        # return data keyed by 'id'
        return {card["id"]: card for card in data}
