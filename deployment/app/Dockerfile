ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION:-3.10}-slim-buster as prod

ENV POETRY_VERSION=1.1.8
RUN pip install "poetry==$POETRY_VERSION" "poetry-core==1.0.4" && poetry config virtualenvs.create false && \
   poetry config installer.parallel false

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_NO_CACHE_DIR=off
ENV PYTHONDONTWRITEBYTECODE=on
ENV PYTHONFAULTHANDLER=on
ENV PYTHONUNBUFFERED=on

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential nano curl \
    && rm -rf /var/lib/apt/lists/*

# Dependencies
ARG RUN_LEVEL=prod
ENV RUN_LEVEL=${RUN_LEVEL}
COPY pyproject.toml poetry.loc[k] /opt/app/
WORKDIR /opt/app
RUN poetry install $(if [ "${RUN_LEVEL}" = "prod" ]; then echo "--no-dev"; fi ) --no-root --no-interaction --no-ansi -vvv

# Application
COPY app ./app

ARG APP_PORT=8080
ENV APP_PORT=${APP_PORT}
ARG APP_PACKAGE=app
ENV APP_PACKAGE=${APP_PACKAGE}

CMD sh -c "uvicorn main:app --app-dir ${APP_PACKAGE} --host 0.0.0.0 --port ${APP_PORT}"


FROM prod as dev

# --- Development image ---

ARG USER_ID
ARG GROUP_ID

RUN addgroup --gid $GROUP_ID user
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user
USER user

RUN poetry config virtualenvs.create false

RUN echo "export PATH=\$PATH:~/.local/bin" > /home/user/.bashrc

ENV PYTHONPATH=$PYTHONPATH:/opt/app/app

CMD sh -c "uvicorn main:app --app-dir ${APP_PACKAGE} --host 0.0.0.0 --port ${APP_PORT} --reload"
