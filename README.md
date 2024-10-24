# reload-be-auth

This repo contains all logic for reload authentication. It exposes documentation about all endpoints and schemas at `/docs` and `/redoc`.

## Requirements

- Docker & docker-compose
- Python (3.10+) and pip

## Prepare

You will need to accomplish 2 steps before running this project:

1. Have a user on `reload-devpi` server and set the following envs on your terminal: `DEVPI_HOST`, `DEVPI_USER` and `DEVPI_PASSWORD`. If you don't have a `devpi` user, ask your manager to create one for you alongside the envvars.
2. Also, make a copy of `.env.tmpl` named `.env` and replace all aplicable envs.

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

### Docker image

You can build and run the standalone docker image, but keep in mind that some stuff will not work well due to other images/services dependecies, like Redis. You'll get a better result using the docker-file and the instructions above.

**_ONLY DO THIS IF YOU KNOW WHAT YOU'RE DOING!_**

```bash
docker build -t api-auth \
  --build-arg="DEVPI_HOST=http://devpi.reloadclub.gg:3141/root/reload" \
  --build-arg="DEVPI_USER=YOUR_DEVPI_USER" \
  --build-arg="DEVPI_PASSWORD=YOUR_DEVPI_PASS" \
  .

# then run the image
docker run --rm --env SECRET_KEY=PLACE_A_SECRET_KEY -p 9000:9000 -v ./app:/project/app api-auth

# or with a specific command
docker run --rm api-auth lint
```
