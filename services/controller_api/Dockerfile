FROM python:3.9.5-slim AS build

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY *.py /
COPY config/*.* config/

CMD [ "python", "-u", "./run.py" ]


FROM build AS unittests

COPY tests/requirements.txt tests/

RUN pip install --no-cache-dir -r tests/requirements.txt

COPY tests/*.py tests/
COPY tests/config/*.* tests/config/

RUN pytest tests/
