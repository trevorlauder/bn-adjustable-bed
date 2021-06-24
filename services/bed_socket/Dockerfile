FROM python:3.9.5-slim AS build

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY *.py /
COPY config/*.* config/

CMD [ "python", "-u", "./run.py" ]
