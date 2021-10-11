FROM python:3.10.0-slim AS base

ENV PIP_NO_CACHE_DIR=off \
    PYTHONDONTWRITEBYTECODE=1

FROM base as poetry

RUN python -m pip install poetry~=1.1


FROM poetry AS build

COPY pyproject.toml poetry.lock /

RUN python -m venv .venv
RUN poetry install --no-root --no-dev

COPY bed_socket/ /bed_socket/


FROM build AS unittests

RUN poetry install

COPY tests/ /tests/

RUN .venv/bin/pytest tests/


FROM base AS final

COPY --from=build .venv .venv
COPY --from=build bed_socket bed_socket

WORKDIR /bed_socket

ENTRYPOINT ["../.venv/bin/python"]

CMD [ "-u", "./run.py" ]
