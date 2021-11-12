FROM python:3.10.0-slim AS final

ARG GIT_TAG
ARG USER="bnab"
ARG VENV="/venv"
ARG PIP="${VENV}/bin/pip"
ARG PYTHON="${VENV}/bin/python"

RUN apt update && apt -y full-upgrade && apt clean

RUN python -m venv ${VENV}

RUN ${PYTHON} -m pip install --upgrade pip
RUN ${PYTHON} -m pip install bn-adjustable-bed==${GIT_TAG}

RUN groupadd -r ${USER} && useradd --no-log-init -m -r -g ${USER} ${USER}

USER ${USER}

ENV PATH="${VENV}/bin:$PATH"
