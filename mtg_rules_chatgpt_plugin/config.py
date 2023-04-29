import os


def get_host():
    return os.environ["HOST"]


def get_port():
    return int(os.environ["PORT"])


def get_env():
    return os.environ["ENV"]


def get_cards_db_path():
    return os.environ["CARDS_DB"]


def get_cards_vs_path():
    return os.environ["CARDS_VS"]


def get_rules_csv_path():
    return os.environ["RULES_CSV"]


def get_rules_vs_path():
    return os.environ["RULES_VS"]


def is_dev_mode():
    return get_env() == "LOCAL"
