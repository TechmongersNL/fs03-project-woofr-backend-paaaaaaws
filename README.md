# Woofr Backend

This is the backend to a full stack project for class FS03.

## Setup

Set up your virtual env.

```shell
$ python -m venv .venv
# then activate it
$ source .venv/bin/activate
```

Install dependencies

```shell
$ pip install pipenv
$ pipenv install # to install the deps in Pipfile
```

### Database

Set up a database using Docker

```shell
$ docker run --name woofrdb -d -p 5445:5432 -e POSTGRES_PASSWORD=secret postgres
```

Then, create a `.env` file in the root of the project, and add:

```shell
DATABASE_URL=postgresql://postgres:secret@localhost:5445/postgres
```
