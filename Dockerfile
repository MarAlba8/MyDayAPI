FROM python:3.11-slim-bookworm

ENV PYTHONPATH="src"

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
