FROM python:3.9-slim-buster as python-base
ENV PYTHONBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PI_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# builder-base is used to build dependencies
FROM python-base as builder-base
RUN buildDeps="build-essential" \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        vim \
        netcat \
    && apt-get install -y --no-install-recommends $buildDeps \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
ENV POETRY_VERSION=1.1.5
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python && \
    chmod a+x /opt/poetry/bin/poetry

# We copy our Python requirements here to cache them
# and install only runtime deps using poetry
WORKDIR $PYSETUP_PATH
COPY ./pyproject.toml ./
ADD opentelemetry-python-contrib opentelemetry-python-contrib
RUN poetry install --no-dev  # respects


# 'development' stage installs all dev deps and can be used to develop code.
# For example using docker-compose to mount local volume under /app
FROM python-base as development
ENV FASTAPI_ENV=development
ENV PYTHONUNBUFFERED=1

# Copying poetry and venv into image
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# Copying in our entrypoint
COPY ./docker/docker-entrypoint.sh /docker-entrypoint.sh
COPY ./docker/start.sh /start.sh
RUN chmod +x /docker-entrypoint.sh

# venv already has runtime deps installed we get a quicker install
WORKDIR $PYSETUP_PATH

# RUN poetry add pathlib2
# RUN poetry remove pathlib2

RUN poetry install

WORKDIR /app
COPY . .

# DB start
#RUN python ./app/backend_pre_start.py


# Run migrations
#RUN alembic upgrade head

# Create initial data in DB
#RUN python ./app/initial_data.py

# RUN poetry show

EXPOSE 8009
#ENTRYPOINT /docker-entrypoint.sh $0 $@
CMD alembic upgrade head && uvicorn --log-level info --host=0.0.0.0 --port=8009 app.main:app 
#CMD [ "poetry", "run", "python", "app/main.py" ]
#CMD ["/start.sh"]