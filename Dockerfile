ARG USER="bnab"

FROM python:3.11.1-slim AS base

RUN apt update && apt -y full-upgrade && apt clean

ARG VENV_DIR="/venv"
ARG USER

RUN python -m venv ${VENV_DIR}
ENV PATH="${VENV_DIR}/bin:$PATH"
RUN python -m pip install --upgrade pip

RUN groupadd -r ${USER} && useradd --no-log-init -m -r -g ${USER} ${USER}

FROM base AS final

ARG GIT_TAG
ARG USER

RUN python -m pip install bn-adjustable-bed==${GIT_TAG}

USER ${USER}


FROM base AS dev

ARG USER

COPY dist dist
RUN python -m pip install dist/*.whl

USER ${USER}
