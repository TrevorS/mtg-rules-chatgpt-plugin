import requests

BASE_URL = "https://api.scryfall.com"


def get_uri(scryfall_uuid) -> str | None:
    card = get_card_by_id(scryfall_uuid)

    if card is None:
        return None

    return card["scryfall_uri"]


def get_card_by_id(id) -> dict | None:
    try:
        return requests.get(f"{BASE_URL}/cards/{id}").json()
    except Exception as e:
        print(f"ran into error getting scryfall results for id: {id} / {e}")
        return None
