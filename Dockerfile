FROM python:3 as base
ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_NO_INTERACTION=1 \
  POETRY_VERSION=1.1.12 \
  PYSETUP_PATH="/opt/pysetup" \
  VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM base as requirements
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
  curl \
  build-essential

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

COPY ./poetry.lock ./pyproject.toml ./
RUN poetry export -f requirements.txt -o requirements.txt --without-hashes

FROM base as final

WORKDIR /app

COPY --from=requirements requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "-m", "minecraft_server_discord_status"]
