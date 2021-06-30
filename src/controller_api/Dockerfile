FROM python:3.9.5-slim AS build

COPY Pipfile Pipfile.lock ./

RUN python -m pip install pipenv
RUN pipenv install --deploy --ignore-pipfile

COPY *.py /
COPY config/*.* config/

ENTRYPOINT ["pipenv"]
CMD [ "run", "python", "-u", "./run.py" ]


FROM build AS unittests

RUN pipenv install --deploy --dev --ignore-pipfile

COPY tests/*.py tests/
COPY tests/config/*.* tests/config/

RUN pipenv run pytest tests/
