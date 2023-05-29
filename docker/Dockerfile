FROM python:3.10.11

RUN pip install -U pip && pip install poetry

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN POETRY_VIRTUALENVS_CREATE=false poetry install --no-dev --no-interaction --no-ansi

COPY . /code

CMD ["uvicorn", "mtg_rules_chatgpt_plugin.main:start", "--host", "0.0.0.0", "--port", "3000"]
