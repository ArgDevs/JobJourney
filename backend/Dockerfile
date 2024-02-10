FROM python:3.12-slim-bookworm
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_HOME="/usr/local" \
  POETRY_VIRTUALENVS_IN_PROJECT=false \
  POETRY_NO_INTERACTION=1 \
  PYSETUP_PATH="/opt/pysetup" \
  VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install poetry
RUN apt-get update && apt-get install --no-install-recommends -y curl build-essential binutils  \
    curl libpq-dev make gcc postgresql-client procps && curl -sSL https://install.python-poetry.org | python3 -

# Ensure poetry is in PATH explicitly for this layer
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app
COPY ./src .
COPY ./poetry.lock ./pyproject.toml ./entrypoint.sh ./

RUN poetry export --only=main --output requirements.txt --without-hashes && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["/app/entrypoint.sh"]
