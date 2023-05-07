import datetime
import os


def get_host() -> str:
    return os.environ["HOST"]


def get_port() -> int:
    return int(os.environ["PORT"])


def get_env() -> str:
    return os.environ["ENV"]


def get_cards_db_path() -> str:
    return os.environ["CARDS_DB"]


def get_cards_vs_path() -> str:
    return os.environ["CARDS_VS"]


def get_rules_csv_path() -> str:
    return os.environ["RULES_CSV"]


def get_rules_vs_path() -> str:
    return os.environ["RULES_VS"]


def get_scryfall_url() -> str:
    return os.environ["SCRYFALL_URL"]


def get_scryfall_cache_path() -> str:
    return os.environ["SCRYFALL_CACHE"]


def is_dev_mode() -> bool:
    return get_env() == "LOCAL"


def get_current_datetime() -> datetime.datetime:
    return datetime.datetime.now()
