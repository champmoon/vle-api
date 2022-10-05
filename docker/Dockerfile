# Creating a python base with shared environment variables
FROM python:3.10-slim-bullseye AS python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" 


# Builder-base is used to build dependencies
FROM python-base AS builder-base
RUN buildDeps="build-essential" \
    && apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    vim \
    netcat \
    && apt-get install -y --no-install-recommends $buildDeps \
    && rm -rf /var/lib/apt/lists/*

# We copy our Python requirements here to cache them
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./

# 'development' stage installs all dev deps and can be used to develop code.
# For example using docker-compose to mount local volume under /app
FROM python-base as development
ENV FASTAPI_ENV=development

# Copying poetry and deps into image
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

WORKDIR $PYSETUP_PATH
ENV POETRY_VERSION=1.2.0

# Install poetry
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN pip install "poetry==$POETRY_VERSION"

# (https://github.com/python-poetry/poetry/issues/3219)
# If frequent intermittent connection failures, uncomment the following line 
# RUN poetry config installer.parallel false

# Install our project dependencies
RUN poetry install --no-root --only main  

# Copying in our entrypoint
COPY ./docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Copying project
WORKDIR /app
COPY . .

EXPOSE 8000
ENTRYPOINT /docker-entrypoint.sh $0 $@
CMD ["uvicorn", "--reload", "--host=0.0.0.0", "--port=8000", "app.main:app"]
