# reload-be-auth

This repo contains all logic for reload authentication.

## Requirements

- Docker & docker-compose
- Python (3.10+) and pip

## Prepare

You will need to have a user on `reload-devpi` server. If you don't have one, ask your manager to create. Also, make a copy of `.env.tmpl` named `.env` and replace all aplicable envs.

### Install and configute reload-devpi server for private libs

1. `pip install devpi-client`
2. `devpi use http://devpi.reloadclub.gg:3141/root/reload`
3. `devpi login USERNAME --password=PASSWORD`

## Usage

- Run `make up` to build and launch the containerized services
- Use `./pipenv-run COMMAND` to run container commands and `Pipfile` scripts
- Run `make down` to stop and remove the containerized services

### Other make functions

- `make halt` will stop the containers but WILL NOT remove volumes
- `make reset` will run a `make down` and a `make up` but WILL build the docker image again
- `make refresh` is a shortcut for `make down` and `make up`

### Installing libs

To install libs, you need to run `pipenv install LIBRARY` and then run `make reset` so the app is rebuilt with the installed lib.
