.PHONY: all start

all: format check start

start:
	@poetry run start

format:
	@poetry run black mtg_rules_chatgpt_plugin
	@poetry run isort mtg_rules_chatgpt_plugin

check:
	@poetry run mypy --ignore-missing-imports mtg_rules_chatgpt_plugin

cards_db:
	@sqlite3 mtg_rules_chatgpt_plugin/data/db/cards/AllPrintings.sqlite
