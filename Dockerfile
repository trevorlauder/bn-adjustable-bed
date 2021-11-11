ARG USER="bnab"
ARG BUILD="/tmp/bn_adjustable_bed"
ARG VENV="/venv"
ARG PIP="${VENV}/bin/pip"
ARG PYTHON="${VENV}/bin/python"

FROM python:3.10.0-slim AS base

ENV PIP_NO_CACHE_DIR=off \
    PYTHONDONTWRITEBYTECODE=1

RUN apt update && apt -y install curl && apt clean



FROM base AS dist

ARG BUILD

RUN python -m pip install poetry==1.1.11

WORKDIR ${BUILD}

COPY poetry.lock pyproject.toml ${BUILD}/

RUN poetry export -f requirements.txt --output requirements.txt
RUN poetry export --dev --extras=test -f requirements.txt --output requirements-dev.txt

COPY src ${BUILD}/src
COPY README.md ${BUILD}/

RUN poetry version $(git describe --tags --abbrev=0)
RUN poetry build -f wheel



FROM base AS bn_adjustable_bed

ARG BUILD
ARG PIP
ARG PYTHON
ARG VENV

WORKDIR ${BUILD}

RUN python -m venv ${VENV}

RUN ${PYTHON} -m pip install --upgrade pip

COPY --from=dist ${BUILD}/requirements.txt requirements.txt

RUN ${PIP} install -r requirements.txt

COPY config /bn_adjustable_bed/config
COPY --from=dist ${BUILD}/dist dist

RUN ${PIP} install dist/*.whl



FROM base as final

ARG USER
ARG VENV

RUN groupadd -r ${USER} && useradd --no-log-init -m -r -g ${USER} ${USER}

WORKDIR /bn_adjustable_bed

COPY --from=bn_adjustable_bed ${VENV} ${VENV}
COPY --from=bn_adjustable_bed /bn_adjustable_bed /bn_adjustable_bed

USER ${USER}

ENV PATH="${VENV}/bin:$PATH"
