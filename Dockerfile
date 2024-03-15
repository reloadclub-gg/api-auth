FROM python:3.12

ENV PYTHONUNBUFFERED=1
ENV TZ="America/Sao_Paulo"

ARG DEVPI_HOST
ARG DEVPI_USER
ARG DEVPI_PASSWORD
ARG WORKDIR=/project

WORKDIR ${WORKDIR}
COPY Pipfile Pipfile.lock .flake8 pyproject.toml ${WORKDIR}
COPY ./app ${WORKDIR}/app

RUN apt update

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --dev --system --deploy

RUN pip install devpi-client
RUN devpi use $DEVPI_HOST
RUN devpi login $DEVPI_USER --password=$DEVPI_PASSWORD

EXPOSE 9000

ENTRYPOINT ["pipenv", "run"]
CMD ["start"]
