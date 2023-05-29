FROM python:3.10.11

ENV HOST="0.0.0.0"
ENV PORT="8080"

RUN pip install -U pip && pip install poetry

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN POETRY_VIRTUALENVS_CREATE=false poetry install --no-dev --no-interaction --no-ansi

COPY . /code

CMD uvicorn mtg_rules_chatgpt_plugin.main:app --host ${HOST} --port ${PORT}
