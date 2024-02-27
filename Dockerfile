FROM python:3.12

ENV PYTHONUNBUFFERED=1
ENV TZ="America/Sao_Paulo"

ARG DEVPI_HOST
ARG DEVPI_USER
ARG DEVPI_PASSWORD
ARG WORKDIR=/app

WORKDIR $WORKDIR

RUN apt update && apt install -y gettext
RUN pip install --upgrade pip pipenv
RUN pip install devpi-client
RUN devpi use $DEVPI_HOST
RUN devpi login $DEVPI_USER --password=$DEVPI_PASSWORD

COPY Pipfile Pipfile.lock $WORKDIR/

RUN pipenv install --deploy

ENTRYPOINT [ "pipenv", "run" ]
