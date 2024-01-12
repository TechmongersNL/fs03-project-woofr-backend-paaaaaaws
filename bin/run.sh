#!/usr/bin/env bash

# This script is used to run the application in a production environment.

set -e

# Run migrations
pipenv run alembic upgrade head

# Run the application
pipenv run uvicorn main:app --host 0.0.0.0 --port $PORT
