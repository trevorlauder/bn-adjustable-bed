ARG USER="bnab"
ARG BUILD="/tmp/bn_adjustable_bed"
ARG PIP="/venv/bin/pip"
ARG PYTHON="/venv/bin/python"

FROM python:3.9.7-slim AS base

ENV PIP_NO_CACHE_DIR=off \
    PYTHONDONTWRITEBYTECODE=1

RUN apt update && apt -y install curl && apt clean



FROM base AS dist

ARG BUILD

ENV POETRY_VERSION="1.1.11"
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

WORKDIR ${BUILD}

ENV PATH="/root/.local/bin:$PATH"

COPY poetry.lock pyproject.toml ${BUILD}/

RUN poetry export -f requirements.txt --output requirements.txt
RUN poetry export --dev --extras=test -f requirements.txt --output requirements-dev.txt

COPY src ${BUILD}/src
COPY README.md ${BUILD}/

RUN poetry build -f wheel



FROM base AS bn_adjustable_bed

ARG BUILD
ARG PIP
ARG PYTHON

WORKDIR ${BUILD}

RUN python -m venv /venv

RUN ${PYTHON} -m pip install --upgrade pip

COPY --from=dist ${BUILD}/requirements.txt requirements.txt

RUN ${PIP} install -r requirements.txt

COPY config /bn_adjustable_bed/config
COPY --from=dist ${BUILD}/dist dist

RUN ${PIP} install dist/*.whl



FROM base as final

ARG USER

RUN groupadd -r ${USER} && useradd --no-log-init -m -r -g ${USER} ${USER}

WORKDIR /bn_adjustable_bed

COPY --from=bn_adjustable_bed /venv /venv
COPY --from=bn_adjustable_bed /bn_adjustable_bed /bn_adjustable_bed

USER ${USER}


FROM dist as unittests

ARG BUILD
ARG PIP
ARG PYTHON

COPY --from=bn_adjustable_bed /venv /venv

RUN ${PIP} install -r requirements-dev.txt

COPY --from=bn_adjustable_bed /bn_adjustable_bed/config config
COPY .coveragerc .coveragerc
COPY tests tests

RUN /venv/bin/tox --installpkg dist/*.whl -e py39
